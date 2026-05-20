""" EstimatedCall dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class EstimatedCall:
    """
    A single estimated call at a stop within an EstimatedVehicleJourney.
    Attributes:
        stop_point_ref (str): NSR Quay/StopPoint identifier. Example: NSR:Quay:1234.
        order (int): Sequence order of this call, 1-based.
        stop_point_name (typing.Optional[str]): Public stop name.
        aimed_arrival_time (typing.Optional[str]): Timetabled arrival time ISO 8601.
        expected_arrival_time (typing.Optional[str]): Real-time expected arrival time ISO 8601.
        aimed_departure_time (typing.Optional[str]): Timetabled departure time ISO 8601.
        expected_departure_time (typing.Optional[str]): Real-time expected departure time ISO 8601.
        arrival_status (typing.Optional[str]): SIRI ArrivalStatus: onTime, early, delayed, cancelled, arrived, noReport.
        departure_status (typing.Optional[str]): SIRI DepartureStatus: onTime, early, delayed, cancelled, departed, noReport.
        departure_platform_name (typing.Optional[str]): Platform/track identifier for departure.
        arrival_boarding_activity (typing.Optional[str]): SIRI ArrivalBoardingActivity: boarding, noBoarding, passthru.
        departure_boarding_activity (typing.Optional[str]): SIRI DepartureBoardingActivity: boarding, noBoarding, passthru.
        is_cancellation (typing.Optional[bool]): True if this individual stop is cancelled.
        is_extra_stop (typing.Optional[bool]): True if this stop was added."""
    
    stop_point_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop_point_ref"))
    order: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="order"))
    stop_point_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop_point_name"))
    aimed_arrival_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aimed_arrival_time"))
    expected_arrival_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expected_arrival_time"))
    aimed_departure_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aimed_departure_time"))
    expected_departure_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expected_departure_time"))
    arrival_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrival_status"))
    departure_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departure_status"))
    departure_platform_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departure_platform_name"))
    arrival_boarding_activity: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrival_boarding_activity"))
    departure_boarding_activity: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departure_boarding_activity"))
    is_cancellation: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_cancellation"))
    is_extra_stop: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_extra_stop"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"EstimatedCall\", \"namespace\": \"no.entur\", \"doc\": \"A single estimated call at a stop within an EstimatedVehicleJourney.\", \"fields\": [{\"name\": \"stop_point_ref\", \"type\": \"string\", \"doc\": \"NSR Quay/StopPoint identifier. Example: NSR:Quay:1234.\"}, {\"name\": \"order\", \"type\": \"int\", \"doc\": \"Sequence order of this call, 1-based.\"}, {\"name\": \"stop_point_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Public stop name.\"}, {\"name\": \"aimed_arrival_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Timetabled arrival time ISO 8601.\"}, {\"name\": \"expected_arrival_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Real-time expected arrival time ISO 8601.\"}, {\"name\": \"aimed_departure_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Timetabled departure time ISO 8601.\"}, {\"name\": \"expected_departure_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Real-time expected departure time ISO 8601.\"}, {\"name\": \"arrival_status\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"SIRI ArrivalStatus: onTime, early, delayed, cancelled, arrived, noReport.\"}, {\"name\": \"departure_status\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"SIRI DepartureStatus: onTime, early, delayed, cancelled, departed, noReport.\"}, {\"name\": \"departure_platform_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Platform/track identifier for departure.\"}, {\"name\": \"arrival_boarding_activity\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"SIRI ArrivalBoardingActivity: boarding, noBoarding, passthru.\"}, {\"name\": \"departure_boarding_activity\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"SIRI DepartureBoardingActivity: boarding, noBoarding, passthru.\"}, {\"name\": \"is_cancellation\", \"type\": [\"null\", \"boolean\"], \"default\": null, \"doc\": \"True if this individual stop is cancelled.\"}, {\"name\": \"is_extra_stop\", \"type\": [\"null\", \"boolean\"], \"default\": null, \"doc\": \"True if this stop was added.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.stop_point_ref=str(self.stop_point_ref)
        self.order=int(self.order)
        self.stop_point_name=str(self.stop_point_name) if self.stop_point_name else None
        self.aimed_arrival_time=str(self.aimed_arrival_time) if self.aimed_arrival_time else None
        self.expected_arrival_time=str(self.expected_arrival_time) if self.expected_arrival_time else None
        self.aimed_departure_time=str(self.aimed_departure_time) if self.aimed_departure_time else None
        self.expected_departure_time=str(self.expected_departure_time) if self.expected_departure_time else None
        self.arrival_status=str(self.arrival_status) if self.arrival_status else None
        self.departure_status=str(self.departure_status) if self.departure_status else None
        self.departure_platform_name=str(self.departure_platform_name) if self.departure_platform_name else None
        self.arrival_boarding_activity=str(self.arrival_boarding_activity) if self.arrival_boarding_activity else None
        self.departure_boarding_activity=str(self.departure_boarding_activity) if self.departure_boarding_activity else None
        self.is_cancellation=bool(self.is_cancellation) if self.is_cancellation else None
        self.is_extra_stop=bool(self.is_extra_stop) if self.is_extra_stop else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'EstimatedCall':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['EstimatedCall']:
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
            return EstimatedCall.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return EstimatedCall.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')