""" Attraction dataclass. """

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
import avro.schema
import avro.name
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Attraction:
    """
    Reference data for a Ticketmaster attraction (performer, artist, sports team, or production).
    Attributes:
        entity_id (str): Stable Ticketmaster attraction identifier.
        name (str): Human-readable name of the attraction.
        url (typing.Optional[str]): URL to the attraction page on Ticketmaster.com.
        locale (typing.Optional[str]): BCP-47 locale string.
        segment_id (typing.Optional[str]): Stable classification segment identifier.
        segment_name (typing.Optional[str]): Classification segment name.
        genre_id (typing.Optional[str]): Stable genre identifier.
        genre_name (typing.Optional[str]): Genre name.
        subgenre_id (typing.Optional[str]): Stable subgenre identifier.
        subgenre_name (typing.Optional[str]): Subgenre name."""
    
    entity_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="entity_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    locale: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="locale"))
    segment_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segment_id"))
    segment_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segment_name"))
    genre_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="genre_id"))
    genre_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="genre_name"))
    subgenre_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subgenre_id"))
    subgenre_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subgenre_name"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Attraction\", \"namespace\": \"Ticketmaster.Reference\", \"doc\": \"Reference data for a Ticketmaster attraction (performer, artist, sports team, or production).\", \"fields\": [{\"name\": \"entity_id\", \"type\": \"string\", \"doc\": \"Stable Ticketmaster attraction identifier.\"}, {\"name\": \"name\", \"type\": \"string\", \"doc\": \"Human-readable name of the attraction.\"}, {\"name\": \"url\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"URL to the attraction page on Ticketmaster.com.\"}, {\"name\": \"locale\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"BCP-47 locale string.\"}, {\"name\": \"segment_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Stable classification segment identifier.\"}, {\"name\": \"segment_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Classification segment name.\"}, {\"name\": \"genre_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Stable genre identifier.\"}, {\"name\": \"genre_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Genre name.\"}, {\"name\": \"subgenre_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Stable subgenre identifier.\"}, {\"name\": \"subgenre_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Subgenre name.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.entity_id=str(self.entity_id)
        self.name=str(self.name)
        self.url=str(self.url) if self.url else None
        self.locale=str(self.locale) if self.locale else None
        self.segment_id=str(self.segment_id) if self.segment_id else None
        self.segment_name=str(self.segment_name) if self.segment_name else None
        self.genre_id=str(self.genre_id) if self.genre_id else None
        self.genre_name=str(self.genre_name) if self.genre_name else None
        self.subgenre_id=str(self.subgenre_id) if self.subgenre_id else None
        self.subgenre_name=str(self.subgenre_name) if self.subgenre_name else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Attraction':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Attraction']:
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
            return Attraction.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Attraction.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')