""" SensorReading dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SensorReading:
    """
    Schema for the latest normalized Sensor.Community telemetry reading for a single sensor and timestamp, covering particulate matter, temperature, humidity, pressure, and supported noise measurements.
    
    Attributes:
        sensor_id (int)
        timestamp (str)
        sensor_type_name (str)
        pm10_ug_m3 (typing.Optional[float])
        pm2_5_ug_m3 (typing.Optional[float])
        pm1_0_ug_m3 (typing.Optional[float])
        pm4_0_ug_m3 (typing.Optional[float])
        temperature_celsius (typing.Optional[float])
        humidity_percent (typing.Optional[float])
        pressure_pa (typing.Optional[float])
        pressure_sealevel_pa (typing.Optional[float])
        noise_laeq_db (typing.Optional[float])
        noise_la_min_db (typing.Optional[float])
        noise_la_max_db (typing.Optional[float])
    """
    
    
    sensor_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_id"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    sensor_type_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_type_name"))
    pm10_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_ug_m3"))
    pm2_5_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm2_5_ug_m3"))
    pm1_0_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm1_0_ug_m3"))
    pm4_0_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm4_0_ug_m3"))
    temperature_celsius: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temperature_celsius"))
    humidity_percent: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity_percent"))
    pressure_pa: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_pa"))
    pressure_sealevel_pa: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_sealevel_pa"))
    noise_laeq_db: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="noise_laeq_db"))
    noise_la_min_db: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="noise_la_min_db"))
    noise_la_max_db: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="noise_la_max_db"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SensorReading':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SensorReading']:
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
                return SensorReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SensorReading':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            sensor_id=int(2),
            timestamp='qqtpshwhltahebudarkb',
            sensor_type_name='publzvkhvwytltyxrqai',
            pm10_ug_m3=float(33.755339014989026),
            pm2_5_ug_m3=float(84.095951246011),
            pm1_0_ug_m3=float(33.600040045365375),
            pm4_0_ug_m3=float(81.07258413037425),
            temperature_celsius=float(60.36022476479885),
            humidity_percent=float(86.2108947244489),
            pressure_pa=float(65.19667270860711),
            pressure_sealevel_pa=float(28.743757110745662),
            noise_laeq_db=float(45.090203455833446),
            noise_la_min_db=float(98.42121512232839),
            noise_la_max_db=float(68.37681598752475)
        )