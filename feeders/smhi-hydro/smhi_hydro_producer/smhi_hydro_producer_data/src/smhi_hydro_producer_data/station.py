""" Station dataclass. """

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
import avro.schema
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Station:
    """
    Station
    
    Attributes:
        station_id (str)
        name (str)
        owner (typing.Optional[str])
        measuring_stations (typing.Optional[str])
        region (typing.Optional[int])
        catchment_name (str)
        catchment_number (typing.Optional[int])
        catchment_size (typing.Optional[float])
        latitude (float)
        longitude (float)
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Station\", \"doc\": \"Station\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\"}, {\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"owner\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"measuring_stations\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"region\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"catchment_name\", \"type\": \"string\", \"doc\": \"Name of the catchment area the station belongs to (SMHI 'catchmentName' field, e.g. 'Torne\u00e4lven', 'Dal\u00e4lven'). Sourced by the bridge from the SMHI bulk API station catalog. When the catalog has no catchmentName for a station the bridge substitutes the lowercase sentinel 'unknown' so the field stays non-null and the {catchment_name} MQTT topic segment remains populated. Normalized to lowercase kebab-case before publishing.\"}, {\"name\": \"catchment_number\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"catchment_size\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"latitude\", \"type\": \"double\"}, {\"name\": \"longitude\", \"type\": \"double\"}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    owner: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="owner"))
    measuring_stations: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="measuring_stations"))
    region: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))
    catchment_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="catchment_name"))
    catchment_number: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="catchment_number"))
    catchment_size: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="catchment_size"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'Station':
        """
        Converts a dictionary from Avro deserialization to a dataclass instance.
        Handles conversion of string representations back to Python types for
        extended logical types.
        
        Args:
            data: The dictionary from Avro deserialization.
        
        Returns:
            The dataclass representation.
        """
        # Convert string values back to Python types for Avro string-based logical types
        converted = data.copy()
        if 'station_id' in converted and converted['station_id'] is not None:
            value = converted['station_id']
        if 'name' in converted and converted['name'] is not None:
            value = converted['name']
        if 'owner' in converted and converted['owner'] is not None:
            value = converted['owner']
        if 'measuring_stations' in converted and converted['measuring_stations'] is not None:
            value = converted['measuring_stations']
        if 'region' in converted and converted['region'] is not None:
            value = converted['region']
        if 'catchment_name' in converted and converted['catchment_name'] is not None:
            value = converted['catchment_name']
        if 'catchment_number' in converted and converted['catchment_number'] is not None:
            value = converted['catchment_number']
        if 'catchment_size' in converted and converted['catchment_size'] is not None:
            value = converted['catchment_size']
        if 'latitude' in converted and converted['latitude'] is not None:
            value = converted['latitude']
        if 'longitude' in converted and converted['longitude'] is not None:
            value = converted['longitude']
        
        return cls(**converted)

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
            if isinstance(v, enum.Enum):
                return v.value
            return v
        def _fix_key(k):
            return k[:-1] if k.endswith('_') else k
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data)}

    def to_avro_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary suitable for Avro serialization.
        Handles conversion of Python types to Avro-compatible string representations
        for extended logical types.

        Returns:
            The dictionary representation suitable for Avro serialization.
        """
        result = self.to_serializer_dict()
        converted = result.copy()
        
        # Convert specific fields based on their source types
        
        return converted

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'application/json': Encodes the data to JSON format.
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
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
            # Convert to Avro binary format using the embedded schema
            writer = avro.io.DatumWriter(self.AvroType)
            with io.BytesIO() as stream:
                encoder = avro.io.BinaryEncoder(stream)
                writer.write(self.to_avro_dict(), encoder)
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Station']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'application/json': Attempts to decode the data from JSON encoded format.
                    'avro/binary': Attempts to decode the data from Avro binary format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            if isinstance(data, bytes):
                # Decode from Avro binary format using the embedded schema
                reader = avro.io.DatumReader(cls.AvroType)
                with io.BytesIO(data) as stream:
                    decoder = avro.io.BinaryDecoder(stream)
                    _record = reader.read(decoder)
                    return Station.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Station':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='iryeinezddowpoablzht',
            name='jnympljcedpeiplfwigd',
            owner='vmivvjigzpxonvcrcjqt',
            measuring_stations='sjiiloplsatwirholcwy',
            region=int(29),
            catchment_name='kbyddazyprospxyhfuyt',
            catchment_number=int(36),
            catchment_size=float(98.74865928998821),
            latitude=float(60.62689330659724),
            longitude=float(15.17152790755577)
        )