"""
Contains all classes and functions related to EPUB meta-data
"""
import datetime

from abc import abstractmethod
from abc import ABCMeta

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


class MetaDataProperty(metaclass=ABCMeta):
    """
    Base class for all meta-data items
    """
    def __init__(self):
        self.value = ""
        self.id = ""
        self.file_as = None
        self.alternative_script = None
        self.display_seq = None
        self.meta_authority = None

    @abstractmethod
    def to_tag(self):
        pass


class Person(MetaDataProperty):
    """
    Base class for Creator and Contributor
    """
    def __init__(self):
        super().__init__()
        self.role = None

    @abstractmethod
    def to_tag(self):
        pass


class Collection(MetaDataProperty):
    """
    identifies the name of a collection to which the EPUB Publication belongs.
    """
    def __init__(self):
        super().__init__()
        self.type = None
        self.group_position = None
        self.identifier = None
        self.collections = []

    def to_tag(self):
        pass


class Contributor(Person):
    """
    An entity responsible for making contributions to the resource.

    Comment:    Examples of a Contributor include a person, an organization, or a service.
                Typically, the name of a Contributor should be used to indicate the
                entity.
    """

    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


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

    def to_tag(self):
        pass


class Creator(Person):
    """
    An entity primarily responsible for making the resource.

    Comment:    Examples of a Creator include a person, an organization, or a service.
                Typically, the name of a Creator should be used to indicate the entity.
    """
    def __init__(self):
        super().__init__()

    def to_tag(self):
        pass


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

    def to_tag(self):
        pass


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
