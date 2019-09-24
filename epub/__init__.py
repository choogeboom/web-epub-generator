"""
For building and editing EPUB books
"""
import pathlib
from typing import (
    Sequence,
    ClassVar,
    List,
    Optional,
    Any,
    Iterator,
    TypeVar,
    MutableSequence,
    Union,
    overload,
)

import bs4
import os
import re
import abc
import copy
import shutil

import dataclasses

from epub import meta
from epub import util


@dataclasses.dataclass()
class Container(util.Documentable):
    """
    The container represents an XML file that is used to point to various renditions of a
    book.
    """

    root_files: List[str] = dataclasses.field(default_factory=list)
    version: str = "1.0"
    xmlns: str = "urn:oasis:names:tc:opendocument:xmlns:container"

    def register_rendition(self, file: str) -> None:
        """
        Register a package document with the container
        :param file: The path to the package document (string)
        """
        self.root_files.append(file)

    def to_document(self) -> bs4.BeautifulSoup:
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


@dataclasses.dataclass()
class Item:
    """
    The item element represents a Publication Resource, such as a chapter
    """

    id: str = ""
    href: str = ""
    media_type: str = ""
    fallback: Optional["Item"] = None
    media_overlay: Optional[str] = None
    is_cover_image: bool = False
    is_mathml: bool = False
    is_nav: bool = False
    has_remote_resources: bool = False
    is_scripted: bool = False
    is_svg: bool = False
    is_switch: bool = False

    def append_to_document(self, parent: bs4.Tag, soup: bs4.BeautifulSoup) -> None:
        tag = soup.new_tag("item", id=self.id, href=self.href)
        tag["media-type"] = self.media_type
        parent.append(tag)
        if self.fallback is not None:
            tag["fallback"] = self.fallback.id
            self.fallback.append_to_document(parent, soup)
        self.append_properties(tag)
        if self.media_overlay is not None:
            tag["media-overlay"] = self.media_overlay

    def append_properties(self, tag: bs4.Tag) -> None:
        properties = []
        if self.is_cover_image:
            properties.append("cover-image")
        if self.is_mathml:
            properties.append("mathml")
        if self.is_nav:
            properties.append("nav")
        if self.has_remote_resources:
            properties.append("remote-resources")
        if self.is_scripted:
            properties.append("scripted")
        if self.is_svg:
            properties.append("svg")
        if self.is_switch:
            properties.append("switch")
        if len(properties) > 0:
            tag["properties"] = " ".join(properties)


@dataclasses.dataclass()
class ItemRef:
    """
     itemref elements of the spine represent a sequential list of Publication Resources
     (typically EPUB Content Documents). The order of the itemref elements defines the
     default reading order of the given Rendition of the EPUB Publication.
    """

    item: Item
    is_primary: Optional[bool] = None
    id: Optional[str] = None
    is_x_aligned_center: bool = False
    flow_mode: Optional[str] = None
    layout_mode: Optional[str] = None
    orientation: Optional[str] = None
    page_spread: Optional[str] = None
    spread_condition: Optional[str] = None

    def append_to_document(self, parent: bs4.Tag, soup: bs4.BeautifulSoup) -> None:
        tag = soup.new_tag("itemref")
        tag["idref"] = self.item.id
        parent.append(tag)
        if self.is_primary is not None:
            tag["linear"] = "yes" if self.is_primary else "no"
        if self.id is not None:
            tag["id"] = self.id
        self.append_properties(tag)

    def append_properties(self, tag: bs4.Tag) -> None:
        properties = []
        if self.is_x_aligned_center:
            properties.append("rendition:align-x-center")
        if self.flow_mode is not None:
            properties.append("rendition:flow-{}".format(self.flow_mode))
        if self.layout_mode is not None:
            properties.append("rendition:layout-{}".format(self.layout_mode))
        if self.orientation is not None:
            properties.append("rendition:orientation-{}".format(self.orientation))
        if self.page_spread == "center":
            properties.append("rendition:page-spread-center")
        elif self.page_spread in ["left", "right"]:
            properties.append("page-spread-{}".format(self.page_spread))
        if self.spread_condition is not None:
            properties.append("rendition:spread-{}".format(self.spread_condition))
        if len(properties) > 0:
            tag["properties"] = " ".join(properties)


@dataclasses.dataclass()
class Manifest:
    """
    Represents the manifest element of the EPUB package

    The manifest element provides an exhaustive list of the Publication Resources that
    constitute the given Rendition, each represented by an item element.
    """

    id: Optional[str] = None
    items: List[Item] = dataclasses.field(default_factory=list)

    def register_chapter(self, chapter_path: str) -> Item:
        parts = chapter_path.split("/")
        chapter_id = parts[-1]
        item = Item(
            href=chapter_path, id=chapter_id, media_type="application/xhtml+xml"
        )
        self.items.append(item)
        return item

    def register_table_of_contents(self, toc: "TableOfContents") -> Item:
        parts = toc.path_v2.split("/")
        toc_id_v2 = parts[-1]
        item_v2 = Item(
            href=toc.path_v2, id=toc_id_v2, media_type="application/x-dtbncx+xml"
        )
        self.items.append(item_v2)
        parts = toc.path_v3.split("/")
        toc_id_v3 = parts[-1]
        item_v3 = Item(
            href=toc.path_v3,
            id=toc_id_v3,
            is_nav=True,
            media_type="application/xhtml+xml",
        )
        self.items.append(item_v3)
        return item_v2

    def append_to_document(self, parent: bs4.Tag, soup: bs4.BeautifulSoup) -> None:
        tag = soup.new_tag("manifest")
        parent.append(tag)
        if self.id is not None:
            tag["id"] = self.id
        for item in self.items:
            item.append_to_document(tag, soup)


T = TypeVar("T", covariant=True)


class Chapter(util.SetGet, abc.ABC):
    """
    Stores chapter data
    """

    _DEFAULT_XHTML: ClassVar[
        str
    ] = '\
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\
          <head><title></title><link rel="stylesheet" href="../Styles/default_style.css" type="text/css"/></head>\
          <body><h1></h1></body>\
        </html>\
        '

    def __init__(self, number: int = 0):
        self.number = number

    @property
    def path(self) -> str:
        fixed_title = re.sub(r"\W", "_", self.title)
        return f"Text/chapter_{self.number:03}_{fixed_title}.xhtml"

    @property
    def title(self) -> str:
        """
        The title Tag of the chapter
        """
        return self.get_title()

    @property
    def content(self) -> Sequence[bs4.Tag]:
        """
        The content tag that contains all the chapter text
        """
        return self.get_content()

    def create_document(self) -> bs4.BeautifulSoup:
        """Create and return a BeautifulSoup document containing the chapter"""
        doc = bs4.BeautifulSoup(Chapter._DEFAULT_XHTML, "xml")
        doc.head.title.string = self.title
        doc.body.h1.string = self.title
        for item in self.content:
            doc.body.append(copy.copy(item))
        return doc

    def write(self, base_directory: pathlib.Path) -> None:
        """
        Write the chapter to a file

        :param base_directory: where to write the chapter
        """
        doc = self.create_document()
        file_name = base_directory / self.path
        print('Writing Chapter "{}" as "{}".'.format(self.title, file_name))
        with open(file_name, "w", encoding="UTF-8") as f:
            print(doc.prettify(formatter="minimal"), file=f)

    @abc.abstractmethod
    def get_title(self) -> str:
        """Return the title of the chapter"""
        pass

    @abc.abstractmethod
    def get_content(self) -> bs4.Tag:
        """Return the content of the chapter"""
        pass

    def __iter__(self: T) -> T:
        return self

    @abc.abstractmethod
    def __next__(self) -> "Chapter":
        pass


class TitleChapter(Chapter):
    def __init__(self, book: "Book"):
        super().__init__(0)
        self.book = book

    def __next__(self) -> Chapter:
        return self.book[1]

    def get_title(self) -> str:
        return self.book.title

    def get_content(self) -> bs4.Tag:
        return bs4.Tag(name="div")


class Book:
    """
    An iterable class for chapters a book
    """

    def __init__(
        self,
        first_chapter: Chapter,
        package_document: Optional["PackageDocument"] = None,
        table_of_contents: Optional["TableOfContents"] = None,
        base_path: pathlib.Path = pathlib.Path(""),
        specific_path: str = "content.opf",
    ):
        self.package_document = (
            PackageDocument() if package_document is None else package_document
        )
        self.table_of_contents = (
            TableOfContents(self) if table_of_contents is None else table_of_contents
        )
        self.base_path = base_path
        self.specific_path = specific_path
        self._current_chapter_index: int = 0
        self._chapters = [TitleChapter(self), first_chapter]

    def process(self) -> None:
        self.process_chapters()
        self.package_document.register_table_of_contents(self.table_of_contents)
        self.package_document.write(self.base_path)
        self.table_of_contents.write(self.base_path)

    def process_chapters(self) -> None:
        for chapter_num, chapter in enumerate(self):
            chapter.number = chapter_num
            self.package_document.register_chapter(chapter)
            chapter.write(self.base_path)

    @property
    def specific_path(self) -> str:
        return self.package_document.path

    @specific_path.setter
    def specific_path(self, value: str) -> None:
        self.package_document.path = value

    @property
    def title(self) -> str:
        return self.package_document.meta_data.titles[0].value

    @title.setter
    def title(self, title: str):
        self.package_document.meta_data.titles[0].value = title

    def __iter__(self) -> Iterator[Chapter]:
        self._current_chapter_index = -1
        return self

    @overload
    def __getitem__(self, item: int) -> Chapter:
        ...

    @overload
    def __getitem__(self, item: slice) -> List[Chapter]:
        ...

    def __getitem__(self, item: Union[slice, int]) -> Union[List[Chapter], Chapter]:
        if isinstance(item, slice):
            max_index: int = item.stop - 1 if item.stop else 0
        elif isinstance(item, int):
            max_index = item
        else:
            raise TypeError(f"Illegal index type: {type(item)}")

        while max_index >= len(self._chapters) or max_index < 0:
            try:
                self._chapters.append(next(self._chapters[-1]))
            except StopIteration:
                raise IndexError
        return self._chapters[item]

    def __setitem__(self, key: int, value: Chapter):
        # ensure that the required chapters have been loaded up until this point
        self[key]
        self._chapters[key] = value

    def __next__(self) -> Chapter:
        self._current_chapter_index += 1
        while self._current_chapter_index >= len(self._chapters):
            self._chapters.append(next(self._chapters[-1]))
        return self._chapters[self._current_chapter_index]


@dataclasses.dataclass()
class TableOfContents:
    _DEFAULT_XML_V2: ClassVar[
        str
    ] = """
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en-US">
          <head/>
          <docTitle/>
          <navMap/>
        </ncx>"""

    _DEFAULT_XML_V3: ClassVar[
        str
    ] = """
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

    book: Book
    chapters: List[Chapter] = dataclasses.field(default_factory=list)

    @property
    def path_v2(self) -> str:
        return "toc.ncx"

    @property
    def path_v3(self) -> str:
        return "toc.xhtml"

    def register_chapter(self, chapter: Chapter) -> None:
        self.chapters.append(chapter)

    def generate_version_2_document(self) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(self._DEFAULT_XML_V2, "xml")
        title_tag = soup.new_tag("text")
        soup.ncx.docTitle.append(title_tag)
        title_tag.append(bs4.NavigableString(self.book.title))
        parent = soup.ncx.navMap
        for chapter in self.book:
            self.append_chapter_to_document_v2(chapter, parent, soup)
        return soup

    @staticmethod
    def append_chapter_to_document_v2(
        chapter: Chapter, parent: bs4.Tag, soup: bs4.BeautifulSoup
    ) -> None:
        nav_point = soup.new_tag("navPoint", playOrder=chapter.number + 1)
        parent.append(nav_point)
        nav_label = soup.new_tag("navLabel")
        nav_point.append(nav_label)
        text = soup.new_tag("text")
        nav_label.append(text)
        text.append(bs4.NavigableString(chapter.title))
        content = soup.new_tag("content", src=chapter.path)
        nav_point.append(content)

    def generate_version_3_document(self) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(self._DEFAULT_XML_V3, "xml")
        soup.head.title.append(bs4.NavigableString(self.book.title))
        parent = soup.html.body.nav.ol
        for chapter in self.book:
            self.append_chapter_to_document_v3(chapter, parent, soup)
        return soup

    @staticmethod
    def append_chapter_to_document_v3(
        chapter: Chapter, parent: bs4.Tag, soup: bs4.BeautifulSoup
    ) -> None:
        li = soup.new_tag("li")
        parent.append(li)
        a = soup.new_tag("a", href=chapter.path)
        li.append(a)
        a.append(bs4.NavigableString(chapter.title))

    def write(self, base_dir: pathlib.Path) -> None:
        doc_v2 = self.generate_version_2_document()
        file_name = base_dir / self.path_v2
        print('Writing Table of Contents as "{}".'.format(file_name))
        with open(file_name, "w") as f:
            print(doc_v2.prettify(formatter="html"), file=f)
        doc_v3 = self.generate_version_3_document()
        file_name = base_dir / self.path_v3
        print('Writing Table of Contents as "{}".'.format(file_name))
        with open(file_name, "w") as f:
            print(doc_v3.prettify(formatter="html"), file=f)


@dataclasses.dataclass()
class Spine:
    """
    The spine element defines the default reading order of the given Rendition of the
    EPUB Publication content by defining an ordered list of manifest item references.
    """

    id: Optional[str] = None
    toc: Optional[str] = None
    page_progression_direction: Optional[str] = None
    itemrefs: List[ItemRef] = dataclasses.field(default_factory=list)

    def append_item(self, item: Item, **kwargs) -> ItemRef:
        itemref = ItemRef(item, **kwargs)
        self.itemrefs.append(itemref)
        return itemref

    def append_to_document(self, parent: bs4.Tag, soup: bs4.BeautifulSoup) -> None:
        tag = soup.new_tag("spine")
        parent.append(tag)
        if self.id is not None:
            tag["id"] = self.id
        if self.toc is not None:
            tag["toc"] = self.toc
        if self.page_progression_direction is not None:
            tag["page-progression-direction"] = self.page_progression_direction
        for itemref in self.itemrefs:
            itemref.append_to_document(tag, soup)


@dataclasses.dataclass()
class PackageDocument(util.Documentable):
    """
    Represents the package document in the EPUB

    The package element is the root container of the Package Document and encapsulates
    metadata and resource information for a Rendition.
    """

    version: str = "3.0"
    unique_identifier: str = "BookID"
    prefix: Optional[str] = None
    language: Optional[str] = None
    text_direction: Optional[str] = None
    id: Optional[str] = None
    meta_data: meta.MetaData = dataclasses.field(default_factory=meta.MetaData)
    manifest: Manifest = dataclasses.field(default_factory=Manifest)
    spine: Spine = dataclasses.field(default_factory=Spine)
    bindings: Optional[str] = None
    collection: List = dataclasses.field(default_factory=list)
    path: str = "content.opf"

    def register_chapter(self, chapter: Chapter) -> None:
        item = self.manifest.register_chapter(chapter.path)
        self.spine.append_item(item)

    def register_table_of_contents(self, table_of_contents: TableOfContents) -> None:
        item = self.manifest.register_table_of_contents(table_of_contents)
        self.spine.toc = item.id

    def to_document(self) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(
            '<package xmlns:opf="http://www.idpf.org/2007/opf"/>', "xml"
        )
        pack = soup.package
        pack["version"] = self.version
        pack["unique_identifier"] = self.unique_identifier
        if self.prefix is not None:
            pack["prefix"] = self.prefix
        if self.language is not None:
            pack["language"] = self.language
        if self.text_direction is not None:
            pack["xml:lang"] = self.language
        if self.id is not None:
            pack["id"] = self.id
        self.meta_data.append_to_document(pack, soup)
        self.manifest.append_to_document(pack, soup)
        self.spine.append_to_document(pack, soup)
        return soup

    def write(self, base_dir: pathlib.Path) -> None:
        doc = self.to_document()
        file_name = base_dir / self.path
        with open(file_name, "w") as f:
            print(doc.prettify(formatter="html"), file=f)


class Bindings(util.SetGet):
    """
    TODO
    """

    pass


@dataclasses.dataclass()
class EPub(util.SetGet):
    container: Container = dataclasses.field(default_factory=Container)
    books: List[Book] = dataclasses.field(default_factory=list)
    path: pathlib.Path = pathlib.Path(os.path.expanduser("~/generated_epubs"))

    @property
    def mimetype(self) -> str:
        return "application/epub+zip"

    @property
    def version(self) -> str:
        return "3.0.1"

    @property
    def directories(self) -> Sequence[pathlib.Path]:
        return [
            self.root_dir,
            self.meta_inf_dir,
            self.content_dir,
            self.text_dir,
            self.images_dir,
            self.styles_dir,
        ]

    @property
    def root_dir(self) -> pathlib.Path:
        title = self.books[0].title.casefold()
        return self.path / re.sub("[^a-z0-9]", "_", title)

    @property
    def meta_inf_dir(self) -> pathlib.Path:
        return self.root_dir / "META-INF"

    @property
    def content_dir(self) -> pathlib.Path:
        return self.root_dir / "CONTENT"

    @property
    def text_dir(self) -> pathlib.Path:
        return self.content_dir / "Text"

    @property
    def images_dir(self) -> pathlib.Path:
        return self.content_dir / "Images"

    @property
    def styles_dir(self) -> pathlib.Path:
        return self.content_dir / "Styles"

    def generate(self) -> None:
        self.create_directory_structure()
        self.write_mimetype()
        self.process_books()
        self.write_container()
        self.compress()

    def create_directory_structure(self) -> None:
        shutil.rmtree(self.root_dir, ignore_errors=True)
        for directory in self.directories:
            directory.mkdir(parents=True, exist_ok=True)

    def write_mimetype(self) -> None:
        mimetype_path = self.root_dir / "mimetype"
        with open(mimetype_path, "w") as f:
            print("application/epub+zip", file=f)

    def process_books(self) -> None:
        for book_num, book in enumerate(self.books):
            book.base_path = self.content_dir
            book.specific_path = "content_{}.opf".format(book_num)
            self.container.register_rendition("CONTENT/{}".format(book.specific_path))
            book.process()

    def write_container(self) -> None:
        container_path = self.meta_inf_dir / "container.xml"
        with open(container_path, "w") as f:
            print(str(self.container), file=f)

    def compress(self) -> None:
        zip_name = shutil.make_archive(str(self.root_dir), "zip", self.root_dir)
        shutil.move(zip_name, "{}.epub".format(self.root_dir))
        shutil.rmtree(self.root_dir, ignore_errors=True)
