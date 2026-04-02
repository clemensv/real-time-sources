""" Trips dataclass. """

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
from gtfs_rt_producer_data.generaltransitfeedstatic.wheelchairaccessible import WheelchairAccessible
from gtfs_rt_producer_data.generaltransitfeedstatic.calendardates import CalendarDates
from gtfs_rt_producer_data.generaltransitfeedstatic.bikesallowed import BikesAllowed
from gtfs_rt_producer_data.generaltransitfeedstatic.directionid import DirectionId
from gtfs_rt_producer_data.generaltransitfeedstatic.calendar import Calendar


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
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
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Trips\", \"namespace\": \"GeneralTransitFeedStatic\", \"doc\": \"Identifies a trip.\", \"fields\": [{\"name\": \"routeId\", \"type\": \"string\", \"doc\": \"Identifies a route.\"}, {\"name\": \"serviceDates\", \"type\": {\"type\": \"record\", \"name\": \"Calendar\", \"fields\": [{\"name\": \"serviceId\", \"type\": \"string\", \"doc\": \"Identifies a set of dates when service is available for one or more routes.\"}, {\"name\": \"monday\", \"type\": {\"type\": \"enum\", \"name\": \"ServiceAvailability\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"NO_SERVICE\", \"SERVICE_AVAILABLE\"], \"doc\": \"Indicates whether the service operates on all Mondays in the date range specified. Symbols: NO_SERVICE - Service is not available; SERVICE_AVAILABLE - Service is available.\"}, \"doc\": \"Indicates whether the service operates on all Mondays in the date range specified.\"}, {\"name\": \"tuesday\", \"type\": \"GeneralTransitFeedStatic.ServiceAvailability\", \"doc\": \"Indicates whether the service operates on all Tuesdays in the date range specified.\"}, {\"name\": \"wednesday\", \"type\": \"GeneralTransitFeedStatic.ServiceAvailability\", \"doc\": \"Indicates whether the service operates on all Wednesdays in the date range specified.\"}, {\"name\": \"thursday\", \"type\": \"GeneralTransitFeedStatic.ServiceAvailability\", \"doc\": \"Indicates whether the service operates on all Thursdays in the date range specified.\"}, {\"name\": \"friday\", \"type\": \"GeneralTransitFeedStatic.ServiceAvailability\", \"doc\": \"Indicates whether the service operates on all Fridays in the date range specified.\"}, {\"name\": \"saturday\", \"type\": \"GeneralTransitFeedStatic.ServiceAvailability\", \"doc\": \"Indicates whether the service operates on all Saturdays in the date range specified.\"}, {\"name\": \"sunday\", \"type\": \"GeneralTransitFeedStatic.ServiceAvailability\", \"doc\": \"Indicates whether the service operates on all Sundays in the date range specified.\"}, {\"name\": \"startDate\", \"type\": \"string\", \"doc\": \"Start service day for the service interval.\"}, {\"name\": \"endDate\", \"type\": \"string\", \"doc\": \"End service day for the service interval.\"}]}}, {\"name\": \"serviceExceptions\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"CalendarDates\", \"fields\": [{\"name\": \"serviceId\", \"type\": \"string\", \"doc\": \"Identifies a set of dates when a service exception occurs for one or more routes.\"}, {\"name\": \"date\", \"type\": \"string\", \"doc\": \"Date when service exception occurs.\"}, {\"name\": \"exceptionType\", \"type\": {\"type\": \"enum\", \"name\": \"ExceptionType\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"SERVICE_ADDED\", \"SERVICE_REMOVED\"], \"doc\": \"Indicates whether service is available on the date specified. Symbols: SERVICE_ADDED - Service has been added for the specified date; SERVICE_REMOVED - Service has been removed for the specified date.\"}, \"doc\": \"Indicates whether service is available on the date specified.\"}]}, \"doc\": \"Identifies a set of dates when a service exception occurs for one or more routes.\"}}, {\"name\": \"tripId\", \"type\": \"string\", \"doc\": \"Identifies a trip.\"}, {\"name\": \"tripHeadsign\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Text that appears on signage identifying the trip's destination to riders.\"}, {\"name\": \"tripShortName\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Public facing text used to identify the trip to riders.\"}, {\"name\": \"directionId\", \"type\": {\"type\": \"enum\", \"name\": \"DirectionId\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"OUTBOUND\", \"INBOUND\"], \"doc\": \"Indicates the direction of travel for a trip. Symbols: OUTBOUND - Travel in one direction; INBOUND - Travel in the opposite direction.\"}, \"doc\": \"Indicates the direction of travel for a trip.\"}, {\"name\": \"blockId\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Identifies the block to which the trip belongs.\"}, {\"name\": \"shapeId\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Identifies a geospatial shape describing the vehicle travel path for a trip.\"}, {\"name\": \"wheelchairAccessible\", \"type\": {\"type\": \"enum\", \"name\": \"WheelchairAccessible\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"NO_INFO\", \"WHEELCHAIR_ACCESSIBLE\", \"NOT_WHEELCHAIR_ACCESSIBLE\"], \"doc\": \"Indicates wheelchair accessibility. Symbols: NO_INFO - No accessibility information for the trip; WHEELCHAIR_ACCESSIBLE - Vehicle can accommodate at least one rider in a wheelchair; NOT_WHEELCHAIR_ACCESSIBLE - No riders in wheelchairs can be accommodated on this trip.\"}, \"doc\": \"Indicates wheelchair accessibility.\"}, {\"name\": \"bikesAllowed\", \"type\": {\"type\": \"enum\", \"name\": \"BikesAllowed\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"NO_INFO\", \"BICYCLE_ALLOWED\", \"BICYCLE_NOT_ALLOWED\"], \"doc\": \"Indicates whether bikes are allowed. Symbols: NO_INFO - No bike information for the trip; BICYCLE_ALLOWED - Vehicle can accommodate at least one bicycle; BICYCLE_NOT_ALLOWED - No bicycles are allowed on this trip.\"}, \"doc\": \"Indicates whether bikes are allowed.\"}]}"), avro.name.Names()
    )

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Trips']:
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
            return Trips.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Trips.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')