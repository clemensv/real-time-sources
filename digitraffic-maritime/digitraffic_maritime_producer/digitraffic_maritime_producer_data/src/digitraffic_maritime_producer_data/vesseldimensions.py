""" VesselDimensions dataclass. """

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
class VesselDimensions:
    """
    Tonnage and dimensional attributes for the vessel.
    
    Attributes:
        tonnage_certificate_issuer (typing.Optional[str])
        date_of_issue (typing.Optional[datetime.datetime])
        gross_tonnage (typing.Optional[int])
        net_tonnage (typing.Optional[int])
        dead_weight (typing.Optional[int])
        length (typing.Optional[float])
        overall_length (typing.Optional[float])
        height (typing.Optional[float])
        breadth (typing.Optional[float])
        draught (typing.Optional[float])
        max_speed (typing.Optional[float])
        engine_power (typing.Optional[str])
    """
    
    
    tonnage_certificate_issuer: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tonnage_certificate_issuer"))
    date_of_issue: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_of_issue", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    gross_tonnage: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gross_tonnage"))
    net_tonnage: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="net_tonnage"))
    dead_weight: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dead_weight"))
    length: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="length"))
    overall_length: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="overall_length"))
    height: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="height"))
    breadth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="breadth"))
    draught: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="draught"))
    max_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_speed"))
    engine_power: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="engine_power"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'VesselDimensions':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VesselDimensions']:
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
                return VesselDimensions.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'VesselDimensions':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            tonnage_certificate_issuer='nggszxxvddksknnrlzky',
            date_of_issue=datetime.datetime.now(datetime.timezone.utc),
            gross_tonnage=int(25),
            net_tonnage=int(6),
            dead_weight=int(87),
            length=float(86.24976867189982),
            overall_length=float(4.933377510902515),
            height=float(8.628623254213618),
            breadth=float(1.016119064432064),
            draught=float(49.09938407108487),
            max_speed=float(96.61775911284222),
            engine_power='rlbamlnocvomkvuokqsv'
        )