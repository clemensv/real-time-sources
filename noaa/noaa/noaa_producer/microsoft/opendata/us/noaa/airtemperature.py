""" AirTemperature """

# pylint: disable=invalid-name,line-too-long,too-many-instance-attributes

from typing import Optional,Any

from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json
import json
import io
import gzip


@dataclass_json
@dataclass
class AirTemperature:
    """
    A AirTemperature record.

    Attributes:
        station_id (str): {"description": "7 character station ID, or a currents station ID."}
        timestamp (str): {"description": "Timestamp of the air temperature measurement"}
        value (float): {"description": "Value of the air temperature"}
        max_temp_exceeded (bool): Flag indicating if the maximum expected air temperature was exceeded
        min_temp_exceeded (bool): Flag indicating if the minimum expected air temperature was exceeded
        rate_of_change_exceeded (bool): Flag indicating if the rate of change tolerance limit was exceeded
    """
    station_id: str
    timestamp: str
    value: float
    max_temp_exceeded: bool
    min_temp_exceeded: bool
    rate_of_change_exceeded: bool

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
    def from_data(cls, data: Any, content_type_string: Optional[str] = None) -> Optional['AirTemperature']:
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
