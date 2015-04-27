"""
    scraper.majors
    ==============

    sub module to handle scraping of UQ majors.
"""


# import shelve
import json
import os
from concurrent import futures
import requests
from bs4 import BeautifulSoup


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

    print('Loading from cache...')
    # Load already downloaded pages first.
    if from_cache and os.path.exists('.cache/majors.json'):
        # Load the 'majors' key from a local dict. the value should be
        with open('.cache/majors.json', 'r') as fh_read:
            majors.update(json.loads(fh_read.read()))
        print('Retrieved {} majors from local cache'.format(len(majors)))

    # Find and retrieve non-downloaded pages (by excluding cached IDs).
    to_dl_ids = set(major_ids) - set(majors.keys())

    print('{} to download'.format(len(to_dl_ids)))

    to_dl_urls = [major_url_template.format(major_id) for major_id in to_dl_ids]
    print('About to download {} major pages'.format(len(to_dl_urls)))

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        page_futures = [executor.submit(requests.get, major_url) for major_url in to_dl_urls]

    print('Downloading...')
    results = futures.wait(page_futures)  # Wait for all the downloads to complete.

    # Create a new dict mapping ids to the content just downloaded.
    sources = {completed.result().url.split('=')[-1].strip(): completed.result().content for completed in results.done}
    print('Downloaded {} more majors.'.format(len(sources)))

    majors.update(sources)  # Incorporate downloaded pages into dict.

    majors = {k: v.decode('utf-8') if isinstance(v, bytes) else v for k,v in majors.items()}

    print()
    # Save everything to local cache.
    with open('.cache/majors.json', 'w') as fh_out:
        fh_out.write(json.dumps(majors))

    return majors
