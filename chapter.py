"""
Chapters for specific web serials
"""
import abc
import re
import urllib.parse
from typing import Sequence

import bs4

from epub import Chapter, util


class WebChapter(Chapter):
    """
    Retrieves chapter content from the web
    """

    def __init__(self, url, **kwargs):
        super().__init__(self)
        self.url = url
        self.raw_html = None
        self.parsed_html = None
        self.set(**kwargs)
        if self.raw_html is None:
            self.load_html()
        if self.parsed_html is None:
            self.parsed_html = bs4.BeautifulSoup(self.raw_html, "lxml")

    @property
    def next_chapter_url(self):
        """
        The URL of the next chapter
        """
        return self.get_next_chapter_url()

    def load_html(self, url=None):
        if url is None:
            url = self.url
        else:
            self.url = url
        self.raw_html = util.read_html(url)

    def fix_url(self, raw_url: str) -> str:
        """
        Fix the URL if it is a relative URL

        :param raw_url: the raw url to fix
        :return: An absolute URL
        """
        if raw_url is not None and len(raw_url) > 2 and raw_url[0:2] == "..":
            return urllib.parse.urljoin(self.url, raw_url)
        else:
            return raw_url

    def __next__(self):
        url = self.fix_url(self.get_next_chapter_url())
        if url is None or len(url) == 0:
            raise StopIteration
        else:
            return self.__class__(url)

    @abc.abstractmethod
    def get_next_chapter_url(self) -> str:
        """Return the URL of the next chapter"""
        pass

    @abc.abstractmethod
    def get_title(self) -> str:
        """Return the title of the chapter"""
        pass

    @abc.abstractmethod
    def get_content(self) -> bs4.Tag:
        """Return the content of the chapter"""
        pass


class HPMoRChapter(WebChapter):
    """
    A Chapter for Harry Potter and the Methods of Rationality
    """

    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)

    def get_title(self) -> str:
        raw_title = self.parsed_html.find(name="div", id="chapter-title").text
        return re.sub(pattern=re.compile(r"\n"), repl=" ", string=raw_title)

    def get_content(self) -> Sequence[bs4.Tag]:
        container = self.parsed_html.find(id="storycontent")
        return container.contents

    def get_next_chapter_url(self) -> str:
        anchor = self.parsed_html.find("a", string=re.compile("Next"))
        return None if anchor is None else self.fix_url(anchor["href"])


class WildbowChapter(WebChapter):
    """
    A Chapter for any of the web serials by J.C. McCrae (AKA Wildbow)
    """

    chapter_regex = re.compile(r"(Last|Next|Previous)")

    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)

    def get_title(self) -> str:
        raw_title = self.parsed_html.find(name="h1", class_="entry-title").text
        return re.sub(r"\n", " ", raw_title)

    def get_content(self) -> Sequence[bs4.Tag]:
        content_div: bs4.Tag = self.parsed_html.find(name="div", class_="entry-content")
        try:
            start_tag = content_div.find(string=self.chapter_regex).find_parent("p")
        except AttributeError:
            yield from content_div.children
            return None
        for current_tag in start_tag.next_siblings:
            if current_tag == "\n":
                continue
            if current_tag.find("a") and current_tag.find(string=self.chapter_regex):
                return None
            else:
                yield current_tag
        return None

    def get_next_chapter_url(self) -> str:
        anchor = self.parsed_html.find("a", string=re.compile("Next"))
        return None if anchor is None else self.fix_url(anchor["href"])
