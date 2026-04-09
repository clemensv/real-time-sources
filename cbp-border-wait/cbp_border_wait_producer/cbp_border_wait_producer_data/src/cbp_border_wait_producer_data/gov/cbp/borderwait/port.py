""" Port dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import json
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import avro.schema
import avro.name
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Port:
    """
    Reference data for a US CBP land border port of entry.
    Attributes:
        port_number (str): Six-digit CBP port number.
        port_name (str): City or locality name.
        border (str): International border: Canadian Border or Mexican Border.
        crossing_name (str): Name of the crossing facility.
        hours (str): Operating hours as a human-readable string.
        passenger_vehicle_max_lanes (typing.Optional[int]): Max passenger vehicle lanes. Null if not available.
        commercial_vehicle_max_lanes (typing.Optional[int]): Max commercial vehicle lanes. Null if not available.
        pedestrian_max_lanes (typing.Optional[int]): Max pedestrian lanes. Null if not available."""
    
    port_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_number"))
    port_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_name"))
    border: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="border"))
    crossing_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="crossing_name"))
    hours: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hours"))
    passenger_vehicle_max_lanes: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_max_lanes"))
    commercial_vehicle_max_lanes: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="commercial_vehicle_max_lanes"))
    pedestrian_max_lanes: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pedestrian_max_lanes"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Port\", \"namespace\": \"gov.cbp.borderwait\", \"doc\": \"Reference data for a US CBP land border port of entry.\", \"fields\": [{\"name\": \"port_number\", \"type\": \"string\", \"doc\": \"Six-digit CBP port number.\"}, {\"name\": \"port_name\", \"type\": \"string\", \"doc\": \"City or locality name.\"}, {\"name\": \"border\", \"type\": \"string\", \"doc\": \"International border: Canadian Border or Mexican Border.\"}, {\"name\": \"crossing_name\", \"type\": \"string\", \"doc\": \"Name of the crossing facility.\"}, {\"name\": \"hours\", \"type\": \"string\", \"doc\": \"Operating hours as a human-readable string.\"}, {\"name\": \"passenger_vehicle_max_lanes\", \"type\": [\"null\", \"int\"], \"doc\": \"Max passenger vehicle lanes. Null if not available.\", \"default\": null}, {\"name\": \"commercial_vehicle_max_lanes\", \"type\": [\"null\", \"int\"], \"doc\": \"Max commercial vehicle lanes. Null if not available.\", \"default\": null}, {\"name\": \"pedestrian_max_lanes\", \"type\": [\"null\", \"int\"], \"doc\": \"Max pedestrian lanes. Null if not available.\", \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.port_number=str(self.port_number)
        self.port_name=str(self.port_name)
        self.border=str(self.border)
        self.crossing_name=str(self.crossing_name)
        self.hours=str(self.hours)
        self.passenger_vehicle_max_lanes=int(self.passenger_vehicle_max_lanes) if self.passenger_vehicle_max_lanes else None
        self.commercial_vehicle_max_lanes=int(self.commercial_vehicle_max_lanes) if self.commercial_vehicle_max_lanes else None
        self.pedestrian_max_lanes=int(self.pedestrian_max_lanes) if self.pedestrian_max_lanes else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Port':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Port']:
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
            return Port.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Port.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')