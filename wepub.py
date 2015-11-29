import urllib.request
import urllib.parse
import copy

import bs4

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
    _DEFAULT_XHTML = '\
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\
          <head><title></title></head>\
          <body><h1></h1></body>\
        </html>\
        '

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

    def create_document(self) -> bs4.BeautifulSoup:
        """Create and return a BeautifulSoup document containing the chapter"""
        doc = bs4.BeautifulSoup(Chapter._DEFAULT_XHTML, "xml")
        doc.head.title.string = self.title
        doc.body.h1.string = self.title
        doc.body.append(copy.copy(self.content))
        return doc

    def write(self, file_name: str):
        """
        Write the chapter to a file

        :param file_name: The name of the file to write
        """
        doc = self.create_document()
        with open(file_name, 'w') as f:
            print(doc.prettify(formatter="html"), file=f)

    @abstractmethod
    def get_title(self) -> str:
        """Return the title of the chapter"""
        pass

    @abstractmethod
    def get_content(self) -> bs4.Tag:
        """Return the content of the chapter"""
        pass

    @abstractmethod
    def get_next_chapter_url(self) -> str:
        """Return the URL of the next chapter"""
        pass


class Book:
    """
    An iterable class for chapters in the Web Series
    """

    def __init__(self, chapter_type, init_url):
        self.chapter_type = chapter_type
        self.init_url = init_url

    def __iter__(self):
        self.current_chapter = None
        return self

    def __next__(self):
        if self.current_chapter is None:
            self.current_chapter = self.chapter_type(self.init_url)
        else:
            next_url = self.current_chapter.next_chapter_url
            if next_url is None:
                raise StopIteration
            self.current_chapter = self.chapter_type(next_url)
        return self.current_chapter


