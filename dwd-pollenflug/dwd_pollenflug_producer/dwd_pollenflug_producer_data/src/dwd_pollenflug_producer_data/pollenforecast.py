""" PollenForecast dataclass. """

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
class PollenForecast:
    """
    Daily pollen forecast for a single German region or sub-region, published by the Deutscher Wetterdienst (DWD). Contains intensity values for eight pollen types across three forecast days (today, tomorrow, day after tomorrow). Intensity is on a scale from 0 (no load) to 3 (high load) with intermediate half-step ranges such as '0-1', '1-2', '2-3'. The bridge maps the German pollen names from the upstream API to English equivalents.
    
    Attributes:
        region_id (int)
        region_name (str)
        last_update (str)
        next_update (str)
        sender (typing.Optional[str])
        hazel_today (typing.Optional[str])
        hazel_tomorrow (typing.Optional[str])
        hazel_dayafter_to (typing.Optional[str])
        alder_today (typing.Optional[str])
        alder_tomorrow (typing.Optional[str])
        alder_dayafter_to (typing.Optional[str])
        birch_today (typing.Optional[str])
        birch_tomorrow (typing.Optional[str])
        birch_dayafter_to (typing.Optional[str])
        ash_today (typing.Optional[str])
        ash_tomorrow (typing.Optional[str])
        ash_dayafter_to (typing.Optional[str])
        grasses_today (typing.Optional[str])
        grasses_tomorrow (typing.Optional[str])
        grasses_dayafter_to (typing.Optional[str])
        rye_today (typing.Optional[str])
        rye_tomorrow (typing.Optional[str])
        rye_dayafter_to (typing.Optional[str])
        mugwort_today (typing.Optional[str])
        mugwort_tomorrow (typing.Optional[str])
        mugwort_dayafter_to (typing.Optional[str])
        ragweed_today (typing.Optional[str])
        ragweed_tomorrow (typing.Optional[str])
        ragweed_dayafter_to (typing.Optional[str])
    """
    
    
    region_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region_id"))
    region_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region_name"))
    last_update: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="last_update"))
    next_update: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="next_update"))
    sender: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sender"))
    hazel_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hazel_today"))
    hazel_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hazel_tomorrow"))
    hazel_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hazel_dayafter_to"))
    alder_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alder_today"))
    alder_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alder_tomorrow"))
    alder_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alder_dayafter_to"))
    birch_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="birch_today"))
    birch_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="birch_tomorrow"))
    birch_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="birch_dayafter_to"))
    ash_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ash_today"))
    ash_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ash_tomorrow"))
    ash_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ash_dayafter_to"))
    grasses_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="grasses_today"))
    grasses_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="grasses_tomorrow"))
    grasses_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="grasses_dayafter_to"))
    rye_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rye_today"))
    rye_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rye_tomorrow"))
    rye_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rye_dayafter_to"))
    mugwort_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mugwort_today"))
    mugwort_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mugwort_tomorrow"))
    mugwort_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mugwort_dayafter_to"))
    ragweed_today: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ragweed_today"))
    ragweed_tomorrow: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ragweed_tomorrow"))
    ragweed_dayafter_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ragweed_dayafter_to"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PollenForecast':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PollenForecast']:
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
                return PollenForecast.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'PollenForecast':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            region_id=int(38),
            region_name='mibeaybvhfrbaesyuwhw',
            last_update='zkxhjztpfywjhywdzwcm',
            next_update='ahsxvoplkkzodcwoakjd',
            sender='ygffiaitdavchyboxixe',
            hazel_today='tsbrajujiwofujizzjys',
            hazel_tomorrow='ynsftgzdxlxvfwbdabxj',
            hazel_dayafter_to='kzypledpklqziiydtilc',
            alder_today='iwgdazwprgryapebqctr',
            alder_tomorrow='qonthetpwjyqzlomveoj',
            alder_dayafter_to='spmkxbokmosytzlazavy',
            birch_today='eocsannertigxehevrvd',
            birch_tomorrow='zzonetnhdzpkvksburxb',
            birch_dayafter_to='eufpdvffcxlmhnfscqnv',
            ash_today='gjqodvqqvbeorfvvbcrz',
            ash_tomorrow='bxjzushvvibwddclplpr',
            ash_dayafter_to='tapnaqpicpfxbsgzezzp',
            grasses_today='vdrtybjahsxwttjsfvzy',
            grasses_tomorrow='zsqlwkevumvvizkewvdj',
            grasses_dayafter_to='pgqngouvmvnllxflbsnf',
            rye_today='ucqqjahduqikvbhuqgun',
            rye_tomorrow='eqyrcwncxisxyktnvqlg',
            rye_dayafter_to='jkplcimkqxfwroddfdkv',
            mugwort_today='wrkctvhjhblomaevhpml',
            mugwort_tomorrow='bcythmtyiodoyqirgozq',
            mugwort_dayafter_to='fdcrjaeelesdgfmbkrhu',
            ragweed_today='ljyxcquqaxodgcbpkdxz',
            ragweed_tomorrow='vkkdgoiuiamuanenfaos',
            ragweed_dayafter_to='oekzpotwmcudnkqmtexk'
        )