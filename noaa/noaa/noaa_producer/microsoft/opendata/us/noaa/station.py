""" Station """

# pylint: disable=invalid-name,line-too-long,too-many-instance-attributes

from typing import Optional,Any

from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json
import json
import io
import gzip

from .stationtypes.sensors import sensors
from .stationtypes.floodlevels import floodlevels
from .stationtypes.benchmarks import benchmarks
from .stationtypes.products import products
from .stationtypes.notices import notices
from .stationtypes.nearby import nearby
from .stationtypes.tidepredoffsets import tidePredOffsets
from .stationtypes.disclaimers import disclaimers
from .stationtypes.harmonicconstituents import harmonicConstituents
from .stationtypes.supersededdatums import supersededdatums
from .stationtypes.details import details
from .stationtypes.ofsmapoffsets import ofsMapOffsets
from .stationtypes.datums import datums

@dataclass_json
@dataclass
class Station:
    """
    A Station record.

    Attributes:
        tidal (bool): {"description": "Indicates whether the station measures tidal data."}
        greatlakes (bool): {"description": "Indicates whether the station is located in the Great Lakes region."}
        shefcode (str): {"description": "Standard Hydrologic Exchange Format code for the station."}
        details (details): 
        sensors (sensors): 
        floodlevels (floodlevels): 
        datums (datums): 
        supersededdatums (supersededdatums): 
        harmonicConstituents (harmonicConstituents): 
        benchmarks (benchmarks): 
        tidePredOffsets (tidePredOffsets): 
        ofsMapOffsets (ofsMapOffsets): 
        state (str): {"description": "State where the station is located."}
        timezone (str): {"description": "Timezone of the station."}
        timezonecorr (int): {"description": "Timezone correction in minutes for the station."}
        observedst (bool): {"description": "Indicates whether the station observes Daylight Saving Time."}
        stormsurge (bool): {"description": "Indicates whether the station measures storm surge data."}
        nearby (nearby): 
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
        products (products): 
        disclaimers (disclaimers): 
        notices (notices): 
        self (str): {"description": "URL to the station's data."}
        expand (str): {"description": "URL to expanded information about the station."}
        tideType (str): {"description": "Type of tide measured by the station."}
    """
    tidal: bool
    greatlakes: bool
    shefcode: str
    details: details
    sensors: sensors
    floodlevels: floodlevels
    datums: datums
    supersededdatums: supersededdatums
    harmonicConstituents: harmonicConstituents
    benchmarks: benchmarks
    tidePredOffsets: tidePredOffsets
    ofsMapOffsets: ofsMapOffsets
    state: str
    timezone: str
    timezonecorr: int
    observedst: bool
    stormsurge: bool
    nearby: nearby
    forecast: bool
    outlook: bool
    HTFhistorical: bool
    nonNavigational: bool
    id: str
    name: str
    lat: float
    lng: float
    affiliations: str
    portscode: str | None
    products: products
    disclaimers: disclaimers
    notices: notices
    self: str
    expand: str
    tideType: str

    def to_byte_array(self, content_type_string: str) -> bytes:
        """Converts the dataclass to a byte array based on the content type string."""
        content_type = content_type_string.split(';')[0].strip()
        result = None

        if content_type == 'application/json':
            result = json.dumps(asdict(self)).encode('utf-8')

        if result is not None and content_type.endswith('+gzip'):
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: Any, content_type_string: Optional[str] = None) -> Optional['Station']:
        """Converts the data to a dataclass based on the content type string."""
        if data is None:
            return None
        if isinstance(data, cls):
            return data
        content_type = (content_type_string or 'application/octet-stream').split(';')[0].strip()

        if content_type.endswith('+gzip'):
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for gzip decompression')
            with gzip.GzipFile(fileobj=stream, mode='rb') as gzip_file:
                data = gzip_file.read()

        if content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                return cls(**json.loads(data_str))
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')
