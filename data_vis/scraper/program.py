from concurrent import futures as futures
import re
import shelve
from bs4 import BeautifulSoup
import requests
from models import Program, Faculty


def _find_program_ids():
    """
    Construct a list of Undergraduate program IDS.
    :param soup:
    :return:
    """
    # Fetch web page.
    program_url = 'https://www.uq.edu.au/study/browse.html?level=ugpg'
    resp = requests.get(program_url)
    soup = BeautifulSoup(resp.content)

    extract_a_tags = lambda t: t.find('a')
    prog_rows = map(extract_a_tags, soup.find_all('td', {'class': 'title'}))

    # Filter to links that have links to Program pages in them.
    progs = [a for a in prog_rows if a and a.has_attr('href')]

    # Extract ID codes.
    prog_ids = [prog['href'].split('=')[-1].strip() for prog in progs]
    return prog_ids


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


def _analyse_webpages(page_sources, session):
    """
    Takes a series of web page sources (bytes) and analyses
    :param page_sources:
    :return:
    """
    prog_dicts = map(_analyse_page_source, page_sources)
    # session = get_session()

    # with session.no_autoflush:
    for prog_dict, faculty_refs in prog_dicts:
        program = Program(**prog_dict)
        print('Analysed {}. ID: {}'.format(program.title, program.id))

        if not session.query(Program).filter_by(id=program.id).count():
            session.add(program)
            session.commit()
        else:
            print('\tPROGRAM ALREADY EXISTS:', program.id)

        for faculty_ref in faculty_refs:
            try:
                faculty_obj = session.query(Faculty).filter_by(html_reference=faculty_ref).first()
                program.faculties.append(faculty_obj)
            except:
                print('\tFAILED FOR FACULTY LINK:', faculty_ref)


def _analyse_page_source(page_source):
    """Return a dictionary of program attributes from a web pages source"""
    soup = BeautifulSoup(page_source)

    # Retrieve attributes from HTML source.
    program_attributes = {}

    # Set the title and ID.
    program_attributes['title'] = soup.find('span', {'id': 'program-title'}).text.strip()
    program_attributes['id'] = int(soup.find('p', {'id': 'program-domestic-programcode'}).text)

    # Attempt to extract other attributes

    try: # Course abbreviation.
        program_attributes['abbr'] = soup.find('span', {'id': 'program-abbreviation'}).text.strip()
    except:
        print('\tCould not find abbr for', program_attributes['title'])

    try: # Number of units
        program_attributes['units'] = int(soup.find('p', {'id': 'program-domestic-units'}).text)
    except:
        print('\tCould not find UNITS for', program_attributes['title'])

    try: # Entry OP
        program_attributes['op'] = int(soup.find('span', {'id': 'program-domestic-entryreq'})
                  .find('p').text.split('/')[0].strip())
    except:
        print('\tCould not find OP for', program_attributes['title'])

    try: # Annual fee
        program_attributes['annual_fee'] = int(soup.find('p', {'class': 'fees'}).text.split()[-1])
    except:
        print('\tCould not find FEE for', program_attributes['title'])

    try: # Numer of Semesters.
        program_attributes['semesters'] = int(2 * float(re.search(
                '(\\d+(\\.\\d+)?)',
                soup.find('p', {'id': 'program-domestic-duration'}).text)
            .group(1)))
    except:
        print('\tCould not find SEMESTERS for', program_attributes['title'])

    try: # Campus.
        program_attributes['location'] = soup.find('p', {'id': 'program-domestic-location'}).text.strip()
    except:
        print('Could not find LOCATION for', program_attributes['title'])

    # Extract faculty references.
    faculty_refs = [a['href'].strip() for a in soup.find(
        'p', {'id': 'program-domestic-faculty'}).find_all('a')]

    return program_attributes, faculty_refs