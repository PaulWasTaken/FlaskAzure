"""
Routes and views for the flask application.
"""
from collections import namedtuple
from datetime import datetime
from flask import render_template, request
from FlaskWebProject1 import app
from FlaskWebProject1.ip_workers import IpTracker, IpStorage
from threading import Timer
from werkzeug.utils import redirect

FeedbackInfo = namedtuple("FeedbackInfo", "sender date text")

FEEDBACK_STORAGE = {"comments": [],
                    "news": [],
                    "contact": []}

ip_storage = IpStorage()
ip_tracker = IpTracker()


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
    ip_from = request.remote_addr
    if ip_from not in ip_tracker.last_visited_ip:
        ip_tracker.track_ip(ip_from, posted=False)
        ip_storage.update(ip_from not in ip_tracker.unique_ips)
        ip_tracker.update_unique(ip_from)

    if request.method == 'POST':
        if ip_from not in ip_tracker.last_posted_ip and request.form['text_area']:
            ip_tracker.track_ip(ip_from, posted=True)
            nickname = request.form['nickname']
            if not nickname:
                nickname = 'Anonymous'
            record = FeedbackInfo(nickname, datetime.now(),
                                  request.form['text_area'])
            FEEDBACK_STORAGE[request.args["from"]].append(record)
        return redirect(request.full_path)

    return render_template("comments.html",
                           data=FEEDBACK_STORAGE[request.args["from"]],
                           visit_info=ip_storage.get_stats())
