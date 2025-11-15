""" Station dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
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
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.disclaimers import Disclaimers
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.ofsmapoffsets import OfsMapOffsets
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.sensors import Sensors
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.benchmarks import Benchmarks
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.supersededdatums import Supersededdatums
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.floodlevels import Floodlevels
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.tidepredoffsets import TidePredOffsets
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.nearby import Nearby
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.harmonicconstituents import HarmonicConstituents
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.notices import Notices
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.details import Details
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.datums import Datums
from noaa.noaa_producer.microsoft.opendata.us.noaa.stationtypes.products import Products


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Station:
    """
    A Station record.
    Attributes:
        tidal (bool): {"description": "Indicates whether the station measures tidal data."}
        greatlakes (bool): {"description": "Indicates whether the station is located in the Great Lakes region."}
        shefcode (str): {"description": "Standard Hydrologic Exchange Format code for the station."}
        details (Details): 
        sensors (Sensors): 
        floodlevels (Floodlevels): 
        datums (Datums): 
        supersededdatums (Supersededdatums): 
        harmonicConstituents (HarmonicConstituents): 
        benchmarks (Benchmarks): 
        tidePredOffsets (TidePredOffsets): 
        ofsMapOffsets (OfsMapOffsets): 
        state (str): {"description": "State where the station is located."}
        timezone (str): {"description": "Timezone of the station."}
        timezonecorr (int): {"description": "Timezone correction in minutes for the station."}
        observedst (bool): {"description": "Indicates whether the station observes Daylight Saving Time."}
        stormsurge (bool): {"description": "Indicates whether the station measures storm surge data."}
        nearby (Nearby): 
        forecast (bool): {"description": "Indicates whether the station provides forecast data."}
        outlook (bool): {"description": "Indicates whether the station provides outlook data."}
        HTFhistorical (bool): {"description": "Indicates whether the station has historical High Tide Flooding data."}
        nonNavigational (bool): {"description": "Indicates whether the station is non-navigational."}
        id (str): {"description": "Unique identifier for the station."}
        name (str): {"description": "Name of the station."}
        lat (float): {"description": "Latitude of the station."}
        lng (float): {"description": "Longitude of the station."}
        affiliations (str): {"description": "Affiliations of the station."}
        portscode (str): {"description": "PORTS code for the station."}
        products (Products): 
        disclaimers (Disclaimers): 
        notices (Notices): 
        self_ (str): {"description": "URL to the station's data."}
        expand (str): {"description": "URL to expanded information about the station."}
        tideType (str): {"description": "Type of tide measured by the station."}"""
    
    tidal: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tidal"))
    greatlakes: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="greatlakes"))
    shefcode: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="shefcode"))
    details: Details=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="details"))
    sensors: Sensors=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensors"))
    floodlevels: Floodlevels=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="floodlevels"))
    datums: Datums=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="datums"))
    supersededdatums: Supersededdatums=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="supersededdatums"))
    harmonicConstituents: HarmonicConstituents=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="harmonicConstituents"))
    benchmarks: Benchmarks=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="benchmarks"))
    tidePredOffsets: TidePredOffsets=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tidePredOffsets"))
    ofsMapOffsets: OfsMapOffsets=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ofsMapOffsets"))
    state: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    timezone: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timezone"))
    timezonecorr: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timezonecorr"))
    observedst: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observedst"))
    stormsurge: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stormsurge"))
    nearby: Nearby=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nearby"))
    forecast: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="forecast"))
    outlook: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="outlook"))
    HTFhistorical: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="HTFhistorical"))
    nonNavigational: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nonNavigational"))
    id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    lat: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat"))
    lng: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lng"))
    affiliations: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="affiliations"))
    portscode: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="portscode"))
    products: Products=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="products"))
    disclaimers: Disclaimers=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="disclaimers"))
    notices: Notices=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="notices"))
    self_: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="self"))
    expand: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="expand"))
    tideType: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tideType"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Station\", \"fields\": [{\"name\": \"tidal\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station measures tidal data.'}\"}, {\"name\": \"greatlakes\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station is located in the Great Lakes region.'}\"}, {\"name\": \"shefcode\", \"type\": \"string\", \"doc\": \"{'description': 'Standard Hydrologic Exchange Format code for the station.'}\"}, {\"name\": \"details\", \"type\": {\"type\": \"record\", \"name\": \"details\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"sensors\", \"type\": {\"type\": \"record\", \"name\": \"sensors\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"floodlevels\", \"type\": {\"type\": \"record\", \"name\": \"floodlevels\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"datums\", \"type\": {\"type\": \"record\", \"name\": \"datums\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"supersededdatums\", \"type\": {\"type\": \"record\", \"name\": \"supersededdatums\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"harmonicConstituents\", \"type\": {\"type\": \"record\", \"name\": \"harmonicConstituents\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"benchmarks\", \"type\": {\"type\": \"record\", \"name\": \"benchmarks\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"tidePredOffsets\", \"type\": {\"type\": \"record\", \"name\": \"tidePredOffsets\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"ofsMapOffsets\", \"type\": {\"type\": \"record\", \"name\": \"ofsMapOffsets\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"state\", \"type\": \"string\", \"doc\": \"{'description': 'State where the station is located.'}\"}, {\"name\": \"timezone\", \"type\": \"string\", \"doc\": \"{'description': 'Timezone of the station.'}\"}, {\"name\": \"timezonecorr\", \"type\": \"int\", \"doc\": \"{'description': 'Timezone correction in minutes for the station.'}\"}, {\"name\": \"observedst\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station observes Daylight Saving Time.'}\"}, {\"name\": \"stormsurge\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station measures storm surge data.'}\"}, {\"name\": \"nearby\", \"type\": {\"type\": \"record\", \"name\": \"nearby\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"forecast\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station provides forecast data.'}\"}, {\"name\": \"outlook\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station provides outlook data.'}\"}, {\"name\": \"HTFhistorical\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station has historical High Tide Flooding data.'}\"}, {\"name\": \"nonNavigational\", \"type\": \"boolean\", \"doc\": \"{'description': 'Indicates whether the station is non-navigational.'}\"}, {\"name\": \"id\", \"type\": \"string\", \"doc\": \"{'description': 'Unique identifier for the station.'}\"}, {\"name\": \"name\", \"type\": \"string\", \"doc\": \"{'description': 'Name of the station.'}\"}, {\"name\": \"lat\", \"type\": \"double\", \"doc\": \"{'description': 'Latitude of the station.'}\"}, {\"name\": \"lng\", \"type\": \"double\", \"doc\": \"{'description': 'Longitude of the station.'}\"}, {\"name\": \"affiliations\", \"type\": \"string\", \"doc\": \"{'description': 'Affiliations of the station.'}\"}, {\"name\": \"portscode\", \"type\": \"string\", \"doc\": \"{'description': 'PORTS code for the station.'}\"}, {\"name\": \"products\", \"type\": {\"type\": \"record\", \"name\": \"products\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"disclaimers\", \"type\": {\"type\": \"record\", \"name\": \"disclaimers\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"notices\", \"type\": {\"type\": \"record\", \"name\": \"notices\", \"namespace\": \"Microsoft.OpenData.US.NOAA.StationTypes\", \"fields\": [{\"name\": \"self\", \"type\": \"string\"}]}}, {\"name\": \"self\", \"type\": \"string\", \"doc\": \"{'description': 'URL to the station's data.'}\"}, {\"name\": \"expand\", \"type\": \"string\", \"doc\": \"{'description': 'URL to expanded information about the station.'}\"}, {\"name\": \"tideType\", \"type\": \"string\", \"doc\": \"{'description': 'Type of tide measured by the station.'}\"}], \"altnames\": {\"kql\": \"Station\"}, \"namespace\": \"Microsoft.OpenData.US.NOAA\"}"
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.tidal=bool(self.tidal)
        self.greatlakes=bool(self.greatlakes)
        self.shefcode=str(self.shefcode)
        value_details = self.details
        self.details = value_details if isinstance(value_details, Details) else Details.from_serializer_dict(value_details) if value_details else None
        value_sensors = self.sensors
        self.sensors = value_sensors if isinstance(value_sensors, Sensors) else Sensors.from_serializer_dict(value_sensors) if value_sensors else None
        value_floodlevels = self.floodlevels
        self.floodlevels = value_floodlevels if isinstance(value_floodlevels, Floodlevels) else Floodlevels.from_serializer_dict(value_floodlevels) if value_floodlevels else None
        value_datums = self.datums
        self.datums = value_datums if isinstance(value_datums, Datums) else Datums.from_serializer_dict(value_datums) if value_datums else None
        value_supersededdatums = self.supersededdatums
        self.supersededdatums = value_supersededdatums if isinstance(value_supersededdatums, Supersededdatums) else Supersededdatums.from_serializer_dict(value_supersededdatums) if value_supersededdatums else None
        value_harmonicConstituents = self.harmonicConstituents
        self.harmonicConstituents = value_harmonicConstituents if isinstance(value_harmonicConstituents, HarmonicConstituents) else HarmonicConstituents.from_serializer_dict(value_harmonicConstituents) if value_harmonicConstituents else None
        value_benchmarks = self.benchmarks
        self.benchmarks = value_benchmarks if isinstance(value_benchmarks, Benchmarks) else Benchmarks.from_serializer_dict(value_benchmarks) if value_benchmarks else None
        value_tidePredOffsets = self.tidePredOffsets
        self.tidePredOffsets = value_tidePredOffsets if isinstance(value_tidePredOffsets, TidePredOffsets) else TidePredOffsets.from_serializer_dict(value_tidePredOffsets) if value_tidePredOffsets else None
        value_ofsMapOffsets = self.ofsMapOffsets
        self.ofsMapOffsets = value_ofsMapOffsets if isinstance(value_ofsMapOffsets, OfsMapOffsets) else OfsMapOffsets.from_serializer_dict(value_ofsMapOffsets) if value_ofsMapOffsets else None
        self.state=str(self.state)
        self.timezone=str(self.timezone)
        self.timezonecorr=int(self.timezonecorr)
        self.observedst=bool(self.observedst)
        self.stormsurge=bool(self.stormsurge)
        value_nearby = self.nearby
        self.nearby = value_nearby if isinstance(value_nearby, Nearby) else Nearby.from_serializer_dict(value_nearby) if value_nearby else None
        self.forecast=bool(self.forecast)
        self.outlook=bool(self.outlook)
        self.HTFhistorical=bool(self.HTFhistorical)
        self.nonNavigational=bool(self.nonNavigational)
        self.id=str(self.id)
        self.name=str(self.name)
        self.lat=float(self.lat)
        self.lng=float(self.lng)
        self.affiliations=str(self.affiliations)
        self.portscode=str(self.portscode)
        value_products = self.products
        self.products = value_products if isinstance(value_products, Products) else Products.from_serializer_dict(value_products) if value_products else None
        value_disclaimers = self.disclaimers
        self.disclaimers = value_disclaimers if isinstance(value_disclaimers, Disclaimers) else Disclaimers.from_serializer_dict(value_disclaimers) if value_disclaimers else None
        value_notices = self.notices
        self.notices = value_notices if isinstance(value_notices, Notices) else Notices.from_serializer_dict(value_notices) if value_notices else None
        self.self_=str(self.self_)
        self.expand=str(self.expand)
        self.tideType=str(self.tideType)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
        """
        data['self_'] = data.pop('self')
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
                _record['self_'] = _record.pop('self')
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')