""" VesselLocation dataclass. """

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
class VesselLocation:
    """
    WSF vessel location.
    Attributes:
        vessel_id (str): 
        vessel_name (str): 
        mmsi (typing.Optional[int]): 
        in_service (bool): 
        at_dock (bool): 
        latitude (float): 
        longitude (float): 
        speed (typing.Optional[float]): 
        heading (typing.Optional[int]): 
        departing_terminal_id (typing.Optional[int]): 
        departing_terminal_name (typing.Optional[str]): 
        departing_terminal_abbrev (typing.Optional[str]): 
        arriving_terminal_id (typing.Optional[int]): 
        arriving_terminal_name (typing.Optional[str]): 
        arriving_terminal_abbrev (typing.Optional[str]): 
        scheduled_departure (typing.Optional[str]): 
        left_dock (typing.Optional[str]): 
        eta (typing.Optional[str]): 
        eta_basis (typing.Optional[str]): 
        route_abbreviation (typing.Optional[str]): 
        timestamp (str): """
    
    vessel_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vessel_id"))
    vessel_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vessel_name"))
    mmsi: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmsi"))
    in_service: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="in_service"))
    at_dock: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="at_dock"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="speed"))
    heading: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="heading"))
    departing_terminal_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departing_terminal_id"))
    departing_terminal_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departing_terminal_name"))
    departing_terminal_abbrev: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departing_terminal_abbrev"))
    arriving_terminal_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arriving_terminal_id"))
    arriving_terminal_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arriving_terminal_name"))
    arriving_terminal_abbrev: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arriving_terminal_abbrev"))
    scheduled_departure: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="scheduled_departure"))
    left_dock: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="left_dock"))
    eta: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta"))
    eta_basis: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="eta_basis"))
    route_abbreviation: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_abbreviation"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"VesselLocation\", \"namespace\": \"us.wa.wsdot.ferries\", \"doc\": \"WSF vessel location.\", \"fields\": [{\"name\": \"vessel_id\", \"type\": \"string\"}, {\"name\": \"vessel_name\", \"type\": \"string\"}, {\"name\": \"mmsi\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"in_service\", \"type\": \"boolean\"}, {\"name\": \"at_dock\", \"type\": \"boolean\"}, {\"name\": \"latitude\", \"type\": \"double\"}, {\"name\": \"longitude\", \"type\": \"double\"}, {\"name\": \"speed\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"heading\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"departing_terminal_id\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"departing_terminal_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"departing_terminal_abbrev\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"arriving_terminal_id\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"arriving_terminal_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"arriving_terminal_abbrev\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"scheduled_departure\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"left_dock\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"eta\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"eta_basis\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"route_abbreviation\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"timestamp\", \"type\": \"string\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.vessel_id=str(self.vessel_id)
        self.vessel_name=str(self.vessel_name)
        self.mmsi=int(self.mmsi) if self.mmsi else None
        self.in_service=bool(self.in_service)
        self.at_dock=bool(self.at_dock)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.speed=float(self.speed) if self.speed else None
        self.heading=int(self.heading) if self.heading else None
        self.departing_terminal_id=int(self.departing_terminal_id) if self.departing_terminal_id else None
        self.departing_terminal_name=str(self.departing_terminal_name) if self.departing_terminal_name else None
        self.departing_terminal_abbrev=str(self.departing_terminal_abbrev) if self.departing_terminal_abbrev else None
        self.arriving_terminal_id=int(self.arriving_terminal_id) if self.arriving_terminal_id else None
        self.arriving_terminal_name=str(self.arriving_terminal_name) if self.arriving_terminal_name else None
        self.arriving_terminal_abbrev=str(self.arriving_terminal_abbrev) if self.arriving_terminal_abbrev else None
        self.scheduled_departure=str(self.scheduled_departure) if self.scheduled_departure else None
        self.left_dock=str(self.left_dock) if self.left_dock else None
        self.eta=str(self.eta) if self.eta else None
        self.eta_basis=str(self.eta_basis) if self.eta_basis else None
        self.route_abbreviation=str(self.route_abbreviation) if self.route_abbreviation else None
        self.timestamp=str(self.timestamp)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'VesselLocation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VesselLocation']:
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
            return VesselLocation.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return VesselLocation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')