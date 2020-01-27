from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user
from flask import request, jsonify, make_response
from .models import Book
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route("/datas/create_entry", methods=["GET", "POST"])
@login_required
def create_entry():
    books = None
    message = None
    if request.form:
        try:
            title = request.form.get("title")
            content = request.form.get("content")
            old_book = Book.query.filter_by(title=title).first()
            if old_book:
                flash('Book is already exists')
                return render_template("books.html", name=current_user.name)
            new_book = Book(title=title, content=content)
            db.session.add(new_book)
            db.session.commit()
            message = "Submitted Successfully"
        except Exception as e:
            db.session.rollback()
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("books.html", books=books, name=current_user.name, message= message)

@main.route('/datas/book_details', methods=["GET", "POST"])
@login_required
def datas():
    books = None
    if request.form:
        title = request.form.get("title")
        book = Book.query.filter_by(title=title).first()
        if book:
            books = Book.query.filter_by(title=title)
    return render_template('book_details.html', name=current_user.name,books=books)

@main.route("/datas/update", methods=["POST"])
def update():
    try:
        title = request.form.get("title")
        newcontent = request.form.get("newcontent")
        oldcontent = request.form.get("oldcontent")
        book = Book.query.filter_by(title=title).first()
        book.content = newcontent
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/datas/book_details")