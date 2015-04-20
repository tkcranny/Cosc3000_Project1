from flask import send_file, render_template

from . import app


@app.route("/")
def server_app():
    """
    Serve the angular app.
    """

    return send_file("static/app/index.html")
