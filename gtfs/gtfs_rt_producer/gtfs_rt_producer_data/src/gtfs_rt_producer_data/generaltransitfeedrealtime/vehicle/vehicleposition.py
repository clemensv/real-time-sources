""" VehiclePosition dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.occupancystatus import OccupancyStatus
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.position import Position
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.tripdescriptor import TripDescriptor
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.congestionlevel import CongestionLevel
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.vehiclestopstatus import VehicleStopStatus
from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicledescriptor import VehicleDescriptor


@dataclasses_json.dataclass_json
@dataclasses.dataclass
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VehiclePosition']:
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
                return VehiclePosition.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')