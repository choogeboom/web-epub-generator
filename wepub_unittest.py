import unittest
import wepub

test_html = """<html>
<head>
    <title>This is a test</title>
</head>
<body>
<h1>Chapter Title</h1>
<div id="content">
<p>This is some text in the chapter.</p>
<p>This is another paragraph.</p>
</div>
<a id="next-chapter" href="next-chapter.html">Next Chapter</a>
</body>
</html>"""


class TestChapter(wepub.Chapter):

    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        return self.parsed_html.h1

    def get_content(self):
        return self.parsed_html("div", id="content")

    def get_next_chapter_url(self):
        return self.fix_url(self.parsed_html("a", id="next-chapter")["href"])


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
