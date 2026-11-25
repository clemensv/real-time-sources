# pylint: disable=line-too-long, trailing-whitespace, missing-module-docstring, missing-function-docstring, missing-class-docstring, wrong-import-position, import-error, no-name-in-module, protected-access

import importlib.util
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_mqtt_producer_mqtt_client/src')))

_SAMPLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'samples', 'sample.py'))


def _load_sample():
    """Import the generated samples/sample.py module by file path.

    Importing executes every top-level statement (the imports of the generated
    client classes, data types and message handlers) without running main(),
    so it fails loudly if the sample references anything the generator does not
    actually emit.
    """
    spec = importlib.util.spec_from_file_location("generated_sample", _SAMPLE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sample_imports_cleanly():
    """The generated samples/sample.py must import without error and expose its
    entry points. Guards against the sample referencing client classes, handler
    attributes or data types that the generator does not emit."""
    module = _load_sample()
    assert callable(module.main)
    assert callable(module.publish_samples)
    assert callable(module._make_paho_client)


def test_sample_defines_a_handler_for_every_message():
    """The sample must define an async handler function for each message."""
    module = _load_sample()
    assert hasattr(module, "handle_de_wsv_pegelonline_mqtt_station"), \
        "sample is missing handler 'handle_de_wsv_pegelonline_mqtt_station' for message 'de.wsv.pegelonline.mqtt.Station'"
    assert hasattr(module, "handle_de_wsv_pegelonline_mqtt_current_measurement"), \
        "sample is missing handler 'handle_de_wsv_pegelonline_mqtt_current_measurement' for message 'de.wsv.pegelonline.mqtt.CurrentMeasurement'"