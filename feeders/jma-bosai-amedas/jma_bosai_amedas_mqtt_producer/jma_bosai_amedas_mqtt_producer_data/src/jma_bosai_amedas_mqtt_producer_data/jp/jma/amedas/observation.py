""" Observation dataclass. """

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
from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.observationeventenum import ObservationEventEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Observation:
    """
    Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.
    
    Attributes:
        station_code (str)
        observed_at (datetime.datetime)
        observed_at_local (datetime.datetime)
        temp (typing.Optional[float])
        temp_qc_flag (typing.Optional[int])
        humidity (typing.Optional[float])
        humidity_qc_flag (typing.Optional[int])
        pressure (typing.Optional[float])
        pressure_qc_flag (typing.Optional[int])
        normal_pressure (typing.Optional[float])
        normal_pressure_qc_flag (typing.Optional[int])
        wind_speed (typing.Optional[float])
        wind_speed_qc_flag (typing.Optional[int])
        wind_direction (typing.Optional[float])
        wind_direction_qc_flag (typing.Optional[int])
        wind_gust (typing.Optional[float])
        wind_gust_qc_flag (typing.Optional[int])
        wind_gust_direction (typing.Optional[float])
        wind_gust_time (typing.Optional[datetime.datetime])
        max_temp (typing.Optional[float])
        max_temp_time (typing.Optional[datetime.datetime])
        min_temp (typing.Optional[float])
        min_temp_time (typing.Optional[datetime.datetime])
        precipitation10m (typing.Optional[float])
        precipitation10m_qc_flag (typing.Optional[int])
        precipitation1h (typing.Optional[float])
        precipitation1h_qc_flag (typing.Optional[int])
        precipitation3h (typing.Optional[float])
        precipitation3h_qc_flag (typing.Optional[int])
        precipitation24h (typing.Optional[float])
        precipitation24h_qc_flag (typing.Optional[int])
        sun10m (typing.Optional[float])
        sun10m_qc_flag (typing.Optional[int])
        sun1h (typing.Optional[float])
        sun1h_qc_flag (typing.Optional[int])
        snow (typing.Optional[float])
        snow_qc_flag (typing.Optional[int])
        snow1h (typing.Optional[float])
        snow1h_qc_flag (typing.Optional[int])
        snow6h (typing.Optional[float])
        snow6h_qc_flag (typing.Optional[int])
        snow12h (typing.Optional[float])
        snow12h_qc_flag (typing.Optional[int])
        snow24h (typing.Optional[float])
        snow24h_qc_flag (typing.Optional[int])
        visibility (typing.Optional[float])
        visibility_qc_flag (typing.Optional[int])
        cloud (typing.Optional[float])
        cloud_qc_flag (typing.Optional[int])
        weather (typing.Optional[float])
        weather_qc_flag (typing.Optional[int])
        prefecture (str)
        event (ObservationEventEnum)
    """
    
    
    station_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_code"))
    observed_at: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observed_at", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    observed_at_local: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observed_at_local", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp"))
    temp_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_qc_flag"))
    humidity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity"))
    humidity_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity_qc_flag"))
    pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure"))
    pressure_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_qc_flag"))
    normal_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="normal_pressure"))
    normal_pressure_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="normal_pressure_qc_flag"))
    wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    wind_speed_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed_qc_flag"))
    wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_direction_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction_qc_flag"))
    wind_gust: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust"))
    wind_gust_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust_qc_flag"))
    wind_gust_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust_direction"))
    wind_gust_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    max_temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_temp"))
    max_temp_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_temp_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    min_temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="min_temp"))
    min_temp_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="min_temp_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    precipitation10m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation10m"))
    precipitation10m_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation10m_qc_flag"))
    precipitation1h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation1h"))
    precipitation1h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation1h_qc_flag"))
    precipitation3h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation3h"))
    precipitation3h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation3h_qc_flag"))
    precipitation24h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation24h"))
    precipitation24h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation24h_qc_flag"))
    sun10m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun10m"))
    sun10m_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun10m_qc_flag"))
    sun1h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun1h"))
    sun1h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun1h_qc_flag"))
    snow: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow"))
    snow_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow_qc_flag"))
    snow1h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow1h"))
    snow1h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow1h_qc_flag"))
    snow6h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow6h"))
    snow6h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow6h_qc_flag"))
    snow12h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow12h"))
    snow12h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow12h_qc_flag"))
    snow24h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow24h"))
    snow24h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow24h_qc_flag"))
    visibility: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility"))
    visibility_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility_qc_flag"))
    cloud: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud"))
    cloud_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud_qc_flag"))
    weather: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="weather"))
    weather_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="weather_qc_flag"))
    prefecture: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="prefecture"))
    event: ObservationEventEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Observation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Observation']:
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
                return Observation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Observation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_code='pnpilvwzscmcgucjnltb',
            observed_at=datetime.datetime.now(datetime.timezone.utc),
            observed_at_local=datetime.datetime.now(datetime.timezone.utc),
            temp=float(72.94007097121123),
            temp_qc_flag=int(79),
            humidity=float(42.429992224333624),
            humidity_qc_flag=int(93),
            pressure=float(86.5005665426254),
            pressure_qc_flag=int(78),
            normal_pressure=float(10.387333359576212),
            normal_pressure_qc_flag=int(16),
            wind_speed=float(20.325938782375786),
            wind_speed_qc_flag=int(59),
            wind_direction=float(23.157858750016167),
            wind_direction_qc_flag=int(72),
            wind_gust=float(44.2675290295839),
            wind_gust_qc_flag=int(39),
            wind_gust_direction=float(29.13984920377638),
            wind_gust_time=datetime.datetime.now(datetime.timezone.utc),
            max_temp=float(59.95056305027473),
            max_temp_time=datetime.datetime.now(datetime.timezone.utc),
            min_temp=float(40.7105204109899),
            min_temp_time=datetime.datetime.now(datetime.timezone.utc),
            precipitation10m=float(20.99366644872508),
            precipitation10m_qc_flag=int(9),
            precipitation1h=float(48.230212405449166),
            precipitation1h_qc_flag=int(71),
            precipitation3h=float(68.48379092250451),
            precipitation3h_qc_flag=int(89),
            precipitation24h=float(3.5769612474544576),
            precipitation24h_qc_flag=int(74),
            sun10m=float(54.78494803095624),
            sun10m_qc_flag=int(2),
            sun1h=float(47.23251303057127),
            sun1h_qc_flag=int(90),
            snow=float(31.166832585464753),
            snow_qc_flag=int(53),
            snow1h=float(88.7853700605655),
            snow1h_qc_flag=int(3),
            snow6h=float(25.78214991128047),
            snow6h_qc_flag=int(74),
            snow12h=float(39.261696099335666),
            snow12h_qc_flag=int(20),
            snow24h=float(89.66684539957838),
            snow24h_qc_flag=int(0),
            visibility=float(38.440824772294576),
            visibility_qc_flag=int(98),
            cloud=float(3.1951278363943514),
            cloud_qc_flag=int(17),
            weather=float(83.32854609529839),
            weather_qc_flag=int(20),
            prefecture='gmwiealcwurspwczbrno',
            event=ObservationEventEnum.observation
        )