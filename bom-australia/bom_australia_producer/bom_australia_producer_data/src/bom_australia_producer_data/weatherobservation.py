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
    Half-hourly surface weather observation from a BOM automatic weather station. Each record contains temperature, wind, pressure, humidity, rainfall, cloud, and visibility measurements as reported in the station's 72-hour observation product.
    
    Attributes:
        station_wmo (int)
        station_name (str)
        observation_time_utc (datetime.datetime)
        local_time (typing.Optional[str])
        air_temp (typing.Optional[float])
        apparent_temp (typing.Optional[float])
        dewpt (typing.Optional[float])
        rel_hum (typing.Optional[int])
        delta_t (typing.Optional[float])
        wind_dir (typing.Optional[str])
        wind_spd_kmh (typing.Optional[int])
        wind_spd_kt (typing.Optional[int])
        gust_kmh (typing.Optional[int])
        gust_kt (typing.Optional[int])
        press (typing.Optional[float])
        press_qnh (typing.Optional[float])
        press_msl (typing.Optional[float])
        press_tend (typing.Optional[str])
        rain_trace (typing.Optional[str])
        cloud (typing.Optional[str])
        cloud_oktas (typing.Optional[int])
        cloud_base_m (typing.Optional[int])
        cloud_type (typing.Optional[str])
        vis_km (typing.Optional[str])
        weather (typing.Optional[str])
        sea_state (typing.Optional[str])
        swell_dir_worded (typing.Optional[str])
        swell_height (typing.Optional[float])
        swell_period (typing.Optional[float])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
    """
    
    
    station_wmo: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_wmo"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    observation_time_utc: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time_utc", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    local_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="local_time"))
    air_temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_temp"))
    apparent_temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="apparent_temp"))
    dewpt: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dewpt"))
    rel_hum: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rel_hum"))
    delta_t: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delta_t"))
    wind_dir: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_dir"))
    wind_spd_kmh: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_spd_kmh"))
    wind_spd_kt: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_spd_kt"))
    gust_kmh: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gust_kmh"))
    gust_kt: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gust_kt"))
    press: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="press"))
    press_qnh: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="press_qnh"))
    press_msl: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="press_msl"))
    press_tend: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="press_tend"))
    rain_trace: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rain_trace"))
    cloud: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud"))
    cloud_oktas: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud_oktas"))
    cloud_base_m: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud_base_m"))
    cloud_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud_type"))
    vis_km: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vis_km"))
    weather: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="weather"))
    sea_state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sea_state"))
    swell_dir_worded: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="swell_dir_worded"))
    swell_height: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="swell_height"))
    swell_period: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="swell_period"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))

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
            station_wmo=int(9),
            station_name='sjyvxzjhdygacjbvqtro',
            observation_time_utc=datetime.datetime.now(datetime.timezone.utc),
            local_time='nuxgwvjhxqeubsjhakgj',
            air_temp=float(85.76195286883929),
            apparent_temp=float(84.37127976386077),
            dewpt=float(14.028182731435345),
            rel_hum=int(1),
            delta_t=float(11.119041078073266),
            wind_dir='hjnszttstlnghfekvpht',
            wind_spd_kmh=int(68),
            wind_spd_kt=int(79),
            gust_kmh=int(48),
            gust_kt=int(25),
            press=float(82.37310490991709),
            press_qnh=float(99.7097175727205),
            press_msl=float(74.56055391802884),
            press_tend='lqmedmrzgyjmutmatgsm',
            rain_trace='dgxdgngizletyqpyboaa',
            cloud='wvdhkbqjciwfcdqyvmpq',
            cloud_oktas=int(24),
            cloud_base_m=int(73),
            cloud_type='pvxrmcmjupkqbxvlufrn',
            vis_km='rytcjcxgubcuwtyjhyyt',
            weather='qmzjypdxcpogkqkeifjv',
            sea_state='tlhsjxydsajclcdxbooa',
            swell_dir_worded='zkijpwuaqdztpigctghy',
            swell_height=float(4.325732776250457),
            swell_period=float(11.389270165994548),
            latitude=float(68.113048697121),
            longitude=float(90.56200345688616)
        )