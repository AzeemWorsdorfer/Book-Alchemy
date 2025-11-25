from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """ Represents an author in the library.

    Attributes:
        id (int): A unique, auto-incrementing primary key.
        name (str): The full name of the author (required).
        birth_date (date): The author's date of birth.
        date_of_death (date): The author's date of death (if applicable)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Book(db.Model):
    """ Represents a book in the library.

    Attributes:
        id (int): A unique, auto-incrementing primary key.
        isbn (str): The International Standard Book Number (unique and required).
        title (str): The title of the book (required).
        publication_year (int): The year the book was published.
        author_id (int): Foreign Key linking the book to its author's id.
        author (relationship): A dynamic attribute to access the associated Author object
    """
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    publication_year = db.Column(db.Integer)

    # Foreign Key Setup
    author_id = db.Column(db.Integer, db.ForeignKey(
        'author.id'), nullable=False)

    # Defines a relationship for easy access
    author = db.relationship('Author', backref='books')

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return f"{self.title} (ISBN: {self.isbn})"
