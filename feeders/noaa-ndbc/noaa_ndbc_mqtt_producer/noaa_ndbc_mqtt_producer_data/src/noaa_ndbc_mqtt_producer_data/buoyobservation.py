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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['BuoyObservation']:
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
            station_id='vxumrqahgilokjysvpes',
            latitude=float(38.262822177562406),
            longitude=float(41.97631389322034),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(86.09647732068318),
            wind_speed=float(95.96576214472924),
            gust=float(69.89725480367012),
            wave_height=float(70.3545703295257),
            dominant_wave_period=float(88.13780112883268),
            average_wave_period=float(58.807339871725176),
            mean_wave_direction=float(12.181548859392421),
            pressure=float(72.39786104627433),
            air_temperature=float(22.668737134686346),
            water_temperature=float(24.871833159929025),
            dewpoint=float(58.85277821898225),
            pressure_tendency=float(58.85184426843628),
            visibility=float(66.37062557739873),
            tide=float(2.8163731797273495),
            region='isayqvbwceqhxrfcwnls'
        )