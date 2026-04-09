""" RiverStation dataclass. """

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
class RiverStation:
    """
    Reference data for a BIPAD river monitoring station in Nepal, including location, river basin, administrative boundaries, and configured danger/warning thresholds.
    Attributes:
        station_id (str): Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility.
        title (str): Human-readable name of the river station, typically in the format 'River at Location'.
        basin (str): Name of the river basin the station belongs to.
        latitude (float): Latitude coordinate of the station in WGS84 decimal degrees.
        longitude (float): Longitude coordinate of the station in WGS84 decimal degrees.
        elevation (typing.Optional[int]): Elevation of the station in meters above sea level. Null when not available.
        danger_level (typing.Optional[float]): Configured danger water level threshold in meters. Null when not configured.
        warning_level (typing.Optional[float]): Configured warning water level threshold in meters. Null when not configured.
        description (typing.Optional[str]): Free-text description of the station. Null when not provided.
        data_source (str): Origin system providing the station data, typically 'hydrology.gov.np'.
        province (typing.Optional[int]): Nepal province administrative code. Null when not assigned.
        district (typing.Optional[int]): Nepal district administrative code. Null when not assigned.
        municipality (typing.Optional[int]): Nepal municipality administrative code. Null when not assigned.
        ward (typing.Optional[int]): Nepal ward-level administrative code. Null when not assigned."""
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    title: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    basin: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    elevation: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="elevation"))
    danger_level: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="danger_level"))
    warning_level: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="warning_level"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    data_source: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_source"))
    province: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="province"))
    district: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="district"))
    municipality: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="municipality"))
    ward: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ward"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"RiverStation\", \"namespace\": \"np.gov.bipad.hydrology\", \"doc\": \"Reference data for a BIPAD river monitoring station in Nepal, including location, river basin, administrative boundaries, and configured danger/warning thresholds.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility.\"}, {\"name\": \"title\", \"type\": \"string\", \"doc\": \"Human-readable name of the river station, typically in the format 'River at Location'.\"}, {\"name\": \"basin\", \"type\": \"string\", \"doc\": \"Name of the river basin the station belongs to.\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"Latitude coordinate of the station in WGS84 decimal degrees.\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"Longitude coordinate of the station in WGS84 decimal degrees.\"}, {\"name\": \"elevation\", \"type\": [\"null\", \"int\"], \"doc\": \"Elevation of the station in meters above sea level. Null when not available.\", \"default\": null}, {\"name\": \"danger_level\", \"type\": [\"null\", \"double\"], \"doc\": \"Configured danger water level threshold in meters. Null when not configured.\", \"default\": null}, {\"name\": \"warning_level\", \"type\": [\"null\", \"double\"], \"doc\": \"Configured warning water level threshold in meters. Null when not configured.\", \"default\": null}, {\"name\": \"description\", \"type\": [\"null\", \"string\"], \"doc\": \"Free-text description of the station. Null when not provided.\", \"default\": null}, {\"name\": \"data_source\", \"type\": \"string\", \"doc\": \"Origin system providing the station data, typically 'hydrology.gov.np'.\"}, {\"name\": \"province\", \"type\": [\"null\", \"int\"], \"doc\": \"Nepal province administrative code. Null when not assigned.\", \"default\": null}, {\"name\": \"district\", \"type\": [\"null\", \"int\"], \"doc\": \"Nepal district administrative code. Null when not assigned.\", \"default\": null}, {\"name\": \"municipality\", \"type\": [\"null\", \"int\"], \"doc\": \"Nepal municipality administrative code. Null when not assigned.\", \"default\": null}, {\"name\": \"ward\", \"type\": [\"null\", \"int\"], \"doc\": \"Nepal ward-level administrative code. Null when not assigned.\", \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.title=str(self.title)
        self.basin=str(self.basin)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.elevation=int(self.elevation) if self.elevation else None
        self.danger_level=float(self.danger_level) if self.danger_level else None
        self.warning_level=float(self.warning_level) if self.warning_level else None
        self.description=str(self.description) if self.description else None
        self.data_source=str(self.data_source)
        self.province=int(self.province) if self.province else None
        self.district=int(self.district) if self.district else None
        self.municipality=int(self.municipality) if self.municipality else None
        self.ward=int(self.ward) if self.ward else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'RiverStation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['RiverStation']:
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
            return RiverStation.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return RiverStation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')