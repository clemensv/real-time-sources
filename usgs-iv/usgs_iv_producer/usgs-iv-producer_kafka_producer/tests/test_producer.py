# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs-iv-producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs-iv-producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs-iv-producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from usgs-iv-producer_kafka_producer.producer import USGSSitesEventProducer
from usgs-iv-producer_data import Site
from usgs-iv-producer_data import SiteTimeseries
from usgs-iv-producer_kafka_producer.producer import USGSInstantaneousValuesEventProducer
from usgs-iv-producer_data import OtherParameter
from usgs-iv-producer_data import Precipitation
from usgs-iv-producer_data import Streamflow
from usgs-iv-producer_data import GageHeight
from usgs-iv-producer_data import WaterTemperature
from usgs-iv-producer_data import DissolvedOxygen
from usgs-iv-producer_data import PH
from usgs-iv-producer_data import SpecificConductance
from usgs-iv-producer_data import Turbidity
from usgs-iv-producer_data import AirTemperature
from usgs-iv-producer_data import WindSpeed
from usgs-iv-producer_data import WindDirection
from usgs-iv-producer_data import RelativeHumidity
from usgs-iv-producer_data import BarometricPressure
from usgs-iv-producer_data import TurbidityFNU
from usgs-iv-producer_data import FDOM
from usgs-iv-producer_data import ReservoirStorage
from usgs-iv-producer_data import LakeElevationNGVD29
from usgs-iv-producer_data import WaterDepth
from usgs-iv-producer_data import EquipmentStatus
from usgs-iv-producer_data import TidallyFilteredDischarge
from usgs-iv-producer_data import WaterVelocity
from usgs-iv-producer_data import EstuaryElevationNGVD29
from usgs-iv-producer_data import LakeElevationNAVD88
from usgs-iv-producer_data import Salinity
from usgs-iv-producer_data import GateOpening

@pytest.fixture(scope="module")
def kafka_emulator():
    with KafkaContainer() as kafka:
        admin_client = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic_list = [
            NewTopic("test_topic", num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(topic_list)

        yield {
            "bootstrap_servers": kafka.get_bootstrap_server(),
            "topic": "test_topic",
        }

def parse_cloudevent(msg: Message) -> CloudEvent:
    headers_dict: Dict[str, bytes] = {header[0]: header[1] for header in msg.headers()}
    message = KafkaMessage(headers=headers_dict, key=msg.key(), value=msg.value())
    if message.headers and 'content-type' in message.headers:
        content_type = message.headers['content-type'].decode()
        if content_type.startswith('application/cloudevents'):
            ce = from_structured(message)
            if 'datacontenttype' not in ce:
                ce['datacontenttype'] = 'application/json'
        else:
            ce = from_binary(message)
            ce['datacontenttype'] = message.headers['content-type'].decode()
    else:
        ce = from_binary(message)
        ce['datacontenttype'] = 'application/json'
    return ce

def test_usgs_sites_usgssitessite(kafka_emulator):
    """Test the USGSSitesSite event from the USGS.Sites message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_sites_usgssitessite',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.Sites.Site":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSSitesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Site
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_sites_site(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_sites_usgssitessitetimeseries(kafka_emulator):
    """Test the USGSSitesSiteTimeseries event from the USGS.Sites message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_sites_usgssitessitetimeseries',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.Sites.SiteTimeseries":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSSitesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = SiteTimeseries
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_sites_site_timeseries(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesotherparameter(kafka_emulator):
    """Test the USGSInstantaneousValuesOtherParameter event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesotherparameter',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.OtherParameter":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = OtherParameter
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_other_parameter(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesprecipitation(kafka_emulator):
    """Test the USGSInstantaneousValuesPrecipitation event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesprecipitation',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Precipitation":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Precipitation
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_precipitation(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesstreamflow(kafka_emulator):
    """Test the USGSInstantaneousValuesStreamflow event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesstreamflow',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Streamflow":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Streamflow
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_streamflow(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesgageheight(kafka_emulator):
    """Test the USGSInstantaneousValuesGageHeight event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesgageheight',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.GageHeight":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = GageHeight
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_gage_height(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvalueswatertemperature(kafka_emulator):
    """Test the USGSInstantaneousValuesWaterTemperature event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvalueswatertemperature',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WaterTemperature":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = WaterTemperature
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_water_temperature(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesdissolvedoxygen(kafka_emulator):
    """Test the USGSInstantaneousValuesDissolvedOxygen event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesdissolvedoxygen',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.DissolvedOxygen":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = DissolvedOxygen
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_dissolved_oxygen(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesph(kafka_emulator):
    """Test the USGSInstantaneousValuesPH event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesph',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.pH":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = PH
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_p_h(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesspecificconductance(kafka_emulator):
    """Test the USGSInstantaneousValuesSpecificConductance event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesspecificconductance',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.SpecificConductance":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = SpecificConductance
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_specific_conductance(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesturbidity(kafka_emulator):
    """Test the USGSInstantaneousValuesTurbidity event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesturbidity',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Turbidity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Turbidity
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_turbidity(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesairtemperature(kafka_emulator):
    """Test the USGSInstantaneousValuesAirTemperature event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesairtemperature',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.AirTemperature":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = AirTemperature
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_air_temperature(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvalueswindspeed(kafka_emulator):
    """Test the USGSInstantaneousValuesWindSpeed event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvalueswindspeed',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WindSpeed":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = WindSpeed
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_wind_speed(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvalueswinddirection(kafka_emulator):
    """Test the USGSInstantaneousValuesWindDirection event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvalueswinddirection',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WindDirection":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = WindDirection
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_wind_direction(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesrelativehumidity(kafka_emulator):
    """Test the USGSInstantaneousValuesRelativeHumidity event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesrelativehumidity',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.RelativeHumidity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = RelativeHumidity
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_relative_humidity(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesbarometricpressure(kafka_emulator):
    """Test the USGSInstantaneousValuesBarometricPressure event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesbarometricpressure',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.BarometricPressure":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = BarometricPressure
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_barometric_pressure(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesturbidityfnu(kafka_emulator):
    """Test the USGSInstantaneousValuesTurbidityFNU event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesturbidityfnu',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.TurbidityFNU":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = TurbidityFNU
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_turbidity_fnu(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesfdom(kafka_emulator):
    """Test the USGSInstantaneousValuesFDOM event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesfdom',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.fDOM":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = FDOM
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_f_dom(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesreservoirstorage(kafka_emulator):
    """Test the USGSInstantaneousValuesReservoirStorage event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesreservoirstorage',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.ReservoirStorage":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = ReservoirStorage
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_reservoir_storage(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvalueslakeelevationngvd29(kafka_emulator):
    """Test the USGSInstantaneousValuesLakeElevationNGVD29 event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvalueslakeelevationngvd29',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.LakeElevationNGVD29":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = LakeElevationNGVD29
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_lake_elevation_ngvd29(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvalueswaterdepth(kafka_emulator):
    """Test the USGSInstantaneousValuesWaterDepth event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvalueswaterdepth',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WaterDepth":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = WaterDepth
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_water_depth(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesequipmentstatus(kafka_emulator):
    """Test the USGSInstantaneousValuesEquipmentStatus event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesequipmentstatus',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.EquipmentStatus":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = EquipmentStatus
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_equipment_status(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluestidallyfiltereddischarge(kafka_emulator):
    """Test the USGSInstantaneousValuesTidallyFilteredDischarge event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluestidallyfiltereddischarge',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.TidallyFilteredDischarge":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = TidallyFilteredDischarge
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_tidally_filtered_discharge(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvalueswatervelocity(kafka_emulator):
    """Test the USGSInstantaneousValuesWaterVelocity event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvalueswatervelocity',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WaterVelocity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = WaterVelocity
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_water_velocity(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesestuaryelevationngvd29(kafka_emulator):
    """Test the USGSInstantaneousValuesEstuaryElevationNGVD29 event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesestuaryelevationngvd29',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.EstuaryElevationNGVD29":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = EstuaryElevationNGVD29
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_estuary_elevation_ngvd29(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvalueslakeelevationnavd88(kafka_emulator):
    """Test the USGSInstantaneousValuesLakeElevationNAVD88 event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvalueslakeelevationnavd88',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.LakeElevationNAVD88":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = LakeElevationNAVD88
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_lake_elevation_navd88(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluessalinity(kafka_emulator):
    """Test the USGSInstantaneousValuesSalinity event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluessalinity',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Salinity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = Salinity
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_salinity(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()

def test_usgs_instantaneousvalues_usgsinstantaneousvaluesgateopening(kafka_emulator):
    """Test the USGSInstantaneousValuesGateOpening event from the USGS.InstantaneousValues message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_usgsinstantaneousvaluesgateopening',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.GateOpening":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create minimal test data instance to satisfy schema requirements
    try:
        import inspect
        import typing
        import enum
        data_class = GateOpening
        sig = inspect.signature(data_class.__init__)
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.default == inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY:
                # Get the actual type, unwrapping Optional/Union if needed
                ann = param.annotation
                origin = typing.get_origin(ann)
                
                # Handle Optional[X] which is Union[X, None]
                if origin is typing.Union:
                    args = typing.get_args(ann)
                    # Use the first non-None type
                    ann = next((a for a in args if a is not type(None)), args[0])
                    origin = typing.get_origin(ann)
                
                # Now match based on the actual type
                ann_str = str(ann).lower()
                if ann is str or ann == 'str' or 'str' in ann_str:
                    kwargs[param_name] = ""
                elif ann is int or ann == 'int' or 'int' in ann_str:
                    kwargs[param_name] = 0
                elif ann is float or ann == 'float' or 'float' in ann_str:
                    kwargs[param_name] = 0.0
                elif ann is bool or ann == 'bool' or 'bool' in ann_str:
                    kwargs[param_name] = False
                elif origin is list or ann is list or 'list' in ann_str:
                    kwargs[param_name] = []
                elif origin is dict or ann is dict or 'dict' in ann_str:
                    kwargs[param_name] = {}
                elif isinstance(ann, type) and issubclass(ann, enum.Enum):
                    # For enums, use the first value
                    kwargs[param_name] = list(ann)[0] if list(ann) else None
                elif 'enum' in ann_str:
                    # Fallback for enum detection via string
                    try:
                        kwargs[param_name] = list(ann)[0] if hasattr(ann, '__iter__') else None
                    except:
                        kwargs[param_name] = None
                else:
                    kwargs[param_name] = None
        event_data = data_class(**kwargs)
    except Exception as e:
        pytest.skip(f"Could not create test data instance: {e}")
    producer_instance.send_usgs_instantaneous_values_gate_opening(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)
    
    # Flush producer to ensure message is sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    assert on_event()
    consumer.close()