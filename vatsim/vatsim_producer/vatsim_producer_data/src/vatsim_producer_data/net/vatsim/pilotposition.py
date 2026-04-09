""" PilotPosition dataclass. """

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
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PilotPosition:
    """
    Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network.
    Attributes:
        cid (int): VATSIM Certificate Identifier (CID) — unique numeric member ID.
        callsign (str): ATC-style callsign chosen by the pilot for this session.
        latitude (float): Aircraft latitude in decimal degrees (WGS-84).
        longitude (float): Aircraft longitude in decimal degrees (WGS-84).
        altitude (int): Indicated altitude in feet above mean sea level.
        groundspeed (int): Ground speed in knots.
        heading (int): Magnetic heading in degrees (0-359).
        transponder (str): Four-digit transponder (squawk) code.
        qnh_mb (int): Altimeter setting (QNH) in millibars.
        flight_rules (typing.Optional[str]): Flight rules: I or V. Null if no flight plan.
        aircraft_short (typing.Optional[str]): ICAO aircraft type designator. Null if no flight plan.
        departure (typing.Optional[str]): ICAO departure airport code. Null if no flight plan.
        arrival (typing.Optional[str]): ICAO arrival airport code. Null if no flight plan.
        route (typing.Optional[str]): Route string from flight plan. Null if no flight plan.
        cruise_altitude (typing.Optional[str]): Planned cruise altitude. Null if no flight plan.
        pilot_rating (int): VATSIM pilot rating bitmask.
        last_updated (datetime.datetime): UTC timestamp of last position update."""
    
    cid: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cid"))
    callsign: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="callsign"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    altitude: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude"))
    groundspeed: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="groundspeed"))
    heading: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="heading"))
    transponder: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="transponder"))
    qnh_mb: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="qnh_mb"))
    flight_rules: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="flight_rules"))
    aircraft_short: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aircraft_short"))
    departure: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="departure"))
    arrival: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrival"))
    route: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route"))
    cruise_altitude: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cruise_altitude"))
    pilot_rating: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pilot_rating"))
    last_updated: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="last_updated"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"PilotPosition\", \"namespace\": \"net.vatsim\", \"doc\": \"Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network.\", \"fields\": [{\"name\": \"cid\", \"type\": \"int\", \"doc\": \"VATSIM Certificate Identifier (CID) \u2014 unique numeric member ID.\"}, {\"name\": \"callsign\", \"type\": \"string\", \"doc\": \"ATC-style callsign chosen by the pilot for this session.\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"Aircraft latitude in decimal degrees (WGS-84).\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"Aircraft longitude in decimal degrees (WGS-84).\"}, {\"name\": \"altitude\", \"type\": \"int\", \"doc\": \"Indicated altitude in feet above mean sea level.\"}, {\"name\": \"groundspeed\", \"type\": \"int\", \"doc\": \"Ground speed in knots.\"}, {\"name\": \"heading\", \"type\": \"int\", \"doc\": \"Magnetic heading in degrees (0-359).\"}, {\"name\": \"transponder\", \"type\": \"string\", \"doc\": \"Four-digit transponder (squawk) code.\"}, {\"name\": \"qnh_mb\", \"type\": \"int\", \"doc\": \"Altimeter setting (QNH) in millibars.\"}, {\"name\": \"flight_rules\", \"type\": [\"null\", \"string\"], \"doc\": \"Flight rules: I or V. Null if no flight plan.\", \"default\": null}, {\"name\": \"aircraft_short\", \"type\": [\"null\", \"string\"], \"doc\": \"ICAO aircraft type designator. Null if no flight plan.\", \"default\": null}, {\"name\": \"departure\", \"type\": [\"null\", \"string\"], \"doc\": \"ICAO departure airport code. Null if no flight plan.\", \"default\": null}, {\"name\": \"arrival\", \"type\": [\"null\", \"string\"], \"doc\": \"ICAO arrival airport code. Null if no flight plan.\", \"default\": null}, {\"name\": \"route\", \"type\": [\"null\", \"string\"], \"doc\": \"Route string from flight plan. Null if no flight plan.\", \"default\": null}, {\"name\": \"cruise_altitude\", \"type\": [\"null\", \"string\"], \"doc\": \"Planned cruise altitude. Null if no flight plan.\", \"default\": null}, {\"name\": \"pilot_rating\", \"type\": \"int\", \"doc\": \"VATSIM pilot rating bitmask.\"}, {\"name\": \"last_updated\", \"type\": {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"UTC timestamp of last position update.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.cid=int(self.cid)
        self.callsign=str(self.callsign)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.altitude=int(self.altitude)
        self.groundspeed=int(self.groundspeed)
        self.heading=int(self.heading)
        self.transponder=str(self.transponder)
        self.qnh_mb=int(self.qnh_mb)
        self.flight_rules=str(self.flight_rules) if self.flight_rules else None
        self.aircraft_short=str(self.aircraft_short) if self.aircraft_short else None
        self.departure=str(self.departure) if self.departure else None
        self.arrival=str(self.arrival) if self.arrival else None
        self.route=str(self.route) if self.route else None
        self.cruise_altitude=str(self.cruise_altitude) if self.cruise_altitude else None
        self.pilot_rating=int(self.pilot_rating)
        value_last_updated = self.last_updated
        self.last_updated = value_last_updated

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PilotPosition':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PilotPosition']:
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
            return PilotPosition.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return PilotPosition.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')