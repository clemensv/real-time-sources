""" ModeS_ADSB_Record dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import orjson
from dataclasses import dataclass
import json
import datetime


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
    
    ts: datetime.datetime=dataclasses.field(kw_only=True)
    icao: str=dataclasses.field(kw_only=True)
    df: int=dataclasses.field(kw_only=True)
    tc: typing.Optional[int]=dataclasses.field(kw_only=True)
    bcode: typing.Optional[str]=dataclasses.field(kw_only=True)
    alt: typing.Optional[int]=dataclasses.field(kw_only=True)
    cs: typing.Optional[str]=dataclasses.field(kw_only=True)
    sq: typing.Optional[str]=dataclasses.field(kw_only=True)
    lat: typing.Optional[float]=dataclasses.field(kw_only=True)
    lon: typing.Optional[float]=dataclasses.field(kw_only=True)
    spd: typing.Optional[float]=dataclasses.field(kw_only=True)
    ang: typing.Optional[float]=dataclasses.field(kw_only=True)
    vr: typing.Optional[int]=dataclasses.field(kw_only=True)
    spd_type: typing.Optional[str]=dataclasses.field(kw_only=True)
    dir_src: typing.Optional[str]=dataclasses.field(kw_only=True)
    vr_src: typing.Optional[str]=dataclasses.field(kw_only=True)
    ws: typing.Optional[int]=dataclasses.field(kw_only=True)
    wd: typing.Optional[int]=dataclasses.field(kw_only=True)
    at: typing.Optional[float]=dataclasses.field(kw_only=True)
    ap: typing.Optional[float]=dataclasses.field(kw_only=True)
    hm: typing.Optional[float]=dataclasses.field(kw_only=True)
    roll: typing.Optional[float]=dataclasses.field(kw_only=True)
    trak: typing.Optional[float]=dataclasses.field(kw_only=True)
    gs: typing.Optional[float]=dataclasses.field(kw_only=True)
    tas: typing.Optional[float]=dataclasses.field(kw_only=True)
    hd: typing.Optional[float]=dataclasses.field(kw_only=True)
    ias: typing.Optional[float]=dataclasses.field(kw_only=True)
    m: typing.Optional[float]=dataclasses.field(kw_only=True)
    vrb: typing.Optional[float]=dataclasses.field(kw_only=True)
    vri: typing.Optional[float]=dataclasses.field(kw_only=True)
    rssi: typing.Optional[float]=dataclasses.field(kw_only=True)
    emst: typing.Optional[str]=dataclasses.field(kw_only=True)
    tgt: typing.Optional[str]=dataclasses.field(kw_only=True)
    opst: typing.Optional[str]=dataclasses.field(kw_only=True)
    

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
        asdict_result = {k: v for k, v in asdict_result.items() if v is not None}
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
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data) if v is not None}

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
            result = orjson.dumps(self.to_serializer_dict())

        if result is not None and content_type.endswith('+gzip'):
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
                _record = orjson.loads(data_str)
                return ModeS_ADSB_Record.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')