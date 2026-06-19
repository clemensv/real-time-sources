""" Arrival dataclass. """

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
from irail_amqp_producer_data.be.irail.occupancyenum import OccupancyEnum


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Arrival:
    """
    A single scheduled arrival at a Belgian railway station with real-time status. Represents a train service reaching the station at a scheduled time, possibly with a delay. The arrival is identified by the combination of station, date, and vehicle identifier encoded in the connection URI.
    
    Attributes:
        origin_station_id (str)
        origin_name (str)
        scheduled_time (str)
        delay_seconds (int)
        is_canceled (bool)
        has_arrived (bool)
        is_extra_stop (bool)
        vehicle_id (str)
        vehicle_short_name (str)
        vehicle_type (str)
        vehicle_number (str)
        platform (typing.Optional[str])
        is_normal_platform (bool)
        occupancy (OccupancyEnum)
        connection_uri (str)
    """
    
    
    origin_station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_station_id"))
    origin_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_name"))
    scheduled_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="scheduled_time"))
    delay_seconds: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay_seconds"))
    is_canceled: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_canceled"))
    has_arrived: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="has_arrived"))
    is_extra_stop: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_extra_stop"))
    vehicle_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_id"))
    vehicle_short_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_short_name"))
    vehicle_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_type"))
    vehicle_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_number"))
    platform: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="platform"))
    is_normal_platform: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_normal_platform"))
    occupancy: OccupancyEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="occupancy"))
    connection_uri: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connection_uri"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Arrival':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Arrival']:
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
                return Arrival.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Arrival':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            origin_station_id='wwsydcqrnquieqdemuzg',
            origin_name='kngamzwgxpjsqfnncjje',
            scheduled_time='iblpkdrhzhjfplufzqps',
            delay_seconds=int(18),
            is_canceled=True,
            has_arrived=False,
            is_extra_stop=True,
            vehicle_id='elealvpfrcyfnuoodzzc',
            vehicle_short_name='nvmefccbpxozxfgpybvy',
            vehicle_type='zdvqvlutgukgxhagiipn',
            vehicle_number='trcwxyhakihwgddbmjie',
            platform='jrsuqrdjitlikvrrmync',
            is_normal_platform=False,
            occupancy=OccupancyEnum.low,
            connection_uri='pqpzisknuruoddwiuyrq'
        )