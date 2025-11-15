""" Profile dataclass. """

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
class Profile:
    """
    A user profile update
    Attributes:
        did (str): Decentralized Identifier
        handle (str): User handle
        display_name (typing.Optional[str]): Display name
        description (typing.Optional[str]): Bio/description
        avatar (typing.Optional[str]): Avatar image URL
        banner (typing.Optional[str]): Banner image URL
        created_at (str): ISO 8601 timestamp of profile creation
        indexed_at (str): ISO 8601 timestamp of indexing
        seq (int): Firehose sequence number"""
    
    did: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="did"))
    handle: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="handle"))
    display_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="display_name"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    avatar: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="avatar"))
    banner: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="banner"))
    created_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created_at"))
    indexed_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="indexed_at"))
    seq: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="seq"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Profile\", \"namespace\": \"Bluesky.Actor\", \"fields\": [{\"name\": \"did\", \"type\": \"string\", \"doc\": \"Decentralized Identifier\"}, {\"name\": \"handle\", \"type\": \"string\", \"doc\": \"User handle\"}, {\"name\": \"display_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Display name\"}, {\"name\": \"description\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Bio/description\"}, {\"name\": \"avatar\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Avatar image URL\"}, {\"name\": \"banner\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Banner image URL\"}, {\"name\": \"created_at\", \"type\": \"string\", \"doc\": \"ISO 8601 timestamp of profile creation\"}, {\"name\": \"indexed_at\", \"type\": \"string\", \"doc\": \"ISO 8601 timestamp of indexing\"}, {\"name\": \"seq\", \"type\": \"long\", \"doc\": \"Firehose sequence number\"}], \"doc\": \"A user profile update\"}"
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.did=str(self.did)
        self.handle=str(self.handle)
        self.display_name=str(self.display_name) if self.display_name else None
        self.description=str(self.description) if self.description else None
        self.avatar=str(self.avatar) if self.avatar else None
        self.banner=str(self.banner) if self.banner else None
        self.created_at=str(self.created_at)
        self.indexed_at=str(self.indexed_at)
        self.seq=int(self.seq)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Profile':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Profile']:
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
            return Profile.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Profile.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')