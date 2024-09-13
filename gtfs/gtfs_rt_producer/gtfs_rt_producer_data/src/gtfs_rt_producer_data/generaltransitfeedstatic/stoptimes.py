""" StopTimes dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedstatic.pickuptype import PickupType
from gtfs_rt_producer_data.generaltransitfeedstatic.continuouspickup import ContinuousPickup
from gtfs_rt_producer_data.generaltransitfeedstatic.dropofftype import DropOffType
from gtfs_rt_producer_data.generaltransitfeedstatic.timepoint import Timepoint
from gtfs_rt_producer_data.generaltransitfeedstatic.continuousdropoff import ContinuousDropOff


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class StopTimes:
    """
    Represents times that a vehicle arrives at and departs from individual stops for each trip.
    Attributes:
        tripId (str): Identifies a trip.
        arrivalTime (typing.Optional[str]): Arrival time at the stop for a specific trip.
        departureTime (typing.Optional[str]): Departure time from the stop for a specific trip.
        stopId (typing.Optional[str]): Identifies the serviced stop.
        stopSequence (int): Order of stops for a particular trip.
        stopHeadsign (typing.Optional[str]): Text that appears on signage identifying the trip's destination to riders.
        pickupType (PickupType): Indicates pickup method.
        dropOffType (DropOffType): Indicates drop off method.
        continuousPickup (typing.Optional[ContinuousPickup]): Indicates continuous stopping pickup.
        continuousDropOff (typing.Optional[ContinuousDropOff]): Indicates continuous stopping drop off.
        shapeDistTraveled (typing.Optional[float]): Actual distance traveled along the shape from the first stop to the stop specified in this record.
        timepoint (Timepoint): Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times."""
    
    tripId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tripId"))
    arrivalTime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrivalTime"))
    departureTime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departureTime"))
    stopId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopId"))
    stopSequence: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopSequence"))
    stopHeadsign: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopHeadsign"))
    pickupType: PickupType=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pickupType"))
    dropOffType: DropOffType=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dropOffType"))
    continuousPickup: typing.Optional[ContinuousPickup]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="continuousPickup"))
    continuousDropOff: typing.Optional[ContinuousDropOff]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="continuousDropOff"))
    shapeDistTraveled: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="shapeDistTraveled"))
    timepoint: Timepoint=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timepoint"))    
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.tripId=str(self.tripId)
        self.arrivalTime=str(self.arrivalTime) if self.arrivalTime else None
        self.departureTime=str(self.departureTime) if self.departureTime else None
        self.stopId=str(self.stopId) if self.stopId else None
        self.stopSequence=int(self.stopSequence)
        self.stopHeadsign=str(self.stopHeadsign) if self.stopHeadsign else None
        self.pickupType=PickupType(self.pickupType)
        self.dropOffType=DropOffType(self.dropOffType)
        self.continuousPickup=ContinuousPickup(self.continuousPickup) if self.continuousPickup else None
        self.continuousDropOff=ContinuousDropOff(self.continuousDropOff) if self.continuousDropOff else None
        self.shapeDistTraveled=float(self.shapeDistTraveled) if self.shapeDistTraveled else None
        self.timepoint=Timepoint(self.timepoint)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'StopTimes':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['StopTimes']:
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
                return StopTimes.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')