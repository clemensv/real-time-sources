""" WeatherObservation dataclass. """

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
class WeatherObservation:
    """
    Latest weather observation from a NWS surface station. Observations are fetched from the api.weather.gov /stations/{stationId}/observations/latest endpoint. Measurement values are extracted from NWS quantity objects (unitCode + value + qualityControl).
    
    Attributes:
        station_id (str)
        timestamp (datetime.datetime)
        text_description (typing.Optional[str])
        temperature (typing.Optional[float])
        dewpoint (typing.Optional[float])
        wind_direction (typing.Optional[float])
        wind_speed (typing.Optional[float])
        wind_gust (typing.Optional[float])
        barometric_pressure (typing.Optional[float])
        sea_level_pressure (typing.Optional[float])
        visibility (typing.Optional[float])
        relative_humidity (typing.Optional[float])
        wind_chill (typing.Optional[float])
        heat_index (typing.Optional[float])
        state (typing.Optional[str])
        zone_id (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"WeatherObservation\", \"doc\": \"Latest weather observation from a NWS surface station. Observations are fetched from the api.weather.gov /stations/{stationId}/observations/latest endpoint. Measurement values are extracted from NWS quantity objects (unitCode + value + qualityControl).\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"ICAO or cooperative observer station identifier.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"UTC timestamp of the observation.\"}, {\"name\": \"text_description\", \"type\": [\"string\", \"null\"], \"doc\": \"Brief text summary of current conditions, e.g. 'Clear', 'Mostly Cloudy', 'Rain'.\", \"default\": null}, {\"name\": \"temperature\", \"type\": [\"double\", \"null\"], \"doc\": \"Air temperature at the time of observation.\", \"default\": null}, {\"name\": \"dewpoint\", \"type\": [\"double\", \"null\"], \"doc\": \"Dew point temperature.\", \"default\": null}, {\"name\": \"wind_direction\", \"type\": [\"double\", \"null\"], \"doc\": \"Wind direction in degrees from which the wind is blowing.\", \"default\": null}, {\"name\": \"wind_speed\", \"type\": [\"double\", \"null\"], \"doc\": \"Sustained wind speed.\", \"default\": null}, {\"name\": \"wind_gust\", \"type\": [\"double\", \"null\"], \"doc\": \"Peak wind gust speed, null if no gusts observed.\", \"default\": null}, {\"name\": \"barometric_pressure\", \"type\": [\"double\", \"null\"], \"doc\": \"Station barometric pressure (not reduced to sea level).\", \"default\": null}, {\"name\": \"sea_level_pressure\", \"type\": [\"double\", \"null\"], \"doc\": \"Atmospheric pressure reduced to mean sea level.\", \"default\": null}, {\"name\": \"visibility\", \"type\": [\"double\", \"null\"], \"doc\": \"Horizontal visibility.\", \"default\": null}, {\"name\": \"relative_humidity\", \"type\": [\"double\", \"null\"], \"doc\": \"Relative humidity percentage.\", \"default\": null}, {\"name\": \"wind_chill\", \"type\": [\"double\", \"null\"], \"doc\": \"Calculated wind chill temperature, null when conditions do not warrant it.\", \"default\": null}, {\"name\": \"heat_index\", \"type\": [\"double\", \"null\"], \"doc\": \"Calculated heat index temperature, null when conditions do not warrant it.\", \"default\": null}, {\"name\": \"state\", \"type\": [\"null\", \"string\"], \"doc\": \"Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.\", \"default\": null}, {\"name\": \"zone_id\", \"type\": [\"null\", \"string\"], \"doc\": \"Normalized routing field 'zone_id' added for MQTT/AMQP subscriber filtering.\", \"default\": null}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    text_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="text_description"))
    temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temperature"))
    dewpoint: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dewpoint"))
    wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    wind_gust: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust"))
    barometric_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="barometric_pressure"))
    sea_level_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sea_level_pressure"))
    visibility: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility"))
    relative_humidity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="relative_humidity"))
    wind_chill: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_chill"))
    heat_index: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="heat_index"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    zone_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="zone_id"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WeatherObservation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'WeatherObservation':
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
        if 'text_description' in converted and converted['text_description'] is not None:
            value = converted['text_description']
        if 'temperature' in converted and converted['temperature'] is not None:
            value = converted['temperature']
        if 'dewpoint' in converted and converted['dewpoint'] is not None:
            value = converted['dewpoint']
        if 'wind_direction' in converted and converted['wind_direction'] is not None:
            value = converted['wind_direction']
        if 'wind_speed' in converted and converted['wind_speed'] is not None:
            value = converted['wind_speed']
        if 'wind_gust' in converted and converted['wind_gust'] is not None:
            value = converted['wind_gust']
        if 'barometric_pressure' in converted and converted['barometric_pressure'] is not None:
            value = converted['barometric_pressure']
        if 'sea_level_pressure' in converted and converted['sea_level_pressure'] is not None:
            value = converted['sea_level_pressure']
        if 'visibility' in converted and converted['visibility'] is not None:
            value = converted['visibility']
        if 'relative_humidity' in converted and converted['relative_humidity'] is not None:
            value = converted['relative_humidity']
        if 'wind_chill' in converted and converted['wind_chill'] is not None:
            value = converted['wind_chill']
        if 'heat_index' in converted and converted['heat_index'] is not None:
            value = converted['heat_index']
        if 'state' in converted and converted['state'] is not None:
            value = converted['state']
        if 'zone_id' in converted and converted['zone_id'] is not None:
            value = converted['zone_id']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WeatherObservation']:
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
                    return WeatherObservation.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WeatherObservation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WeatherObservation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='shcmjielraphkphcfyqa',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            text_description='rphklnlczlhwwftnfbnl',
            temperature=float(96.42844992261912),
            dewpoint=float(30.6193707631788),
            wind_direction=float(47.707175693992774),
            wind_speed=float(4.126417494562751),
            wind_gust=float(36.96584813702104),
            barometric_pressure=float(86.96102529627561),
            sea_level_pressure=float(7.043521736462511),
            visibility=float(50.33218787657866),
            relative_humidity=float(64.25007981578977),
            wind_chill=float(2.4575051133748693),
            heat_index=float(76.26793257969209),
            state='iztzrykifsrvmndebdvr',
            zone_id='kzrndfoydahbdaojchwe'
        )