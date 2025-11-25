import os
import dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import date

# Load variables from the local .env file
dotenv.load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'default-fallback-key-for-testing')

db.init_app(app)

# ------ Routes ------


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """ Handles adding a new author to the database.

    GET: Renders the 'add_author.html' form.
    POST: Processes form data, validates/converts date fields,
          creates a new Author object, commits it to the database,
          flashes a success message, and redirects.
    """
    if request.method == 'GET':
        return render_template('add_author.html')

    elif request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        birth_date = date.fromisoformat(
            birth_date_str) if birth_date_str else None
        date_of_death = date.fromisoformat(
            date_of_death_str) if date_of_death_str else None

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()

        flash(f"Author '{name}' successfully added to the library!")
        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """ Handles adding a new book to the database.

    GET: Queries all existing authors, renders the 'add_book.html' form,
         and passes the authors list to populate the dropdown.
    POST: Processes form data (title, ISBN, year, author_id),
          creates a new Book object, commits it to the database,
          flashes a success message, and redirects.
    """
    authors = db.session.execute(db.select(Author)).scalars().all()

    if request.method == 'GET':
        return render_template('add_book.html', authors=authors)

    elif request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id
        )

        db.session.add(new_book)
        db.session.commit()

        flash(f"Book '{title}' successfully added to the library!")
        return redirect(url_for('add_book'))


@app.route('/')
def home():
    """ Handles the main library display page.

    Retrieves optional 'sort' and 'search_term' query parameters.
    Queries the Book table (applying filters/joins/ordering as needed).
    Renders the 'home.html' template, passing the filtered/sorted list of books.
    """
    sort_by = request.args.get('sort')
    search_term = request.args.get('search_term')

    query = db.select(Book)

    if search_term:
        search_pattern = f"%{search_term}%"
        query = query.filter(
            (Book.title.ilike(search_pattern)) |
            (Book.isbn.ilike(search_pattern))
        )

    if sort_by == 'title':
        query = query.order_by(Book.title)

    elif sort_by == 'author':
        query = query.join(Book.author).order_by(Author.name)

    all_books = db.session.execute(query).scalars().all()

    message = None
    if search_term and not all_books:
        message = f"No books found matching '{search_term}'. Showing all books instead."

    elif search_term and all_books:
        message = f"Found {len(all_books)} book(s) matching '{search_term}'."

    return render_template('home.html', books=all_books, search_message=message)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """ Handles deletion of a specific book by ID.
    Also checks if the author has any remaining books; if not, deletes the author too.
    """
    book_to_delete = db.session.get(Book, book_id)

    if not book_to_delete:
        flash("Error: Book not found.", 'error')
        return redirect(url_for('home'))

    author_id = book_to_delete.author_id
    book_title = book_to_delete.title

    db.session.delete(book_to_delete)

    remaining_books = db.session.execute(
        db.select(Book).filter_by(author_id=author_id)
    ).scalars().all()

    if not remaining_books:
        author_to_delete = db.session.get(Author, author_id)
        if author_to_delete:
            author_name = author_to_delete.name
            db.session.delete(author_to_delete)
            flash_message = f"Book '{book_title}' deleted. Author '{author_name}' deleted as they have no remaining books."
        else:
            flash_message = f"Book '{book_title}' deleted."
    else:
        flash_message = f"Book '{book_title}' deleted."

    db.session.commit()

    flash(flash_message)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

# with app.app_context():
#    db.create_all()
#    print("Database tables created successfully.")
