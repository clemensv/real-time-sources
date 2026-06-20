""" Measurement dataclass. """

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
from openaq_amqp_producer_data.org.openaq.parameternameenum import ParameterNameenum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Measurement:
    """
    Latest air-quality measurement for one OpenAQ sensor/location pair from API v3 `GET /v3/locations/{locations_id}/latest`. It carries the observed concentration or meteorological value, parameter metadata and units, timestamp, and coordinates. The bridge polls latest values and emits only changed timestamps/values per sensor.
    
    Attributes:
        location_id (int)
        sensor_id (int)
        country_iso (str)
        parameter_id (int)
        parameter_name (ParameterNameenum)
        parameter_units (str)
        datetime (datetime.datetime)
        value (typing.Optional[float])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        is_valid (typing.Optional[bool])
        has_flags (typing.Optional[bool])
        poll_time (datetime.datetime)
    """
    
    
    location_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    sensor_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    country_iso: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_iso"))
    parameter_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    parameter_name: ParameterNameenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter_name"))
    parameter_units: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter_units"))
    datetime: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    value: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    is_valid: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_valid"))
    has_flags: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="has_flags"))
    poll_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="poll_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Measurement':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        if 'location_id' in data and isinstance(data['location_id'], str):
            data['location_id'] = int(data['location_id'])
        if 'sensor_id' in data and isinstance(data['sensor_id'], str):
            data['sensor_id'] = int(data['sensor_id'])
        if 'parameter_id' in data and isinstance(data['parameter_id'], str):
            data['parameter_id'] = int(data['parameter_id'])
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        if 'location_id' in asdict_result and asdict_result['location_id'] is not None:
            asdict_result['location_id'] = str(asdict_result['location_id'])
        if 'sensor_id' in asdict_result and asdict_result['sensor_id'] is not None:
            asdict_result['sensor_id'] = str(asdict_result['sensor_id'])
        if 'parameter_id' in asdict_result and asdict_result['parameter_id'] is not None:
            asdict_result['parameter_id'] = str(asdict_result['parameter_id'])
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Measurement']:
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
                return Measurement.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Measurement':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            location_id=int(57),
            sensor_id=int(58),
            country_iso='mbyrzhyyidprtsicorih',
            parameter_id=int(30),
            parameter_name=ParameterNameenum.pm25,
            parameter_units='rvfsykyhkkxwfnswvepn',
            datetime=datetime.datetime.now(datetime.timezone.utc),
            value=float(57.99868296510344),
            latitude=float(12.948436879546632),
            longitude=float(46.01056551508931),
            is_valid=False,
            has_flags=False,
            poll_time=datetime.datetime.now(datetime.timezone.utc)
        )