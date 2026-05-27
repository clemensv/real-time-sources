""" XrayFlare dataclass. """

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
import avro.schema
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class XrayFlare:
    """
    Individual solar X-ray flare event detected by the GOES primary satellite XRS instrument, as reported by the SWPC goes/primary/xray-flares-7-day endpoint. Each record represents a discrete flare event with onset, peak, and end times plus X-ray classifications on the standard A/B/C/M/X logarithmic scale. The flare classification is based on peak 0.1-0.8 nm X-ray flux: C-class (1e-6 W/m²), M-class (1e-5), X-class (1e-4).
    
    Attributes:
        time_tag (str)
        begin_time (str)
        begin_class (typing.Optional[str])
        max_time (typing.Optional[str])
        max_class (typing.Optional[str])
        max_xrlong (typing.Optional[float])
        max_ratio (typing.Optional[float])
        max_ratio_time (typing.Optional[str])
        current_int_xrlong (typing.Optional[float])
        end_time (typing.Optional[str])
        end_class (typing.Optional[str])
        satellite (int)
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"XrayFlare\", \"doc\": \"Individual solar X-ray flare event detected by the GOES primary satellite XRS instrument, as reported by the SWPC goes/primary/xray-flares-7-day endpoint. Each record represents a discrete flare event with onset, peak, and end times plus X-ray classifications on the standard A/B/C/M/X logarithmic scale. The flare classification is based on peak 0.1-0.8 nm X-ray flux: C-class (1e-6 W/m\u00b2), M-class (1e-5), X-class (1e-4).\", \"fields\": [{\"name\": \"time_tag\", \"type\": \"string\", \"doc\": \"UTC date-time when this flare record was reported/filed by SWPC, in ISO 8601 format.\"}, {\"name\": \"begin_time\", \"type\": \"string\", \"doc\": \"UTC date-time of the flare onset (start of the X-ray flux rise above background), in ISO 8601 format. Used as part of the Kafka key to uniquely identify each flare event.\"}, {\"name\": \"begin_class\", \"type\": [\"string\", \"null\"], \"doc\": \"X-ray classification at flare onset, e.g., 'B6.9' or 'C1.0'. Format is a letter (A/B/C/M/X) followed by a decimal multiplier within that decade of flux.\", \"default\": null}, {\"name\": \"max_time\", \"type\": [\"string\", \"null\"], \"doc\": \"UTC date-time of the peak X-ray flux during the flare, in ISO 8601 format.\", \"default\": null}, {\"name\": \"max_class\", \"type\": [\"string\", \"null\"], \"doc\": \"X-ray classification at flare peak, e.g., 'C1.2', 'M5.3', 'X1.0'. This is the official flare magnitude used in space weather bulletins.\", \"default\": null}, {\"name\": \"max_xrlong\", \"type\": [\"double\", \"null\"], \"doc\": \"Peak X-ray flux in the 0.1-0.8 nm (long wavelength) band at the time of maximum.\", \"default\": null}, {\"name\": \"max_ratio\", \"type\": [\"double\", \"null\"], \"doc\": \"Ratio of 0.05-0.4 nm (short) to 0.1-0.8 nm (long) X-ray flux at flare maximum. Higher ratios indicate a spectrally harder (more energetic) flare, which correlates with stronger ionospheric effects.\", \"default\": null}, {\"name\": \"max_ratio_time\", \"type\": [\"string\", \"null\"], \"doc\": \"UTC date-time of the maximum short/long flux ratio, in ISO 8601 format. May differ from max_time.\", \"default\": null}, {\"name\": \"current_int_xrlong\", \"type\": [\"double\", \"null\"], \"doc\": \"Current time-integrated X-ray flux in the 0.1-0.8 nm band since flare onset, representing total X-ray energy delivered.\", \"default\": null}, {\"name\": \"end_time\", \"type\": [\"string\", \"null\"], \"doc\": \"UTC date-time when the flare X-ray flux returned to half the peak value above background, in ISO 8601 format. Null if the flare is still in progress.\", \"default\": null}, {\"name\": \"end_class\", \"type\": [\"string\", \"null\"], \"doc\": \"X-ray classification at the declared end of the flare event.\", \"default\": null}, {\"name\": \"satellite\", \"type\": \"integer\", \"doc\": \"GOES satellite number that detected this flare event (e.g., 18 for GOES-18, 19 for GOES-19).\"}]}"
    )
    
    
    time_tag: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_tag"))
    begin_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="begin_time"))
    begin_class: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="begin_class"))
    max_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_time"))
    max_class: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_class"))
    max_xrlong: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_xrlong"))
    max_ratio: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_ratio"))
    max_ratio_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_ratio_time"))
    current_int_xrlong: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_int_xrlong"))
    end_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_time"))
    end_class: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_class"))
    satellite: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="satellite"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'XrayFlare':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'XrayFlare':
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
        if 'time_tag' in converted and converted['time_tag'] is not None:
            value = converted['time_tag']
        if 'begin_time' in converted and converted['begin_time'] is not None:
            value = converted['begin_time']
        if 'begin_class' in converted and converted['begin_class'] is not None:
            value = converted['begin_class']
        if 'max_time' in converted and converted['max_time'] is not None:
            value = converted['max_time']
        if 'max_class' in converted and converted['max_class'] is not None:
            value = converted['max_class']
        if 'max_xrlong' in converted and converted['max_xrlong'] is not None:
            value = converted['max_xrlong']
        if 'max_ratio' in converted and converted['max_ratio'] is not None:
            value = converted['max_ratio']
        if 'max_ratio_time' in converted and converted['max_ratio_time'] is not None:
            value = converted['max_ratio_time']
        if 'current_int_xrlong' in converted and converted['current_int_xrlong'] is not None:
            value = converted['current_int_xrlong']
        if 'end_time' in converted and converted['end_time'] is not None:
            value = converted['end_time']
        if 'end_class' in converted and converted['end_class'] is not None:
            value = converted['end_class']
        if 'satellite' in converted and converted['satellite'] is not None:
            value = converted['satellite']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['XrayFlare']:
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
                    return XrayFlare.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return XrayFlare.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'XrayFlare':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            time_tag='nizduevegkdyuxkhkneh',
            begin_time='qorfzukmpfzzrvgyncxh',
            begin_class='nqjfnuwhahurgdfkqxux',
            max_time='itnendaxnkciasrzprhn',
            max_class='dxxipxcdbzhcpmvugngr',
            max_xrlong=float(11.261005527848145),
            max_ratio=float(33.687905329914734),
            max_ratio_time='xpsddxihpliljzqhzbjz',
            current_int_xrlong=float(95.60404258842775),
            end_time='nxdlbzvpkaqqmqtrhgll',
            end_class='dsejdzxzjhwczncjpmut',
            satellite=int(16)
        )