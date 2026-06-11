""" RoadWeatherReading dataclass. """

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
from wsdot_mqtt_producer_data.us.wa.wsdot.roadweather.subsurfacemeasurement import SubSurfaceMeasurement
from wsdot_mqtt_producer_data.us.wa.wsdot.roadweather.surfacemeasurement import SurfaceMeasurement


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RoadWeatherReading:
    """
    A current Scanweb road weather reading including air temperature, humidity, wind, visibility, precipitation totals, and per-sensor road surface and sub-surface measurements.
    
    Attributes:
        station_id (str)
        station_name (str)
        latitude (float)
        longitude (float)
        elevation (typing.Optional[int])
        reading_time (str)
        air_temperature (typing.Optional[float])
        relative_humidity (typing.Optional[int])
        average_wind_speed (typing.Optional[float])
        average_wind_direction (typing.Optional[int])
        wind_gust (typing.Optional[float])
        visibility (typing.Optional[int])
        precipitation_intensity (typing.Optional[int])
        precipitation_type (typing.Optional[int])
        precipitation_past_1_hour (typing.Optional[float])
        precipitation_past_3_hours (typing.Optional[float])
        precipitation_past_6_hours (typing.Optional[float])
        precipitation_past_12_hours (typing.Optional[float])
        precipitation_past_24_hours (typing.Optional[float])
        precipitation_accumulation (typing.Optional[float])
        barometric_pressure (typing.Optional[float])
        snow_depth (typing.Optional[float])
        surface_measurements (typing.List[SurfaceMeasurement])
        sub_surface_measurements (typing.List[SubSurfaceMeasurement])
    """
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    elevation: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="elevation"))
    reading_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reading_time"))
    air_temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_temperature"))
    relative_humidity: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="relative_humidity"))
    average_wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_wind_speed"))
    average_wind_direction: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_wind_direction"))
    wind_gust: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust"))
    visibility: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility"))
    precipitation_intensity: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_intensity"))
    precipitation_type: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_type"))
    precipitation_past_1_hour: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_past_1_hour"))
    precipitation_past_3_hours: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_past_3_hours"))
    precipitation_past_6_hours: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_past_6_hours"))
    precipitation_past_12_hours: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_past_12_hours"))
    precipitation_past_24_hours: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_past_24_hours"))
    precipitation_accumulation: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_accumulation"))
    barometric_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="barometric_pressure"))
    snow_depth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow_depth"))
    surface_measurements: typing.List[SurfaceMeasurement]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="surface_measurements"))
    sub_surface_measurements: typing.List[SubSurfaceMeasurement]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sub_surface_measurements"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'RoadWeatherReading':
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
            if isinstance(result, str):
                result = result.encode('utf-8')

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['RoadWeatherReading']:
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
                return RoadWeatherReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'RoadWeatherReading':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='lgsfozjzafjbvovdjksv',
            station_name='aamctsysxlzpvqcodozu',
            latitude=float(35.620445094874775),
            longitude=float(18.581036461348567),
            elevation=int(82),
            reading_time='solqpczpyrxclksqbzsf',
            air_temperature=float(97.39890250789084),
            relative_humidity=int(28),
            average_wind_speed=float(76.62047755750349),
            average_wind_direction=int(65),
            wind_gust=float(75.62955893402136),
            visibility=int(9),
            precipitation_intensity=int(90),
            precipitation_type=int(3),
            precipitation_past_1_hour=float(66.73140641216348),
            precipitation_past_3_hours=float(34.31822563874627),
            precipitation_past_6_hours=float(48.34768676449488),
            precipitation_past_12_hours=float(42.825732920816364),
            precipitation_past_24_hours=float(30.972271419701126),
            precipitation_accumulation=float(8.907756436410374),
            barometric_pressure=float(83.75795727992266),
            snow_depth=float(76.83888192845549),
            surface_measurements=[None],
            sub_surface_measurements=[None, None, None]
        )