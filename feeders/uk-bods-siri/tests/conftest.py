from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "uk_bods_siri_core",
    ROOT / "uk_bods_siri_kafka",
    ROOT / "uk_bods_siri_mqtt",
    ROOT / "uk_bods_siri_amqp",
    ROOT / "uk_bods_siri_producer" / "uk_bods_siri_producer_data" / "src",
    ROOT / "uk_bods_siri_producer" / "uk_bods_siri_producer_kafka_producer" / "src",
    ROOT / "uk_bods_siri_mqtt_producer" / "uk_bods_siri_mqtt_producer_data" / "src",
    ROOT / "uk_bods_siri_mqtt_producer" / "uk_bods_siri_mqtt_producer_mqtt_client" / "src",
    ROOT / "uk_bods_siri_amqp_producer" / "uk_bods_siri_amqp_producer_data" / "src",
    ROOT / "uk_bods_siri_amqp_producer" / "uk_bods_siri_amqp_producer_amqp_producer" / "src",
]
for path in PATHS:
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)
