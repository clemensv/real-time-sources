""" TrafficMeasurement dataclass. """

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
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TrafficMeasurement:
    """
    Normalized traffic measurement from a DATEX II MeasuredDataPublication. The schema covers point and route observations emitted by NDW and Bison Futé including speed, flow, occupancy, and travel time.
    
    Attributes:
        supplier_id (str)
        measurement_site_id (str)
        feed_url (str)
        measurement_time (datetime.datetime)
        measurement_time_key (str)
        country_code (str)
        operator_id (str)
        road_number (typing.Optional[str])
        average_speed_kmh (typing.Optional[float])
        vehicle_flow_rate_veh_per_hour (typing.Optional[int])
        occupancy_percent (typing.Optional[float])
        travel_time_seconds (typing.Optional[float])
        free_flow_travel_time_seconds (typing.Optional[float])
        input_value_count (typing.Optional[int])
        quality_status (typing.Optional[str])
        vehicle_type (typing.Optional[str])
        lane (typing.Optional[str])
        raw_measurements (typing.Optional[str])
    """
    
    
    supplier_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="supplier_id"))
    measurement_site_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="measurement_site_id"))
    feed_url: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feed_url"))
    measurement_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="measurement_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    measurement_time_key: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="measurement_time_key"))
    country_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_code"))
    operator_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_id"))
    road_number: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_number"))
    average_speed_kmh: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_speed_kmh"))
    vehicle_flow_rate_veh_per_hour: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_flow_rate_veh_per_hour"))
    occupancy_percent: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="occupancy_percent"))
    travel_time_seconds: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="travel_time_seconds"))
    free_flow_travel_time_seconds: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="free_flow_travel_time_seconds"))
    input_value_count: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="input_value_count"))
    quality_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="quality_status"))
    vehicle_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_type"))
    lane: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lane"))
    raw_measurements: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="raw_measurements"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TrafficMeasurement':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TrafficMeasurement']:
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
                return TrafficMeasurement.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'TrafficMeasurement':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            supplier_id='kzwmdfzpnxlcgudnoztf',
            measurement_site_id='mdwsjaegksjjpyjthzbv',
            feed_url='dfaoilszdgudwmcpvszj',
            measurement_time=datetime.datetime.now(datetime.timezone.utc),
            measurement_time_key='odzgrmlubauctqgdiyaa',
            country_code='crpybedykfkbrhfhuhsm',
            operator_id='tuvvaowcczqzgbeygsoh',
            road_number='paacuqlylwdjfhkswrbm',
            average_speed_kmh=float(60.976125651549594),
            vehicle_flow_rate_veh_per_hour=int(74),
            occupancy_percent=float(62.43710267093948),
            travel_time_seconds=float(21.6081862953711),
            free_flow_travel_time_seconds=float(47.31038594093624),
            input_value_count=int(47),
            quality_status='yxjgsyhdfevxilfjlvxv',
            vehicle_type='evnfuwkfakyzwxxqtjyr',
            lane='lnxpbblkmafltfwwmlvz',
            raw_measurements='dndngzrgeblrwjumrrmm'
        )