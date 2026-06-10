""" DisasterAlert dataclass. """

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
from marshmallow import fields
import json
from gdacs_amqp_producer_data.alertcolorenum import AlertColorenum
from gdacs_amqp_producer_data.eventtypeenum import EventTypeenum
from gdacs_amqp_producer_data.alertlevelenum import AlertLevelenum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class DisasterAlert:
    """
    A disaster alert from the Global Disaster Alert and Coordination System (GDACS), covering earthquakes, tropical cyclones, floods, volcanoes, forest fires, and droughts worldwide.
    
    Attributes:
        event_type (EventTypeenum)
        event_id (str)
        episode_id (typing.Optional[str])
        alert_level (AlertLevelenum)
        alert_score (typing.Optional[float])
        episode_alert_level (typing.Optional[str])
        episode_alert_score (typing.Optional[float])
        event_name (typing.Optional[str])
        severity_value (float)
        severity_unit (str)
        severity_text (typing.Optional[str])
        country (str)
        iso3 (typing.Optional[str])
        latitude (float)
        longitude (float)
        from_date (datetime.datetime)
        to_date (typing.Optional[datetime.datetime])
        population_value (typing.Optional[float])
        population_unit (typing.Optional[str])
        vulnerability (typing.Optional[float])
        bbox_min_lon (typing.Optional[float])
        bbox_max_lon (typing.Optional[float])
        bbox_min_lat (typing.Optional[float])
        bbox_max_lat (typing.Optional[float])
        is_current (typing.Optional[bool])
        version (typing.Optional[int])
        description (typing.Optional[str])
        link (typing.Optional[str])
        pub_date (typing.Optional[datetime.datetime])
        alert_color (AlertColorenum)
    """
    
    
    event_type: EventTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_type"))
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    episode_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="episode_id"))
    alert_level: AlertLevelenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_level"))
    alert_score: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_score"))
    episode_alert_level: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="episode_alert_level"))
    episode_alert_score: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="episode_alert_score"))
    event_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_name"))
    severity_value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity_value"))
    severity_unit: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity_unit"))
    severity_text: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity_text"))
    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    iso3: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="iso3"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    from_date: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="from_date", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    to_date: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="to_date", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    population_value: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="population_value"))
    population_unit: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="population_unit"))
    vulnerability: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vulnerability"))
    bbox_min_lon: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_min_lon"))
    bbox_max_lon: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_max_lon"))
    bbox_min_lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_min_lat"))
    bbox_max_lat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_max_lat"))
    is_current: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_current"))
    version: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    link: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="link"))
    pub_date: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pub_date", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    alert_color: AlertColorenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alert_color"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'DisasterAlert':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
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
            if isinstance(v, enum.Enum):
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['DisasterAlert']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
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
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return DisasterAlert.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'DisasterAlert':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            event_type=EventTypeenum.EQ,
            event_id='vrhamecdmrfzjdtqfscr',
            episode_id='ycdkoksqxseklzikriyu',
            alert_level=AlertLevelenum.Green,
            alert_score=float(88.82843281586064),
            episode_alert_level='dyrsgfvimrcbwdhzxrlb',
            episode_alert_score=float(35.021092015096855),
            event_name='urfkfzuryuglzwodwjax',
            severity_value=float(16.39509696609933),
            severity_unit='qbtnkisjfzfjufrfbdlc',
            severity_text='bvqtettvpnzacwpqmtyi',
            country='jgcftplpqybhvqhhdpve',
            iso3='upweorexoivpzugnzeoa',
            latitude=float(8.138030584117583),
            longitude=float(48.23882513658292),
            from_date=datetime.datetime.now(datetime.timezone.utc),
            to_date=datetime.datetime.now(datetime.timezone.utc),
            population_value=float(96.47794081006624),
            population_unit='kjojcblhkrapoeunqayb',
            vulnerability=float(11.236174123608633),
            bbox_min_lon=float(45.730374135568),
            bbox_max_lon=float(18.074212040390925),
            bbox_min_lat=float(68.34653898126605),
            bbox_max_lat=float(69.81562658937897),
            is_current=True,
            version=int(43),
            description='pgiefgcvzfruqnrekber',
            link='zamwyqaweubqlokbhiae',
            pub_date=datetime.datetime.now(datetime.timezone.utc),
            alert_color=AlertColorenum.green
        )