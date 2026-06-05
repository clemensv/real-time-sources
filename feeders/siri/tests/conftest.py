from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "siri_core",
    ROOT / "siri_kafka",
    ROOT / "siri_mqtt",
    ROOT / "siri_amqp",
    ROOT / "siri_producer" / "siri_producer_data" / "src",
    ROOT / "siri_producer" / "siri_producer_kafka_producer" / "src",
    ROOT / "siri_mqtt_producer" / "siri_mqtt_producer_data" / "src",
    ROOT / "siri_mqtt_producer" / "siri_mqtt_producer_mqtt_client" / "src",
    ROOT / "siri_amqp_producer" / "siri_amqp_producer_data" / "src",
    ROOT / "siri_amqp_producer" / "siri_amqp_producer_amqp_producer" / "src",
]
for path in PATHS:
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)
