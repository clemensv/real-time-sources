""" SpotPrice dataclass. """

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
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SpotPrice:
    """
    Day-ahead electricity spot price for a given bidding zone at a specific timestamp. Sourced from the Energy-Charts /price endpoint (Fraunhofer ISE) which provides wholesale electricity market prices from ENTSO-E and national exchanges. Prices are the day-ahead auction clearing price in EUR per MWh. The bidding zone identifies the market area (e.g. 'DE-LU' for the Germany-Luxembourg zone).

    Attributes:
        country (str)
        bidding_zone (str)
        timestamp (datetime.datetime)
        unix_seconds (int)
        price_eur_per_mwh (typing.Optional[float])
        unit (typing.Optional[str])
    """

    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"SpotPrice\", \"doc\": \"Day-ahead electricity spot price for a given bidding zone at a specific timestamp. Sourced from the Energy-Charts /price endpoint (Fraunhofer ISE) which provides wholesale electricity market prices from ENTSO-E and national exchanges. Prices are the day-ahead auction clearing price in EUR per MWh. The bidding zone identifies the market area (e.g. 'DE-LU' for the Germany-Luxembourg zone).\", \"fields\": [{\"name\": \"country\", \"type\": \"string\", \"doc\": \"ISO 3166-1 alpha-2 country code derived from the bidding zone (e.g. 'de' from 'DE-LU'). Used for Kafka key partitioning.\"}, {\"name\": \"bidding_zone\", \"type\": \"string\", \"doc\": \"European electricity bidding zone identifier as used by ENTSO-E (e.g. 'DE-LU' for Germany-Luxembourg, 'FR' for France, 'NO1' for Norway zone 1). The bzn parameter in the Energy-Charts /price API.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"UTC timestamp derived from the unix_seconds value. Marks the start of the price interval (typically 15-minute or hourly depending on the market).\"}, {\"name\": \"unix_seconds\", \"type\": \"long\", \"doc\": \"Unix epoch timestamp in seconds as returned by the Energy-Charts API.\"}, {\"name\": \"price_eur_per_mwh\", \"type\": [\"double\", \"null\"], \"doc\": \"Day-ahead electricity spot price in EUR per megawatt-hour (EUR/MWh). This is the clearing price from the day-ahead auction on the relevant power exchange. Can be negative during periods of excess generation.\", \"default\": null}, {\"name\": \"unit\", \"type\": [\"string\", \"null\"], \"doc\": \"Unit label as returned by the Energy-Charts API (e.g. 'EUR / MWh'). Included for traceability with the upstream response.\", \"default\": null}]}"
    )


    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    bidding_zone: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bidding_zone"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    unix_seconds: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unix_seconds"))
    price_eur_per_mwh: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_eur_per_mwh"))
    unit: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unit"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SpotPrice':
        """
        Converts a dictionary to a dataclass instance.

        Args:
            data: The dictionary to convert to a dataclass.

        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'SpotPrice':
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
        if 'country' in converted and converted['country'] is not None:
            value = converted['country']
        if 'bidding_zone' in converted and converted['bidding_zone'] is not None:
            value = converted['bidding_zone']
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, str):
                converted['timestamp'] = datetime.datetime.fromisoformat(value)
        if 'unix_seconds' in converted and converted['unix_seconds'] is not None:
            value = converted['unix_seconds']
        if 'price_eur_per_mwh' in converted and converted['price_eur_per_mwh'] is not None:
            value = converted['price_eur_per_mwh']
        if 'unit' in converted and converted['unit'] is not None:
            value = converted['unit']

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
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, datetime.datetime):
                converted['timestamp'] = value.isoformat()

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SpotPrice']:
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
                    return SpotPrice.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return SpotPrice.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SpotPrice':
        """
        Creates an instance of the dataclass with test values.

        Returns:
            An instance of the dataclass.
        """
        return cls(
            country='bgtwuixdnyvwnekqbzcr',
            bidding_zone='oegludapwxeoaltjjpij',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(9),
            price_eur_per_mwh=float(45.860063566150224),
            unit='jzaeferrbisiilkyqqqo'
        )