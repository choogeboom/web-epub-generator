import unittest
import epub


class TestPackage(unittest.TestCase):
    pass


class TestManifest(unittest.TestCase):
    pass


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
