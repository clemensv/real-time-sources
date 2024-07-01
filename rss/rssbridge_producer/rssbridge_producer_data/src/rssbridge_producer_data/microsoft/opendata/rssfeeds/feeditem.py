""" FeedItem dataclass. """

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
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsource import FeedItemSource
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemcontent import FeedItemContent
from datetime import datetime
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor
from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsummary import FeedItemSummary
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemenclosure import FeedItemEnclosure
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditempublisher import FeedItemPublisher


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class FeedItem:
    """
    A FeedItem record.
    Attributes:
        author (typing.Optional[FeedItemAuthor]): 
        publisher (typing.Optional[FeedItemPublisher]): 
        summary (typing.Optional[FeedItemSummary]): 
        title (typing.Optional[FeedItemTitle]): 
        source (typing.Optional[FeedItemSource]): 
        content (typing.Optional[typing.List[FeedItemContent]]): 
        enclosures (typing.Optional[typing.List[FeedItemEnclosure]]): 
        published (typing.Optional[datetime]): 
        updated (typing.Optional[datetime]): 
        created (typing.Optional[datetime]): 
        expired (typing.Optional[datetime]): 
        id (typing.Optional[str]): 
        license (typing.Optional[str]): 
        comments (typing.Optional[str]): 
        contributors (typing.Optional[typing.List[FeedItemAuthor]]): 
        links (typing.Optional[typing.List[Link]]): """
    
    author: typing.Optional[FeedItemAuthor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="author"))
    publisher: typing.Optional[FeedItemPublisher]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="publisher"))
    summary: typing.Optional[FeedItemSummary]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="summary"))
    title: typing.Optional[FeedItemTitle]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    source: typing.Optional[FeedItemSource]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source"))
    content: typing.Optional[typing.List[FeedItemContent]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="content"))
    enclosures: typing.Optional[typing.List[FeedItemEnclosure]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="enclosures"))
    published: typing.Optional[datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published"))
    updated: typing.Optional[datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated"))
    created: typing.Optional[datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created"))
    expired: typing.Optional[datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expired"))
    id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    license: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="license"))
    comments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="comments"))
    contributors: typing.Optional[typing.List[FeedItemAuthor]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contributors"))
    links: typing.Optional[typing.List[Link]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="links"))    
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"FeedItem\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"author\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemAuthor\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"email\", \"type\": [\"null\", \"string\"], \"default\": null}]}], \"default\": null}, {\"name\": \"publisher\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemPublisher\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"email\", \"type\": [\"null\", \"string\"], \"default\": null}]}], \"default\": null}, {\"name\": \"summary\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemSummary\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"value\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"language\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"base\", \"type\": [\"null\", \"string\"], \"default\": null}]}], \"default\": null}, {\"name\": \"title\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemTitle\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"value\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"language\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"base\", \"type\": [\"null\", \"string\"], \"default\": null}]}], \"default\": null}, {\"name\": \"source\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemSource\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"author\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"author_detail\", \"type\": [\"null\", \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"], \"default\": null}, {\"name\": \"contributors\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"}], \"default\": null}, {\"name\": \"icon\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"id\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"link\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"links\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"Link\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"rel\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null}]}}], \"default\": null}, {\"name\": \"logo\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"rights\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"subtitle\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"updated\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null}]}], \"default\": null}, {\"name\": \"content\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"FeedItemContent\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"value\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"language\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"base\", \"type\": [\"null\", \"string\"], \"default\": null}]}}], \"default\": null}, {\"name\": \"enclosures\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"FeedItemEnclosure\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"fields\": [{\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"length\", \"type\": [\"null\", \"long\"], \"default\": null}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null}]}}], \"default\": null}, {\"name\": \"published\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null}, {\"name\": \"updated\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null}, {\"name\": \"created\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null}, {\"name\": \"expired\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null}, {\"name\": \"id\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"license\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"comments\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"contributors\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"}], \"default\": null}, {\"name\": \"links\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.Link\"}], \"default\": null}]}"
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.author=self.author if isinstance(self.author, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(self.author) if self.author else None
        self.publisher=self.publisher if isinstance(self.publisher, FeedItemPublisher) else FeedItemPublisher.from_serializer_dict(self.publisher) if self.publisher else None
        self.summary=self.summary if isinstance(self.summary, FeedItemSummary) else FeedItemSummary.from_serializer_dict(self.summary) if self.summary else None
        self.title=self.title if isinstance(self.title, FeedItemTitle) else FeedItemTitle.from_serializer_dict(self.title) if self.title else None
        self.source=self.source if isinstance(self.source, FeedItemSource) else FeedItemSource.from_serializer_dict(self.source) if self.source else None
        self.content=self.content if isinstance(self.content, list) else [v if isinstance(v, FeedItemContent) else FeedItemContent.from_serializer_dict(v) if v else None for v in self.content] if self.content else None
        self.enclosures=self.enclosures if isinstance(self.enclosures, list) else [v if isinstance(v, FeedItemEnclosure) else FeedItemEnclosure.from_serializer_dict(v) if v else None for v in self.enclosures] if self.enclosures else None
        self.published=self.published
        self.updated=self.updated
        self.created=self.created
        self.expired=self.expired
        self.id=str(self.id)
        self.license=str(self.license)
        self.comments=str(self.comments)
        self.contributors=self.contributors if isinstance(self.contributors, list) else [v if isinstance(v, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(v) if v else None for v in self.contributors] if self.contributors else None
        self.links=self.links if isinstance(self.links, list) else [v if isinstance(v, Link) else Link.from_serializer_dict(v) if v else None for v in self.links] if self.links else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'FeedItem':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['FeedItem']:
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
            return FeedItem.from_serializer_dict(_record)
        if content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return FeedItem.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')