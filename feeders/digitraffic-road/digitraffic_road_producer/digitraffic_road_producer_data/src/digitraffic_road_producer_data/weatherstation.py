""" WeatherStation dataclass. """

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
class WeatherStation:
    """
    Road weather station metadata from the Finnish national road network operated by Fintraffic. Over 350 road weather stations measure atmospheric and road surface conditions. Station metadata includes geographic location, road address, municipality, sensor list, collection parameters, and administrative details. This reference data contextualizes the real-time WeatherSensorData telemetry events and is fetched from the Digitraffic REST API at https://tie.digitraffic.fi/api/weather/v1/stations. See https://www.digitraffic.fi/en/road-traffic/ for full documentation.
    
    Attributes:
        station_id (int)
        name (str)
        names_fi (typing.Optional[str])
        names_sv (typing.Optional[str])
        names_en (typing.Optional[str])
        longitude (float)
        latitude (float)
        altitude (typing.Optional[float])
        municipality (str)
        municipality_code (int)
        province (str)
        province_code (int)
        road_number (int)
        road_section (int)
        distance_from_section_start (typing.Optional[int])
        carriageway (typing.Optional[str])
        side (typing.Optional[str])
        contract_area (typing.Optional[str])
        contract_area_code (typing.Optional[int])
        station_type (str)
        master (bool)
        collection_status (str)
        collection_interval (int)
        state (typing.Optional[str])
        start_time (str)
        livi_id (typing.Optional[str])
        sensors (typing.List[int])
        data_updated_time (typing.Optional[str])
    """
    
    
    station_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    names_fi: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="names_fi"))
    names_sv: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="names_sv"))
    names_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="names_en"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    altitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude"))
    municipality: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="municipality"))
    municipality_code: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="municipality_code"))
    province: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="province"))
    province_code: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="province_code"))
    road_number: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_number"))
    road_section: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_section"))
    distance_from_section_start: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="distance_from_section_start"))
    carriageway: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="carriageway"))
    side: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="side"))
    contract_area: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contract_area"))
    contract_area_code: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contract_area_code"))
    station_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_type"))
    master: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="master"))
    collection_status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="collection_status"))
    collection_interval: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="collection_interval"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    start_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    livi_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="livi_id"))
    sensors: typing.List[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensors"))
    data_updated_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_updated_time"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WeatherStation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WeatherStation']:
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
                return WeatherStation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WeatherStation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id=int(35),
            name='ihficlkuolbzdtubrfkr',
            names_fi='cpdkbznnylhigmnpyspq',
            names_sv='xxrbcwtoebiuvdjcrcov',
            names_en='joszvxjbibjttlvbusfo',
            longitude=float(22.36188932627188),
            latitude=float(75.7689500886018),
            altitude=float(85.71589562186816),
            municipality='duoloywyozscdsezdawa',
            municipality_code=int(6),
            province='ozxpmhuiyegvypzrrlfn',
            province_code=int(56),
            road_number=int(69),
            road_section=int(1),
            distance_from_section_start=int(88),
            carriageway='grsbdcabeznvkgvoxhlc',
            side='tjomvvdhaqawhwacecit',
            contract_area='hvppggxusdfsrjmsdatm',
            contract_area_code=int(57),
            station_type='efkwxhbabcqwkxcmioic',
            master=True,
            collection_status='cybofqmnxufifiunykdz',
            collection_interval=int(49),
            state='mlbujtwdsdskvobhsqde',
            start_time='xoxpfvpbcnzmmemciczp',
            livi_id='odeiuktkxiypnvdsvpzn',
            sensors=[int(23), int(90)],
            data_updated_time='teqwrnbkdrpftvpptftk'
        )