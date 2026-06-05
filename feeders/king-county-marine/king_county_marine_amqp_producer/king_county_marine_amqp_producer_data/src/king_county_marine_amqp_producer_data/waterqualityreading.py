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
    A transport update from King County Metro marine feeds. It carries marine transit schedule and status updates for King County water-taxi routes and sailings.
    
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
            station_id='dinvkscmzhwlxtusxjgr',
            station_name='vbmfgzzlnzagrpxqjede',
            observation_time='fcdsgspqqrwcbmnwrnoi',
            water_temperature_c=float(97.20251511363985),
            conductivity_s_m=float(5.362811896633146),
            pressure_dbar=float(33.44230830094127),
            dissolved_oxygen_mg_l=float(85.46629539707949),
            ph=float(88.93776827583036),
            chlorophyll_ug_l=float(88.18424654691182),
            turbidity_ntu=float(70.89392227142561),
            chlorophyll_stddev_ug_l=float(76.03940418751013),
            turbidity_stddev_ntu=float(50.475205078336835),
            salinity_psu=float(73.42911851601094),
            specific_conductivity_s_m=float(44.722378517045044),
            dissolved_oxygen_saturation_pct=float(44.337654374289556),
            nitrate_umol=float(89.03541103602304),
            nitrate_mg_l=float(58.614979585446356),
            wind_direction_deg=float(26.991791187487024),
            wind_speed_m_s=float(53.69964001765367),
            photosynthetically_active_radiation_umol_s_m2=float(54.81545934780201),
            air_temperature_f=float(25.349891414851953),
            air_humidity_pct=float(54.73842533768307),
            air_pressure_in_hg=float(50.03021119318145),
            system_battery_v=float(82.06549959939647),
            sensor_battery_v=float(65.90198397258601)
        )