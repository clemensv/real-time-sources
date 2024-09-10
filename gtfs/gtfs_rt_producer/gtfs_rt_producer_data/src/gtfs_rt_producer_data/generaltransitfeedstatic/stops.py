""" Stops dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedstatic.wheelchairboarding import WheelchairBoarding
from gtfs_rt_producer_data.generaltransitfeedstatic.locationtype import LocationType


@dataclasses_json.dataclass_json
@dataclasses.dataclass
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Stops']:
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
                return Stops.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')