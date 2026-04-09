""" Metar dataclass. """

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
class Metar:
    """
    METAR aviation weather observation from the AviationWeather.gov API.

    Attributes:
        icao_id (str)
        obs_time (str)
        report_time (typing.Optional[str])
        temp (typing.Optional[float])
        dewp (typing.Optional[float])
        wdir (typing.Optional[int])
        wspd (typing.Optional[int])
        wgst (typing.Optional[int])
        visib (typing.Optional[str])
        altim (typing.Optional[float])
        slp (typing.Optional[float])
        qc_field (typing.Optional[int])
        wx_string (typing.Optional[str])
        metar_type (typing.Optional[str])
        raw_ob (str)
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        elevation (typing.Optional[float])
        flt_cat (typing.Optional[str])
        clouds (typing.Optional[str])
        name (typing.Optional[str])
    """


    icao_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icao_id"))
    obs_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="obs_time"))
    report_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="report_time"))
    temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp"))
    dewp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dewp"))
    wdir: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wdir"))
    wspd: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wspd"))
    wgst: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wgst"))
    visib: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visib"))
    altim: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altim"))
    slp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="slp"))
    qc_field: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="qc_field"))
    wx_string: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wx_string"))
    metar_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="metar_type"))
    raw_ob: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="raw_ob"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    elevation: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="elevation"))
    flt_cat: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="flt_cat"))
    clouds: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="clouds"))
    name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Metar':
        """Converts a dictionary to a dataclass instance."""
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """Converts the dataclass to a dictionary."""
        return self.to_dict()

    def to_byte_array(self, content_type: str = "application/json") -> bytes:
        """Converts the dataclass to a byte array."""
        if content_type == "application/json":
            return json.dumps(self.to_serializer_dict()).encode("utf-8")
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        """Converts the dataclass to a JSON string."""
        return json.dumps(self.to_serializer_dict())
