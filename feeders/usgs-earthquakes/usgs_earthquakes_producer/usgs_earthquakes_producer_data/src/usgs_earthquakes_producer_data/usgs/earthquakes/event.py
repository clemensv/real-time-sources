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
    USGS earthquake event data from the Earthquake Hazards Program.
    
    Attributes:
        id (str)
        magnitude (typing.Optional[float])
        mag_type (typing.Optional[str])
        place (typing.Optional[str])
        event_time (str)
        updated (str)
        url (typing.Optional[str])
        detail_url (typing.Optional[str])
        felt (typing.Optional[int])
        cdi (typing.Optional[float])
        mmi (typing.Optional[float])
        alert (typing.Optional[str])
        status (str)
        tsunami (int)
        sig (typing.Optional[int])
        net (str)
        code (str)
        sources (typing.Optional[str])
        nst (typing.Optional[int])
        dmin (typing.Optional[float])
        rms (typing.Optional[float])
        gap (typing.Optional[float])
        event_type (typing.Optional[str])
        latitude (float)
        longitude (float)
        depth (typing.Optional[float])
        magnitude_bucket (str)
    """
    
    
    id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    magnitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="magnitude"))
    mag_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mag_type"))
    place: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="place"))
    event_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_time"))
    updated: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated"))
    url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    detail_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="detail_url"))
    felt: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="felt"))
    cdi: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cdi"))
    mmi: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmi"))
    alert: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert"))
    status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    tsunami: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tsunami"))
    sig: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sig"))
    net: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="net"))
    code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code"))
    sources: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sources"))
    nst: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nst"))
    dmin: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dmin"))
    rms: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rms"))
    gap: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gap"))
    event_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_type"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    depth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="depth"))
    magnitude_bucket: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="magnitude_bucket"))

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
            id='ugfvejcrlqllefpspfyf',
            magnitude=float(19.2869532535221),
            mag_type='chsscdgsfhhagtopwutz',
            place='ucylfymgpbisfctzpwxk',
            event_time='gtbzrbwnalpyuchucggq',
            updated='gfpyowdxlcjffzemaqrd',
            url='gfukhjrgbeljvfhuiqdy',
            detail_url='pinhrbwyrbuyracfbqze',
            felt=int(0),
            cdi=float(33.22554433980667),
            mmi=float(33.295593051573825),
            alert='ovldswqmetwvsxfmzbfa',
            status='grbmsmmstsbnhkqhxedk',
            tsunami=int(20),
            sig=int(99),
            net='mcrbogmkvqghsdtheevj',
            code='zlhefpxliwhtbtzdjfyn',
            sources='yytaywgvycbxhkxeuqzr',
            nst=int(75),
            dmin=float(11.640702276192272),
            rms=float(49.482617695850294),
            gap=float(64.57920062824157),
            event_type='txismxnbzwqxoipsviju',
            latitude=float(60.26969425739552),
            longitude=float(42.85005448875439),
            depth=float(5.682403687610982),
            magnitude_bucket='hkbuumdhqhuzlcucamxj'
        )