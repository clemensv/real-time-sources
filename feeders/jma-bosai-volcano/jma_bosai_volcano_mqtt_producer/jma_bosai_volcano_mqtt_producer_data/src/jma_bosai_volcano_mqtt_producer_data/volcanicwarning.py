""" VolcanicWarning dataclass. """

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
from jma_bosai_volcano_mqtt_producer_data.conditionenum import ConditionEnum
from jma_bosai_volcano_mqtt_producer_data.alertlevelcodeenum import AlertLevelCodeenum
from jma_bosai_volcano_mqtt_producer_data.eventenum import EventEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class VolcanicWarning:
    """
    JMA Bosai active volcanic warning or forecast for a target volcano.
    
    Attributes:
        volcano_code (str)
        event_id (str)
        report_datetime (datetime.datetime)
        report_datetime_local (datetime.datetime)
        alert_level_code (AlertLevelCodeenum)
        alert_level_name (str)
        previous_level_code (typing.Optional[str])
        condition (ConditionEnum)
        info_type_jp (str)
        area_codes (typing.List[str])
        prefecture (str)
        event (EventEnum)
    """
    
    
    volcano_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="volcano_code"))
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    report_datetime: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="report_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    report_datetime_local: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="report_datetime_local", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    alert_level_code: AlertLevelCodeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_level_code"))
    alert_level_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_level_name"))
    previous_level_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="previous_level_code"))
    condition: ConditionEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="condition"))
    info_type_jp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="info_type_jp"))
    area_codes: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_codes"))
    prefecture: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="prefecture"))
    event: EventEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'VolcanicWarning':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VolcanicWarning']:
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
                return VolcanicWarning.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'VolcanicWarning':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            volcano_code='qglhcqawclwsjgzoifrl',
            event_id='mbfgjgfgrsnolucohvdg',
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            alert_level_code=AlertLevelCodeenum.CODE_02,
            alert_level_name='fiwvhqhazxmorxcocbhe',
            previous_level_code='iflwglljambdkqinfskd',
            condition=ConditionEnum.ISSUED,
            info_type_jp='vytxzqlzdovzjovhczmn',
            area_codes=['qafsmtzbbhdrsigpvjpu', 'uzwqjaeyxrxfufttaxah', 'kmvhgksjjjndgalukjxe', 'aiixmfaiyhdjmfumcovq', 'lvhbqvzurzrxlvcbccww'],
            prefecture='qfrsyohkdieelouubkdk',
            event=EventEnum.warning
        )