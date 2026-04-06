# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from usgs_iv_producer_kafka_producer.producer import USGSSitesEventProducer
from usgs_iv_producer_data import Site
from test_usgs_iv_producer_data_site import Test_Site
from usgs_iv_producer_kafka_producer.producer import USGSSiteTimeseriesEventProducer
from usgs_iv_producer_data import SiteTimeseries
from test_usgs_iv_producer_data_sitetimeseries import Test_SiteTimeseries
from usgs_iv_producer_kafka_producer.producer import USGSInstantaneousValuesEventProducer
from usgs_iv_producer_data import OtherParameter
from test_usgs_iv_producer_data_otherparameter import Test_OtherParameter
from usgs_iv_producer_data import Precipitation
from test_usgs_iv_producer_data_precipitation import Test_Precipitation
from usgs_iv_producer_data import Streamflow
from test_usgs_iv_producer_data_streamflow import Test_Streamflow
from usgs_iv_producer_data import GageHeight
from test_usgs_iv_producer_data_gageheight import Test_GageHeight
from usgs_iv_producer_data import WaterTemperature
from test_usgs_iv_producer_data_watertemperature import Test_WaterTemperature
from usgs_iv_producer_data import DissolvedOxygen
from test_usgs_iv_producer_data_dissolvedoxygen import Test_DissolvedOxygen
from usgs_iv_producer_data import PH
from test_usgs_iv_producer_data_ph import Test_PH
from usgs_iv_producer_data import SpecificConductance
from test_usgs_iv_producer_data_specificconductance import Test_SpecificConductance
from usgs_iv_producer_data import Turbidity
from test_usgs_iv_producer_data_turbidity import Test_Turbidity
from usgs_iv_producer_data import AirTemperature
from test_usgs_iv_producer_data_airtemperature import Test_AirTemperature
from usgs_iv_producer_data import WindSpeed
from test_usgs_iv_producer_data_windspeed import Test_WindSpeed
from usgs_iv_producer_data import WindDirection
from test_usgs_iv_producer_data_winddirection import Test_WindDirection
from usgs_iv_producer_data import RelativeHumidity
from test_usgs_iv_producer_data_relativehumidity import Test_RelativeHumidity
from usgs_iv_producer_data import BarometricPressure
from test_usgs_iv_producer_data_barometricpressure import Test_BarometricPressure
from usgs_iv_producer_data import TurbidityFNU
from test_usgs_iv_producer_data_turbidityfnu import Test_TurbidityFNU
from usgs_iv_producer_data import FDOM
from test_usgs_iv_producer_data_fdom import Test_FDOM
from usgs_iv_producer_data import ReservoirStorage
from test_usgs_iv_producer_data_reservoirstorage import Test_ReservoirStorage
from usgs_iv_producer_data import LakeElevationNGVD29
from test_usgs_iv_producer_data_lakeelevationngvd29 import Test_LakeElevationNGVD29
from usgs_iv_producer_data import WaterDepth
from test_usgs_iv_producer_data_waterdepth import Test_WaterDepth
from usgs_iv_producer_data import EquipmentStatus
from test_usgs_iv_producer_data_equipmentstatus import Test_EquipmentStatus
from usgs_iv_producer_data import TidallyFilteredDischarge
from test_usgs_iv_producer_data_tidallyfiltereddischarge import Test_TidallyFilteredDischarge
from usgs_iv_producer_data import WaterVelocity
from test_usgs_iv_producer_data_watervelocity import Test_WaterVelocity
from usgs_iv_producer_data import EstuaryElevationNGVD29
from test_usgs_iv_producer_data_estuaryelevationngvd29 import Test_EstuaryElevationNGVD29
from usgs_iv_producer_data import LakeElevationNAVD88
from test_usgs_iv_producer_data_lakeelevationnavd88 import Test_LakeElevationNAVD88
from usgs_iv_producer_data import Salinity
from test_usgs_iv_producer_data_salinity import Test_Salinity
from usgs_iv_producer_data import GateOpening
from test_usgs_iv_producer_data_gateopening import Test_GateOpening

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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.Sites.Site":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSSitesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Site.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_sites_site(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}".format(agency_cd=f'test_{i}', site_no=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_usgs_sitetimeseries_usgssitessitetimeseries(kafka_emulator):
    """Test the USGSSitesSiteTimeseries event from the USGS.SiteTimeseries message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_sitetimeseries_usgssitessitetimeseries',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.Sites.SiteTimeseries":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSSiteTimeseriesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SiteTimeseries.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_sites_site_timeseries(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.OtherParameter":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_OtherParameter.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_other_parameter(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Precipitation":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Precipitation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_precipitation(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Streamflow":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Streamflow.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_streamflow(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.GageHeight":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_GageHeight.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_gage_height(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WaterTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_water_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.DissolvedOxygen":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_DissolvedOxygen.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_dissolved_oxygen(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.pH":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_PH.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_p_h(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.SpecificConductance":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SpecificConductance.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_specific_conductance(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Turbidity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Turbidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_turbidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.AirTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_air_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WindSpeed":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WindSpeed.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_wind_speed(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WindDirection":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WindDirection.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_wind_direction(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.RelativeHumidity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RelativeHumidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_relative_humidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.BarometricPressure":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_BarometricPressure.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_barometric_pressure(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.TurbidityFNU":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_TurbidityFNU.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_turbidity_fnu(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.fDOM":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_FDOM.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_f_dom(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.ReservoirStorage":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ReservoirStorage.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_reservoir_storage(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.LakeElevationNGVD29":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_LakeElevationNGVD29.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_lake_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WaterDepth":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterDepth.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_water_depth(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.EquipmentStatus":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_EquipmentStatus.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_equipment_status(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.TidallyFilteredDischarge":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_TidallyFilteredDischarge.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_tidally_filtered_discharge(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.WaterVelocity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterVelocity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_water_velocity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.EstuaryElevationNGVD29":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_EstuaryElevationNGVD29.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_estuary_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.LakeElevationNAVD88":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_LakeElevationNAVD88.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_lake_elevation_navd88(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.Salinity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Salinity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_salinity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "USGS.InstantaneousValues.GateOpening":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_GateOpening.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_gate_opening(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _datetime = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_usgs_instantaneousvalues_cross_event_type_kafka_key(kafka_emulator):
    """Test that different event types in USGS.InstantaneousValues produce the same Kafka key for the same placeholder values"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_cross_key',
        'auto.offset.reset': 'latest'
    })
    consumer.subscribe([topic])

    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    # Drain any pre-existing messages before producing our test messages
    drain_timeout = time.time() + 3
    while time.time() < drain_timeout:
        msg = consumer.poll(0.5)
    time.sleep(1)

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')

    shared_key_value = "shared_entity_42"
    data1 = Test_OtherParameter.create_instance()
    data2 = Test_Precipitation.create_instance()

    producer_instance.send_usgs_instantaneous_values_other_parameter(_source_uri = shared_key_value, _agency_cd = shared_key_value, _site_no = shared_key_value, _parameter_cd = shared_key_value, _timeseries_cd = shared_key_value, _datetime = shared_key_value, data = data1)
    producer_instance.send_usgs_instantaneous_values_precipitation(_source_uri = shared_key_value, _agency_cd = shared_key_value, _site_no = shared_key_value, _parameter_cd = shared_key_value, _timeseries_cd = shared_key_value, _datetime = shared_key_value, data = data2)
    kafka_producer.flush(timeout=5.0)

    # Collect keys from both messages
    collected_keys = []
    timeout = time.time() + 20
    while len(collected_keys) < 2 and time.time() < timeout:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        cloudevent = parse_cloudevent(msg)
        if cloudevent['type'] in ["USGS.InstantaneousValues.OtherParameter", "USGS.InstantaneousValues.Precipitation"]:
            key = msg.key().decode('utf-8') if msg.key() else None
            collected_keys.append(key)

    assert len(collected_keys) == 2, f"Expected 2 messages but received {len(collected_keys)}"
    assert collected_keys[0] == collected_keys[1], \
        f"Expected same Kafka key for different event types but got '{collected_keys[0]}' and '{collected_keys[1]}'"
    expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=shared_key_value, site_no=shared_key_value, parameter_cd=shared_key_value, timeseries_cd=shared_key_value)
    assert collected_keys[0] == expected_key, \
        f"Expected Kafka key '{expected_key}' but got '{collected_keys[0]}'"
    consumer.close()