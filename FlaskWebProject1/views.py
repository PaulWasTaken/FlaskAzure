"""
Routes and views for the flask application.
"""
from collections import namedtuple
from datetime import datetime
from flask import render_template, request, json

from FlaskWebProject1 import app
from FlaskWebProject1.ip_workers import IpTracker, IpStorage
from FlaskWebProject1.text_filter import StringProcessor

FeedbackInfo = namedtuple("FeedbackInfo", "sender date text")

FEEDBACK_STORAGE = {"comments": [],
                    "news": [],
                    "contact": []}

ip_storage = IpStorage()
ip_tracker = IpTracker()
string_processor = StringProcessor()


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


def process_post(ip_from):
    nickname = request.form['nickname']
    if not nickname:
        nickname = 'Anonymous'
    ip_tracker.track_ip(ip_from, posted=True)
    nickname = string_processor.shield(nickname)
    feedback = string_processor.shield(request.form['text_area'])
    record = FeedbackInfo(nickname, datetime.now(), feedback)
    FEEDBACK_STORAGE[request.args["from"]].append(record)


def get_client_info():
    try:
        resolution = "%sx%s" % (request.cookies['width'],
                                request.cookies['height'])
    except KeyError:
        resolution = "Cookie is turned off."

    browser = "%s %s" % (request.user_agent.browser,
                         request.user_agent.version.split('.')[0])
    return resolution, browser


@app.route("/comments", methods=["GET", "POST"])
def comments():
    ip_from = request.remote_addr

    if request.method == 'POST':
        if ip_from not in ip_tracker.last_posted_ip and request.form['text_area']:
            process_post(ip_from)
        return json.dumps(FEEDBACK_STORAGE[request.args["from"]])
    else:
        if ip_from not in ip_tracker.last_visited_ip:
            ip_tracker.track_ip(ip_from, posted=False)
            ip_storage.update(ip_from not in ip_tracker.unique_ips)

        ip_tracker.update_unique(ip_from)

    resolution, browser = get_client_info()

    return render_template("comments.html",
                           data=FEEDBACK_STORAGE[request.args["from"]],
                           visit_info=ip_storage.get_stats(),
                           last_time=ip_tracker.get_last_visited_time(ip_from),
                           resolution=resolution,
                           browser_info=browser)


@app.errorhandler(Exception)
def internal_error(error):
    return repr(error)
