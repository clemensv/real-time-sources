""" Messages dataclass. """

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
from mode_s_producer_data.mode_s.modes_adsb_record import ModeS_ADSB_Record


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Messages:
    """
    A container for multiple Mode-S and ADS-B decoded messages.
    Attributes:
        messages (typing.List[ModeS_ADSB_Record]): An array of Mode-S and ADS-B decoded message records."""
    
    messages: typing.List[ModeS_ADSB_Record]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="messages"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Messages\", \"namespace\": \"Mode_S\", \"doc\": \"A container for multiple Mode-S and ADS-B decoded messages.\", \"fields\": [{\"name\": \"messages\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"ModeS_ADSB_Record\", \"doc\": \"A comprehensive schema for Mode-S and ADS-B decoded messages, including fields for various BDS codes and ADS-B type codes.\", \"fields\": [{\"name\": \"ts\", \"type\": {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"The timestamp of the message reception in milliseconds since the epoch. Required.\"}, {\"name\": \"icao\", \"type\": \"string\", \"doc\": \"The ICAO 24-bit address of the aircraft. Required.\"}, {\"name\": \"df\", \"type\": \"int\", \"doc\": \"The Downlink Format (DF) of the Mode-S message, indicating the message category. Required.\"}, {\"name\": \"tc\", \"type\": [\"null\", \"int\"], \"doc\": \"The Type Code (TC) of the ADS-B message. Present for DF17 and DF18 messages; null otherwise.\"}, {\"name\": \"bcode\", \"type\": [\"null\", \"string\"], \"doc\": \"The BDS (Comm-B Data Selector) code. Present for DF20 and DF21 messages; null otherwise.\"}, {\"name\": \"alt\", \"type\": [\"null\", \"int\"], \"doc\": \"Barometric altitude in feet. Present for certain BDS and ADS-B messages; null otherwise.\"}, {\"name\": \"cs\", \"type\": [\"null\", \"string\"], \"doc\": \"Aircraft identification (call sign). Present for BDS20 and some ADS-B messages; null otherwise.\"}, {\"name\": \"sq\", \"type\": [\"null\", \"string\"], \"doc\": \"Transponder code (Squawk). Present for BDS17 messages; null otherwise.\"}, {\"name\": \"lat\", \"type\": [\"null\", \"double\"], \"doc\": \"Latitude in degrees. Present for ADS-B position messages; null otherwise.\"}, {\"name\": \"lon\", \"type\": [\"null\", \"double\"], \"doc\": \"Longitude in degrees. Present for ADS-B position messages; null otherwise.\"}, {\"name\": \"spd\", \"type\": [\"null\", \"float\"], \"doc\": \"Speed in knots. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"ang\", \"type\": [\"null\", \"float\"], \"doc\": \"Angle in degrees. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"vr\", \"type\": [\"null\", \"int\"], \"doc\": \"Vertical rate in ft/min. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"spd_type\", \"type\": [\"null\", \"string\"], \"doc\": \"Speed type. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"dir_src\", \"type\": [\"null\", \"string\"], \"doc\": \"Direction source. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"vr_src\", \"type\": [\"null\", \"string\"], \"doc\": \"Vertical rate source. Present for ADS-B TC19 messages; null otherwise.\"}, {\"name\": \"ws\", \"type\": [\"null\", \"int\"], \"doc\": \"Wind speed in knots. Present for BDS44 messages; null otherwise.\"}, {\"name\": \"wd\", \"type\": [\"null\", \"int\"], \"doc\": \"Wind direction in degrees. Present for BDS44 messages; null otherwise.\"}, {\"name\": \"at\", \"type\": [\"null\", \"float\"], \"doc\": \"Air temperature in degrees Celsius. Present for BDS44/BDS45 messages; null otherwise.\"}, {\"name\": \"ap\", \"type\": [\"null\", \"float\"], \"doc\": \"Air pressure in hPa. Present for BDS44/BDS45 messages; null otherwise.\"}, {\"name\": \"hm\", \"type\": [\"null\", \"float\"], \"doc\": \"Relative humidity in percentage. Present for BDS44 messages; null otherwise.\"}, {\"name\": \"roll\", \"type\": [\"null\", \"float\"], \"doc\": \"Aircraft roll angle in degrees. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"trak\", \"type\": [\"null\", \"float\"], \"doc\": \"True track angle in degrees. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"gs\", \"type\": [\"null\", \"float\"], \"doc\": \"Ground speed in knots. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"tas\", \"type\": [\"null\", \"float\"], \"doc\": \"True airspeed in knots. Present for BDS50 messages; null otherwise.\"}, {\"name\": \"hd\", \"type\": [\"null\", \"float\"], \"doc\": \"Aircraft heading in degrees. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"ias\", \"type\": [\"null\", \"float\"], \"doc\": \"Indicated airspeed in knots. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"m\", \"type\": [\"null\", \"float\"], \"doc\": \"Mach number. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"vrb\", \"type\": [\"null\", \"float\"], \"doc\": \"Vertical rate based on barometric altitude in ft/min. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"vri\", \"type\": [\"null\", \"float\"], \"doc\": \"Vertical rate based on inertial navigation system in ft/min. Present for BDS60 messages; null otherwise.\"}, {\"name\": \"rssi\", \"type\": [\"null\", \"float\"], \"doc\": \"Received Signal Strength Indicator in dBFS. Present for all messages if available; null otherwise.\"}, {\"name\": \"emst\", \"type\": [\"null\", \"string\"], \"doc\": \"Emergency or priority status. Present for ADS-B TC28; null otherwise.\"}, {\"name\": \"tgt\", \"type\": [\"null\", \"string\"], \"doc\": \"Target state info. Present for certain BDS6,2 or ADS-B TC29; null otherwise.\"}, {\"name\": \"opst\", \"type\": [\"null\", \"string\"], \"doc\": \"Operational status info. Present for certain BDS6,5 or ADS-B TC31; null otherwise.\"}]}}, \"doc\": \"An array of Mode-S and ADS-B decoded message records.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.messages=self.messages if isinstance(self.messages, list) else [v if isinstance(v, ModeS_ADSB_Record) else ModeS_ADSB_Record.from_serializer_dict(v) if v else None for v in self.messages] if self.messages else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Messages':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Messages']:
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
            return Messages.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Messages.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')