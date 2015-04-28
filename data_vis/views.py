from flask import abort, send_file

from . import app


@app.route("/")
def server_app():
    """
    Serve the angular app.
    """

    return send_file("static/app/index.html")


@app.route("/api/update/<string:resource>")
def update_resource(resource):
    """
    Update a data resource.
    :param resource: the name of a resource type (e.x. 'programs', 'courses')
    :return: A HTTP response, 200 or 400
    """

    known_resources = {'courses', 'programs'}

    if not resource in known_resources:
        return abort(400, 'Not a known data resource.')

    return "200 - OK!"

@app.route('/Presentation')
def serve_presentation():
    return app.send_static_file('presentation/pres.html')