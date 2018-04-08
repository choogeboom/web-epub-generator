"""
Chapters for specific web serials
"""
import copy
import re
from typing import Sequence

import bs4

import epub


class HPMoRChapter(epub.WebChapter):
    """
    A Chapter for Harry Potter and the Methods of Rationality
    """
    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)

    def get_title(self) -> str:
        raw_title = self.parsed_html.find(name="div", id="chapter-title").text
        return re.sub(pattern=re.compile(r'\n'), repl=' ', string=raw_title)

    def get_content(self) -> Sequence[bs4.Tag]:
        container = self.parsed_html.find(id="storycontent")
        return container.contents

    def get_next_chapter_url(self) -> str:
        anchor = self.parsed_html.find("a", string=re.compile("Next"))
        return None if anchor is None else self.fix_url(anchor["href"])


wildbow_chapter_regex = re.compile(r'(Last|Next) Chapter')


class WildbowChapter(epub.WebChapter):
    """
    A Chapter for any of the web serials by J.C. McCrae (AKA Wildbow)
    """
    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)

    def get_title(self) -> str:
        raw_title = self.parsed_html.find(name='h1', class_='entry-title').text
        return re.sub(r'\n', ' ', raw_title)

    def get_content(self) -> Sequence[bs4.Tag]:
        content_div = copy.copy(
            self.parsed_html.find(name='div', class_='entry-content'))
        start_tag = content_div.find(string=wildbow_chapter_regex).find_parent('p')
        for current_tag in start_tag.next_siblings:
            if current_tag == '\n':
                continue
            if current_tag.find('a') and current_tag.find(string=wildbow_chapter_regex):
                return None
            else:
                yield current_tag
        return None

    def get_next_chapter_url(self) -> str:
        anchor = self.parsed_html.find("a", string='Next Chapter')
        return None if anchor is None else self.fix_url(anchor['href'])