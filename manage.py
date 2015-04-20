#!/usr/bin/env python

"""
    Manage.py
    =========

    Manager script for teh data_vis project.

    Can start up a server instance, run analyses and purge database records.
"""

from flask.ext.script import Manager

from data_vis import app


manager = Manager(app)


@manager.command
def run_debug():
    """
    Run a debug server.
    """
    app.run(debug=True)


if __name__ == "__main__":
    manager.run()
