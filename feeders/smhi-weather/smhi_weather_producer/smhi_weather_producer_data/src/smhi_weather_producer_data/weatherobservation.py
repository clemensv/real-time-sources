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
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WeatherObservation:
    """
    Hourly weather observation from a SMHI meteorological station. Multi-parameter observations are assembled from the per-parameter latest-hour API endpoints. Each record contains the most recent values for temperature, wind, pressure, humidity, precipitation, visibility, cloud cover, irradiance, and present weather.
    
    Attributes:
        station_id (str)
        station_name (str)
        observation_time (datetime.datetime)
        air_temperature (typing.Optional[float])
        wind_gust (typing.Optional[float])
        dew_point (typing.Optional[float])
        air_pressure (typing.Optional[float])
        relative_humidity (typing.Optional[int])
        precipitation_last_hour (typing.Optional[float])
        wind_direction (typing.Optional[float])
        wind_speed (typing.Optional[float])
        max_wind_speed (typing.Optional[float])
        visibility (typing.Optional[float])
        total_cloud_cover (typing.Optional[int])
        present_weather (typing.Optional[int])
        sunshine_duration (typing.Optional[float])
        global_irradiance (typing.Optional[float])
        precipitation_intensity (typing.Optional[float])
        quality (typing.Optional[str])
    """
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    observation_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    air_temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_temperature"))
    wind_gust: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust"))
    dew_point: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dew_point"))
    air_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_pressure"))
    relative_humidity: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="relative_humidity"))
    precipitation_last_hour: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_last_hour"))
    wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    max_wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_wind_speed"))
    visibility: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility"))
    total_cloud_cover: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="total_cloud_cover"))
    present_weather: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="present_weather"))
    sunshine_duration: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sunshine_duration"))
    global_irradiance: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="global_irradiance"))
    precipitation_intensity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_intensity"))
    quality: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="quality"))

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

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
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
            station_id='fthtuzcwncrnkclzqqme',
            station_name='sqsktssbwgquawfamgdc',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            air_temperature=float(64.5441699428818),
            wind_gust=float(38.23184509675938),
            dew_point=float(54.93410678058955),
            air_pressure=float(6.359459132231793),
            relative_humidity=int(76),
            precipitation_last_hour=float(17.581222680062623),
            wind_direction=float(85.53436150630421),
            wind_speed=float(5.24440973321052),
            max_wind_speed=float(50.16910145375015),
            visibility=float(43.69004223271664),
            total_cloud_cover=int(37),
            present_weather=int(81),
            sunshine_duration=float(97.76537147210188),
            global_irradiance=float(34.07089640340112),
            precipitation_intensity=float(86.4539701294217),
            quality='inosktkrsfusrscvvmfv'
        )