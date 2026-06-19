""" HighwayAlert dataclass. """

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
from wsdot_mqtt_producer_data.us.wa.wsdot.alerts.eventstatusenum import EventStatusenum
from wsdot_mqtt_producer_data.us.wa.wsdot.alerts.priorityenum import PriorityEnum


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class HighwayAlert:
    """
    An active WSDOT highway alert describing an incident, construction, closure, special event, or weather impact, with start and end roadway locations on the Washington State highway network.
    
    Attributes:
        alert_id (str)
        county (typing.Optional[str])
        region (typing.Optional[str])
        priority (PriorityEnum)
        event_category (typing.Optional[str])
        event_status (EventStatusenum)
        headline_description (typing.Optional[str])
        extended_description (typing.Optional[str])
        start_time (typing.Optional[str])
        end_time (typing.Optional[str])
        last_updated_time (typing.Optional[str])
        start_description (typing.Optional[str])
        start_direction (typing.Optional[str])
        start_road_name (typing.Optional[str])
        start_milepost (typing.Optional[float])
        start_latitude (typing.Optional[float])
        start_longitude (typing.Optional[float])
        end_description (typing.Optional[str])
        end_direction (typing.Optional[str])
        end_road_name (typing.Optional[str])
        end_milepost (typing.Optional[float])
        end_latitude (typing.Optional[float])
        end_longitude (typing.Optional[float])
    """
    
    
    alert_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_id"))
    county: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="county"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))
    priority: PriorityEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="priority"))
    event_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_category"))
    event_status: EventStatusenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_status"))
    headline_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="headline_description"))
    extended_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="extended_description"))
    start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    end_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_time"))
    last_updated_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="last_updated_time"))
    start_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_description"))
    start_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_direction"))
    start_road_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_road_name"))
    start_milepost: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_milepost"))
    start_latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_latitude"))
    start_longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_longitude"))
    end_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_description"))
    end_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_direction"))
    end_road_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_road_name"))
    end_milepost: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_milepost"))
    end_latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_latitude"))
    end_longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_longitude"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'HighwayAlert':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['HighwayAlert']:
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
                return HighwayAlert.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'HighwayAlert':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            alert_id='ackolqrvpszcpnvjijhi',
            county='fagxfuuutczuwfluvuuh',
            region='tyqdgvfxplxmczauqdxm',
            priority=PriorityEnum.Highest,
            event_category='etmagvgxnsyheindracm',
            event_status=EventStatusenum.Open,
            headline_description='vrouabjvpwvcdmtixvkg',
            extended_description='csheiltyliqddoyqddne',
            start_time='vduzptzmivnstagpuaqh',
            end_time='qyiogbcaukweclobosnb',
            last_updated_time='ptxsfnlkkybiqwdsjifd',
            start_description='surizzthynzzfclmquqt',
            start_direction='dfjompvqchybicktivmf',
            start_road_name='acuvunxsginuiakyujfg',
            start_milepost=float(20.662227210034047),
            start_latitude=float(17.32566282443563),
            start_longitude=float(2.864518030580332),
            end_description='tihqgpqoitfmossmfakk',
            end_direction='raxdcddwgbmvwdpmrmuc',
            end_road_name='lwanoistyjufgifdwdad',
            end_milepost=float(74.17495563106307),
            end_latitude=float(77.16812255575555),
            end_longitude=float(53.835407251330444)
        )