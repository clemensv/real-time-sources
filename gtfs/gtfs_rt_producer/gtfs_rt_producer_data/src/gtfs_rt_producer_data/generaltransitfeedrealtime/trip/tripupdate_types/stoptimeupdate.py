""" StopTimeUpdate dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate_types.schedulerelationship import ScheduleRelationship
from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeevent import StopTimeEvent


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class StopTimeUpdate:
    """
    Realtime update for arrival and/or departure events for a given stop on a trip. Updates can be supplied for both past and future events. The producer is allowed, although not required, to drop past events.
    Attributes:
        stop_sequence (typing.Optional[int]): The update is linked to a specific stop either through stop_sequence or stop_id, so one of the fields below must necessarily be set. See the documentation in TripDescriptor for more information. Must be the same as in stop_times.txt in the corresponding GTFS feed.
        stop_id (typing.Optional[str]): Must be the same as in stops.txt in the corresponding GTFS feed.
        arrival (typing.Optional[StopTimeEvent]): 
        departure (typing.Optional[StopTimeEvent]): 
        schedule_relationship (typing.Optional[ScheduleRelationship]): """
    
    stop_sequence: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop_sequence"))
    stop_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop_id"))
    arrival: typing.Optional[StopTimeEvent]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrival"))
    departure: typing.Optional[StopTimeEvent]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departure"))
    schedule_relationship: typing.Optional[ScheduleRelationship]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="schedule_relationship"))    
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.stop_sequence=int(self.stop_sequence) if self.stop_sequence else None
        self.stop_id=str(self.stop_id) if self.stop_id else None
        self.arrival=self.arrival if isinstance(self.arrival, StopTimeEvent) else StopTimeEvent.from_serializer_dict(self.arrival) if self.arrival else None if self.arrival else None
        self.departure=self.departure if isinstance(self.departure, StopTimeEvent) else StopTimeEvent.from_serializer_dict(self.departure) if self.departure else None if self.departure else None
        self.schedule_relationship=ScheduleRelationship(self.schedule_relationship) if self.schedule_relationship else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'StopTimeUpdate':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['StopTimeUpdate']:
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
                return StopTimeUpdate.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')