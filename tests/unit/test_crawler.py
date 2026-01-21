"""
Unit tests for the crawler.
"""

import pytest
import requests

from scheduler_graph.crawler import fetch_website


class MockResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP error")


def test_fetch_website_returns_content(monkeypatch):
    html = "<html><body><h1>Test</h1></body></html>"

    def mock_get(*args, **kwargs):
        return MockResponse(html)

    monkeypatch.setattr(requests.Session, "get", mock_get)

    normalized_date, url, result = fetch_website("2020-01-02")

    assert "<h1>Test</h1>" in result


def test_fetch_website_constructs_correct_url(monkeypatch):
    captured = {}

    html = "<html></html>"

    def mock_get(self, url, **kwargs):
        captured["url"] = url
        return MockResponse(html)

    monkeypatch.setattr(requests.Session, "get", mock_get)

    fetch_website("2026-02-20")

    assert captured["url"] == "https://www.hamburg-tourism.de/sehen-erleben/veranstaltungen/veranstaltungskalender/?filter%5Bdate%5D=20.02.2026%2C20.02.2026&filter%5Bsearchword%5D=&filter%5Bdaytime%5D%5B%5D=evening&filter%5Bvadbcategorygroup%5D%5B%5D=19&filter%5Bdistrict%5D=hh_all&filter%5Bdistance%5D=15"
