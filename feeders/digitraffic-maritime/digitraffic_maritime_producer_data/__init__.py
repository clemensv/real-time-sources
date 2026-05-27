"""Compatibility wrapper for the generated Digitraffic Maritime data package."""

from pathlib import Path


_GENERATED_PACKAGE_DIR = (
    Path(__file__).resolve().parents[1]
    / "digitraffic_maritime_producer"
    / "digitraffic_maritime_producer_data"
    / "src"
    / "digitraffic_maritime_producer_data"
)

if _GENERATED_PACKAGE_DIR.is_dir():
    __path__.append(str(_GENERATED_PACKAGE_DIR))


from .berth import Berth
from .digitraffic_maritime_producer_data import VesselLocation
from .digitraffic_maritime_producer_data import VesselMetadata
from .portarea import PortArea
from .portcall import PortCall
from .portcallagent import PortCallAgent
from .portcallareadetail import PortCallAreaDetail
from .portlocation import PortLocation
from .vesseldetails import VesselDetails


__all__ = [
    "Berth",
    "PortArea",
    "PortCall",
    "PortCallAgent",
    "PortCallAreaDetail",
    "PortLocation",
    "VesselDetails",
    "VesselLocation",
    "VesselMetadata",
]