""" ExtendedClassBPositionReport dataclass. """

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
from aisstream_mqtt_producer_data.dimension import Dimension


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ExtendedClassBPositionReport:
    """
    A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.
    
    Attributes:
        MessageID (int)
        RepeatIndicator (typing.Optional[int])
        UserID (int)
        Valid (bool)
        Spare1 (typing.Optional[int])
        Sog (typing.Optional[float])
        PositionAccuracy (typing.Optional[bool])
        Longitude (float)
        Latitude (float)
        Cog (typing.Optional[float])
        TrueHeading (typing.Optional[int])
        Timestamp (typing.Optional[int])
        Spare2 (typing.Optional[int])
        Name (typing.Optional[str])
        Type (typing.Optional[int])
        Dimension (typing.Optional[Dimension])
        FixType (typing.Optional[int])
        Raim (typing.Optional[bool])
        Dte (typing.Optional[bool])
        AssignedMode (typing.Optional[bool])
        Spare3 (typing.Optional[int])
    """
    
    
    MessageID: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="MessageID"))
    RepeatIndicator: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="RepeatIndicator"))
    UserID: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="UserID"))
    Valid: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Valid"))
    Spare1: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Spare1"))
    Sog: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Sog"))
    PositionAccuracy: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="PositionAccuracy"))
    Longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Longitude"))
    Latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Latitude"))
    Cog: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Cog"))
    TrueHeading: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="TrueHeading"))
    Timestamp: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Timestamp"))
    Spare2: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Spare2"))
    Name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Name"))
    Type: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Type"))
    Dimension: typing.Optional[Dimension]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Dimension"))
    FixType: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="FixType"))
    Raim: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Raim"))
    Dte: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Dte"))
    AssignedMode: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="AssignedMode"))
    Spare3: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Spare3"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'ExtendedClassBPositionReport':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['ExtendedClassBPositionReport']:
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
                return ExtendedClassBPositionReport.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'ExtendedClassBPositionReport':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            MessageID=int(85),
            RepeatIndicator=int(8),
            UserID=int(50),
            Valid=True,
            Spare1=int(37),
            Sog=float(13.568940028754906),
            PositionAccuracy=True,
            Longitude=float(65.94063111158417),
            Latitude=float(49.275624356774685),
            Cog=float(79.84376243914036),
            TrueHeading=int(22),
            Timestamp=int(64),
            Spare2=int(53),
            Name='meugrubchywefspxgdqv',
            Type=int(59),
            Dimension=None,
            FixType=int(12),
            Raim=False,
            Dte=True,
            AssignedMode=True,
            Spare3=int(79)
        )