"""
For building and editing EPUB books
"""
import bs4
import os
import re
import abc
import copy
import shutil
import urllib.parse
from epub import meta
from epub import util


class Container:
    """
    The container represents an XML file that is used to point to various renditions of a
    book.
    """

    def __init__(self, root_files=None):
        if root_files is None:
            self.root_files = []
        else:
            self.root_files = root_files
        self.version = "1.0"
        self.xmlns = "urn:oasis:names:tc:opendocument:xmlns:container"

    def register_rendition(self, file: str):
        """
        Register a package document with the container
        :param file: The path to the package document (string)
        """
        self.root_files.append(file)

    def to_document(self):
        """
        Turn the container into an XML document
        :return: The container document in a bs4.BeautifulSoup object
        """
        doc = bs4.BeautifulSoup("<container/>", "xml")
        doc.container["version"] = self.version
        doc.container["xmlns"] = self.xmlns
        doc.container.append(doc.new_tag("rootfiles"))
        for root_file in self.root_files:
            tag = doc.new_tag("rootfile")
            tag["full-path"] = root_file
            tag["media-type"] = "application/oebps-package+xml"
            doc.container.rootfiles.append(tag)
        return doc

    def __str__(self):
        return self.to_document().prettify()


class PackageDocument:
    """
    Represents the package document in the EPUB

    The package element is the root container of the Package Document and encapsulates
    metadata and resource information for a Rendition.
    """

    def __init__(self):
        self.version = "3.0"
        self.unique_identifier = "BookID"
        self.prefix = None
        self.language = None
        self.text_direction = None
        self.id = None
        self.meta_data = meta.MetaData()
        self.manifest = Manifest()
        self.spine = Spine()
        self.bindings = None
        self.collection = []
        self.path = 'content.opf'

    def register_chapter(self, chapter):
        item = self.manifest.register_chapter(chapter.path)
        self.spine.append_item(item)

    def register_table_of_contents(self, table_of_contents):
        item = self.manifest.register_table_of_contents(table_of_contents)
        self.spine.toc = item.id

    def to_document(self):
        soup = bs4.BeautifulSoup('<package xmlns:opf="http://www.idpf.org/2007/opf"/>',
                                 'xml')
        pack = soup.package
        pack['version'] = self.version
        pack['unique_identifier'] = self.unique_identifier
        if self.prefix is not None:
            pack['prefix'] = self.prefix
        if self.language is not None:
            pack['language'] = self.language
        if self.text_direction is not None:
            pack['xml:lang'] = self.language
        if self.id is not None:
            pack['id'] = self.id
        self.meta_data.append_to_document(pack, soup)
        self.manifest.append_to_document(pack, soup)
        self.spine.append_to_document(pack, soup)
        return soup

    def write(self, base_dir):
        doc = self.to_document()
        file_name = '{}/{}'.format(base_dir, self.path)
        with open(file_name, 'w') as f:
            print(doc.prettify(formatter="html"), file=f)


class Manifest(util.SetGet):
    """
    Represents the manifest element of the EPUB package

    The manifest element provides an exhaustive list of the Publication Resources that
    constitute the given Rendition, each represented by an item element.
    """
    def __init__(self, **kwargs):
        self.id = None
        self.items = []
        self.set(**kwargs)

    def register_chapter(self, chapter_path):
        parts = chapter_path.split('/')
        chapter_id = parts[-1]
        item = Item(href=chapter_path, id=chapter_id, media_type='application/xhtml+xml')
        self.items.append(item)
        return item

    def register_table_of_contents(self, toc):
        parts = toc.path_v2.split('/')
        toc_id_v2 = parts[-1]
        item_v2 = Item(href=toc.path_v2, id=toc_id_v2,
                       media_type="application/x-dtbncx+xml")
        self.items.append(item_v2)
        parts = toc.path_v3.split('/')
        toc_id_v3 = parts[-1]
        item_v3 = Item(href=toc.path_v3, id=toc_id_v3, is_nav=True,
                       media_type='application/xhtml+xml')
        self.items.append(item_v3)
        return item_v2

    def append_to_document(self, parent, soup):
        tag = soup.new_tag('manifest')
        parent.append(tag)
        if self.id is not None:
            tag['id'] = self.id
        for item in self.items:
            item.append_to_document(tag, soup)


class Item(util.SetGet):
    """
    The item element represents a Publication Resource, such as a chapter
    """
    def __init__(self, **kwargs):
        self.id = ''
        self.href = ''
        self.media_type = ''
        self.fallback = None
        self.media_overlay = None
        self.is_cover_image = False
        self.is_mathml = False
        self.is_nav = False
        self.has_remote_resources = False
        self.is_scripted = False
        self.is_svg = False
        self.is_switch = False
        self.set(**kwargs)

    def append_to_document(self, parent, soup):
        tag = soup.new_tag("item", id=self.id, href=self.href)
        tag["media-type"] = self.media_type
        parent.append(tag)
        if self.fallback is not None:
            tag['fallback'] = self.fallback.id
            self.fallback.append_to_document(parent, soup)
        self.append_properties(tag)
        if self.media_overlay is not None:
            tag['media-overlay'] = self.media_overlay

    def append_properties(self, tag):
        properties = []
        if self.is_cover_image:
            properties.append('cover-image')
        if self.is_mathml:
            properties.append('mathml')
        if self.is_nav:
            properties.append('nav')
        if self.has_remote_resources:
            properties.append('remote-resources')
        if self.is_scripted:
            properties.append('scripted')
        if self.is_svg:
            properties.append('svg')
        if self.is_switch:
            properties.append('switch')
        if len(properties) > 0:
            tag['properties'] = ' '.join(properties)


class ItemRef(util.SetGet):
    """
     itemref elements of the spine represent a sequential list of Publication Resources
     (typically EPUB Content Documents). The order of the itemref elements defines the
     default reading order of the given Rendition of the EPUB Publication.
    """
    def __init__(self, item, **kwargs):
        self.item = item
        self.is_primary = None
        self.id = None
        self.is_x_aligned_center = False
        self.flow_mode = None
        self.layout_mode = None
        self.orientation = None
        self.page_spread = None
        self.spread_condition = None
        self.set(**kwargs)

    def append_to_document(self, parent, soup):
        tag = soup.new_tag('itemref')
        tag['idref'] = self.item.id
        parent.append(tag)
        if self.is_primary is not None:
            tag['linear'] = 'yes' if self.is_primary else 'no'
        if self.id is not None:
            tag['id'] = self.id
        self.append_properties(tag)

    def append_properties(self, tag):
        properties = []
        if self.is_x_aligned_center:
            properties.append('rendition:align-x-center')
        if self.flow_mode is not None:
            properties.append('rendition:flow-{}'.format(self.flow_mode))
        if self.layout_mode is not None:
            properties.append('rendition:layout-{}'.format(self.layout_mode))
        if self.orientation is not None:
            properties.append('rendition:orientation-{}'.format(self.orientation))
        if self.page_spread == 'center':
            properties.append('rendition:page-spread-center')
        elif self.page_spread in ['left', 'right']:
            properties.append('page-spread-{}'.format(self.page_spread))
        if self.spread_condition is not None:
            properties.append('rendition:spread-{}'.format(self.spread_condition))
        if len(properties) > 0:
            tag['properties'] = ' '.join(properties)


class Spine(util.SetGet):
    """
    The spine element defines the default reading order of the given Rendition of the
    EPUB Publication content by defining an ordered list of manifest item references.
    """
    def __init__(self, **kwargs):
        self.id = None
        self.toc = None
        self.page_progression_direction = None
        self.itemrefs = []
        self.set(**kwargs)

    def append_item(self, item, **kwargs):
        itemref = ItemRef(item, **kwargs)
        self.itemrefs.append(itemref)
        return itemref

    def append_to_document(self, parent, soup):
        tag = soup.new_tag('spine')
        parent.append(tag)
        if self.id is not None:
            tag['id'] = self.id
        if self.toc is not None:
            tag['toc'] = self.toc
        if self.page_progression_direction is not None:
            tag['page-progression-direction'] = self.page_progression_direction
        for itemref in self.itemrefs:
            itemref.append_to_document(tag, soup)


class Bindings(util.SetGet):
    """
    TODO
    """
    pass


class EPub(util.SetGet):

    def __init__(self, **kwargs):
        self.container = Container()
        self.books = []
        self.path = None
        self.set(**kwargs)
        if self.path is None:
            self.path = os.path.expanduser('~/generated_epubs')

    @property
    def mimetype(self):
        return "application/epub+zip"

    @property
    def version(self):
        return "3.0.1"

    @property
    def directories(self):
        return [self.root_dir,
                self.meta_inf_dir,
                self.content_dir,
                self.text_dir,
                self.images_dir,
                self.styles_dir]

    @property
    def root_dir(self):
        title = self.books[0].title.casefold()
        return "{}/{}".format(self.path, re.sub("[^a-z0-9]", "_", title))

    @property
    def meta_inf_dir(self):
        return "{}/{}".format(self.root_dir, "META-INF")

    @property
    def content_dir(self):
        return "{}/{}".format(self.root_dir, "CONTENT")

    @property
    def text_dir(self):
        return "{}/{}".format(self.content_dir, "Text")

    @property
    def images_dir(self):
        return "{}/{}".format(self.content_dir, "Images")

    @property
    def styles_dir(self):
        return "{}/{}".format(self.content_dir, "Styles")

    def generate(self):
        self.create_directory_structure()
        self.write_mimetype()
        self.process_books()
        self.write_container()
        self.compress()

    def create_directory_structure(self):
        shutil.rmtree(self.root_dir, ignore_errors=True)
        for directory in self.directories:
            os.makedirs(directory, exist_ok=True)

    def write_mimetype(self):
        mimetype_file = "{}/{}".format(self.root_dir, "mimetype")
        with open(mimetype_file, 'w') as f:
            print("application/epub+zip", file=f)

    def process_books(self):
        for book_num, book in enumerate(self.books):
            book.base_path = self.content_dir
            book.specific_path = 'content_{}.opf'.format(book_num)
            self.container.register_rendition('CONTENT/{}'.format(book.specific_path))
            book.process()

    def write_container(self):
        container_file = "{}/{}".format(self.meta_inf_dir, "container.xml")
        with open(container_file, 'w') as f:
            print(str(self.container), file=f)

    def compress(self):
        zip_name = shutil.make_archive(self.root_dir, 'zip', self.root_dir)
        shutil.move(zip_name, '{}.epub'.format(self.root_dir))
        shutil.rmtree(self.root_dir, ignore_errors=True)


class Book(util.SetGet):
    """
    An iterable class for chapters a book
    """

    def __init__(self, first_chapter, **kwargs):
        self.package_document = PackageDocument()
        self.table_of_contents = TableOfContents(self)
        self.base_path = None
        self.specific_path = 'content.opf'
        self._current_chapter_index = 0
        self._chapters = [TitleChapter(self), first_chapter]
        self.set(**kwargs)

    def process(self):
        self.process_chapters()
        self.package_document.register_table_of_contents(self.table_of_contents)
        self.package_document.write(self.base_path)
        self.table_of_contents.write(self.base_path)

    def process_chapters(self):
        for chapter_num, chapter in enumerate(self):
            chapter.number = chapter_num
            self.package_document.register_chapter(chapter)
            chapter.write(self.base_path)

    @property
    def specific_path(self):
        return self.package_document.path

    @specific_path.setter
    def specific_path(self, value):
        self.package_document.path = value

    @property
    def title(self):
        return self.package_document.meta_data.titles[0].value

    @title.setter
    def title(self, title):
        self.package_document.meta_data.titles[0].value = title

    def __iter__(self):
        self._current_chapter_index = -1
        return self

    def __getitem__(self, item):
        if isinstance(item, slice):
            max_index = item.stop-1
        elif isinstance(item, int):
            max_index = item
        else:
            raise TypeError

        while max_index >= len(self._chapters) or item < 0:
            try:
                self._chapters.append(next(self._chapters[-1]))
            except StopIteration:
                raise IndexError
        return self._chapters[item]

    def __setitem__(self, key, value):
        # ensure that the required chapters have been loaded up until this point
        self[key]
        self._chapters[key] = value

    def __next__(self):
        self._current_chapter_index += 1
        while self._current_chapter_index >= len(self._chapters):
            self._chapters.append(next(self._chapters[-1]))
        return self._chapters[self._current_chapter_index]


class TableOfContents:
    _DEFAULT_XML_V2 = """
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en-US">
          <head/>
          <docTitle/>
          <navMap/>
        </ncx>"""

    _DEFAULT_XML_V3 = """
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\
          <head>
            <title/>
          </head>
          <body>
            <nav epub:type="toc">
              <h1>Table of Contents</h1>
              <ol/>
            </nav>
          </body>
        </html>"""

    def __init__(self, book):
        self.book = book
        self.chapters = []

    @property
    def path_v2(self):
        return 'toc.ncx'

    @property
    def path_v3(self):
        return 'toc.xhtml'

    def register_chapter(self, chapter):
        self.chapters.append(chapter)

    def generate_version_2_document(self):
        soup = bs4.BeautifulSoup(self._DEFAULT_XML_V2, 'xml')
        title_tag = soup.new_tag('text')
        soup.ncx.docTitle.append(title_tag)
        title_tag.append(bs4.NavigableString(self.book.title))
        parent = soup.ncx.navMap
        for chapter in self.book:
            self.append_chapter_to_document_v2(chapter, parent, soup)
        return soup

    @staticmethod
    def append_chapter_to_document_v2(chapter, parent, soup):
        nav_point = soup.new_tag('navPoint', playOrder=chapter.number+1)
        parent.append(nav_point)
        nav_label = soup.new_tag('navLabel')
        nav_point.append(nav_label)
        text = soup.new_tag('text')
        nav_label.append(text)
        text.append(bs4.NavigableString(chapter.title))
        content = soup.new_tag('content', src=chapter.path)
        nav_point.append(content)

    def generate_version_3_document(self):
        soup = bs4.BeautifulSoup(self._DEFAULT_XML_V3, 'xml')
        soup.head.title.append(bs4.NavigableString(self.book.title))
        parent = soup.html.body.nav.ol
        for chapter in self.book:
            self.append_chapter_to_document_v3(chapter, parent, soup)
        return soup

    @staticmethod
    def append_chapter_to_document_v3(chapter, parent, soup):
        li = soup.new_tag('li')
        parent.append(li)
        a = soup.new_tag('a', href=chapter.path)
        li.append(a)
        a.append(bs4.NavigableString(chapter.title))

    def write(self, base_dir):
        doc_v2 = self.generate_version_2_document()
        file_name = '{}/{}'.format(base_dir, self.path_v2)
        print('Writing Table of Contents as "{}".'.format(file_name))
        with open(file_name, 'w') as f:
            print(doc_v2.prettify(formatter="html"), file=f)
        doc_v3 = self.generate_version_3_document()
        file_name = '{}/{}'.format(base_dir, self.path_v3)
        print('Writing Table of Contents as "{}".'.format(file_name))
        with open(file_name, 'w') as f:
            print(doc_v3.prettify(formatter="html"), file=f)


class Chapter(util.SetGet, metaclass=abc.ABCMeta):
    """
    Stores chapter data
    """
    _DEFAULT_XHTML = '\
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\
          <head><title></title><link rel="stylesheet" ' \
                     'href="../Styles/default_style.css" type="text/css"/></head>\
          <body><h1></h1></body>\
        </html>\
        '

    def __init__(self, number=0):
        self.number = number

    @property
    def path(self):
        return 'Text/chapter_{:03}.xhtml'.format(self.number)

    @property
    def title(self) -> bs4.Tag:
        """
        The title Tag of the chapter
        """
        return self.get_title()

    @property
    def content(self) -> bs4.Tag:
        """
        The content tag that contains all the chapter text
        """
        return self.get_content()

    def create_document(self) -> bs4.BeautifulSoup:
        """Create and return a BeautifulSoup document containing the chapter"""
        doc = bs4.BeautifulSoup(WebChapter._DEFAULT_XHTML, "xml")
        doc.head.title.string = self.title
        doc.body.h1.string = self.title
        doc.body.append(copy.copy(self.content))
        return doc

    def write(self, base_directory: str):
        """
        Write the chapter to a file

        :param base_directory: where to write the chapter
        """
        doc = self.create_document()
        file_name = '{}/{}'.format(base_directory, self.path)
        print('Writing Chapter "{}" as "{}".'.format(self.title, file_name))
        with open(file_name, 'w') as f:
            print(doc.prettify(formatter="minimal"), file=f)

    @abc.abstractmethod
    def get_title(self) -> str:
        """Return the title of the chapter"""
        pass

    @abc.abstractmethod
    def get_content(self) -> bs4.Tag:
        """Return the content of the chapter"""
        pass

    def __iter__(self):
        return self

    @abc.abstractmethod
    def __next__(self):
        pass


class WebChapter(Chapter):
    """
    Retrieves chapter content from the web
    """

    def __init__(self, url, **kwargs):
        self.url = url
        self.raw_html = None
        self.parsed_html = None
        self.set(**kwargs)
        if self.raw_html is None:
            self.load_html()
        if self.parsed_html is None:
            self.parsed_html = bs4.BeautifulSoup(self.raw_html, 'lxml')

    @property
    def next_chapter_url(self):
        """
        The URL of the next chapter
        """
        return self.get_next_chapter_url()

    def load_html(self, url=None):
        if url is None:
            url = self.url
        else:
            self.url = url
        self.raw_html = util.read_html(url)

    def fix_url(self, raw_url: str) -> str:
        """
        Fix the URL if it is a relative URL

        :param raw_url: the raw url to fix
        :return: An absolute URL
        """
        if raw_url is not None and len(raw_url) > 2 and raw_url[0:2] == "..":
            return urllib.parse.urljoin(self.url, raw_url)
        else:
            return raw_url

    def __next__(self):
        url = self.fix_url(self.get_next_chapter_url())
        if url is None or len(url) == 0:
            raise StopIteration
        else:
            return self.__class__(url)

    @abc.abstractmethod
    def get_next_chapter_url(self) -> str:
        """Return the URL of the next chapter"""
        pass

    @abc.abstractmethod
    def get_title(self) -> str:
        """Return the title of the chapter"""
        pass

    @abc.abstractmethod
    def get_content(self) -> bs4.Tag:
        """Return the content of the chapter"""
        pass


class TitleChapter(Chapter):

    def __init__(self, book):
        self.book = book

    def __next__(self):
        return self.book[1]

    def get_title(self) -> str:
        return self.book.title

    def get_content(self):
        return bs4.Tag(name='div')
