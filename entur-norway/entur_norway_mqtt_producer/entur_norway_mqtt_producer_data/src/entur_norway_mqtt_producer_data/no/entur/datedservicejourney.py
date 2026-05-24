""" DatedServiceJourney dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class DatedServiceJourney:
    """
    Reference data for a dated service journey in the Norwegian public transport network. A DatedServiceJourney is a specific vehicle journey operating on a particular operating day, identified by its NeTEx ServiceJourney reference (DatedVehicleJourneyRef) and operating day (DataFrameRef). This reference record is extracted from the SIRI-ET feed and published at startup and refresh intervals.
    
    Attributes:
        service_journey_id (str)
        operating_day (str)
        line_ref (str)
        operator_ref (str)
        direction_ref (typing.Optional[str])
        vehicle_mode (typing.Optional[str])
        route_ref (typing.Optional[str])
        published_line_name (typing.Optional[str])
        external_line_ref (typing.Optional[str])
        origin_name (typing.Optional[str])
        destination_name (typing.Optional[str])
        data_source (typing.Optional[str])
    """
    
    
    service_journey_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="service_journey_id"))
    operating_day: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operating_day"))
    line_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="line_ref"))
    operator_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_ref"))
    direction_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction_ref"))
    vehicle_mode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_mode"))
    route_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_ref"))
    published_line_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published_line_name"))
    external_line_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="external_line_ref"))
    origin_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_name"))
    destination_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_name"))
    data_source: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_source"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'DatedServiceJourney':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['DatedServiceJourney']:
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
                return DatedServiceJourney.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'DatedServiceJourney':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            service_journey_id='wpcdkzopsonqfjifmypm',
            operating_day='elpxrmzfexqmtryaftmq',
            line_ref='nflrztopdrstiqmejbct',
            operator_ref='kefuvdddfuubbifxrcyn',
            direction_ref='bjosodtvwcujojhohhli',
            vehicle_mode='pzgmxjiyqyqpicrezcdb',
            route_ref='pirnagfydkciqmlrapix',
            published_line_name='txazpasynzplknpccbfu',
            external_line_ref='unnpekzlletsxbhddict',
            origin_name='xujzzxdnepoymnbhxihu',
            destination_name='jaajqepsvgzzopcqezsv',
            data_source='lynxqsflxzivuebvqicg'
        )