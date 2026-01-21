"""
Parser for the html content of the fetched website.
"""

import re
from urllib.parse import urljoin
from typing import Optional, List, Dict

from bs4 import BeautifulSoup

from models.event import Event


def _clean_text(s: Optional[str]) -> Optional[str]:
    _ws = re.compile(r"\s+")
    
    if not s:
        return None
    s = _ws.sub(" ", s).strip()
    return s or None


def _extract_info_list(article: BeautifulSoup) -> Dict[str, str]:
    """
    Parses:
      <ul class="listTeaser-event__text__infos">
        <li><span class="icon-calendar"></span> 02.01.2020 </li>
        <li><span class="icon-clock"></span> 20:00 </li>
        <li><span class="icon-located"></span>Example Venue</li>
      </ul>
    """

    out = {"event_date": None, "event_time": None, "event_venue": None}

    ul = article.select_one("ul.listTeaser-event__text__infos")
    if not ul:
        return out

    for li in ul.select("li"):
        li_text = _clean_text(li.get_text(" ", strip=True))
        if not li_text:
            continue

        if li.select_one(".icon-calendar"):
            out["event_date"] = _clean_text(
                li_text.replace("icon-calendar", "")
            ) or _clean_text(li_text)
        elif li.select_one(".icon-clock"):
            out["event_time"] = _clean_text(
                li_text.replace("icon-clock", "")
            ) or _clean_text(li_text) 
        elif li.select_one(".icon-located"):
            out["event_venue"] = _clean_text(
                li_text.replace("icon-located", "")
            ) or _clean_text(li_text)

    return out


def _extract_short_description(article: BeautifulSoup) -> Optional[str]:
    """
    Parses:
    <div ...><p><p>TEXT</p></p></div>
    """

    container = article.select_one("div.listTeaser-event__text > p")

    if not container:
        return None
    return _clean_text(container.get_text(" ", strip=True))


def extract_events(html: str, page_url: str) -> List[Event]:
    """
    Extracts event details from the HTML.
    """
    
    soup = BeautifulSoup(html, "lxml")

    events: List[Event] = []

    for art in soup.select("article.listTeaser-event"):
        event_dict = {}

        title_el = art.select_one("div.listTeaser-event__text > h3")
        event_name = _clean_text(
            title_el.get_text(" ", strip=True)
        ) if title_el else None
        event_dict["event_name"] = event_name

        info = _extract_info_list(art)
        event_dict["event_date"] = info["event_date"]
        event_dict["event_time"] = info["event_time"]
        event_dict["event_venue"] = info["event_venue"]

        event_description = _extract_short_description(art)
        event_dict["event_description"] = event_description

        link_el = art.select_one("a.listTeaser-event__link[href]")
        event_url = urljoin(
            page_url, link_el["href"]
        ) if link_el and link_el.get("href") else None
        event_dict["event_url"] = event_url

        events.append(Event.from_dict(event_dict))

    return events
