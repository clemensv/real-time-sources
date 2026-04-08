""" Timeseries dataclass. """

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
from typing import Any


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Timeseries:
    """
    Reference data for a single IRCELINE timeseries from GET /timeseries or GET /timeseries/{id}?expanded=true. Each timeseries combines a stable numeric timeseries identifier with a station, a phenomenon/category pair, the published unit of measurement, and optional statusIntervals that describe threshold bands used by IRCELINE for display and air-quality interpretation.
    
    Attributes:
        timeseries_id (str)
        label (str)
        uom (str)
        station_id (str)
        station_label (str)
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        phenomenon_id (typing.Optional[str])
        phenomenon_label (typing.Optional[str])
        category_id (typing.Optional[str])
        category_label (typing.Optional[str])
        status_intervals (typing.Optional[Any])
    """
    
    
    timeseries_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timeseries_id"))
    label: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="label"))
    uom: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="uom"))
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_label: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_label"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    phenomenon_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="phenomenon_id"))
    phenomenon_label: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="phenomenon_label"))
    category_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category_id"))
    category_label: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category_label"))
    status_intervals: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status_intervals"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Timeseries':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Timeseries']:
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
                return Timeseries.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Timeseries':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            timeseries_id='rhgtcmnewkdoerytfxcy',
            label='gmvchtbwodxtxwhuadim',
            uom='utyhhmdxkxqdknckjryr',
            station_id='uhzezmstmnixlfoddvpm',
            station_label='jzdomalvtjoupdxhnytl',
            latitude=float(11.617483197746193),
            longitude=float(44.251306491297896),
            phenomenon_id='aiptebhrivqspggptbyi',
            phenomenon_label='sdwiructihiiqpojdtum',
            category_id='cvfdvkjkokpxsyshqkln',
            category_label='ynszagyuxhjqtcxxtuqs',
            status_intervals=None
        )