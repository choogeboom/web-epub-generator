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
    book.title = 'Harry Potter and the Methods of Rationality'
    volume = epub.EPub()
    volume.books.append(book)
    creator = epub.meta.Creator(value='Eliezer Yudkowsky',
                                file_as='Yudkowsky, Eliezer',
                                scheme='marc:relators',
                                role='aut')
    transcriber = epub.meta.Contributor(value='Christopher Hoogeboom',
                                        file_as='Hoogeboom, Christopher',
                                        scheme='mark:relators',
                                        role='trc')
    description = epub.meta.Description(value='Petunia married a biochemist, and Harry '
                                              'grew up reading science and science '
                                              'fiction. Then came the Hogwarts letter, '
                                              'and a world of intriguing new '
                                              'possibilities to exploit. And new '
                                              'friends, like Hermione Granger, '
                                              'and Professor McGonagall, and Professor '
                                              'Quirrell... ')
    book.package_document.meta_data.creators.append(creator)
    book.package_document.meta_data.contributors.append(transcriber)
    book.package_document.meta_data.descriptions.append(description)
    volume.generate()
    return volume

if __name__ == "__main__":
    generate_epub()


