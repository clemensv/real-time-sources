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
from aisstream_mqtt_producer_data.msgtypeenum import MsgTypeenum


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PositionReport:
    """
    Position report (Type 1/2/3/4/9/18/19/27) projected onto the UNS axes.
    
    Attributes:
        mmsi (str)
        flag (str)
        ship_type (str)
        geohash5 (str)
        msg_type (MsgTypeenum)
        user_id (int)
        latitude (float)
        longitude (float)
        sog (typing.Optional[float])
        cog (typing.Optional[float])
        true_heading (typing.Optional[int])
        navigational_status (typing.Optional[int])
        rate_of_turn (typing.Optional[int])
        position_accuracy (typing.Optional[bool])
        timestamp (typing.Optional[int])
        raim (typing.Optional[bool])
        message_id (int)
    """
    
    
    mmsi: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmsi"))
    flag: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="flag"))
    ship_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ship_type"))
    geohash5: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geohash5"))
    msg_type: MsgTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="msg_type"))
    user_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="user_id"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    sog: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sog"))
    cog: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cog"))
    true_heading: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="true_heading"))
    navigational_status: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="navigational_status"))
    rate_of_turn: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rate_of_turn"))
    position_accuracy: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="position_accuracy"))
    timestamp: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    raim: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="raim"))
    message_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="message_id"))

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
            mmsi='uudyoizfzjwuullooakn',
            flag='vndpbmqftybthapayvqe',
            ship_type='hyulboedtjbgryjzapxt',
            geohash5='dycltjatmqxrakfzimhk',
            msg_type=MsgTypeenum.position_report,
            user_id=int(60),
            latitude=float(38.208578709108224),
            longitude=float(3.8532608893931064),
            sog=float(80.56243265872253),
            cog=float(67.98247708819484),
            true_heading=int(15),
            navigational_status=int(33),
            rate_of_turn=int(27),
            position_accuracy=False,
            timestamp=int(100),
            raim=True,
            message_id=int(86)
        )