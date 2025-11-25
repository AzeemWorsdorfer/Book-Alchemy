from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)
    
    def __repr__(self):
        return f"<Author {self.name}>"
    
    def __str__(self):
        return f"{self.name} (ID: {self.id})"   