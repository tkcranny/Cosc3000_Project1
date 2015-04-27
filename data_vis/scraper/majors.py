"""
    scraper.majors
    ==============

    sub module to handle scraping of UQ majors.
"""


# import shelve
import json
import os
from concurrent import futures
from collections import namedtuple

import requests
from bs4 import BeautifulSoup

from data_vis.models import Program, Faculty, get_session

# Tuple to store a majors information.
ProgramRecord = namedtuple('Program', ['title', 'id', 'program_id'])


def get_major_ids():
    """
    Get a set of all UQ major codes.
    :return:
    """
    url = 'https://www.uq.edu.au/study/browse.html?level=ugpg'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content)

    links = soup.find_all('a', {'href': True})

    is_major = lambda t: '/study/plan.html?acad_plan=' in t['href']
    major_codes = {t['href'].split('=')[-1] for t in filter(is_major, links)}
    return major_codes


def harvest_majors(major_ids, from_cache=True):
    """
    Fetch a collection of UQ major web pages asyncronously.

    This method can use a local cache, where results are stored in
    an external JSON file.

    :param major_ids: A collection of 10 character major codes.
    :param from_cache: Use a local cache if possible.
    :return: A list of web page sources.
    """

    major_url_template = 'https://www.uq.edu.au/study/plan.html?acad_plan={}'

    majors = {} # The mapping to be populated and returned.

    # Load already downloaded pages first.
    if from_cache and os.path.exists('.cache/majors.json'):
        # Load the 'majors' key from a local dict. the value should be
        with open('.cache/majors.json', 'r') as fh_read:
            majors.update(json.loads(fh_read.read()))

    # Find and retrieve non-downloaded pages (by excluding cached IDs).
    to_dl_ids = set(major_ids) - set(majors.keys())

    to_dl_urls = [major_url_template.format(major_id) for major_id in to_dl_ids]
    print('About to download {} major pages'.format(len(to_dl_urls)))

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        page_futures = [executor.submit(requests.get, major_url) for major_url in to_dl_urls]

    results = futures.wait(page_futures)  # Wait for all the downloads to complete.

    # Create a new dict mapping ids to the content just downloaded.
    sources = {completed.result().url.split('=')[-1].strip(): completed.result().content for completed in results.done}
    print('Downloaded {} more majors.'.format(len(sources)))

    # Add and convert new web pages.
    majors.update(sources)
    majors = {k: v.decode('utf-8') if isinstance(v, bytes) else v for k,v in majors.items()}

    # Save everything to local cache.
    with open('.cache/majors.json', 'w') as fh_out:
        fh_out.write(json.dumps(majors))

    return majors


def process_pages(page_sources):
    """
    Analyse a series of web pages of UQ majors to extract the features.
    :param page_sources: a dict mapping major IDs to their respective web content.
    :return: A list of ProgramRecords for each program type.
    """
    program_records = []

    for major_id, source in page_sources.items():
        soup = BeautifulSoup(source)

        try:
            attrs = {
                'title': soup.find('div', {'id': 'page-head'}).h1.text.strip(),
                'id': major_id,
                'program_id': int(soup.find('p', {'id': 'plan-field-key'}).text)
            }
            program_records.append(ProgramRecord(**attrs))
        except AttributeError:  # Catch bad web pages.
            print('Major {} has bad html!'.format(major_id))

    return program_records


def add_programs_to_db(program_rows):
    """
    Adds a collection of UQ major records into the database. Opens a connection and closes it.
    :param programs: a collection of ProgramRecord named-tuples.
    :return: None.
    """
    programs = []
    for program_row in program_rows:
        program = Major(id=program_row.id, title=program_row.title)
        program.program_id = program_row.program_id

    session = get_session()
    session.add_all(programs)
    session.commit()
    session.close()