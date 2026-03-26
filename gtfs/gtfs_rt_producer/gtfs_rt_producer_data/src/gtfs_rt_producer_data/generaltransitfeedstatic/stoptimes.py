""" StopTimes dataclass. """

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
from gtfs_rt_producer_data.generaltransitfeedstatic.timepoint import Timepoint
from gtfs_rt_producer_data.generaltransitfeedstatic.pickuptype import PickupType
from gtfs_rt_producer_data.generaltransitfeedstatic.dropofftype import DropOffType
from gtfs_rt_producer_data.generaltransitfeedstatic.continuouspickup import ContinuousPickup
from gtfs_rt_producer_data.generaltransitfeedstatic.continuousdropoff import ContinuousDropOff


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
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
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"StopTimes\", \"namespace\": \"GeneralTransitFeedStatic\", \"doc\": \"Represents times that a vehicle arrives at and departs from individual stops for each trip.\", \"fields\": [{\"name\": \"tripId\", \"type\": \"string\", \"doc\": \"Identifies a trip.\"}, {\"name\": \"arrivalTime\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Arrival time at the stop for a specific trip.\"}, {\"name\": \"departureTime\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Departure time from the stop for a specific trip.\"}, {\"name\": \"stopId\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Identifies the serviced stop.\"}, {\"name\": \"stopSequence\", \"type\": \"int\", \"doc\": \"Order of stops for a particular trip.\"}, {\"name\": \"stopHeadsign\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Text that appears on signage identifying the trip's destination to riders.\"}, {\"name\": \"pickupType\", \"type\": {\"type\": \"enum\", \"name\": \"PickupType\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"REGULAR\", \"NO_PICKUP\", \"PHONE_AGENCY\", \"COORDINATE_WITH_DRIVER\"], \"doc\": \"Indicates pickup method. Symbols: REGULAR - Regularly scheduled pickup; NO_PICKUP - No pickup available; PHONE_AGENCY - Must phone agency to arrange pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange pickup.\"}, \"doc\": \"Indicates pickup method.\"}, {\"name\": \"dropOffType\", \"type\": {\"type\": \"enum\", \"name\": \"DropOffType\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"REGULAR\", \"NO_DROP_OFF\", \"PHONE_AGENCY\", \"COORDINATE_WITH_DRIVER\"], \"doc\": \"Indicates drop off method. Symbols: REGULAR - Regularly scheduled drop off; NO_DROP_OFF - No drop off available; PHONE_AGENCY - Must phone agency to arrange drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange drop off.\"}, \"doc\": \"Indicates drop off method.\"}, {\"name\": \"continuousPickup\", \"type\": [\"null\", {\"type\": \"enum\", \"name\": \"ContinuousPickup\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"CONTINUOUS_STOPPING\", \"NO_CONTINUOUS_STOPPING\", \"PHONE_AGENCY\", \"COORDINATE_WITH_DRIVER\"], \"doc\": \"Indicates that the rider can board the transit vehicle at any point along the vehicle\u2019s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping pickup; NO_CONTINUOUS_STOPPING - No continuous stopping pickup; PHONE_AGENCY - Must phone agency to arrange continuous stopping pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping pickup.\"}], \"default\": null, \"doc\": \"Indicates continuous stopping pickup.\"}, {\"name\": \"continuousDropOff\", \"type\": [\"null\", {\"type\": \"enum\", \"name\": \"ContinuousDropOff\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"CONTINUOUS_STOPPING\", \"NO_CONTINUOUS_STOPPING\", \"PHONE_AGENCY\", \"COORDINATE_WITH_DRIVER\"], \"doc\": \"Indicates that the rider can alight from the transit vehicle at any point along the vehicle\u2019s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping drop off; NO_CONTINUOUS_STOPPING - No continuous stopping drop off; PHONE_AGENCY - Must phone agency to arrange continuous stopping drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping drop off.\"}], \"default\": null, \"doc\": \"Indicates continuous stopping drop off.\"}, {\"name\": \"shapeDistTraveled\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Actual distance traveled along the shape from the first stop to the stop specified in this record.\"}, {\"name\": \"timepoint\", \"type\": {\"type\": \"enum\", \"name\": \"Timepoint\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"APPROXIMATE\", \"EXACT\"], \"doc\": \"Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times. Symbols: APPROXIMATE - Times are considered approximate; EXACT - Times are considered exact.\"}, \"doc\": \"Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times.\"}]}"), avro.name.Names()
    )

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['StopTimes']:
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
            return StopTimes.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return StopTimes.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')