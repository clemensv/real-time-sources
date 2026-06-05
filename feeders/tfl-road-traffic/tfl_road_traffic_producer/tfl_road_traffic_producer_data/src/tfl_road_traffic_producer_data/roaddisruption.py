""" RoadDisruption dataclass. """

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
from typing import Any
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RoadDisruption:
    """
    Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.
    
    Attributes:
        road_id (str)
        disruption_id (str)
        category (typing.Optional[str])
        sub_category (typing.Optional[str])
        severity (str)
        ordinal (typing.Optional[int])
        url (typing.Optional[str])
        point (typing.Optional[str])
        comments (typing.Optional[str])
        current_update (typing.Optional[str])
        current_update_datetime (typing.Optional[datetime.datetime])
        corridor_ids (typing.Optional[Any])
        start_datetime (typing.Optional[datetime.datetime])
        end_datetime (typing.Optional[datetime.datetime])
        last_modified_time (typing.Optional[datetime.datetime])
        level_of_interest (typing.Optional[str])
        location (typing.Optional[str])
        is_provisional (typing.Optional[bool])
        has_closures (typing.Optional[bool])
        streets (typing.Optional[Any])
        geography (typing.Optional[str])
        geometry (typing.Optional[str])
        status (typing.Optional[str])
        is_active (typing.Optional[bool])
    """
    
    
    road_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_id"))
    disruption_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="disruption_id"))
    category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    sub_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sub_category"))
    severity: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    ordinal: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ordinal"))
    url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    point: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="point"))
    comments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="comments"))
    current_update: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_update"))
    current_update_datetime: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_update_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    corridor_ids: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="corridor_ids"))
    start_datetime: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    end_datetime: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    last_modified_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="last_modified_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    level_of_interest: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="level_of_interest"))
    location: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location"))
    is_provisional: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_provisional"))
    has_closures: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="has_closures"))
    streets: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="streets"))
    geography: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geography"))
    geometry: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geometry"))
    status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    is_active: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_active"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'RoadDisruption':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['RoadDisruption']:
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
                return RoadDisruption.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'RoadDisruption':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            road_id='sajyldmvnsjykuxwkzls',
            disruption_id='uprybrrmsqfyobeavfgn',
            category='ldcnwidgiyzytoagloux',
            sub_category='ylgjnupitnhgthxmveqq',
            severity='cnrzidtsrssmjkulxbtm',
            ordinal=int(34),
            url='oejgryanvrogcmwazuub',
            point='idzmyrdzrhxospfduvok',
            comments='tosvbcbljppbrxpcgggy',
            current_update='vdbktgbcgbmrtlauusvt',
            current_update_datetime=datetime.datetime.now(datetime.timezone.utc),
            corridor_ids=None,
            start_datetime=datetime.datetime.now(datetime.timezone.utc),
            end_datetime=datetime.datetime.now(datetime.timezone.utc),
            last_modified_time=datetime.datetime.now(datetime.timezone.utc),
            level_of_interest='tvauxlxpcxdjzgjdqthz',
            location='atpypmaficmxatmgrjxd',
            is_provisional=False,
            has_closures=False,
            streets=None,
            geography='ejfkjylvggmbbyzbviou',
            geometry='hfnuzxvzpihwwejbrplq',
            status='dmrfgktpvxquxuopshjw',
            is_active=True
        )