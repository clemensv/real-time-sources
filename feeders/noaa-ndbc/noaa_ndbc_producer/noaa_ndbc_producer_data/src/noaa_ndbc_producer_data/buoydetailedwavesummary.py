""" BuoyDetailedWaveSummary dataclass. """

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
class BuoyDetailedWaveSummary:
    """
    Detailed wave-summary record from the NDBC .spec realtime2 product. Each record summarizes significant wave height together with swell and wind-wave components, qualitative steepness, and mean wave direction for one station timestamp.
    
    Attributes:
        station_id (str)
        timestamp (datetime.datetime)
        significant_wave_height (typing.Optional[float])
        swell_height (typing.Optional[float])
        swell_period (typing.Optional[float])
        wind_wave_height (typing.Optional[float])
        wind_wave_period (typing.Optional[float])
        swell_direction (typing.Optional[str])
        wind_wave_direction (typing.Optional[str])
        steepness (typing.Optional[str])
        average_wave_period (typing.Optional[float])
        mean_wave_direction (typing.Optional[float])
        region (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"BuoyDetailedWaveSummary\", \"doc\": \"Detailed wave-summary record from the NDBC .spec realtime2 product. Each record summarizes significant wave height together with swell and wind-wave components, qualitative steepness, and mean wave direction for one station timestamp.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"NDBC station identifier for the station publishing the .spec realtime2 file.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .spec realtime2 file.\"}, {\"name\": \"significant_wave_height\", \"type\": [\"double\", \"null\"], \"doc\": \"Significant wave height from the WVHT column, representing the average height of the highest one-third of waves during the sampling period. Unit: meters.\", \"default\": null}, {\"name\": \"swell_height\", \"type\": [\"double\", \"null\"], \"doc\": \"Swell-wave height from the SwH column. Unit: meters.\", \"default\": null}, {\"name\": \"swell_period\", \"type\": [\"double\", \"null\"], \"doc\": \"Swell-wave period from the SwP column. Unit: seconds.\", \"default\": null}, {\"name\": \"wind_wave_height\", \"type\": [\"double\", \"null\"], \"doc\": \"Wind-wave height from the WWH column. Unit: meters.\", \"default\": null}, {\"name\": \"wind_wave_period\", \"type\": [\"double\", \"null\"], \"doc\": \"Wind-wave period from the WWP column. Unit: seconds.\", \"default\": null}, {\"name\": \"swell_direction\", \"type\": [\"string\", \"null\"], \"doc\": \"Swell direction from the SwD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value.\", \"default\": null}, {\"name\": \"wind_wave_direction\", \"type\": [\"string\", \"null\"], \"doc\": \"Wind-wave direction from the WWD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value.\", \"default\": null}, {\"name\": \"steepness\", \"type\": [\"string\", \"null\"], \"doc\": \"Wave steepness category from the STEEPNESS column, for example SWELL, AVERAGE, or VERY_STEEP.\", \"default\": null}, {\"name\": \"average_wave_period\", \"type\": [\"double\", \"null\"], \"doc\": \"Average wave period from the APD column. Unit: seconds.\", \"default\": null}, {\"name\": \"mean_wave_direction\", \"type\": [\"double\", \"null\"], \"doc\": \"Mean wave direction from the MWD column, measured clockwise from true north. Unit: degrees true.\", \"default\": null}, {\"name\": \"region\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.\", \"default\": null}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    significant_wave_height: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="significant_wave_height"))
    swell_height: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="swell_height"))
    swell_period: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="swell_period"))
    wind_wave_height: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_wave_height"))
    wind_wave_period: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_wave_period"))
    swell_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="swell_direction"))
    wind_wave_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_wave_direction"))
    steepness: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="steepness"))
    average_wave_period: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_wave_period"))
    mean_wave_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mean_wave_direction"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'BuoyDetailedWaveSummary':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'BuoyDetailedWaveSummary':
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
        if 'significant_wave_height' in converted and converted['significant_wave_height'] is not None:
            value = converted['significant_wave_height']
        if 'swell_height' in converted and converted['swell_height'] is not None:
            value = converted['swell_height']
        if 'swell_period' in converted and converted['swell_period'] is not None:
            value = converted['swell_period']
        if 'wind_wave_height' in converted and converted['wind_wave_height'] is not None:
            value = converted['wind_wave_height']
        if 'wind_wave_period' in converted and converted['wind_wave_period'] is not None:
            value = converted['wind_wave_period']
        if 'swell_direction' in converted and converted['swell_direction'] is not None:
            value = converted['swell_direction']
        if 'wind_wave_direction' in converted and converted['wind_wave_direction'] is not None:
            value = converted['wind_wave_direction']
        if 'steepness' in converted and converted['steepness'] is not None:
            value = converted['steepness']
        if 'average_wave_period' in converted and converted['average_wave_period'] is not None:
            value = converted['average_wave_period']
        if 'mean_wave_direction' in converted and converted['mean_wave_direction'] is not None:
            value = converted['mean_wave_direction']
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['BuoyDetailedWaveSummary']:
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
                    return BuoyDetailedWaveSummary.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return BuoyDetailedWaveSummary.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'BuoyDetailedWaveSummary':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='cyrbdesiqinmgovqkavq',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            significant_wave_height=float(37.905496833725515),
            swell_height=float(4.224934338890085),
            swell_period=float(75.2206447273858),
            wind_wave_height=float(59.59573657481053),
            wind_wave_period=float(81.82586907648279),
            swell_direction='ecsplhhzlogaqmxjhfxm',
            wind_wave_direction='nshcthowkqovyacqlqio',
            steepness='gvpwbbhiulyjvztkcopd',
            average_wave_period=float(58.03084277265129),
            mean_wave_direction=float(4.2421570136677245),
            region='zdapxyzpxhfiytcahhzy'
        )