""" VehiclePosition dataclass. """

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
class VehiclePosition:
    """
    Normalized payload for one BODS SIRI 2.0 VehicleActivity element from the Department for Transport Bus Open Data Service AVL bulk archive. The bridge emits one event per monitored vehicle activity in each poll cycle, keyed by the stable operator code and vehicle fleet reference.
    
    Attributes:
        operator_ref (str)
        vehicle_ref (str)
        line_ref (typing.Optional[str])
        direction_ref (typing.Optional[str])
        published_line_name (typing.Optional[str])
        origin_ref (typing.Optional[str])
        origin_name (typing.Optional[str])
        destination_ref (typing.Optional[str])
        destination_name (typing.Optional[str])
        longitude (typing.Optional[float])
        latitude (typing.Optional[float])
        bearing (typing.Optional[int])
        recorded_at_time (datetime.datetime)
        valid_until_time (typing.Optional[datetime.datetime])
        block_ref (typing.Optional[str])
        vehicle_journey_ref (typing.Optional[str])
        origin_aimed_departure_time (typing.Optional[datetime.datetime])
        data_frame_ref (typing.Optional[str])
        dated_vehicle_journey_ref (typing.Optional[str])
        item_identifier (str)
    """
    
    
    operator_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_ref"))
    vehicle_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_ref"))
    line_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="line_ref"))
    direction_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction_ref"))
    published_line_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published_line_name"))
    origin_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_ref"))
    origin_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_name"))
    destination_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_ref"))
    destination_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_name"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    bearing: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bearing"))
    recorded_at_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="recorded_at_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    valid_until_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="valid_until_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    block_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="block_ref"))
    vehicle_journey_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_journey_ref"))
    origin_aimed_departure_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_aimed_departure_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    data_frame_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_frame_ref"))
    dated_vehicle_journey_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dated_vehicle_journey_ref"))
    item_identifier: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="item_identifier"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'VehiclePosition':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VehiclePosition']:
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
                return VehiclePosition.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'VehiclePosition':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            operator_ref='nohjylonxiverbtnkbci',
            vehicle_ref='owgwfhkgoxxbkmfxxwvl',
            line_ref='pmwzqkmvndvicmdvmozt',
            direction_ref='wfzxhvvkkobxevgtldkv',
            published_line_name='unosbxdkaehfzyugdsxh',
            origin_ref='angyyozjmtnmhqhbocmk',
            origin_name='sadfvfsyexjjsagccjpy',
            destination_ref='jjrzzwxyffpiiikymtwi',
            destination_name='hvveryxsvwlksvnqymkz',
            longitude=float(35.086710385056996),
            latitude=float(67.54757415106832),
            bearing=int(74),
            recorded_at_time=datetime.datetime.now(datetime.timezone.utc),
            valid_until_time=datetime.datetime.now(datetime.timezone.utc),
            block_ref='hofwoovaurzyqpdzrckb',
            vehicle_journey_ref='evxrwkhgmgztbsoaohum',
            origin_aimed_departure_time=datetime.datetime.now(datetime.timezone.utc),
            data_frame_ref='abgmlirnbxhkrlcekmgh',
            dated_vehicle_journey_ref='gugnwqznvykigmdtoqwb',
            item_identifier='jujyxzmaflfyhvzxgpzn'
        )