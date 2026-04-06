""" EvseStatus dataclass. """

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
from ndl_netherlands_producer_data.connectorsummary import ConnectorSummary
from typing import Any
from ndl_netherlands_producer_data.statusenum import StatusEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class EvseStatus:
    """
    Telemetry event for an EVSE status change from the NDL. Contains the EVSE identification, current status, and a summary of its connectors.
    
    Attributes:
        location_id (str)
        evse_uid (str)
        evse_id (typing.Optional[str])
        status (StatusEnum)
        capabilities (typing.Optional[Any])
        floor_level (typing.Optional[str])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        physical_reference (typing.Optional[str])
        parking_restrictions (typing.Optional[Any])
        connectors (typing.List[ConnectorSummary])
        last_updated (datetime.datetime)
    """
    
    
    location_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_id"))
    evse_uid: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="evse_uid"))
    evse_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="evse_id"))
    status: StatusEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    capabilities: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="capabilities"))
    floor_level: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="floor_level"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    physical_reference: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="physical_reference"))
    parking_restrictions: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parking_restrictions"))
    connectors: typing.List[ConnectorSummary]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connectors"))
    last_updated: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="last_updated", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'EvseStatus':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['EvseStatus']:
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
                return EvseStatus.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'EvseStatus':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            location_id='vodvjkkearcylptcvvmc',
            evse_uid='jybkenamktjyuulxuwiv',
            evse_id='fyuwwqwkcxxehbkbkobe',
            status=StatusEnum.AVAILABLE,
            capabilities=None,
            floor_level='cokhiidvmxhfxdcprhbh',
            latitude=float(83.89513744706177),
            longitude=float(83.69309957756292),
            physical_reference='wpfinqhnaollthafbqyj',
            parking_restrictions=None,
            connectors=[None, None, None],
            last_updated=datetime.datetime.now(datetime.timezone.utc)
        )