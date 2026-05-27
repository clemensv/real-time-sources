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
    A current environmental measurement from Environment and Climate Change Canada (ECCC). It carries current weather observations when the upstream feed reports a new or refreshed value.
    
    Attributes:
        msc_id (str)
        station_name (str)
        observation_time (datetime.datetime)
        air_temperature (typing.Optional[float])
        dew_point (typing.Optional[float])
        relative_humidity (typing.Optional[int])
        station_pressure (typing.Optional[float])
        wind_speed (typing.Optional[float])
        wind_direction (typing.Optional[int])
        wind_gust (typing.Optional[float])
        precipitation_1hr (typing.Optional[float])
        mean_sea_level_pressure (typing.Optional[float])
        visibility (typing.Optional[float])
        snow_depth (typing.Optional[float])
        total_cloud_cover (typing.Optional[int])
        pressure_tendency_3hr (typing.Optional[float])
        max_temperature_24hr (typing.Optional[float])
        min_temperature_24hr (typing.Optional[float])
        wind_speed_1hr (typing.Optional[float])
        wind_gust_1hr (typing.Optional[float])
        precipitation_24hr (typing.Optional[float])
        altimeter_setting (typing.Optional[float])
        province (typing.Optional[str])
    """
    
    
    msc_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="msc_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    observation_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    air_temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_temperature"))
    dew_point: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dew_point"))
    relative_humidity: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="relative_humidity"))
    station_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_pressure"))
    wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    wind_direction: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_gust: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust"))
    precipitation_1hr: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_1hr"))
    mean_sea_level_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mean_sea_level_pressure"))
    visibility: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility"))
    snow_depth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow_depth"))
    total_cloud_cover: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="total_cloud_cover"))
    pressure_tendency_3hr: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_tendency_3hr"))
    max_temperature_24hr: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_temperature_24hr"))
    min_temperature_24hr: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="min_temperature_24hr"))
    wind_speed_1hr: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed_1hr"))
    wind_gust_1hr: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust_1hr"))
    precipitation_24hr: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation_24hr"))
    altimeter_setting: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altimeter_setting"))
    province: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="province"))

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
            msc_id='noirkavciddkauqghvfn',
            station_name='ewnvnscttfitghlwuqex',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            air_temperature=float(3.9560623594654953),
            dew_point=float(94.13671232386865),
            relative_humidity=int(82),
            station_pressure=float(48.710152802659564),
            wind_speed=float(19.570613969869456),
            wind_direction=int(87),
            wind_gust=float(1.6150822451561408),
            precipitation_1hr=float(86.37514867049363),
            mean_sea_level_pressure=float(43.91634080143666),
            visibility=float(81.89156901298549),
            snow_depth=float(14.833501506351187),
            total_cloud_cover=int(65),
            pressure_tendency_3hr=float(79.15076588305237),
            max_temperature_24hr=float(57.21662318600189),
            min_temperature_24hr=float(70.57700771076539),
            wind_speed_1hr=float(97.15491425828388),
            wind_gust_1hr=float(20.39500676832763),
            precipitation_24hr=float(93.83655232595864),
            altimeter_setting=float(33.52341956509982),
            province='lxtbecirwobjdcwjrnvf'
        )