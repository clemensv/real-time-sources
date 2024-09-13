""" TripUpdate dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate import StopTimeUpdate
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripdescriptor import TripDescriptor
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.vehicledescriptor import VehicleDescriptor


@dataclasses_json.dataclass_json
@dataclasses.dataclass
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
                    'application/json': Encodes the data to JSON format.
                Supported content type extensions:
                    '+gzip': Compresses the byte array using gzip, e.g. 'application/json+gzip'.

        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        result = None
        if content_type == 'application/json':
            result = self.to_json()

        if result is not None and content_type.endswith('+gzip'):
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
        if content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return TripUpdate.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')