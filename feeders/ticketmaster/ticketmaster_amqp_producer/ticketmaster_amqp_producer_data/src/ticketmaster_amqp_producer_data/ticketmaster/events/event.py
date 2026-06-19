""" Event dataclass. """

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
class Event:
    """
    A Ticketmaster event representing a concert, sports match, theater performance, or other live public event. Sourced from the Discovery API v2 /events endpoint.
    
    Attributes:
        event_id (str)
        name (str)
        type (typing.Optional[str])
        url (typing.Optional[str])
        locale (typing.Optional[str])
        start_date (typing.Optional[str])
        start_time (typing.Optional[str])
        start_datetime_local (typing.Optional[str])
        start_datetime_utc (typing.Optional[str])
        status (typing.Optional[str])
        segment_id (typing.Optional[str])
        segment_name (typing.Optional[str])
        genre_id (typing.Optional[str])
        genre_name (typing.Optional[str])
        subgenre_id (typing.Optional[str])
        subgenre_name (typing.Optional[str])
        venue_id (typing.Optional[str])
        venue_name (typing.Optional[str])
        venue_city (typing.Optional[str])
        venue_state_code (typing.Optional[str])
        venue_country_code (typing.Optional[str])
        venue_latitude (typing.Optional[float])
        venue_longitude (typing.Optional[float])
        price_min (typing.Optional[float])
        price_max (typing.Optional[float])
        currency (typing.Optional[str])
        attraction_ids (typing.Optional[str])
        attraction_names (typing.Optional[str])
        onsale_start_datetime (typing.Optional[str])
        onsale_end_datetime (typing.Optional[str])
        info (typing.Optional[str])
        please_note (typing.Optional[str])
    """
    
    
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="type"))
    url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    locale: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="locale"))
    start_date: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_date"))
    start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    start_datetime_local: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_datetime_local"))
    start_datetime_utc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_datetime_utc"))
    status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    segment_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segment_id"))
    segment_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segment_name"))
    genre_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="genre_id"))
    genre_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="genre_name"))
    subgenre_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subgenre_id"))
    subgenre_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subgenre_name"))
    venue_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_id"))
    venue_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_name"))
    venue_city: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_city"))
    venue_state_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_state_code"))
    venue_country_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_country_code"))
    venue_latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_latitude"))
    venue_longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_longitude"))
    price_min: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_min"))
    price_max: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_max"))
    currency: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="currency"))
    attraction_ids: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attraction_ids"))
    attraction_names: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attraction_names"))
    onsale_start_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onsale_start_datetime"))
    onsale_end_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onsale_end_datetime"))
    info: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="info"))
    please_note: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="please_note"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Event':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Event']:
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
                return Event.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Event':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            event_id='xnokjabwuddiztprlwbx',
            name='osiavrtdkrsiphrizhha',
            type='edfiodojpqtcaxilehlh',
            url='ehnqddcgtkpyyqfgpmfr',
            locale='jypaprauyhellgxifotw',
            start_date='nwvgcgxseubzysbecvpd',
            start_time='qvddhqlhtkbpaznurxgx',
            start_datetime_local='mizdmysfbsipqnsbhugi',
            start_datetime_utc='dnvwxpekabrvrsusfwgo',
            status='sghcrgcohxnrigflcamo',
            segment_id='gwlbgkpsxvvdyacivvvz',
            segment_name='mqqcvjqqjpceohefvrgm',
            genre_id='fixjinmnsjobxcrnucyu',
            genre_name='ueyfswswfqeszwwmbixk',
            subgenre_id='wmrpcqjfxrxmpuipicby',
            subgenre_name='qsneyterzylhkbxmbaal',
            venue_id='gthityeczbujbrjuwxkx',
            venue_name='dremhboyjbjnnzlshbgh',
            venue_city='cqobyvzdrwaejdyjjkqn',
            venue_state_code='xyvdqgaetdegipmjjkjg',
            venue_country_code='yzwxxeeeqjxkvqwqvycv',
            venue_latitude=float(72.4638211021218),
            venue_longitude=float(85.98352414584963),
            price_min=float(90.15652554158955),
            price_max=float(35.655828625863975),
            currency='apgrbkqsjcevxvnuzmwe',
            attraction_ids='gkntywwdzwmshdkywwdf',
            attraction_names='ecgthqgfvzfxytuvapuc',
            onsale_start_datetime='hloksrsyyoexdrgejmku',
            onsale_end_datetime='iwvusqrtjqabatmccdsf',
            info='mjhhraemjywuvmclqqlw',
            please_note='jcdsialwjgdnlsowaenb'
        )