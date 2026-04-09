""" WeatherObservation dataclass. """

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
class WeatherObservation:
    """
    10-minute weather observation from a GeoSphere Austria TAWES station.
    Attributes:
        station_id (str): GeoSphere Austria numeric station identifier for the observing station.
        observation_time (str): Observation timestamp in UTC from the GeoSphere API timestamps array.
        temperature (typing.Optional[float]): Air temperature in degrees Celsius over the 10-minute interval.
        humidity (typing.Optional[float]): Relative humidity as a percentage over the 10-minute interval.
        precipitation (typing.Optional[float]): Precipitation in millimeters accumulated during the 10-minute interval.
        wind_direction (typing.Optional[float]): Wind direction in degrees over the 10-minute interval.
        wind_speed (typing.Optional[float]): Wind speed in meters per second over the 10-minute interval.
        pressure (typing.Optional[float]): Atmospheric pressure in hectopascals at station level.
        sunshine_duration (typing.Optional[float]): Sunshine duration in seconds during the 10-minute interval.
        global_radiation (typing.Optional[float]): Global radiation in watts per square meter during the 10-minute interval."""
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    observation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time"))
    temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temperature"))
    humidity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity"))
    precipitation: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation"))
    wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure"))
    sunshine_duration: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sunshine_duration"))
    global_radiation: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="global_radiation"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"WeatherObservation\", \"namespace\": \"at.geosphere.tawes\", \"doc\": \"10-minute weather observation from a GeoSphere Austria TAWES station.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"GeoSphere Austria numeric station identifier for the observing station.\"}, {\"name\": \"observation_time\", \"type\": \"string\", \"doc\": \"Observation timestamp in UTC from the GeoSphere API timestamps array.\"}, {\"name\": \"temperature\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Air temperature in degrees Celsius over the 10-minute interval.\"}, {\"name\": \"humidity\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Relative humidity as a percentage over the 10-minute interval.\"}, {\"name\": \"precipitation\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Precipitation in millimeters accumulated during the 10-minute interval.\"}, {\"name\": \"wind_direction\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Wind direction in degrees over the 10-minute interval.\"}, {\"name\": \"wind_speed\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Wind speed in meters per second over the 10-minute interval.\"}, {\"name\": \"pressure\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Atmospheric pressure in hectopascals at station level.\"}, {\"name\": \"sunshine_duration\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Sunshine duration in seconds during the 10-minute interval.\"}, {\"name\": \"global_radiation\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Global radiation in watts per square meter during the 10-minute interval.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.observation_time=str(self.observation_time)
        self.temperature=float(self.temperature) if self.temperature else None
        self.humidity=float(self.humidity) if self.humidity else None
        self.precipitation=float(self.precipitation) if self.precipitation else None
        self.wind_direction=float(self.wind_direction) if self.wind_direction else None
        self.wind_speed=float(self.wind_speed) if self.wind_speed else None
        self.pressure=float(self.pressure) if self.pressure else None
        self.sunshine_duration=float(self.sunshine_duration) if self.sunshine_duration else None
        self.global_radiation=float(self.global_radiation) if self.global_radiation else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WeatherObservation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WeatherObservation']:
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
            return WeatherObservation.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WeatherObservation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')