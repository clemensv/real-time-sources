"""Station dataclass."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
import gzip
import io
import json
import typing

import dataclasses_json
from dataclasses_json import Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Station:
    station_id: int = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_code: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_code"))
    station_name: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    station_city: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_city"))
    station_synonym: typing.Optional[str] = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_synonym"))
    active_from: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="active_from"))
    active_to: typing.Optional[str] = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="active_to"))
    longitude: float = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    latitude: float = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    network_id: int = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="network_id"))
    network_code: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="network_code"))
    network_name: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="network_name"))
    setting_name: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="setting_name"))
    setting_short: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="setting_short"))
    type_name: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="type_name"))
    street: typing.Optional[str] = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="street"))
    street_nr: typing.Optional[str] = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="street_nr"))
    zip_code: typing.Optional[str] = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="zip_code"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> "Station":
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        return dataclasses.asdict(self)

    def to_byte_array(self, content_type_string: str) -> bytes:
        content_type = content_type_string.split(";")[0].strip()
        payload: bytes | str | None = None
        if content_type.replace("+gzip", "") == "application/json":
            payload = self.to_json()
        if payload is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        if content_type.endswith("+gzip"):
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode="wb") as gzip_file:
                    gzip_file.write(payload)
                payload = stream.getvalue()
        return payload

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: str | None = None) -> typing.Optional["Station"]:
        if data is None:
            return None
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            return cls.from_serializer_dict(data)
        content_type = (content_type_string or "application/octet-stream").split(";")[0].strip()
        if content_type.endswith("+gzip"):
            stream = io.BytesIO(data) if isinstance(data, bytes) else data
            with gzip.GzipFile(fileobj=stream, mode="rb") as gzip_file:
                data = gzip_file.read()
        if content_type.replace("+gzip", "") == "application/json":
            data_str = data.decode("utf-8") if isinstance(data, bytes) else data
            return cls.from_serializer_dict(json.loads(data_str))
        raise NotImplementedError(f"Unsupported media type {content_type}")

    @classmethod
    def create_instance(cls) -> "Station":
        return cls(
            station_id=21,
            station_code="DEBE021",
            station_name="Berlin Wedding",
            station_city="Berlin",
            station_synonym="BEWT",
            active_from="2000-01-01",
            active_to=None,
            longitude=13.3495,
            latitude=52.5491,
            network_id=3,
            network_code="BE",
            network_name="Berlin",
            setting_name="urban area",
            setting_short="urban",
            type_name="background",
            street="Amrumer Str.",
            street_nr="4-6",
            zip_code="13353",
        )
