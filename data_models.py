from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

# Model Definitions
class Author(db.Model):
    """Represents an Author in the digital library.

    The primary key is 'id'. The relationship to the 'Book' model includes
    a cascading delete rule, ensuring that when an Author is deleted, all 
    associated Book records are also removed from the database.
    """
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    books = db.relationship('Book', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Author {self.name}>'

class Book(db.Model):
    """
    Represents a Book in the digital library.
    Books are linked to Authors via a Foreign Key relationship.
    """
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'