# Search App

This is a search engine application that returns photos and videos based on search requirements.

## Frontend

The frontend of this application is built using HTML, CSS, and Jinga a template. It provides a user-friendly interface for searching and displaying the results.

Run the flask server (See backend), and find the Search engine at http://localhost:5000/

Type your search query into the search box to get results.

Click on the photo/video name to go the source for the media.

Clicking the title will reset the search.

## Backend

The backend of this application is built using Python and Flask. It handles the search requests, retrieves the matching photos and videos from a database, and sends the results back to the frontend.

To run the backend, follow these steps:

1. Install Python on your machine. (Using Python 3.12.3 for this project)
2. Install the required dependencies by running the following command in your terminal:
   ```
   pip install -r requirements.txt
   ```
3. Set your youtube API key within your bash terminal
   ```
   export YOUTUBE_API_KEY={YOUR_API_KEY}
   ```
4. Start the Flask development server by running the following command in your terminal:
   ```
   python app.py
   ```

The backend server should now be running at `http://localhost:5000`.

Photo:
`http://localhost:5000/photos/dog?num_of_photos=3` will get you a 3 random photos of dogs.

Videos:
`http://localhost:5000/videos/dog` will get you videos of dogs from youtube. (Default of 5 from youtube API)
