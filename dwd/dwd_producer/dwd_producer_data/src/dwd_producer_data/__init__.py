from .dwd_producer_data import Document
from .de.dwd.cdc import (
    StationMetadata,
    AirTemperature10Min,
    HourlyObservation,
    Alert,
    Precipitation10Min,
    Solar10Min,
    Wind10Min,
)

__all__ = [
    "Document",
    "StationMetadata",
    "AirTemperature10Min",
    "HourlyObservation",
    "Alert",
    "Precipitation10Min",
    "Solar10Min",
    "Wind10Min",
]
