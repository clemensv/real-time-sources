""" Record dataclass. """

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
class Record:
    """
    Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.
    Attributes:
        icao24 (str): ICAO 24-bit address (lowercase hex).
        receiver_id (str): Stable identifier of the receiver/station that decoded this message.
        msg_type (str): Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).
        ts (int): Reception timestamp (epoch millis).
        df (int): Downlink Format value.
        tc (typing.Optional[int]): Type Code (ADS-B only).
        bcode (typing.Optional[str]): BDS code (Comm-B only).
        alt (typing.Optional[int]): Barometric altitude (ft).
        cs (typing.Optional[str]): Aircraft callsign.
        sq (typing.Optional[str]): Squawk code.
        lat (typing.Optional[float]): Latitude (deg).
        lon (typing.Optional[float]): Longitude (deg).
        spd (typing.Optional[float]): Speed (kn).
        ang (typing.Optional[float]): Heading angle (deg).
        vr (typing.Optional[int]): Vertical rate (ft/min).
        rssi (typing.Optional[float]): RSSI (dBFS)."""
    
    icao24: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icao24"))
    receiver_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="receiver_id"))
    msg_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="msg_type"))
    ts: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ts"))
    df: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="df"))
    tc: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tc"))
    bcode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bcode"))
    alt: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt"))
    cs: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cs"))
    sq: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sq"))
    lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat"))
    lon: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lon"))
    spd: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="spd"))
    ang: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ang"))
    vr: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vr"))
    rssi: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rssi"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Record\", \"namespace\": \"Mode_S\", \"doc\": \"Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.\", \"fields\": [{\"name\": \"icao24\", \"type\": \"string\", \"doc\": \"ICAO 24-bit address (lowercase hex).\"}, {\"name\": \"receiver_id\", \"type\": \"string\", \"doc\": \"Stable identifier of the receiver/station that decoded this message.\"}, {\"name\": \"msg_type\", \"type\": \"string\", \"doc\": \"Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).\"}, {\"name\": \"ts\", \"type\": \"long\", \"doc\": \"Reception timestamp (epoch millis).\"}, {\"name\": \"df\", \"type\": \"int\", \"doc\": \"Downlink Format value.\"}, {\"name\": \"tc\", \"type\": [\"null\", \"int\"], \"doc\": \"Type Code (ADS-B only).\", \"default\": null}, {\"name\": \"bcode\", \"type\": [\"null\", \"string\"], \"doc\": \"BDS code (Comm-B only).\", \"default\": null}, {\"name\": \"alt\", \"type\": [\"null\", \"int\"], \"doc\": \"Barometric altitude (ft).\", \"default\": null}, {\"name\": \"cs\", \"type\": [\"null\", \"string\"], \"doc\": \"Aircraft callsign.\", \"default\": null}, {\"name\": \"sq\", \"type\": [\"null\", \"string\"], \"doc\": \"Squawk code.\", \"default\": null}, {\"name\": \"lat\", \"type\": [\"null\", \"double\"], \"doc\": \"Latitude (deg).\", \"default\": null}, {\"name\": \"lon\", \"type\": [\"null\", \"double\"], \"doc\": \"Longitude (deg).\", \"default\": null}, {\"name\": \"spd\", \"type\": [\"null\", \"float\"], \"doc\": \"Speed (kn).\", \"default\": null}, {\"name\": \"ang\", \"type\": [\"null\", \"float\"], \"doc\": \"Heading angle (deg).\", \"default\": null}, {\"name\": \"vr\", \"type\": [\"null\", \"int\"], \"doc\": \"Vertical rate (ft/min).\", \"default\": null}, {\"name\": \"rssi\", \"type\": [\"null\", \"float\"], \"doc\": \"RSSI (dBFS).\", \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.icao24=str(self.icao24)
        self.receiver_id=str(self.receiver_id)
        self.msg_type=str(self.msg_type)
        self.ts=int(self.ts)
        self.df=int(self.df)
        self.tc=int(self.tc) if self.tc else None
        self.bcode=str(self.bcode) if self.bcode else None
        self.alt=int(self.alt) if self.alt else None
        self.cs=str(self.cs) if self.cs else None
        self.sq=str(self.sq) if self.sq else None
        self.lat=float(self.lat) if self.lat else None
        self.lon=float(self.lon) if self.lon else None
        self.spd=float(self.spd) if self.spd else None
        self.ang=float(self.ang) if self.ang else None
        self.vr=int(self.vr) if self.vr else None
        self.rssi=float(self.rssi) if self.rssi else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Record':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Record']:
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
            return Record.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Record.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')