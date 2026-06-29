""" VehicleEvent dataclass. """

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
class VehicleEvent:
    """
    Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`). All fields except the operator/vehicle/timestamp identity are optional because their presence depends on the event type and on data availability.
    
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
        seq (typing.Optional[int])
        label (typing.Optional[str])
        spd (typing.Optional[float])
        hdg (typing.Optional[int])
        lat (typing.Optional[float])
        long (typing.Optional[float])
        acc (typing.Optional[float])
        odo (typing.Optional[int])
        drst (typing.Optional[int])
        loc (typing.Optional[str])
        ttarr (typing.Optional[str])
        ttdep (typing.Optional[str])
        dr_type (typing.Optional[int])
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
    seq: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="seq"))
    label: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="label"))
    spd: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="spd"))
    hdg: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hdg"))
    lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat"))
    long: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="long"))
    acc: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="acc"))
    odo: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="odo"))
    drst: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drst"))
    loc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="loc"))
    ttarr: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ttarr"))
    ttdep: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ttdep"))
    dr_type: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dr_type"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'VehicleEvent':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['VehicleEvent']:
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
                return VehicleEvent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'VehicleEvent':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            oper=int(4),
            veh=int(60),
            tst='ubvfkznlxsbeduhxebro',
            tsi=int(24),
            operator_id='okpilwjceffikgomlzgl',
            vehicle_number='meuwtjllmmnpldpntvgl',
            temporal_type=None,
            transport_mode=None,
            route_id='rasvuqqgmgsnaitutsbv',
            direction_id='ojtfgzfavlduqdqwazmx',
            headsign='npnsjdfgmhuozuhzlkbt',
            start_time='usbkcltjkjvtasalmnrx',
            next_stop='wklkpnydeudmzhoyyqcd',
            geohash_level='euspkmebddnuhuysfnio',
            geohash='ushujaeleacrzlihgelb',
            desi='yjvzwfvuuvagafyiyxqi',
            dir='ljtoatljkhobojsphavw',
            dl=int(6),
            oday='cknmbayifautefvmdwna',
            jrn=int(32),
            line=int(10),
            start='eawgrfwxjvqksfybanyp',
            stop=int(87),
            route='opjfvdjgzmvxodpxoksa',
            occu=int(100),
            seq=int(16),
            label='nduwkciyzihozrrckiuy',
            spd=float(79.57530251548664),
            hdg=int(50),
            lat=float(61.93554527084895),
            long=float(73.34452770389996),
            acc=float(82.82143747133294),
            odo=int(18),
            drst=int(0),
            loc='ggojydteqzjaoyegsygb',
            ttarr='dagiwgiyfjuxiadlbqze',
            ttdep='ifszgshdzcqdzgbxnbgl',
            dr_type=int(68)
        )