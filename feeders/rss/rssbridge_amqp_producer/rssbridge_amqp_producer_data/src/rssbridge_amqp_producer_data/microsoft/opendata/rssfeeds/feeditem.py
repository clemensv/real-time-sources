""" FeedItem dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
from __future__ import annotations
import io
import gzip
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import json
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditemsource import FeedItemSource
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditemenclosure import FeedItemEnclosure
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditempublisher import FeedItemPublisher
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.link import Link
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditemcontent import FeedItemContent
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditemsummary import FeedItemSummary


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class FeedItem:
    """
    Represents an item in an RSS feed, containing metadata such as the author, title, and content.
    
    Attributes:
        feed_slug (str)
        item (str)
        author (typing.Optional[FeedItemAuthor])
        publisher (typing.Optional[FeedItemPublisher])
        summary (typing.Optional[FeedItemSummary])
        title (typing.Optional[FeedItemTitle])
        source (typing.Optional[FeedItemSource])
        content (typing.Optional[typing.List[FeedItemContent]])
        enclosures (typing.Optional[typing.List[FeedItemEnclosure]])
        published (typing.Optional[int])
        updated (typing.Optional[int])
        created (typing.Optional[int])
        expired (typing.Optional[int])
        id (typing.Optional[str])
        license (typing.Optional[str])
        comments (typing.Optional[str])
        contributors (typing.Optional[typing.List[FeedItemAuthor]])
        links (typing.Optional[typing.List[Link]])
    """
    
    
    feed_slug: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feed_slug"))
    item: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="item"))
    author: typing.Optional[FeedItemAuthor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="author"))
    publisher: typing.Optional[FeedItemPublisher]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="publisher"))
    summary: typing.Optional[FeedItemSummary]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="summary"))
    title: typing.Optional[FeedItemTitle]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    source: typing.Optional[FeedItemSource]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source"))
    content: typing.Optional[typing.List[FeedItemContent]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="content"))
    enclosures: typing.Optional[typing.List[FeedItemEnclosure]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="enclosures"))
    published: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    updated: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    created: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    expired: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expired", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    license: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="license"))
    comments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="comments"))
    contributors: typing.Optional[typing.List[FeedItemAuthor]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contributors"))
    links: typing.Optional[typing.List[Link]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="links"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'FeedItem':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        if 'published' in data and isinstance(data['published'], str):
            data['published'] = int(data['published'])
        if 'updated' in data and isinstance(data['updated'], str):
            data['updated'] = int(data['updated'])
        if 'created' in data and isinstance(data['created'], str):
            data['created'] = int(data['created'])
        if 'expired' in data and isinstance(data['expired'], str):
            data['expired'] = int(data['expired'])
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        if 'published' in asdict_result and asdict_result['published'] is not None:
            asdict_result['published'] = str(asdict_result['published'])
        if 'updated' in asdict_result and asdict_result['updated'] is not None:
            asdict_result['updated'] = str(asdict_result['updated'])
        if 'created' in asdict_result and asdict_result['created'] is not None:
            asdict_result['created'] = str(asdict_result['created'])
        if 'expired' in asdict_result and asdict_result['expired'] is not None:
            asdict_result['expired'] = str(asdict_result['expired'])
        return asdict_result

    def _dict_resolver(self, data):
        """
        Helps resolving the Enum values to their actual values and fixes the key names.
        """ 
        def _resolve_enum(v):
            if isinstance(v, enum.Enum):
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
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return FeedItem.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'FeedItem':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            feed_slug='rzlttftxocnloreojugd',
            item='ujltaaprgrqbifehhdbt',
            author=None,
            publisher=None,
            summary=None,
            title=None,
            source=None,
            content=[None, None, None],
            enclosures=[None, None, None, None, None],
            published=int(62),
            updated=int(6),
            created=int(18),
            expired=int(18),
            id='hgcsxekqxcvltgcoqprs',
            license='fjbjmynzipvxslmemtxf',
            comments='paydlpcctovlfdsamrem',
            contributors=[None, None, None, None],
            links=[None]
        )