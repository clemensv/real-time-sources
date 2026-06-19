""" MonitoredVehicleJourney dataclass. """

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
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class MonitoredVehicleJourney:
    """
    Real-time vehicle monitoring update from the Entur SIRI-VM feed (GET /realtime/v1/rest/vm). Contains the current geographic position of a vehicle, its bearing, delay, occupancy status, and the next monitored call. Uses incremental requestorId polling for efficient change delivery.
    
    Attributes:
        service_journey_id (str)
        operating_day (str)
        recorded_at_time (datetime.datetime)
        line_ref (str)
        operator_ref (str)
        direction_ref (typing.Optional[str])
        vehicle_mode (typing.Optional[str])
        published_line_name (typing.Optional[str])
        origin_name (typing.Optional[str])
        destination_name (typing.Optional[str])
        vehicle_ref (typing.Optional[str])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        bearing (typing.Optional[float])
        delay_seconds (typing.Optional[int])
        occupancy_status (typing.Optional[str])
        progress_status (typing.Optional[str])
        monitored (bool)
    """
    
    
    service_journey_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="service_journey_id"))
    operating_day: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operating_day"))
    recorded_at_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="recorded_at_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    line_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="line_ref"))
    operator_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_ref"))
    direction_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction_ref"))
    vehicle_mode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_mode"))
    published_line_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published_line_name"))
    origin_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_name"))
    destination_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_name"))
    vehicle_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_ref"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    bearing: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bearing"))
    delay_seconds: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="delay_seconds"))
    occupancy_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="occupancy_status"))
    progress_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="progress_status"))
    monitored: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="monitored"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'MonitoredVehicleJourney':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['MonitoredVehicleJourney']:
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
                return MonitoredVehicleJourney.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'MonitoredVehicleJourney':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            service_journey_id='hssvoodqueljavbtlmza',
            operating_day='vohziuxjxuiwpzysiclh',
            recorded_at_time=datetime.datetime.now(datetime.timezone.utc),
            line_ref='ceczoldiohvndjhkueze',
            operator_ref='mwwrbwuarwexhwscwnsz',
            direction_ref='zjubxwojtouchuicaznv',
            vehicle_mode='edibqcjguxblcczlaifj',
            published_line_name='khjwtrnppofqczinbkxp',
            origin_name='byqzqhkdiipcnxrppjrl',
            destination_name='ykcnokajjspnswejbfsa',
            vehicle_ref='odhsvhrlevbwthhtmspa',
            latitude=float(34.306845897410774),
            longitude=float(43.836791521835174),
            bearing=float(54.92874462692369),
            delay_seconds=int(92),
            occupancy_status='xjjantbuxvbbrhynfxsx',
            progress_status='fzolarukqdueldnoabpj',
            monitored=False
        )