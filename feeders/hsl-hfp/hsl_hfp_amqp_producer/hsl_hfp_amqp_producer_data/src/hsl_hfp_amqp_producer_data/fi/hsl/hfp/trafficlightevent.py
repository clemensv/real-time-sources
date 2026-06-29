""" TrafficLightEvent dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
from __future__ import annotations
import io
import gzip
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import json
from typing import Any


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TrafficLightEvent:
    """
    Telemetry payload for the traffic-light priority events: the request (`tlr`) and the response (`tla`). Carries the vehicle identity, time and position context plus the `tlp-*`, `sid` and `signal-groupid` priority fields. Mirrors the HFP v2 payload field table for these event types.
    
    Attributes:
        oper (int)
        veh (int)
        tst (str)
        tsi (int)
        operator_id (str)
        vehicle_number (str)
        temporal_type (Any)
        transport_mode (Any)
        route_id (typing.Optional[str])
        direction_id (typing.Optional[str])
        headsign (typing.Optional[str])
        start_time (typing.Optional[str])
        next_stop (typing.Optional[str])
        geohash_level (typing.Optional[str])
        geohash (typing.Optional[str])
        desi (typing.Optional[str])
        dir (typing.Optional[str])
        dl (typing.Optional[int])
        oday (typing.Optional[str])
        jrn (typing.Optional[int])
        line (typing.Optional[int])
        start (typing.Optional[str])
        stop (typing.Optional[int])
        route (typing.Optional[str])
        occu (typing.Optional[int])
        spd (typing.Optional[float])
        hdg (typing.Optional[int])
        lat (typing.Optional[float])
        long (typing.Optional[float])
        acc (typing.Optional[float])
        odo (typing.Optional[int])
        drst (typing.Optional[int])
        loc (typing.Optional[str])
        tlp_requestid (typing.Optional[int])
        tlp_requesttype (typing.Optional[Any])
        tlp_prioritylevel (typing.Optional[Any])
        tlp_reason (typing.Optional[Any])
        tlp_att_seq (typing.Optional[int])
        tlp_decision (typing.Optional[Any])
        sid (typing.Optional[int])
        signal_groupid (typing.Optional[int])
        tlp_signalgroupnbr (typing.Optional[int])
        tlp_line_configid (typing.Optional[int])
        tlp_point_configid (typing.Optional[int])
        tlp_frequency (typing.Optional[int])
        tlp_protocol (typing.Optional[str])
    """
    
    
    oper: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="oper"))
    veh: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="veh"))
    tst: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tst"))
    tsi: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tsi"))
    operator_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_id"))
    vehicle_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_number"))
    temporal_type: Any=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temporal_type"))
    transport_mode: Any=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="transport_mode"))
    route_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_id"))
    direction_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction_id"))
    headsign: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headsign"))
    start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    next_stop: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="next_stop"))
    geohash_level: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geohash_level"))
    geohash: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geohash"))
    desi: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="desi"))
    dir: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dir"))
    dl: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dl"))
    oday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="oday"))
    jrn: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="jrn"))
    line: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="line"))
    start: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start"))
    stop: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stop"))
    route: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route"))
    occu: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="occu"))
    spd: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="spd"))
    hdg: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hdg"))
    lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat"))
    long: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="long"))
    acc: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="acc"))
    odo: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="odo"))
    drst: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drst"))
    loc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="loc"))
    tlp_requestid: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_requestid"))
    tlp_requesttype: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_requesttype"))
    tlp_prioritylevel: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_prioritylevel"))
    tlp_reason: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_reason"))
    tlp_att_seq: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_att_seq"))
    tlp_decision: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_decision"))
    sid: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sid"))
    signal_groupid: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="signal_groupid"))
    tlp_signalgroupnbr: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_signalgroupnbr"))
    tlp_line_configid: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_line_configid"))
    tlp_point_configid: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_point_configid"))
    tlp_frequency: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_frequency"))
    tlp_protocol: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tlp_protocol"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TrafficLightEvent':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
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
            if isinstance(v, enum.Enum):
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
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member
            if isinstance(result, str):
                result = result.encode('utf-8')

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TrafficLightEvent']:
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
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return TrafficLightEvent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'TrafficLightEvent':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            oper=int(78),
            veh=int(32),
            tst='wckmnbbbvdapmbfbcyrf',
            tsi=int(11),
            operator_id='zvxzwtkrgyoutpyqzsvc',
            vehicle_number='xszjgnmgcvhwiaiqhcgl',
            temporal_type=None,
            transport_mode=None,
            route_id='idfdmrdfbqloytwttsyj',
            direction_id='aqtwnmpbfyzdxpricoll',
            headsign='lqgacuqhuxvfelhkdhvw',
            start_time='vvdkcunyejlzpdmqtipf',
            next_stop='uzonfolsxdtzkvklijxv',
            geohash_level='suqmevydbdsgddscbncb',
            geohash='fzvdehlhljertdfzaeer',
            desi='pdwnitmqwqwffhownibc',
            dir='byybagsxghxmdvzszoip',
            dl=int(12),
            oday='ighwqfmmdcbsdgtgvcrr',
            jrn=int(24),
            line=int(16),
            start='hgwtoccscrtegnhhgpym',
            stop=int(16),
            route='jiskfobkbvcjzdybsdpp',
            occu=int(62),
            spd=float(85.09381588637743),
            hdg=int(7),
            lat=float(36.97998241319041),
            long=float(4.878617651520445),
            acc=float(7.821331527244968),
            odo=int(87),
            drst=int(68),
            loc='jjdqujtzajmyhogxprxk',
            tlp_requestid=int(25),
            tlp_requesttype=None,
            tlp_prioritylevel=None,
            tlp_reason=None,
            tlp_att_seq=int(51),
            tlp_decision=None,
            sid=int(83),
            signal_groupid=int(78),
            tlp_signalgroupnbr=int(10),
            tlp_line_configid=int(5),
            tlp_point_configid=int(7),
            tlp_frequency=int(15),
            tlp_protocol='bzudbqagyrddljjfauql'
        )