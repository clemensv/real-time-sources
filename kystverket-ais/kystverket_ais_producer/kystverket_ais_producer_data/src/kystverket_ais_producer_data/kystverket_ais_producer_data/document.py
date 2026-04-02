""" Document dataclass. """

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
class Document:
    """
    A Document record.
    Attributes:
        mmsi (int): 
        imo_number (typing.Optional[int]): 
        callsign (typing.Optional[str]): 
        ship_name (typing.Optional[str]): 
        ship_type (typing.Optional[int]): 
        dimension_to_bow (typing.Optional[int]): 
        dimension_to_stern (typing.Optional[int]): 
        dimension_to_port (typing.Optional[int]): 
        dimension_to_starboard (typing.Optional[int]): 
        draught (typing.Optional[float]): 
        destination (typing.Optional[str]): 
        eta_month (typing.Optional[int]): 
        eta_day (typing.Optional[int]): 
        eta_hour (typing.Optional[int]): 
        eta_minute (typing.Optional[int]): 
        timestamp (str): 
        station_id (typing.Optional[str]): """
    
    mmsi: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmsi"))
    imo_number: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imo_number"))
    callsign: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="callsign"))
    ship_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ship_name"))
    ship_type: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ship_type"))
    dimension_to_bow: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_bow"))
    dimension_to_stern: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_stern"))
    dimension_to_port: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_port"))
    dimension_to_starboard: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_starboard"))
    draught: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="draught"))
    destination: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination"))
    eta_month: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_month"))
    eta_day: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_day"))
    eta_hour: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_hour"))
    eta_minute: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_minute"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    station_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"document\", \"fields\": [{\"name\": \"mmsi\", \"type\": \"int\"}, {\"name\": \"imo_number\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"callsign\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"ship_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"ship_type\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"dimension_to_bow\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"dimension_to_stern\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"dimension_to_port\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"dimension_to_starboard\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"draught\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"destination\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"eta_month\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"eta_day\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"eta_hour\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"eta_minute\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"timestamp\", \"type\": \"string\"}, {\"name\": \"station_id\", \"type\": [\"null\", \"string\"], \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.mmsi=int(self.mmsi)
        self.imo_number=int(self.imo_number) if self.imo_number else None
        self.callsign=str(self.callsign) if self.callsign else None
        self.ship_name=str(self.ship_name) if self.ship_name else None
        self.ship_type=int(self.ship_type) if self.ship_type else None
        self.dimension_to_bow=int(self.dimension_to_bow) if self.dimension_to_bow else None
        self.dimension_to_stern=int(self.dimension_to_stern) if self.dimension_to_stern else None
        self.dimension_to_port=int(self.dimension_to_port) if self.dimension_to_port else None
        self.dimension_to_starboard=int(self.dimension_to_starboard) if self.dimension_to_starboard else None
        self.draught=float(self.draught) if self.draught else None
        self.destination=str(self.destination) if self.destination else None
        self.eta_month=int(self.eta_month) if self.eta_month else None
        self.eta_day=int(self.eta_day) if self.eta_day else None
        self.eta_hour=int(self.eta_hour) if self.eta_hour else None
        self.eta_minute=int(self.eta_minute) if self.eta_minute else None
        self.timestamp=str(self.timestamp)
        self.station_id=str(self.station_id) if self.station_id else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Document':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Document']:
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
            return Document.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Document.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')