"""
For building and editing EPUB books
"""
import bs4
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


class Manifest:
    """
    Represents the manifest element of the EPUB package

    The manifest element provides an exhaustive list of the Publication Resources that
    constitute the given Rendition, each represented by an item element.
    """
    def __init__(self):
        self.id = None
        self.items = []

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
        self.properties = []
        self.media_overlay = None
        self.set(**kwargs)

    def append_to_document(self, parent, soup):
        tag = soup.new_tag("item", id=self.id, href=self.href)
        tag["media-type"] = self.media_type
        parent.append(tag)
        if self.fallback is not None:
            tag['fallback'] = self.fallback.id
            self.fallback.append_to_document(parent, soup)
        if len(self.properties) > 0:
            tag['properties'] = ' '.join(self.properties)
        if self.media_overlay is not None:
            tag['media-overlay'] = self.media_overlay


class Spine:
    pass


class EPub:

    def __init__(self):
        self.container = Container()

    @property
    def mimetype(self):
        return "application/epub+zip"

    @property
    def version(self):
        return "3.0.1"
