""" FeedItem dataclass. """

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
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsource import FeedItemSource
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle
from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditempublisher import FeedItemPublisher
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemcontent import FeedItemContent
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsummary import FeedItemSummary
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemenclosure import FeedItemEnclosure
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class FeedItem:
    """
    Represents an item in an RSS feed, containing metadata such as the author, title, and content.
    Attributes:
        author (typing.Optional[FeedItemAuthor]): Information about the feed item's author.
        publisher (typing.Optional[FeedItemPublisher]): Information about the feed item's publisher.
        summary (typing.Optional[FeedItemSummary]): A short summary of the feed item.
        title (typing.Optional[FeedItemTitle]): The feed item's title.
        source (typing.Optional[FeedItemSource]): Information about the source feed of the item.
        content (typing.Optional[typing.List[FeedItemContent]]): The content of the feed item, potentially including multiple formats.
        enclosures (typing.Optional[typing.List[FeedItemEnclosure]]): Media attachments associated with the feed item.
        published (typing.Optional[datetime.datetime]): The publication date and time of the feed item.
        updated (typing.Optional[datetime.datetime]): The last updated date and time of the feed item.
        created (typing.Optional[datetime.datetime]): The creation date and time of the feed item.
        expired (typing.Optional[datetime.datetime]): The expiration date and time of the feed item.
        id (typing.Optional[str]): A unique identifier for the feed item.
        license (typing.Optional[str]): License information for the feed item.
        comments (typing.Optional[str]): A link to comments or feedback related to the feed item.
        contributors (typing.Optional[typing.List[FeedItemAuthor]]): A list of individuals who contributed to the feed item.
        links (typing.Optional[typing.List[Link]]): A collection of links related to the feed item."""
    
    author: typing.Optional[FeedItemAuthor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="author"))
    publisher: typing.Optional[FeedItemPublisher]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="publisher"))
    summary: typing.Optional[FeedItemSummary]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="summary"))
    title: typing.Optional[FeedItemTitle]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    source: typing.Optional[FeedItemSource]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source"))
    content: typing.Optional[typing.List[FeedItemContent]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="content"))
    enclosures: typing.Optional[typing.List[FeedItemEnclosure]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="enclosures"))
    published: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    updated: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    created: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    expired: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expired", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    license: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="license"))
    comments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="comments"))
    contributors: typing.Optional[typing.List[FeedItemAuthor]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contributors"))
    links: typing.Optional[typing.List[Link]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="links"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"FeedItem\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Represents an item in an RSS feed, containing metadata such as the author, title, and content.\", \"fields\": [{\"name\": \"author\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemAuthor\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Contains information about the author of the feed item.\", \"fields\": [{\"name\": \"name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The full name of the author.\"}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A URL associated with the author, such as a personal website or profile.\"}, {\"name\": \"email\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The author's email address.\"}]}], \"default\": null, \"doc\": \"Information about the feed item's author.\"}, {\"name\": \"publisher\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemPublisher\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Contains information about the publisher of the feed item.\", \"fields\": [{\"name\": \"name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The name of the publisher.\"}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A URL associated with the publisher.\"}, {\"name\": \"email\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The publisher's email address.\"}]}], \"default\": null, \"doc\": \"Information about the feed item's publisher.\"}, {\"name\": \"summary\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemSummary\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"A brief summary or abstract of the feed item.\", \"fields\": [{\"name\": \"value\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The text content of the summary.\"}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The content type of the summary, such as 'text/plain' or 'text/html'.\"}, {\"name\": \"language\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The language of the summary content.\"}, {\"name\": \"base\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The base URI for resolving relative URIs within the summary.\"}]}], \"default\": null, \"doc\": \"A short summary of the feed item.\"}, {\"name\": \"title\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemTitle\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"The title of the feed item.\", \"fields\": [{\"name\": \"value\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The text content of the title.\"}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The content type of the title.\"}, {\"name\": \"language\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The language of the title.\"}, {\"name\": \"base\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The base URI for resolving relative URIs within the title.\"}]}], \"default\": null, \"doc\": \"The feed item's title.\"}, {\"name\": \"source\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"FeedItemSource\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Metadata about the original source feed, useful if the item was republished from another feed.\", \"fields\": [{\"name\": \"author\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The name of the original author.\"}, {\"name\": \"author_detail\", \"type\": [\"null\", \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"], \"default\": null, \"doc\": \"Detailed information about the original author.\"}, {\"name\": \"contributors\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"}], \"default\": null, \"doc\": \"A list of contributors to the source feed.\"}, {\"name\": \"icon\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"An icon image associated with the source feed.\"}, {\"name\": \"id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A unique identifier for the source feed.\"}, {\"name\": \"link\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A link to the source feed.\"}, {\"name\": \"links\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"Link\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Represents a hyperlink associated with the feed or feed item.\", \"fields\": [{\"name\": \"rel\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The relationship type of the link, such as 'alternate' or 'self'.\"}, {\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The URL of the link.\"}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The MIME type of the linked resource.\"}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The title or description of the link.\"}]}}], \"default\": null, \"doc\": \"A collection of links related to the source feed.\"}, {\"name\": \"logo\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A logo image associated with the source feed.\"}, {\"name\": \"rights\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Rights information for the source feed, such as copyright notices.\"}, {\"name\": \"subtitle\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A secondary title or tagline for the source feed.\"}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The title of the source feed.\"}, {\"name\": \"updated\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null, \"doc\": \"The last updated timestamp of the source feed.\"}]}], \"default\": null, \"doc\": \"Information about the source feed of the item.\"}, {\"name\": \"content\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"FeedItemContent\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Represents the main content of the feed item.\", \"fields\": [{\"name\": \"value\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The actual content of the feed item.\"}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The content type, such as 'text/html' or 'text/plain'.\"}, {\"name\": \"language\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The language of the content.\"}, {\"name\": \"base\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The base URI for resolving relative URIs within the content.\"}]}}], \"default\": null, \"doc\": \"The content of the feed item, potentially including multiple formats.\"}, {\"name\": \"enclosures\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"FeedItemEnclosure\", \"namespace\": \"Microsoft.OpenData.RssFeeds\", \"doc\": \"Represents media content attached to the feed item, such as audio or video files.\", \"fields\": [{\"name\": \"href\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The URL of the enclosure.\"}, {\"name\": \"length\", \"type\": [\"null\", \"long\"], \"default\": null, \"doc\": \"The size of the enclosure in bytes.\"}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"The MIME type of the enclosure content.\"}]}}], \"default\": null, \"doc\": \"Media attachments associated with the feed item.\"}, {\"name\": \"published\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null, \"doc\": \"The publication date and time of the feed item.\"}, {\"name\": \"updated\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null, \"doc\": \"The last updated date and time of the feed item.\"}, {\"name\": \"created\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null, \"doc\": \"The creation date and time of the feed item.\"}, {\"name\": \"expired\", \"type\": [\"null\", {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}], \"default\": null, \"doc\": \"The expiration date and time of the feed item.\"}, {\"name\": \"id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A unique identifier for the feed item.\"}, {\"name\": \"license\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"License information for the feed item.\"}, {\"name\": \"comments\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"A link to comments or feedback related to the feed item.\"}, {\"name\": \"contributors\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.FeedItemAuthor\"}], \"default\": null, \"doc\": \"A list of individuals who contributed to the feed item.\"}, {\"name\": \"links\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"Microsoft.OpenData.RssFeeds.Link\"}], \"default\": null, \"doc\": \"A collection of links related to the feed item.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.author=self.author if isinstance(self.author, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(self.author) if self.author else None if self.author else None
        self.publisher=self.publisher if isinstance(self.publisher, FeedItemPublisher) else FeedItemPublisher.from_serializer_dict(self.publisher) if self.publisher else None if self.publisher else None
        self.summary=self.summary if isinstance(self.summary, FeedItemSummary) else FeedItemSummary.from_serializer_dict(self.summary) if self.summary else None if self.summary else None
        self.title=self.title if isinstance(self.title, FeedItemTitle) else FeedItemTitle.from_serializer_dict(self.title) if self.title else None if self.title else None
        self.source=self.source if isinstance(self.source, FeedItemSource) else FeedItemSource.from_serializer_dict(self.source) if self.source else None if self.source else None
        self.content=self.content if isinstance(self.content, list) else [v if isinstance(v, FeedItemContent) else FeedItemContent.from_serializer_dict(v) if v else None for v in self.content] if self.content else None if self.content else None
        self.enclosures=self.enclosures if isinstance(self.enclosures, list) else [v if isinstance(v, FeedItemEnclosure) else FeedItemEnclosure.from_serializer_dict(v) if v else None for v in self.enclosures] if self.enclosures else None if self.enclosures else None
        self.published=self.published if self.published else None
        self.updated=self.updated if self.updated else None
        self.created=self.created if self.created else None
        self.expired=self.expired if self.expired else None
        self.id=str(self.id) if self.id else None
        self.license=str(self.license) if self.license else None
        self.comments=str(self.comments) if self.comments else None
        self.contributors=self.contributors if isinstance(self.contributors, list) else [v if isinstance(v, FeedItemAuthor) else FeedItemAuthor.from_serializer_dict(v) if v else None for v in self.contributors] if self.contributors else None if self.contributors else None
        self.links=self.links if isinstance(self.links, list) else [v if isinstance(v, Link) else Link.from_serializer_dict(v) if v else None for v in self.links] if self.links else None if self.links else None

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
            return FeedItem.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return FeedItem.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')