""" Departure dataclass. """

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
class Departure:
    """
    A single scheduled departure from a Belgian railway station with real-time status.
    Attributes:
        destination_station_id (str): Nine-digit UIC-derived numeric identifier of the destination station.
        destination_name (str): Display name of the destination station.
        scheduled_time (str): Scheduled departure time in ISO 8601 UTC.
        delay_seconds (int): Current delay in seconds.
        is_canceled (bool): True if this departure has been canceled.
        has_left (bool): True if the train has already departed.
        is_extra_stop (bool): True if this stop is not part of the original schedule.
        vehicle_id (str): Full iRail vehicle identifier.
        vehicle_short_name (str): Human-readable short name of the train service.
        vehicle_type (str): NMBS train service type abbreviation.
        vehicle_number (str): Numeric part of the vehicle identifier.
        platform (typing.Optional[str]): Platform number. Null if not assigned.
        is_normal_platform (bool): True if the platform is the normally scheduled one.
        occupancy (str): Crowd-sourced occupancy estimate: low, medium, high, or unknown.
        departure_connection_uri (str): Stable linked-data URI uniquely identifying this departure."""
    
    destination_station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_station_id"))
    destination_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_name"))
    scheduled_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="scheduled_time"))
    delay_seconds: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay_seconds"))
    is_canceled: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_canceled"))
    has_left: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="has_left"))
    is_extra_stop: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_extra_stop"))
    vehicle_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_id"))
    vehicle_short_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_short_name"))
    vehicle_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_type"))
    vehicle_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_number"))
    platform: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="platform"))
    is_normal_platform: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_normal_platform"))
    occupancy: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="occupancy"))
    departure_connection_uri: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departure_connection_uri"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Departure\", \"doc\": \"A single scheduled departure from a Belgian railway station with real-time status.\", \"fields\": [{\"name\": \"destination_station_id\", \"type\": \"string\", \"doc\": \"Nine-digit UIC-derived numeric identifier of the destination station.\"}, {\"name\": \"destination_name\", \"type\": \"string\", \"doc\": \"Display name of the destination station.\"}, {\"name\": \"scheduled_time\", \"type\": \"string\", \"doc\": \"Scheduled departure time in ISO 8601 UTC.\"}, {\"name\": \"delay_seconds\", \"type\": \"int\", \"doc\": \"Current delay in seconds.\"}, {\"name\": \"is_canceled\", \"type\": \"boolean\", \"doc\": \"True if this departure has been canceled.\"}, {\"name\": \"has_left\", \"type\": \"boolean\", \"doc\": \"True if the train has already departed.\"}, {\"name\": \"is_extra_stop\", \"type\": \"boolean\", \"doc\": \"True if this stop is not part of the original schedule.\"}, {\"name\": \"vehicle_id\", \"type\": \"string\", \"doc\": \"Full iRail vehicle identifier.\"}, {\"name\": \"vehicle_short_name\", \"type\": \"string\", \"doc\": \"Human-readable short name of the train service.\"}, {\"name\": \"vehicle_type\", \"type\": \"string\", \"doc\": \"NMBS train service type abbreviation.\"}, {\"name\": \"vehicle_number\", \"type\": \"string\", \"doc\": \"Numeric part of the vehicle identifier.\"}, {\"name\": \"platform\", \"type\": [\"null\", \"string\"], \"doc\": \"Platform number. Null if not assigned.\", \"default\": null}, {\"name\": \"is_normal_platform\", \"type\": \"boolean\", \"doc\": \"True if the platform is the normally scheduled one.\"}, {\"name\": \"occupancy\", \"type\": \"string\", \"doc\": \"Crowd-sourced occupancy estimate: low, medium, high, or unknown.\"}, {\"name\": \"departure_connection_uri\", \"type\": \"string\", \"doc\": \"Stable linked-data URI uniquely identifying this departure.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.destination_station_id=str(self.destination_station_id)
        self.destination_name=str(self.destination_name)
        self.scheduled_time=str(self.scheduled_time)
        self.delay_seconds=int(self.delay_seconds)
        self.is_canceled=bool(self.is_canceled)
        self.has_left=bool(self.has_left)
        self.is_extra_stop=bool(self.is_extra_stop)
        self.vehicle_id=str(self.vehicle_id)
        self.vehicle_short_name=str(self.vehicle_short_name)
        self.vehicle_type=str(self.vehicle_type)
        self.vehicle_number=str(self.vehicle_number)
        self.platform=str(self.platform) if self.platform else None
        self.is_normal_platform=bool(self.is_normal_platform)
        self.occupancy=str(self.occupancy)
        self.departure_connection_uri=str(self.departure_connection_uri)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Departure':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Departure']:
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
            return Departure.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Departure.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')