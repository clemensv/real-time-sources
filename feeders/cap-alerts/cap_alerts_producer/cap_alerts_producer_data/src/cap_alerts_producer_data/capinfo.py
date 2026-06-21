""" CapInfo dataclass. """

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
from cap_alerts_producer_data.categorylistenum import CategoryListEnum
from cap_alerts_producer_data.responsetypelistenum import ResponseTypelistenum
from cap_alerts_producer_data.urgencyenum import UrgencyEnum
from cap_alerts_producer_data.capresource import CapResource
from cap_alerts_producer_data.certaintyenum import CertaintyEnum
from cap_alerts_producer_data.severityenum import SeverityEnum
from cap_alerts_producer_data.valuepair import ValuePair
from cap_alerts_producer_data.caparea import CapArea
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CapInfo:
    """
    CAP 1.2 info block containing audience-facing alert content in a specific language and for one set of areas/resources. CAP permits multiple info blocks, commonly for multilingual MeteoAlarm alerts or updated instructions; the feeder preserves all blocks in order.
    
    Attributes:
        language (typing.Optional[str])
        category (typing.Optional[typing.List[CategoryListEnum]])
        event (typing.Optional[str])
        response_type (typing.Optional[typing.List[ResponseTypelistenum]])
        urgency (typing.Optional[UrgencyEnum])
        severity (typing.Optional[SeverityEnum])
        certainty (typing.Optional[CertaintyEnum])
        audience (typing.Optional[str])
        event_code (typing.Optional[typing.List[ValuePair]])
        effective (typing.Optional[datetime.datetime])
        onset (typing.Optional[datetime.datetime])
        expires (typing.Optional[datetime.datetime])
        sender_name (typing.Optional[str])
        headline (typing.Optional[str])
        description (typing.Optional[str])
        instruction (typing.Optional[str])
        web (typing.Optional[str])
        contact (typing.Optional[str])
        parameter (typing.Optional[typing.List[ValuePair]])
        resource (typing.Optional[typing.List[CapResource]])
        area (typing.Optional[typing.List[CapArea]])
    """
    
    
    language: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="language"))
    category: typing.Optional[typing.List[CategoryListEnum]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    event: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event"))
    response_type: typing.Optional[typing.List[ResponseTypelistenum]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="response_type"))
    urgency: typing.Optional[UrgencyEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="urgency"))
    severity: typing.Optional[SeverityEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    certainty: typing.Optional[CertaintyEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="certainty"))
    audience: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="audience"))
    event_code: typing.Optional[typing.List[ValuePair]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_code"))
    effective: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="effective", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    onset: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onset", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    expires: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expires", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    sender_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender_name"))
    headline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headline"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    instruction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="instruction"))
    web: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="web"))
    contact: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contact"))
    parameter: typing.Optional[typing.List[ValuePair]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter"))
    resource: typing.Optional[typing.List[CapResource]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="resource"))
    area: typing.Optional[typing.List[CapArea]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'CapInfo':
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
            if isinstance(result, str):
                result = result.encode('utf-8')
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['CapInfo']:
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
                return CapInfo.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'CapInfo':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            language='cuvuhgssyoewnrldglms',
            category=[CategoryListEnum.Geo, CategoryListEnum.Geo, CategoryListEnum.Geo, CategoryListEnum.Geo],
            event='dsbpkzambsdprhkhyigc',
            response_type=[ResponseTypelistenum.Shelter],
            urgency=UrgencyEnum.Immediate,
            severity=SeverityEnum.Extreme,
            certainty=CertaintyEnum.Observed,
            audience='wheschcypwnxlgyrscxb',
            event_code=[None, None, None, None, None],
            effective=datetime.datetime.now(datetime.timezone.utc),
            onset=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            sender_name='cnzjbdsmdsgyqxcyoymk',
            headline='koliywudgxaebovlqeuj',
            description='rptjxtwnfsuqvcfegfxp',
            instruction='opwcrpahhklwqxiqnpdc',
            web='oricepifcpogfiokheyh',
            contact='wudlmxbgybvdxanhldqx',
            parameter=[None, None],
            resource=[None, None, None],
            area=[None, None, None, None, None]
        )