""" Stops dataclass. """

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
from gtfs_rt_producer_data.generaltransitfeedstatic.wheelchairboarding import WheelchairBoarding
from gtfs_rt_producer_data.generaltransitfeedstatic.locationtype import LocationType


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Stops:
    """
    Identifies locations such as stop/platform, station, entrance/exit, generic node or boarding area.
    Attributes:
        stopId (str): Identifies a location: stop/platform, station, entrance/exit, generic node or boarding area.
        stopCode (typing.Optional[str]): Short text or a number that identifies the location for riders.
        stopName (typing.Optional[str]): Name of the location.
        ttsStopName (typing.Optional[str]): Readable version of the stop_name.
        stopDesc (typing.Optional[str]): Description of the location that provides useful, quality information.
        stopLat (typing.Optional[float]): Latitude of the location.
        stopLon (typing.Optional[float]): Longitude of the location.
        zoneId (typing.Optional[str]): Identifies the fare zone for a stop.
        stopUrl (typing.Optional[str]): URL of a web page about the location.
        locationType (LocationType): Location type.
        parentStation (typing.Optional[str]): Defines hierarchy between the different locations.
        stopTimezone (typing.Optional[str]): Timezone of the location.
        wheelchairBoarding (WheelchairBoarding): Indicates whether wheelchair boardings are possible from the location.
        levelId (typing.Optional[str]): Level of the location.
        platformCode (typing.Optional[str]): Platform identifier for a platform stop."""
    
    stopId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopId"))
    stopCode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopCode"))
    stopName: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopName"))
    ttsStopName: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ttsStopName"))
    stopDesc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopDesc"))
    stopLat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopLat"))
    stopLon: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopLon"))
    zoneId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="zoneId"))
    stopUrl: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopUrl"))
    locationType: LocationType=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="locationType"))
    parentStation: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parentStation"))
    stopTimezone: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stopTimezone"))
    wheelchairBoarding: WheelchairBoarding=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wheelchairBoarding"))
    levelId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="levelId"))
    platformCode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="platformCode"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Stops\", \"namespace\": \"GeneralTransitFeedStatic\", \"doc\": \"Identifies locations such as stop/platform, station, entrance/exit, generic node or boarding area.\", \"fields\": [{\"name\": \"stopId\", \"type\": \"string\", \"doc\": \"Identifies a location: stop/platform, station, entrance/exit, generic node or boarding area.\"}, {\"name\": \"stopCode\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Short text or a number that identifies the location for riders.\"}, {\"name\": \"stopName\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Name of the location.\"}, {\"name\": \"ttsStopName\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Readable version of the stop_name.\"}, {\"name\": \"stopDesc\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Description of the location that provides useful, quality information.\"}, {\"name\": \"stopLat\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Latitude of the location.\"}, {\"name\": \"stopLon\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Longitude of the location.\"}, {\"name\": \"zoneId\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Identifies the fare zone for a stop.\"}, {\"name\": \"stopUrl\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"URL of a web page about the location.\"}, {\"name\": \"locationType\", \"type\": {\"type\": \"enum\", \"name\": \"LocationType\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"STOP\", \"STATION\", \"ENTRANCE_EXIT\", \"GENERIC_NODE\", \"BOARDING_AREA\"], \"doc\": \"Location type. Symbols: STOP - Stop or platform; STATION - Physical structure or area that contains one or more platforms; ENTRANCE_EXIT - Location where passengers can enter or exit a station; GENERIC_NODE - Location within a station used to link pathways; BOARDING_AREA - Specific location on a platform where passengers can board and/or alight vehicles.\"}, \"doc\": \"Location type.\"}, {\"name\": \"parentStation\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Defines hierarchy between the different locations.\"}, {\"name\": \"stopTimezone\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Timezone of the location.\"}, {\"name\": \"wheelchairBoarding\", \"type\": {\"type\": \"enum\", \"name\": \"WheelchairBoarding\", \"namespace\": \"GeneralTransitFeedStatic\", \"symbols\": [\"NO_INFO\", \"SOME_VEHICLES\", \"NOT_POSSIBLE\"], \"doc\": \"Indicates whether wheelchair boardings are possible from the location. Symbols: NO_INFO - No accessibility information; SOME_VEHICLES - Some vehicles at this stop can be boarded by a rider in a wheelchair; NOT_POSSIBLE - Wheelchair boarding is not possible at this stop.\"}, \"doc\": \"Indicates whether wheelchair boardings are possible from the location.\"}, {\"name\": \"levelId\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Level of the location.\"}, {\"name\": \"platformCode\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Platform identifier for a platform stop.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.stopId=str(self.stopId)
        self.stopCode=str(self.stopCode) if self.stopCode else None
        self.stopName=str(self.stopName) if self.stopName else None
        self.ttsStopName=str(self.ttsStopName) if self.ttsStopName else None
        self.stopDesc=str(self.stopDesc) if self.stopDesc else None
        self.stopLat=float(self.stopLat) if self.stopLat else None
        self.stopLon=float(self.stopLon) if self.stopLon else None
        self.zoneId=str(self.zoneId) if self.zoneId else None
        self.stopUrl=str(self.stopUrl) if self.stopUrl else None
        self.locationType=LocationType(self.locationType)
        self.parentStation=str(self.parentStation) if self.parentStation else None
        self.stopTimezone=str(self.stopTimezone) if self.stopTimezone else None
        self.wheelchairBoarding=WheelchairBoarding(self.wheelchairBoarding)
        self.levelId=str(self.levelId) if self.levelId else None
        self.platformCode=str(self.platformCode) if self.platformCode else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Stops':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Stops']:
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
            return Stops.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Stops.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')