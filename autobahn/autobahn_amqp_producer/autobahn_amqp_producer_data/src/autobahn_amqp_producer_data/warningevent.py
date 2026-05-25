""" WarningEvent dataclass. """

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
from autobahn_amqp_producer_data.displaytypeenum import DisplayTypeenum
from typing import Any
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WarningEvent:
    """
    A transport update from Germany's Autobahn GmbH traffic APIs. It carries road traffic incidents, closures, webcams, and travel information for German motorway segments, roadworks, closures, and traffic messages.
    
    Attributes:
        identifier (str)
        road (str)
        road_ids (typing.List[str])
        event_time (datetime.datetime)
        display_type (DisplayTypeenum)
        title (typing.Optional[str])
        subtitle (typing.Optional[str])
        description_lines (typing.Optional[Any])
        future (typing.Optional[bool])
        is_blocked (typing.Optional[bool])
        icon (typing.Optional[str])
        start_lc_position (typing.Optional[int])
        start_timestamp (typing.Optional[datetime.datetime])
        extent (typing.Optional[str])
        point (typing.Optional[str])
        coordinate_lat (typing.Optional[float])
        coordinate_lon (typing.Optional[float])
        geometry_json (typing.Optional[str])
        impact_lower (typing.Optional[str])
        impact_upper (typing.Optional[str])
        impact_symbols (typing.Optional[Any])
        route_recommendation_json (typing.Optional[str])
        footer_lines (typing.Optional[Any])
        delay_minutes (typing.Optional[int])
        average_speed_kmh (typing.Optional[int])
        abnormal_traffic_type (typing.Optional[str])
        source_name (typing.Optional[str])
    """
    
    
    identifier: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="identifier"))
    road: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road"))
    road_ids: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_ids"))
    event_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    display_type: DisplayTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="display_type"))
    title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    subtitle: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subtitle"))
    description_lines: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description_lines"))
    future: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="future"))
    is_blocked: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_blocked"))
    icon: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icon"))
    start_lc_position: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_lc_position"))
    start_timestamp: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    extent: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="extent"))
    point: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="point"))
    coordinate_lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coordinate_lat"))
    coordinate_lon: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coordinate_lon"))
    geometry_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geometry_json"))
    impact_lower: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="impact_lower"))
    impact_upper: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="impact_upper"))
    impact_symbols: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="impact_symbols"))
    route_recommendation_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_recommendation_json"))
    footer_lines: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="footer_lines"))
    delay_minutes: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay_minutes"))
    average_speed_kmh: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_speed_kmh"))
    abnormal_traffic_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="abnormal_traffic_type"))
    source_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_name"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WarningEvent':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WarningEvent']:
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
                return WarningEvent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WarningEvent':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            identifier='vbuzdqqmdhjrzjgjtzjy',
            road='sbynygyhbfmovaxkmiie',
            road_ids=['btvveqhuynkrwzpsxnrx', 'oclnwhxgwlixzsahbigr', 'wnoqkelivvhssdjiyjzq'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.ROADWORKS,
            title='qsnakezuxhfoditzwobw',
            subtitle='pwgqlqbapdooqjqtowri',
            description_lines=None,
            future=True,
            is_blocked=True,
            icon='cfodrvzxfycfctkdjjlg',
            start_lc_position=int(91),
            start_timestamp=datetime.datetime.now(datetime.timezone.utc),
            extent='dotnjspeiafkatmyzwcq',
            point='hndyzsxrekvacpauqrab',
            coordinate_lat=float(43.58093378197858),
            coordinate_lon=float(73.08368192293142),
            geometry_json='kvtuqovhrbjwbppkwcfb',
            impact_lower='mbgtsevmblywekpbvxfi',
            impact_upper='qkvbfkpjngtiyutuhmpo',
            impact_symbols=None,
            route_recommendation_json='coikwiwpteannhbnxcmr',
            footer_lines=None,
            delay_minutes=int(12),
            average_speed_kmh=int(33),
            abnormal_traffic_type='zmdbyimuivyysaojnonn',
            source_name='scjuqsmpngrratamgxej'
        )