""" FeedItemSource dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import json
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
from marshmallow import fields
import avro.schema
import avro.name
import avro.io
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor
from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class FeedItemSource:
    """
    Metadata about the original source feed, useful if the item was republished from another feed.
    Attributes:
        author (typing.Optional[str]): The name of the original author.
        author_detail (typing.Optional[FeedItemAuthor]): Detailed information about the original author.
        contributors (typing.Optional[typing.List[FeedItemAuthor]]): A list of contributors to the source feed.
        icon (typing.Optional[str]): An icon image associated with the source feed.
        id (typing.Optional[str]): A unique identifier for the source feed.
        link (typing.Optional[str]): A link to the source feed.
        links (typing.Optional[typing.List[Link]]): A collection of links related to the source feed.
        logo (typing.Optional[str]): A logo image associated with the source feed.
        rights (typing.Optional[str]): Rights information for the source feed, such as copyright notices.
        subtitle (typing.Optional[str]): A secondary title or tagline for the source feed.
        title (typing.Optional[str]): The title of the source feed.
        updated (typing.Optional[datetime.datetime]): The last updated timestamp of the source feed."""
    
    author: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="author"))
    author_detail: typing.Optional[FeedItemAuthor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="author_detail"))
    contributors: typing.Optional[typing.List[FeedItemAuthor]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contributors"))
    icon: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icon"))
    id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    link: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="link"))
    links: typing.Optional[typing.List[Link]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="links"))
    logo: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="logo"))
    rights: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rights"))
    subtitle: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subtitle"))
    title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    updated: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"FeedItemSource\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Metadata about the original source feed, useful if the item was republished from another feed.\", \"fields\": [{\"name\": \"author\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The name of the original author.\"}, {\"name\": \"author_detail\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemAuthor\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Contains information about the author of the feed item.\", \"fields\": [{\"name\": \"name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The full name of the author.\"}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A URL associated with the author, such as a personal website or profile.\"}, {\"name\": \"email\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The author's email address.\"}]}], \"default\": null, \"doc\": \"Detailed information about the original author.\"}, {\"name\": \"contributors\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"}], \"default\": null, \"doc\": \"A list of contributors to the source feed.\"}, {\"name\": \"icon\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"An icon image associated with the source feed.\"}, {\"name\": \"id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A unique identifier for the source feed.\"}, {\"name\": \"link\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A link to the source feed.\"}, {\"name\": \"links\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"Link\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Represents a hyperlink associated with the feed or feed item.\", \"fields\": [{\"name\": \"rel\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The relationship type of the link, such as 'alternate' or 'self'.\"}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The URL of the link.\"}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The MIME type of the linked resource.\"}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The title or description of the link.\"}]}}], \"default\": null, \"doc\": \"A collection of links related to the source feed.\"}, {\"name\": \"logo\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A logo image associated with the source feed.\"}, {\"name\": \"rights\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Rights information for the source feed, such as copyright notices.\"}, {\"name\": \"subtitle\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A secondary title or tagline for the source feed.\"}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The title of the source feed.\"}, {\"name\": \"updated\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null, \"doc\": \"The last updated timestamp of the source feed.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.author=str(self.author) if self.author else None
        self.author_detail=self.author_detail if isinstance(self.author_detail, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(self.author_detail) if self.author_detail else None if self.author_detail else None
        self.contributors=self.contributors if isinstance(self.contributors, list) else [v if isinstance(v, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(v) if v else None for v in self.contributors] if self.contributors else None if self.contributors else None
        self.icon=str(self.icon) if self.icon else None
        self.id=str(self.id) if self.id else None
        self.link=str(self.link) if self.link else None
        self.links=self.links if isinstance(self.links, list) else [v if isinstance(v, Link) else Link.from_serializer_dict(v) if v else None for v in self.links] if self.links else None if self.links else None
        self.logo=str(self.logo) if self.logo else None
        self.rights=str(self.rights) if self.rights else None
        self.subtitle=str(self.subtitle) if self.subtitle else None
        self.title=str(self.title) if self.title else None
        self.updated=self.updated if self.updated else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'FeedItemSource':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
        """
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        return asdict_result

    def _dict_resolver(self, data):
        """
        Helps resolving the Enum values to their actual values and fixes the key names.
        """ 
        def _resolve_enum(v):
            if isinstance(v,enum.Enum):
                return v.value
            return v
        def _fix_key(k):
            return k[:-1] if k.endswith('_') else k
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data)}

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
                    'application/json': Encodes the data to JSON format.
                Supported content type extensions:
                    '+gzip': Compresses the byte array using gzip, e.g. 'application/json+gzip'.

        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        result = None
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(self.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
            result = stream.getvalue()
        if base_content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member

        if result is not None and content_type.endswith('+gzip'):
            # Handle string result from to_json()
            if isinstance(result, str):
                result = result.encode('utf-8')
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['FeedItemSource']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'avro/binary': Attempts to decode the data from Avro binary encoded format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary encoded format.
                    'avro/json': Attempts to decode the data from Avro JSON encoded format.
                    'application/vnd.apache.avro+json': Attempts to decode the data from Avro JSON encoded format.
                    'application/json': Attempts to decode the data from JSON encoded format.
                Supported content type extensions:
                    '+gzip': First decompresses the data using gzip, e.g. 'application/json+gzip'.
        Returns:
            The dataclass representation of the data.
        """
        if data is None:
            return None
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            return cls.from_serializer_dict(data)

        content_type = (content_type_string or 'application/octet-stream').split(';')[0].strip()

        if content_type.endswith('+gzip'):
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for gzip decompression')
            with gzip.GzipFile(fileobj=stream, mode='rb') as gzip_file:
                data = gzip_file.read()
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro', 'avro/json', 'application/vnd.apache.avro+json']:
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for conversion to Stream')
            reader = avro.io.DatumReader(cls.AvroType)
            if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
                decoder = avro.io.BinaryDecoder(stream)
            else:
                raise NotImplementedError(f'Unsupported Avro media type {content_type}')
            _record = reader.read(decoder)            
            return FeedItemSource.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return FeedItemSource.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')