import random
import os
import requests
import googleapiclient.discovery
import googleapiclient.errors
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
name = "Search App"

@app.route('/')
def search_engine():
    """
    Renders the home page of the search app.

    Returns:
        The rendered template of the search.html page.
    """
    search_term = request.args.get("input", "")
    image_response = requests.get(f"http://127.0.0.1:5000/photos/{search_term}?num_of_photos=1")
    video_response = requests.get(f"http://127.0.0.1:5000/videos/{search_term}")
    
    image = image_response.json()[0] if image_response.status_code == 200 and len(image_response.json()) > 0 else None
    video = video_response.json()[0] if video_response.status_code == 200 and len(video_response.json()) > 0 else None

    return render_template('index.html', name=name, photo=image, video=video, search_term=search_term)

@app.route("/photos/<string:search_term>", methods=["GET"])
def get_photos(search_term: str):
    """
    Retrieves photos related to the given search term.

    Args:
        search_term (str): The search term for photos.

    Returns:
        The JSON response containing the retrieved photos.

    Query Parameters:
        num_of_photos (int, optional): The number of photos to retrieve. Defaults to 1.

    Raises:
        ValueError: If the value of num_of_photos is not a valid integer.

    """
    try:
        num_of_photos = min(int(request.args.get("num_of_photos", default=1)), 3)
    except ValueError:
        num_of_photos = 1
    response = requests.get(f"https://www.flickr.com/services/feeds/photos_public.gne?format=json&tags={search_term}&nojsoncallback=1")

    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve photos"}), 500  # Return 500 Internal Server Error
    
    photos = response.json()["items"]
    
    if not photos:
        return jsonify([])
    
    # Randomly select num_of_photos from photos
    photos = [photos[i] for i in random.sample(range(0, len(photos)), num_of_photos)]
    return jsonify(photos)


@app.route("/videos/<string:search_term>", methods=["GET"])
def get_videos(search_term: str):
    """
    Retrieves videos related to the given search term.

    Args:
        search_term (str): The search term for videos.

    Returns:
        The JSON response containing the retrieved videos.
    """
    response = youtube_search(search_term)
    if response is None or "items" not in response:
        return jsonify({"error": "Bad response"}), 500  # Return 500 Internal Server Error
    videos = response["items"]
    return jsonify(videos)


def youtube_search(search_term: str):
    """
    Searches for videos on YouTube using the YouTube Data API.

    Args:
        search_term (str): The search term for videos.

    Returns:
        The response containing the retrieved videos.
    """
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = app.config["YOUTUBE_API_KEY"]
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Setting to get embeddable videos that are short
    request = youtube.search().list(
        part="snippet",
        eventType="completed",
        q=search_term,
        type="video",
        videoDuration="short",
        videoEmbeddable="true",
    )

    try:
        response = request.execute()
        return response
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    app.config["YOUTUBE_API_KEY"] = os.environ.get("YOUTUBE_API_KEY")
    app.run(port=5000, debug=True)
