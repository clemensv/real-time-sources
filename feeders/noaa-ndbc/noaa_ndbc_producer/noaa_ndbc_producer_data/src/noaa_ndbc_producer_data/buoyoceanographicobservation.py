""" BuoyOceanographicObservation dataclass. """

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
class BuoyOceanographicObservation:
    """
    Oceanographic observation from the NDBC .ocean realtime2 product. Each record reports the measurement depth together with direct ocean temperature, conductivity, salinity, dissolved oxygen, chlorophyll, turbidity, pH, and redox potential for one station and timestamp.
    
    Attributes:
        station_id (str)
        timestamp (datetime.datetime)
        depth (float)
        ocean_temperature (typing.Optional[float])
        conductivity (typing.Optional[float])
        salinity (typing.Optional[float])
        oxygen_saturation (typing.Optional[float])
        oxygen_concentration (typing.Optional[float])
        chlorophyll_concentration (typing.Optional[float])
        turbidity (typing.Optional[float])
        ph (typing.Optional[float])
        redox_potential (typing.Optional[float])
        region (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"BuoyOceanographicObservation\", \"doc\": \"Oceanographic observation from the NDBC .ocean realtime2 product. Each record reports the measurement depth together with direct ocean temperature, conductivity, salinity, dissolved oxygen, chlorophyll, turbidity, pH, and redox potential for one station and timestamp.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"NDBC station identifier. The .ocean realtime2 file is published per station and keyed by this identifier.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .ocean realtime2 file.\"}, {\"name\": \"depth\", \"type\": \"double\", \"doc\": \"Depth in meters at which the oceanographic measurements in this record were taken.\"}, {\"name\": \"ocean_temperature\", \"type\": [\"double\", \"null\"], \"doc\": \"Direct ocean temperature measurement from the OTMP column. Unit: degrees Celsius.\", \"default\": null}, {\"name\": \"conductivity\", \"type\": [\"double\", \"null\"], \"doc\": \"Electrical conductivity of seawater from the COND column. Unit: millisiemens per centimeter.\", \"default\": null}, {\"name\": \"salinity\", \"type\": [\"double\", \"null\"], \"doc\": \"Practical salinity computed from conductivity, temperature, and pressure using the Practical Salinity Scale of 1978. Unit: practical salinity units.\", \"default\": null}, {\"name\": \"oxygen_saturation\", \"type\": [\"double\", \"null\"], \"doc\": \"Dissolved oxygen saturation percentage from the O2% column.\", \"default\": null}, {\"name\": \"oxygen_concentration\", \"type\": [\"double\", \"null\"], \"doc\": \"Dissolved oxygen concentration from the O2PPM column. Unit: parts per million.\", \"default\": null}, {\"name\": \"chlorophyll_concentration\", \"type\": [\"double\", \"null\"], \"doc\": \"Chlorophyll concentration from the CLCON column. Unit: micrograms per liter.\", \"default\": null}, {\"name\": \"turbidity\", \"type\": [\"double\", \"null\"], \"doc\": \"Turbidity from the TURB column. Unit: Formazin Turbidity Units.\", \"default\": null}, {\"name\": \"ph\", \"type\": [\"double\", \"null\"], \"doc\": \"Acidity or alkalinity of the seawater sample from the PH column. This is dimensionless.\", \"default\": null}, {\"name\": \"redox_potential\", \"type\": [\"double\", \"null\"], \"doc\": \"Oxidation-reduction potential of seawater from the EH column. Unit: millivolts.\", \"default\": null}, {\"name\": \"region\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for noaa-ndbc.\", \"default\": null}]}"
    )
    
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    depth: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="depth"))
    ocean_temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ocean_temperature"))
    conductivity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="conductivity"))
    salinity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="salinity"))
    oxygen_saturation: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="oxygen_saturation"))
    oxygen_concentration: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="oxygen_concentration"))
    chlorophyll_concentration: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="chlorophyll_concentration"))
    turbidity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="turbidity"))
    ph: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ph"))
    redox_potential: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="redox_potential"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'BuoyOceanographicObservation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'BuoyOceanographicObservation':
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
        if 'station_id' in converted and converted['station_id'] is not None:
            value = converted['station_id']
        if 'timestamp' in converted and converted['timestamp'] is not None:
            value = converted['timestamp']
            if isinstance(value, str):
                converted['timestamp'] = datetime.datetime.fromisoformat(value)
        if 'depth' in converted and converted['depth'] is not None:
            value = converted['depth']
        if 'ocean_temperature' in converted and converted['ocean_temperature'] is not None:
            value = converted['ocean_temperature']
        if 'conductivity' in converted and converted['conductivity'] is not None:
            value = converted['conductivity']
        if 'salinity' in converted and converted['salinity'] is not None:
            value = converted['salinity']
        if 'oxygen_saturation' in converted and converted['oxygen_saturation'] is not None:
            value = converted['oxygen_saturation']
        if 'oxygen_concentration' in converted and converted['oxygen_concentration'] is not None:
            value = converted['oxygen_concentration']
        if 'chlorophyll_concentration' in converted and converted['chlorophyll_concentration'] is not None:
            value = converted['chlorophyll_concentration']
        if 'turbidity' in converted and converted['turbidity'] is not None:
            value = converted['turbidity']
        if 'ph' in converted and converted['ph'] is not None:
            value = converted['ph']
        if 'redox_potential' in converted and converted['redox_potential'] is not None:
            value = converted['redox_potential']
        if 'region' in converted and converted['region'] is not None:
            value = converted['region']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['BuoyOceanographicObservation']:
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
                    return BuoyOceanographicObservation.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return BuoyOceanographicObservation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'BuoyOceanographicObservation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_id='zwazzbgejxvhfzvxtfeb',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            depth=float(94.77649903305735),
            ocean_temperature=float(2.324698768189526),
            conductivity=float(30.065378639415506),
            salinity=float(56.153057480079326),
            oxygen_saturation=float(52.45421410643414),
            oxygen_concentration=float(53.87911310383936),
            chlorophyll_concentration=float(29.89429980063999),
            turbidity=float(48.644136506636926),
            ph=float(22.652782857375588),
            redox_potential=float(85.36195424038927),
            region='azkamqzbiefntiniutnm'
        )