""" TrafficMessage dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TrafficMessage:
    """
    Traffic message from the Finnish national road network operated by Fintraffic, delivered in real time via the Digitraffic MQTT stream at wss://tie.digitraffic.fi/mqtt on topic traffic-message-v3/simple/{situationType}. Traffic messages describe situations such as accidents, road works, weight restrictions, and exempted transports. Each message carries a stable situation identifier (GUID), a version counter, and one or more announcements with location, timing, and descriptive detail. The MQTT payload is gzip-compressed and base64-encoded Simple JSON derived from the GeoJSON-based Digitraffic traffic-message API. See https://www.digitraffic.fi/en/road-traffic/ for the full API documentation and situation type taxonomy.
    
    Attributes:
        situation_id (str)
        situation_type (str)
        traffic_announcement_type (typing.Optional[str])
        version (int)
        release_time (str)
        version_time (str)
        title (typing.Optional[str])
        language (typing.Optional[str])
        sender (typing.Optional[str])
        location_description (typing.Optional[str])
        start_time (typing.Optional[str])
        end_time (typing.Optional[str])
        features_json (typing.Optional[str])
        road_work_phases_json (typing.Optional[str])
        comment (typing.Optional[str])
        additional_information (typing.Optional[str])
        contact_phone (typing.Optional[str])
        contact_email (typing.Optional[str])
        announcements_json (typing.Optional[str])
        geometry_type (typing.Optional[str])
        geometry_coordinates_json (typing.Optional[str])
    """
    
    
    situation_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="situation_id"))
    situation_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="situation_type"))
    traffic_announcement_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="traffic_announcement_type"))
    version: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version"))
    release_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="release_time"))
    version_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version_time"))
    title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    language: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="language"))
    sender: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender"))
    location_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_description"))
    start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    end_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_time"))
    features_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="features_json"))
    road_work_phases_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_work_phases_json"))
    comment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="comment"))
    additional_information: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="additional_information"))
    contact_phone: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contact_phone"))
    contact_email: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contact_email"))
    announcements_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="announcements_json"))
    geometry_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geometry_type"))
    geometry_coordinates_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geometry_coordinates_json"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TrafficMessage':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TrafficMessage']:
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
                return TrafficMessage.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'TrafficMessage':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            situation_id='nmresqlnuzfclsirpkzu',
            situation_type='bykybozubehcpdmpbuza',
            traffic_announcement_type='aqhzdwsbfgjzkpmwcpaj',
            version=int(28),
            release_time='semhaxygxdlhxycobxls',
            version_time='wbxxyrxfezwnugbdqkdk',
            title='ynsknvnujscmeaprdbgg',
            language='eciyxvfcbhtrecuuiazz',
            sender='sdtpqtpdocikunseukzs',
            location_description='hcxxltyshlvfyhqzvxsk',
            start_time='eyzfcydxiouitgxvzthf',
            end_time='cxxgagczzfozlmghfshm',
            features_json='eaxfstzfqfcaqfeasmmw',
            road_work_phases_json='yxufmromcrlkjftutajv',
            comment='jxokorouhkcvcsbxklfp',
            additional_information='qtonckeqqmqcgketkcvk',
            contact_phone='vgdhcamcgtprvkrqhrly',
            contact_email='nhldpyhtkonqkotncoei',
            announcements_json='djswnnpryqeifcjudhgf',
            geometry_type='jqnllyckucvnzevsmkol',
            geometry_coordinates_json='hifyymwvtyrzpitjhjmo'
        )