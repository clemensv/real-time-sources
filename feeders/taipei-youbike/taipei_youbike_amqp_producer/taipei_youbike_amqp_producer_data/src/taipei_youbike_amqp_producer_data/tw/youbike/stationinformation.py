""" StationInformation dataclass. """

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
class StationInformation:
    """
    Reference record for one Taiwan YouBike 2.0 docking station as returned by the YouBike public station feed `https://apis.youbike.com.tw/json/station-yb2.json`. Identity, bilingual name, administrative district, street address, WGS 84 location, nominal docking capacity, station type, and administrative region codes. YouBike 2.0 is Taiwan's dominant station-based public bike-sharing system with roughly 9,300 stations across Taipei, New Taipei, Taoyuan, Hsinchu, Taichung, Chiayi, Tainan, Kaohsiung, and Pingtung.
    
    Attributes:
        station_id (str)
        name_tw (str)
        name_en (typing.Optional[str])
        name_cn (typing.Optional[str])
        district_tw (typing.Optional[str])
        district_en (typing.Optional[str])
        district_cn (typing.Optional[str])
        address_tw (typing.Optional[str])
        address_en (typing.Optional[str])
        address_cn (typing.Optional[str])
        lat (float)
        lon (float)
        capacity (typing.Optional[int])
        station_type (typing.Optional[int])
        country_code (typing.Optional[str])
        area_code (typing.Optional[str])
        img (typing.Optional[str])
    """
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    name_tw: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name_tw"))
    name_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name_en"))
    name_cn: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name_cn"))
    district_tw: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="district_tw"))
    district_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="district_en"))
    district_cn: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="district_cn"))
    address_tw: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address_tw"))
    address_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address_en"))
    address_cn: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address_cn"))
    lat: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat"))
    lon: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lon"))
    capacity: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="capacity"))
    station_type: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_type"))
    country_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_code"))
    area_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_code"))
    img: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="img"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'StationInformation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['StationInformation']:
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
                return StationInformation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'StationInformation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='zqvnaeyoisogcfqypfrd',
            name_tw='fezboiwjxwmmebybsexm',
            name_en='adsapxoxrlcbcywcgoyz',
            name_cn='lkzvkqxrdtmwrbkabpnl',
            district_tw='kabdosqfgzuclecdxvuj',
            district_en='zfcxklzsilusorhptdhd',
            district_cn='qrlngmnkpkmulmmacaak',
            address_tw='mlzkugcstiashcjrtmlr',
            address_en='eqqkonnhdcseachmnwia',
            address_cn='jojeggmtpxhsbpygfvvl',
            lat=float(16.754200224628015),
            lon=float(11.923907960439895),
            capacity=int(45),
            station_type=int(30),
            country_code='orqabouppqkqztphvhxe',
            area_code='fdzvtygykxrauhwhxrco',
            img='rcetydkksmnplwdazxtv'
        )