"""
    API
    ===

    Provides the classes used for providing a HTTP JSON API.

"""

import re

from flask.ext.restful import abort, Resource


class CourseList(Resource):
    """
    """

    def get(self, number):
        """ Return a listing of courses.
        """


class Course(Resource):
    """
    """

    def get(self, course_code):
        """ Return information in JSON form about a UQ Course.
        """
        if not re.match('^[a-z]{4}[0-9]{4}$', course_code):
            abort(404, message='Not a valid course code')


        return {
            'name': 'not known',
            'code': course_code,
        }