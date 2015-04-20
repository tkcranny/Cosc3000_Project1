"""
    Data Vis
    ========


    Data visualisation web server project for COSC3000 Semester 1 2015.

"""

from flask import Flask
from flask.ext import restful

from api import Course

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(Course, '/api/course/<string:course_code>')


from . import views