""" Trips dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedstatic.calendardates import CalendarDates
from gtfs_rt_producer_data.generaltransitfeedstatic.calendar import Calendar
from gtfs_rt_producer_data.generaltransitfeedstatic.wheelchairaccessible import WheelchairAccessible
from gtfs_rt_producer_data.generaltransitfeedstatic.directionid import DirectionId
from gtfs_rt_producer_data.generaltransitfeedstatic.bikesallowed import BikesAllowed


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Trips:
    """
    Identifies a trip.
    Attributes:
        routeId (str): Identifies a route.
        serviceDates (Calendar): 
        serviceExceptions (typing.List[CalendarDates]): 
        tripId (str): Identifies a trip.
        tripHeadsign (typing.Optional[str]): Text that appears on signage identifying the trip's destination to riders.
        tripShortName (typing.Optional[str]): Public facing text used to identify the trip to riders.
        directionId (DirectionId): Indicates the direction of travel for a trip.
        blockId (typing.Optional[str]): Identifies the block to which the trip belongs.
        shapeId (typing.Optional[str]): Identifies a geospatial shape describing the vehicle travel path for a trip.
        wheelchairAccessible (WheelchairAccessible): Indicates wheelchair accessibility.
        bikesAllowed (BikesAllowed): Indicates whether bikes are allowed."""
    
    routeId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeId"))
    serviceDates: Calendar=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="serviceDates"))
    serviceExceptions: typing.List[CalendarDates]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="serviceExceptions"))
    tripId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tripId"))
    tripHeadsign: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tripHeadsign"))
    tripShortName: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tripShortName"))
    directionId: DirectionId=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="directionId"))
    blockId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="blockId"))
    shapeId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="shapeId"))
    wheelchairAccessible: WheelchairAccessible=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wheelchairAccessible"))
    bikesAllowed: BikesAllowed=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bikesAllowed"))
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.routeId=str(self.routeId)
        value_serviceDates = self.serviceDates
        self.serviceDates = value_serviceDates if isinstance(value_serviceDates, Calendar) else Calendar.from_serializer_dict(value_serviceDates) if value_serviceDates else None
        self.serviceExceptions=self.serviceExceptions if isinstance(self.serviceExceptions, list) else [v if isinstance(v, CalendarDates) else CalendarDates.from_serializer_dict(v) if v else None for v in self.serviceExceptions] if self.serviceExceptions else None
        self.tripId=str(self.tripId)
        self.tripHeadsign=str(self.tripHeadsign) if self.tripHeadsign else None
        self.tripShortName=str(self.tripShortName) if self.tripShortName else None
        self.directionId=DirectionId(self.directionId)
        self.blockId=str(self.blockId) if self.blockId else None
        self.shapeId=str(self.shapeId) if self.shapeId else None
        self.wheelchairAccessible=WheelchairAccessible(self.wheelchairAccessible)
        self.bikesAllowed=BikesAllowed(self.bikesAllowed)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Trips':
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
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member

        if result is not None and content_type.endswith('+gzip'):
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Trips']:
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
                return Trips.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')