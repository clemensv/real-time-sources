""" Post dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import json
import avro.schema
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Post:
    """
    A post in the Bluesky feed
    Attributes:
        uri (str): AT-URI of the post (at://did:plc:xxx/app.bsky.feed.post/xxx)
        cid (str): Content Identifier (CID) of the post
        did (str): Decentralized Identifier of the author
        handle (typing.Optional[str]): Handle of the author
        text (str): Text content of the post
        langs (typing.List[str]): Language codes for the post
        reply_parent (typing.Optional[str]): AT-URI of parent post if this is a reply
        reply_root (typing.Optional[str]): AT-URI of root post in thread
        embed_type (typing.Optional[str]): Type of embedded content (images, external, record, etc.)
        embed_uri (typing.Optional[str]): URI of embedded content
        facets (typing.Optional[str]): JSON string of rich text facets (mentions, links, tags)
        tags (typing.List[str]): Hashtags in the post
        created_at (str): ISO 8601 timestamp of post creation
        indexed_at (str): ISO 8601 timestamp of when the post was indexed
        seq (int): Firehose sequence number"""
    
    uri: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="uri"))
    cid: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cid"))
    did: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="did"))
    handle: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="handle"))
    text: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="text"))
    langs: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="langs"))
    reply_parent: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reply_parent"))
    reply_root: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reply_root"))
    embed_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="embed_type"))
    embed_uri: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="embed_uri"))
    facets: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="facets"))
    tags: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tags"))
    created_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created_at"))
    indexed_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="indexed_at"))
    seq: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="seq"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Post\", \"namespace\": \"Bluesky.Feed\", \"fields\": [{\"name\": \"uri\", \"type\": \"string\", \"doc\": \"AT-URI of the post (at://did:plc:xxx/app.bsky.feed.post/xxx)\"}, {\"name\": \"cid\", \"type\": \"string\", \"doc\": \"Content Identifier (CID) of the post\"}, {\"name\": \"did\", \"type\": \"string\", \"doc\": \"Decentralized Identifier of the author\"}, {\"name\": \"handle\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Handle of the author\"}, {\"name\": \"text\", \"type\": \"string\", \"doc\": \"Text content of the post\"}, {\"name\": \"langs\", \"type\": {\"type\": \"array\", \"items\": \"string\"}, \"default\": [], \"doc\": \"Language codes for the post\"}, {\"name\": \"reply_parent\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"AT-URI of parent post if this is a reply\"}, {\"name\": \"reply_root\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"AT-URI of root post in thread\"}, {\"name\": \"embed_type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Type of embedded content (images, external, record, etc.)\"}, {\"name\": \"embed_uri\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"URI of embedded content\"}, {\"name\": \"facets\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"JSON string of rich text facets (mentions, links, tags)\"}, {\"name\": \"tags\", \"type\": {\"type\": \"array\", \"items\": \"string\"}, \"default\": [], \"doc\": \"Hashtags in the post\"}, {\"name\": \"created_at\", \"type\": \"string\", \"doc\": \"ISO 8601 timestamp of post creation\"}, {\"name\": \"indexed_at\", \"type\": \"string\", \"doc\": \"ISO 8601 timestamp of when the post was indexed\"}, {\"name\": \"seq\", \"type\": \"long\", \"doc\": \"Firehose sequence number\"}], \"doc\": \"A post in the Bluesky feed\"}"
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.uri=str(self.uri)
        self.cid=str(self.cid)
        self.did=str(self.did)
        self.handle=str(self.handle) if self.handle else None
        self.text=str(self.text)
        self.langs=self.langs if isinstance(self.langs, list) else [str(v) for v in self.langs] if self.langs else None
        self.reply_parent=str(self.reply_parent) if self.reply_parent else None
        self.reply_root=str(self.reply_root) if self.reply_root else None
        self.embed_type=str(self.embed_type) if self.embed_type else None
        self.embed_uri=str(self.embed_uri) if self.embed_uri else None
        self.facets=str(self.facets) if self.facets else None
        self.tags=self.tags if isinstance(self.tags, list) else [str(v) for v in self.tags] if self.tags else None
        self.created_at=str(self.created_at)
        self.indexed_at=str(self.indexed_at)
        self.seq=int(self.seq)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Post':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Post']:
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
            return Post.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Post.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')