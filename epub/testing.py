import unittest
import bs4
import epub


class PackageTest(unittest.TestCase):
    pass


class SpineTest(unittest.TestCase):
    def setUp(self):
        self.spine = epub.Spine()
        self.soup = bs4.BeautifulSoup('<package/>', 'xml')
        self.parent = self.soup.package

    def test_basic(self):
        self.spine.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<spine/>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_id(self):
        self.spine.id = 'test-id'
        self.spine.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<spine id="test-id"/>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_toc(self):
        self.spine.toc = 'ncx'
        self.spine.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<spine toc="ncx"/>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_page_progression_direction(self):
        self.spine.page_progression_direction = 'ltr'
        self.spine.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<spine page-progression-direction="ltr"/>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_itemrefs(self):
        self.spine.itemrefs = [epub.ItemRef(epub.Item(id='item-id'))]
        self.spine.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<spine>' \
              '<itemref idref="item-id"/>' \
              '</spine>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))


class ItemRefTest(unittest.TestCase):
    def setUp(self):
        self.itemref = epub.ItemRef(epub.Item(id='test-id'))
        self.soup = bs4.BeautifulSoup('<spine/>', 'xml')
        self.parent = self.soup.spine

    def test_item(self):
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_is_primary(self):
        self.itemref.is_primary = True
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" linear="yes"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_id(self):
        self.itemref.id = 'ref-id'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref id="ref-id" idref="test-id"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_is_x_aligned_center(self):
        self.itemref.is_x_aligned_center = True
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" properties="rendition:align-x-center"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_flow_auto(self):
        self.itemref.flow_mode = 'auto'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" properties="rendition:flow-auto"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_flow_paginated(self):
        self.itemref.flow_mode = 'paginated'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" properties="rendition:flow-paginated"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_flow_scrolled_continuous(self):
        self.itemref.flow_mode = 'scrolled-continuous'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" ' \
              'properties="rendition:flow-scrolled-continuous"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_layout_mode(self):
        self.itemref.layout_mode = 'pre-paginated'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" ' \
              'properties="rendition:layout-pre-paginated"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_orientation(self):
        self.itemref.orientation = 'auto'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" ' \
              'properties="rendition:orientation-auto"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_page_spread(self):
        self.itemref.page_spread = 'right'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" ' \
              'properties="page-spread-right"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))

    def test_spread_condition(self):
        self.itemref.spread_condition = 'auto'
        self.itemref.append_to_document(self.parent, self.soup)
        xml = '<spine>' \
              '<itemref idref="test-id" ' \
              'properties="rendition:spread-auto"/>' \
              '</spine>'
        self.assertEqual(xml, str(self.parent))


class TestManifest(unittest.TestCase):
    def setUp(self):
        self.manifest = epub.Manifest()
        self.soup = bs4.BeautifulSoup('<package/>', 'xml')
        self.parent = self.soup.package

    def test_no_items(self):
        self.manifest.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<manifest/>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_with_items(self):
        n_items = 2
        ids = ['id_{}'.format(i) for i in range(n_items)]
        hrefs = ['Text/chapter_{}.xhtml'.format(i) for i in range(n_items)]
        media_type = 'application/xhtml+xml'
        self.manifest.items = [epub.Item(id=_id, href=href, media_type=media_type)
                               for _id, href in zip(ids, hrefs)]
        self.manifest.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<manifest>' \
              '<item href="Text/chapter_0.xhtml" id="id_0" ' \
              'media-type="application/xhtml+xml"/>' \
              '<item href="Text/chapter_1.xhtml" id="id_1" ' \
              'media-type="application/xhtml+xml"/>' \
              '</manifest>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))


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

    def test_is_cover_image(self):
        self.item.is_cover_image = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="cover-image"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_is_math_ml(self):
        self.item.is_mathml = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="mathml"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_is_nav(self):
        self.item.is_nav = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="nav"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_has_remote_resources(self):
        self.item.has_remote_resources = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="remote-resources"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_is_scripted(self):
        self.item.is_scripted = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="scripted"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_is_svg(self):
        self.item.is_svg = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="svg"/>' \
              '</manifest>'
        self.assertEqual(xml, str(self.parent))

    def test_is_switch(self):
        self.item.is_switch = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="switch"/>' \
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

    def test_multiple_properties(self):
        self.item.is_mathml = True
        self.item.is_scripted = True
        self.item.append_to_document(self.parent, self.soup)
        xml = '<manifest>' \
              '<item href="Text/chapter_01.xhtml" id="test-id" ' \
              'media-type="application/xhtml+xml" properties="mathml scripted"/>' \
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
