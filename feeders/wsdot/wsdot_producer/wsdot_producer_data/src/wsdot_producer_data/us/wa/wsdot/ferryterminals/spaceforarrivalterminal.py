""" SpaceForArrivalTerminal dataclass. """

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
class SpaceForArrivalTerminal:
    """
    Vehicle space availability for one arrival terminal served by a sailing.
    
    Attributes:
        terminal_id (typing.Optional[int])
        terminal_name (typing.Optional[str])
        vessel_id (typing.Optional[int])
        vessel_name (typing.Optional[str])
        display_reservable_space (bool)
        reservable_space_count (typing.Optional[int])
        reservable_space_hex_color (typing.Optional[str])
        display_drive_up_space (bool)
        drive_up_space_count (typing.Optional[int])
        drive_up_space_hex_color (typing.Optional[str])
        max_space_count (typing.Optional[int])
        arrival_terminal_ids (typing.List[int])
    """
    
    
    terminal_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="terminal_id"))
    terminal_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="terminal_name"))
    vessel_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vessel_id"))
    vessel_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vessel_name"))
    display_reservable_space: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="display_reservable_space"))
    reservable_space_count: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reservable_space_count"))
    reservable_space_hex_color: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reservable_space_hex_color"))
    display_drive_up_space: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="display_drive_up_space"))
    drive_up_space_count: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drive_up_space_count"))
    drive_up_space_hex_color: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drive_up_space_hex_color"))
    max_space_count: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_space_count"))
    arrival_terminal_ids: typing.List[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrival_terminal_ids"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SpaceForArrivalTerminal':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SpaceForArrivalTerminal']:
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
                return SpaceForArrivalTerminal.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SpaceForArrivalTerminal':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            terminal_id=int(94),
            terminal_name='fkwnnrsguxxtyxpjtjir',
            vessel_id=int(24),
            vessel_name='sahkalqumfmfjiqedlta',
            display_reservable_space=False,
            reservable_space_count=int(25),
            reservable_space_hex_color='gymryuodqdaonvvmtfcy',
            display_drive_up_space=True,
            drive_up_space_count=int(20),
            drive_up_space_hex_color='mjjosyebqpomktzneepc',
            max_space_count=int(59),
            arrival_terminal_ids=[int(16), int(69), int(33)]
        )