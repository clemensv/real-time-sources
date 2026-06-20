""" Location dataclass. """

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
class Location:
    """
    Reference metadata for one OpenAQ monitoring location from API v3 `GET /v3/locations`. It identifies a physical or mobile air-quality monitoring site, its WGS 84 coordinates, country, ownership/provider context, monitor/mobile flags, license attribution, and first/last observation dates. Emitted before telemetry and refreshed periodically so consumers can interpret measurements without separately calling OpenAQ.
    
    Attributes:
        location_id (int)
        name (typing.Optional[str])
        locality (typing.Optional[str])
        timezone (str)
        country_iso (str)
        country_name (str)
        owner_id (typing.Optional[int])
        owner_name (typing.Optional[str])
        provider_id (typing.Optional[int])
        provider_name (typing.Optional[str])
        is_mobile (bool)
        is_monitor (bool)
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        datetime_first (typing.Optional[datetime.datetime])
        datetime_last (typing.Optional[datetime.datetime])
        license (typing.Optional[str])
        sensor_count (int)
    """
    
    
    location_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    locality: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="locality"))
    timezone: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timezone"))
    country_iso: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_iso"))
    country_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_name"))
    owner_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="owner_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    owner_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="owner_name"))
    provider_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="provider_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    provider_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="provider_name"))
    is_mobile: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_mobile"))
    is_monitor: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_monitor"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    datetime_first: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="datetime_first", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    datetime_last: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="datetime_last", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    license: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="license"))
    sensor_count: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_count"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Location':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        if 'location_id' in data and isinstance(data['location_id'], str):
            data['location_id'] = int(data['location_id'])
        if 'owner_id' in data and isinstance(data['owner_id'], str):
            data['owner_id'] = int(data['owner_id'])
        if 'provider_id' in data and isinstance(data['provider_id'], str):
            data['provider_id'] = int(data['provider_id'])
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
        if 'owner_id' in asdict_result and asdict_result['owner_id'] is not None:
            asdict_result['owner_id'] = str(asdict_result['owner_id'])
        if 'provider_id' in asdict_result and asdict_result['provider_id'] is not None:
            asdict_result['provider_id'] = str(asdict_result['provider_id'])
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Location']:
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
                return Location.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Location':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            location_id=int(15),
            name='koqrxbhwzjjwiakrizkt',
            locality='cwpnlalrhgplodmjnyvf',
            timezone='kxcrlydygngyiijlvtvs',
            country_iso='xptebqjxrhrekhfbrcee',
            country_name='voocgfhyibgscpomykth',
            owner_id=int(81),
            owner_name='xlwtoyysrzbwohqnakqn',
            provider_id=int(59),
            provider_name='zzcddaqwnqtcjnrrjajd',
            is_mobile=True,
            is_monitor=False,
            latitude=float(22.564077837523467),
            longitude=float(74.70415498878317),
            datetime_first=datetime.datetime.now(datetime.timezone.utc),
            datetime_last=datetime.datetime.now(datetime.timezone.utc),
            license='qdsqfnbywrobqxgpnmzn',
            sensor_count=int(67)
        )