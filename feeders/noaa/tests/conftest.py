import os
import sys


_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_FEEDER_DIR = os.path.abspath(os.path.join(_TEST_DIR, ".."))

_EXTRA_PATHS = [
    _FEEDER_DIR,
    # The transport-agnostic core and the MQTT/AMQP apps each live one level
    # deeper than their wrapper directory (e.g. `noaa_core/noaa_core/`). The
    # wrapper dirs sit directly under _FEEDER_DIR, so without these entries
    # `import noaa_core` resolves to the *wrapper* as an empty namespace
    # package and `from noaa_core import NOAAClient` fails with
    # "unknown location".
    os.path.join(_FEEDER_DIR, "noaa_core"),
    os.path.join(_FEEDER_DIR, "noaa_producer", "noaa_producer_data", "src"),
    os.path.join(_FEEDER_DIR, "noaa_producer", "noaa_producer_kafka_producer", "src"),
]

for extra_path in reversed(_EXTRA_PATHS):
    if extra_path not in sys.path:
        sys.path.insert(0, extra_path)
