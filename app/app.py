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

@app.route("/boards_user")
def boards_user():
    content = boards.query.filter_by(user_id=session["user_id"]).all()
    data = list()
    for i in range(len(content)):
        dic = dict()
        dic["id"] = i
        dic["title"] = content[i].title
        dic["content"] = content[i].content
        data.append(dic)
    
    return render_template("boards_user.html", values=json.dumps(data))

@app.route("/table_boards")
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
        session.pop("title", None)
        session.pop("content", None)
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
    exists = boards.query.filter_by(title=content["title"]).first()
    if exists is None:
        db.session.add(board)
        db.session.commit()
    else:
        exists.content = content["content"]
        db.session.commit()

    return redirect(url_for("main"))

@app.route("/resume", methods=['POST', 'GET'])
def resume():
    data = request.json

    title = data["title"]

    content = data["content"]

    print(title)

    print(content)

    session["title"] = title

    session["content"] = content

    return redirect(url_for("boards_user"))

@app.route("/", methods=['POST', 'GET'])
def main():
    logged = 0
    given_name = None
    title = None
    content = [
      { "id": 0, "text": '' },
      { "id": 1, "text": '' },
      { "id": 2, "text": '' }
    ]
    if "user_name" in session:
        logged = 1
        given_name = session["user_name"]

    if "title" in session:
        title = session["title"]
        content = session["content"]

    return render_template("index.html", given_name = given_name, logged=logged, title=title, content=json.dumps(content))



