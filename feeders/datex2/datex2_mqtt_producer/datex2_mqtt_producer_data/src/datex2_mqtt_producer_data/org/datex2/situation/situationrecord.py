""" SituationRecord dataclass. """

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
class SituationRecord:
    """
    Normalized situation record from a DATEX II SituationPublication. It represents incidents, accidents, roadworks, abnormal traffic, obstructions, weather impacts, and network-management measures with stable situation and record identifiers.
    
    Attributes:
        supplier_id (str)
        situation_id (str)
        situation_record_id (str)
        feed_url (str)
        version (typing.Optional[str])
        record_type (str)
        severity (typing.Optional[str])
        probability (typing.Optional[str])
        validity_status (typing.Optional[str])
        creation_time (typing.Optional[datetime.datetime])
        observation_time (typing.Optional[datetime.datetime])
        overall_start_time (typing.Optional[datetime.datetime])
        overall_end_time (typing.Optional[datetime.datetime])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        road_number (typing.Optional[str])
        direction (typing.Optional[str])
        location_description (typing.Optional[str])
        description (typing.Optional[str])
        source_name (typing.Optional[str])
        cause (typing.Optional[str])
        management_type (typing.Optional[str])
        raw_record (typing.Optional[str])
        country_code (str)
        operator_id (str)
    """
    
    
    supplier_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="supplier_id"))
    situation_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="situation_id"))
    situation_record_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="situation_record_id"))
    feed_url: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feed_url"))
    version: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version"))
    record_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="record_type"))
    severity: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    probability: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="probability"))
    validity_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="validity_status"))
    creation_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="creation_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    observation_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    overall_start_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="overall_start_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    overall_end_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="overall_end_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    road_number: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_number"))
    direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction"))
    location_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_description"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    source_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_name"))
    cause: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cause"))
    management_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="management_type"))
    raw_record: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="raw_record"))
    country_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_code"))
    operator_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_id"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SituationRecord':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SituationRecord']:
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
                return SituationRecord.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SituationRecord':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            supplier_id='nzoajpozzdtkunwtxhzh',
            situation_id='rdsdoknqajhwrososaku',
            situation_record_id='raimfwyqvornafpgbirt',
            feed_url='hpvpobajxhydbwzeszdf',
            version='gcvfskbohgxklsuzubvs',
            record_type='pfenjdlmvnflkyzrlhts',
            severity='ofecvjtxjsyuzfvaneev',
            probability='dbcsskfgkzrkqynvigej',
            validity_status='mwgsqpjjjzuuxfnmquvi',
            creation_time=datetime.datetime.now(datetime.timezone.utc),
            observation_time=datetime.datetime.now(datetime.timezone.utc),
            overall_start_time=datetime.datetime.now(datetime.timezone.utc),
            overall_end_time=datetime.datetime.now(datetime.timezone.utc),
            latitude=float(80.79358562528928),
            longitude=float(93.86704512216087),
            road_number='qjutwxtzodjlitinagvl',
            direction='upmtuqyqkyxmxohxvmol',
            location_description='mjtfifijrqpdcszmbcyn',
            description='nmfgumdchzwmitwadkpo',
            source_name='ssensiqvuftxqafwzxxe',
            cause='plptwdresmhdjfxdaysl',
            management_type='rlkwbweqpyossnrkdgjt',
            raw_record='tikakwknffavjskhrmbc',
            country_code='iwuaopzmhbbmlzjudwko',
            operator_id='emztxcibltggkzhiutxb'
        )