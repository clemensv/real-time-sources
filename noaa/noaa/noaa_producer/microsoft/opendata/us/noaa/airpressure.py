""" AirPressure dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
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
class AirPressure:
    """
    A AirPressure record.
    Attributes:
        station_id (str): {"description": "7 character station ID, or a currents station ID."}
        timestamp (str): {"description": "Timestamp of the air pressure measurement"}
        value (float): {"description": "Value of the air pressure"}
        max_pressure_exceeded (bool): Flag indicating if the maximum expected air pressure was exceeded
        min_pressure_exceeded (bool): Flag indicating if the minimum expected air pressure was exceeded
        rate_of_change_exceeded (bool): Flag indicating if the rate of change tolerance limit was exceeded"""
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    max_pressure_exceeded: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_pressure_exceeded"))
    min_pressure_exceeded: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="min_pressure_exceeded"))
    rate_of_change_exceeded: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rate_of_change_exceeded"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"AirPressure\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"{'description': '7 character station ID, or a currents station ID.'}\"}, {\"name\": \"timestamp\", \"type\": \"string\", \"logicalType\": \"timestamp-millis\", \"doc\": \"{'description': 'Timestamp of the air pressure measurement'}\"}, {\"name\": \"value\", \"type\": \"double\", \"doc\": \"{'description': 'Value of the air pressure'}\", \"unit\": \"hPa\"}, {\"name\": \"max_pressure_exceeded\", \"type\": \"boolean\", \"doc\": \"Flag indicating if the maximum expected air pressure was exceeded\"}, {\"name\": \"min_pressure_exceeded\", \"type\": \"boolean\", \"doc\": \"Flag indicating if the minimum expected air pressure was exceeded\"}, {\"name\": \"rate_of_change_exceeded\", \"type\": \"boolean\", \"doc\": \"Flag indicating if the rate of change tolerance limit was exceeded\"}], \"altnames\": {\"kql\": \"AirPressure\"}, \"namespace\": \"Microsoft.OpenData.US.NOAA\"}"
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.timestamp=str(self.timestamp)
        self.value=float(self.value)
        self.max_pressure_exceeded=bool(self.max_pressure_exceeded)
        self.min_pressure_exceeded=bool(self.min_pressure_exceeded)
        self.rate_of_change_exceeded=bool(self.rate_of_change_exceeded)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'AirPressure':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
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
            if isinstance(v,enum.Enum):
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
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(self.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['AirPressure']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'avro/binary': Attempts to decode the data from Avro binary encoded format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary encoded format.
                    'avro/json': Attempts to decode the data from Avro JSON encoded format.
                    'application/vnd.apache.avro+json': Attempts to decode the data from Avro JSON encoded format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro', 'avro/json', 'application/vnd.apache.avro+json']:
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for conversion to Stream')
            reader = avro.io.DatumReader(cls.AvroType)
            if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
                decoder = avro.io.BinaryDecoder(stream)
            else:
                raise NotImplementedError(f'Unsupported Avro media type {content_type}')
            _record = reader.read(decoder)            
            return AirPressure.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return AirPressure.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')