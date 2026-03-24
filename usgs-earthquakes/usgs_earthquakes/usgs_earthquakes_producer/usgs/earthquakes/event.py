""" Event dataclass for USGS earthquake events. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Event:
    """
    USGS earthquake event data from the Earthquake Hazards Program.
    Attributes:
        id (str): Unique identifier for the earthquake event.
        magnitude (typing.Optional[float]): Magnitude of the earthquake.
        mag_type (typing.Optional[str]): Method or algorithm used to calculate the magnitude.
        place (typing.Optional[str]): Textual description of the named geographic region near the event.
        event_time (str): Time of the earthquake event in ISO-8601 format.
        updated (str): Time when the event was most recently updated in ISO-8601 format.
        url (typing.Optional[str]): Link to USGS Event Page for this event.
        detail_url (typing.Optional[str]): Link to GeoJSON detail feed for this event.
        felt (typing.Optional[int]): Number of felt reports submitted to the DYFI system.
        cdi (typing.Optional[float]): Maximum reported community determined intensity.
        mmi (typing.Optional[float]): Maximum estimated instrumental intensity.
        alert (typing.Optional[str]): PAGER alert level (green, yellow, orange, red).
        status (str): Review status of the event (automatic, reviewed, deleted).
        tsunami (int): Flag indicating whether the event has a tsunami advisory.
        sig (typing.Optional[int]): Significance of the event (0-1000).
        net (str): ID of the data contributor network.
        code (str): Identifying code assigned by the source for the event.
        sources (typing.Optional[str]): Comma-separated list of network contributors.
        nst (typing.Optional[int]): Number of seismic stations used.
        dmin (typing.Optional[float]): Horizontal distance to nearest station (degrees).
        rms (typing.Optional[float]): Root-mean-square travel time residual (seconds).
        gap (typing.Optional[float]): Largest azimuthal gap between stations (degrees).
        event_type (typing.Optional[str]): Type of seismic event.
        latitude (float): Latitude of the earthquake epicenter.
        longitude (float): Longitude of the earthquake epicenter.
        depth (typing.Optional[float]): Depth of the earthquake in kilometers."""

    id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    magnitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="magnitude"))
    mag_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mag_type"))
    place: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="place"))
    event_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_time"))
    updated: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated"))
    url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    detail_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="detail_url"))
    felt: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="felt"))
    cdi: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cdi"))
    mmi: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mmi"))
    alert: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert"))
    status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    tsunami: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tsunami"))
    sig: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sig"))
    net: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="net"))
    code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code"))
    sources: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sources"))
    nst: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nst"))
    dmin: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dmin"))
    rms: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rms"))
    gap: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gap"))
    event_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_type"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    depth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="depth"))

    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        json.dumps({
            "type": "record",
            "name": "Event",
            "namespace": "USGS.Earthquakes",
            "doc": "USGS earthquake event data from the Earthquake Hazards Program.",
            "fields": [
                {"name": "id", "type": "string", "doc": "Unique identifier for the earthquake event."},
                {"name": "magnitude", "type": ["double", "null"], "doc": "Magnitude of the earthquake."},
                {"name": "mag_type", "type": ["string", "null"], "doc": "Method or algorithm used to calculate the magnitude."},
                {"name": "place", "type": ["string", "null"], "doc": "Textual description of the named geographic region near the event."},
                {"name": "event_time", "type": "string", "logicalType": "timestamp-millis", "doc": "Time of the earthquake event in ISO-8601 format."},
                {"name": "updated", "type": "string", "logicalType": "timestamp-millis", "doc": "Time when the event was most recently updated in ISO-8601 format."},
                {"name": "url", "type": ["string", "null"], "doc": "Link to USGS Event Page for this event."},
                {"name": "detail_url", "type": ["string", "null"], "doc": "Link to GeoJSON detail feed for this event."},
                {"name": "felt", "type": ["int", "null"], "doc": "Number of felt reports submitted to the DYFI system."},
                {"name": "cdi", "type": ["double", "null"], "doc": "Maximum reported community determined intensity."},
                {"name": "mmi", "type": ["double", "null"], "doc": "Maximum estimated instrumental intensity."},
                {"name": "alert", "type": ["string", "null"], "doc": "PAGER alert level (green, yellow, orange, red)."},
                {"name": "status", "type": "string", "doc": "Review status of the event (automatic, reviewed, deleted)."},
                {"name": "tsunami", "type": "int", "doc": "Flag indicating whether the event has a tsunami advisory."},
                {"name": "sig", "type": ["int", "null"], "doc": "Significance of the event (0-1000)."},
                {"name": "net", "type": "string", "doc": "ID of the data contributor network."},
                {"name": "code", "type": "string", "doc": "Identifying code assigned by the source for the event."},
                {"name": "sources", "type": ["string", "null"], "doc": "Comma-separated list of network contributors."},
                {"name": "nst", "type": ["int", "null"], "doc": "Number of seismic stations used."},
                {"name": "dmin", "type": ["double", "null"], "doc": "Horizontal distance to nearest station (degrees)."},
                {"name": "rms", "type": ["double", "null"], "doc": "Root-mean-square travel time residual (seconds)."},
                {"name": "gap", "type": ["double", "null"], "doc": "Largest azimuthal gap between stations (degrees)."},
                {"name": "event_type", "type": ["string", "null"], "doc": "Type of seismic event."},
                {"name": "latitude", "type": "double", "doc": "Latitude of the earthquake epicenter."},
                {"name": "longitude", "type": "double", "doc": "Longitude of the earthquake epicenter."},
                {"name": "depth", "type": ["double", "null"], "doc": "Depth of the earthquake in kilometers."}
            ]
        })
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.id=str(self.id)
        self.magnitude=float(self.magnitude) if self.magnitude is not None else None
        self.mag_type=str(self.mag_type) if self.mag_type else None
        self.place=str(self.place) if self.place else None
        self.event_time=str(self.event_time)
        self.updated=str(self.updated)
        self.url=str(self.url) if self.url else None
        self.detail_url=str(self.detail_url) if self.detail_url else None
        self.felt=int(self.felt) if self.felt is not None else None
        self.cdi=float(self.cdi) if self.cdi is not None else None
        self.mmi=float(self.mmi) if self.mmi is not None else None
        self.alert=str(self.alert) if self.alert else None
        self.status=str(self.status)
        self.tsunami=int(self.tsunami)
        self.sig=int(self.sig) if self.sig is not None else None
        self.net=str(self.net)
        self.code=str(self.code)
        self.sources=str(self.sources) if self.sources else None
        self.nst=int(self.nst) if self.nst is not None else None
        self.dmin=float(self.dmin) if self.dmin is not None else None
        self.rms=float(self.rms) if self.rms is not None else None
        self.gap=float(self.gap) if self.gap is not None else None
        self.event_type=str(self.event_type) if self.event_type else None
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.depth=float(self.depth) if self.depth is not None else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Event':
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
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result if isinstance(result, bytes) else result.encode('utf-8'))
                result = stream.getvalue()

        if result is not None:
            return result if isinstance(result, bytes) else result.encode('utf-8')

        raise NotImplementedError(f"Unsupported content type: {content_type_string}")

    @classmethod
    def from_data(cls, data: dict) -> 'Event':
        """
        Converts a dictionary from the incoming object model to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
        """
        return cls(**data)
