""" Superevent dataclass. """

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
class Superevent:
    """
    A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata.
    
    Attributes:
        superevent_id (str)
        category (str)
        created (str)
        t_start (float)
        t_0 (float)
        t_end (float)
        far (float)
        time_coinc_far (typing.Optional[float])
        space_coinc_far (typing.Optional[float])
        labels_json (str)
        preferred_event_id (typing.Optional[str])
        pipeline (typing.Optional[str])
        group (str)
        instruments (typing.Optional[str])
        gw_id (typing.Optional[str])
        submitter (str)
        em_type (typing.Optional[str])
        search (typing.Optional[str])
        far_is_upper_limit (typing.Optional[bool])
        nevents (typing.Optional[int])
        self_uri (str)
    """
    
    
    superevent_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="superevent_id"))
    category: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    created: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created"))
    t_start: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="t_start"))
    t_0: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="t_0"))
    t_end: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="t_end"))
    far: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="far"))
    time_coinc_far: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_coinc_far"))
    space_coinc_far: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="space_coinc_far"))
    labels_json: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="labels_json"))
    preferred_event_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="preferred_event_id"))
    pipeline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pipeline"))
    group: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="group"))
    instruments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="instruments"))
    gw_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gw_id"))
    submitter: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="submitter"))
    em_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="em_type"))
    search: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="search"))
    far_is_upper_limit: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="far_is_upper_limit"))
    nevents: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nevents"))
    self_uri: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="self_uri"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Superevent':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Superevent']:
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
                return Superevent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Superevent':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            superevent_id='dpwzlubgtqyocshswoad',
            category='cugexbrcybqiopswqzfz',
            created='eozbervyqauljdenfmbt',
            t_start=float(46.00731348834702),
            t_0=float(6.216539142067323),
            t_end=float(95.98859572815056),
            far=float(45.09366332126189),
            time_coinc_far=float(43.187109628862345),
            space_coinc_far=float(30.252769065132558),
            labels_json='pbdwctllumbedaplukcu',
            preferred_event_id='ifuumbcvfvbethugjyya',
            pipeline='terdydltawvbgwbcluiu',
            group='iepmiahtstflnusffncn',
            instruments='jkebjgyrxqxcwchxrosa',
            gw_id='bntseqmxfiaythguxzcb',
            submitter='jdkfnamjvfydlrwlyskq',
            em_type='mmdylpcuxcsfnwzsamhu',
            search='herllsvzdhlenfrftroq',
            far_is_upper_limit=False,
            nevents=int(37),
            self_uri='wbyhxvmfzhjlsxzmrcmq'
        )