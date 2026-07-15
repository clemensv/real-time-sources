""" Connection dataclass. """

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
class Connection:
    """
    One physical charging connection (EVSE connector) at the charging location, from an element of the upstream POI `Connections` array. Describes the connector standard, its charging level and current type, the electrical rating, the operational status, and how many identical connectors of this configuration the equipment provides.
    
    Attributes:
        connection_id (int)
        connection_type_id (typing.Optional[int])
        connection_type_title (typing.Optional[str])
        connection_type_formal_name (typing.Optional[str])
        reference (typing.Optional[str])
        status_type_id (typing.Optional[int])
        is_operational (typing.Optional[bool])
        level_id (typing.Optional[int])
        level_title (typing.Optional[str])
        is_fast_charge_capable (typing.Optional[bool])
        amps (typing.Optional[int])
        voltage (typing.Optional[int])
        power_kw (typing.Optional[float])
        current_type_id (typing.Optional[int])
        current_type_title (typing.Optional[str])
        quantity (typing.Optional[int])
        comments (typing.Optional[str])
    """
    
    
    connection_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connection_id"))
    connection_type_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connection_type_id"))
    connection_type_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connection_type_title"))
    connection_type_formal_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connection_type_formal_name"))
    reference: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reference"))
    status_type_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status_type_id"))
    is_operational: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_operational"))
    level_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="level_id"))
    level_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="level_title"))
    is_fast_charge_capable: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_fast_charge_capable"))
    amps: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="amps"))
    voltage: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="voltage"))
    power_kw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="power_kw"))
    current_type_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_type_id"))
    current_type_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_type_title"))
    quantity: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="quantity"))
    comments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="comments"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Connection':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Connection']:
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
                return Connection.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Connection':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            connection_id=int(36),
            connection_type_id=int(40),
            connection_type_title='vipvqmnoizezxhbmrvop',
            connection_type_formal_name='uktjckwgbenuheqjmwao',
            reference='yrbirkvsdwligfudrpue',
            status_type_id=int(7),
            is_operational=False,
            level_id=int(77),
            level_title='bsdypkrbwlcbcnnrflwt',
            is_fast_charge_capable=False,
            amps=int(68),
            voltage=int(98),
            power_kw=float(47.42408733868005),
            current_type_id=int(15),
            current_type_title='atmvczknckaycpqcdaqw',
            quantity=int(68),
            comments='qkpzewavogwawvnktlxx'
        )