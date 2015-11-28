import bs4
import urllib.request
import re

from abc import ABCMeta, abstractmethod


def load_html(url: str) -> str:
    """
    Load the html from a URL into a string

    Args:
        url: The URL of the page to load
    Returns:
        A string containing the HTML of the specified page
    Raises:
        urllib.request.URLError: on errors with opening the page
    """
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html.decode('utf-8')


class Chapter:
    __meta_class__ = ABCMeta

    def __init__(self, url: str, html: str=None):
        self.url = url
        if html:
            self.raw_html = html
        else:
            self.raw_html = load_html(url)
        self.parsed_html = bs4.BeautifulSoup(self.raw_html, "lxml")

    @property
    def title(self) -> bs4.Tag:
        return self.get_title()

    @abstractmethod
    def get_title(self) -> bs4.Tag:
        pass

    @property
    def content(self) -> bs4.Tag:
        return self.get_content()

    @abstractmethod
    def get_content(self):
        pass

    @property
    def next_chapter_url(self):
        return self.get_next_chapter_url()

    @abstractmethod
    def get_next_chapter_url(self):
        pass


class HPMoR(Chapter):

    def __init__(self, html: str):
        super().__init__(html)

    def get_title(self) -> bs4.Tag:
        return self.parsed_html.find(name="div", id="chapter-title")

    def get_content(self) -> bs4.Tag:
        return self.parsed_html.find(id="storycontent")

    def get_next_chapter_url(self):
        return self.parsed_html.find("a", string=re.compile("Next"))

