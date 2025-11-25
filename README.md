📚 Book Alchemy Library

Book Alchemy is a simple, secure, and user-friendly web application for managing a digital library collection. Built with Flask and SQLAlchemy, it allows users to track authors and the books they've published, including features for searching, sorting, and maintaining data integrity through cascading deletes.

✨ Features

Create Authors and Books: Add new records via dedicated forms (/add_author, /add_book).

Search and Sort: Filter the main library view by title or ISBN, and sort the list by Book Title or Author Name.

Secure Session Management: Uses a secret key loaded from environment variables to secure user sessions and flash messages.

Data Integrity:

Delete Book: Remove individual books. If a deleted book was the author's last work, the author is also automatically removed.

Delete Author: Remove an author, which automatically deletes all associated books (cascading delete).

🚀 Setup and Installation

Follow these steps to get the Book Alchemy application running locally on your machine.

1. Prerequisites

You will need Python 3.8+ installed.

2. Clone the Repository

git clone [YOUR_REPOSITORY_URL_HERE]
cd Book-Alchemy


3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies:

python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# .\venv\Scripts\activate   # On Windows (CMD)



4. Install Dependencies

Install all required packages (Flask, SQLAlchemy, python-dotenv):

pip install -r requirements.txt



(If you haven't created a requirements.txt, run: pip freeze > requirements.txt)

5. Configure the Secret Key

For security, the application loads its session secret key from an environment variable.

Create a file named .env in the root directory of the project.

Add a strong, random string for the SECRET_KEY:

SECRET_KEY='your_long_and_very_secret_key_here_a1b2c3d4e5'



6. Initialize the Database

The application uses a SQLite database (data/library.sqlite). You need to initialize the tables by uncommenting the setup code at the bottom of app.py and running the file once, or by running this command:

python -c "from app import app, db; with app.app_context(): db.create_all(); print('Database tables created successfully.')"



7. Run the Application

Start the Flask development server:

flask run



The application will typically be available at http://127.0.0.1:5000/.

📌 Usage

Route

Method

Description

/

GET

Main Library view. Displays all books, search bar, and sorting options.

/add_author

GET/POST

Form to create a new author record.

/add_book

GET/POST

Form to create a new book, linking it to an existing author.

/book/<id>/delete

POST

Deletes a specific book.

/author/<id>/delete

POST

Deletes an author and all their associated books.

👩‍💻 Built With

Flask - The web framework used.

Flask-SQLAlchemy - ORM for interacting with the database.

python-dotenv - For secure handling of environment variables.

SQLite - Database engine.