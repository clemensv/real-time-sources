""" PowerSystemSnapshot dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PowerSystemSnapshot:
    """
    Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet). Published by the PowerSystemRightNow dataset at approximately 1-minute intervals.
    Attributes:
        minutes1_utc (str): UTC timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format.
        minutes1_dk (str): Danish local-time timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format.
        price_area (str): Price area code. Set to 'DK' for system-wide power system snapshots.
        co2_emission (typing.Optional[float]): CO2 emission intensity in g/kWh.
        production_ge_100mw (typing.Optional[float]): Production from plants >= 100 MW in MW.
        production_lt_100mw (typing.Optional[float]): Production from plants < 100 MW in MW.
        solar_power (typing.Optional[float]): Solar PV production in MW.
        offshore_wind_power (typing.Optional[float]): Offshore wind production in MW.
        onshore_wind_power (typing.Optional[float]): Onshore wind production in MW.
        exchange_sum (typing.Optional[float]): Net total cross-border exchange in MW.
        exchange_dk1_de (typing.Optional[float]): DK1-Germany exchange in MW.
        exchange_dk1_nl (typing.Optional[float]): DK1-Netherlands exchange in MW.
        exchange_dk1_gb (typing.Optional[float]): DK1-Great Britain exchange in MW.
        exchange_dk1_no (typing.Optional[float]): DK1-Norway exchange in MW.
        exchange_dk1_se (typing.Optional[float]): DK1-Sweden exchange in MW.
        exchange_dk1_dk2 (typing.Optional[float]): DK1-DK2 (Great Belt) exchange in MW.
        exchange_dk2_de (typing.Optional[float]): DK2-Germany exchange in MW.
        exchange_dk2_se (typing.Optional[float]): DK2-Sweden exchange in MW.
        exchange_bornholm_se (typing.Optional[float]): Bornholm-Sweden exchange in MW.
        afrr_activated_dk1 (typing.Optional[float]): aFRR activated in DK1 in MW.
        afrr_activated_dk2 (typing.Optional[float]): aFRR activated in DK2 in MW.
        mfrr_activated_dk1 (typing.Optional[float]): mFRR activated in DK1 in MW.
        mfrr_activated_dk2 (typing.Optional[float]): mFRR activated in DK2 in MW.
        imbalance_dk1 (typing.Optional[float]): Grid imbalance in DK1 in MW.
        imbalance_dk2 (typing.Optional[float]): Grid imbalance in DK2 in MW."""
    
    minutes1_utc: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="minutes1_utc"))
    minutes1_dk: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="minutes1_dk"))
    price_area: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_area"))
    co2_emission: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="co2_emission"))
    production_ge_100mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="production_ge_100mw"))
    production_lt_100mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="production_lt_100mw"))
    solar_power: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="solar_power"))
    offshore_wind_power: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="offshore_wind_power"))
    onshore_wind_power: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onshore_wind_power"))
    exchange_sum: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_sum"))
    exchange_dk1_de: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_de"))
    exchange_dk1_nl: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_nl"))
    exchange_dk1_gb: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_gb"))
    exchange_dk1_no: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_no"))
    exchange_dk1_se: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_se"))
    exchange_dk1_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_dk2"))
    exchange_dk2_de: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk2_de"))
    exchange_dk2_se: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk2_se"))
    exchange_bornholm_se: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_bornholm_se"))
    afrr_activated_dk1: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="afrr_activated_dk1"))
    afrr_activated_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="afrr_activated_dk2"))
    mfrr_activated_dk1: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mfrr_activated_dk1"))
    mfrr_activated_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mfrr_activated_dk2"))
    imbalance_dk1: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imbalance_dk1"))
    imbalance_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imbalance_dk2"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"PowerSystemSnapshot\", \"namespace\": \"dk.energinet.energidataservice\", \"doc\": \"Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet). Published by the PowerSystemRightNow dataset at approximately 1-minute intervals.\", \"fields\": [{\"name\": \"minutes1_utc\", \"type\": \"string\", \"doc\": \"UTC timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format.\"}, {\"name\": \"minutes1_dk\", \"type\": \"string\", \"doc\": \"Danish local-time timestamp of the snapshot rounded to the nearest minute, in ISO 8601 format.\"}, {\"name\": \"price_area\", \"type\": \"string\", \"doc\": \"Price area code. Set to 'DK' for system-wide power system snapshots.\"}, {\"name\": \"co2_emission\", \"type\": [\"double\", \"null\"], \"doc\": \"CO2 emission intensity in g/kWh.\"}, {\"name\": \"production_ge_100mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Production from plants >= 100 MW in MW.\"}, {\"name\": \"production_lt_100mw\", \"type\": [\"double\", \"null\"], \"doc\": \"Production from plants < 100 MW in MW.\"}, {\"name\": \"solar_power\", \"type\": [\"double\", \"null\"], \"doc\": \"Solar PV production in MW.\"}, {\"name\": \"offshore_wind_power\", \"type\": [\"double\", \"null\"], \"doc\": \"Offshore wind production in MW.\"}, {\"name\": \"onshore_wind_power\", \"type\": [\"double\", \"null\"], \"doc\": \"Onshore wind production in MW.\"}, {\"name\": \"exchange_sum\", \"type\": [\"double\", \"null\"], \"doc\": \"Net total cross-border exchange in MW.\"}, {\"name\": \"exchange_dk1_de\", \"type\": [\"double\", \"null\"], \"doc\": \"DK1-Germany exchange in MW.\"}, {\"name\": \"exchange_dk1_nl\", \"type\": [\"double\", \"null\"], \"doc\": \"DK1-Netherlands exchange in MW.\"}, {\"name\": \"exchange_dk1_gb\", \"type\": [\"double\", \"null\"], \"doc\": \"DK1-Great Britain exchange in MW.\"}, {\"name\": \"exchange_dk1_no\", \"type\": [\"double\", \"null\"], \"doc\": \"DK1-Norway exchange in MW.\"}, {\"name\": \"exchange_dk1_se\", \"type\": [\"double\", \"null\"], \"doc\": \"DK1-Sweden exchange in MW.\"}, {\"name\": \"exchange_dk1_dk2\", \"type\": [\"double\", \"null\"], \"doc\": \"DK1-DK2 (Great Belt) exchange in MW.\"}, {\"name\": \"exchange_dk2_de\", \"type\": [\"double\", \"null\"], \"doc\": \"DK2-Germany exchange in MW.\"}, {\"name\": \"exchange_dk2_se\", \"type\": [\"double\", \"null\"], \"doc\": \"DK2-Sweden exchange in MW.\"}, {\"name\": \"exchange_bornholm_se\", \"type\": [\"double\", \"null\"], \"doc\": \"Bornholm-Sweden exchange in MW.\"}, {\"name\": \"afrr_activated_dk1\", \"type\": [\"double\", \"null\"], \"doc\": \"aFRR activated in DK1 in MW.\"}, {\"name\": \"afrr_activated_dk2\", \"type\": [\"double\", \"null\"], \"doc\": \"aFRR activated in DK2 in MW.\"}, {\"name\": \"mfrr_activated_dk1\", \"type\": [\"double\", \"null\"], \"doc\": \"mFRR activated in DK1 in MW.\"}, {\"name\": \"mfrr_activated_dk2\", \"type\": [\"double\", \"null\"], \"doc\": \"mFRR activated in DK2 in MW.\"}, {\"name\": \"imbalance_dk1\", \"type\": [\"double\", \"null\"], \"doc\": \"Grid imbalance in DK1 in MW.\"}, {\"name\": \"imbalance_dk2\", \"type\": [\"double\", \"null\"], \"doc\": \"Grid imbalance in DK2 in MW.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.minutes1_utc=str(self.minutes1_utc)
        self.minutes1_dk=str(self.minutes1_dk)
        self.price_area=str(self.price_area)
        self.co2_emission=float(self.co2_emission) if self.co2_emission else None
        self.production_ge_100mw=float(self.production_ge_100mw) if self.production_ge_100mw else None
        self.production_lt_100mw=float(self.production_lt_100mw) if self.production_lt_100mw else None
        self.solar_power=float(self.solar_power) if self.solar_power else None
        self.offshore_wind_power=float(self.offshore_wind_power) if self.offshore_wind_power else None
        self.onshore_wind_power=float(self.onshore_wind_power) if self.onshore_wind_power else None
        self.exchange_sum=float(self.exchange_sum) if self.exchange_sum else None
        self.exchange_dk1_de=float(self.exchange_dk1_de) if self.exchange_dk1_de else None
        self.exchange_dk1_nl=float(self.exchange_dk1_nl) if self.exchange_dk1_nl else None
        self.exchange_dk1_gb=float(self.exchange_dk1_gb) if self.exchange_dk1_gb else None
        self.exchange_dk1_no=float(self.exchange_dk1_no) if self.exchange_dk1_no else None
        self.exchange_dk1_se=float(self.exchange_dk1_se) if self.exchange_dk1_se else None
        self.exchange_dk1_dk2=float(self.exchange_dk1_dk2) if self.exchange_dk1_dk2 else None
        self.exchange_dk2_de=float(self.exchange_dk2_de) if self.exchange_dk2_de else None
        self.exchange_dk2_se=float(self.exchange_dk2_se) if self.exchange_dk2_se else None
        self.exchange_bornholm_se=float(self.exchange_bornholm_se) if self.exchange_bornholm_se else None
        self.afrr_activated_dk1=float(self.afrr_activated_dk1) if self.afrr_activated_dk1 else None
        self.afrr_activated_dk2=float(self.afrr_activated_dk2) if self.afrr_activated_dk2 else None
        self.mfrr_activated_dk1=float(self.mfrr_activated_dk1) if self.mfrr_activated_dk1 else None
        self.mfrr_activated_dk2=float(self.mfrr_activated_dk2) if self.mfrr_activated_dk2 else None
        self.imbalance_dk1=float(self.imbalance_dk1) if self.imbalance_dk1 else None
        self.imbalance_dk2=float(self.imbalance_dk2) if self.imbalance_dk2 else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PowerSystemSnapshot':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PowerSystemSnapshot']:
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
            return PowerSystemSnapshot.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return PowerSystemSnapshot.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')