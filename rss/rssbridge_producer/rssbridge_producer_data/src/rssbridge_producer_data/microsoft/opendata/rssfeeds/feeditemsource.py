""" FeedItemSource dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
import avro.schema
import avro.io
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor
from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link
from datetime import datetime


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class FeedItemSource:
    """
    A FeedItemSource record.
    Attributes:
        author (typing.Optional[str]): 
        author_detail (typing.Optional[FeedItemAuthor]): 
        contributors (typing.Optional[typing.List[FeedItemAuthor]]): 
        icon (typing.Optional[str]): 
        id (typing.Optional[str]): 
        link (typing.Optional[str]): 
        links (typing.Optional[typing.List[Link]]): 
        logo (typing.Optional[str]): 
        rights (typing.Optional[str]): 
        subtitle (typing.Optional[str]): 
        title (typing.Optional[str]): 
        updated (typing.Optional[datetime]): """
    
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
    updated: typing.Optional[datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated"))    
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"FeedItemSource\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"author\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"author_detail\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemAuthor\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"email\", \"type\": [\"null\", \"string\"], \"default\": null}]}], \"default\": null}, {\"name\": \"contributors\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"}], \"default\": null}, {\"name\": \"icon\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"id\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"link\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"links\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"Link\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"rel\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null}]}}], \"default\": null}, {\"name\": \"logo\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"rights\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"subtitle\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"updated\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null}]}"
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.author=str(self.author)
        self.author_detail=self.author_detail if isinstance(self.author_detail, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(self.author_detail) if self.author_detail else None
        self.contributors=self.contributors if isinstance(self.contributors, list) else [v if isinstance(v, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(v) if v else None for v in self.contributors] if self.contributors else None
        self.icon=str(self.icon)
        self.id=str(self.id)
        self.link=str(self.link)
        self.links=self.links if isinstance(self.links, list) else [v if isinstance(v, Link) else Link.from_serializer_dict(v) if v else None for v in self.links] if self.links else None
        self.logo=str(self.logo)
        self.rights=str(self.rights)
        self.subtitle=str(self.subtitle)
        self.title=str(self.title)
        self.updated=self.updated

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
        if content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(self.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
            result = stream.getvalue()
        if content_type == 'application/json':
            result = self.to_json()

        if result is not None and content_type.endswith('+gzip'):
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
        if content_type in ['avro/binary', 'application/vnd.apache.avro+avro', 'avro/json', 'application/vnd.apache.avro+json']:
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for conversion to Stream')
            reader = avro.io.DatumReader(cls.AvroType)
            if content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
                decoder = avro.io.BinaryDecoder(stream)
            else:
                raise NotImplementedError(f'Unsupported Avro media type {content_type}')
            _record = reader.read(decoder)            
            return FeedItemSource.from_serializer_dict(_record)
        if content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return FeedItemSource.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')