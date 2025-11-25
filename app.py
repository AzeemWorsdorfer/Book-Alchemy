import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import date

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

#------ Routes ------

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """ Route to add author
    """
    if request.method == 'GET':
        return render_template('add_author.html')
    
    elif request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')
        
        birth_date = date.fromisoformat(birth_date_str) if birth_date_str else None
        date_of_death = date.fromisoformat(date_of_death_str) if date_of_death_str else None
        
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )
        
        with app.app_context():
            db.session.add(new_author)
            db.session.commit()
            
        flash(f"Author '{name}' successfully added to the library!")
        return redirect(url_for('add_author.html'))
    
    return render_template('add_author.html')


    





# with app.app_context():
#    db.create_all()
#    print("Database tables created successfully.")
