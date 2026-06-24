""" TripUpdate dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
from __future__ import annotations
import io
import gzip
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import json
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate import StopTimeUpdate
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.trip.tripdescriptor import TripDescriptor
from gtfs_mqtt_producer_data.generaltransitfeedrealtime.trip.vehicledescriptor import VehicleDescriptor


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TripUpdate:
    """
    Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule. - A trip that proceeds along a route but has no fixed schedule. - A trip that have been added or removed with regard to schedule. The updates can be for future, predicted arrival/departure events, or for past events that already occurred. Normally, updates should get more precise and more certain (see uncertainty below) as the events gets closer to current time. Even if that is not possible, the information for past events should be precise and certain. In particular, if an update points to time in the past but its update's uncertainty is not 0, the client should conclude that the update is a (wrong) prediction and that the trip has not completed yet. Note that the update can describe a trip that is already completed. To this end, it is enough to provide an update for the last stop of the trip. If the time of that is in the past, the client will conclude from that that the whole trip is in the past (it is possible, although inconsequential, to also provide updates for preceding stops). This option is most relevant for a trip that has completed ahead of schedule, but according to the schedule, the trip is still proceeding at the current time. Removing the updates for this trip could make the client assume that the trip is still proceeding. Note that the feed provider is allowed, but not required, to purge past updates - this is one case where this would be practically useful.
    
    Attributes:
        trip (TripDescriptor)
        vehicle (typing.Optional[VehicleDescriptor])
        stop_time_update (typing.List[StopTimeUpdate])
        timestamp (typing.Optional[int])
        delay (typing.Optional[int])
    """
    
    
    trip: TripDescriptor=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trip"))
    vehicle: typing.Optional[VehicleDescriptor]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle"))
    stop_time_update: typing.List[StopTimeUpdate]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop_time_update"))
    timestamp: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TripUpdate':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = int(data['timestamp'])
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        if 'timestamp' in asdict_result and asdict_result['timestamp'] is not None:
            asdict_result['timestamp'] = str(asdict_result['timestamp'])
        return asdict_result

    def _dict_resolver(self, data):
        """
        Helps resolving the Enum values to their actual values and fixes the key names.
        """ 
        def _resolve_enum(v):
            if isinstance(v, enum.Enum):
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
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member
            if isinstance(result, str):
                result = result.encode('utf-8')

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
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return TripUpdate.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'TripUpdate':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            trip=None,
            vehicle=None,
            stop_time_update=[None, None, None],
            timestamp=int(51),
            delay=int(90)
        )