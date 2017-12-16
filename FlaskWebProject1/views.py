"""
Routes and views for the flask application.
"""
from collections import namedtuple
from datetime import datetime
from flask import render_template, request
from FlaskWebProject1 import app
from threading import Timer
from werkzeug.utils import redirect

FeedbackInfo = namedtuple("FeedbackInfo", "sender date text")

FEEDBACK_STORAGE = {"comments": [],
                    "news": [],
                    "contact": []}
LAST_VISITED_IP = set()


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


@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == 'POST':
        ip_from = request.remote_addr
        if request.remote_addr in LAST_VISITED_IP:
            return redirect(request.full_path)
        LAST_VISITED_IP.add(ip_from)
        Timer(10, lambda: LAST_VISITED_IP.remove(ip_from)).start()
        record = FeedbackInfo(request.form['nickname'], datetime.now(),
                              request.form['text_area'])
        FEEDBACK_STORAGE[request.args["from"]].append(record)
        return redirect(request.full_path)
    return render_template("comments.html",
                           data=FEEDBACK_STORAGE[request.args["from"]])
