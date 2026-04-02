""" StaticVoyageData dataclass. """

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
class StaticVoyageData:
    """
    A StaticVoyageData record.
    Attributes:
        mmsi (int): 
        imo_number (int): 
        callsign (str): 
        ship_name (str): 
        ship_type (int): 
        dimension_to_bow (int): 
        dimension_to_stern (int): 
        dimension_to_port (int): 
        dimension_to_starboard (int): 
        draught (float): 
        destination (str): 
        eta_month (int): 
        eta_day (int): 
        eta_hour (int): 
        eta_minute (int): 
        timestamp (str): 
        station_id (str): """
    
    mmsi: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmsi"))
    imo_number: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imo_number"))
    callsign: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="callsign"))
    ship_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ship_name"))
    ship_type: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ship_type"))
    dimension_to_bow: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_bow"))
    dimension_to_stern: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_stern"))
    dimension_to_port: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_port"))
    dimension_to_starboard: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dimension_to_starboard"))
    draught: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="draught"))
    destination: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination"))
    eta_month: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_month"))
    eta_day: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_day"))
    eta_hour: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_hour"))
    eta_minute: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_minute"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"StaticVoyageData\", \"namespace\": \"NO.Kystverket.AIS\", \"fields\": [{\"name\": \"mmsi\", \"type\": \"long\"}, {\"name\": \"imo_number\", \"type\": \"long\"}, {\"name\": \"callsign\", \"type\": \"string\"}, {\"name\": \"ship_name\", \"type\": \"string\"}, {\"name\": \"ship_type\", \"type\": \"long\"}, {\"name\": \"dimension_to_bow\", \"type\": \"long\"}, {\"name\": \"dimension_to_stern\", \"type\": \"long\"}, {\"name\": \"dimension_to_port\", \"type\": \"long\"}, {\"name\": \"dimension_to_starboard\", \"type\": \"long\"}, {\"name\": \"draught\", \"type\": \"double\"}, {\"name\": \"destination\", \"type\": \"string\"}, {\"name\": \"eta_month\", \"type\": \"long\"}, {\"name\": \"eta_day\", \"type\": \"long\"}, {\"name\": \"eta_hour\", \"type\": \"long\"}, {\"name\": \"eta_minute\", \"type\": \"long\"}, {\"name\": \"timestamp\", \"type\": \"string\"}, {\"name\": \"station_id\", \"type\": \"string\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.mmsi=int(self.mmsi)
        self.imo_number=int(self.imo_number)
        self.callsign=str(self.callsign)
        self.ship_name=str(self.ship_name)
        self.ship_type=int(self.ship_type)
        self.dimension_to_bow=int(self.dimension_to_bow)
        self.dimension_to_stern=int(self.dimension_to_stern)
        self.dimension_to_port=int(self.dimension_to_port)
        self.dimension_to_starboard=int(self.dimension_to_starboard)
        self.draught=float(self.draught)
        self.destination=str(self.destination)
        self.eta_month=int(self.eta_month)
        self.eta_day=int(self.eta_day)
        self.eta_hour=int(self.eta_hour)
        self.eta_minute=int(self.eta_minute)
        self.timestamp=str(self.timestamp)
        self.station_id=str(self.station_id)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'StaticVoyageData':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['StaticVoyageData']:
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
            return StaticVoyageData.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return StaticVoyageData.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')