""" BuoySupplementalMeasurement dataclass. """

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
class BuoySupplementalMeasurement:
    """
    Supplemental hourly extrema from the NDBC .supl realtime2 product. Each record reports the lowest one-minute pressure recorded during the hour and the highest one-minute wind speed with its direction and HHMM occurrence times.
    
    Attributes:
        station_id (str)
        timestamp (datetime.datetime)
        lowest_pressure (typing.Optional[float])
        lowest_pressure_time_code (typing.Optional[str])
        highest_wind_speed (typing.Optional[float])
        highest_wind_direction (typing.Optional[float])
        highest_wind_time_code (typing.Optional[str])
        region (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"BuoySupplementalMeasurement\", \"doc\": \"Supplemental hourly extrema from the NDBC .supl realtime2 product. Each record reports the lowest one-minute pressure recorded during the hour and the highest one-minute wind speed with its direction and HHMM occurrence times.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"NDBC station identifier for the station publishing the .supl realtime2 file.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .supl realtime2 file.\"}, {\"name\": \"lowest_pressure\", \"type\": [\"double\", \"null\"], \"doc\": \"Lowest one-minute atmospheric pressure recorded during the hour from the PRES column. Unit: hectopascals.\", \"default\": null}, {\"name\": \"lowest_pressure_time_code\", \"type\": [\"string\", \"null\"], \"doc\": \"HHMM UTC time code from the PTIME column indicating when the lowest one-minute pressure occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. [pattern: ^[0-9]{4}$]\", \"default\": null}, {\"name\": \"highest_wind_speed\", \"type\": [\"double\", \"null\"], \"doc\": \"Highest one-minute wind speed recorded during the hour from the WSPD column. Unit: meters per second.\", \"default\": null}, {\"name\": \"highest_wind_direction\", \"type\": [\"double\", \"null\"], \"doc\": \"Direction associated with the highest one-minute wind speed from the WDIR column, measured clockwise from true north. Unit: degrees true.\", \"default\": null}, {\"name\": \"highest_wind_time_code\", \"type\": [\"string\", \"null\"], \"doc\": \"HHMM UTC time code from the WTIME column indicating when the highest one-minute wind speed occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. [pattern: ^[0-9]{4}$]\", \"default\": null}, {\"name\": \"region\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.\", \"default\": null}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    lowest_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lowest_pressure"))
    lowest_pressure_time_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lowest_pressure_time_code"))
    highest_wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="highest_wind_speed"))
    highest_wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="highest_wind_direction"))
    highest_wind_time_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="highest_wind_time_code"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'BuoySupplementalMeasurement':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'BuoySupplementalMeasurement':
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
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, str):
                converted['timestamp'] = datetime.datetime.fromisoformat(value)
        if 'lowest_pressure' in converted and converted['lowest_pressure'] is not None:
            value = converted['lowest_pressure']
        if 'lowest_pressure_time_code' in converted and converted['lowest_pressure_time_code'] is not None:
            value = converted['lowest_pressure_time_code']
        if 'highest_wind_speed' in converted and converted['highest_wind_speed'] is not None:
            value = converted['highest_wind_speed']
        if 'highest_wind_direction' in converted and converted['highest_wind_direction'] is not None:
            value = converted['highest_wind_direction']
        if 'highest_wind_time_code' in converted and converted['highest_wind_time_code'] is not None:
            value = converted['highest_wind_time_code']
        if 'region' in converted and converted['region'] is not None:
            value = converted['region']
        
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
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, datetime.datetime):
                converted['timestamp'] = value.isoformat()
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['BuoySupplementalMeasurement']:
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
                    return BuoySupplementalMeasurement.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return BuoySupplementalMeasurement.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'BuoySupplementalMeasurement':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='cfmbbnhyfetxadjvxlor',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            lowest_pressure=float(10.767155100906367),
            lowest_pressure_time_code='yeerzmzxbtupokeayxed',
            highest_wind_speed=float(27.13729584622562),
            highest_wind_direction=float(66.69639230130664),
            highest_wind_time_code='ceuubrmjjtqhxiwcrbda',
            region='zvrbznjrbjdomhplvxdd'
        )