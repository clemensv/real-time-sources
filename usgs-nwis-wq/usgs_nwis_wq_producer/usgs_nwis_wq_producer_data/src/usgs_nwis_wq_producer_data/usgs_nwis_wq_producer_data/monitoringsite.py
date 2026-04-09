""" MonitoringSite dataclass. """

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
class MonitoringSite:
    """
    A MonitoringSite record.
    Attributes:
        site_number (str): 
        site_name (str): 
        agency_code (str): 
        latitude (typing.Optional[float]): 
        longitude (typing.Optional[float]): 
        site_type (typing.Optional[str]): 
        state_code (typing.Optional[str]): 
        county_code (typing.Optional[str]): 
        huc_code (typing.Optional[str]): """
    
    site_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_number"))
    site_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_name"))
    agency_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agency_code"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    site_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_type"))
    state_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_code"))
    county_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="county_code"))
    huc_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="huc_code"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"$id\": \"gov.usgs.waterservices.wq.MonitoringSite\", \"type\": \"record\", \"name\": \"MonitoringSite\", \"description\": \"USGS water quality monitoring site. Describes a physical surface-water or groundwater monitoring location equipped with continuous water quality sensors. Site metadata is extracted from the WaterML 2.0 JSON response sourceInfo block returned by the USGS Instantaneous Values Service.\", \"fields\": [{\"name\": \"site_number\", \"type\": \"string\", \"description\": \"USGS site identification number. A unique 8-to-15-digit number assigned by the USGS to each monitoring location (e.g. '01646500').\"}, {\"name\": \"site_name\", \"type\": \"string\", \"description\": \"Official USGS station name describing the monitoring location (e.g. 'POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA').\"}, {\"name\": \"agency_code\", \"type\": \"string\", \"description\": \"Code identifying the agency responsible for the site. Typically 'USGS' for United States Geological Survey.\"}, {\"name\": \"latitude\", \"type\": [\"double\", \"null\"], \"description\": \"Decimal latitude of the monitoring site in the WGS84 (EPSG:4326) coordinate reference system.\"}, {\"name\": \"longitude\", \"type\": [\"double\", \"null\"], \"description\": \"Decimal longitude of the monitoring site in the WGS84 (EPSG:4326) coordinate reference system.\"}, {\"name\": \"site_type\", \"type\": [\"string\", \"null\"], \"description\": \"USGS site type code indicating the category of the monitoring location. Common values include 'ST' (stream), 'LK' (lake), 'GW' (groundwater), 'ES' (estuary).\"}, {\"name\": \"state_code\", \"type\": [\"string\", \"null\"], \"description\": \"Two-digit FIPS state code for the state or territory where the site is located (e.g. '24' for Maryland).\"}, {\"name\": \"county_code\", \"type\": [\"string\", \"null\"], \"description\": \"Five-digit FIPS county code for the county where the site is located (e.g. '24031' for Montgomery County, MD).\"}, {\"name\": \"huc_code\", \"type\": [\"string\", \"null\"], \"description\": \"Hydrologic Unit Code (HUC) identifying the watershed or drainage basin containing the site.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.site_number=str(self.site_number)
        self.site_name=str(self.site_name)
        self.agency_code=str(self.agency_code)
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None
        self.site_type=str(self.site_type) if self.site_type else None
        self.state_code=str(self.state_code) if self.state_code else None
        self.county_code=str(self.county_code) if self.county_code else None
        self.huc_code=str(self.huc_code) if self.huc_code else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'MonitoringSite':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['MonitoringSite']:
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
            return MonitoringSite.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return MonitoringSite.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')