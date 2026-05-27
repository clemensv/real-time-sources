""" WaterLevelObservation dataclass. """

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
class WaterLevelObservation:
    """
    WaterLevelObservation
    
    Attributes:
        station_code (str)
        location_name (typing.Optional[str])
        timestamp (datetime.datetime)
        value (float)
        unit (typing.Optional[str])
        quality_code (typing.Optional[str])
        status (typing.Optional[str])
        compartment (typing.Optional[str])
        parameter (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"WaterLevelObservation\", \"doc\": \"WaterLevelObservation\", \"fields\": [{\"name\": \"station_code\", \"type\": \"string\"}, {\"name\": \"location_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"timestamp\", \"type\": \"string\"}, {\"name\": \"value\", \"type\": \"double\"}, {\"name\": \"unit\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"quality_code\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"status\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"compartment\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"parameter\", \"type\": [\"null\", \"string\"], \"default\": null}]}"
    )
    
    
    station_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_code"))
    location_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_name"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    unit: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unit"))
    quality_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="quality_code"))
    status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    compartment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="compartment"))
    parameter: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WaterLevelObservation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'WaterLevelObservation':
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
        if 'station_code' in converted and converted['station_code'] is not None:
            value = converted['station_code']
        if 'location_name' in converted and converted['location_name'] is not None:
            value = converted['location_name']
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, str):
                converted['timestamp'] = datetime.datetime.fromisoformat(value)
        if 'value' in converted and converted['value'] is not None:
            value = converted['value']
        if 'unit' in converted and converted['unit'] is not None:
            value = converted['unit']
        if 'quality_code' in converted and converted['quality_code'] is not None:
            value = converted['quality_code']
        if 'status' in converted and converted['status'] is not None:
            value = converted['status']
        if 'compartment' in converted and converted['compartment'] is not None:
            value = converted['compartment']
        if 'parameter' in converted and converted['parameter'] is not None:
            value = converted['parameter']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WaterLevelObservation']:
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
                    return WaterLevelObservation.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WaterLevelObservation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WaterLevelObservation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_code='fmlytokxosojnmlsgvlr',
            location_name='nfawgwbrhqwrqvxznake',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(50.697599691699835),
            unit='bxckqhelshmmhyqnxdfq',
            quality_code='sdpknoezggfvflaezxzk',
            status='qaevsxczyowxopcbfuer',
            compartment='xcfmwoqxiobmdcevkeht',
            parameter='qxevnsprbawkcxeywelh'
        )
