""" WaitTime dataclass. """

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
from cbp_border_wait_amqp_producer_data.gov.cbp.borderwait.borderslugenum import BorderSlugenum


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WaitTime:
    """
    Flattened wait time snapshot for a single US land border port of entry. Derived from the CBP Border Wait Time API nested lane structure. Each record captures delay in minutes and number of open lanes for every combination of traveler category (passenger vehicle, pedestrian, commercial vehicle) and lane type (standard, SENTRI/NEXUS, Ready Lane, FAST). Operational status values from CBP include 'no delay', 'delay', 'N/A', 'Lanes Closed', and 'Update Pending'.
    
    Attributes:
        port_number (str)
        port_name (str)
        border (str)
        crossing_name (str)
        port_status (str)
        date (str)
        time (str)
        passenger_vehicle_standard_delay (typing.Optional[int])
        passenger_vehicle_standard_lanes_open (typing.Optional[int])
        passenger_vehicle_standard_operational_status (typing.Optional[str])
        passenger_vehicle_nexus_sentri_delay (typing.Optional[int])
        passenger_vehicle_nexus_sentri_lanes_open (typing.Optional[int])
        passenger_vehicle_nexus_sentri_operational_status (typing.Optional[str])
        passenger_vehicle_ready_delay (typing.Optional[int])
        passenger_vehicle_ready_lanes_open (typing.Optional[int])
        passenger_vehicle_ready_operational_status (typing.Optional[str])
        pedestrian_standard_delay (typing.Optional[int])
        pedestrian_standard_lanes_open (typing.Optional[int])
        pedestrian_standard_operational_status (typing.Optional[str])
        pedestrian_ready_delay (typing.Optional[int])
        pedestrian_ready_lanes_open (typing.Optional[int])
        pedestrian_ready_operational_status (typing.Optional[str])
        commercial_vehicle_standard_delay (typing.Optional[int])
        commercial_vehicle_standard_lanes_open (typing.Optional[int])
        commercial_vehicle_standard_operational_status (typing.Optional[str])
        commercial_vehicle_fast_delay (typing.Optional[int])
        commercial_vehicle_fast_lanes_open (typing.Optional[int])
        commercial_vehicle_fast_operational_status (typing.Optional[str])
        construction_notice (typing.Optional[str])
        border_slug (BorderSlugenum)
    """
    
    
    port_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_number"))
    port_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_name"))
    border: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="border"))
    crossing_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="crossing_name"))
    port_status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="port_status"))
    date: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date"))
    time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time"))
    passenger_vehicle_standard_delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_standard_delay"))
    passenger_vehicle_standard_lanes_open: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_standard_lanes_open"))
    passenger_vehicle_standard_operational_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_standard_operational_status"))
    passenger_vehicle_nexus_sentri_delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_nexus_sentri_delay"))
    passenger_vehicle_nexus_sentri_lanes_open: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_nexus_sentri_lanes_open"))
    passenger_vehicle_nexus_sentri_operational_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_nexus_sentri_operational_status"))
    passenger_vehicle_ready_delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_ready_delay"))
    passenger_vehicle_ready_lanes_open: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_ready_lanes_open"))
    passenger_vehicle_ready_operational_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="passenger_vehicle_ready_operational_status"))
    pedestrian_standard_delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pedestrian_standard_delay"))
    pedestrian_standard_lanes_open: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pedestrian_standard_lanes_open"))
    pedestrian_standard_operational_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pedestrian_standard_operational_status"))
    pedestrian_ready_delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pedestrian_ready_delay"))
    pedestrian_ready_lanes_open: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pedestrian_ready_lanes_open"))
    pedestrian_ready_operational_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pedestrian_ready_operational_status"))
    commercial_vehicle_standard_delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="commercial_vehicle_standard_delay"))
    commercial_vehicle_standard_lanes_open: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="commercial_vehicle_standard_lanes_open"))
    commercial_vehicle_standard_operational_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="commercial_vehicle_standard_operational_status"))
    commercial_vehicle_fast_delay: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="commercial_vehicle_fast_delay"))
    commercial_vehicle_fast_lanes_open: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="commercial_vehicle_fast_lanes_open"))
    commercial_vehicle_fast_operational_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="commercial_vehicle_fast_operational_status"))
    construction_notice: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="construction_notice"))
    border_slug: BorderSlugenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="border_slug"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WaitTime':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WaitTime']:
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
                return WaitTime.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WaitTime':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            port_number='hxzpmpuhpskprioidbpg',
            port_name='ldemhtezhyjfuyeitwbj',
            border='hskubkyfdhxvmerrvkco',
            crossing_name='fvvqmycnnmibtegypovd',
            port_status='qzgwtzdamcuwqacbwhyu',
            date='uftwhlioqxzkfjefvraa',
            time='cqvfesfugunykmizifqy',
            passenger_vehicle_standard_delay=int(89),
            passenger_vehicle_standard_lanes_open=int(29),
            passenger_vehicle_standard_operational_status='jfmzulsvnugyspxxbsky',
            passenger_vehicle_nexus_sentri_delay=int(38),
            passenger_vehicle_nexus_sentri_lanes_open=int(66),
            passenger_vehicle_nexus_sentri_operational_status='ozhzttdjdzeajpkrbptf',
            passenger_vehicle_ready_delay=int(81),
            passenger_vehicle_ready_lanes_open=int(99),
            passenger_vehicle_ready_operational_status='yxwtxhugzebccwlwzayp',
            pedestrian_standard_delay=int(83),
            pedestrian_standard_lanes_open=int(19),
            pedestrian_standard_operational_status='ijkrmzifuvpxcpqjenwk',
            pedestrian_ready_delay=int(24),
            pedestrian_ready_lanes_open=int(28),
            pedestrian_ready_operational_status='hietiohmpxkgzlwjbpsr',
            commercial_vehicle_standard_delay=int(12),
            commercial_vehicle_standard_lanes_open=int(32),
            commercial_vehicle_standard_operational_status='feniyaeyvrschofoxyrl',
            commercial_vehicle_fast_delay=int(60),
            commercial_vehicle_fast_lanes_open=int(62),
            commercial_vehicle_fast_operational_status='fgpnwjqcqvhecrnhuott',
            construction_notice='nbqoxstoaweelmcuowah',
            border_slug=BorderSlugenum.canadian_border
        )