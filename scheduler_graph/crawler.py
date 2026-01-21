"""
Crawler for the event website for Hamburg:
https://www.hamburg-tourism.de/sehen-erleben/veranstaltungen/veranstaltungskalender/
"""

import os
from datetime import datetime
import requests
from urllib.parse import urlencode


BASE_URL = "https://www.hamburg-tourism.de"
EXTENDED_URL = BASE_URL + "/sehen-erleben/veranstaltungen/veranstaltungskalender/"


def fetch_website(select_date: str) -> tuple[str, str, str]:
    """
    Return date, url, and html from the website for the selected day.
    """

    normalized_date = datetime.strptime(
        select_date, "%Y-%m-%d"
    ).strftime("%d.%m.%Y")

    params = {
        "filter[date]": f"{normalized_date},{normalized_date}",
        "filter[searchword]": "",    # No keywords used
        "filter[daytime][]": ["evening"],    # i.e. 18:00-24:00
        "filter[vadbcategorygroup][]": ["19"],    # i.e. concerts and music
        "filter[district]": "hh_all",    # entirety of Hamburg
        "filter[distance]": "15",    # distance of 15 km
    }
    url = f"{EXTENDED_URL}?{urlencode(params, doseq=True)}"

    headers = {
        "User-Agent": "Event Scheduler 1.0",
        "From": os.getenv("CONTACT_EMAIL"),
    }

    with requests.Session() as session:
        result = session.get(url, headers=headers, timeout=30)
        result.raise_for_status()
        return select_date, url, result.text
