""" Community dataclass. """

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
class Community:
    """
    Reference record for an AQHI community from the official ECCC AQHI city lists.
    Attributes:
        province (str): Two-letter Canadian province or territory abbreviation resolved for the AQHI community.
        community_name (str): English AQHI community name as published by Environment and Climate Change Canada.
        cgndb_code (str): Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds.
        latitude (float): Latitude of the AQHI community reference point in WGS84 decimal degrees.
        longitude (float): Longitude of the AQHI community reference point in WGS84 decimal degrees.
        observation_url (typing.Optional[str]): Current XML observation feed URL for the AQHI community, or null when observations are not distributed for that community.
        forecast_url (typing.Optional[str]): Current XML forecast feed URL for the AQHI community, or null when a public forecast feed is not available."""
    
    province: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="province"))
    community_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="community_name"))
    cgndb_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cgndb_code"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    observation_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_url"))
    forecast_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="forecast_url"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Community\", \"namespace\": \"ca.gc.weather.aqhi\", \"doc\": \"Reference record for an AQHI community from the official ECCC AQHI city lists.\", \"fields\": [{\"name\": \"province\", \"type\": \"string\", \"doc\": \"Two-letter Canadian province or territory abbreviation resolved for the AQHI community.\"}, {\"name\": \"community_name\", \"type\": \"string\", \"doc\": \"English AQHI community name as published by Environment and Climate Change Canada.\"}, {\"name\": \"cgndb_code\", \"type\": \"string\", \"doc\": \"Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds.\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"Latitude of the AQHI community reference point in WGS84 decimal degrees.\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"Longitude of the AQHI community reference point in WGS84 decimal degrees.\"}, {\"name\": \"observation_url\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Current XML observation feed URL for the AQHI community, or null when observations are not distributed for that community.\"}, {\"name\": \"forecast_url\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Current XML forecast feed URL for the AQHI community, or null when a public forecast feed is not available.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.province=str(self.province)
        self.community_name=str(self.community_name)
        self.cgndb_code=str(self.cgndb_code)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.observation_url=str(self.observation_url) if self.observation_url else None
        self.forecast_url=str(self.forecast_url) if self.forecast_url else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Community':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Community']:
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
            return Community.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Community.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')