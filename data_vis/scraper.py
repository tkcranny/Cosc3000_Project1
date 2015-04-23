"""
    Scraper
    =======

    Sub module for retreiving parsing and loading course data.

"""

import re
import shelve
import concurrent.futures as futures

import requests
from bs4 import BeautifulSoup


from .models import Program, Faculty, get_session


# FACULTY_REF = {
#     'index.html?id=4405': 'BEL',
#     'index.html?id=4406': 'EAIT',
#     # '': 'HABS',
#     'http://hass.uq.edu.au/': 'HASS',
#     'http://health.uq.edu.au/medicine-biomedical-sciences': 'MBS',
#     'index.html?id=4404': 'SCI',
# }


class UqDataScraperError(Exception):
    """ Custom error for this scraping sub-module.
    """
    pass


def scrape():
    """

    :return:
    """
    program_url = 'https://www.uq.edu.au/study/browse.html?level=ugpg'
    resp = requests.get(program_url)
    program_ids = _find_program_ids(resp.content)
    page_sources = _harvest_webpages(program_ids)



def _harvest_webpages(program_ids, from_shelf=True):
    """
    Download the source of program pages efficiently.
    :param program_ids: A collection of UQ Program IDs.
    :return: A list of web page sources
    """

    if from_shelf:
        with shelve.open('local_shelf') as db_read:
            sources = db_read.get('program_pages')
        if sources:
            return sources

    prog_url_template = 'https://www.uq.edu.au/study/program.html?acad_prog={}'
    prog_urls = (prog_url_template.format(prog_id) for prog_id in program_ids)

    print('About to download {} pages'.format(len(program_ids)))
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        page_futures = [executor.submit(requests.get, prog_url) for prog_url in prog_urls]

    print('Downloading...')

    # Wait to load all results
    results = futures.wait(page_futures)

    sources = [completed.result().content for completed in results.done]
    print('Downloaded {} pages'.format(len(sources)))

    with shelve.open('local_shelf') as db_write:
        db_write['program_pages'] = sources

    return sources



def _process_program_page(page_source):
    """Return a dictionary of proram attributes from a web pages source"""
    soup = BeautifulSoup(page_source)

    # Retrieve attributes from HTML source.
    program_attributes = {
        'title': soup.find('span', {'id': 'program-title'}).text.strip(),
        'abbr': soup.find('span', {'id': 'program-abbreviation'}).text.strip(),
        'units': int(soup.find('p', {'id': 'program-domestic-units'}).text),
        'op': int(soup.find('span', {'id': 'program-domestic-entryreq'})
                  .find('p').text.split('/')[0].strip()),
        'annual_fee': int(soup.find('p', {'class': 'fees'}).text.split()[-1]),
        'semesters': int(2 * float(re.search(  # Calculate number of semesters.
                '(\\d+(\\.\\d+)?)',
                soup.find('p', {'id': 'program-domestic-duration'}).text)
            .group(1))),
    }


def _scrape_program(prog_code, session):
    """
    Build a (UQ) Program object by scraping the website.
    :param prog_code: A program's code as assigned by UQ.
    :return: A :models.Program: instance.
    """

    prog_url = 'https://www.uq.edu.au/study/program.html?acad_prog={}'
    resp = requests.get(prog_url.format(prog_code))
    soup = BeautifulSoup(resp.content)

    print('Program ID:', prog_code)


    print('Program {} analysed (id: {})'.format(program_attributes['title'], prog_code))

    # Create the program object.
    program = Program(id=prog_code, **program_attributes)

    # Link the relevant faculties.
    faculty_references = [a['href'].strip() for a in soup.find(
        'p', {'id': 'program-domestic-faculty'}).find_all('a')]


    faculties = []
    for faculty_ref in faculty_references:
        faculty_obj = session.query(Faculty).filter_by(html_reference=faculty_ref).one()
        faculties.append(faculty_obj)

    program.faculties.extend(faculties)

    return program




def _find_program_ids(page_source):
    """
    Construct a list of Undergraduate program IDS.
    :param soup:
    :return:
    """

    soup = BeautifulSoup(page_source)

    extract_a_tags = lambda t: t.find('a')
    prog_rows = map(extract_a_tags, soup.find_all('td', {'class': 'title'}))

    # Filter to links that have links to Program pages in them.
    progs = [a for a in prog_rows if a and a.has_attr('href')]

    # Construct a list of program objects.

    # failed = []

    prog_ids = [prog['href'].split('=')[-1].strip() for prog in progs]
    return prog_ids

    # for prog in progs:
    #         prog_id = prog['href'].split('=')[-1].strip()
    #         try:
    #             prog_obj = _scrape_program(prog_id, session)
    #             session.add(prog_obj)
    #         except:
    #             print('  failed for', prog_id)
    #             failed.append(prog_id)

    # prog_objs = [_scrape_program(prog['href'].split('=')[-1].strip(), session) for prog in progs]
    # session.add_all(prog_objs)
    # print("{} ({:%}) failed programs:".format(failed, len(failed)/len(progs)))
    # session.commit()


def retrieve_programs():
    """
    Fetch *data structure* of courses from the UQ undergraduate site.
    :return: A list of :models.Course: Objects
    """




