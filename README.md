# Real Estate API

## Sets up a web application using Flask for managing real estate listings. Here’s a breakdown of what it does:

### Imports and Configuration:
Imports necessary libraries and modules.
Configures the Flask app, including secret key, database URI, and upload folder settings.
###Database Setup:
Connects to a SQLite database named listings.db.
Defines a Listings model for storing real estate listings with fields like address, type, rooms, baths, link, description, price, and image URL.
Creates the database table if it doesn’t exist.
###Form Setup:
Defines a CreateListingForm using Flask-WTF for adding new listings. The form includes fields for address, type, rooms, baths, description, link, price, and image.
Helper Functions:
bad_request(message): Returns a JSON response with a 400 status code.
allowed_file(filename): Checks if the uploaded file has an allowed extension.
### Routes:
/: Displays all listings.
/add: Handles the form for adding new listings. Validates the form, saves the image, and adds the listing to the database.
/listing/<int:listing_id>: Displays a specific listing based on its ID.
### Running the App:

This setup allows users to view, add, and manage real estate listings through a web interface. If you have any specific questions about parts of the code, feel free to ask!
