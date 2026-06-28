""" PositionReport dataclass. """

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
class PositionReport:
    """
    Class A Automatic Identification System (AIS) position report (ITU-R M.1371 messages 1, 2 and 3) as decoded and relayed by the aisstream.io firehose. It reports a Class A vessel's instantaneous navigational situation - position, course, speed, heading, rate of turn and navigational status - together with the TDMA communication state used for slot management.
    
    Attributes:
        MessageID (int)
        RepeatIndicator (typing.Optional[int])
        UserID (int)
        Valid (bool)
        NavigationalStatus (typing.Optional[int])
        RateOfTurn (typing.Optional[int])
        Sog (typing.Optional[float])
        PositionAccuracy (typing.Optional[bool])
        Longitude (float)
        Latitude (float)
        Cog (typing.Optional[float])
        TrueHeading (typing.Optional[int])
        Timestamp (typing.Optional[int])
        SpecialManoeuvreIndicator (typing.Optional[int])
        Spare (typing.Optional[int])
        Raim (typing.Optional[bool])
        CommunicationState (typing.Optional[int])
    """
    
    
    MessageID: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="MessageID"))
    RepeatIndicator: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="RepeatIndicator"))
    UserID: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="UserID"))
    Valid: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Valid"))
    NavigationalStatus: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="NavigationalStatus"))
    RateOfTurn: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="RateOfTurn"))
    Sog: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Sog"))
    PositionAccuracy: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="PositionAccuracy"))
    Longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Longitude"))
    Latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Latitude"))
    Cog: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Cog"))
    TrueHeading: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="TrueHeading"))
    Timestamp: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Timestamp"))
    SpecialManoeuvreIndicator: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="SpecialManoeuvreIndicator"))
    Spare: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Spare"))
    Raim: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="Raim"))
    CommunicationState: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="CommunicationState"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PositionReport':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PositionReport']:
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
                return PositionReport.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'PositionReport':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            MessageID=int(49),
            RepeatIndicator=int(64),
            UserID=int(61),
            Valid=False,
            NavigationalStatus=int(50),
            RateOfTurn=int(58),
            Sog=float(7.265722223218307),
            PositionAccuracy=True,
            Longitude=float(81.65627924308613),
            Latitude=float(59.628229567783066),
            Cog=float(2.8850614410830477),
            TrueHeading=int(7),
            Timestamp=int(38),
            SpecialManoeuvreIndicator=int(15),
            Spare=int(29),
            Raim=True,
            CommunicationState=int(1)
        )