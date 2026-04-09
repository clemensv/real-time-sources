""" MagneticFieldReading dataclass. """

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
import datetime as _datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class MagneticFieldReading:
    """
    One-minute resolution geomagnetic field variation reading from a USGS observatory.

    Attributes:
        iaga_code (str)
        timestamp (_datetime.datetime)
        h (typing.Optional[float])
        d (typing.Optional[float])
        z (typing.Optional[float])
        f (typing.Optional[float])
    """


    iaga_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="iaga_code"))
    timestamp: _datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="h"))
    d: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="d"))
    z: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="z"))
    f: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="f"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'MagneticFieldReading':
        """Converts a dictionary to a dataclass instance."""
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """Converts the dataclass to a dictionary."""
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        return asdict_result

    def _dict_resolver(self, data):
        """Helps resolving the Enum values to their actual values and fixes the key names."""
        def _resolve_enum(v):
            if isinstance(v, enum.Enum):
                return v.value
            if isinstance(v, _datetime.datetime):
                return v.isoformat()
            return v
        def _fix_key(k):
            return k[:-1] if k.endswith('_') else k
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data)}

    def to_byte_array(self, content_type_string: str) -> bytes:
        """Converts the dataclass to a byte array based on the content type string."""
        content_type = content_type_string.split(';')[0].strip()
        result = None
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            #pylint: disable=no-member
            result = json.dumps(self.to_serializer_dict())
            #pylint: enable=no-member
        if result is not None and content_type.endswith('+gzip'):
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['MagneticFieldReading']:
        """Converts the data to a dataclass based on the content type string."""
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
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return MagneticFieldReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'MagneticFieldReading':
        """Creates an instance of the dataclass with test values."""
        return cls(
            iaga_code='BOU',
            timestamp=_datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=_datetime.timezone.utc),
            h=float(20656.086),
            d=float(5.173),
            z=float(46726.692),
            f=float(51107.760)
        )
