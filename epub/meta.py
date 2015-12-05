"""
Contains all classes and functions related to EPUB meta-data
"""
import datetime
import bs4
from epub import util


class MetaData:
    def __init__(self, titles=None, languages=None, identifiers=None):
        self.contributors = []
        self.coverages = []
        self.creators = []
        self.dates = []
        self.descriptions = []
        self.formats = []
        self.identifiers = identifiers if identifiers else [Identifier()]
        self.languages = languages if languages else [Language()]
        self.publishers = []
        self.relations = []
        self.rights = []
        self.sources = []
        self.subjects = []
        self.types = []
        self.titles = titles if titles else [Title()]
        self.collections = []
        self.modified = datetime.date.today()

    def append_to_document(self, parent=None):
        """
        Add the meta data object to the document as a child of the specified parent

        :param parent: the parent tag of the meta data object
        :return: The document object
        """
        if parent is None:
            soup = bs4.BeautifulSoup("<package/>", "xml")
            parent = soup.package
        else:
            soup = util.get_soup(parent)

        tag = soup.new_tag("metadata")
        parent.append(tag)
        for contributor in self.contributors:
            contributor.append_to_document(parent=tag)
        for coverage in self.coverages:
            coverage.append_to_document(parent=tag)
        for creator in self.creators:
            creator.append_to_document(parent=tag)
        for date in self.dates:
            date.append_to_document(parent=tag)
        for description in self.descriptions:
            description.append_to_document(parent=tag)
        for fmt in self.formats:
            fmt.append_to_document(parent=tag)
        for identifier in self.identifiers:
            identifier.append_to_document(parent=tag)
        for language in self.languages:
            language.append_to_document(parent=tag)
        for publisher in self.publishers:
            publisher.append_to_document(parent=tag)
        for relation in self.relations:
            relation.append_to_document(parent=tag)
        for right in self.rights:
            right.append_to_document(parent=tag)
        for source in self.sources:
            source.append_to_document(parent=tag)
        for subject in self.subjects:
            subject.append_to_document(parent=tag)
        for tp in self.types:
            tp.append_to_document(parent=tag)
        for title in self.titles:
            title.append_to_document(parent=tag)
        for collection in self.collections:
            collection.append_to_document(parent=tag)
        modified_tag = soup.new_tag("meta")
        modified_tag["property"] = "dcterms:modified"
        modified_tag.append(bs4.NavigableString(self.modified.isoformat()))
        tag.append(modified_tag)

        return tag, soup


class MetaDataProperty:
    """
    Base class for all meta-data items
    """
    def __init__(self):
        self.value = ""
        self.id = util.generate_random_string(12)
        self.file_as = None
        self.alternative_script = None
        self.display_seq = None
        self.meta_authority = None
        self._main_tag_name = "default"

    @staticmethod
    def get_parent_and_soup(parent):
        if parent is None:
            soup = bs4.BeautifulSoup("<package><metadata/></package>", "xml")
            parent = soup.package.metadata
        else:
            soup = util.get_soup(parent)
        return parent, soup

    def append_to_document(self, parent=None):
        parent, soup = MetaDataProperty.get_parent_and_soup(parent)
        self.append_main_tag(parent, soup)
        self.append_alternative_script(parent, soup)
        self.append_display_seq(parent, soup)
        self.append_file_as(parent, soup)
        self.append_meta_authority(parent, soup)
        return parent, soup

    def append_main_tag(self, parent, soup):
        main_tag = soup.new_tag(self._main_tag_name)
        main_tag.append(bs4.NavigableString(self.value))
        parent.append(main_tag)
        if self.id is not None:
            main_tag["id"] = self.id
        return main_tag

    def append_alternative_script(self, parent, soup):
        if self.alternative_script is None:
            return
        as_tag = soup.new_tag(
                              name="meta",
                              property="alternative-script",
                              refines=self.id)
        parent.append(as_tag)
        as_tag.append(bs4.NavigableString(self.alternative_script))

    def append_display_seq(self, parent, soup):
        if self.display_seq is None:
            return
        tag = soup.new_tag(
                           name="meta",
                           property="display-seq",
                           refines=self.id)
        parent.append(tag)
        tag.append(bs4.NavigableString(str(self.display_seq)))

    def append_file_as(self, parent, soup):
        if self.file_as is None:
            return
        tag = soup.new_tag(
                           name="meta",
                           property="file-as",
                           refines=self.id)
        parent.append(tag)
        tag.append(bs4.NavigableString(self.file_as))

    def append_meta_authority(self, parent, soup):
        if self.meta_authority is None:
            return
        tag = soup.new_tag(name="meta", property="meta-auth", refines=self.id)
        parent.append(tag)
        tag.append(bs4.NavigableString(self.meta_authority))


class Person(MetaDataProperty):
    """
    Base class for Creator and Contributor
    """
    def __init__(self):
        super().__init__()
        self.role = None
        self.role_scheme = None
        self._main_tag_name = 'person'

    def append_to_document(self, parent=None):
        parent, soup = super().append_to_document(parent)
        self.append_role(parent, soup)
        return parent, soup

    def append_role(self, parent, soup):
        if self.role is None:
            return
        tag = soup.new_tag(name="meta", property="role", refines=self.id)
        parent.append(tag)
        if self.role_scheme is not None:
            tag["scheme"] = self.role_scheme
        tag.append(bs4.NavigableString(self.role))


class Collection(MetaDataProperty):
    """
    identifies the name of a collection to which the EPUB Publication belongs.
    """
    def __init__(self):
        super().__init__()
        self._main_tag_name = 'meta'
        self.type = None
        self.group_position = None
        self.identifier = None
        self.collection = None
        self.refines_id = None

    def append_to_document(self, parent=None):
        parent, soup = super().append_to_document(parent)
        self.append_type(parent, soup)
        self.append_group_position(parent, soup)
        self.append_identifier(parent, soup)
        self.append_collection(parent)

    def append_main_tag(self, parent, soup):
        main_tag = soup.new_tag("meta", property="belongs-to-collection")
        main_tag.append(bs4.NavigableString(self.value))
        parent.append(main_tag)
        if self.id is not None:
            main_tag["id"] = self.id
        if self.refines_id is not None:
            main_tag["refines"] = self.refines_id
        return main_tag

    def append_type(self, parent, soup):
        if self.type is None:
            return
        tag = soup.new_tag(name="meta", property="collection-type", refines=self.id)
        tag.append(bs4.NavigableString(self.type))
        parent.append(tag)

    def append_group_position(self, parent, soup):
        if self.group_position is None:
            return
        tag = soup.new_tag(name="meta", property="group-position", refines=self.id)
        tag.append(bs4.NavigableString(str(self.group_position)))
        parent.append(tag)

    def append_identifier(self, parent, soup):
        if self.identifier is None:
            return
        tag = soup.new_tag(name="meta", property="dcterms:identifier", refines=self.id)
        tag.append(bs4.NavigableString(self.identifier))
        parent.append(tag)

    def append_collection(self, parent):
        if self.collection is None:
            return
        self.collection.refines_id = self.id
        self.collection.append_to_document(parent)


class Contributor(Person):
    """
    An entity responsible for making contributions to the resource.

    Comment:    Examples of a Contributor include a person, an organization, or a service.
                Typically, the name of a Contributor should be used to indicate the
                entity.
    """

    def __init__(self):
        super().__init__()
        self._main_tag_name = 'dc:contributor'

    def append_to_document(self, parent=None):
        super().append_to_document(parent)


class Coverage(MetaDataProperty):
    """
    The spatial or temporal topic of the resource, the spatial applicability of the
    resource, or the jurisdiction under which the resource is relevant.

    Comment:    Spatial topic and spatial applicability may be a named place or a location
                specified by its geographic coordinates. Temporal topic may be a named
                period, date, or date range. A jurisdiction may be a named
                administrative entity or a geographic place to which the resource
                applies. Recommended best practice is to use a controlled vocabulary
                such as the Thesaurus of Geographic Names [TGN]. Where appropriate,
                named places or time periods can be used in preference to numeric
                identifiers such as sets of coordinates or date ranges.

    References:	[TGN] http://www.getty.edu/research/tools/vocabulary/tgn/index.html
    """
    def __init__(self):
        super().__init__()
        self._main_tag_name = 'dc:coverage'


class Creator(Person):
    """
    An entity primarily responsible for making the resource.

    Comment:    Examples of a Creator include a person, an organization, or a service.
                Typically, the name of a Creator should be used to indicate the entity.
    """
    def __init__(self):
        super().__init__()
        self._main_tag_name = 'dc:creator'


class Date(MetaDataProperty):
    """
    A point or period of time associated with an event in the lifecycle of the resource.

    Comment:	Date may be used to express temporal information at any level of
                granularity. Recommended best practice is to use an encoding scheme,
                such as the W3CDTF profile of ISO 8601 [W3CDTF].

    References:	[W3CDTF] http://www.w3.org/TR/NOTE-datetime
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Description(MetaDataProperty):
    """
    An account of the resource.

    Comment:	Description may include but is not limited to: an abstract, a table of
                contents, a graphical representation, or a free-text account of the
                resource.
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Format(MetaDataProperty):
    """
    The file format, physical medium, or dimensions of the resource.

    Comment:	Examples of dimensions include size and duration. Recommended best
                practice is to use a controlled vocabulary such as the list of Internet
                Media Types [MIME].

    References:	[MIME] http://www.iana.org/assignments/media-types/
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Identifier(MetaDataProperty):
    """
    An unambiguous reference to the resource within a given context.

    Comment:	Recommended best practice is to identify the resource by means of a
                string conforming to a formal identification system.
    """
    def __init__(self):
        super().__init__()
        self.type = None
        self.scheme = None

    def to_tag(self):
        pass


class Language(MetaDataProperty):
    """
    A language of the resource.

    Comment:	Recommended best practice is to use a controlled vocabulary such as
                RFC 4646 [RFC4646].

    References:	[RFC4646] http://www.ietf.org/rfc/rfc4646.txt
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Publisher(MetaDataProperty):
    """
    An entity responsible for making the resource available.

    Comment:	Examples of a Publisher include a person, an organization, or a service.
                Typically, the name of a Publisher should be used to indicate the entity.
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Relation(MetaDataProperty):
    """
    A related resource.

    Comment:	Recommended best practice is to identify the related resource by means of
                a string conforming to a formal identification system.
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Rights(MetaDataProperty):
    """
    Information about rights held in and over the resource.

    Comment:	Typically, rights information includes a statement about various property
                rights associated with the resource, including intellectual property
                rights.
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Source(MetaDataProperty):
    """
    A related resource from which the described resource is derived.

    Comment:	The described resource may be derived from the related resource in whole
                or in part. Recommended best practice is to identify the related
                resource by means of a string conforming to a formal identification
                system.
    """
    def __init__(self):
        super().__init__()
        self.type = None
        self.source_of = None

    def to_tag(self):
        pass


class Subject(MetaDataProperty):
    """
    The topic of the resource.

    Comment:	Typically, the subject will be represented using keywords, key phrases, or
                classification codes. Recommended best practice is to use a controlled
                vocabulary.
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


class Title(MetaDataProperty):
    """
    A name given to the resource.

    Comment:	Typically, a Title will be a name by which the resource is formally known.
    """
    def __init__(self):
        super().__init__()
        self.type = None
        self._main_tag_name = "dc:title"

    def append_to_document(self, parent=None):
        parent, soup = MetaDataProperty.get_parent_and_soup(parent)
        tag = soup.new_tag("title", nsprefix="dc")
        if self.id is not None:
            tag["id"] = self.id
        parent.append(tag)
        tag.append(bs4.NavigableString(self.value))
        if self.type is not None:
            tag = soup.new_tag(
                               "meta",
                               refines=self.id,
                               property="title-type")
            parent.append(tag)
            tag.append(bs4.NavigableString(self.type))
        return tag, soup


class Type(MetaDataProperty):
    """
    The nature or genre of the resource.

    Comment:	Recommended best practice is to use a controlled vocabulary such as the
                DCMI Type Vocabulary [DCMITYPE]. To describe the file format, physical
                medium, or dimensions of the resource, use the Format element.

    References:	[DCMITYPE] http://dublincore.org/documents/dcmi-type-vocabulary/
                http://www.idpf.org/epub/vocab/package/types/
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass
