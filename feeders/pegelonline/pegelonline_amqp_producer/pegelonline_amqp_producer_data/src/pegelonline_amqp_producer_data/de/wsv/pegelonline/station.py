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
from pegelonline_amqp_producer_data.de.wsv.pegelonline.water import Water




@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Station:
    """
    WSV PegelOnline gauge installation. Each instance represents one physical Pegelmessstelle on a federally administered German inland or coastal waterway. Sourced from `GET /stations.json` on the PegelOnline REST API v2 (https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Emitted as reference data at bridge startup and re-emitted periodically.
    Attributes:
        station_id (typing.Optional[str]): Stable UUID assigned by WSV to identify the gauge installation; persists across station renaming, relocation within the same Pegelmessstelle, and timeseries reconfiguration. Sourced from the upstream `uuid` field. Used as the CloudEvents `subject`, the Kafka partition key, the MQTT topic `{station_id}` segment, and the AMQP message subject for every event emitted by this source.
        number (typing.Optional[str]): Official PegelOnline station number. Carries multiple agency-scoped numbering schemes within the same field: WSV Pegelmessstellennummer (6–8 digits) for German federal gauges; partner-agency identifiers such as Austrian via-donau station numbers (4–5 digits), small Regierungspräsidium-IDs for Bodensee gauges (3-digit numbers e.g. '906' KONSTANZ), and German state-agency IDs (e.g. Ruhrverband 13-digit Messstellennummer). Numeric-only across all observed providers; length is provider-specific. National / agency-scoped identifier — not globally unique across data providers; prefer `station_id` (UUID) for cross-system joins. [pattern: ^[0-9]+$]
        shortname (typing.Optional[str]): Operator-assigned display label for the gauge (≤40 characters). May differ from the town name when multiple gauges share a town. Mutable — do not use as a routing key or stable identifier.
        longname (typing.Optional[str]): Canonical gauge name as used in WSV publications (≤255 characters). Mutable — do not use as a routing key.
        km (typing.Optional[float]): Position along the federal waterway expressed as river-kilometre downstream from the waterway's official origin (e.g. Rhine-km 0 at the Old Rhine Bridge in Konstanz). The decimal fraction is the hectometre offset within the kilometre. Negative values occur on tributaries where the kilometre count is measured upstream from a confluence (e.g. Ohře gauge LOUNY at km -61.4 of the Elbe/Ohře system). **Optional**: absent or null for tidal / coastal gauges (Küstenpegel on the North Sea and Baltic) and for waterways without a kilometre reference. Sourced from the upstream `km` field. Unit: km.
        agency (typing.Optional[str]): Free-form name of the Wasserstraßen- und Schifffahrtsamt (WSA) operating the gauge — e.g. 'WSA RHEIN', 'WSA ELBE'. Sourced from the upstream `agency` field. Provided so downstream consumers can attribute observations to the operating authority; not a stable identifier and not suitable as a routing key.
        longitude (float): WGS84 decimal-degree longitude of the gauge installation; positive east of the prime meridian. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `longitude` field. [minimum: -180, maximum: 180]
        latitude (float): WGS84 decimal-degree latitude of the gauge installation; positive north of the equator. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `latitude` field. [minimum: -90, maximum: 90]
        water (Water): Federal waterway the gauge measures. See the nested Water schema for routing semantics."""


    station_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    number: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="number"))
    shortname: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="shortname"))
    longname: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longname"))
    km: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="km"))
    agency: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agency"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    water: Water=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water"))

    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Station\", \"namespace\": \"de.wsv.pegelonline\", \"doc\": \"WSV PegelOnline gauge installation. Each instance represents one physical Pegelmessstelle on a federally administered German inland or coastal waterway. Sourced from `GET /stations.json` on the PegelOnline REST API v2 (https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Emitted as reference data at bridge startup and re-emitted periodically.\", \"fields\": [{\"name\": \"station_id\", \"type\": [\"string\", \"null\"], \"doc\": \"Stable UUID assigned by WSV to identify the gauge installation; persists across station renaming, relocation within the same Pegelmessstelle, and timeseries reconfiguration. Sourced from the upstream `uuid` field. Used as the CloudEvents `subject`, the Kafka partition key, the MQTT topic `{station_id}` segment, and the AMQP message subject for every event emitted by this source.\"}, {\"name\": \"number\", \"type\": [\"string\", \"null\"], \"doc\": \"Official PegelOnline station number. Carries multiple agency-scoped numbering schemes within the same field: WSV Pegelmessstellennummer (6\u20138 digits) for German federal gauges; partner-agency identifiers such as Austrian via-donau station numbers (4\u20135 digits), small Regierungspr\u00e4sidium-IDs for Bodensee gauges (3-digit numbers e.g. '906' KONSTANZ), and German state-agency IDs (e.g. Ruhrverband 13-digit Messstellennummer). Numeric-only across all observed providers; length is provider-specific. National / agency-scoped identifier \u2014 not globally unique across data providers; prefer `station_id` (UUID) for cross-system joins. [pattern: ^[0-9]+$]\"}, {\"name\": \"shortname\", \"type\": [\"string\", \"null\"], \"doc\": \"Operator-assigned display label for the gauge (\u226440 characters). May differ from the town name when multiple gauges share a town. Mutable \u2014 do not use as a routing key or stable identifier.\"}, {\"name\": \"longname\", \"type\": [\"string\", \"null\"], \"doc\": \"Canonical gauge name as used in WSV publications (\u2264255 characters). Mutable \u2014 do not use as a routing key.\"}, {\"name\": \"km\", \"type\": [\"double\", \"null\"], \"doc\": \"Position along the federal waterway expressed as river-kilometre downstream from the waterway's official origin (e.g. Rhine-km 0 at the Old Rhine Bridge in Konstanz). The decimal fraction is the hectometre offset within the kilometre. Negative values occur on tributaries where the kilometre count is measured upstream from a confluence (e.g. Oh\u0159e gauge LOUNY at km -61.4 of the Elbe/Oh\u0159e system). **Optional**: absent or null for tidal / coastal gauges (K\u00fcstenpegel on the North Sea and Baltic) and for waterways without a kilometre reference. Sourced from the upstream `km` field. Unit: km.\", \"default\": null}, {\"name\": \"agency\", \"type\": [\"string\", \"null\"], \"doc\": \"Free-form name of the Wasserstra\u00dfen- und Schifffahrtsamt (WSA) operating the gauge \u2014 e.g. 'WSA RHEIN', 'WSA ELBE'. Sourced from the upstream `agency` field. Provided so downstream consumers can attribute observations to the operating authority; not a stable identifier and not suitable as a routing key.\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"WGS84 decimal-degree longitude of the gauge installation; positive east of the prime meridian. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `longitude` field. [minimum: -180, maximum: 180]\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"WGS84 decimal-degree latitude of the gauge installation; positive north of the equator. Surveyed to the gauge structure, not to the river centreline. Sourced from the upstream `latitude` field. [minimum: -90, maximum: 90]\"}, {\"name\": \"water\", \"type\": {\"type\": \"record\", \"name\": \"Water\", \"namespace\": \"de.wsv.pegelonline\", \"doc\": \"Federal waterway / water body the gauge measures, as returned in the nested `water` object of `GET /stations.json` on the PegelOnline REST API v2. Acts as the routing hierarchy for the MQTT Unified Namespace topology.\", \"fields\": [{\"name\": \"shortname\", \"type\": [\"string\", \"null\"], \"doc\": \"Lowercase routing token for the waterway as published by WSV \u2014 e.g. 'rhein', 'elbe', 'donau', 'mosel'. Used (after ASCII-normalization for non-ASCII characters such as '\u00df' \u2192 'ss' or umlauts) as the `{water_shortname}` template variable on the MQTT topic and the AMQP application property. Sourced from the upstream `water.shortname` key. Maximum 40 characters.\"}, {\"name\": \"longname\", \"type\": [\"string\", \"null\"], \"doc\": \"Canonical uppercase WSV name of the waterway (e.g. 'RHEIN', 'ELBE') as published in official German hydrology bulletins. Sourced from the upstream `water.longname` key. Maximum 255 characters.\"}]}, \"doc\": \"Federal waterway the gauge measures. See the nested Water schema for routing semantics.\"}]}"), avro.name.Names()
    )


    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=(str(self.station_id)) if self.station_id is not None else None
        self.number=(str(self.number)) if self.number is not None else None
        self.shortname=(str(self.shortname)) if self.shortname is not None else None
        self.longname=(str(self.longname)) if self.longname is not None else None
        self.km=(float(self.km)) if self.km is not None else None
        self.agency=(str(self.agency)) if self.agency is not None else None
        self.longitude=float(self.longitude)
        self.latitude=float(self.latitude)
        value_water = self.water
        self.water = value_water if isinstance(value_water, Water) else Water.from_serializer_dict(value_water) if value_water else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
        """
        data = dict(data)
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
            if isinstance(result, str):
                result = result.encode('utf-8')

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