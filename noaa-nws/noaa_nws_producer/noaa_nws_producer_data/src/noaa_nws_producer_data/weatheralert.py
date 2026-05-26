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
import avro.schema
import avro.io
from noaa_nws_producer_data.categoryenum import CategoryEnum
from noaa_nws_producer_data.urgencyenum import UrgencyEnum
from noaa_nws_producer_data.messagetypeenum import MessageTypeenum
from noaa_nws_producer_data.certaintyenum import CertaintyEnum
from noaa_nws_producer_data.severityenum import SeverityEnum
from noaa_nws_producer_data.statusenum import StatusEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WeatherAlert:
    """
    Active weather alert from the NWS Common Alerting Protocol (CAP) feed. Alerts cover severe weather warnings, watches, advisories, and statements issued by NWS Weather Forecast Offices.
    
    Attributes:
        alert_id (str)
        area_desc (str)
        sent (datetime.datetime)
        effective (datetime.datetime)
        expires (datetime.datetime)
        status (StatusEnum)
        message_type (MessageTypeenum)
        category (typing.Optional[CategoryEnum])
        severity (SeverityEnum)
        certainty (CertaintyEnum)
        urgency (UrgencyEnum)
        event (str)
        sender_name (typing.Optional[str])
        headline (typing.Optional[str])
        description (typing.Optional[str])
        zone_id (typing.Optional[str])
        state (typing.Optional[str])
        event_type (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"WeatherAlert\", \"doc\": \"Active weather alert from the NWS Common Alerting Protocol (CAP) feed. Alerts cover severe weather warnings, watches, advisories, and statements issued by NWS Weather Forecast Offices.\", \"fields\": [{\"name\": \"alert_id\", \"type\": \"string\"}, {\"name\": \"area_desc\", \"type\": \"string\"}, {\"name\": \"sent\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}}, {\"name\": \"effective\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}}, {\"name\": \"expires\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}}, {\"name\": \"status\", \"type\": \"string\"}, {\"name\": \"message_type\", \"type\": \"string\"}, {\"name\": \"category\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"severity\", \"type\": \"string\"}, {\"name\": \"certainty\", \"type\": \"string\"}, {\"name\": \"urgency\", \"type\": \"string\"}, {\"name\": \"event\", \"type\": \"string\"}, {\"name\": \"sender_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"headline\", \"type\": [\"string\", \"null\"], \"default\": null}, {\"name\": \"description\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"zone_id\", \"type\": [\"null\", \"string\"], \"doc\": \"Normalized routing field 'zone_id' added for MQTT/AMQP subscriber filtering.\", \"default\": null}, {\"name\": \"state\", \"type\": [\"null\", \"string\"], \"doc\": \"Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.\", \"default\": null}, {\"name\": \"event_type\", \"type\": [\"null\", \"string\"], \"doc\": \"Normalized routing field 'event_type' added for MQTT/AMQP subscriber filtering.\", \"default\": null}]}"
    )
    
    
    alert_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_id"))
    area_desc: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_desc"))
    sent: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sent", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    effective: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="effective", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    expires: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expires", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    status: StatusEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    message_type: MessageTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="message_type"))
    category: typing.Optional[CategoryEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    severity: SeverityEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    certainty: CertaintyEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="certainty"))
    urgency: UrgencyEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="urgency"))
    event: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event"))
    sender_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender_name"))
    headline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headline"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    zone_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="zone_id"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    event_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_type"))

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
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'WeatherAlert':
        """
        Converts a dictionary from Avro deserialization to a dataclass instance.
        Handles conversion of string representations back to Python types for
        extended logical types.
        
        Args:
            data: The dictionary from Avro deserialization.
        
        Returns:
            The dataclass representation.
        """
        # Convert string values back to Python types for Avro string-based logical types
        converted = data.copy()
        if 'alert_id' in converted and converted['alert_id'] is not None:
            value = converted['alert_id']
        if 'area_desc' in converted and converted['area_desc'] is not None:
            value = converted['area_desc']
        if 'sent' in converted and converted['sent'] is not None:
            value = converted['sent']
            if isinstance(value, str):
                converted['sent'] = datetime.datetime.fromisoformat(value)
        if 'effective' in converted and converted['effective'] is not None:
            value = converted['effective']
            if isinstance(value, str):
                converted['effective'] = datetime.datetime.fromisoformat(value)
        if 'expires' in converted and converted['expires'] is not None:
            value = converted['expires']
            if isinstance(value, str):
                converted['expires'] = datetime.datetime.fromisoformat(value)
        if 'status' in converted and converted['status'] is not None:
            value = converted['status']
        if 'message_type' in converted and converted['message_type'] is not None:
            value = converted['message_type']
        if 'category' in converted and converted['category'] is not None:
            value = converted['category']
        if 'severity' in converted and converted['severity'] is not None:
            value = converted['severity']
        if 'certainty' in converted and converted['certainty'] is not None:
            value = converted['certainty']
        if 'urgency' in converted and converted['urgency'] is not None:
            value = converted['urgency']
        if 'event' in converted and converted['event'] is not None:
            value = converted['event']
        if 'sender_name' in converted and converted['sender_name'] is not None:
            value = converted['sender_name']
        if 'headline' in converted and converted['headline'] is not None:
            value = converted['headline']
        if 'description' in converted and converted['description'] is not None:
            value = converted['description']
        if 'zone_id' in converted and converted['zone_id'] is not None:
            value = converted['zone_id']
        if 'state' in converted and converted['state'] is not None:
            value = converted['state']
        if 'event_type' in converted and converted['event_type'] is not None:
            value = converted['event_type']
        
        return cls(**converted)

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

    def to_avro_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary suitable for Avro serialization.
        Handles conversion of Python types to Avro-compatible string representations
        for extended logical types.

        Returns:
            The dictionary representation suitable for Avro serialization.
        """
        result = self.to_serializer_dict()
        converted = result.copy()
        
        # Convert specific fields based on their source types
        if 'sent' in converted and converted['sent'] is not None:
            value = converted['sent']
            if isinstance(value, datetime.datetime):
                converted['sent'] = value.isoformat()
        if 'effective' in converted and converted['effective'] is not None:
            value = converted['effective']
            if isinstance(value, datetime.datetime):
                converted['effective'] = value.isoformat()
        if 'expires' in converted and converted['expires'] is not None:
            value = converted['expires']
            if isinstance(value, datetime.datetime):
                converted['expires'] = value.isoformat()
        
        return converted

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'application/json': Encodes the data to JSON format.
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
                Supported content type extensions:
                    '+gzip': Compresses the byte array using gzip, e.g. 'application/json+gzip'.

        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        result = None
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            # Convert to Avro binary format using the embedded schema
            writer = avro.io.DatumWriter(self.AvroType)
            with io.BytesIO() as stream:
                encoder = avro.io.BinaryEncoder(stream)
                writer.write(self.to_avro_dict(), encoder)
                result = stream.getvalue()
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
                    'avro/binary': Attempts to decode the data from Avro binary format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            if isinstance(data, bytes):
                # Decode from Avro binary format using the embedded schema
                reader = avro.io.DatumReader(cls.AvroType)
                with io.BytesIO(data) as stream:
                    decoder = avro.io.BinaryDecoder(stream)
                    _record = reader.read(decoder)
                    return WeatherAlert.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
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
            alert_id='wxqtvjxewiutlogizyoe',
            area_desc='bzrgvjyipdmeymcxqeiv',
            sent=datetime.datetime.now(datetime.timezone.utc),
            effective=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            message_type=MessageTypeenum.Alert,
            category=CategoryEnum.Met,
            severity=SeverityEnum.Extreme,
            certainty=CertaintyEnum.Observed,
            urgency=UrgencyEnum.Immediate,
            event='vxsiddltxwfnoqgdiflw',
            sender_name='lxetkugzbtsorzksmpfz',
            headline='vqbruhrtykmfuqulkbpv',
            description='vrsvurnfoclypjbgfdou',
            zone_id='grlyjrtdgpekhrnczxko',
            state='zrpcunetfqvkzhmvqgbs',
            event_type='oqunhkmhaqwpvthsqnxx'
        )