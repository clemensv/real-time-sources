""" MaintenanceTracking dataclass. """

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
class MaintenanceTracking:
    """
    Road maintenance vehicle tracking update from the Finnish national road network operated by Fintraffic. Each message represents a position and task report from a maintenance vehicle, delivered in real time via the Digitraffic MQTT stream at wss://tie.digitraffic.fi/mqtt on topic maintenance-v2/routes/{domain}. Data originates from the Finnish Transport Infrastructure Agency's Harja system for state roads and from municipal systems for other domains. Updates arrive approximately every minute. A new tracking event is created when the vehicle's task changes, the gap between consecutive positions exceeds 5 minutes, or the calculated speed exceeds 140 km/h. See https://www.digitraffic.fi/en/road-traffic/ for the full API documentation and task type taxonomy at /api/maintenance/v1/tracking/tasks.
    
    Attributes:
        domain (str)
        time (int)
        source (typing.Optional[str])
        tasks (typing.List[str])
        x (float)
        y (float)
        direction (typing.Optional[float])
    """
    
    
    domain: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="domain"))
    time: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time"))
    source: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source"))
    tasks: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tasks"))
    x: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="x"))
    y: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="y"))
    direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'MaintenanceTracking':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['MaintenanceTracking']:
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
                return MaintenanceTracking.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'MaintenanceTracking':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            domain='merdtyqtnshipcdqwswf',
            time=int(35),
            source='emqjbgsspjqrrggrwmok',
            tasks=['lyiisrggnfotkzouctip'],
            x=float(89.67540381376187),
            y=float(3.582368335275954),
            direction=float(99.63456323795602)
        )