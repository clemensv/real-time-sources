""" DeforestationAlert dataclass. """

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
class DeforestationAlert:
    """
    INPE DETER deforestation alert for Amazon and Cerrado biomes.
    Attributes:
        alert_id (str): Stable reference ID from INPE (gid).
        biome (str): Biome of the alert: amazon or cerrado.
        classname (str): Deforestation class: DESMATAMENTO_CR, DEGRADACAO, MINERACAO, CS_DESORDENADO, etc.
        view_date (str): Observation date in YYYY-MM-DD format.
        satellite (str): Satellite name (CBERS-4, Amazonia-1, etc.).
        sensor (str): Sensor name (AWFI, WFI, MSI).
        area_km2 (float): Area of the deforestation polygon in square kilometers.
        municipality (typing.Optional[str]): Municipality name.
        state_code (typing.Optional[str]): Brazilian state code (UF), e.g. PA, MT.
        path_row (typing.Optional[str]): Satellite path/row identifier.
        publish_month (typing.Optional[str]): Publication month in YYYY-MM-DD format.
        centroid_latitude (float): Latitude of the polygon centroid in decimal degrees.
        centroid_longitude (float): Longitude of the polygon centroid in decimal degrees."""
    
    alert_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_id"))
    biome: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="biome"))
    classname: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="classname"))
    view_date: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="view_date"))
    satellite: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="satellite"))
    sensor: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor"))
    area_km2: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_km2"))
    municipality: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="municipality"))
    state_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_code"))
    path_row: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="path_row"))
    publish_month: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="publish_month"))
    centroid_latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="centroid_latitude"))
    centroid_longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="centroid_longitude"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"DeforestationAlert\", \"namespace\": \"BR.INPE.DETER\", \"doc\": \"INPE DETER deforestation alert for Amazon and Cerrado biomes.\", \"fields\": [{\"name\": \"alert_id\", \"type\": \"string\", \"doc\": \"Stable reference ID from INPE (gid).\"}, {\"name\": \"biome\", \"type\": \"string\", \"doc\": \"Biome of the alert: amazon or cerrado.\"}, {\"name\": \"classname\", \"type\": \"string\", \"doc\": \"Deforestation class: DESMATAMENTO_CR, DEGRADACAO, MINERACAO, CS_DESORDENADO, etc.\"}, {\"name\": \"view_date\", \"type\": \"string\", \"doc\": \"Observation date in YYYY-MM-DD format.\"}, {\"name\": \"satellite\", \"type\": \"string\", \"doc\": \"Satellite name (CBERS-4, Amazonia-1, etc.).\"}, {\"name\": \"sensor\", \"type\": \"string\", \"doc\": \"Sensor name (AWFI, WFI, MSI).\"}, {\"name\": \"area_km2\", \"type\": \"double\", \"doc\": \"Area of the deforestation polygon in square kilometers.\"}, {\"name\": \"municipality\", \"type\": [\"string\", \"null\"], \"doc\": \"Municipality name.\"}, {\"name\": \"state_code\", \"type\": [\"string\", \"null\"], \"doc\": \"Brazilian state code (UF), e.g. PA, MT.\"}, {\"name\": \"path_row\", \"type\": [\"string\", \"null\"], \"doc\": \"Satellite path/row identifier.\"}, {\"name\": \"publish_month\", \"type\": [\"string\", \"null\"], \"doc\": \"Publication month in YYYY-MM-DD format.\"}, {\"name\": \"centroid_latitude\", \"type\": \"double\", \"doc\": \"Latitude of the polygon centroid in decimal degrees.\"}, {\"name\": \"centroid_longitude\", \"type\": \"double\", \"doc\": \"Longitude of the polygon centroid in decimal degrees.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.alert_id=str(self.alert_id)
        self.biome=str(self.biome)
        self.classname=str(self.classname)
        self.view_date=str(self.view_date)
        self.satellite=str(self.satellite)
        self.sensor=str(self.sensor)
        self.area_km2=float(self.area_km2)
        self.municipality=str(self.municipality) if self.municipality else None
        self.state_code=str(self.state_code) if self.state_code else None
        self.path_row=str(self.path_row) if self.path_row else None
        self.publish_month=str(self.publish_month) if self.publish_month else None
        self.centroid_latitude=float(self.centroid_latitude)
        self.centroid_longitude=float(self.centroid_longitude)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'DeforestationAlert':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['DeforestationAlert']:
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
            return DeforestationAlert.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return DeforestationAlert.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')