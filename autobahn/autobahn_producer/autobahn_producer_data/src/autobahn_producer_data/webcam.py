""" Webcam dataclass. """

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
import avro.schema
import avro.io
from autobahn_producer_data.displaytypeenum import DisplayTypeenum
from typing import Any
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Webcam:
    """
    Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.
    
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
        extent (typing.Optional[str])
        point (typing.Optional[str])
        coordinate_lat (typing.Optional[float])
        coordinate_lon (typing.Optional[float])
        route_recommendation_json (typing.Optional[str])
        footer_lines (typing.Optional[Any])
        operator_name (typing.Optional[str])
        image_url (typing.Optional[str])
        stream_url (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "[{\"type\": \"record\", \"name\": \"Webcam\", \"doc\": \"Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.\", \"fields\": [{\"name\": \"identifier\", \"type\": \"string\", \"doc\": \"Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key.\"}, {\"name\": \"road\", \"type\": \"string\", \"doc\": \"Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. [pattern: ^[a-z0-9-]+$]\"}, {\"name\": \"road_ids\", \"type\": {\"type\": \"array\", \"items\": \"string\"}, \"doc\": \"Autobahn road identifiers for the road query that yielded this webcam item.\"}, {\"name\": \"event_time\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload.\"}, {\"name\": \"display_type\", \"type\": \"string\", \"doc\": \"Autobahn API display_type for webcam items.\"}, {\"name\": \"title\", \"type\": [\"string\", \"null\"], \"doc\": \"Human-readable title from the Autobahn API webcam item.\", \"default\": null}, {\"name\": \"subtitle\", \"type\": [\"string\", \"null\"], \"doc\": \"Human-readable subtitle from the Autobahn API webcam item.\", \"default\": null}, {\"name\": \"description_lines\", \"type\": [\"null\", \"StringList\"], \"doc\": \"Description lines from the Autobahn API description array.\", \"default\": null}, {\"name\": \"future\", \"type\": [\"boolean\", \"null\"], \"doc\": \"Whether the Autobahn API marks the webcam item as a future entry.\", \"default\": null}, {\"name\": \"is_blocked\", \"type\": [\"boolean\", \"null\"], \"doc\": \"Whether the Autobahn API marks the webcam location as blocked.\", \"default\": null}, {\"name\": \"icon\", \"type\": [\"string\", \"null\"], \"doc\": \"Autobahn API icon identifier for the webcam item.\", \"default\": null}, {\"name\": \"extent\", \"type\": [\"string\", \"null\"], \"doc\": \"Autobahn API extent text for the webcam location.\", \"default\": null}, {\"name\": \"point\", \"type\": [\"string\", \"null\"], \"doc\": \"Autobahn API point text that identifies the webcam location.\", \"default\": null}, {\"name\": \"coordinate_lat\", \"type\": [\"double\", \"null\"], \"doc\": \"Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. [minimum: -90, maximum: 90]\", \"default\": null}, {\"name\": \"coordinate_lon\", \"type\": [\"double\", \"null\"], \"doc\": \"Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. [minimum: -180, maximum: 180]\", \"default\": null}, {\"name\": \"route_recommendation_json\", \"type\": [\"string\", \"null\"], \"doc\": \"Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location.\", \"default\": null}, {\"name\": \"footer_lines\", \"type\": [\"null\", \"StringList\"], \"doc\": \"Footer lines from the Autobahn API footer array.\", \"default\": null}, {\"name\": \"operator_name\", \"type\": [\"string\", \"null\"], \"doc\": \"operator value from the Autobahn API webcam item.\", \"default\": null}, {\"name\": \"image_url\", \"type\": [\"string\", \"null\"], \"doc\": \"imageurl value from the Autobahn API webcam item for the still image.\", \"default\": null}, {\"name\": \"stream_url\", \"type\": [\"string\", \"null\"], \"doc\": \"linkurl value from the Autobahn API webcam item for the linked stream or detail page.\", \"default\": null}]}, {\"type\": \"record\", \"name\": \"StringList\", \"fields\": [{\"name\": \"items\", \"type\": {\"type\": \"array\", \"items\": \"string\"}}]}]"
    )
    
    
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
    extent: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="extent"))
    point: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="point"))
    coordinate_lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coordinate_lat"))
    coordinate_lon: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coordinate_lon"))
    route_recommendation_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_recommendation_json"))
    footer_lines: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="footer_lines"))
    operator_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_name"))
    image_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="image_url"))
    stream_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stream_url"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Webcam':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'Webcam':
        """
        Converts a dictionary from Avro deserialization to a dataclass instance.
        Handles conversion of string representations back to Python types for
        extended logical types.
        
        Args:
            data: The dictionary from Avro deserialization.
        
        Returns:
            The dataclass representation.
        """
        # Convert string values back to Python types for Avro string-based logical types
        converted = data.copy()
        if 'identifier' in converted and converted['identifier'] is not None:
            value = converted['identifier']
        if 'road' in converted and converted['road'] is not None:
            value = converted['road']
        if 'road_ids' in converted and converted['road_ids'] is not None:
            value = converted['road_ids']
        if 'event_time' in converted and converted['event_time'] is not None:
            value = converted['event_time']
            if isinstance(value, str):
                converted['event_time'] = datetime.datetime.fromisoformat(value)
        if 'display_type' in converted and converted['display_type'] is not None:
            value = converted['display_type']
        if 'title' in converted and converted['title'] is not None:
            value = converted['title']
        if 'subtitle' in converted and converted['subtitle'] is not None:
            value = converted['subtitle']
        if 'description_lines' in converted and converted['description_lines'] is not None:
            value = converted['description_lines']
        if 'future' in converted and converted['future'] is not None:
            value = converted['future']
        if 'is_blocked' in converted and converted['is_blocked'] is not None:
            value = converted['is_blocked']
        if 'icon' in converted and converted['icon'] is not None:
            value = converted['icon']
        if 'extent' in converted and converted['extent'] is not None:
            value = converted['extent']
        if 'point' in converted and converted['point'] is not None:
            value = converted['point']
        if 'coordinate_lat' in converted and converted['coordinate_lat'] is not None:
            value = converted['coordinate_lat']
        if 'coordinate_lon' in converted and converted['coordinate_lon'] is not None:
            value = converted['coordinate_lon']
        if 'route_recommendation_json' in converted and converted['route_recommendation_json'] is not None:
            value = converted['route_recommendation_json']
        if 'footer_lines' in converted and converted['footer_lines'] is not None:
            value = converted['footer_lines']
        if 'operator_name' in converted and converted['operator_name'] is not None:
            value = converted['operator_name']
        if 'image_url' in converted and converted['image_url'] is not None:
            value = converted['image_url']
        if 'stream_url' in converted and converted['stream_url'] is not None:
            value = converted['stream_url']
        
        return cls(**converted)

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

    def to_avro_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary suitable for Avro serialization.
        Handles conversion of Python types to Avro-compatible string representations
        for extended logical types.

        Returns:
            The dictionary representation suitable for Avro serialization.
        """
        result = self.to_serializer_dict()
        converted = result.copy()
        
        # Convert specific fields based on their source types
        if 'event_time' in converted and converted['event_time'] is not None:
            value = converted['event_time']
            if isinstance(value, datetime.datetime):
                converted['event_time'] = value.isoformat()
        
        return converted

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'application/json': Encodes the data to JSON format.
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
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
            # Convert to Avro binary format using the embedded schema
            writer = avro.io.DatumWriter(self.AvroType)
            with io.BytesIO() as stream:
                encoder = avro.io.BinaryEncoder(stream)
                writer.write(self.to_avro_dict(), encoder)
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Webcam']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'application/json': Attempts to decode the data from JSON encoded format.
                    'avro/binary': Attempts to decode the data from Avro binary format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            if isinstance(data, bytes):
                # Decode from Avro binary format using the embedded schema
                reader = avro.io.DatumReader(cls.AvroType)
                with io.BytesIO(data) as stream:
                    decoder = avro.io.BinaryDecoder(stream)
                    _record = reader.read(decoder)
                    return Webcam.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Webcam.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Webcam':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            identifier='elhgznmygjotcstqmccr',
            road='eggqhaoukpkagtypvijw',
            road_ids=['fbmddvnowkkwkgwjzvkl', 'grxvgmwbxczwfqnxjqaz', 'yvweawhzwdfqdsfymrdv'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.WEBCAM,
            title='atfjzukanwxcjiqirhka',
            subtitle='iixtolfexzhsaiertwap',
            description_lines=None,
            future=True,
            is_blocked=False,
            icon='lecnvdzvuxreknztrjzl',
            extent='nooxkbayojsginjwdpoc',
            point='nakyjfabklortzlozkax',
            coordinate_lat=float(53.312079389940195),
            coordinate_lon=float(87.04523302393108),
            route_recommendation_json='qwlcnapzkejjgfwewtpi',
            footer_lines=None,
            operator_name='xwzgeztyxhjfgvvarobt',
            image_url='gzglzctkduccaijsvdbk',
            stream_url='ukahtbplvjssqdehkuzo'
        )