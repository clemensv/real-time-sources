""" MonitoredVehicleJourney dataclass. """

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
class MonitoredVehicleJourney:
    """
    Real-time vehicle monitoring update from the Entur SIRI-VM feed.
    Attributes:
        service_journey_id (str): NeTEx ServiceJourney identifier from FramedVehicleJourneyRef/DatedVehicleJourneyRef.
        operating_day (str): ISO 8601 date string from FramedVehicleJourneyRef/DataFrameRef.
        recorded_at_time (str): ISO 8601 UTC timestamp from VehicleActivity/RecordedAtTime.
        line_ref (str): NeTEx Line reference.
        operator_ref (str): Operator codespace.
        direction_ref (typing.Optional[str]): Direction reference.
        vehicle_mode (typing.Optional[str]): Transport mode.
        published_line_name (typing.Optional[str]): Public-facing line name.
        origin_name (typing.Optional[str]): Origin stop name.
        destination_name (typing.Optional[str]): Destination stop name.
        vehicle_ref (typing.Optional[str]): VehicleRef identifier. This is payload data, not the Kafka key.
        latitude (typing.Optional[float]): WGS84 latitude from VehicleLocation.
        longitude (typing.Optional[float]): WGS84 longitude from VehicleLocation.
        bearing (typing.Optional[float]): Compass bearing in degrees (0-360).
        delay_seconds (typing.Optional[int]): Current delay in seconds, parsed from SIRI Delay ISO 8601 duration.
        occupancy_status (typing.Optional[str]): OccupancyStatus: full, standingRoomOnly, seatsAvailable, empty, etc.
        progress_status (typing.Optional[str]): ProgressStatus: inProgress, notExpected, notRun, cancelled.
        monitored (bool): True if this journey is actively monitored by an AVL system."""
    
    service_journey_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="service_journey_id"))
    operating_day: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operating_day"))
    recorded_at_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="recorded_at_time"))
    line_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="line_ref"))
    operator_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_ref"))
    direction_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction_ref"))
    vehicle_mode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_mode"))
    published_line_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published_line_name"))
    origin_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_name"))
    destination_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_name"))
    vehicle_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_ref"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    bearing: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bearing"))
    delay_seconds: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay_seconds"))
    occupancy_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="occupancy_status"))
    progress_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="progress_status"))
    monitored: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="monitored"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"MonitoredVehicleJourney\", \"namespace\": \"no.entur\", \"doc\": \"Real-time vehicle monitoring update from the Entur SIRI-VM feed.\", \"fields\": [{\"name\": \"service_journey_id\", \"type\": \"string\", \"doc\": \"NeTEx ServiceJourney identifier from FramedVehicleJourneyRef/DatedVehicleJourneyRef.\"}, {\"name\": \"operating_day\", \"type\": \"string\", \"doc\": \"ISO 8601 date string from FramedVehicleJourneyRef/DataFrameRef.\"}, {\"name\": \"recorded_at_time\", \"type\": \"string\", \"doc\": \"ISO 8601 UTC timestamp from VehicleActivity/RecordedAtTime.\"}, {\"name\": \"line_ref\", \"type\": \"string\", \"doc\": \"NeTEx Line reference.\"}, {\"name\": \"operator_ref\", \"type\": \"string\", \"doc\": \"Operator codespace.\"}, {\"name\": \"direction_ref\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Direction reference.\"}, {\"name\": \"vehicle_mode\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Transport mode.\"}, {\"name\": \"published_line_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Public-facing line name.\"}, {\"name\": \"origin_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Origin stop name.\"}, {\"name\": \"destination_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Destination stop name.\"}, {\"name\": \"vehicle_ref\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"VehicleRef identifier. This is payload data, not the Kafka key.\"}, {\"name\": \"latitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS84 latitude from VehicleLocation.\"}, {\"name\": \"longitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS84 longitude from VehicleLocation.\"}, {\"name\": \"bearing\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Compass bearing in degrees (0-360).\"}, {\"name\": \"delay_seconds\", \"type\": [\"null\", \"int\"], \"default\": null, \"doc\": \"Current delay in seconds, parsed from SIRI Delay ISO 8601 duration.\"}, {\"name\": \"occupancy_status\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"OccupancyStatus: full, standingRoomOnly, seatsAvailable, empty, etc.\"}, {\"name\": \"progress_status\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ProgressStatus: inProgress, notExpected, notRun, cancelled.\"}, {\"name\": \"monitored\", \"type\": \"boolean\", \"doc\": \"True if this journey is actively monitored by an AVL system.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.service_journey_id=str(self.service_journey_id)
        self.operating_day=str(self.operating_day)
        self.recorded_at_time=str(self.recorded_at_time)
        self.line_ref=str(self.line_ref)
        self.operator_ref=str(self.operator_ref)
        self.direction_ref=str(self.direction_ref) if self.direction_ref else None
        self.vehicle_mode=str(self.vehicle_mode) if self.vehicle_mode else None
        self.published_line_name=str(self.published_line_name) if self.published_line_name else None
        self.origin_name=str(self.origin_name) if self.origin_name else None
        self.destination_name=str(self.destination_name) if self.destination_name else None
        self.vehicle_ref=str(self.vehicle_ref) if self.vehicle_ref else None
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None
        self.bearing=float(self.bearing) if self.bearing else None
        self.delay_seconds=int(self.delay_seconds) if self.delay_seconds else None
        self.occupancy_status=str(self.occupancy_status) if self.occupancy_status else None
        self.progress_status=str(self.progress_status) if self.progress_status else None
        self.monitored=bool(self.monitored)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'MonitoredVehicleJourney':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['MonitoredVehicleJourney']:
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
            return MonitoredVehicleJourney.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return MonitoredVehicleJourney.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')