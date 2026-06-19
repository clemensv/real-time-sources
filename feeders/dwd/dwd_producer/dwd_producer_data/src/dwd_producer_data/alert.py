""" Alert dataclass. """

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
class Alert:
    """
    A weather or environmental alert from Germany's Deutscher Wetterdienst (DWD). It fires when the upstream source publishes or updates a warning that may affect the covered area.
    
    Attributes:
        identifier (str)
        sender (str)
        sent (str)
        status (typing.Optional[str])
        msg_type (typing.Optional[str])
        severity (str)
        urgency (typing.Optional[str])
        certainty (typing.Optional[str])
        event (str)
        headline (typing.Optional[str])
        description (typing.Optional[str])
        effective (typing.Optional[str])
        onset (typing.Optional[str])
        expires (typing.Optional[str])
        area_desc (typing.Optional[str])
        geocodes (typing.Optional[str])
        state (typing.Optional[str])
    """
    
    
    identifier: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="identifier"))
    sender: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender"))
    sent: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sent"))
    status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    msg_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="msg_type"))
    severity: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    urgency: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="urgency"))
    certainty: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="certainty"))
    event: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event"))
    headline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headline"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    effective: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="effective"))
    onset: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onset"))
    expires: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expires"))
    area_desc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_desc"))
    geocodes: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geocodes"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Alert':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Alert']:
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
                return Alert.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Alert':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            identifier='tdexoflvmzmikrqbaoem',
            sender='jsnngdyefkaxtxinofcp',
            sent='jyjabiucqlkaulvbythk',
            status='kkcsblmdtbiltwjdvyen',
            msg_type='kebpkoyfhyurjeaxwxrh',
            severity='pnqadsdqostxihoxrclq',
            urgency='ykwbwdeoxyombrdidogd',
            certainty='jvpczkbeazprtrlamrbk',
            event='yhvaqfolrxstskxoymxi',
            headline='qhvjgouwnwuiezcvyadd',
            description='ngyznslufaynvakwprdw',
            effective='qzenblynhpuuducyevwm',
            onset='mvcwkxwcyqjucjtvtney',
            expires='btpvogdteieyqnbmpspw',
            area_desc='pytaunfhlnhbibufjlwo',
            geocodes='snjlomyctckjqidzthio',
            state='snxdpaoqdsnqkpilcftw'
        )