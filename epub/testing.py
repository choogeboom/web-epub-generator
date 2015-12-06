import unittest
import bs4
import epub


class PackageTest(unittest.TestCase):
    pass


class ManifestTest(unittest.TestCase):
    pass


class ItemTest(unittest.TestCase):
    def setUp(self):
        self.item = epub.Item(id='test-id', href='Text/chapter_01.xhtml',
                              media_type='application/xhtml+xml')
        self.soup = bs4.BeautifulSoup('<manifest/>', 'xml')
        self.parent = self.soup.manifest

    def test_basic(self):
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_fallback(self):
        self.item.fallback = epub.Item(id='fallback-id', href='Text/fallback.xhtml',
                                       media_type='application/xhtml+xml')
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item fallback="fallback-id" href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml"/>' \
              '<item href="Text/fallback.xhtml" id="fallback-id" ' \
              'media-type="application/xhtml+xml"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_properties(self):
        self.item.properties = ['cover-image', 'svg']
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="cover-image svg"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_media_overlay(self):
        self.item.media_overlay = 'test'
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" media-overlay="test" ' \
              'media-type="application/xhtml+xml"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))



class TestContainer(unittest.TestCase):
    def test_container(self):
        container = epub.Container()
        container.register_rendition('EPUB/My Crazy Life.opf')
        xml = '<?xml version="1.0" encoding="utf-8"?>\n' \
              '<container version="1.0" ' \
              'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">' \
              '<rootfiles>' \
              '<rootfile full-path="EPUB/My Crazy Life.opf" ' \
              'media-type="application/oebps-package+xml"/>' \
              '</rootfiles>' \
              '</container>'
        self.assertEqual(xml, str(container.to_document()))


if __name__ == '__main__':
    unittest.main()
