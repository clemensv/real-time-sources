""" MapChange dataclass. """

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
class MapChange:
    """
    An individual element change from the OpenStreetMap minutely replication diff feed. Each event describes a create, modify, or delete of a node, way, or relation. Latitude and longitude are present only for node elements. Tags are JSON-encoded because xreg does not support map types natively. The geohash5 axis is the 5-character base32 geohash of the element's representative coordinate; relations without a derivable bounding box receive the sentinel 'nogeo' so they still publish onto the UNS tree.
    
    Attributes:
        change_type (str)
        element_type (str)
        element_id (int)
        geohash5 (str)
        version (int)
        timestamp (datetime.datetime)
        changeset_id (int)
        user_name (typing.Optional[str])
        user_id (typing.Optional[int])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        tags (str)
        sequence_number (int)
    """
    
    
    change_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="change_type"))
    element_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="element_type"))
    element_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="element_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    geohash5: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geohash5"))
    version: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    changeset_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="changeset_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    user_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="user_name"))
    user_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="user_id", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    tags: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tags"))
    sequence_number: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sequence_number", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'MapChange':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        if 'element_id' in data and isinstance(data['element_id'], str):
            data['element_id'] = int(data['element_id'])
        if 'changeset_id' in data and isinstance(data['changeset_id'], str):
            data['changeset_id'] = int(data['changeset_id'])
        if 'user_id' in data and isinstance(data['user_id'], str):
            data['user_id'] = int(data['user_id'])
        if 'sequence_number' in data and isinstance(data['sequence_number'], str):
            data['sequence_number'] = int(data['sequence_number'])
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        if 'element_id' in asdict_result and asdict_result['element_id'] is not None:
            asdict_result['element_id'] = str(asdict_result['element_id'])
        if 'changeset_id' in asdict_result and asdict_result['changeset_id'] is not None:
            asdict_result['changeset_id'] = str(asdict_result['changeset_id'])
        if 'user_id' in asdict_result and asdict_result['user_id'] is not None:
            asdict_result['user_id'] = str(asdict_result['user_id'])
        if 'sequence_number' in asdict_result and asdict_result['sequence_number'] is not None:
            asdict_result['sequence_number'] = str(asdict_result['sequence_number'])
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['MapChange']:
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
                return MapChange.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'MapChange':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            change_type='ywourxyvprajixnhbvxg',
            element_type='dcsfxptysxljtnenbwhc',
            element_id=int(95),
            geohash5='tpyjxgmfiukzmdbjzahw',
            version=int(85),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            changeset_id=int(83),
            user_name='dezvyvddzfzfpburndmf',
            user_id=int(60),
            latitude=float(77.00236233783212),
            longitude=float(97.77545182880151),
            tags='imkjmyuxqawcawcxhdrz',
            sequence_number=int(46)
        )