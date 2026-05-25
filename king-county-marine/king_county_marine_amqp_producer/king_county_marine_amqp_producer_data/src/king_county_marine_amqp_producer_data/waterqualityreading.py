""" WaterQualityReading dataclass. """

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
class WaterQualityReading:
    """
    Normalized King County buoy or mooring reading carrying the documented water-quality and weather measurements published by the current raw-data datasets.
    
    Attributes:
        station_id (str)
        station_name (str)
        observation_time (str)
        water_temperature_c (typing.Optional[float])
        conductivity_s_m (typing.Optional[float])
        pressure_dbar (typing.Optional[float])
        dissolved_oxygen_mg_l (typing.Optional[float])
        ph (typing.Optional[float])
        chlorophyll_ug_l (typing.Optional[float])
        turbidity_ntu (typing.Optional[float])
        chlorophyll_stddev_ug_l (typing.Optional[float])
        turbidity_stddev_ntu (typing.Optional[float])
        salinity_psu (typing.Optional[float])
        specific_conductivity_s_m (typing.Optional[float])
        dissolved_oxygen_saturation_pct (typing.Optional[float])
        nitrate_umol (typing.Optional[float])
        nitrate_mg_l (typing.Optional[float])
        wind_direction_deg (typing.Optional[float])
        wind_speed_m_s (typing.Optional[float])
        photosynthetically_active_radiation_umol_s_m2 (typing.Optional[float])
        air_temperature_f (typing.Optional[float])
        air_humidity_pct (typing.Optional[float])
        air_pressure_in_hg (typing.Optional[float])
        system_battery_v (typing.Optional[float])
        sensor_battery_v (typing.Optional[float])
    """
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    observation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time"))
    water_temperature_c: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_temperature_c"))
    conductivity_s_m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="conductivity_s_m"))
    pressure_dbar: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_dbar"))
    dissolved_oxygen_mg_l: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dissolved_oxygen_mg_l"))
    ph: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ph"))
    chlorophyll_ug_l: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="chlorophyll_ug_l"))
    turbidity_ntu: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="turbidity_ntu"))
    chlorophyll_stddev_ug_l: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="chlorophyll_stddev_ug_l"))
    turbidity_stddev_ntu: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="turbidity_stddev_ntu"))
    salinity_psu: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="salinity_psu"))
    specific_conductivity_s_m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="specific_conductivity_s_m"))
    dissolved_oxygen_saturation_pct: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dissolved_oxygen_saturation_pct"))
    nitrate_umol: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nitrate_umol"))
    nitrate_mg_l: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nitrate_mg_l"))
    wind_direction_deg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction_deg"))
    wind_speed_m_s: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed_m_s"))
    photosynthetically_active_radiation_umol_s_m2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="photosynthetically_active_radiation_umol_s_m2"))
    air_temperature_f: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_temperature_f"))
    air_humidity_pct: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_humidity_pct"))
    air_pressure_in_hg: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_pressure_in_hg"))
    system_battery_v: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="system_battery_v"))
    sensor_battery_v: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_battery_v"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WaterQualityReading':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WaterQualityReading']:
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
                return WaterQualityReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WaterQualityReading':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='xgjexukvjfbilaucufgr',
            station_name='fjymfoafvjeyiulwjnwb',
            observation_time='pjgkgckfvwwntspafooq',
            water_temperature_c=float(48.77456045397357),
            conductivity_s_m=float(37.266055331041606),
            pressure_dbar=float(44.861332221535555),
            dissolved_oxygen_mg_l=float(92.5267414439993),
            ph=float(83.17600478322025),
            chlorophyll_ug_l=float(94.04027506527905),
            turbidity_ntu=float(44.088321111976015),
            chlorophyll_stddev_ug_l=float(76.14315154843737),
            turbidity_stddev_ntu=float(86.5310663422413),
            salinity_psu=float(50.338343930760345),
            specific_conductivity_s_m=float(25.5135980900531),
            dissolved_oxygen_saturation_pct=float(48.86976785782298),
            nitrate_umol=float(82.53309603309027),
            nitrate_mg_l=float(25.983211491705116),
            wind_direction_deg=float(20.816425048829068),
            wind_speed_m_s=float(47.14336665581882),
            photosynthetically_active_radiation_umol_s_m2=float(13.543481251644419),
            air_temperature_f=float(19.598605013524974),
            air_humidity_pct=float(18.109443226101263),
            air_pressure_in_hg=float(41.72443009486676),
            system_battery_v=float(86.38391676066604),
            sensor_battery_v=float(2.083432892778081)
        )