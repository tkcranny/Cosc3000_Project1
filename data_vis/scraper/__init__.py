from models import get_session
from scraper.program import _find_program_ids, _harvest_webpages, _analyse_webpages


def scrape_programs():
    """

    :return:
    """
    session = get_session()

    program_ids = _find_program_ids()
    page_sources = _harvest_webpages(program_ids)
    _analyse_webpages(page_sources, session)

    session.commit()