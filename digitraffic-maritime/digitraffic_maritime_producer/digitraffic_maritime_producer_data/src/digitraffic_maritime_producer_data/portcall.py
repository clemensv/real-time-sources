""" PortCall dataclass. """

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
from marshmallow import fields
import json
from digitraffic_maritime_producer_data.portcallareadetail import PortCallAreaDetail
from digitraffic_maritime_producer_data.portcallagent import PortCallAgent
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PortCall:
    """
    Port call update from Digitraffic's Portnet-backed port-call API. Each event represents one vessel visit plan or update keyed by the Digitraffic port call identifier and carries the vessel identity, routing context, assigned agents, and berth-area timing details.
    
    Attributes:
        port_call_id (int)
        updated_at (datetime.datetime)
        customs_reference (typing.Optional[str])
        port_to_visit (str)
        previous_port (typing.Optional[str])
        next_port (typing.Optional[str])
        mmsi (typing.Optional[int])
        imo_lloyds (typing.Optional[int])
        vessel_name (str)
        vessel_name_prefix (typing.Optional[str])
        radio_call_sign (typing.Optional[str])
        nationality (typing.Optional[str])
        vessel_type_code (typing.Optional[int])
        domestic_traffic_arrival (bool)
        domestic_traffic_departure (bool)
        arrival_with_cargo (bool)
        not_loading (bool)
        discharge (typing.Optional[int])
        current_security_level (typing.Optional[int])
        agents (typing.List[PortCallAgent])
        port_areas (typing.List[PortCallAreaDetail])
    """
    
    
    port_call_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_call_id"))
    updated_at: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated_at", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    customs_reference: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="customs_reference"))
    port_to_visit: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_to_visit"))
    previous_port: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="previous_port"))
    next_port: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="next_port"))
    mmsi: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmsi"))
    imo_lloyds: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imo_lloyds"))
    vessel_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vessel_name"))
    vessel_name_prefix: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vessel_name_prefix"))
    radio_call_sign: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="radio_call_sign"))
    nationality: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nationality"))
    vessel_type_code: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vessel_type_code"))
    domestic_traffic_arrival: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="domestic_traffic_arrival"))
    domestic_traffic_departure: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="domestic_traffic_departure"))
    arrival_with_cargo: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arrival_with_cargo"))
    not_loading: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="not_loading"))
    discharge: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="discharge"))
    current_security_level: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_security_level"))
    agents: typing.List[PortCallAgent]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agents"))
    port_areas: typing.List[PortCallAreaDetail]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_areas"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PortCall':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PortCall']:
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
                return PortCall.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'PortCall':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            port_call_id=int(52),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            customs_reference='yuacskdtmddxtcrejxsr',
            port_to_visit='hzgaoeyqpdtlfgzvabgf',
            previous_port='cnzgrylnsrkggspnmzqe',
            next_port='zoipzcmwcdgkglczrwym',
            mmsi=int(41),
            imo_lloyds=int(12),
            vessel_name='gtonppfpkbeilausdlfi',
            vessel_name_prefix='arxntwmnruaeywqrwyhk',
            radio_call_sign='elsdjezwrzpcmchscgkd',
            nationality='nwmbtuqqizieyiutjrex',
            vessel_type_code=int(14),
            domestic_traffic_arrival=True,
            domestic_traffic_departure=True,
            arrival_with_cargo=True,
            not_loading=False,
            discharge=int(25),
            current_security_level=int(26),
            agents=[None],
            port_areas=[None, None, None, None]
        )