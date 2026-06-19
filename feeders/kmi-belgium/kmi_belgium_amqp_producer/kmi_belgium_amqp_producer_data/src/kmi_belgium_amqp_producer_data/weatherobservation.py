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
    A current environmental measurement from the Royal Meteorological Institute of Belgium (KMI/IRM). It carries weather observations when the upstream feed reports a new or refreshed value.
    
    Attributes:
        station_code (str)
        observation_time (datetime.datetime)
        precip_quantity (typing.Optional[float])
        temp_dry_shelter_avg (typing.Optional[float])
        temp_grass_pt100_avg (typing.Optional[float])
        temp_soil_avg (typing.Optional[float])
        temp_soil_avg_5cm (typing.Optional[float])
        temp_soil_avg_10cm (typing.Optional[float])
        temp_soil_avg_20cm (typing.Optional[float])
        temp_soil_avg_50cm (typing.Optional[float])
        wind_speed_10m (typing.Optional[float])
        wind_speed_avg_30m (typing.Optional[float])
        wind_direction (typing.Optional[float])
        wind_gusts_speed (typing.Optional[float])
        humidity_rel_shelter_avg (typing.Optional[float])
        pressure (typing.Optional[float])
        sun_duration (typing.Optional[float])
        short_wave_from_sky_avg (typing.Optional[float])
        sun_int_avg (typing.Optional[float])
        region (typing.Optional[str])
    """
    
    
    station_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_code"))
    observation_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    precip_quantity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precip_quantity"))
    temp_dry_shelter_avg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_dry_shelter_avg"))
    temp_grass_pt100_avg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_grass_pt100_avg"))
    temp_soil_avg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_soil_avg"))
    temp_soil_avg_5cm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_soil_avg_5cm"))
    temp_soil_avg_10cm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_soil_avg_10cm"))
    temp_soil_avg_20cm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_soil_avg_20cm"))
    temp_soil_avg_50cm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_soil_avg_50cm"))
    wind_speed_10m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed_10m"))
    wind_speed_avg_30m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed_avg_30m"))
    wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_gusts_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gusts_speed"))
    humidity_rel_shelter_avg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity_rel_shelter_avg"))
    pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure"))
    sun_duration: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun_duration"))
    short_wave_from_sky_avg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="short_wave_from_sky_avg"))
    sun_int_avg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun_int_avg"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))

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
            station_code='cvydkhacryayperuxuwh',
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            precip_quantity=float(35.68285787338961),
            temp_dry_shelter_avg=float(63.89207844948036),
            temp_grass_pt100_avg=float(60.51326482451592),
            temp_soil_avg=float(0.6738602770033242),
            temp_soil_avg_5cm=float(80.52348369183446),
            temp_soil_avg_10cm=float(66.6760341794662),
            temp_soil_avg_20cm=float(37.49375254599118),
            temp_soil_avg_50cm=float(47.97090955162303),
            wind_speed_10m=float(12.660959361537794),
            wind_speed_avg_30m=float(20.29214687153622),
            wind_direction=float(59.23494445850744),
            wind_gusts_speed=float(28.22994855179939),
            humidity_rel_shelter_avg=float(67.98238410709943),
            pressure=float(67.36873105744074),
            sun_duration=float(51.61202376869443),
            short_wave_from_sky_avg=float(48.949418189655105),
            sun_int_avg=float(70.96067529622438),
            region='zlhxdztolenbphdugqmd'
        )