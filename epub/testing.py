import unittest
import bs4
import string
from epub import meta
from epub import util


class UtilTest(unittest.TestCase):

    def test_generate_random_string_default(self):
        size = 12
        random_string = util.generate_random_string(size)
        self.assertEqual(size, len(random_string))

    def test_generate_random_string_digits(self):
        chars = string.digits
        size = 12
        random_string = util.generate_random_string(size, chars)
        self.assertEqual(size, len(random_string))
        self.assertTrue(random_string.isdigit())

    def test_get_soup(self):
        html = '<html>' \
               '<body>' \
               '<table>' \
               '<tbody>' \
               '<tr>' \
               '<td>' \
               'item' \
               '</td>' \
               '</tr>' \
               '</tbody>' \
               '</table>' \
               '</body>' \
               '</html>'
        soup = bs4.BeautifulSoup(html, "lxml")
        for child in soup.descendants:
            self.assertEqual(soup, util.get_soup(child))


class MetaDataPropertyTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.MetaDataProperty()
        self.meta.id = 'test-id'
        self.meta.value = 'Test Value'
        self.soup = bs4.BeautifulSoup('<package><metadata/></package>', 'xml')
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.id = None
        self.meta.append_to_document(self.parent)
        xml = '<metadata>' \
              '<default>Test Value</default>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_id_only(self):
        self.meta.append_to_document(self.parent)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_file_as(self):
        self.meta.file_as = 'Value, Test'
        self.meta.append_to_document(self.parent)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="file-as" refines="test-id">' \
              'Value, Test' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_alternative_script(self):
        self.meta.alternative_script = 'Test Alt'
        self.meta.append_to_document(self.parent)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="alternative-script" refines="test-id">' \
              'Test Alt' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_display_seq(self):
        self.meta.display_seq = 6
        self.meta.append_to_document(self.parent)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="display-seq" refines="test-id">' \
              '6' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_meta_authority(self):
        self.meta.meta_authority = 'Test'
        self.meta.append_to_document(self.parent)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="meta-auth" refines="test-id">' \
              'Test' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class PersonTest(unittest.TestCase):
    def setUp(self):
        self.person = meta.Person()
        self.person.id = 'test-id'
        self.person.value = 'John Doe'
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.person.id = None
        self.person.append_to_document(self.parent)
        xml = '<metadata>' \
              '<person>John Doe</person>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role(self):
        self.person.role = 'Author'
        self.person.append_to_document(self.parent)
        xml = '<metadata>' \
              '<person id="test-id">John Doe</person>' \
              '<meta property="role" refines="test-id">' \
              'Author' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role_scheme(self):
        self.person.role = 'aut'
        self.person.role_scheme = 'marc:relators'
        self.person.append_to_document(self.parent)
        xml = '<metadata>' \
              '<person id="test-id">John Doe</person>' \
              '<meta property="role" refines="test-id" scheme="marc:relators">' \
              'aut' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class CollectionTest(unittest.TestCase):
    def setUp(self):
        self.coll = meta.Collection()
        self.coll.value = 'Test Value'
        self.coll.id = 'test-id'
        self.soup = bs4.BeautifulSoup('<package><metadata/></package>', 'xml')
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.coll.id = None
        self.coll.append_to_document(self.parent)
        xml = '<metadata>' \
              '<meta property="belongs-to-collection">Test Value</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_type(self):
        self.coll.type = 'series'
        self.coll.append_to_document(self.parent)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta property="collection-type" refines="test-id">series</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_group_position(self):
        self.coll.group_position = 10
        self.coll.append_to_document(self.parent)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta property="group-position" refines="test-id">10</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_identifier(self):
        self.coll.identifier = 'identifier'
        self.coll.append_to_document(self.parent)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta property="dcterms:identifier" refines="test-id">identifier</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_refines_id(self):
        self.coll.refines_id = 'other-id'
        self.coll.append_to_document(self.parent)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection" ' \
              'refines="other-id">Test ' \
              'Value</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_collection(self):
        self.coll.collection = meta.Collection()
        self.coll.collection.id = 'other-id'
        self.coll.collection.identifier = 'identifier'
        self.coll.collection.value = 'Other Value'
        self.coll.append_to_document(self.parent)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta id="other-id" property="belongs-to-collection" ' \
              'refines="test-id">Other Value</meta>' \
              '<meta property="dcterms:identifier" refines="other-id">identifier</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaTitleTest(unittest.TestCase):
    def setUp(self):
        self.title = meta.Title()
        self.title.value = "Test Title"
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic_title(self):
        self.title.id = None
        self.title.append_to_document(self.parent)
        xml = "<metadata><dc:title>Test Title</dc:title></metadata>"
        self.assertEqual(xml, str(self.parent))

    def test_title_with_id(self):
        self.title.id = "titleId"
        tag, soup = self.title.append_to_document(self.parent)
        xml = '<dc:title id="titleId">Test Title</dc:title>'
        self.assertEqual(xml, str(tag))

    def test_title_with_id_and_type(self):
        self.title.id = "titleId"
        self.title.type = "main"
        self.title.append_to_document(self.parent)
        xml = '<metadata>' \
              '<dc:title id="titleId">Test Title</dc:title>' \
              '<meta property="title-type" refines="titleId">main</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

if __name__ == '__main__':
    unittest.main()
