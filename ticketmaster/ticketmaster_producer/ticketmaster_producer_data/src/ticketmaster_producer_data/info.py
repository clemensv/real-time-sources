""" Info dataclass. """

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
import avro.schema
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Info:
    """
    Reference information for the source, area, or event collection used by MQTT retained topics and AMQP consumers to discover the logical feed scope.

    Attributes:
        info_id (str)
        name (str)
        country (typing.Optional[str])
        city (typing.Optional[str])
        category (typing.Optional[str])
        price_area (typing.Optional[str])
        settlement_date (typing.Optional[str])
        settlement_period (typing.Optional[int])
        area_code (typing.Optional[str])
        segment (typing.Optional[str])
        entity_id (typing.Optional[str])
        event_id (typing.Optional[str])
        venue_id (typing.Optional[str])
    """

    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Info\", \"doc\": \"Reference information for the source, area, or event collection used by MQTT retained topics and AMQP consumers to discover the logical feed scope.\", \"fields\": [{\"name\": \"info_id\", \"type\": \"string\", \"doc\": \"Stable identifier for the reference information record; used as the CloudEvents subject when no more specific upstream entity exists.\"}, {\"name\": \"name\", \"type\": \"string\", \"doc\": \"Human-readable name for the source, area, or event collection represented by this reference information record.\"}, {\"name\": \"country\", \"type\": [\"string\", \"null\"], \"doc\": \"Lower-case ISO 3166-1 alpha-2 country code or intl when the feed spans countries.\", \"default\": null}, {\"name\": \"city\", \"type\": [\"string\", \"null\"], \"doc\": \"City segment used in civic-events topic routing, or null when not applicable.\", \"default\": null}, {\"name\": \"category\", \"type\": [\"string\", \"null\"], \"doc\": \"Event category segment used in topic routing, or null when not applicable.\", \"default\": null}, {\"name\": \"price_area\", \"type\": [\"string\", \"null\"], \"doc\": \"Energy market price area or bidding zone represented by this reference record, when applicable.\", \"default\": null}, {\"name\": \"settlement_date\", \"type\": [\"string\", \"null\"], \"doc\": \"GB settlement date for Elexon retained information topics when applicable.\", \"default\": null}, {\"name\": \"settlement_period\", \"type\": [\"int\", \"null\"], \"doc\": \"GB settlement period for Elexon retained information topics when applicable.\", \"default\": null}, {\"name\": \"area_code\", \"type\": [\"string\", \"null\"], \"doc\": \"Electricity control area or utility service area code represented by this record when applicable.\", \"default\": null}, {\"name\": \"segment\", \"type\": [\"string\", \"null\"], \"doc\": \"Ticketmaster classification segment used for wildcard topic routing, when applicable.\", \"default\": null}, {\"name\": \"entity_id\", \"type\": [\"string\", \"null\"], \"doc\": \"Stable upstream entity identifier for reference topics, when applicable.\", \"default\": null}, {\"name\": \"event_id\", \"type\": [\"string\", \"null\"], \"doc\": \"Stable upstream event identifier for event-scoped reference topics, when applicable.\", \"default\": null}, {\"name\": \"venue_id\", \"type\": [\"string\", \"null\"], \"doc\": \"Stable venue identifier for venue-scoped civic event topics, when applicable.\", \"default\": null}]}"
    )


    info_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="info_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    country: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    city: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="city"))
    category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    price_area: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_area"))
    settlement_date: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="settlement_date"))
    settlement_period: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="settlement_period"))
    area_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_code"))
    segment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segment"))
    entity_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="entity_id"))
    event_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    venue_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_id"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Info':
        """
        Converts a dictionary to a dataclass instance.

        Args:
            data: The dictionary to convert to a dataclass.

        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'Info':
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
        if 'info_id' in converted and converted['info_id'] is not None:
            value = converted['info_id']
        if 'name' in converted and converted['name'] is not None:
            value = converted['name']
        if 'country' in converted and converted['country'] is not None:
            value = converted['country']
        if 'city' in converted and converted['city'] is not None:
            value = converted['city']
        if 'category' in converted and converted['category'] is not None:
            value = converted['category']
        if 'price_area' in converted and converted['price_area'] is not None:
            value = converted['price_area']
        if 'settlement_date' in converted and converted['settlement_date'] is not None:
            value = converted['settlement_date']
        if 'settlement_period' in converted and converted['settlement_period'] is not None:
            value = converted['settlement_period']
        if 'area_code' in converted and converted['area_code'] is not None:
            value = converted['area_code']
        if 'segment' in converted and converted['segment'] is not None:
            value = converted['segment']
        if 'entity_id' in converted and converted['entity_id'] is not None:
            value = converted['entity_id']
        if 'event_id' in converted and converted['event_id'] is not None:
            value = converted['event_id']
        if 'venue_id' in converted and converted['venue_id'] is not None:
            value = converted['venue_id']

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Info']:
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
                    return Info.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Info.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Info':
        """
        Creates an instance of the dataclass with test values.

        Returns:
            An instance of the dataclass.
        """
        return cls(
            info_id='btlvpozkkzrzqejunvbc',
            name='rrxkxoyrlqrpjgsfeaqu',
            country='kgkckfeyncpjmcsfoczu',
            city='ustakjbastultakxpojd',
            category='uinhdvvjayyhnmebusqj',
            price_area='frnusicreqgiqrcmgnjz',
            settlement_date='ggxipkycbelucukwaybm',
            settlement_period=int(18),
            area_code='wqqgskouwjltzgdxkqht',
            segment='coazssecjdqgxuhcqfpq',
            entity_id='vpjsneifagppyeeqdveu',
            event_id='cucvsrotmcizteaxmkwe',
            venue_id='leeuedqqhwjravajvtrs'
        )