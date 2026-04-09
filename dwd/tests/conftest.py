"""Pytest bootstrap for local package imports in the DWD source tree."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LOCAL_SRC_DIRS = [
    ROOT / "dwd_producer" / "dwd_producer_data" / "src",
    ROOT / "dwd_producer" / "dwd_producer_kafka_producer" / "src",
]

for src_dir in reversed(LOCAL_SRC_DIRS):
    src_path = str(src_dir)
    if src_dir.exists() and src_path not in sys.path:
        sys.path.insert(0, src_path)


import dwd_producer_data  # noqa: E402
from dwd_producer_data.de import (  # noqa: E402
    AirTemperature10Min,
    Alert,
    HourlyObservation,
    Precipitation10Min,
    Solar10Min,
    StationMetadata,
    Wind10Min,
)


dwd_producer_data.StationMetadata = StationMetadata
dwd_producer_data.AirTemperature10Min = AirTemperature10Min
dwd_producer_data.Precipitation10Min = Precipitation10Min
dwd_producer_data.Wind10Min = Wind10Min
dwd_producer_data.Solar10Min = Solar10Min
dwd_producer_data.HourlyObservation = HourlyObservation
dwd_producer_data.Alert = Alert
