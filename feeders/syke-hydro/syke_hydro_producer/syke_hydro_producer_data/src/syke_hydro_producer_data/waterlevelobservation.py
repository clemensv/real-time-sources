""" WaterLevelObservation dataclass. """

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
class WaterLevelObservation:
    """
    Measurement payload for water level and discharge observations in the SYKE Hydrology source.
    
    Attributes:
        station_id (str)
        water_level (typing.Optional[float])
        water_level_unit (typing.Optional[str])
        water_level_timestamp (typing.Optional[datetime.datetime])
        discharge (typing.Optional[float])
        discharge_unit (typing.Optional[str])
        discharge_timestamp (typing.Optional[datetime.datetime])
        basin (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"WaterLevelObservation\", \"doc\": \"Measurement payload for water level and discharge observations in the SYKE Hydrology source.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Stable identifier assigned by the upstream provider for the monitoring station or site.\"}, {\"name\": \"water_level\", \"type\": [\"double\", \"null\"], \"doc\": \"Water level reading value in centimetres. Null when the station does not report a water level in the current polling window.\", \"default\": null}, {\"name\": \"water_level_unit\", \"type\": [\"string\", \"null\"], \"doc\": \"Unit of measurement for water_level. Constant 'cm' when present, null when water_level is null.\", \"default\": null}, {\"name\": \"water_level_timestamp\", \"type\": [{\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"null\"], \"doc\": \"RFC3339 UTC timestamp (with 'Z' suffix) of the water level observation, derived from the SYKE 'Aika' field. Null when no water level is available.\", \"default\": null}, {\"name\": \"discharge\", \"type\": [\"double\", \"null\"], \"doc\": \"Discharge (flow) reading value in cubic metres per second. Null for stations that do not measure discharge.\", \"default\": null}, {\"name\": \"discharge_unit\", \"type\": [\"string\", \"null\"], \"doc\": \"Unit of measurement for discharge. Constant 'm3/s' when present, null when discharge is null.\", \"default\": null}, {\"name\": \"discharge_timestamp\", \"type\": [{\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"null\"], \"doc\": \"RFC3339 UTC timestamp (with 'Z' suffix) of the discharge observation, derived from the SYKE 'Aika' field. Null when no discharge is available.\", \"default\": null}, {\"name\": \"basin\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for syke-hydro.\", \"default\": null}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    water_level: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_level"))
    water_level_unit: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_level_unit"))
    water_level_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_level_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    discharge: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="discharge"))
    discharge_unit: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="discharge_unit"))
    discharge_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="discharge_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    basin: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WaterLevelObservation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'WaterLevelObservation':
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
        if 'water_level' in converted and converted['water_level'] is not None:
            value = converted['water_level']
        if 'water_level_unit' in converted and converted['water_level_unit'] is not None:
            value = converted['water_level_unit']
        if 'water_level_timestamp' in converted and converted['water_level_timestamp'] is not None:
            value = converted['water_level_timestamp']
        if 'discharge' in converted and converted['discharge'] is not None:
            value = converted['discharge']
        if 'discharge_unit' in converted and converted['discharge_unit'] is not None:
            value = converted['discharge_unit']
        if 'discharge_timestamp' in converted and converted['discharge_timestamp'] is not None:
            value = converted['discharge_timestamp']
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WaterLevelObservation']:
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
                    return WaterLevelObservation.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WaterLevelObservation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WaterLevelObservation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='qptplgyivrtnmlbuclwn',
            water_level=float(14.497867667696497),
            water_level_unit='jgybjywcitcvvradgijy',
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(56.04344460734243),
            discharge_unit='tutzzkktnumzceenbdng',
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            basin='zfeblzdyxpvbluklkgbs'
        )