from flask import Flask, request, render_template, redirect, flash, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, DataError
from models import Author, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  

db = SQLAlchemy(app)
migrate = Migrate(app, db)


db.init_app(app)


@app.route('/')
def index():
    return 'Validations lab'

@app.route('/authors', methods=['GET', 'POST'])
def authors():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone_number = request.form['phone_number']
            author = Author(name=name, phone_number=phone_number)
            db.session.add(author)
            db.session.commit()
            flash('Author added successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Author with the same name already exists', 'danger')
        except DataError:
            db.session.rollback()
            flash('Invalid phone number (must be 10 digits)', 'danger')

    authors = Author.query.all()
    return render_template('authors.html', authors=authors)

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            summary = request.form['summary']
            category = request.form['category']
            
            post = Post(title=title, content=content, summary=summary, category=category)
            db.session.add(post)
            db.session.commit()
            flash('Post added successfully', 'success')
        except DataError:
            db.session.rollback()
            flash('Invalid input data', 'danger')
        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'danger')

    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
