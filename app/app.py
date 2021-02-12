from flask import Flask, redirect, url_for, render_template, request, session, jsonify

import google_auth

import json

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = "12345678910"

app.register_blueprint(google_auth.app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

app.config['SQLALCHEMY_BINDS'] = {
    'boards':'sqlite:///boards.sqlite3'}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class boards(db.Model):
    __bind_key__ = 'boards'
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    content = db.Column(db.String(1000))

    def __init__(self, title, author, user_id, content):
        self.title = title
        self.author = author
        self.user_id = user_id
        self.content = content

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/table")
def table():
    usr = users.query.all()

    return render_template("users.html", values=usr)

@app.route("/boards")
def table_boards():
    values = boards.query.all()

    return render_template("boards.html", values=values)

@app.route("/login")
def login():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        found = users.query.filter_by(email=user_info["email"]).first()
        session["user_id"] = user_info["email"]
        session["user_name"] = user_info["given_name"]
        if found is None:
            usr = users(user_info["given_name"], user_info["email"])
            db.session.add(usr)
            db.session.commit()
    else:
        session.pop("user_id", None)
        session.pop("user_name", None)
    return redirect(url_for("main"))

@app.route("/backup")
def backup():
    return render_template("static.html")

@app.route("/login_screen")
def login_screen():
    return render_template("login.html")

@app.route("/update", methods=['POST', 'GET'])
def update():
    content = request.json
    board = boards(content["title"], session["user_name"], session["user_id"], content["content"])
    db.session.add(board)
    db.session.commit()

    return redirect(url_for("main"))

@app.route("/", methods=['POST', 'GET'])
def main():
    logged = 0
    if google_auth.is_logged_in():
        logged = 1
        user_info = google_auth.get_user_info()
    else:
        user_info = None

    if request.method == 'POST':
        title = request.form["title"]
        board = boards(title, session["user_name"], session["user_id"], "people")
        db.session.add(board)
        db.session.commit()



    return render_template("index.html", user_info=user_info, logged=logged)


