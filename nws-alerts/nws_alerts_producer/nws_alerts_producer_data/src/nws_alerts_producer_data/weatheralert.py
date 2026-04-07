""" WeatherAlert dataclass. """

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
from nws_alerts_producer_data.certaintyenum import CertaintyEnum
from nws_alerts_producer_data.severityenum import SeverityEnum
from nws_alerts_producer_data.urgencyenum import UrgencyEnum
from nws_alerts_producer_data.messagetypeenum import MessageTypeenum
from nws_alerts_producer_data.statusenum import StatusEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WeatherAlert:
    """
    A weather or non-weather alert from the US National Weather Service (NWS/NOAA). Contains full CAP properties including severity, urgency, certainty, VTEC codes for event tracking, and UGC/SAME zone geocodes.
    
    Attributes:
        alert_id (str)
        area_desc (typing.Optional[str])
        same_codes (typing.Optional[str])
        ugc_codes (typing.Optional[str])
        sent (datetime.datetime)
        effective (typing.Optional[datetime.datetime])
        onset (typing.Optional[datetime.datetime])
        expires (typing.Optional[datetime.datetime])
        ends (typing.Optional[datetime.datetime])
        status (StatusEnum)
        message_type (MessageTypeenum)
        category (typing.Optional[str])
        severity (SeverityEnum)
        certainty (CertaintyEnum)
        urgency (UrgencyEnum)
        event (str)
        sender (typing.Optional[str])
        sender_name (typing.Optional[str])
        headline (typing.Optional[str])
        description (typing.Optional[str])
        instruction (typing.Optional[str])
        response (typing.Optional[str])
        scope (typing.Optional[str])
        code (typing.Optional[str])
        nws_headline (typing.Optional[str])
        vtec (typing.Optional[str])
        web (typing.Optional[str])
    """
    
    
    alert_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_id"))
    area_desc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_desc"))
    same_codes: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="same_codes"))
    ugc_codes: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ugc_codes"))
    sent: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sent", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    effective: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="effective", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    onset: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onset", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    expires: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expires", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    ends: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ends", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    status: StatusEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    message_type: MessageTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="message_type"))
    category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    severity: SeverityEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    certainty: CertaintyEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="certainty"))
    urgency: UrgencyEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="urgency"))
    event: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event"))
    sender: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender"))
    sender_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender_name"))
    headline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headline"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    instruction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="instruction"))
    response: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="response"))
    scope: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="scope"))
    code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code"))
    nws_headline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nws_headline"))
    vtec: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vtec"))
    web: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="web"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WeatherAlert':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WeatherAlert']:
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
                return WeatherAlert.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WeatherAlert':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            alert_id='qkocnvopesgeypfivbnh',
            area_desc='vimpkczbibnylcuechip',
            same_codes='umofbnuysklsmyzttyqq',
            ugc_codes='wfladtzwhkqxkvtwpcfl',
            sent=datetime.datetime.now(datetime.timezone.utc),
            effective=datetime.datetime.now(datetime.timezone.utc),
            onset=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            ends=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            message_type=MessageTypeenum.Alert,
            category='labipkbqicpzlqhiznei',
            severity=SeverityEnum.Extreme,
            certainty=CertaintyEnum.Observed,
            urgency=UrgencyEnum.Immediate,
            event='jxqngiwekneemgshnrkn',
            sender='shudqnfgxmhrvyvgfewp',
            sender_name='lnwqwbkxowwhjnflzhpr',
            headline='ylnzvjtxvtcfzuedfxrt',
            description='dhrdvfjmswsjxmgqnroi',
            instruction='wqgmpkzekulfjostgkqy',
            response='imvsfhdpoodzrjbbqtpw',
            scope='qptioijdgtufxgoaqvev',
            code='izimctvtqhpekrsmujmc',
            nws_headline='bwsjicdtnapbbrqozpqy',
            vtec='hokhcopozgutenitrzyg',
            web='kiumdfugtiwiattqzrbz'
        )