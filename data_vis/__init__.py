"""
    Data Vis
    ========


    Data visualisation web server project for COSC3000 Semester 1 2015.

"""

from flask import Flask
from flask.ext import restful

from .web_api import ProgramListApi, ProgramApi

app = Flask(__name__)
api = restful.Api(app)  # Initialise Flask-Restful extension.

# Load HTTP routes for RESTful models.
# api.add_resource(Course, '/api/course/<string:course_code>')
api.add_resource(ProgramListApi, '/api/program')
api.add_resource(ProgramApi, '/api/program/<string:program_id>')

from . import views