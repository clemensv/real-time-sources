""" WarningEvent dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WarningEvent:
    """
    Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.
    Attributes:
        identifier (str): 
        road_ids (typing.List[str]): 
        event_time (str): 
        display_type (str): 
        title (typing.Optional[str]): 
        subtitle (typing.Optional[str]): 
        description_lines (typing.Optional[typing.List[str]]): 
        future (typing.Optional[bool]): 
        is_blocked (typing.Optional[bool]): 
        icon (typing.Optional[str]): 
        start_lc_position (typing.Optional[int]): 
        start_timestamp (typing.Optional[str]): 
        extent (typing.Optional[str]): 
        point (typing.Optional[str]): 
        coordinate_lat (typing.Optional[float]): 
        coordinate_lon (typing.Optional[float]): 
        geometry_json (typing.Optional[str]): 
        impact_lower (typing.Optional[str]): 
        impact_upper (typing.Optional[str]): 
        impact_symbols (typing.Optional[typing.List[str]]): 
        route_recommendation_json (typing.Optional[str]): 
        footer_lines (typing.Optional[typing.List[str]]): 
        delay_minutes (typing.Optional[int]): 
        average_speed_kmh (typing.Optional[int]): 
        abnormal_traffic_type (typing.Optional[str]): 
        source_name (typing.Optional[str]): """
    
    identifier: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="identifier"))
    road_ids: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_ids"))
    event_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_time"))
    display_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="display_type"))
    title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    subtitle: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subtitle"))
    description_lines: typing.Optional[typing.List[str]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description_lines"))
    future: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="future"))
    is_blocked: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_blocked"))
    icon: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icon"))
    start_lc_position: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_lc_position"))
    start_timestamp: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_timestamp"))
    extent: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="extent"))
    point: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="point"))
    coordinate_lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coordinate_lat"))
    coordinate_lon: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coordinate_lon"))
    geometry_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geometry_json"))
    impact_lower: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="impact_lower"))
    impact_upper: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="impact_upper"))
    impact_symbols: typing.Optional[typing.List[str]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="impact_symbols"))
    route_recommendation_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_recommendation_json"))
    footer_lines: typing.Optional[typing.List[str]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="footer_lines"))
    delay_minutes: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay_minutes"))
    average_speed_kmh: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_speed_kmh"))
    abnormal_traffic_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="abnormal_traffic_type"))
    source_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_name"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"WarningEvent\", \"namespace\": \"DE.Autobahn\", \"doc\": \"Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.\", \"fields\": [{\"name\": \"identifier\", \"type\": \"string\"}, {\"name\": \"road_ids\", \"type\": {\"type\": \"array\", \"items\": \"string\"}}, {\"name\": \"event_time\", \"type\": \"string\"}, {\"name\": \"display_type\", \"type\": \"string\"}, {\"name\": \"title\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"subtitle\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"description_lines\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"string\"}], \"default\": null}, {\"name\": \"future\", \"type\": [\"null\", \"boolean\"], \"default\": null}, {\"name\": \"is_blocked\", \"type\": [\"null\", \"boolean\"], \"default\": null}, {\"name\": \"icon\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"start_lc_position\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"start_timestamp\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"extent\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"point\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"coordinate_lat\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"coordinate_lon\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"geometry_json\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"impact_lower\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"impact_upper\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"impact_symbols\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"string\"}], \"default\": null}, {\"name\": \"route_recommendation_json\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"footer_lines\", \"type\": [\"null\", {\"type\": \"array\", \"items\": \"string\"}], \"default\": null}, {\"name\": \"delay_minutes\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"average_speed_kmh\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"abnormal_traffic_type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"source_name\", \"type\": [\"null\", \"string\"], \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.identifier=str(self.identifier)
        self.road_ids=self.road_ids if isinstance(self.road_ids, list) else [str(v) for v in self.road_ids] if self.road_ids else None
        self.event_time=str(self.event_time)
        self.display_type=str(self.display_type)
        self.title=str(self.title) if self.title else None
        self.subtitle=str(self.subtitle) if self.subtitle else None
        self.description_lines=self.description_lines if isinstance(self.description_lines, list) else [str(v) for v in self.description_lines] if self.description_lines else None if self.description_lines else None
        self.future=bool(self.future) if self.future else None
        self.is_blocked=bool(self.is_blocked) if self.is_blocked else None
        self.icon=str(self.icon) if self.icon else None
        self.start_lc_position=int(self.start_lc_position) if self.start_lc_position else None
        self.start_timestamp=str(self.start_timestamp) if self.start_timestamp else None
        self.extent=str(self.extent) if self.extent else None
        self.point=str(self.point) if self.point else None
        self.coordinate_lat=float(self.coordinate_lat) if self.coordinate_lat else None
        self.coordinate_lon=float(self.coordinate_lon) if self.coordinate_lon else None
        self.geometry_json=str(self.geometry_json) if self.geometry_json else None
        self.impact_lower=str(self.impact_lower) if self.impact_lower else None
        self.impact_upper=str(self.impact_upper) if self.impact_upper else None
        self.impact_symbols=self.impact_symbols if isinstance(self.impact_symbols, list) else [str(v) for v in self.impact_symbols] if self.impact_symbols else None if self.impact_symbols else None
        self.route_recommendation_json=str(self.route_recommendation_json) if self.route_recommendation_json else None
        self.footer_lines=self.footer_lines if isinstance(self.footer_lines, list) else [str(v) for v in self.footer_lines] if self.footer_lines else None if self.footer_lines else None
        self.delay_minutes=int(self.delay_minutes) if self.delay_minutes else None
        self.average_speed_kmh=int(self.average_speed_kmh) if self.average_speed_kmh else None
        self.abnormal_traffic_type=str(self.abnormal_traffic_type) if self.abnormal_traffic_type else None
        self.source_name=str(self.source_name) if self.source_name else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WarningEvent':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WarningEvent']:
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
            return WarningEvent.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WarningEvent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')