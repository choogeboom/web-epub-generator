import re

import bs4
import epub


class HPMoRChapter(epub.WebChapter):

    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)

    def get_title(self) -> str:
        raw_title = self.parsed_html.find(name="div", id="chapter-title").text
        return re.sub(pattern=re.compile(r'\n'), repl=' ', string=raw_title)

    def get_content(self) -> bs4.Tag:
        return self.parsed_html.find(id="storycontent")

    def get_next_chapter_url(self) -> str:
        anchor = self.parsed_html.find("a", string=re.compile("Next"))
        return None if anchor is None else self.fix_url(anchor["href"])


def generate_epub(path=None):
    first_chapter = HPMoRChapter(url='http://hpmor.com/chapter/1')
    book = epub.Book(first_chapter=first_chapter)

                     # chapter_type=HPMoR,
                     # init_url="http://hpmor.com/chapter/1",
                     # title="Harry Potter and the Methods of Rationality",
                     # author="Eliezer Yudkowsky")
    for chapter in book:
        print(chapter.title)
    return book


