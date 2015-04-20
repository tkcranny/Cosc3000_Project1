"""
    Data Vis
    ========


    Data visualisation web server project for COSC3000 Semester 1 2015.

"""

from flask import Flask

app = Flask(__name__)


from . import views