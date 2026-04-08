""" XrayFlare dataclass. """

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
class XrayFlare:
    """
    Individual solar X-ray flare event detected by the GOES primary satellite XRS instrument, as reported by the SWPC goes/primary/xray-flares-7-day endpoint. Each record represents a discrete flare event with onset, peak, and end times plus X-ray classifications on the standard A/B/C/M/X logarithmic scale. The flare classification is based on peak 0.1-0.8 nm X-ray flux: C-class (1e-6 W/m²), M-class (1e-5), X-class (1e-4).
    
    Attributes:
        time_tag (str)
        begin_time (str)
        begin_class (typing.Optional[str])
        max_time (typing.Optional[str])
        max_class (typing.Optional[str])
        max_xrlong (typing.Optional[float])
        max_ratio (typing.Optional[float])
        max_ratio_time (typing.Optional[str])
        current_int_xrlong (typing.Optional[float])
        end_time (typing.Optional[str])
        end_class (typing.Optional[str])
        satellite (int)
    """
    
    
    time_tag: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_tag"))
    begin_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="begin_time"))
    begin_class: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="begin_class"))
    max_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_time"))
    max_class: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_class"))
    max_xrlong: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_xrlong"))
    max_ratio: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_ratio"))
    max_ratio_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_ratio_time"))
    current_int_xrlong: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_int_xrlong"))
    end_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_time"))
    end_class: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_class"))
    satellite: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="satellite"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'XrayFlare':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['XrayFlare']:
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
                return XrayFlare.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'XrayFlare':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            time_tag='pflynkluyuctxtfiakhk',
            begin_time='xnbrnsoloqyqzsxfczvd',
            begin_class='bzurjomhwoateyhougtw',
            max_time='scylairhvxdqmyvilwpe',
            max_class='akkkaugdaudywkopoupp',
            max_xrlong=float(22.144160546759984),
            max_ratio=float(66.57445055449168),
            max_ratio_time='oihcwmgrpmfmpdxhcaxt',
            current_int_xrlong=float(71.09975348967642),
            end_time='pdmovackguvevtuibryq',
            end_class='slcygqcxjrtalcwveyud',
            satellite=int(19)
        )