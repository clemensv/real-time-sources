""" PeakDemandForecast dataclass. """

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
class PeakDemandForecast:
    """
    Daily peak demand forecast record from TEPCO Electricity Forecast.
    Attributes:
        date (str): Operating date in ISO 8601 calendar-date form.
        time (str): Stable key time component; peak demand forecast uses _peak_forecast_.
        peak_demand_forecast_mw (float): Forecast maximum demand converted from 万kW to MW.
        peak_demand_forecast_jp_unit_value (int): Original forecast maximum demand value in 万kW.
        peak_time_slot (str): Forecast maximum-demand time slot.
        update_datetime (str): Peak-demand forecast update timestamp converted to UTC RFC 3339.
        update_datetime_local (str): Peak-demand forecast update timestamp in JST RFC 3339.
        area_code (str): Constant TEPCO area code.
        area_name_jp (str): Japanese TEPCO service area name.
        area_name_en (str): English TEPCO service area name."""
    
    date: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date"))
    time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time"))
    peak_demand_forecast_mw: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="peak_demand_forecast_mw"))
    peak_demand_forecast_jp_unit_value: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="peak_demand_forecast_jp_unit_value"))
    peak_time_slot: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="peak_time_slot"))
    update_datetime: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="update_datetime"))
    update_datetime_local: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="update_datetime_local"))
    area_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_code"))
    area_name_jp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_name_jp"))
    area_name_en: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="area_name_en"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"PeakDemandForecast\", \"namespace\": \"jp.tepco.denkiyoho\", \"doc\": \"Daily peak demand forecast record from TEPCO Electricity Forecast.\", \"fields\": [{\"name\": \"date\", \"type\": \"string\", \"doc\": \"Operating date in ISO 8601 calendar-date form.\"}, {\"name\": \"time\", \"type\": \"string\", \"doc\": \"Stable key time component; peak demand forecast uses _peak_forecast_.\"}, {\"name\": \"peak_demand_forecast_mw\", \"type\": \"double\", \"doc\": \"Forecast maximum demand converted from \u4e07kW to MW.\"}, {\"name\": \"peak_demand_forecast_jp_unit_value\", \"type\": \"int\", \"doc\": \"Original forecast maximum demand value in \u4e07kW.\"}, {\"name\": \"peak_time_slot\", \"type\": \"string\", \"doc\": \"Forecast maximum-demand time slot.\"}, {\"name\": \"update_datetime\", \"type\": \"string\", \"doc\": \"Peak-demand forecast update timestamp converted to UTC RFC 3339.\"}, {\"name\": \"update_datetime_local\", \"type\": \"string\", \"doc\": \"Peak-demand forecast update timestamp in JST RFC 3339.\"}, {\"name\": \"area_code\", \"type\": \"string\", \"doc\": \"Constant TEPCO area code.\"}, {\"name\": \"area_name_jp\", \"type\": \"string\", \"doc\": \"Japanese TEPCO service area name.\"}, {\"name\": \"area_name_en\", \"type\": \"string\", \"doc\": \"English TEPCO service area name.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.date=str(self.date)
        self.time=str(self.time)
        self.peak_demand_forecast_mw=float(self.peak_demand_forecast_mw)
        self.peak_demand_forecast_jp_unit_value=int(self.peak_demand_forecast_jp_unit_value)
        self.peak_time_slot=str(self.peak_time_slot)
        self.update_datetime=str(self.update_datetime)
        self.update_datetime_local=str(self.update_datetime_local)
        self.area_code=str(self.area_code)
        self.area_name_jp=str(self.area_name_jp)
        self.area_name_en=str(self.area_name_en)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PeakDemandForecast':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PeakDemandForecast']:
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
            return PeakDemandForecast.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return PeakDemandForecast.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')