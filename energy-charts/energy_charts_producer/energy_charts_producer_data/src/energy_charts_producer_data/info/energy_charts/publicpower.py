""" PublicPower dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import json
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import avro.schema
import avro.name
import avro.io
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PublicPower:
    """
    A PublicPower record.
    Attributes:
        country (str): 
        timestamp (datetime.datetime): 
        unix_seconds (int): 
        hydro_pumped_storage_consumption_mw (typing.Optional[float]): 
        cross_border_electricity_trading_mw (typing.Optional[float]): 
        hydro_run_of_river_mw (typing.Optional[float]): 
        biomass_mw (typing.Optional[float]): 
        fossil_brown_coal_lignite_mw (typing.Optional[float]): 
        fossil_hard_coal_mw (typing.Optional[float]): 
        fossil_oil_mw (typing.Optional[float]): 
        fossil_coal_derived_gas_mw (typing.Optional[float]): 
        fossil_gas_mw (typing.Optional[float]): 
        geothermal_mw (typing.Optional[float]): 
        hydro_water_reservoir_mw (typing.Optional[float]): 
        hydro_pumped_storage_mw (typing.Optional[float]): 
        others_mw (typing.Optional[float]): 
        waste_mw (typing.Optional[float]): 
        wind_offshore_mw (typing.Optional[float]): 
        wind_onshore_mw (typing.Optional[float]): 
        solar_mw (typing.Optional[float]): 
        nuclear_mw (typing.Optional[float]): 
        load_mw (typing.Optional[float]): 
        residual_load_mw (typing.Optional[float]): 
        renewable_share_of_generation_pct (typing.Optional[float]): 
        renewable_share_of_load_pct (typing.Optional[float]): """
    
    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
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
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"PublicPower\", \"namespace\": \"info.energy_charts\", \"fields\": [{\"name\": \"country\", \"type\": \"string\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}}, {\"name\": \"unix_seconds\", \"type\": \"long\"}, {\"name\": \"hydro_pumped_storage_consumption_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"cross_border_electricity_trading_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"hydro_run_of_river_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"biomass_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"fossil_brown_coal_lignite_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"fossil_hard_coal_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"fossil_oil_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"fossil_coal_derived_gas_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"fossil_gas_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"geothermal_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"hydro_water_reservoir_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"hydro_pumped_storage_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"others_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"waste_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"wind_offshore_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"wind_onshore_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"solar_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"nuclear_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"load_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"residual_load_mw\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"renewable_share_of_generation_pct\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"renewable_share_of_load_pct\", \"type\": [\"null\", \"double\"], \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.country=str(self.country)
        value_timestamp = self.timestamp
        self.timestamp = value_timestamp
        self.unix_seconds=int(self.unix_seconds)
        self.hydro_pumped_storage_consumption_mw=float(self.hydro_pumped_storage_consumption_mw) if self.hydro_pumped_storage_consumption_mw else None
        self.cross_border_electricity_trading_mw=float(self.cross_border_electricity_trading_mw) if self.cross_border_electricity_trading_mw else None
        self.hydro_run_of_river_mw=float(self.hydro_run_of_river_mw) if self.hydro_run_of_river_mw else None
        self.biomass_mw=float(self.biomass_mw) if self.biomass_mw else None
        self.fossil_brown_coal_lignite_mw=float(self.fossil_brown_coal_lignite_mw) if self.fossil_brown_coal_lignite_mw else None
        self.fossil_hard_coal_mw=float(self.fossil_hard_coal_mw) if self.fossil_hard_coal_mw else None
        self.fossil_oil_mw=float(self.fossil_oil_mw) if self.fossil_oil_mw else None
        self.fossil_coal_derived_gas_mw=float(self.fossil_coal_derived_gas_mw) if self.fossil_coal_derived_gas_mw else None
        self.fossil_gas_mw=float(self.fossil_gas_mw) if self.fossil_gas_mw else None
        self.geothermal_mw=float(self.geothermal_mw) if self.geothermal_mw else None
        self.hydro_water_reservoir_mw=float(self.hydro_water_reservoir_mw) if self.hydro_water_reservoir_mw else None
        self.hydro_pumped_storage_mw=float(self.hydro_pumped_storage_mw) if self.hydro_pumped_storage_mw else None
        self.others_mw=float(self.others_mw) if self.others_mw else None
        self.waste_mw=float(self.waste_mw) if self.waste_mw else None
        self.wind_offshore_mw=float(self.wind_offshore_mw) if self.wind_offshore_mw else None
        self.wind_onshore_mw=float(self.wind_onshore_mw) if self.wind_onshore_mw else None
        self.solar_mw=float(self.solar_mw) if self.solar_mw else None
        self.nuclear_mw=float(self.nuclear_mw) if self.nuclear_mw else None
        self.load_mw=float(self.load_mw) if self.load_mw else None
        self.residual_load_mw=float(self.residual_load_mw) if self.residual_load_mw else None
        self.renewable_share_of_generation_pct=float(self.renewable_share_of_generation_pct) if self.renewable_share_of_generation_pct else None
        self.renewable_share_of_load_pct=float(self.renewable_share_of_load_pct) if self.renewable_share_of_load_pct else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PublicPower':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
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
            if isinstance(v,enum.Enum):
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
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(self.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
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
                    'avro/binary': Attempts to decode the data from Avro binary encoded format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary encoded format.
                    'avro/json': Attempts to decode the data from Avro JSON encoded format.
                    'application/vnd.apache.avro+json': Attempts to decode the data from Avro JSON encoded format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro', 'avro/json', 'application/vnd.apache.avro+json']:
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for conversion to Stream')
            reader = avro.io.DatumReader(cls.AvroType)
            if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
                decoder = avro.io.BinaryDecoder(stream)
            else:
                raise NotImplementedError(f'Unsupported Avro media type {content_type}')
            _record = reader.read(decoder)            
            return PublicPower.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return PublicPower.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')