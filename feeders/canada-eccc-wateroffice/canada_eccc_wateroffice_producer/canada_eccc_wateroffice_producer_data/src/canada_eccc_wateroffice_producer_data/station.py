""" Station dataclass. """

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
class Station:
    """
    Reference data for a Water Survey of Canada hydrometric monitoring station from the ECCC OGC API hydrometric-stations collection.
    
    Attributes:
        station_number (str)
        station_name (str)
        prov_terr_state_loc (str)
        status_en (typing.Optional[str])
        contributor_en (typing.Optional[str])
        drainage_area_gross (typing.Optional[float])
        drainage_area_effect (typing.Optional[float])
        rhbn (typing.Optional[bool])
        real_time (typing.Optional[bool])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        basin (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Station\", \"doc\": \"Reference data for a Water Survey of Canada hydrometric monitoring station from the ECCC OGC API hydrometric-stations collection.\", \"fields\": [{\"name\": \"station_number\", \"type\": \"string\", \"doc\": \"Unique WSC station identifier following the scheme 2-digit major drainage area + letter + station digits, e.g. '05BJ004'. Upstream field: STATION_NUMBER.\"}, {\"name\": \"station_name\", \"type\": \"string\", \"doc\": \"Official name of the hydrometric station, e.g. 'ELBOW RIVER AT BRAGG CREEK'. Upstream field: STATION_NAME.\"}, {\"name\": \"prov_terr_state_loc\", \"type\": \"string\", \"doc\": \"Two-letter province, territory or state location code where the station is situated, e.g. 'AB' for Alberta. Upstream field: PROV_TERR_STATE_LOC.\"}, {\"name\": \"status_en\", \"type\": [\"string\", \"null\"], \"doc\": \"Operational status of the station in English, e.g. 'Active', 'Discontinued'. Upstream field: STATUS_EN.\", \"default\": null}, {\"name\": \"contributor_en\", \"type\": [\"string\", \"null\"], \"doc\": \"Name of the contributing agency responsible for operating this station in English, e.g. 'Water Survey of Canada'. Upstream field: CONTRIBUTOR_EN.\", \"default\": null}, {\"name\": \"drainage_area_gross\", \"type\": [\"double\", \"null\"], \"doc\": \"Gross drainage area of the watershed upstream of this station in square kilometres. Upstream field: DRAINAGE_AREA_GROSS.\", \"default\": null}, {\"name\": \"drainage_area_effect\", \"type\": [\"double\", \"null\"], \"doc\": \"Effective (contributing) drainage area of the watershed upstream of this station in square kilometres, excluding non-contributing areas. Upstream field: DRAINAGE_AREA_EFFECT.\", \"default\": null}, {\"name\": \"rhbn\", \"type\": [\"boolean\", \"null\"], \"doc\": \"Indicates whether the station is part of the Reference Hydrometric Basin Network (RHBN), a subset of hydrologically stable, minimally disturbed basins used for climate change studies. Upstream field: RHBN.\", \"default\": null}, {\"name\": \"real_time\", \"type\": [\"boolean\", \"null\"], \"doc\": \"Indicates whether real-time data are available for this station via the WSC real-time data service. Upstream field: REAL_TIME.\", \"default\": null}, {\"name\": \"latitude\", \"type\": [\"double\", \"null\"], \"doc\": \"Geographic latitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.\", \"default\": null}, {\"name\": \"longitude\", \"type\": [\"double\", \"null\"], \"doc\": \"Geographic longitude of the station in decimal degrees (WGS84), derived from the GeoJSON geometry coordinates.\", \"default\": null}, {\"name\": \"basin\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for canada-eccc-wateroffice.\", \"default\": null}]}"
    )
    
    
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
    basin: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'Station':
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
        if 'station_number' in converted and converted['station_number'] is not None:
            value = converted['station_number']
        if 'station_name' in converted and converted['station_name'] is not None:
            value = converted['station_name']
        if 'prov_terr_state_loc' in converted and converted['prov_terr_state_loc'] is not None:
            value = converted['prov_terr_state_loc']
        if 'status_en' in converted and converted['status_en'] is not None:
            value = converted['status_en']
        if 'contributor_en' in converted and converted['contributor_en'] is not None:
            value = converted['contributor_en']
        if 'drainage_area_gross' in converted and converted['drainage_area_gross'] is not None:
            value = converted['drainage_area_gross']
        if 'drainage_area_effect' in converted and converted['drainage_area_effect'] is not None:
            value = converted['drainage_area_effect']
        if 'rhbn' in converted and converted['rhbn'] is not None:
            value = converted['rhbn']
        if 'real_time' in converted and converted['real_time'] is not None:
            value = converted['real_time']
        if 'latitude' in converted and converted['latitude'] is not None:
            value = converted['latitude']
        if 'longitude' in converted and converted['longitude'] is not None:
            value = converted['longitude']
        if 'basin' in converted and converted['basin'] is not None:
            value = converted['basin']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Station']:
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
                    return Station.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Station':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            station_number='zrezmupqrqnnowokvcan',
            station_name='mpxdubvhvxejgnrofggv',
            prov_terr_state_loc='uiafqhglxlrqgsvpaftr',
            status_en='samnbokasfixtlhulzhv',
            contributor_en='iucjnsobvlztrcudycqp',
            drainage_area_gross=float(51.65007898726148),
            drainage_area_effect=float(92.69364517124814),
            rhbn=True,
            real_time=True,
            latitude=float(62.32127529544537),
            longitude=float(48.80642695643327),
            basin='easlncwdvryfemcyuaem'
        )