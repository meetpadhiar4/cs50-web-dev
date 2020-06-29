import os

from flask import Flask, session, render_template, request, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(
    os.getenv("DATABASE_URL"))

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if not name and not password:
            return render_template("error.html", message="Please enter your username and password.")
        elif not name:
            return render_template("error.html", message="Please enter your username.")
        elif not password:
            return render_template("error.html", message="Please enter your password.")
        result = db.execute(
            "SELECT * FROM users WHERE name = :name", {"name": name})
        cred = result.fetchone()
        if cred == None or cred[1] != password:
            return render_template("error.html", message="Incorrect username or password.")
        session["user_id"] = cred[0]
        return redirect("/home")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        temp = db.execute(
            "SELECT * FROM users WHERE name = :name", {"name": name}).fetchone()
        if temp:
            return render_template("error.html", message="This username already exists. Please enter another username.")
        if not name and not password:
            return render_template("error.html", message="Please enter your username and password.")
        elif not name:
            return render_template("error.html", message="Please enter your username.")
        elif not password:
            return render_template("error.html", message="Please enter your password.")

        db.execute("INSERT INTO users(name, password) VALUES(:name, :password)",
                   {"name": name, "password": password})
        db.commit()
        flash('You are registered', 'info')
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/logout")
# @login_required
def logout():
    session.clear()
    return redirect("/")


@app.route("/home", methods=["GET", "POST"])
# @login_required
def home():
    return render_template("home.html")


@app.route("/search", methods=["POST"])
# @login_required
def search():
    data = request.form.get("input")
    if not data:
        return render_template("error.html", message="Please provide an input.")
    else:
        data = "%" + data + "%"
        data = data.title()
        result = db.execute(
            "SELECT * FROM books WHERE isbn LIKE :data OR title LIKE :data OR author LIKE :data LIMIT 15", {"data": data})
        if result.rowcount == 0:
            return render_template("error.html", message="The book that you are looking for is not available")
        books = result.fetchall()
        return render_template("results.html", books=books)


@app.route("/book/<isbn>", methods=["GET", "POST"])
# @login_required
def book(isbn):
    if request.method == "POST":
        currentUser = session['user_id']
        data = db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
        data2 = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND isbn = :isbn",
                           {"user_id": currentUser, "isbn": isbn})
        if data2.rowcount == 1:
            flash('You have already given a review for the book', 'info')
            return redirect("/book/" + isbn)
        bookInfo = data.fetchone()
        rating = request.form.get("rating")
        text = request.form.get("text")
        db.execute("INSERT INTO reviews (user_id, rating, text, isbn) VALUES (:user_id, :rating, :text, :isbn)", {
                   "user_id": currentUser, "rating": rating, "text": text, "isbn": isbn})
        db.commit()
        flash('Review submitted', 'info')
        return redirect("/book/" + isbn)
    else:
        data = db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
        bookInfo = data.fetchone()
        review = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": bookInfo[0]})
        temp = review.fetchall()
        return render_template("book.html", isbn=bookInfo[1], reviews=temp)
