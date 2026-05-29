""" CurrentMeasurement dataclass. """

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
from pegelonline_amqp_producer_data.de.wsv.pegelonline.statenswhswenum import StateNswHswEnum
from pegelonline_amqp_producer_data.de.wsv.pegelonline.trendenum import TrendEnum
from pegelonline_amqp_producer_data.de.wsv.pegelonline.statemnwmhwenum import StateMnwMhwEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CurrentMeasurement:
    """
    Latest 15-minute water-level reading for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Carries only the W (water-level) timeseries; other timeseries (Q discharge, LT water temperature) are not emitted by this source.
    
    Attributes:
        station_id (str)
        timestamp (datetime.datetime)
        value (float)
        stateMnwMhw (typing.Optional[StateMnwMhwEnum])
        stateNswHsw (typing.Optional[StateNswHswEnum])
        trend (typing.Optional[TrendEnum])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"CurrentMeasurement\", \"doc\": \"Latest 15-minute water-level reading for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Carries only the W (water-level) timeseries; other timeseries (Q discharge, LT water temperature) are not emitted by this source.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Stable UUID of the gauge this reading was taken at. References the `station_id` of the corresponding Station reference event. Used as the CloudEvents `subject` and the Kafka partition key so all readings for a given gauge land on the same partition / topic key.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"Wall-clock time the upstream reading was taken, in ISO 8601 / RFC 3339 with an explicit UTC offset. PegelOnline publishes the value in Europe/Berlin local time, so the offset shifts between `+01:00` (CET) and `+02:00` (CEST) across the DST boundary \u2014 preserve the offset when storing. Sourced from the upstream `timestamp` field.\"}, {\"name\": \"value\", \"type\": \"double\", \"doc\": \"Water-level reading on the W (water-level) timeseries, in centimetres above the gauge's Pegelnullpunkt (PNP \u2014 a geodetically fixed datum specific to each gauge, see https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Typical operational range is 0\u20131500 cm; flood events at major Rhine gauges can exceed 1000 cm. Negative readings are valid at gauges whose normal pool is below PNP (e.g. tidal Elbe at low water). Unit: cm. [minimum: -1000, maximum: 2500]\"}, {\"name\": \"stateMnwMhw\", \"type\": [\"null\", \"string\"], \"doc\": \"Categorical classification of the current water level against the gauge's long-term mean low water (MNW) and mean high water (MHW) reference values, as computed by the upstream feed. Omitted by upstream when the gauge has no MNW/MHW reference series configured (treat absence as 'unknown').\", \"default\": null}, {\"name\": \"stateNswHsw\", \"type\": [\"null\", \"string\"], \"doc\": \"Categorical classification of the current water level against the highest navigable water level (HSW) reference for the reach, as computed by the upstream feed. Drives inland-shipping operational decisions (HSW = stop sign for commercial traffic). Note: upstream never emits 'low' on this series \u2014 HSW is an upper bound only. Omitted by upstream when the gauge has no HSW reference (treat absence as 'unknown').\", \"default\": null}, {\"name\": \"trend\", \"type\": [\"int\", \"null\"], \"doc\": \"Short-term trend of the water level relative to the previous reading, as classified by the upstream feed. First-class signal for flood-monitoring dashboards. Sourced from the upstream `trend` field; omitted when upstream cannot compute a trend (e.g. first reading after a gap).\", \"default\": null}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    stateMnwMhw: typing.Optional[StateMnwMhwEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stateMnwMhw"))
    stateNswHsw: typing.Optional[StateNswHswEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stateNswHsw"))
    trend: typing.Optional[TrendEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trend"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'CurrentMeasurement':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'CurrentMeasurement':
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
        if 'value' in converted and converted['value'] is not None:
            value = converted['value']
        if 'stateMnwMhw' in converted and converted['stateMnwMhw'] is not None:
            value = converted['stateMnwMhw']
        if 'stateNswHsw' in converted and converted['stateNswHsw'] is not None:
            value = converted['stateNswHsw']
        if 'trend' in converted and converted['trend'] is not None:
            value = converted['trend']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['CurrentMeasurement']:
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
                    return CurrentMeasurement.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return CurrentMeasurement.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'CurrentMeasurement':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='snpdzjlokjukgsazmsxq',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(92.08288387236927),
            stateMnwMhw=StateMnwMhwEnum.low,
            stateNswHsw=StateNswHswEnum.normal,
            trend=TrendEnum.VALUE_NEG_1
        )