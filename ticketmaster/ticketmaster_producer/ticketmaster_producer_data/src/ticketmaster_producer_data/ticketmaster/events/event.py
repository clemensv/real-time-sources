""" Event dataclass. """

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
class Event:
    """
    A Ticketmaster event representing a concert, sports match, theater performance, or other live public event.
    Attributes:
        event_id (str): Stable Ticketmaster event identifier.
        name (str): Human-readable event name.
        type (typing.Optional[str]): Ticketmaster resource type discriminator.
        url (typing.Optional[str]): URL to the event page on Ticketmaster.com.
        locale (typing.Optional[str]): BCP-47 locale string for the event page.
        start_date (typing.Optional[str]): Local calendar date the event starts, YYYY-MM-DD.
        start_time (typing.Optional[str]): Local clock time the event starts, HH:MM:SS.
        start_datetime_local (typing.Optional[str]): Combined local start date and time as ISO 8601.
        start_datetime_utc (typing.Optional[str]): Start date and time in UTC as ISO 8601.
        status (typing.Optional[str]): On-sale status: onsale, offsale, cancelled, postponed, rescheduled.
        segment_id (typing.Optional[str]): Stable classification segment identifier.
        segment_name (typing.Optional[str]): Classification segment name.
        genre_id (typing.Optional[str]): Stable genre identifier within the segment.
        genre_name (typing.Optional[str]): Genre name.
        subgenre_id (typing.Optional[str]): Stable subgenre identifier.
        subgenre_name (typing.Optional[str]): Subgenre name.
        venue_id (typing.Optional[str]): Stable venue identifier.
        venue_name (typing.Optional[str]): Venue name.
        venue_city (typing.Optional[str]): City where the venue is located.
        venue_state_code (typing.Optional[str]): ISO 3166-2 state or province code.
        venue_country_code (typing.Optional[str]): ISO 3166-1 alpha-2 country code.
        venue_latitude (typing.Optional[float]): WGS-84 latitude of the venue.
        venue_longitude (typing.Optional[float]): WGS-84 longitude of the venue.
        price_min (typing.Optional[float]): Minimum face-value ticket price.
        price_max (typing.Optional[float]): Maximum face-value ticket price.
        currency (typing.Optional[str]): ISO 4217 currency code for price fields.
        attraction_ids (typing.Optional[str]): JSON-encoded array of attraction identifiers.
        attraction_names (typing.Optional[str]): JSON-encoded array of attraction names.
        onsale_start_datetime (typing.Optional[str]): UTC datetime when public ticket sales open.
        onsale_end_datetime (typing.Optional[str]): UTC datetime when public ticket sales close.
        info (typing.Optional[str]): General informational text about the event.
        please_note (typing.Optional[str]): Important notes for ticket purchasers."""
    
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="type"))
    url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    locale: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="locale"))
    start_date: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_date"))
    start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    start_datetime_local: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_datetime_local"))
    start_datetime_utc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_datetime_utc"))
    status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    segment_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segment_id"))
    segment_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segment_name"))
    genre_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="genre_id"))
    genre_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="genre_name"))
    subgenre_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subgenre_id"))
    subgenre_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subgenre_name"))
    venue_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_id"))
    venue_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_name"))
    venue_city: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_city"))
    venue_state_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_state_code"))
    venue_country_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_country_code"))
    venue_latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_latitude"))
    venue_longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_longitude"))
    price_min: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_min"))
    price_max: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_max"))
    currency: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="currency"))
    attraction_ids: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attraction_ids"))
    attraction_names: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attraction_names"))
    onsale_start_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onsale_start_datetime"))
    onsale_end_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onsale_end_datetime"))
    info: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="info"))
    please_note: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="please_note"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Event\", \"namespace\": \"Ticketmaster.Events\", \"doc\": \"A Ticketmaster event representing a concert, sports match, theater performance, or other live public event.\", \"fields\": [{\"name\": \"event_id\", \"type\": \"string\", \"doc\": \"Stable Ticketmaster event identifier.\"}, {\"name\": \"name\", \"type\": \"string\", \"doc\": \"Human-readable event name.\"}, {\"name\": \"type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Ticketmaster resource type discriminator.\"}, {\"name\": \"url\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"URL to the event page on Ticketmaster.com.\"}, {\"name\": \"locale\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"BCP-47 locale string for the event page.\"}, {\"name\": \"start_date\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Local calendar date the event starts, YYYY-MM-DD.\"}, {\"name\": \"start_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Local clock time the event starts, HH:MM:SS.\"}, {\"name\": \"start_datetime_local\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Combined local start date and time as ISO 8601.\"}, {\"name\": \"start_datetime_utc\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Start date and time in UTC as ISO 8601.\"}, {\"name\": \"status\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"On-sale status: onsale, offsale, cancelled, postponed, rescheduled.\"}, {\"name\": \"segment_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Stable classification segment identifier.\"}, {\"name\": \"segment_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Classification segment name.\"}, {\"name\": \"genre_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Stable genre identifier within the segment.\"}, {\"name\": \"genre_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Genre name.\"}, {\"name\": \"subgenre_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Stable subgenre identifier.\"}, {\"name\": \"subgenre_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Subgenre name.\"}, {\"name\": \"venue_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Stable venue identifier.\"}, {\"name\": \"venue_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Venue name.\"}, {\"name\": \"venue_city\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"City where the venue is located.\"}, {\"name\": \"venue_state_code\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 3166-2 state or province code.\"}, {\"name\": \"venue_country_code\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 3166-1 alpha-2 country code.\"}, {\"name\": \"venue_latitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS-84 latitude of the venue.\"}, {\"name\": \"venue_longitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS-84 longitude of the venue.\"}, {\"name\": \"price_min\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Minimum face-value ticket price.\"}, {\"name\": \"price_max\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Maximum face-value ticket price.\"}, {\"name\": \"currency\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 4217 currency code for price fields.\"}, {\"name\": \"attraction_ids\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"JSON-encoded array of attraction identifiers.\"}, {\"name\": \"attraction_names\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"JSON-encoded array of attraction names.\"}, {\"name\": \"onsale_start_datetime\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"UTC datetime when public ticket sales open.\"}, {\"name\": \"onsale_end_datetime\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"UTC datetime when public ticket sales close.\"}, {\"name\": \"info\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"General informational text about the event.\"}, {\"name\": \"please_note\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Important notes for ticket purchasers.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.event_id=str(self.event_id)
        self.name=str(self.name)
        self.type=str(self.type) if self.type else None
        self.url=str(self.url) if self.url else None
        self.locale=str(self.locale) if self.locale else None
        self.start_date=str(self.start_date) if self.start_date else None
        self.start_time=str(self.start_time) if self.start_time else None
        self.start_datetime_local=str(self.start_datetime_local) if self.start_datetime_local else None
        self.start_datetime_utc=str(self.start_datetime_utc) if self.start_datetime_utc else None
        self.status=str(self.status) if self.status else None
        self.segment_id=str(self.segment_id) if self.segment_id else None
        self.segment_name=str(self.segment_name) if self.segment_name else None
        self.genre_id=str(self.genre_id) if self.genre_id else None
        self.genre_name=str(self.genre_name) if self.genre_name else None
        self.subgenre_id=str(self.subgenre_id) if self.subgenre_id else None
        self.subgenre_name=str(self.subgenre_name) if self.subgenre_name else None
        self.venue_id=str(self.venue_id) if self.venue_id else None
        self.venue_name=str(self.venue_name) if self.venue_name else None
        self.venue_city=str(self.venue_city) if self.venue_city else None
        self.venue_state_code=str(self.venue_state_code) if self.venue_state_code else None
        self.venue_country_code=str(self.venue_country_code) if self.venue_country_code else None
        self.venue_latitude=float(self.venue_latitude) if self.venue_latitude else None
        self.venue_longitude=float(self.venue_longitude) if self.venue_longitude else None
        self.price_min=float(self.price_min) if self.price_min else None
        self.price_max=float(self.price_max) if self.price_max else None
        self.currency=str(self.currency) if self.currency else None
        self.attraction_ids=str(self.attraction_ids) if self.attraction_ids else None
        self.attraction_names=str(self.attraction_names) if self.attraction_names else None
        self.onsale_start_datetime=str(self.onsale_start_datetime) if self.onsale_start_datetime else None
        self.onsale_end_datetime=str(self.onsale_end_datetime) if self.onsale_end_datetime else None
        self.info=str(self.info) if self.info else None
        self.please_note=str(self.please_note) if self.please_note else None

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Event']:
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
            return Event.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Event.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')