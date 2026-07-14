""" StationStatus dataclass. """

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
class StationStatus:
    """
    Near-real-time availability record for one Taiwan YouBike 2.0 docking station, from the YouBike public station feed `https://apis.youbike.com.tw/json/station-yb2.json`. Reports the current count of rentable bikes (with the per-generation breakdown), empty docks available for returns, out-of-service docks, the discrete availability gauge level, the station service status, and the upstream data-update timestamps. The upstream feed refreshes approximately every minute.
    
    Attributes:
        station_id (str)
        num_bikes_available (int)
        num_bikes_yb1 (typing.Optional[int])
        num_bikes_yb2 (typing.Optional[int])
        num_ebikes_available (typing.Optional[int])
        num_empty_docks (int)
        num_forbidden_docks (typing.Optional[int])
        availability_level (typing.Optional[int])
        service_status (int)
        updated_at (datetime.datetime)
        snapshot_time (typing.Optional[datetime.datetime])
    """
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    num_bikes_available: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="num_bikes_available"))
    num_bikes_yb1: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="num_bikes_yb1"))
    num_bikes_yb2: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="num_bikes_yb2"))
    num_ebikes_available: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="num_ebikes_available"))
    num_empty_docks: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="num_empty_docks"))
    num_forbidden_docks: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="num_forbidden_docks"))
    availability_level: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="availability_level"))
    service_status: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="service_status"))
    updated_at: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated_at", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    snapshot_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snapshot_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'StationStatus':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['StationStatus']:
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
                return StationStatus.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'StationStatus':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='mzctamjszzyqdotnupjm',
            num_bikes_available=int(26),
            num_bikes_yb1=int(42),
            num_bikes_yb2=int(60),
            num_ebikes_available=int(40),
            num_empty_docks=int(55),
            num_forbidden_docks=int(21),
            availability_level=int(45),
            service_status=int(94),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            snapshot_time=datetime.datetime.now(datetime.timezone.utc)
        )