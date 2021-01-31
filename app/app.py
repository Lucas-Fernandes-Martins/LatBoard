from flask import Flask, redirect, url_for, render_template, request, session, jsonify

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

