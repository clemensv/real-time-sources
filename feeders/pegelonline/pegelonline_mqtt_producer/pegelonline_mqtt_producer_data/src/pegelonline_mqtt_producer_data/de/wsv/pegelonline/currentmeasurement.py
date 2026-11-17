""" CurrentMeasurement dataclass. """

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
from marshmallow import fields, ValidationError
import json
from pegelonline_mqtt_producer_data.de.wsv.pegelonline.statemnwmhwenum import StateMnwMhwEnum
from pegelonline_mqtt_producer_data.de.wsv.pegelonline.statenswhswenum import StateNswHswEnum
from pegelonline_mqtt_producer_data.de.wsv.pegelonline.trendenum import TrendEnum
import datetime





def _normalize_iso_string(value: str) -> str:
    """ Normalizes an RFC 3339 string into a form datetime.fromisoformat accepts.

    A trailing 'Z' is rewritten to '+00:00' and fractional seconds are padded or
    truncated to exactly microsecond precision, because fromisoformat only
    accepts the 'Z' designator and arbitrary fraction lengths from Python 3.11
    onwards, and this package supports Python 3.10.

    A non-string value raises ValueError so that callers report it the same way
    they report a malformed string, rather than leaking an AttributeError.
    """
    if not isinstance(value, str):
        raise ValueError(f'expected an ISO 8601 string, got {type(value).__name__}')
    text = value[:-1] + '+00:00' if value.endswith(('Z', 'z')) else value
    dot = text.find('.')
    if dot != -1:
        end = dot + 1
        while end < len(text) and text[end].isdigit():
            end += 1
        digits = text[dot + 1:end]
        if digits and len(digits) != 6:
            text = text[:dot + 1] + digits[:6].ljust(6, '0') + text[end:]
    return text



def _parse_iso_datetime(value: str, field_name: str) -> datetime.datetime:
    """ Parses an ISO 8601 / RFC 3339 datetime string, raising ValueError if it is malformed. """
    try:
        return datetime.datetime.fromisoformat(_normalize_iso_string(value))
    except ValueError as error:
        raise ValueError(
            f"Invalid ISO 8601 datetime for field '{field_name}': {value!r}") from error





class _IsoDateTimeField(fields.DateTime):
    """ A marshmallow datetime field that shares the module's ISO datetime parser. """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        # datetime.date is accepted as well because marshmallow's own
        # DateTime(format='iso') serialized anything with an isoformat().
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return _parse_iso_datetime(value, self.data_key or attr or 'value')
        except ValueError as error:
            raise ValidationError(str(error)) from error








@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CurrentMeasurement:
    """
    Latest 15-minute water-level reading for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Carries only the W (water-level) timeseries; other timeseries (Q discharge, LT water temperature) are not emitted by this source.
    
    Attributes:
        station_id (str)
        timestamp (datetime.datetime)
        value (float)
        stateMnwMhw (typing.Optional[StateMnwMhwEnum])
        stateNswHsw (typing.Optional[StateNswHswEnum])
        trend (typing.Optional[TrendEnum])
    """
    
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda v: v.isoformat() if isinstance(v, datetime.datetime) else v, decoder=lambda v: _parse_iso_datetime(v, 'timestamp') if isinstance(v, str) else v, mm_field=_IsoDateTimeField(data_key='timestamp', required=True)))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    stateMnwMhw: typing.Optional[StateMnwMhwEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stateMnwMhw"))
    stateNswHsw: typing.Optional[StateNswHswEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stateNswHsw"))
    trend: typing.Optional[TrendEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trend"))


    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'CurrentMeasurement':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        data = dict(data)
        if 'timestamp' in data:
            data['timestamp'] = (lambda v: _parse_iso_datetime(v, 'timestamp') if isinstance(v, str) else v)(data['timestamp'])
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['CurrentMeasurement']:
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
                return CurrentMeasurement.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'CurrentMeasurement':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='trdpnvztspxsjalmwvws',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(34.870051443645714),
            stateMnwMhw=StateMnwMhwEnum.low,
            stateNswHsw=StateNswHswEnum.normal,
            trend=TrendEnum.VALUE_NEG_1
        )