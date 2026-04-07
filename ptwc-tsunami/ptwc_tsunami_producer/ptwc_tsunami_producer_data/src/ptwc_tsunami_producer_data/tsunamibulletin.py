""" TsunamiBulletin dataclass. """

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
from ptwc_tsunami_producer_data.feedenum import FeedEnum
from ptwc_tsunami_producer_data.categoryenum import CategoryEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TsunamiBulletin:
    """
    A tsunami bulletin from the US National Tsunami Warning Center (NTWC) or the Pacific Tsunami Warning Center (PTWC). Contains seismic event details and tsunami threat assessment parsed from NOAA Atom feeds.
    
    Attributes:
        bulletin_id (str)
        feed (FeedEnum)
        center (typing.Optional[str])
        title (str)
        updated (datetime.datetime)
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        category (typing.Optional[CategoryEnum])
        magnitude (typing.Optional[str])
        affected_region (typing.Optional[str])
        note (typing.Optional[str])
        bulletin_url (typing.Optional[str])
        cap_url (typing.Optional[str])
    """
    
    
    bulletin_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bulletin_id"))
    feed: FeedEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feed"))
    center: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="center"))
    title: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    updated: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    category: typing.Optional[CategoryEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    magnitude: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="magnitude"))
    affected_region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="affected_region"))
    note: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="note"))
    bulletin_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bulletin_url"))
    cap_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cap_url"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TsunamiBulletin':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TsunamiBulletin']:
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
                return TsunamiBulletin.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'TsunamiBulletin':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            bulletin_id='zozvsmsrgjgktarutdmt',
            feed=FeedEnum.PAAQ,
            center='sibnzudbaclrhfuexlph',
            title='vxdjuxgpawgcvateuuyf',
            updated=datetime.datetime.now(datetime.timezone.utc),
            latitude=float(54.25712874733606),
            longitude=float(35.3821450592146),
            category=CategoryEnum.Warning,
            magnitude='bisyvvloqafiboemhasb',
            affected_region='lakedmqruinfvlicibzc',
            note='txksothxhcpsockkiqte',
            bulletin_url='ghfbigpxkbsztxukaiqg',
            cap_url='eyrtmknwpqvhpqksilti'
        )