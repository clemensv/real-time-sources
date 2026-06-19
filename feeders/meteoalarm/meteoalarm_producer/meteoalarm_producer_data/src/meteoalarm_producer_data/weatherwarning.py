""" WeatherWarning dataclass. """

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
from meteoalarm_producer_data.severityenum import SeverityEnum
from meteoalarm_producer_data.certaintyenum import CertaintyEnum
from meteoalarm_producer_data.msgtypeenum import MsgTypeenum
from meteoalarm_producer_data.statusenum import StatusEnum
from meteoalarm_producer_data.categoryenum import CategoryEnum
from meteoalarm_producer_data.scopeenum import ScopeEnum
from meteoalarm_producer_data.urgencyenum import UrgencyEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WeatherWarning:
    """
    A severe weather warning from the EUMETNET Meteoalarm system, aggregating warnings from 30+ European national meteorological services. Each warning follows the CAP (Common Alerting Protocol) structure with awareness levels and hazard types.
    
    Attributes:
        identifier (str)
        sender (str)
        sent (datetime.datetime)
        status (StatusEnum)
        msg_type (MsgTypeenum)
        scope (ScopeEnum)
        country (str)
        event (str)
        category (typing.Optional[CategoryEnum])
        severity (SeverityEnum)
        urgency (UrgencyEnum)
        certainty (CertaintyEnum)
        headline (typing.Optional[str])
        description (typing.Optional[str])
        instruction (typing.Optional[str])
        effective (typing.Optional[datetime.datetime])
        onset (typing.Optional[datetime.datetime])
        expires (typing.Optional[datetime.datetime])
        web (typing.Optional[str])
        contact (typing.Optional[str])
        awareness_level (typing.Optional[str])
        awareness_type (str)
        area_desc (str)
        geocodes (typing.Optional[str])
        language (typing.Optional[str])
        awareness_type_raw (typing.Optional[str])
    """
    
    
    identifier: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="identifier"))
    sender: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender"))
    sent: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sent", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    status: StatusEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    msg_type: MsgTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="msg_type"))
    scope: ScopeEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="scope"))
    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    event: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event"))
    category: typing.Optional[CategoryEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    severity: SeverityEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    urgency: UrgencyEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="urgency"))
    certainty: CertaintyEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="certainty"))
    headline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headline"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    instruction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="instruction"))
    effective: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="effective", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    onset: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onset", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    expires: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expires", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    web: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="web"))
    contact: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contact"))
    awareness_level: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="awareness_level"))
    awareness_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="awareness_type"))
    area_desc: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_desc"))
    geocodes: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geocodes"))
    language: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="language"))
    awareness_type_raw: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="awareness_type_raw"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WeatherWarning':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WeatherWarning']:
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
                return WeatherWarning.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WeatherWarning':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            identifier='nxwmokdwxopowtvftqsx',
            sender='bnsljdleeearxfefrfny',
            sent=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            msg_type=MsgTypeenum.Alert,
            scope=ScopeEnum.Public,
            country='wygaccjtsarnswvzrntk',
            event='szwbcmhozahavowzvcbk',
            category=CategoryEnum.Met,
            severity=SeverityEnum.Extreme,
            urgency=UrgencyEnum.Immediate,
            certainty=CertaintyEnum.Observed,
            headline='masokoqhttofwolzczbg',
            description='rrljatnjbqrsmwyfuzfv',
            instruction='ebcigkxlrxjuxmiwkrlv',
            effective=datetime.datetime.now(datetime.timezone.utc),
            onset=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            web='ftmtkhfjxyrbbbskgspf',
            contact='qwwetrzjqeangxccqwxb',
            awareness_level='dlacbrtroalrxaviuaex',
            awareness_type='chhahmlpfsztuyydomxn',
            area_desc='nzppqnyomikzfmisftii',
            geocodes='xgfhakpirnzaviqdchfj',
            language='samqgzyuxffwwonzmgrb',
            awareness_type_raw='jivojmyahuytrflabqdj'
        )