"""Pytest bootstrap for local package imports in the RWS source tree."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LOCAL_SRC_DIRS = [
    ROOT / "rws_waterwebservices_producer" / "rws_waterwebservices_producer_data" / "src",
    ROOT / "rws_waterwebservices_producer" / "rws_waterwebservices_producer_kafka_producer" / "src",
]

for src_dir in reversed(LOCAL_SRC_DIRS):
    src_path = str(src_dir)
    if src_dir.exists() and src_path not in sys.path:
        sys.path.insert(0, src_path)
