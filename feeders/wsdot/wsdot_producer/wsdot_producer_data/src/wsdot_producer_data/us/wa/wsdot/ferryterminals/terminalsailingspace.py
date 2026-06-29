""" TerminalSailingSpace dataclass. """

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
from wsdot_producer_data.us.wa.wsdot.ferryterminals.departingspace import DepartingSpace


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TerminalSailingSpace:
    """
    Real-time drive-up and reservable vehicle space availability for upcoming Washington State Ferries departures from a terminal, broken down by sailing and arrival terminal.
    
    Attributes:
        terminal_id (str)
        terminal_subject_id (typing.Optional[int])
        region_id (typing.Optional[int])
        terminal_name (typing.Optional[str])
        terminal_abbrev (typing.Optional[str])
        sort_seq (typing.Optional[int])
        departing_spaces (typing.List[DepartingSpace])
        is_no_fare_collected (typing.Optional[bool])
        no_fare_collected_msg (typing.Optional[str])
    """
    
    
    terminal_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="terminal_id"))
    terminal_subject_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="terminal_subject_id"))
    region_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region_id"))
    terminal_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="terminal_name"))
    terminal_abbrev: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="terminal_abbrev"))
    sort_seq: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sort_seq"))
    departing_spaces: typing.List[DepartingSpace]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departing_spaces"))
    is_no_fare_collected: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_no_fare_collected"))
    no_fare_collected_msg: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no_fare_collected_msg"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TerminalSailingSpace':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TerminalSailingSpace']:
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
                return TerminalSailingSpace.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'TerminalSailingSpace':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            terminal_id='hsdsdgccwccxqvpzamhw',
            terminal_subject_id=int(48),
            region_id=int(61),
            terminal_name='trmnvvjfiwdmdblmbgrm',
            terminal_abbrev='yvskcoqfogycfupaeegw',
            sort_seq=int(98),
            departing_spaces=[None, None, None, None, None],
            is_no_fare_collected=True,
            no_fare_collected_msg='masxhxsbdxpuvjtmtcpn'
        )