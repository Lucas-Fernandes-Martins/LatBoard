from flask import Flask, redirect, url_for, render_template, request, session, jsonify

import google_auth

import json

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = "12345678910"

app.register_blueprint(google_auth.app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class board(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    content = db.Column(db.String(1000))

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

@app.route("/login")
def login():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        found = users.query.filter_by(email=user_info["email"]).first()
        if found is None:
            usr = users(user_info["given_name"], user_info["email"])
            db.session.add(usr)
            db.session.commit()
    return redirect(url_for("main"))

@app.route("/backup")
def backup():
    return render_template("static.html")

@app.route("/login_screen")
def login_screen():
    return render_template("login.html")

@app.route("/")
def main():
    logged = 0
    if google_auth.is_logged_in():
        logged = 1
        user_info = google_auth.get_user_info()
    else:
        user_info = None

    return render_template("index.html", user_info=user_info, logged=logged)


