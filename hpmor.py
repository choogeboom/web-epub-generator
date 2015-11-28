import wepub
import bs4


class HPMoR(wepub.Chapter):

    def __init__(self, url: str, html: str=None):
        super().__init__(url, html)

    def get_title(self) -> bs4.Tag:
        return self.parsed_html.find(name="div", id="chapter-title")

    def get_content(self) -> bs4.Tag:
        return self.parsed_html.find(id="storycontent")

    def get_next_chapter_url(self):
        anchor = self.parsed_html.find("a", string=re.compile("Next"))
        return self.fix_url(anchor["href"])