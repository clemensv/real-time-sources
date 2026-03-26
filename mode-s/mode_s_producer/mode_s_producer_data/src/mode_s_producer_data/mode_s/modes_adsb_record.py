""" ModeS_ADSB_Record dataclass. """

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
class ModeS_ADSB_Record:
    """
    A comprehensive schema for Mode-S and ADS-B decoded messages, including fields for various BDS codes and ADS-B type codes.
    Attributes:
        ts (datetime.datetime): The timestamp of the message reception in milliseconds since the epoch. Required.
        icao (str): The ICAO 24-bit address of the aircraft. Required.
        df (int): The Downlink Format (DF) of the Mode-S message, indicating the message category. Required.
        tc (typing.Optional[int]): The Type Code (TC) of the ADS-B message. Present for DF17 and DF18 messages; null otherwise.
        bcode (typing.Optional[str]): The BDS (Comm-B Data Selector) code. Present for DF20 and DF21 messages; null otherwise.
        alt (typing.Optional[int]): Barometric altitude in feet. Present for certain BDS and ADS-B messages; null otherwise.
        cs (typing.Optional[str]): Aircraft identification (call sign). Present for BDS20 and some ADS-B messages; null otherwise.
        sq (typing.Optional[str]): Transponder code (Squawk). Present for BDS17 messages; null otherwise.
        lat (typing.Optional[float]): Latitude in degrees. Present for ADS-B position messages; null otherwise.
        lon (typing.Optional[float]): Longitude in degrees. Present for ADS-B position messages; null otherwise.
        spd (typing.Optional[float]): Speed in knots. Present for ADS-B TC19 messages; null otherwise.
        ang (typing.Optional[float]): Angle in degrees. Present for ADS-B TC19 messages; null otherwise.
        vr (typing.Optional[int]): Vertical rate in ft/min. Present for ADS-B TC19 messages; null otherwise.
        spd_type (typing.Optional[str]): Speed type. Present for ADS-B TC19 messages; null otherwise.
        dir_src (typing.Optional[str]): Direction source. Present for ADS-B TC19 messages; null otherwise.
        vr_src (typing.Optional[str]): Vertical rate source. Present for ADS-B TC19 messages; null otherwise.
        ws (typing.Optional[int]): Wind speed in knots. Present for BDS44 messages; null otherwise.
        wd (typing.Optional[int]): Wind direction in degrees. Present for BDS44 messages; null otherwise.
        at (typing.Optional[float]): Air temperature in degrees Celsius. Present for BDS44/BDS45 messages; null otherwise.
        ap (typing.Optional[float]): Air pressure in hPa. Present for BDS44/BDS45 messages; null otherwise.
        hm (typing.Optional[float]): Relative humidity in percentage. Present for BDS44 messages; null otherwise.
        roll (typing.Optional[float]): Aircraft roll angle in degrees. Present for BDS50 messages; null otherwise.
        trak (typing.Optional[float]): True track angle in degrees. Present for BDS50 messages; null otherwise.
        gs (typing.Optional[float]): Ground speed in knots. Present for BDS50 messages; null otherwise.
        tas (typing.Optional[float]): True airspeed in knots. Present for BDS50 messages; null otherwise.
        hd (typing.Optional[float]): Aircraft heading in degrees. Present for BDS60 messages; null otherwise.
        ias (typing.Optional[float]): Indicated airspeed in knots. Present for BDS60 messages; null otherwise.
        m (typing.Optional[float]): Mach number. Present for BDS60 messages; null otherwise.
        vrb (typing.Optional[float]): Vertical rate based on barometric altitude in ft/min. Present for BDS60 messages; null otherwise.
        vri (typing.Optional[float]): Vertical rate based on inertial navigation system in ft/min. Present for BDS60 messages; null otherwise.
        rssi (typing.Optional[float]): Received Signal Strength Indicator in dBFS. Present for all messages if available; null otherwise.
        emst (typing.Optional[str]): Emergency or priority status. Present for ADS-B TC28; null otherwise.
        tgt (typing.Optional[str]): Target state info. Present for certain BDS6,2 or ADS-B TC29; null otherwise.
        opst (typing.Optional[str]): Operational status info. Present for certain BDS6,5 or ADS-B TC31; null otherwise."""
    
    ts: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ts"))
    icao: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icao"))
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
    spd_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="spd_type"))
    dir_src: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dir_src"))
    vr_src: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vr_src"))
    ws: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ws"))
    wd: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wd"))
    at: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="at"))
    ap: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ap"))
    hm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hm"))
    roll: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="roll"))
    trak: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trak"))
    gs: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gs"))
    tas: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tas"))
    hd: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hd"))
    ias: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ias"))
    m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="m"))
    vrb: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vrb"))
    vri: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vri"))
    rssi: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rssi"))
    emst: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="emst"))
    tgt: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tgt"))
    opst: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="opst"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"ModeS_ADSB_Record\", \"doc\": \"A comprehensive schema for Mode-S and ADS-B decoded messages, including fields for various BDS codes and ADS-B type codes.\", \"fields\": [{\"name\": \"ts\", \"type\": {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"The timestamp of the message reception in milliseconds since the epoch. Required.\"}, {\"name\": \"icao\", \"type\": \"string\", \"doc\": \"The ICAO 24-bit address of the aircraft. Required.\"}, {\"name\": \"df\", \"type\": \"int\", \"doc\": \"The Downlink Format (DF) of the Mode-S message, indicating the message category. Required.\"}, {\"name\": \"tc\", \"type\": [\"null\", \"int\"], \"doc\": \"The Type Code (TC) of the ADS-B message. Present for DF17 and DF18 messages; null otherwise.\"}, {\"name\": \"bcode\", \"type\": [\"null\", \"string\"], \"doc\": \"The BDS (Comm-B Data Selector) code. Present for DF20 and DF21 messages; null otherwise.\"}, {\"name\": \"alt\", \"type\": [\"null\", \"int\"], \"doc\": \"Barometric altitude in feet. Present for certain BDS and ADS-B messages; null otherwise.\"}, {\"name\": \"cs\", \"type\": [\"null\", \"string\"], \"doc\": \"Aircraft identification (call sign). Present for BDS20 and some ADS-B messages; null otherwise.\"}, {\"name\": \"sq\", \"type\": [\"null\", \"string\"], \"doc\": \"Transponder code (Squawk). Present for BDS17 messages; null otherwise.\"}, {\"name\": \"lat\", \"type\": [\"null\", \"double\"], \"doc\": \"Latitude in degrees. Present for ADS-B position messages; null otherwise.\"}, {\"name\": \"lon\", \"type\": [\"null\", \"double\"], \"doc\": \"Longitude in degrees. Present for ADS-B position messages; null otherwise.\"}, {\"name\": \"spd\", \"type\": [\"null\", \"float\"], \"doc\": \"Speed in knots. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"ang\", \"type\": [\"null\", \"float\"], \"doc\": \"Angle in degrees. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"vr\", \"type\": [\"null\", \"int\"], \"doc\": \"Vertical rate in ft/min. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"spd_type\", \"type\": [\"null\", \"string\"], \"doc\": \"Speed type. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"dir_src\", \"type\": [\"null\", \"string\"], \"doc\": \"Direction source. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"vr_src\", \"type\": [\"null\", \"string\"], \"doc\": \"Vertical rate source. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"ws\", \"type\": [\"null\", \"int\"], \"doc\": \"Wind speed in knots. Present for BDS44 messages; null otherwise.\"}, {\"name\": \"wd\", \"type\": [\"null\", \"int\"], \"doc\": \"Wind direction in degrees. Present for BDS44 messages; null otherwise.\"}, {\"name\": \"at\", \"type\": [\"null\", \"float\"], \"doc\": \"Air temperature in degrees Celsius. Present for BDS44/BDS45 messages; null otherwise.\"}, {\"name\": \"ap\", \"type\": [\"null\", \"float\"], \"doc\": \"Air pressure in hPa. Present for BDS44/BDS45 messages; null otherwise.\"}, {\"name\": \"hm\", \"type\": [\"null\", \"float\"], \"doc\": \"Relative humidity in percentage. Present for BDS44 messages; null otherwise.\"}, {\"name\": \"roll\", \"type\": [\"null\", \"float\"], \"doc\": \"Aircraft roll angle in degrees. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"trak\", \"type\": [\"null\", \"float\"], \"doc\": \"True track angle in degrees. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"gs\", \"type\": [\"null\", \"float\"], \"doc\": \"Ground speed in knots. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"tas\", \"type\": [\"null\", \"float\"], \"doc\": \"True airspeed in knots. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"hd\", \"type\": [\"null\", \"float\"], \"doc\": \"Aircraft heading in degrees. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"ias\", \"type\": [\"null\", \"float\"], \"doc\": \"Indicated airspeed in knots. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"m\", \"type\": [\"null\", \"float\"], \"doc\": \"Mach number. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"vrb\", \"type\": [\"null\", \"float\"], \"doc\": \"Vertical rate based on barometric altitude in ft/min. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"vri\", \"type\": [\"null\", \"float\"], \"doc\": \"Vertical rate based on inertial navigation system in ft/min. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"rssi\", \"type\": [\"null\", \"float\"], \"doc\": \"Received Signal Strength Indicator in dBFS. Present for all messages if available; null otherwise.\"}, {\"name\": \"emst\", \"type\": [\"null\", \"string\"], \"doc\": \"Emergency or priority status. Present for ADS-B TC28; null otherwise.\"}, {\"name\": \"tgt\", \"type\": [\"null\", \"string\"], \"doc\": \"Target state info. Present for certain BDS6,2 or ADS-B TC29; null otherwise.\"}, {\"name\": \"opst\", \"type\": [\"null\", \"string\"], \"doc\": \"Operational status info. Present for certain BDS6,5 or ADS-B TC31; null otherwise.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        value_ts = self.ts
        self.ts = value_ts
        self.icao=str(self.icao)
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
        self.spd_type=str(self.spd_type) if self.spd_type else None
        self.dir_src=str(self.dir_src) if self.dir_src else None
        self.vr_src=str(self.vr_src) if self.vr_src else None
        self.ws=int(self.ws) if self.ws else None
        self.wd=int(self.wd) if self.wd else None
        self.at=float(self.at) if self.at else None
        self.ap=float(self.ap) if self.ap else None
        self.hm=float(self.hm) if self.hm else None
        self.roll=float(self.roll) if self.roll else None
        self.trak=float(self.trak) if self.trak else None
        self.gs=float(self.gs) if self.gs else None
        self.tas=float(self.tas) if self.tas else None
        self.hd=float(self.hd) if self.hd else None
        self.ias=float(self.ias) if self.ias else None
        self.m=float(self.m) if self.m else None
        self.vrb=float(self.vrb) if self.vrb else None
        self.vri=float(self.vri) if self.vri else None
        self.rssi=float(self.rssi) if self.rssi else None
        self.emst=str(self.emst) if self.emst else None
        self.tgt=str(self.tgt) if self.tgt else None
        self.opst=str(self.opst) if self.opst else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'ModeS_ADSB_Record':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['ModeS_ADSB_Record']:
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
            return ModeS_ADSB_Record.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return ModeS_ADSB_Record.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')