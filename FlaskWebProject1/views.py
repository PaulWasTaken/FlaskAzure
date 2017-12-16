"""
Routes and views for the flask application.
"""

from flask import render_template
from FlaskWebProject1 import app


@app.route("/")
@app.route("/base")
def home():
    return render_template("base.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/news")
def news():
    return render_template("news.html")
