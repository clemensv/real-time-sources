""" Observation dataclass. """

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
from marshmallow import fields
import json
import avro.schema
import avro.io
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Observation:
    """
    Real-time hydrometric observation from the ECCC OGC API hydrometric-realtime collection. Data are provisional and updated approximately every 5 minutes.
    
    Attributes:
        station_number (str)
        identifier (str)
        station_name (str)
        prov_terr_state_loc (str)
        observation_datetime (datetime.datetime)
        level (typing.Optional[float])
        discharge (typing.Optional[float])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        basin (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Observation\", \"doc\": \"Real-time hydrometric observation from the ECCC OGC API hydrometric-realtime collection. Data are provisional and updated approximately every 5 minutes.\", \"fields\": [{\"name\": \"station_number\", \"type\": \"string\", \"doc\": \"Unique WSC station identifier, e.g. '05BJ004'. Upstream field: STATION_NUMBER.\"}, {\"name\": \"identifier\", \"type\": \"string\", \"doc\": \"Unique observation identifier composed of station number and ISO 8601 observation datetime, e.g. '05BJ004.2026-03-07T07:00:00Z'. Upstream field: IDENTIFIER.\"}, {\"name\": \"station_name\", \"type\": \"string\", \"doc\": \"Official name of the hydrometric station. Upstream field: STATION_NAME.\"}, {\"name\": \"prov_terr_state_loc\", \"type\": \"string\", \"doc\": \"Two-letter province, territory or state location code. Upstream field: PROV_TERR_STATE_LOC.\"}, {\"name\": \"observation_datetime\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"Timestamp of the observation in UTC. Upstream field: DATETIME.\"}, {\"name\": \"level\", \"type\": [\"double\", \"null\"], \"doc\": \"Water level at the station gauge in metres above the station datum. Null when not measured or unavailable. Upstream field: LEVEL.\", \"default\": null}, {\"name\": \"discharge\", \"type\": [\"double\", \"null\"], \"doc\": \"Water discharge (flow rate) at the station in cubic metres per second. Null when not measured or unavailable. Upstream field: DISCHARGE.\", \"default\": null}, {\"name\": \"latitude\", \"type\": [\"double\", \"null\"], \"doc\": \"Geographic latitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.\", \"default\": null}, {\"name\": \"longitude\", \"type\": [\"double\", \"null\"], \"doc\": \"Geographic longitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.\", \"default\": null}, {\"name\": \"basin\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for canada-eccc-wateroffice.\", \"default\": null}]}"
    )
    
    
    station_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_number"))
    identifier: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="identifier"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    prov_terr_state_loc: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="prov_terr_state_loc"))
    observation_datetime: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    level: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="level"))
    discharge: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="discharge"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    basin: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Observation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'Observation':
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
        if 'station_number' in converted and converted['station_number'] is not None:
            value = converted['station_number']
        if 'identifier' in converted and converted['identifier'] is not None:
            value = converted['identifier']
        if 'station_name' in converted and converted['station_name'] is not None:
            value = converted['station_name']
        if 'prov_terr_state_loc' in converted and converted['prov_terr_state_loc'] is not None:
            value = converted['prov_terr_state_loc']
        if 'observation_datetime' in converted and converted['observation_datetime'] is not None:
            value = converted['observation_datetime']
            if isinstance(value, str):
                converted['observation_datetime'] = datetime.datetime.fromisoformat(value)
        if 'level' in converted and converted['level'] is not None:
            value = converted['level']
        if 'discharge' in converted and converted['discharge'] is not None:
            value = converted['discharge']
        if 'latitude' in converted and converted['latitude'] is not None:
            value = converted['latitude']
        if 'longitude' in converted and converted['longitude'] is not None:
            value = converted['longitude']
        if 'basin' in converted and converted['basin'] is not None:
            value = converted['basin']
        
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
        if 'observation_datetime' in converted and converted['observation_datetime'] is not None:
            value = converted['observation_datetime']
            if isinstance(value, datetime.datetime):
                converted['observation_datetime'] = value.isoformat()
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Observation']:
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
                    return Observation.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Observation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Observation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_number='hhqrcbocrvgwmrygpdgc',
            identifier='orxqedwocwjkdyodkrfc',
            station_name='tkacxhcjixntpsirfzii',
            prov_terr_state_loc='vtwhxfkxnbsikgysvyyp',
            observation_datetime=datetime.datetime.now(datetime.timezone.utc),
            level=float(97.40408830145512),
            discharge=float(18.221563127027697),
            latitude=float(61.701267747305735),
            longitude=float(43.01218386529443),
            basin='ofxqmvjkgtbscsbisoow'
        )