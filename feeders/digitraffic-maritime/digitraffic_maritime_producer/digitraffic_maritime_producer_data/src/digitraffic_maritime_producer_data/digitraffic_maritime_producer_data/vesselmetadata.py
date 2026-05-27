""" VesselMetadata dataclass. """

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
class VesselMetadata:
    """
    AIS vessel static and voyage data from Digitraffic MQTT stream. Represents decoded AIS message type 5/24 data.
    Attributes:
        mmsi (typing.Optional[int]): 
        timestamp (int): 
        name (typing.Optional[str]): 
        callSign (typing.Optional[str]): 
        imo (typing.Optional[int]): 
        type (typing.Optional[int]): 
        draught (typing.Optional[int]): 
        eta (typing.Optional[int]): 
        destination (typing.Optional[str]): 
        posType (typing.Optional[int]): 
        refA (typing.Optional[int]): 
        refB (typing.Optional[int]): 
        refC (typing.Optional[int]): 
        refD (typing.Optional[int]): """
    
    mmsi: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmsi"))
    timestamp: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    callSign: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="callSign"))
    imo: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imo"))
    type: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="type"))
    draught: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="draught"))
    eta: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta"))
    destination: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination"))
    posType: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="posType"))
    refA: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="refA"))
    refB: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="refB"))
    refC: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="refC"))
    refD: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="refD"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"VesselMetadata\", \"doc\": \"AIS vessel static and voyage data from Digitraffic MQTT stream. Represents decoded AIS message type 5/24 data.\", \"fields\": [{\"name\": \"mmsi\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"timestamp\", \"type\": \"int\"}, {\"name\": \"name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"callSign\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"imo\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"type\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"draught\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"eta\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"destination\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"posType\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"refA\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"refB\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"refC\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"refD\", \"type\": [\"null\", \"int\"], \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.mmsi=int(self.mmsi) if self.mmsi else None
        self.timestamp=int(self.timestamp)
        self.name=str(self.name) if self.name else None
        self.callSign=str(self.callSign) if self.callSign else None
        self.imo=int(self.imo) if self.imo else None
        self.type=int(self.type) if self.type else None
        self.draught=int(self.draught) if self.draught else None
        self.eta=int(self.eta) if self.eta else None
        self.destination=str(self.destination) if self.destination else None
        self.posType=int(self.posType) if self.posType else None
        self.refA=int(self.refA) if self.refA else None
        self.refB=int(self.refB) if self.refB else None
        self.refC=int(self.refC) if self.refC else None
        self.refD=int(self.refD) if self.refD else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'VesselMetadata':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VesselMetadata']:
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
            return VesselMetadata.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return VesselMetadata.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')