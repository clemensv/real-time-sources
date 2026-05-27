"""Component dataclass."""

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
class Component:
    component_id: int = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="component_id"))
    component_code: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="component_code"))
    symbol: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="symbol"))
    unit: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unit"))
    name: str = dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> "Component":
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
    def from_data(cls, data: typing.Any, content_type_string: str | None = None) -> typing.Optional["Component"]:
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
    def create_instance(cls) -> "Component":
        return cls(
            component_id=5,
            component_code="NO2",
            symbol="NO₂",
            unit="µg/m³",
            name="Nitrogen dioxide",
        )
