"""
This is me just messing around with the EPUB specification. I plan to eventually build
this into a full library for creating and editing EPUB files.
"""

import bs4


"""The mimetype string for EPUB version 3.0"""
MIMETYPE = "application/epub+zip"


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

    def to_doc(self):
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
        doc = self.to_doc()
        return doc.prettify()


class PackageDocument:
    pass


class EPub:

    def __init__(self):
        self.container = Container()

    @property
    def mimetype(self):
        return MIMETYPE

    @property
    def version(self):
        return "3.0.1"


