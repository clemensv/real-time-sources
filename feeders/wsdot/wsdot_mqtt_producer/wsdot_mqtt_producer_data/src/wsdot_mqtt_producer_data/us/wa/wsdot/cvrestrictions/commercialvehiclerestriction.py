""" CommercialVehicleRestriction dataclass. """

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
class CommercialVehicleRestriction:
    """
    A commercial vehicle restriction on a Washington State highway bridge or road segment. Restrictions limit vehicle weight, height, length, or width.
    
    Attributes:
        state_route_id (str)
        bridge_number (str)
        bridge_name (typing.Optional[str])
        location_name (typing.Optional[str])
        location_description (typing.Optional[str])
        latitude (float)
        longitude (float)
        state (typing.Optional[str])
        restriction_type (typing.Optional[str])
        vehicle_type (typing.Optional[str])
        restriction_weight_in_pounds (typing.Optional[int])
        maximum_gross_vehicle_weight_in_pounds (typing.Optional[int])
        restriction_height_in_inches (typing.Optional[int])
        restriction_width_in_inches (typing.Optional[int])
        restriction_length_in_inches (typing.Optional[int])
        is_permanent_restriction (bool)
        is_warning (bool)
        is_detour_available (bool)
        is_exceptions_allowed (bool)
        restriction_comment (typing.Optional[str])
        date_posted (typing.Optional[str])
        date_effective (typing.Optional[str])
        date_expires (typing.Optional[str])
    """
    
    
    state_route_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_route_id"))
    bridge_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bridge_number"))
    bridge_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bridge_name"))
    location_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_name"))
    location_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_description"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    restriction_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_type"))
    vehicle_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_type"))
    restriction_weight_in_pounds: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_weight_in_pounds"))
    maximum_gross_vehicle_weight_in_pounds: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="maximum_gross_vehicle_weight_in_pounds"))
    restriction_height_in_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_height_in_inches"))
    restriction_width_in_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_width_in_inches"))
    restriction_length_in_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_length_in_inches"))
    is_permanent_restriction: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_permanent_restriction"))
    is_warning: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_warning"))
    is_detour_available: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_detour_available"))
    is_exceptions_allowed: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_exceptions_allowed"))
    restriction_comment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_comment"))
    date_posted: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_posted"))
    date_effective: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_effective"))
    date_expires: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_expires"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'CommercialVehicleRestriction':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['CommercialVehicleRestriction']:
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
                return CommercialVehicleRestriction.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'CommercialVehicleRestriction':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            state_route_id='zudqjrsapvqxyrpsypmz',
            bridge_number='iofeneitilfjqhbpigio',
            bridge_name='faqyvbsenqcdapudduqp',
            location_name='cxkisxmkekouhrvmrizi',
            location_description='vdtvtgfejwjvrwbqoxlv',
            latitude=float(93.02126238074852),
            longitude=float(93.61310825581242),
            state='jpqczpdlgchanhmciagr',
            restriction_type='kbwtavgnbnuhlylxfhzh',
            vehicle_type='xfjkxnchtttxycxhroby',
            restriction_weight_in_pounds=int(15),
            maximum_gross_vehicle_weight_in_pounds=int(27),
            restriction_height_in_inches=int(73),
            restriction_width_in_inches=int(36),
            restriction_length_in_inches=int(60),
            is_permanent_restriction=True,
            is_warning=True,
            is_detour_available=True,
            is_exceptions_allowed=False,
            restriction_comment='lalnjrgyjzodztuigulk',
            date_posted='knfulgwmyuidhlglqrlo',
            date_effective='wzrieibqwzotovkijrzk',
            date_expires='akoxvvqyvouvrrjvnhsg'
        )