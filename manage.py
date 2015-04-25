#!/usr/bin/env python

"""
    Manage.py
    =========

    Manager script for teh data_vis project.

    Can start up a server instance, run analyses and purge database records.
"""

from pathlib import Path

from flask.ext.script import Manager

from data_vis import app
from data_vis.models import get_session, Faculty


manager = Manager(app)


@manager.command
def reset_db():
    """ Initialise the database tables.
    """
    db_file = Path('courses.db')

    # Delete database file
    if db_file.exists():
        print('SQLite file exists, removing it.')
        db_file.unlink()
    else:
        print('No SQLite file found.')


    from data_vis.models import Base, engine
    Base.metadata.create_all(engine)

    session = get_session()

    # Load Faculties.
    faculty_info = [
        ('BEL', 'Business, Economics and Law', 'index.html?id=4405'),
        ('EAIT', 'Engineering, Architecture and Information Technology', 'index.html?id=4406'),
        ('HABS', 'Health and Behavioural Sciences', 'http://health.uq.edu.au/health-behavioural-sciences'),
        ('HASS', 'Humanities and Social Sciences', 'http://hass.uq.edu.au/'),
        ('MBS', 'Medicine and Biomedical Sciences', 'http://health.uq.edu.au/medicine-biomedical-sciences'),
        ('SCI', 'Science', 'index.html?id=4404'),
    ]
    # Add faculties to the database.
    for fac_id, title, href in faculty_info:
        fac_obj = Faculty(id=fac_id, title=title, html_reference=href)
        session.merge(fac_obj)
    session.commit()


@manager.command
def run_debug():
    """
    Run a debug server.
    """
    app.run(debug=True)


@manager.command
def debug():
    from scraper import scrape_programs

    reset_db()
    scrape_programs()



if __name__ == "__main__":
    manager.run()
