""" Alert dataclass. """

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
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.effect import Effect
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.translatedstring import TranslatedString
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.timerange import TimeRange
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.entityselector import EntitySelector
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.cause import Cause


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Alert:
    """
    An alert, indicating some sort of incident in the public transit network.
    Attributes:
        active_period (typing.List[TimeRange]): Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them.
        informed_entity (typing.List[EntitySelector]): Entities whose users we should notify of this alert.
        cause (typing.Optional[Cause]): 
        effect (typing.Optional[Effect]): 
        url (typing.Optional[TranslatedString]): The URL which provides additional information about the alert.
        header_text (typing.Optional[TranslatedString]): Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the
        description_text (typing.Optional[TranslatedString]): description should add to the information of the header."""
    
    active_period: typing.List[TimeRange]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="active_period"))
    informed_entity: typing.List[EntitySelector]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="informed_entity"))
    cause: typing.Optional[Cause]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cause"))
    effect: typing.Optional[Effect]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="effect"))
    url: typing.Optional[TranslatedString]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    header_text: typing.Optional[TranslatedString]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="header_text"))
    description_text: typing.Optional[TranslatedString]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description_text"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Alert\", \"namespace\": \"GeneralTransitFeedRealTime.Alert\", \"fields\": [{\"name\": \"active_period\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"TimeRange\", \"namespace\": \"GeneralTransitFeedRealTime.Alert\", \"fields\": [{\"name\": \"start\", \"type\": [\"null\", \"long\"], \"doc\": \"Start time, in POSIX time (i.e., number of seconds since January 1st 1970 00:00:00 UTC). If missing, the interval starts at minus infinity.\"}, {\"name\": \"end\", \"type\": [\"null\", \"long\"], \"doc\": \"End time, in POSIX time (i.e., number of seconds since January 1st 1970 00:00:00 UTC). If missing, the interval ends at plus infinity.\"}], \"doc\": \"Low level data structures used above. A time interval. The interval is considered active at time 't' if 't' is greater than or equal to the start time and less than the end time.\"}}, \"doc\": \"Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them.\"}, {\"name\": \"informed_entity\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"EntitySelector\", \"namespace\": \"GeneralTransitFeedRealTime.Alert\", \"fields\": [{\"name\": \"agency_id\", \"type\": [\"null\", \"string\"], \"doc\": \"The values of the fields should correspond to the appropriate fields in the GTFS feed. At least one specifier must be given. If several are given, then the matching has to apply to all the given specifiers.\"}, {\"name\": \"route_id\", \"type\": [\"null\", \"string\"]}, {\"name\": \"route_type\", \"type\": [\"null\", \"int\"], \"doc\": \"corresponds to route_type in GTFS.\"}, {\"name\": \"trip\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"TripDescriptor\", \"namespace\": \"GeneralTransitFeedRealTime.Alert\", \"fields\": [{\"name\": \"trip_id\", \"type\": [\"null\", \"string\"], \"doc\": \"The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary.\"}, {\"name\": \"route_id\", \"type\": [\"null\", \"string\"], \"doc\": \"The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the\"}, {\"name\": \"direction_id\", \"type\": [\"null\", \"int\"], \"doc\": \"direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future.\"}, {\"name\": \"start_time\", \"type\": [\"null\", \"string\"], \"doc\": \"The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance.\"}, {\"name\": \"start_date\", \"type\": [\"null\", \"string\"], \"doc\": \"Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format.\"}, {\"name\": \"schedule_relationship\", \"type\": [\"null\", {\"name\": \"ScheduleRelationship\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Alert.TripDescriptor_types\", \"symbols\": [\"SCHEDULED\", \"ADDED\", \"UNSCHEDULED\", \"CANCELED\"], \"ordinals\": {\"SCHEDULED\": 0, \"ADDED\": 1, \"UNSCHEDULED\": 2, \"CANCELED\": 3}, \"doc\": \"The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.\"}]}], \"doc\": \"A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary,   start_time) is set. If route_id is also set, then it should be same as one   that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be   set. Note that if the trip_id is not known, then stop sequence ids in   TripUpdate are not sufficient, and stop_ids must be provided as well. In   addition, absolute arrival/departure times must be provided.\"}]}, {\"name\": \"stop_id\", \"type\": [\"null\", \"string\"]}], \"doc\": \"A selector for an entity in a GTFS feed.\"}}, \"doc\": \"Entities whose users we should notify of this alert.\"}, {\"name\": \"cause\", \"type\": [\"null\", {\"name\": \"Cause\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Alert.Alert_types\", \"symbols\": [\"UNKNOWN_CAUSE\", \"OTHER_CAUSE\", \"TECHNICAL_PROBLEM\", \"STRIKE\", \"DEMONSTRATION\", \"ACCIDENT\", \"HOLIDAY\", \"WEATHER\", \"MAINTENANCE\", \"CONSTRUCTION\", \"POLICE_ACTIVITY\", \"MEDICAL_EMERGENCY\"], \"ordinals\": {\"UNKNOWN_CAUSE\": 1, \"OTHER_CAUSE\": 2, \"TECHNICAL_PROBLEM\": 3, \"STRIKE\": 4, \"DEMONSTRATION\": 5, \"ACCIDENT\": 6, \"HOLIDAY\": 7, \"WEATHER\": 8, \"MAINTENANCE\": 9, \"CONSTRUCTION\": 10, \"POLICE_ACTIVITY\": 11, \"MEDICAL_EMERGENCY\": 12}, \"doc\": \"Cause of this alert.\"}]}, {\"name\": \"effect\", \"type\": [\"null\", {\"name\": \"Effect\", \"type\": \"enum\", \"namespace\": \"GeneralTransitFeedRealTime.Alert.Alert_types\", \"symbols\": [\"NO_SERVICE\", \"REDUCED_SERVICE\", \"SIGNIFICANT_DELAYS\", \"DETOUR\", \"ADDITIONAL_SERVICE\", \"MODIFIED_SERVICE\", \"OTHER_EFFECT\", \"UNKNOWN_EFFECT\", \"STOP_MOVED\"], \"ordinals\": {\"NO_SERVICE\": 1, \"REDUCED_SERVICE\": 2, \"SIGNIFICANT_DELAYS\": 3, \"DETOUR\": 4, \"ADDITIONAL_SERVICE\": 5, \"MODIFIED_SERVICE\": 6, \"OTHER_EFFECT\": 7, \"UNKNOWN_EFFECT\": 8, \"STOP_MOVED\": 9}, \"doc\": \"What is the effect of this problem on the affected entity.\"}]}, {\"name\": \"url\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"TranslatedString\", \"namespace\": \"GeneralTransitFeedRealTime.Alert\", \"fields\": [{\"name\": \"translation\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"Translation\", \"namespace\": \"GeneralTransitFeedRealTime.Alert.TranslatedString_types\", \"fields\": [{\"name\": \"text\", \"type\": \"string\", \"doc\": \"A UTF-8 string containing the message.\"}, {\"name\": \"language\", \"type\": [\"null\", \"string\"], \"doc\": \"BCP-47 language code. Can be omitted if the language is unknown or if no i18n is done at all for the feed. At most one translation is allowed to have an unspecified language tag.\"}]}}, \"doc\": \"At least one translation must be provided.\"}], \"doc\": \"An internationalized message containing per-language versions of a snippet of text or a URL. One of the strings from a message will be picked up. The resolution proceeds as follows: 1. If the UI language matches the language code of a translation,    the first matching translation is picked. 2. If a default UI language (e.g., English) matches the language code of a    translation, the first matching translation is picked. 3. If some translation has an unspecified language code, that translation is    picked.\"}], \"doc\": \"The URL which provides additional information about the alert.\"}, {\"name\": \"header_text\", \"type\": [\"null\", \"GeneralTransitFeedRealTime.Alert.TranslatedString\"], \"doc\": \"Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the\"}, {\"name\": \"description_text\", \"type\": [\"null\", \"GeneralTransitFeedRealTime.Alert.TranslatedString\"], \"doc\": \"description should add to the information of the header.\"}], \"doc\": \"An alert, indicating some sort of incident in the public transit network.\"}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.active_period=self.active_period if isinstance(self.active_period, list) else [v if isinstance(v, TimeRange) else TimeRange.from_serializer_dict(v) if v else None for v in self.active_period] if self.active_period else None
        self.informed_entity=self.informed_entity if isinstance(self.informed_entity, list) else [v if isinstance(v, EntitySelector) else EntitySelector.from_serializer_dict(v) if v else None for v in self.informed_entity] if self.informed_entity else None
        self.cause=Cause(self.cause) if self.cause else None
        self.effect=Effect(self.effect) if self.effect else None
        self.url=self.url if isinstance(self.url, TranslatedString) else TranslatedString.from_serializer_dict(self.url) if self.url else None if self.url else None
        self.header_text=self.header_text if isinstance(self.header_text, TranslatedString) else TranslatedString.from_serializer_dict(self.header_text) if self.header_text else None if self.header_text else None
        self.description_text=self.description_text if isinstance(self.description_text, TranslatedString) else TranslatedString.from_serializer_dict(self.description_text) if self.description_text else None if self.description_text else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Alert':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Alert']:
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
            return Alert.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Alert.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')