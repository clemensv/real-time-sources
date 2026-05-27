""" ArrivalBoard dataclass. """

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
from irail_producer_data.be.irail.arrival import Arrival


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ArrivalBoard:
    """
    Real-time arrival board for a Belgian railway station.
    Attributes:
        station_id (str): Nine-digit UIC-derived numeric identifier of the station.
        station_name (str): Display name of the station.
        retrieved_at (str): ISO 8601 UTC timestamp when this board was retrieved.
        arrival_count (int): Number of arrivals in this board snapshot.
        arrivals (typing.List[Arrival]): Array of arrival entries on the station board."""
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    retrieved_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="retrieved_at"))
    arrival_count: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrival_count"))
    arrivals: typing.List[Arrival]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrivals"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"ArrivalBoard\", \"namespace\": \"be.irail\", \"doc\": \"Real-time arrival board for a Belgian railway station.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Nine-digit UIC-derived numeric identifier of the station.\"}, {\"name\": \"station_name\", \"type\": \"string\", \"doc\": \"Display name of the station.\"}, {\"name\": \"retrieved_at\", \"type\": \"string\", \"doc\": \"ISO 8601 UTC timestamp when this board was retrieved.\"}, {\"name\": \"arrival_count\", \"type\": \"int\", \"doc\": \"Number of arrivals in this board snapshot.\"}, {\"name\": \"arrivals\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"Arrival\", \"doc\": \"A single scheduled arrival at a Belgian railway station with real-time status.\", \"fields\": [{\"name\": \"origin_station_id\", \"type\": \"string\", \"doc\": \"Nine-digit UIC-derived numeric identifier of the origin station.\"}, {\"name\": \"origin_name\", \"type\": \"string\", \"doc\": \"Display name of the origin station.\"}, {\"name\": \"scheduled_time\", \"type\": \"string\", \"doc\": \"Scheduled arrival time in ISO 8601 UTC.\"}, {\"name\": \"delay_seconds\", \"type\": \"int\", \"doc\": \"Current delay in seconds.\"}, {\"name\": \"is_canceled\", \"type\": \"boolean\", \"doc\": \"True if this arrival has been canceled.\"}, {\"name\": \"has_arrived\", \"type\": \"boolean\", \"doc\": \"True if the train has already arrived.\"}, {\"name\": \"is_extra_stop\", \"type\": \"boolean\", \"doc\": \"True if this stop is not part of the original schedule.\"}, {\"name\": \"vehicle_id\", \"type\": \"string\", \"doc\": \"Full iRail vehicle identifier.\"}, {\"name\": \"vehicle_short_name\", \"type\": \"string\", \"doc\": \"Human-readable short name of the train service.\"}, {\"name\": \"vehicle_type\", \"type\": \"string\", \"doc\": \"NMBS train service type abbreviation.\"}, {\"name\": \"vehicle_number\", \"type\": \"string\", \"doc\": \"Numeric part of the vehicle identifier.\"}, {\"name\": \"platform\", \"type\": [\"null\", \"string\"], \"doc\": \"Platform number. Null if not assigned.\", \"default\": null}, {\"name\": \"is_normal_platform\", \"type\": \"boolean\", \"doc\": \"True if the platform is the normally scheduled one.\"}, {\"name\": \"occupancy\", \"type\": \"string\", \"doc\": \"Crowd-sourced occupancy estimate: low, medium, high, or unknown.\"}, {\"name\": \"connection_uri\", \"type\": \"string\", \"doc\": \"Stable linked-data URI uniquely identifying this arrival.\"}]}}, \"doc\": \"Array of arrival entries on the station board.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.station_name=str(self.station_name)
        self.retrieved_at=str(self.retrieved_at)
        self.arrival_count=int(self.arrival_count)
        self.arrivals=self.arrivals if isinstance(self.arrivals, list) else [v if isinstance(v, Arrival) else Arrival.from_serializer_dict(v) if v else None for v in self.arrivals] if self.arrivals else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'ArrivalBoard':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['ArrivalBoard']:
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
            return ArrivalBoard.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return ArrivalBoard.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')