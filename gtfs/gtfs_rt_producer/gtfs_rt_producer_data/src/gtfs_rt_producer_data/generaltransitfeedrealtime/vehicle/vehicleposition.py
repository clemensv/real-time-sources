""" VehiclePosition dataclass. """

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
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.tripdescriptor import TripDescriptor
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.position import Position
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.vehiclestopstatus import VehicleStopStatus
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicledescriptor import VehicleDescriptor
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.congestionlevel import CongestionLevel
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.occupancystatus import OccupancyStatus


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class VehiclePosition:
    """
    Realtime positioning information for a given vehicle.
    Attributes:
        trip (typing.Optional[TripDescriptor]): The Trip that this vehicle is serving. Can be empty or partial if the vehicle can not be identified with a given trip instance.
        vehicle (typing.Optional[VehicleDescriptor]): Additional information on the vehicle that is serving this trip.
        position (typing.Optional[Position]): Current position of this vehicle. The stop sequence index of the current stop. The meaning of
        current_stop_sequence (typing.Optional[int]): current_stop_sequence (i.e., the stop that it refers to) is determined by current_status. If current_status is missing IN_TRANSIT_TO is assumed. Identifies the current stop. The value must be the same as in stops.txt in
        stop_id (typing.Optional[str]): the corresponding GTFS feed.
        current_status (typing.Optional[VehicleStopStatus]): The exact status of the vehicle with respect to the current stop. Ignored if current_stop_sequence is missing. Moment at which the vehicle's position was measured. In POSIX time
        timestamp (typing.Optional[int]): (i.e., number of seconds since January 1st 1970 00:00:00 UTC).
        congestion_level (typing.Optional[CongestionLevel]): 
        occupancy_status (typing.Optional[OccupancyStatus]): """
    
    trip: typing.Optional[TripDescriptor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trip"))
    vehicle: typing.Optional[VehicleDescriptor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle"))
    position: typing.Optional[Position]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="position"))
    current_stop_sequence: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_stop_sequence"))
    stop_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop_id"))
    current_status: typing.Optional[VehicleStopStatus]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_status"))
    timestamp: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    congestion_level: typing.Optional[CongestionLevel]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="congestion_level"))
    occupancy_status: typing.Optional[OccupancyStatus]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="occupancy_status"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"VehiclePosition\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle\", \"fields\": [{\"name\": \"trip\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"TripDescriptor\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle\", \"fields\": [{\"name\": \"trip_id\", \"type\": [\"null\", \"string\"], \"doc\": \"The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary.\"}, {\"name\": \"route_id\", \"type\": [\"null\", \"string\"], \"doc\": \"The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the\"}, {\"name\": \"direction_id\", \"type\": [\"null\", \"int\"], \"doc\": \"direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future.\"}, {\"name\": \"start_time\", \"type\": [\"null\", \"string\"], \"doc\": \"The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance.\"}, {\"name\": \"start_date\", \"type\": [\"null\", \"string\"], \"doc\": \"Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format.\"}, {\"name\": \"schedule_relationship\", \"type\": [\"null\", {\"name\": \"ScheduleRelationship\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle.TripDescriptor_types\", \"symbols\": [\"SCHEDULED\", \"ADDED\", \"UNSCHEDULED\", \"CANCELED\"], \"ordinals\": {\"SCHEDULED\": 0, \"ADDED\": 1, \"UNSCHEDULED\": 2, \"CANCELED\": 3}, \"doc\": \"The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.\"}]}], \"doc\": \"A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary,   start_time) is set. If route_id is also set, then it should be same as one   that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be   set. Note that if the trip_id is not known, then stop sequence ids in   TripUpdate are not sufficient, and stop_ids must be provided as well. In   addition, absolute arrival/departure times must be provided.\"}], \"doc\": \"The Trip that this vehicle is serving. Can be empty or partial if the vehicle can not be identified with a given trip instance.\"}, {\"name\": \"vehicle\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"VehicleDescriptor\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle\", \"fields\": [{\"name\": \"id\", \"type\": [\"null\", \"string\"], \"doc\": \"Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to\"}, {\"name\": \"label\", \"type\": [\"null\", \"string\"], \"doc\": \"help identify the correct vehicle.\"}, {\"name\": \"license_plate\", \"type\": [\"null\", \"string\"], \"doc\": \"The license plate of the vehicle.\"}], \"doc\": \"Identification information for the vehicle performing the trip.\"}], \"doc\": \"Additional information on the vehicle that is serving this trip.\"}, {\"name\": \"position\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"Position\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle\", \"fields\": [{\"name\": \"latitude\", \"type\": \"float\", \"doc\": \"Degrees North, in the WGS-84 coordinate system.\"}, {\"name\": \"longitude\", \"type\": \"float\", \"doc\": \"Degrees East, in the WGS-84 coordinate system.\"}, {\"name\": \"bearing\", \"type\": [\"null\", \"float\"], \"doc\": \"Bearing, in degrees, clockwise from North, i.e., 0 is North and 90 is East. This can be the compass bearing, or the direction towards the next stop or intermediate location. This should not be direction deduced from the sequence of previous positions, which can be computed from previous data.\"}, {\"name\": \"odometer\", \"type\": [\"null\", \"double\"], \"doc\": \"Odometer value, in meters.\"}, {\"name\": \"speed\", \"type\": [\"null\", \"float\"], \"doc\": \"Momentary speed measured by the vehicle, in meters per second.\"}], \"doc\": \"A position.\"}], \"doc\": \"Current position of this vehicle. The stop sequence index of the current stop. The meaning of\"}, {\"name\": \"current_stop_sequence\", \"type\": [\"null\", \"int\"], \"doc\": \"current_stop_sequence (i.e., the stop that it refers to) is determined by current_status. If current_status is missing IN_TRANSIT_TO is assumed. Identifies the current stop. The value must be the same as in stops.txt in\"}, {\"name\": \"stop_id\", \"type\": [\"null\", \"string\"], \"doc\": \"the corresponding GTFS feed.\"}, {\"name\": \"current_status\", \"type\": [\"null\", {\"name\": \"VehicleStopStatus\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle.VehiclePosition_types\", \"symbols\": [\"INCOMING_AT\", \"STOPPED_AT\", \"IN_TRANSIT_TO\"], \"ordinals\": {\"INCOMING_AT\": 0, \"STOPPED_AT\": 1, \"IN_TRANSIT_TO\": 2}}], \"doc\": \"The exact status of the vehicle with respect to the current stop. Ignored if current_stop_sequence is missing. Moment at which the vehicle's position was measured. In POSIX time\"}, {\"name\": \"timestamp\", \"type\": [\"null\", \"long\"], \"doc\": \"(i.e., number of seconds since January 1st 1970 00:00:00 UTC).\"}, {\"name\": \"congestion_level\", \"type\": [\"null\", {\"name\": \"CongestionLevel\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle.VehiclePosition_types\", \"symbols\": [\"UNKNOWN_CONGESTION_LEVEL\", \"RUNNING_SMOOTHLY\", \"STOP_AND_GO\", \"CONGESTION\", \"SEVERE_CONGESTION\"], \"ordinals\": {\"UNKNOWN_CONGESTION_LEVEL\": 0, \"RUNNING_SMOOTHLY\": 1, \"STOP_AND_GO\": 2, \"CONGESTION\": 3, \"SEVERE_CONGESTION\": 4}, \"doc\": \"Congestion level that is affecting this vehicle.\"}]}, {\"name\": \"occupancy_status\", \"type\": [\"null\", {\"name\": \"OccupancyStatus\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Vehicle.VehiclePosition_types\", \"symbols\": [\"EMPTY\", \"MANY_SEATS_AVAILABLE\", \"FEW_SEATS_AVAILABLE\", \"STANDING_ROOM_ONLY\", \"CRUSHED_STANDING_ROOM_ONLY\", \"FULL\", \"NOT_ACCEPTING_PASSENGERS\"], \"ordinals\": {\"EMPTY\": 0, \"MANY_SEATS_AVAILABLE\": 1, \"FEW_SEATS_AVAILABLE\": 2, \"STANDING_ROOM_ONLY\": 3, \"CRUSHED_STANDING_ROOM_ONLY\": 4, \"FULL\": 5, \"NOT_ACCEPTING_PASSENGERS\": 6}, \"doc\": \"The degree of passenger occupancy of the vehicle. This field is still experimental, and subject to change. It may be formally adopted in the future.\"}]}], \"doc\": \"Realtime positioning information for a given vehicle.\"}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.trip=self.trip if isinstance(self.trip, TripDescriptor) else TripDescriptor.from_serializer_dict(self.trip) if self.trip else None if self.trip else None
        self.vehicle=self.vehicle if isinstance(self.vehicle, VehicleDescriptor) else VehicleDescriptor.from_serializer_dict(self.vehicle) if self.vehicle else None if self.vehicle else None
        self.position=self.position if isinstance(self.position, Position) else Position.from_serializer_dict(self.position) if self.position else None if self.position else None
        self.current_stop_sequence=int(self.current_stop_sequence) if self.current_stop_sequence else None
        self.stop_id=str(self.stop_id) if self.stop_id else None
        self.current_status=VehicleStopStatus(self.current_status) if self.current_status else None
        self.timestamp=int(self.timestamp) if self.timestamp else None
        self.congestion_level=CongestionLevel(self.congestion_level) if self.congestion_level else None
        self.occupancy_status=OccupancyStatus(self.occupancy_status) if self.occupancy_status else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'VehiclePosition':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VehiclePosition']:
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
            return VehiclePosition.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return VehiclePosition.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')