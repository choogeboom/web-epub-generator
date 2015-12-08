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
    def __init__(self, item):
        self.item = item
        self.is_primary = None
        self.id = None
        self.is_x_aligned_center = False
        self.flow_mode = None
        self.layout_mode = None
        self.orientation = None
        self.page_spread = None
        self.spread_condition = None

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


class EPub:

    def __init__(self):
        self.container = Container()

    @property
    def mimetype(self):
        return "application/epub+zip"

    @property
    def version(self):
        return "3.0.1"
