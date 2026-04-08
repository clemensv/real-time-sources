""" AirQualityIndex dataclass. """

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
class AirQualityIndex:
    """
    Current Polish Air Quality Index (Indeks Jakości Powietrza) for a GIOŚ monitoring station. Includes the overall index value and category plus sub-indices for SO₂, NO₂, PM10, PM2.5, and O₃. Each sub-index uses a 0–5 scale: 0=Bardzo dobry (Very good), 1=Dobry (Good), 2=Umiarkowany (Moderate), 3=Dostateczny (Sufficient), 4=Zły (Bad), 5=Bardzo zły (Very bad). Fields are mapped from the Polish-language /aqindex/getIndex/{stationId} endpoint.
    
    Attributes:
        station_id (int)
        calculation_timestamp (datetime.datetime)
        index_value (typing.Optional[int])
        index_category (typing.Optional[str])
        source_data_timestamp (typing.Optional[datetime.datetime])
        so2_calculation_timestamp (typing.Optional[datetime.datetime])
        so2_index_value (typing.Optional[int])
        so2_index_category (typing.Optional[str])
        so2_source_data_timestamp (typing.Optional[datetime.datetime])
        no2_calculation_timestamp (typing.Optional[datetime.datetime])
        no2_index_value (typing.Optional[int])
        no2_index_category (typing.Optional[str])
        no2_source_data_timestamp (typing.Optional[datetime.datetime])
        pm10_calculation_timestamp (typing.Optional[datetime.datetime])
        pm10_index_value (typing.Optional[int])
        pm10_index_category (typing.Optional[str])
        pm10_source_data_timestamp (typing.Optional[datetime.datetime])
        pm25_calculation_timestamp (typing.Optional[datetime.datetime])
        pm25_index_value (typing.Optional[int])
        pm25_index_category (typing.Optional[str])
        pm25_source_data_timestamp (typing.Optional[datetime.datetime])
        o3_calculation_timestamp (typing.Optional[datetime.datetime])
        o3_index_value (typing.Optional[int])
        o3_index_category (typing.Optional[str])
        o3_source_data_timestamp (typing.Optional[datetime.datetime])
        overall_status (typing.Optional[bool])
        critical_pollutant_code (typing.Optional[str])
    """
    
    
    station_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    calculation_timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="calculation_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    index_value: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="index_value"))
    index_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="index_category"))
    source_data_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_data_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    so2_calculation_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="so2_calculation_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    so2_index_value: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="so2_index_value"))
    so2_index_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="so2_index_category"))
    so2_source_data_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="so2_source_data_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    no2_calculation_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no2_calculation_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    no2_index_value: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no2_index_value"))
    no2_index_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no2_index_category"))
    no2_source_data_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no2_source_data_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    pm10_calculation_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_calculation_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    pm10_index_value: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_index_value"))
    pm10_index_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_index_category"))
    pm10_source_data_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_source_data_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    pm25_calculation_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm25_calculation_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    pm25_index_value: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm25_index_value"))
    pm25_index_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm25_index_category"))
    pm25_source_data_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm25_source_data_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    o3_calculation_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3_calculation_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    o3_index_value: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3_index_value"))
    o3_index_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3_index_category"))
    o3_source_data_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3_source_data_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    overall_status: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="overall_status"))
    critical_pollutant_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="critical_pollutant_code"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'AirQualityIndex':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['AirQualityIndex']:
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
                return AirQualityIndex.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'AirQualityIndex':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id=int(3),
            calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            index_value=int(48),
            index_category='weutxygkyhfrwttbjvfw',
            source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            so2_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            so2_index_value=int(45),
            so2_index_category='zefcyppeqyrhrkxltjjw',
            so2_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            no2_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            no2_index_value=int(63),
            no2_index_category='skhaexghkqwqfpsdiufd',
            no2_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm10_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm10_index_value=int(24),
            pm10_index_category='husnwuvhtabqkynscwkz',
            pm10_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm25_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm25_index_value=int(56),
            pm25_index_category='xpewhlojcgkihtctkjjp',
            pm25_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            o3_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            o3_index_value=int(36),
            o3_index_category='tkfpujxheczxbduzqqvp',
            o3_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            overall_status=False,
            critical_pollutant_code='gisspskutktcndxxnqkb'
        )