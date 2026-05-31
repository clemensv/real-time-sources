import os
import sys


_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_FEEDER_DIR = os.path.abspath(os.path.join(_TEST_DIR, ".."))

_EXTRA_PATHS = [
    _FEEDER_DIR,
    os.path.join(_FEEDER_DIR, "meteoalarm_mqtt"),
    os.path.join(_FEEDER_DIR, "meteoalarm_amqp"),
    os.path.join(_FEEDER_DIR, "meteoalarm_producer", "meteoalarm_producer_data", "src"),
    os.path.join(_FEEDER_DIR, "meteoalarm_producer", "meteoalarm_producer_kafka_producer", "src"),
    os.path.join(_FEEDER_DIR, "meteoalarm_mqtt_producer", "meteoalarm_mqtt_producer_data", "src"),
    os.path.join(_FEEDER_DIR, "meteoalarm_mqtt_producer", "meteoalarm_mqtt_producer_mqtt_client", "src"),
]

for extra_path in reversed(_EXTRA_PATHS):
    if extra_path not in sys.path:
        sys.path.insert(0, extra_path)
