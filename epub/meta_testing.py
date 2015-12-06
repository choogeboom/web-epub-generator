import unittest
import bs4
import string
import datetime
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

    def test_set_get(self):
        set_get = util.SetGet()
        set_get.set(prop_0=0, prop_1=1, prop_2=2)
        values = set_get.get('prop_0', 'prop_1', 'prop_2')
        for i, val in enumerate(values):
            self.assertEqual(i, val)


class MetaDataPropertyTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.MetaDataProperty(
                                          id='test-id',
                                          value='Test Value')
        self.soup = bs4.BeautifulSoup('<package><metadata/></package>', 'xml')
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.id = None
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<default>Test Value</default>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_id_only(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_file_as(self):
        self.meta.file_as = 'Value, Test'
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="file-as" refines="test-id">' \
              'Value, Test' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_alternative_script(self):
        self.meta.alternative_script = 'Test Alt'
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="alternative-script" refines="test-id">' \
              'Test Alt' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_display_seq(self):
        self.meta.display_seq = 6
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="display-seq" refines="test-id">' \
              '6' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_meta_authority(self):
        self.meta.meta_authority = 'Test'
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<default id="test-id">Test Value</default>' \
              '<meta property="meta-auth" refines="test-id">' \
              'Test' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaPersonTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Person(id='test-id', value='John Doe')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.id = None
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<person>John Doe</person>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role(self):
        self.meta.role = 'Author'
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<person id="test-id">John Doe</person>' \
              '<meta property="role" refines="test-id">' \
              'Author' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role_scheme(self):
        self.meta.role = 'aut'
        self.meta.role_scheme = 'marc:relators'
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<person id="test-id">John Doe</person>' \
              '<meta property="role" refines="test-id" scheme="marc:relators">' \
              'aut' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaCoverageTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Coverage()
        self.meta.id = 'test-id'
        self.meta.value = 'John Doe'
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic_id(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:coverage id="test-id">John Doe</dc:coverage>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaCollectionTest(unittest.TestCase):
    def setUp(self):
        self.coll = meta.Collection(id='test-id', value='Test Value')
        self.soup = bs4.BeautifulSoup('<package><metadata/></package>', 'xml')
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.coll.id = None
        self.coll.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<meta property="belongs-to-collection">Test Value</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_type(self):
        self.coll.type = 'series'
        self.coll.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta property="collection-type" refines="test-id">series</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_group_position(self):
        self.coll.group_position = 10
        self.coll.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta property="group-position" refines="test-id">10</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_identifier(self):
        self.coll.identifier = 'identifier'
        self.coll.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta property="dcterms:identifier" refines="test-id">identifier</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_refines_id(self):
        self.coll.refines_id = 'other-id'
        self.coll.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection" ' \
              'refines="other-id">Test ' \
              'Value</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_collection(self):
        self.coll.collection = meta.Collection(id='other-id', identifier='identifier',
                                               value='Other Value')
        self.coll.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<meta id="test-id" property="belongs-to-collection">Test Value</meta>' \
              '<meta id="other-id" property="belongs-to-collection" ' \
              'refines="test-id">Other Value</meta>' \
              '<meta property="dcterms:identifier" refines="other-id">identifier</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaContributorTest(unittest.TestCase):
    def setUp(self):
        self.main = meta.Contributor(id='test-id', value='John Doe')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.main.id = None
        self.main.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:contributor>John Doe</dc:contributor>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role(self):
        self.main.role = 'Author'
        self.main.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:contributor id="test-id">John Doe</dc:contributor>' \
              '<meta property="role" refines="test-id">' \
              'Author' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role_scheme(self):
        self.main.set(role='aut', role_scheme='marc:relators')
        self.main.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:contributor id="test-id">John Doe</dc:contributor>' \
              '<meta property="role" refines="test-id" scheme="marc:relators">' \
              'aut' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaCreatorTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Creator(id='test-id', value='John Doe')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.id = None
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:creator>John Doe</dc:creator>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role(self):
        self.meta.role = 'Author'
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:creator id="test-id">John Doe</dc:creator>' \
              '<meta property="role" refines="test-id">' \
              'Author' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_role_scheme(self):
        self.meta.set(role='aut', role_scheme='marc:relators')
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:creator id="test-id">John Doe</dc:creator>' \
              '<meta property="role" refines="test-id" scheme="marc:relators">' \
              'aut' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaDateTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Date(id=None, value=datetime.datetime(1983, 11, 16))
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:date>1983-11-16T00:00:00</dc:date>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaDescriptionTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Description(id=None, value='This is a description')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:description>This is a description</dc:description>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaFormatTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Format(id=None, value='application/epub+zip')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:format>application/epub+zip</dc:format>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaIdentifierTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Identifier(id='test-id', value='identifier')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.id = None
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:identifier>identifier</dc:identifier>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_basic_id(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:identifier id="test-id">identifier</dc:identifier>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_type(self):
        self.meta.type = 'ISBN'
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:identifier id="test-id">identifier</dc:identifier>' \
              '<meta property="identifier-type" refines="test-id">' \
              'ISBN' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_type_and_scheme(self):
        self.meta.set(type='06', scheme='onix:codelist5')
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:identifier id="test-id">identifier</dc:identifier>' \
              '<meta property="identifier-type" refines="test-id" ' \
              'scheme="onix:codelist5">' \
              '06' \
              '</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaLanguageTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Language(id=None, value='en-US')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:language>en-US</dc:language>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaPublisherTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Publisher(id=None, value='Test')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:publisher>Test</dc:publisher>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaRelationTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Relation(id=None, value='Test')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:relation>Test</dc:relation>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaRightsTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Rights(id=None, value='Test')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:rights>Test</dc:rights>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaSourceTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Source(id=None, value='Test')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:source>Test</dc:source>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaSubjectTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Subject(id=None, value='Test')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:subject>Test</dc:subject>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaTitleTest(unittest.TestCase):
    def setUp(self):
        self.title = meta.Title(id='test-id', value='Test Title')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic_title(self):
        self.title.id = None
        self.title.append_to_document(self.parent, self.soup)
        xml = "<metadata><dc:title>Test Title</dc:title></metadata>"
        self.assertEqual(xml, str(self.parent))

    def test_title_with_id(self):
        self.title.append_to_document(self.parent, self.soup)
        xml = '<metadata><dc:title id="test-id">Test Title</dc:title></metadata>'
        self.assertEqual(xml, str(self.parent))

    def test_title_with_id_and_type(self):
        self.title.type = "main"
        self.title.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:title id="test-id">Test Title</dc:title>' \
              '<meta property="title-type" refines="test-id">main</meta>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaTypeTest(unittest.TestCase):
    def setUp(self):
        self.meta = meta.Type(id=None, value='Test')
        self.soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
        self.parent = self.soup.package.metadata

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<metadata>' \
              '<dc:type>Test</dc:type>' \
              '</metadata>'
        self.assertEqual(xml, str(self.parent))


class MetaDataTest(unittest.TestCase):
    def setUp(self):
        ids = [meta.Identifier(value='identifier', id='identifier-id')]
        languages = [meta.Language(id='language-id', value='en-US')]
        titles = [meta.Title(id='title-id', value='Test Title')]
        modified = datetime.datetime(1987, 6, 5)
        self.meta = meta.MetaData(identifiers=ids, languages=languages, titles=titles,
                                  modified=modified)
        self.soup = bs4.BeautifulSoup("<package/>", "xml")
        self.parent = self.soup.package

    def test_basic(self):
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">' \
              '<dc:title id="title-id">Test Title</dc:title>' \
              '<dc:identifier id="identifier-id">identifier</dc:identifier>' \
              '<dc:language id="language-id">en-US</dc:language>' \
              '<meta property="dcterms:modified">1987-06-05T00:00:00</meta>' \
              '</metadata>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_contributor(self):
        contributor = meta.Contributor(id='contributor-id', role='Illustrator',
                                       value='Bob')
        self.meta.contributors.append(contributor)
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">' \
              '<dc:title id="title-id">Test Title</dc:title>' \
              '<dc:identifier id="identifier-id">identifier</dc:identifier>' \
              '<dc:contributor id="contributor-id">' \
              'Bob' \
              '</dc:contributor>' \
              '<meta property="role" refines="contributor-id">' \
              'Illustrator' \
              '</meta>' \
              '<dc:language id="language-id">en-US</dc:language>' \
              '<meta property="dcterms:modified">1987-06-05T00:00:00</meta>' \
              '</metadata>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_multiple_contributors(self):
        values = ['Bob', 'Jake', 'Sue']
        roles = ['Illustrator', 'Chef', 'Scientist']
        ids = ['contributor_{}'.format(i) for i in range(3)]
        contributors = [meta.Contributor(value=value, role=role, id=id)
                        for value, role, id in zip(values, roles, ids)]
        self.meta.contributors = contributors
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">' \
              '<dc:title id="title-id">Test Title</dc:title>' \
              '<dc:identifier id="identifier-id">identifier</dc:identifier>' \
              '<dc:contributor id="contributor_0">' \
              'Bob' \
              '</dc:contributor>' \
              '<meta property="display-seq" refines="contributor_0">' \
              '0' \
              '</meta>' \
              '<meta property="role" refines="contributor_0">' \
              'Illustrator' \
              '</meta>' \
              '<dc:contributor id="contributor_1">' \
              'Jake' \
              '</dc:contributor>' \
              '<meta property="display-seq" refines="contributor_1">' \
              '1' \
              '</meta>' \
              '<meta property="role" refines="contributor_1">' \
              'Chef' \
              '</meta>' \
              '<dc:contributor id="contributor_2">' \
              'Sue' \
              '</dc:contributor>' \
              '<meta property="display-seq" refines="contributor_2">' \
              '2' \
              '</meta>' \
              '<meta property="role" refines="contributor_2">' \
              'Scientist' \
              '</meta>' \
              '<dc:language id="language-id">en-US</dc:language>' \
              '<meta property="dcterms:modified">1987-06-05T00:00:00</meta>' \
              '</metadata>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_coverages(self):
        coverage = meta.Coverage(value='USA', id=None)
        self.meta.contributors.append(coverage)
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">' \
              '<dc:title id="title-id">Test Title</dc:title>' \
              '<dc:identifier id="identifier-id">identifier</dc:identifier>' \
              '<dc:coverage>' \
              'USA' \
              '</dc:coverage>' \
              '<dc:language id="language-id">en-US</dc:language>' \
              '<meta property="dcterms:modified">1987-06-05T00:00:00</meta>' \
              '</metadata>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_multiple_coverages(self):
        values = ['USA', 'France', 'Germany']
        ids = ['coverage_{}'.format(i) for i in range(3)]
        coverages = [meta.Coverage(value=value, id=_id) for value, _id in zip(values, ids)]
        self.meta.coverages = coverages
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">' \
              '<dc:title id="title-id">Test Title</dc:title>' \
              '<dc:identifier id="identifier-id">identifier</dc:identifier>' \
              '<dc:coverage id="coverage_0">' \
              'USA' \
              '</dc:coverage>' \
              '<meta property="display-seq" refines="coverage_0">' \
              '0' \
              '</meta>' \
              '<dc:coverage id="coverage_1">' \
              'France' \
              '</dc:coverage>' \
              '<meta property="display-seq" refines="coverage_1">' \
              '1' \
              '</meta>' \
              '<dc:coverage id="coverage_2">' \
              'Germany' \
              '</dc:coverage>' \
              '<meta property="display-seq" refines="coverage_2">' \
              '2' \
              '</meta>' \
              '<dc:language id="language-id">en-US</dc:language>' \
              '<meta property="dcterms:modified">1987-06-05T00:00:00</meta>' \
              '</metadata>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

    def test_major(self):
        self.meta.creators = [meta.Creator(value='Bram Stoker', id=None)]
        self.meta.titles = [meta.Title(value='Dracula '
                                             '(Barnes & Noble Classics Series)', id=None)]
        self.meta.rights = [meta.Rights(value='NONE', id=None)]
        self.meta.identifiers = [meta.Identifier(value='9781411431645', id='book-id')]
        self.meta.languages = [meta.Language(value='en', id=None)]
        self.meta.publishers = [meta.Publisher(value='Barnes&Noble', id=None)]
        self.meta.append_to_document(self.parent, self.soup)
        xml = '<package>' \
              '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">' \
              '<dc:title>Dracula (Barnes &amp; Noble Classics Series)</dc:title>' \
              '<dc:creator>Bram Stoker</dc:creator>' \
              '<dc:identifier id="book-id">9781411431645</dc:identifier>' \
              '<dc:language>en</dc:language>' \
              '<dc:publisher>Barnes&amp;Noble</dc:publisher>' \
              '<dc:rights>NONE</dc:rights>' \
              '<meta property="dcterms:modified">1987-06-05T00:00:00</meta>' \
              '</metadata>' \
              '</package>'
        self.assertEqual(xml, str(self.parent))

if __name__ == '__main__':
    unittest.main()
