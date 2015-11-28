import bs4
import urllib.request
import urllib.parse
import re

from abc import ABCMeta, abstractmethod


def load_html(url: str) -> str:
    """
    Load the html from a URL into a string

    :param url: The URL of the page to load
    :return: A string containing the HTML of the specified page
    :raise urllib.request.URLError: on errors with opening the page
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
        """
        The title Tag of the chapter
        """
        return self.get_title()

    @property
    def content(self) -> bs4.Tag:
        """
        The content tag that contains all the chapter text
        """
        return self.get_content()

    @property
    def next_chapter_url(self):
        """
        The URL of the next chapter
        """
        return self.get_next_chapter_url()

    def fix_url(self, raw_url: str) -> str:
        """
        Fix the URL if it is a relative URL

        :param raw_url: the raw url to fix
        :return: An absolute URL
        """
        if len(raw_url) > 2 and raw_url[0:2] == "..":
            return urllib.parse.urljoin(self.url, raw_url)
        else:
            return raw_url

    def create_chapter_document(self):
        pass

    @abstractmethod
    def get_title(self) -> bs4.Tag:
        """Return the title of the chapter"""
        pass

    @abstractmethod
    def get_content(self):
        """Return the content of the chapter"""
        pass

    @abstractmethod
    def get_next_chapter_url(self):
        """Return the URL of the next chapter"""
        pass




