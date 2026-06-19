""" PublicPower dataclass. """

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
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PublicPower:
    """
    Net electricity generation by fuel type for a given country at a specific 15-minute interval. Sourced from the Energy-Charts /public_power endpoint (Fraunhofer ISE) which aggregates ENTSO-E transparency platform data. Each record represents one timestamp in the parallel-array response, with individual production types flattened into named fields in megawatts (MW). Negative values for hydro pumped storage consumption and cross-border trading indicate consumption or export. The renewable_share_of_generation and renewable_share_of_load fields are percentages (0–100). Load represents total grid demand.
    
    Attributes:
        country (str)
        timestamp (datetime.datetime)
        unix_seconds (int)
        hydro_pumped_storage_consumption_mw (typing.Optional[float])
        cross_border_electricity_trading_mw (typing.Optional[float])
        hydro_run_of_river_mw (typing.Optional[float])
        biomass_mw (typing.Optional[float])
        fossil_brown_coal_lignite_mw (typing.Optional[float])
        fossil_hard_coal_mw (typing.Optional[float])
        fossil_oil_mw (typing.Optional[float])
        fossil_coal_derived_gas_mw (typing.Optional[float])
        fossil_gas_mw (typing.Optional[float])
        geothermal_mw (typing.Optional[float])
        hydro_water_reservoir_mw (typing.Optional[float])
        hydro_pumped_storage_mw (typing.Optional[float])
        others_mw (typing.Optional[float])
        waste_mw (typing.Optional[float])
        wind_offshore_mw (typing.Optional[float])
        wind_onshore_mw (typing.Optional[float])
        solar_mw (typing.Optional[float])
        nuclear_mw (typing.Optional[float])
        load_mw (typing.Optional[float])
        residual_load_mw (typing.Optional[float])
        renewable_share_of_generation_pct (typing.Optional[float])
        renewable_share_of_load_pct (typing.Optional[float])
    """
    
    
    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    unix_seconds: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unix_seconds", encoder=lambda v: str(v) if v is not None else None, decoder=lambda v: int(v) if isinstance(v, str) else v))
    hydro_pumped_storage_consumption_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hydro_pumped_storage_consumption_mw"))
    cross_border_electricity_trading_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cross_border_electricity_trading_mw"))
    hydro_run_of_river_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hydro_run_of_river_mw"))
    biomass_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="biomass_mw"))
    fossil_brown_coal_lignite_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fossil_brown_coal_lignite_mw"))
    fossil_hard_coal_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fossil_hard_coal_mw"))
    fossil_oil_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fossil_oil_mw"))
    fossil_coal_derived_gas_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fossil_coal_derived_gas_mw"))
    fossil_gas_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fossil_gas_mw"))
    geothermal_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geothermal_mw"))
    hydro_water_reservoir_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hydro_water_reservoir_mw"))
    hydro_pumped_storage_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hydro_pumped_storage_mw"))
    others_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="others_mw"))
    waste_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="waste_mw"))
    wind_offshore_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_offshore_mw"))
    wind_onshore_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_onshore_mw"))
    solar_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="solar_mw"))
    nuclear_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nuclear_mw"))
    load_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="load_mw"))
    residual_load_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="residual_load_mw"))
    renewable_share_of_generation_pct: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="renewable_share_of_generation_pct"))
    renewable_share_of_load_pct: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="renewable_share_of_load_pct"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PublicPower':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        if 'unix_seconds' in data and isinstance(data['unix_seconds'], str):
            data['unix_seconds'] = int(data['unix_seconds'])
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        if 'unix_seconds' in asdict_result and asdict_result['unix_seconds'] is not None:
            asdict_result['unix_seconds'] = str(asdict_result['unix_seconds'])
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PublicPower']:
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
                return PublicPower.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'PublicPower':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            country='cwdtsllrhjkidgezcyto',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(76),
            hydro_pumped_storage_consumption_mw=float(74.2151705902063),
            cross_border_electricity_trading_mw=float(32.093777071939854),
            hydro_run_of_river_mw=float(5.7400638051479),
            biomass_mw=float(47.71488904607214),
            fossil_brown_coal_lignite_mw=float(58.43176274564526),
            fossil_hard_coal_mw=float(71.9353466436519),
            fossil_oil_mw=float(34.0832135324627),
            fossil_coal_derived_gas_mw=float(24.973796978251638),
            fossil_gas_mw=float(83.87053376099516),
            geothermal_mw=float(29.321902867196414),
            hydro_water_reservoir_mw=float(94.20175616792243),
            hydro_pumped_storage_mw=float(73.16456292550775),
            others_mw=float(28.565722511680747),
            waste_mw=float(46.18823805176289),
            wind_offshore_mw=float(52.172115018193836),
            wind_onshore_mw=float(96.6346753126622),
            solar_mw=float(93.12767508694067),
            nuclear_mw=float(31.19034156681093),
            load_mw=float(31.384008731437685),
            residual_load_mw=float(59.64968836790896),
            renewable_share_of_generation_pct=float(95.6762410502686),
            renewable_share_of_load_pct=float(76.22615227512345)
        )