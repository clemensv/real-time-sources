""" BridgeClearance dataclass. """

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
class BridgeClearance:
    """
    Reference catalog record of the surveyed vertical clearance of a structure crossing a Washington State highway, used for commercial vehicle routing. Largely static; refreshed periodically.
    
    Attributes:
        crossing_location_id (str)
        bridge_number (typing.Optional[str])
        state_route_id (typing.Optional[str])
        state_structure_id (typing.Optional[str])
        crossing_description (typing.Optional[str])
        inventory_direction (typing.Optional[str])
        srmp (typing.Optional[float])
        srmp_ahead_back_indicator (typing.Optional[str])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        vertical_clearance_maximum_inches (typing.Optional[int])
        vertical_clearance_maximum_feet_inch (typing.Optional[str])
        vertical_clearance_minimum_inches (typing.Optional[int])
        vertical_clearance_minimum_feet_inch (typing.Optional[str])
        control_entity_guid (typing.Optional[str])
        crossing_record_guid (typing.Optional[str])
        location_guid (typing.Optional[str])
        route_date (typing.Optional[str])
        api_last_update (typing.Optional[str])
    """
    
    
    crossing_location_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="crossing_location_id"))
    bridge_number: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bridge_number"))
    state_route_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_route_id"))
    state_structure_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_structure_id"))
    crossing_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="crossing_description"))
    inventory_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="inventory_direction"))
    srmp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="srmp"))
    srmp_ahead_back_indicator: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="srmp_ahead_back_indicator"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    vertical_clearance_maximum_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vertical_clearance_maximum_inches"))
    vertical_clearance_maximum_feet_inch: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vertical_clearance_maximum_feet_inch"))
    vertical_clearance_minimum_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vertical_clearance_minimum_inches"))
    vertical_clearance_minimum_feet_inch: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vertical_clearance_minimum_feet_inch"))
    control_entity_guid: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="control_entity_guid"))
    crossing_record_guid: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="crossing_record_guid"))
    location_guid: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_guid"))
    route_date: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_date"))
    api_last_update: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="api_last_update"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'BridgeClearance':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['BridgeClearance']:
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
                return BridgeClearance.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'BridgeClearance':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            crossing_location_id='iwwbwhqqmswnndidssnp',
            bridge_number='gdzrpmxsxvqibukbgvjl',
            state_route_id='jphewjhprrcyhsdejahv',
            state_structure_id='nnlbnsuulqoxkxlglcws',
            crossing_description='roxckozotqiomxlzfnpc',
            inventory_direction='wvypligqaofrrmkffecm',
            srmp=float(33.31796998851721),
            srmp_ahead_back_indicator='lpizgqvyckwevwydyzvy',
            latitude=float(75.74080144128885),
            longitude=float(1.7943195842884174),
            vertical_clearance_maximum_inches=int(62),
            vertical_clearance_maximum_feet_inch='ceiczypamblmvwpkubzw',
            vertical_clearance_minimum_inches=int(64),
            vertical_clearance_minimum_feet_inch='ueqqkqxrqwhxzwqhtrax',
            control_entity_guid='zqmvrguxwolmnxomurqm',
            crossing_record_guid='nwwenhqupurgdwjodbac',
            location_guid='wybmenugtypzntksftjf',
            route_date='gkkhsagyfgspuixnepvp',
            api_last_update='zjlspsezheqotojeuxxz'
        )