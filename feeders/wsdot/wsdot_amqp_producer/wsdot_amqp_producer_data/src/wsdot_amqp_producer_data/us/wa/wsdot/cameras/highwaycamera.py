""" HighwayCamera dataclass. """

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
class HighwayCamera:
    """
    Reference catalog entry for a WSDOT highway traffic camera, including its location and a claim-check image URL. The image bytes are not transported; consumers fetch the most recent frame from ImageURL on demand.
    
    Attributes:
        camera_id (str)
        title (typing.Optional[str])
        description (typing.Optional[str])
        camera_owner (typing.Optional[str])
        owner_url (typing.Optional[str])
        image_url (str)
        image_width (typing.Optional[int])
        image_height (typing.Optional[int])
        is_active (bool)
        region (typing.Optional[str])
        sort_order (typing.Optional[int])
        display_latitude (typing.Optional[float])
        display_longitude (typing.Optional[float])
        location_description (typing.Optional[str])
        location_direction (typing.Optional[str])
        location_road_name (typing.Optional[str])
        location_milepost (typing.Optional[float])
        location_latitude (typing.Optional[float])
        location_longitude (typing.Optional[float])
    """
    
    
    camera_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="camera_id"))
    title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    camera_owner: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="camera_owner"))
    owner_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="owner_url"))
    image_url: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="image_url"))
    image_width: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="image_width"))
    image_height: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="image_height"))
    is_active: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_active"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))
    sort_order: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sort_order"))
    display_latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="display_latitude"))
    display_longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="display_longitude"))
    location_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_description"))
    location_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_direction"))
    location_road_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_road_name"))
    location_milepost: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_milepost"))
    location_latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_latitude"))
    location_longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_longitude"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'HighwayCamera':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['HighwayCamera']:
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
                return HighwayCamera.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'HighwayCamera':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            camera_id='mkojfynvcxxvkmcrvcdo',
            title='muooccgezbxiwlpflwkn',
            description='krjxmunfjjbaelucjqlb',
            camera_owner='ptcxenncxbiiezyzyhtn',
            owner_url='fyabgondqcysbprqzgxx',
            image_url='dmhfxsuzsydxkoebxzgi',
            image_width=int(74),
            image_height=int(60),
            is_active=False,
            region='muutdvoxdftmbvjtlatg',
            sort_order=int(79),
            display_latitude=float(15.832046168353564),
            display_longitude=float(21.190438912937605),
            location_description='ngidknqicldgxpkvbsye',
            location_direction='pbnsemqskcpnqusyivig',
            location_road_name='igqfqhhoeprwknxpixpv',
            location_milepost=float(18.72915852070125),
            location_latitude=float(6.329023455211747),
            location_longitude=float(40.284733368406265)
        )