""" BuoyObservation dataclass. """

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
class BuoyObservation:
    """
    Real-time standard meteorological and oceanographic observation from an NDBC buoy, C-MAN station, or partner platform. Sourced from the NDBC latest_obs.txt composite file which is updated every five minutes. Fields cover wind, waves, pressure, temperature, dewpoint, pressure tendency, visibility, and tide.
    
    Attributes:
        station_id (str)
        latitude (float)
        longitude (float)
        timestamp (datetime.datetime)
        wind_direction (typing.Optional[float])
        wind_speed (typing.Optional[float])
        gust (typing.Optional[float])
        wave_height (typing.Optional[float])
        dominant_wave_period (typing.Optional[float])
        average_wave_period (typing.Optional[float])
        mean_wave_direction (typing.Optional[float])
        pressure (typing.Optional[float])
        air_temperature (typing.Optional[float])
        water_temperature (typing.Optional[float])
        dewpoint (typing.Optional[float])
        pressure_tendency (typing.Optional[float])
        visibility (typing.Optional[float])
        tide (typing.Optional[float])
        region (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"BuoyObservation\", \"doc\": \"Real-time standard meteorological and oceanographic observation from an NDBC buoy, C-MAN station, or partner platform. Sourced from the NDBC latest_obs.txt composite file which is updated every five minutes. Fields cover wind, waves, pressure, temperature, dewpoint, pressure tendency, visibility, and tide.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"NDBC station identifier. Five-character alphanumeric code assigned by NDBC (e.g. '41001' for deep-ocean buoys, 'BURL1' for C-MAN stations).\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"Latitude of the observing platform in decimal degrees north. Negative values indicate southern hemisphere.\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"Longitude of the observing platform in decimal degrees east. Negative values indicate western hemisphere.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC data.\"}, {\"name\": \"wind_direction\", \"type\": [\"double\", \"null\"], \"doc\": \"Wind direction (the direction the wind is coming from) averaged over an 8-minute period for buoys or a 2-minute period for land stations. Unit: degrees true.\", \"default\": null}, {\"name\": \"wind_speed\", \"type\": [\"double\", \"null\"], \"doc\": \"Average wind speed during the observation period: 8 minutes for buoys, 2 minutes for land stations. Unit: meters per second.\", \"default\": null}, {\"name\": \"gust\", \"type\": [\"double\", \"null\"], \"doc\": \"Peak 5-second or 8-second gust speed during the observation period. Unit: meters per second.\", \"default\": null}, {\"name\": \"wave_height\", \"type\": [\"double\", \"null\"], \"doc\": \"Significant wave height \u2014 the average of the highest one-third of all wave heights during a 20-minute sampling period. Unit: meters.\", \"default\": null}, {\"name\": \"dominant_wave_period\", \"type\": [\"double\", \"null\"], \"doc\": \"Dominant wave period \u2014 the period (in seconds) of the wave band with the maximum energy in the spectral wave analysis. Unit: seconds.\", \"default\": null}, {\"name\": \"average_wave_period\", \"type\": [\"double\", \"null\"], \"doc\": \"Average wave period of all waves during the 20-minute sampling period. Unit: seconds.\", \"default\": null}, {\"name\": \"mean_wave_direction\", \"type\": [\"double\", \"null\"], \"doc\": \"Mean wave direction corresponding to the energy at the dominant wave period (DPD). Unit: degrees true.\", \"default\": null}, {\"name\": \"pressure\", \"type\": [\"double\", \"null\"], \"doc\": \"Sea-level pressure reduced using the standard atmosphere from the station elevation. Unit: hectopascals.\", \"default\": null}, {\"name\": \"air_temperature\", \"type\": [\"double\", \"null\"], \"doc\": \"Air temperature measured at the station. Unit: degrees Celsius.\", \"default\": null}, {\"name\": \"water_temperature\", \"type\": [\"double\", \"null\"], \"doc\": \"Sea surface temperature. For buoys, measured by a hull-contact sensor near the waterline. Unit: degrees Celsius.\", \"default\": null}, {\"name\": \"dewpoint\", \"type\": [\"double\", \"null\"], \"doc\": \"Dewpoint temperature computed from air temperature and relative humidity. Unit: degrees Celsius.\", \"default\": null}, {\"name\": \"pressure_tendency\", \"type\": [\"double\", \"null\"], \"doc\": \"Pressure tendency \u2014 the signed change in sea-level pressure over the preceding 3 hours. A negative value indicates falling pressure; a positive value indicates rising pressure. Unit: hectopascals.\", \"default\": null}, {\"name\": \"visibility\", \"type\": [\"double\", \"null\"], \"doc\": \"Station visibility as reported by the observing platform. Buoy visibility sensors have a range of 0 to 1.6 nautical miles and are generally only available on C-MAN stations. Unit: nautical miles.\", \"default\": null}, {\"name\": \"tide\", \"type\": [\"double\", \"null\"], \"doc\": \"Water level above or below Mean Lower Low Water (MLLW) at coastal and C-MAN stations. Unit: feet.\", \"default\": null}, {\"name\": \"region\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.\", \"default\": null}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    gust: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gust"))
    wave_height: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wave_height"))
    dominant_wave_period: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dominant_wave_period"))
    average_wave_period: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_wave_period"))
    mean_wave_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mean_wave_direction"))
    pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure"))
    air_temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_temperature"))
    water_temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_temperature"))
    dewpoint: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dewpoint"))
    pressure_tendency: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_tendency"))
    visibility: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility"))
    tide: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tide"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'BuoyObservation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'BuoyObservation':
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
        if 'latitude' in converted and converted['latitude'] is not None:
            value = converted['latitude']
        if 'longitude' in converted and converted['longitude'] is not None:
            value = converted['longitude']
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, str):
                converted['timestamp'] = datetime.datetime.fromisoformat(value)
        if 'wind_direction' in converted and converted['wind_direction'] is not None:
            value = converted['wind_direction']
        if 'wind_speed' in converted and converted['wind_speed'] is not None:
            value = converted['wind_speed']
        if 'gust' in converted and converted['gust'] is not None:
            value = converted['gust']
        if 'wave_height' in converted and converted['wave_height'] is not None:
            value = converted['wave_height']
        if 'dominant_wave_period' in converted and converted['dominant_wave_period'] is not None:
            value = converted['dominant_wave_period']
        if 'average_wave_period' in converted and converted['average_wave_period'] is not None:
            value = converted['average_wave_period']
        if 'mean_wave_direction' in converted and converted['mean_wave_direction'] is not None:
            value = converted['mean_wave_direction']
        if 'pressure' in converted and converted['pressure'] is not None:
            value = converted['pressure']
        if 'air_temperature' in converted and converted['air_temperature'] is not None:
            value = converted['air_temperature']
        if 'water_temperature' in converted and converted['water_temperature'] is not None:
            value = converted['water_temperature']
        if 'dewpoint' in converted and converted['dewpoint'] is not None:
            value = converted['dewpoint']
        if 'pressure_tendency' in converted and converted['pressure_tendency'] is not None:
            value = converted['pressure_tendency']
        if 'visibility' in converted and converted['visibility'] is not None:
            value = converted['visibility']
        if 'tide' in converted and converted['tide'] is not None:
            value = converted['tide']
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['BuoyObservation']:
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
                    return BuoyObservation.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return BuoyObservation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'BuoyObservation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='qtfhenhavhgpgxfhipau',
            latitude=float(87.74970790989157),
            longitude=float(98.82256358210442),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(22.38205373388469),
            wind_speed=float(50.51766989495352),
            gust=float(74.07549028306242),
            wave_height=float(40.10805684143786),
            dominant_wave_period=float(51.71656111542266),
            average_wave_period=float(40.433094224576415),
            mean_wave_direction=float(24.004512614747032),
            pressure=float(45.17902293158993),
            air_temperature=float(6.743070241314053),
            water_temperature=float(42.818570880536136),
            dewpoint=float(97.2401376580231),
            pressure_tendency=float(57.27401451866777),
            visibility=float(9.256365123513977),
            tide=float(82.97439426800291),
            region='bxehglnogjasjkoxomnb'
        )