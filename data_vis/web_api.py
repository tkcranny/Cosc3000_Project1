"""
    API
    ===

    Provides the classes used for providing a HTTP JSON API.

"""

import re

from flask.ext.restful import abort, Resource

from .models import Program, Major, get_session


class ProgramListApi(Resource):
    """
    Restful configuration for listing Programs.
    """

    def get(self):
        """
        Return all known programs in json form.
        :return: A JSON HTTP response.
        """

        session = get_session()
        query = session.query(Program)
        result = [program.to_dict() for program in query]
        return result



class ProgramApi(Resource):
    """

    """

    def get(self, program_id):
        """

        :param code:
        :return:
        """

        session = get_session()

        query = session.query(Program).filter_by(id=program_id)

        if query.count() != 1:
            abort(404)

        return query.one().to_dict()