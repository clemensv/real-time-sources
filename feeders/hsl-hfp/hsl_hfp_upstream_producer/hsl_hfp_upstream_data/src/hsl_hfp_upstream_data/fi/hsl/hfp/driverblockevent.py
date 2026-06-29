""" DriverBlockEvent dataclass. """

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
class DriverBlockEvent:
    """
    Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`). These carry a reduced field set — vehicle identity, time, position and driver type — because route, schedule and stop context are not available when the vehicle is not signed on to a public journey.
    
    Attributes:
        oper (int)
        veh (int)
        tst (str)
        tsi (int)
        operator_id (str)
        vehicle_number (str)
        temporal_type (typing.Optional[Any])
        transport_mode (typing.Optional[Any])
        route_id (typing.Optional[str])
        direction_id (typing.Optional[str])
        headsign (typing.Optional[str])
        start_time (typing.Optional[str])
        next_stop (typing.Optional[str])
        geohash_level (typing.Optional[str])
        geohash (typing.Optional[str])
        spd (typing.Optional[float])
        hdg (typing.Optional[int])
        lat (typing.Optional[float])
        long (typing.Optional[float])
        acc (typing.Optional[float])
        odo (typing.Optional[int])
        drst (typing.Optional[int])
        loc (typing.Optional[str])
        oday (typing.Optional[str])
        dr_type (typing.Optional[int])
    """
    
    
    oper: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="oper"))
    veh: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="veh"))
    tst: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tst"))
    tsi: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tsi"))
    operator_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_id"))
    vehicle_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_number"))
    temporal_type: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temporal_type"))
    transport_mode: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="transport_mode"))
    route_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_id"))
    direction_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction_id"))
    headsign: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headsign"))
    start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    next_stop: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="next_stop"))
    geohash_level: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geohash_level"))
    geohash: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geohash"))
    spd: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="spd"))
    hdg: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hdg"))
    lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat"))
    long: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="long"))
    acc: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="acc"))
    odo: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="odo"))
    drst: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drst"))
    loc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="loc"))
    oday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="oday"))
    dr_type: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dr-type"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'DriverBlockEvent':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        if 'dr-type' in data:
            data['dr_type'] = data.pop('dr-type')
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        if 'dr_type' in asdict_result:
            asdict_result['dr-type'] = asdict_result.pop('dr_type')
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['DriverBlockEvent']:
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
                if 'dr-type' in _record:
                    _record['dr_type'] = _record.pop('dr-type')
                return DriverBlockEvent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'DriverBlockEvent':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            oper=int(12),
            veh=int(20),
            tst='sjqntobsiqkrraledupo',
            tsi=int(26),
            operator_id='xhexcgspvrbvyqqmsxvn',
            vehicle_number='utspzwfvszlmzeskwtwo',
            temporal_type=None,
            transport_mode=None,
            route_id='thckzndzaduczsrbdmcx',
            direction_id='zsbkrvyethqfpccemfzp',
            headsign='jyhkkcohwikccrhxhoqb',
            start_time='nninswuajghfgablfxpl',
            next_stop='mtjuofeyhrgshcfbifvv',
            geohash_level='ohyfsngtojivtavxfcpg',
            geohash='uhasjzhglxgmbumfwjyp',
            spd=float(35.740713143007554),
            hdg=int(51),
            lat=float(16.743472321379393),
            long=float(68.79004944008929),
            acc=float(1.921939114250304),
            odo=int(66),
            drst=int(44),
            loc='veopohaqlfmdotbhlwdu',
            oday='gpatndalxqqwuhphxvxs',
            dr_type=int(8)
        )