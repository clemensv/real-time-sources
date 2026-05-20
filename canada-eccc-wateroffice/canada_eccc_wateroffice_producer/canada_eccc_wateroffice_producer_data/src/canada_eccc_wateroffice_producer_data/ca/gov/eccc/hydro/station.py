""" Station dataclass. """

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
class Station:
    """
    Reference data for a Water Survey of Canada hydrometric monitoring station.
    Attributes:
        station_number (str): Unique WSC station identifier, e.g. '05BJ004'. Upstream field: STATION_NUMBER.
        station_name (str): Official name of the hydrometric station. Upstream field: STATION_NAME.
        prov_terr_state_loc (str): Two-letter province, territory or state location code. Upstream field: PROV_TERR_STATE_LOC.
        status_en (typing.Optional[str]): Operational status of the station in English. Upstream field: STATUS_EN.
        contributor_en (typing.Optional[str]): Name of the contributing agency in English. Upstream field: CONTRIBUTOR_EN.
        drainage_area_gross (typing.Optional[float]): Gross drainage area in km². Upstream field: DRAINAGE_AREA_GROSS.
        drainage_area_effect (typing.Optional[float]): Effective drainage area in km². Upstream field: DRAINAGE_AREA_EFFECT.
        rhbn (typing.Optional[bool]): Part of the Reference Hydrometric Basin Network. Upstream field: RHBN.
        real_time (typing.Optional[bool]): Real-time data availability flag. Upstream field: REAL_TIME.
        latitude (typing.Optional[float]): Station latitude in decimal degrees (WGS84).
        longitude (typing.Optional[float]): Station longitude in decimal degrees (WGS84)."""
    
    station_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_number"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    prov_terr_state_loc: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="prov_terr_state_loc"))
    status_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status_en"))
    contributor_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contributor_en"))
    drainage_area_gross: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drainage_area_gross"))
    drainage_area_effect: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drainage_area_effect"))
    rhbn: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rhbn"))
    real_time: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="real_time"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Station\", \"namespace\": \"CA.Gov.ECCC.Hydro\", \"doc\": \"Reference data for a Water Survey of Canada hydrometric monitoring station.\", \"fields\": [{\"name\": \"station_number\", \"type\": \"string\", \"doc\": \"Unique WSC station identifier, e.g. '05BJ004'. Upstream field: STATION_NUMBER.\"}, {\"name\": \"station_name\", \"type\": \"string\", \"doc\": \"Official name of the hydrometric station. Upstream field: STATION_NAME.\"}, {\"name\": \"prov_terr_state_loc\", \"type\": \"string\", \"doc\": \"Two-letter province, territory or state location code. Upstream field: PROV_TERR_STATE_LOC.\"}, {\"name\": \"status_en\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Operational status of the station in English. Upstream field: STATUS_EN.\"}, {\"name\": \"contributor_en\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Name of the contributing agency in English. Upstream field: CONTRIBUTOR_EN.\"}, {\"name\": \"drainage_area_gross\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Gross drainage area in km\u00b2. Upstream field: DRAINAGE_AREA_GROSS.\"}, {\"name\": \"drainage_area_effect\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Effective drainage area in km\u00b2. Upstream field: DRAINAGE_AREA_EFFECT.\"}, {\"name\": \"rhbn\", \"type\": [\"null\", \"boolean\"], \"default\": null, \"doc\": \"Part of the Reference Hydrometric Basin Network. Upstream field: RHBN.\"}, {\"name\": \"real_time\", \"type\": [\"null\", \"boolean\"], \"default\": null, \"doc\": \"Real-time data availability flag. Upstream field: REAL_TIME.\"}, {\"name\": \"latitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Station latitude in decimal degrees (WGS84).\"}, {\"name\": \"longitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Station longitude in decimal degrees (WGS84).\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_number=str(self.station_number)
        self.station_name=str(self.station_name)
        self.prov_terr_state_loc=str(self.prov_terr_state_loc)
        self.status_en=str(self.status_en) if self.status_en else None
        self.contributor_en=str(self.contributor_en) if self.contributor_en else None
        self.drainage_area_gross=float(self.drainage_area_gross) if self.drainage_area_gross else None
        self.drainage_area_effect=float(self.drainage_area_effect) if self.drainage_area_effect else None
        self.rhbn=bool(self.rhbn) if self.rhbn else None
        self.real_time=bool(self.real_time) if self.real_time else None
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Station']:
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
            return Station.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')