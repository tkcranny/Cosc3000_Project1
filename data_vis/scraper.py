"""
    Scraper
    =======

    Sub module for retreiving parsing and loading course data.

"""

import requests
from bs4 import BeautifulSoup


from .models import Program


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
    soup = BeautifulSoup(resp.content)

    _find_programs(soup)


def _scrape_program(prog_code):
    """
    Build a (UQ) Program object by scraping the website.
    :param prog_code: A program's code as assigned by UQ.
    :return: A :models.Program: instance.
    """

    prog_url = 'https://www.uq.edu.au/study/program.html?acad_prog=' + prog_code
    resp = requests.get(prog_url)
    soup = BeautifulSoup(resp.content)




def _find_programs(soup):
    """
    Construct a list of Undergraduate programs from the webpage source.
    :param soup:
    :return:
    """

    extract_a_tags = lambda t: t.find('a')
    prog_rows = map(extract_a_tags, soup.find_all('td', {'class': 'title'}))

    # Filter to links that have links to Program pages in them.
    progs = [a for a in prog_rows if a and a.has_attr('href')]

    # Construct a list of program objects.
    prog_objs = [_scrape_program(prog.href.split('=')[-1].strip()) for prog in progs]

    for prog_obj in prog_objs:
        print(prog_obj)


def retrieve_programs():
    """
    Fetch *data structure* of courses from the UQ undergraduate site.
    :return: A list of :models.Course: Objects
    """




