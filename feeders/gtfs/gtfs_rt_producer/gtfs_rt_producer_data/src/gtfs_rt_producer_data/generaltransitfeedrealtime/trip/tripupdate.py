""" TripUpdate dataclass. """

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
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate import StopTimeUpdate
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripdescriptor import TripDescriptor
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.vehicledescriptor import VehicleDescriptor


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TripUpdate:
    """
    Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule. - A trip that proceeds along a route but has no fixed schedule. - A trip that have been added or removed with regard to schedule. The updates can be for future, predicted arrival/departure events, or for past events that already occurred. Normally, updates should get more precise and more certain (see uncertainty below) as the events gets closer to current time. Even if that is not possible, the information for past events should be precise and certain. In particular, if an update points to time in the past but its update's uncertainty is not 0, the client should conclude that the update is a (wrong) prediction and that the trip has not completed yet. Note that the update can describe a trip that is already completed. To this end, it is enough to provide an update for the last stop of the trip. If the time of that is in the past, the client will conclude from that that the whole trip is in the past (it is possible, although inconsequential, to also provide updates for preceding stops). This option is most relevant for a trip that has completed ahead of schedule, but according to the schedule, the trip is still proceeding at the current time. Removing the updates for this trip could make the client assume that the trip is still proceeding. Note that the feed provider is allowed, but not required, to purge past updates - this is one case where this would be practically useful.
    Attributes:
        trip (TripDescriptor): The Trip that this message applies to. There can be at most one TripUpdate entity for each actual trip instance. If there is none, that means there is no prediction information available. It does *not* mean that the trip is progressing according to schedule.
        vehicle (typing.Optional[VehicleDescriptor]): Additional information on the vehicle that is serving this trip.
        stop_time_update (typing.List[StopTimeUpdate]): Updates to StopTimes for the trip (both future, i.e., predictions, and in some cases, past ones, i.e., those that already happened). The updates must be sorted by stop_sequence, and apply for all the following stops of the trip up to the next specified one. Example 1: For a trip with 20 stops, a StopTimeUpdate with arrival delay and departure delay of 0 for stop_sequence of the current stop means that the trip is exactly on time. Example 2: For the same trip instance, 3 StopTimeUpdates are provided: - delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 - delay of unspecified duration for stop_sequence 10 This will be interpreted as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9 have delay of 1 min. - stop_sequences 10,... have unknown delay. Moment at which the vehicle's real-time progress was measured. In POSIX
        timestamp (typing.Optional[int]): time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC). The current schedule deviation for the trip.  Delay should only be
        delay (typing.Optional[int]): specified when the prediction is given relative to some existing schedule in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time. Delay information in StopTimeUpdates take precedent of trip-level delay information, such that trip-level delay is only propagated until the next stop along the trip with a StopTimeUpdate delay value specified. Feed providers are strongly encouraged to provide a TripUpdate.timestamp value indicating when the delay value was last updated, in order to evaluate the freshness of the data. NOTE: This field is still experimental, and subject to change. It may be formally adopted in the future."""
    
    trip: TripDescriptor=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trip"))
    vehicle: typing.Optional[VehicleDescriptor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle"))
    stop_time_update: typing.List[StopTimeUpdate]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop_time_update"))
    timestamp: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"TripUpdate\", \"namespace\": \"GeneralTransitFeedRealTime.Trip\", \"fields\": [{\"name\": \"trip\", \"type\": {\"type\": \"record\", \"name\": \"TripDescriptor\", \"namespace\": \"GeneralTransitFeedRealTime.Trip\", \"fields\": [{\"name\": \"trip_id\", \"type\": [\"null\", \"string\"], \"doc\": \"The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary.\"}, {\"name\": \"route_id\", \"type\": [\"null\", \"string\"], \"doc\": \"The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the\"}, {\"name\": \"direction_id\", \"type\": [\"null\", \"int\"], \"doc\": \"direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future.\"}, {\"name\": \"start_time\", \"type\": [\"null\", \"string\"], \"doc\": \"The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance.\"}, {\"name\": \"start_date\", \"type\": [\"null\", \"string\"], \"doc\": \"Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format.\"}, {\"name\": \"schedule_relationship\", \"type\": [\"null\", {\"name\": \"ScheduleRelationship\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Trip.TripDescriptor_types\", \"symbols\": [\"SCHEDULED\", \"ADDED\", \"UNSCHEDULED\", \"CANCELED\"], \"ordinals\": {\"SCHEDULED\": 0, \"ADDED\": 1, \"UNSCHEDULED\": 2, \"CANCELED\": 3}, \"doc\": \"The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.\"}]}], \"doc\": \"A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary,   start_time) is set. If route_id is also set, then it should be same as one   that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be   set. Note that if the trip_id is not known, then stop sequence ids in   TripUpdate are not sufficient, and stop_ids must be provided as well. In   addition, absolute arrival/departure times must be provided.\"}, \"doc\": \"The Trip that this message applies to. There can be at most one TripUpdate entity for each actual trip instance. If there is none, that means there is no prediction information available. It does *not* mean that the trip is progressing according to schedule.\"}, {\"name\": \"vehicle\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"VehicleDescriptor\", \"namespace\": \"GeneralTransitFeedRealTime.Trip\", \"fields\": [{\"name\": \"id\", \"type\": [\"null\", \"string\"], \"doc\": \"Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to\"}, {\"name\": \"label\", \"type\": [\"null\", \"string\"], \"doc\": \"help identify the correct vehicle.\"}, {\"name\": \"license_plate\", \"type\": [\"null\", \"string\"], \"doc\": \"The license plate of the vehicle.\"}], \"doc\": \"Identification information for the vehicle performing the trip.\"}], \"doc\": \"Additional information on the vehicle that is serving this trip.\"}, {\"name\": \"stop_time_update\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"StopTimeUpdate\", \"namespace\": \"GeneralTransitFeedRealTime.Trip.TripUpdate_types\", \"fields\": [{\"name\": \"stop_sequence\", \"type\": [\"null\", \"int\"], \"doc\": \"The update is linked to a specific stop either through stop_sequence or stop_id, so one of the fields below must necessarily be set. See the documentation in TripDescriptor for more information. Must be the same as in stop_times.txt in the corresponding GTFS feed.\"}, {\"name\": \"stop_id\", \"type\": [\"null\", \"string\"], \"doc\": \"Must be the same as in stops.txt in the corresponding GTFS feed.\"}, {\"name\": \"arrival\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"StopTimeEvent\", \"namespace\": \"GeneralTransitFeedRealTime.Trip.TripUpdate_types\", \"fields\": [{\"name\": \"delay\", \"type\": [\"null\", \"int\"], \"doc\": \"Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time.\"}, {\"name\": \"time\", \"type\": [\"null\", \"long\"], \"doc\": \"Event as absolute time. In Unix time (i.e., number of seconds since January 1st 1970 00:00:00 UTC). If uncertainty is omitted, it is interpreted as unknown.\"}, {\"name\": \"uncertainty\", \"type\": [\"null\", \"int\"], \"doc\": \"If the prediction is unknown or too uncertain, the delay (or time) field should be empty. In such case, the uncertainty field is ignored. To specify a completely certain prediction, set its uncertainty to 0.\"}], \"doc\": \"Timing information for a single predicted event (either arrival or departure). Timing consists of delay and/or estimated time, and uncertainty. - delay should be used when the prediction is given relative to some   existing schedule in GTFS. - time should be given whether there is a predicted schedule or not. If   both time and delay are specified, time will take precedence   (although normally, time, if given for a scheduled trip, should be   equal to scheduled time in GTFS + delay). Uncertainty applies equally to both time and delay. The uncertainty roughly specifies the expected error in true delay (but note, we don't yet define its precise statistical meaning). It's possible for the uncertainty to be 0, for example for trains that are driven under computer timing control.\"}]}, {\"name\": \"departure\", \"type\": [\"null\", \"GeneralTransitFeedRealTime.Trip.TripUpdate_types.StopTimeEvent\"]}, {\"name\": \"schedule_relationship\", \"type\": [\"null\", {\"name\": \"ScheduleRelationship\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Trip.TripUpdate_types.StopTimeUpdate_types\", \"symbols\": [\"SCHEDULED\", \"SKIPPED\", \"NO_DATA\"], \"ordinals\": {\"SCHEDULED\": 0, \"SKIPPED\": 1, \"NO_DATA\": 2}, \"doc\": \"The relation between this StopTime and the static schedule.\"}]}], \"doc\": \"Realtime update for arrival and/or departure events for a given stop on a trip. Updates can be supplied for both past and future events. The producer is allowed, although not required, to drop past events.\"}}, \"doc\": \"Updates to StopTimes for the trip (both future, i.e., predictions, and in some cases, past ones, i.e., those that already happened). The updates must be sorted by stop_sequence, and apply for all the following stops of the trip up to the next specified one. Example 1: For a trip with 20 stops, a StopTimeUpdate with arrival delay and departure delay of 0 for stop_sequence of the current stop means that the trip is exactly on time. Example 2: For the same trip instance, 3 StopTimeUpdates are provided: - delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 - delay of unspecified duration for stop_sequence 10 This will be interpreted as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9 have delay of 1 min. - stop_sequences 10,... have unknown delay. Moment at which the vehicle's real-time progress was measured. In POSIX\"}, {\"name\": \"timestamp\", \"type\": [\"null\", \"long\"], \"doc\": \"time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC). The current schedule deviation for the trip.  Delay should only be\"}, {\"name\": \"delay\", \"type\": [\"null\", \"int\"], \"doc\": \"specified when the prediction is given relative to some existing schedule in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time. Delay information in StopTimeUpdates take precedent of trip-level delay information, such that trip-level delay is only propagated until the next stop along the trip with a StopTimeUpdate delay value specified. Feed providers are strongly encouraged to provide a TripUpdate.timestamp value indicating when the delay value was last updated, in order to evaluate the freshness of the data. NOTE: This field is still experimental, and subject to change. It may be formally adopted in the future.\"}], \"doc\": \"Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule. - A trip that proceeds along a route but has no fixed schedule. - A trip that have been added or removed with regard to schedule. The updates can be for future, predicted arrival/departure events, or for past events that already occurred. Normally, updates should get more precise and more certain (see uncertainty below) as the events gets closer to current time. Even if that is not possible, the information for past events should be precise and certain. In particular, if an update points to time in the past but its update's uncertainty is not 0, the client should conclude that the update is a (wrong) prediction and that the trip has not completed yet. Note that the update can describe a trip that is already completed. To this end, it is enough to provide an update for the last stop of the trip. If the time of that is in the past, the client will conclude from that that the whole trip is in the past (it is possible, although inconsequential, to also provide updates for preceding stops). This option is most relevant for a trip that has completed ahead of schedule, but according to the schedule, the trip is still proceeding at the current time. Removing the updates for this trip could make the client assume that the trip is still proceeding. Note that the feed provider is allowed, but not required, to purge past updates - this is one case where this would be practically useful.\"}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        value_trip = self.trip
        self.trip = value_trip if isinstance(value_trip, TripDescriptor) else TripDescriptor.from_serializer_dict(value_trip) if value_trip else None
        self.vehicle=self.vehicle if isinstance(self.vehicle, VehicleDescriptor) else VehicleDescriptor.from_serializer_dict(self.vehicle) if self.vehicle else None if self.vehicle else None
        self.stop_time_update=self.stop_time_update if isinstance(self.stop_time_update, list) else [v if isinstance(v, StopTimeUpdate) else StopTimeUpdate.from_serializer_dict(v) if v else None for v in self.stop_time_update] if self.stop_time_update else None
        self.timestamp=int(self.timestamp) if self.timestamp else None
        self.delay=int(self.delay) if self.delay else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TripUpdate':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TripUpdate']:
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
            return TripUpdate.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return TripUpdate.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')