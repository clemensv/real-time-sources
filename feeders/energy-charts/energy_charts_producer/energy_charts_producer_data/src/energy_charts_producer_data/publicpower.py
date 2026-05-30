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
import avro.schema
import avro.io
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
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"PublicPower\", \"doc\": \"Net electricity generation by fuel type for a given country at a specific 15-minute interval. Sourced from the Energy-Charts /public_power endpoint (Fraunhofer ISE) which aggregates ENTSO-E transparency platform data. Each record represents one timestamp in the parallel-array response, with individual production types flattened into named fields in megawatts (MW). Negative values for hydro pumped storage consumption and cross-border trading indicate consumption or export. The renewable_share_of_generation and renewable_share_of_load fields are percentages (0\u2013100). Load represents total grid demand.\", \"fields\": [{\"name\": \"country\", \"type\": \"string\", \"doc\": \"ISO 3166-1 alpha-2 country code identifying the electricity market area (e.g. 'de' for Germany, 'fr' for France). Used as the query parameter in the Energy-Charts API.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"UTC timestamp derived from the unix_seconds value. Marks the start of the 15-minute measurement interval.\"}, {\"name\": \"unix_seconds\", \"type\": \"long\", \"doc\": \"Unix epoch timestamp in seconds as returned by the Energy-Charts API. Each value corresponds to one row in the parallel arrays of production_types.\"}, {\"name\": \"hydro_pumped_storage_consumption_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net power consumed by pumped-storage hydroelectric plants (MW). Values are typically negative, indicating the plant is pumping water uphill (consuming electricity). Corresponds to the 'Hydro pumped storage consumption' production type.\", \"default\": null}, {\"name\": \"cross_border_electricity_trading_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net cross-border electricity exchange (MW). Positive values indicate net imports; negative values indicate net exports. Corresponds to the 'Cross border electricity trading' production type.\", \"default\": null}, {\"name\": \"hydro_run_of_river_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from run-of-river hydroelectric plants (MW). These plants generate electricity from the natural flow of rivers without significant storage. Corresponds to the 'Hydro Run-of-River' production type.\", \"default\": null}, {\"name\": \"biomass_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from biomass power plants (MW). Includes solid biomass, biogas, and bioliquids. Corresponds to the 'Biomass' production type.\", \"default\": null}, {\"name\": \"fossil_brown_coal_lignite_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from brown coal (lignite) power plants (MW). Lignite is a low-grade coal with high moisture content used primarily in Germany. Corresponds to the 'Fossil brown coal / lignite' production type.\", \"default\": null}, {\"name\": \"fossil_hard_coal_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from hard coal power plants (MW). Hard coal (anthracite/bituminous) has higher energy density than lignite. Corresponds to the 'Fossil hard coal' production type.\", \"default\": null}, {\"name\": \"fossil_oil_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from oil-fired power plants (MW). Includes heavy fuel oil and light oil combustion turbines. Corresponds to the 'Fossil oil' production type.\", \"default\": null}, {\"name\": \"fossil_coal_derived_gas_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from coal-derived gas power plants (MW). Includes blast furnace gas, coke oven gas, and coal mine methane. Corresponds to the 'Fossil coal-derived gas' production type.\", \"default\": null}, {\"name\": \"fossil_gas_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from natural gas power plants (MW). Includes combined-cycle gas turbines (CCGT) and open-cycle gas turbines (OCGT). Corresponds to the 'Fossil gas' production type.\", \"default\": null}, {\"name\": \"geothermal_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from geothermal power plants (MW). Uses heat from the earth's interior to generate electricity. Corresponds to the 'Geothermal' production type.\", \"default\": null}, {\"name\": \"hydro_water_reservoir_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from reservoir hydroelectric plants (MW). These plants store water behind a dam and release it to generate electricity on demand. Corresponds to the 'Hydro water reservoir' production type.\", \"default\": null}, {\"name\": \"hydro_pumped_storage_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from pumped-storage hydroelectric plants when generating (MW). Positive values indicate the plant is releasing stored water to generate electricity. Corresponds to the 'Hydro pumped storage' (generation) production type.\", \"default\": null}, {\"name\": \"others_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from other power sources not classified into specific categories (MW). May include mixed-fuel plants or uncategorized sources. Corresponds to the 'Others' production type.\", \"default\": null}, {\"name\": \"waste_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from waste incineration power plants (MW). Includes municipal solid waste and industrial waste combustion. Corresponds to the 'Waste' production type.\", \"default\": null}, {\"name\": \"wind_offshore_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from offshore wind turbines (MW). Offshore wind farms are located in bodies of water, typically on the continental shelf. Corresponds to the 'Wind offshore' production type.\", \"default\": null}, {\"name\": \"wind_onshore_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from onshore wind turbines (MW). Onshore wind farms are located on land. Corresponds to the 'Wind onshore' production type.\", \"default\": null}, {\"name\": \"solar_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from solar photovoltaic (PV) and concentrated solar power (CSP) plants (MW). Corresponds to the 'Solar' production type.\", \"default\": null}, {\"name\": \"nuclear_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Net generation from nuclear power plants (MW). Not present for all countries (e.g. absent for Germany after nuclear phase-out). Corresponds to the 'Nuclear' production type when available.\", \"default\": null}, {\"name\": \"load_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Total electricity grid load (demand) for the country (MW). Represents the sum of all electricity consumption at the given timestamp. Corresponds to the 'Load' production type.\", \"default\": null}, {\"name\": \"residual_load_mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Residual load (MW). Calculated as total load minus generation from variable renewable sources (wind and solar). A high residual load indicates that conventional or dispatchable power plants must cover most of the demand. Corresponds to the 'Residual load' production type.\", \"default\": null}, {\"name\": \"renewable_share_of_generation_pct\", \"type\": [\"double\", \"null\"], \"doc\": \"Percentage of total electricity generation that comes from renewable sources (0\u2013100). Calculated by dividing renewable generation by total generation. Corresponds to the 'Renewable share of generation' production type.\", \"default\": null}, {\"name\": \"renewable_share_of_load_pct\", \"type\": [\"double\", \"null\"], \"doc\": \"Percentage of the total grid load that is covered by renewable generation (0\u2013100). Calculated by dividing renewable generation by total load. Corresponds to the 'Renewable share of load' production type.\", \"default\": null}]}"
    )
    
    
    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    unix_seconds: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unix_seconds"))
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
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'PublicPower':
        """
        Converts a dictionary from Avro deserialization to a dataclass instance.
        Handles conversion of string representations back to Python types for
        extended logical types.
        
        Args:
            data: The dictionary from Avro deserialization.
        
        Returns:
            The dataclass representation.
        """
        # Convert string values back to Python types for Avro string-based logical types
        converted = data.copy()
        if 'country' in converted and converted['country'] is not None:
            value = converted['country']
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, str):
                converted['timestamp'] = datetime.datetime.fromisoformat(value)
        if 'unix_seconds' in converted and converted['unix_seconds'] is not None:
            value = converted['unix_seconds']
        if 'hydro_pumped_storage_consumption_mw' in converted and converted['hydro_pumped_storage_consumption_mw'] is not None:
            value = converted['hydro_pumped_storage_consumption_mw']
        if 'cross_border_electricity_trading_mw' in converted and converted['cross_border_electricity_trading_mw'] is not None:
            value = converted['cross_border_electricity_trading_mw']
        if 'hydro_run_of_river_mw' in converted and converted['hydro_run_of_river_mw'] is not None:
            value = converted['hydro_run_of_river_mw']
        if 'biomass_mw' in converted and converted['biomass_mw'] is not None:
            value = converted['biomass_mw']
        if 'fossil_brown_coal_lignite_mw' in converted and converted['fossil_brown_coal_lignite_mw'] is not None:
            value = converted['fossil_brown_coal_lignite_mw']
        if 'fossil_hard_coal_mw' in converted and converted['fossil_hard_coal_mw'] is not None:
            value = converted['fossil_hard_coal_mw']
        if 'fossil_oil_mw' in converted and converted['fossil_oil_mw'] is not None:
            value = converted['fossil_oil_mw']
        if 'fossil_coal_derived_gas_mw' in converted and converted['fossil_coal_derived_gas_mw'] is not None:
            value = converted['fossil_coal_derived_gas_mw']
        if 'fossil_gas_mw' in converted and converted['fossil_gas_mw'] is not None:
            value = converted['fossil_gas_mw']
        if 'geothermal_mw' in converted and converted['geothermal_mw'] is not None:
            value = converted['geothermal_mw']
        if 'hydro_water_reservoir_mw' in converted and converted['hydro_water_reservoir_mw'] is not None:
            value = converted['hydro_water_reservoir_mw']
        if 'hydro_pumped_storage_mw' in converted and converted['hydro_pumped_storage_mw'] is not None:
            value = converted['hydro_pumped_storage_mw']
        if 'others_mw' in converted and converted['others_mw'] is not None:
            value = converted['others_mw']
        if 'waste_mw' in converted and converted['waste_mw'] is not None:
            value = converted['waste_mw']
        if 'wind_offshore_mw' in converted and converted['wind_offshore_mw'] is not None:
            value = converted['wind_offshore_mw']
        if 'wind_onshore_mw' in converted and converted['wind_onshore_mw'] is not None:
            value = converted['wind_onshore_mw']
        if 'solar_mw' in converted and converted['solar_mw'] is not None:
            value = converted['solar_mw']
        if 'nuclear_mw' in converted and converted['nuclear_mw'] is not None:
            value = converted['nuclear_mw']
        if 'load_mw' in converted and converted['load_mw'] is not None:
            value = converted['load_mw']
        if 'residual_load_mw' in converted and converted['residual_load_mw'] is not None:
            value = converted['residual_load_mw']
        if 'renewable_share_of_generation_pct' in converted and converted['renewable_share_of_generation_pct'] is not None:
            value = converted['renewable_share_of_generation_pct']
        if 'renewable_share_of_load_pct' in converted and converted['renewable_share_of_load_pct'] is not None:
            value = converted['renewable_share_of_load_pct']
        
        return cls(**converted)

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

    def to_avro_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary suitable for Avro serialization.
        Handles conversion of Python types to Avro-compatible string representations
        for extended logical types.

        Returns:
            The dictionary representation suitable for Avro serialization.
        """
        result = self.to_serializer_dict()
        converted = result.copy()
        
        # Convert specific fields based on their source types
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, datetime.datetime):
                converted['timestamp'] = value.isoformat()
        
        return converted

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'application/json': Encodes the data to JSON format.
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
                Supported content type extensions:
                    '+gzip': Compresses the byte array using gzip, e.g. 'application/json+gzip'.

        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        result = None
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            # Convert to Avro binary format using the embedded schema
            writer = avro.io.DatumWriter(self.AvroType)
            with io.BytesIO() as stream:
                encoder = avro.io.BinaryEncoder(stream)
                writer.write(self.to_avro_dict(), encoder)
                result = stream.getvalue()
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PublicPower']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'application/json': Attempts to decode the data from JSON encoded format.
                    'avro/binary': Attempts to decode the data from Avro binary format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            if isinstance(data, bytes):
                # Decode from Avro binary format using the embedded schema
                reader = avro.io.DatumReader(cls.AvroType)
                with io.BytesIO(data) as stream:
                    decoder = avro.io.BinaryDecoder(stream)
                    _record = reader.read(decoder)
                    return PublicPower.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
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
            country='vzunxzucrjmecgbvplov',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(61),
            hydro_pumped_storage_consumption_mw=float(30.17663783772837),
            cross_border_electricity_trading_mw=float(40.91244433376172),
            hydro_run_of_river_mw=float(30.737141188931894),
            biomass_mw=float(89.99621506661262),
            fossil_brown_coal_lignite_mw=float(55.12713951352119),
            fossil_hard_coal_mw=float(26.10951404334618),
            fossil_oil_mw=float(88.78399079816805),
            fossil_coal_derived_gas_mw=float(93.36397028304091),
            fossil_gas_mw=float(68.7738171449079),
            geothermal_mw=float(64.32399620191555),
            hydro_water_reservoir_mw=float(66.44622792369516),
            hydro_pumped_storage_mw=float(73.89784041776832),
            others_mw=float(72.00679450888062),
            waste_mw=float(21.39032318976224),
            wind_offshore_mw=float(14.52012714198412),
            wind_onshore_mw=float(49.4625207536421),
            solar_mw=float(32.42710410469362),
            nuclear_mw=float(39.82425326053508),
            load_mw=float(37.5068075533941),
            residual_load_mw=float(22.23252227692516),
            renewable_share_of_generation_pct=float(34.762798988493536),
            renewable_share_of_load_pct=float(70.02987540892885)
        )