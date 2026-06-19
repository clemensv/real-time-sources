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
from test_site import Test_Site
from usgs_iv_producer_kafka_producer.producer import USGSSiteTimeseriesEventProducer
from usgs_iv_producer_data import SiteTimeseries
from test_sitetimeseries import Test_SiteTimeseries
from usgs_iv_producer_kafka_producer.producer import USGSInstantaneousValuesEventProducer
from usgs_iv_producer_data import OtherParameter
from test_otherparameter import Test_OtherParameter
from usgs_iv_producer_data import Precipitation
from test_precipitation import Test_Precipitation
from usgs_iv_producer_data import Streamflow
from test_streamflow import Test_Streamflow
from usgs_iv_producer_data import GageHeight
from test_gageheight import Test_GageHeight
from usgs_iv_producer_data import WaterTemperature
from test_watertemperature import Test_WaterTemperature
from usgs_iv_producer_data import DissolvedOxygen
from test_dissolvedoxygen import Test_DissolvedOxygen
from usgs_iv_producer_data import PH
from test_ph import Test_PH
from usgs_iv_producer_data import SpecificConductance
from test_specificconductance import Test_SpecificConductance
from usgs_iv_producer_data import Turbidity
from test_turbidity import Test_Turbidity
from usgs_iv_producer_data import AirTemperature
from test_airtemperature import Test_AirTemperature
from usgs_iv_producer_data import WindSpeed
from test_windspeed import Test_WindSpeed
from usgs_iv_producer_data import WindDirection
from test_winddirection import Test_WindDirection
from usgs_iv_producer_data import RelativeHumidity
from test_relativehumidity import Test_RelativeHumidity
from usgs_iv_producer_data import BarometricPressure
from test_barometricpressure import Test_BarometricPressure
from usgs_iv_producer_data import TurbidityFNU
from test_turbidityfnu import Test_TurbidityFNU
from usgs_iv_producer_data import FDOM
from test_fdom import Test_FDOM
from usgs_iv_producer_data import ReservoirStorage
from test_reservoirstorage import Test_ReservoirStorage
from usgs_iv_producer_data import LakeElevationNGVD29
from test_lakeelevationngvd29 import Test_LakeElevationNGVD29
from usgs_iv_producer_data import WaterDepth
from test_waterdepth import Test_WaterDepth
from usgs_iv_producer_data import EquipmentStatus
from test_equipmentstatus import Test_EquipmentStatus
from usgs_iv_producer_data import TidallyFilteredDischarge
from test_tidallyfiltereddischarge import Test_TidallyFilteredDischarge
from usgs_iv_producer_data import WaterVelocity
from test_watervelocity import Test_WaterVelocity
from usgs_iv_producer_data import EstuaryElevationNGVD29
from test_estuaryelevationngvd29 import Test_EstuaryElevationNGVD29
from usgs_iv_producer_data import LakeElevationNAVD88
from test_lakeelevationnavd88 import Test_LakeElevationNAVD88
from usgs_iv_producer_data import Salinity
from test_salinity import Test_Salinity
from usgs_iv_producer_data import GateOpening
from test_gateopening import Test_GateOpening
from usgs_iv_producer_kafka_producer.producer import USGSSitesMqttEventProducer
from usgs_iv_producer_kafka_producer.producer import USGSSiteTimeseriesMqttEventProducer
from usgs_iv_producer_kafka_producer.producer import USGSInstantaneousValuesMqttEventProducer
from usgs_iv_producer_kafka_producer.producer import USGSSitesAmqpEventProducer
from usgs_iv_producer_kafka_producer.producer import USGSSiteTimeseriesAmqpEventProducer
from usgs_iv_producer_kafka_producer.producer import USGSInstantaneousValuesAmqpEventProducer

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
        producer_instance.send_usgs_sites_site(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_sites_site_timeseries(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_other_parameter(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_precipitation(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_streamflow(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_gage_height(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_water_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_dissolved_oxygen(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_p_h(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_specific_conductance(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_turbidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_air_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_wind_speed(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_wind_direction(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_relative_humidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_barometric_pressure(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_turbidity_fnu(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_f_dom(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_reservoir_storage(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_lake_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_water_depth(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_equipment_status(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_tidally_filtered_discharge(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_water_velocity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_estuary_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_lake_elevation_navd88(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_salinity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
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
        producer_instance.send_usgs_instantaneous_values_gate_opening(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd=f'test_{i}', site_no=f'test_{i}', parameter_cd=f'test_{i}', timeseries_cd=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_usgs_sites_mqtt_usgssitesmqttsite(kafka_emulator):
    """Test the USGSSitesMqttSite event from the USGS.Sites.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_sites_mqtt_usgssitesmqttsite',  # Unique group per test
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
    producer_instance = USGSSitesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Site.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_sites_mqtt_site(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_sitetimeseries_mqtt_usgssitetimeseriesmqttsitetimeseries(kafka_emulator):
    """Test the USGSSiteTimeseriesMqttSiteTimeseries event from the USGS.SiteTimeseries.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_sitetimeseries_mqtt_usgssitetimeseriesmqttsitetimeseries',  # Unique group per test
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
    producer_instance = USGSSiteTimeseriesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SiteTimeseries.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_site_timeseries_mqtt_site_timeseries(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttotherparameter(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttOtherParameter event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttotherparameter',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_OtherParameter.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_other_parameter(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttprecipitation(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttPrecipitation event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttprecipitation',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Precipitation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_precipitation(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttstreamflow(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttStreamflow event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttstreamflow',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Streamflow.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_streamflow(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttgageheight(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttGageHeight event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttgageheight',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_GageHeight.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_gage_height(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwatertemperature(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttWaterTemperature event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwatertemperature',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_water_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttdissolvedoxygen(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttDissolvedOxygen event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttdissolvedoxygen',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_DissolvedOxygen.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_dissolved_oxygen(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttph(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttPH event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttph',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_PH.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_p_h(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttspecificconductance(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttSpecificConductance event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttspecificconductance',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SpecificConductance.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_specific_conductance(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttturbidity(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttTurbidity event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttturbidity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Turbidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_turbidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttairtemperature(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttAirTemperature event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttairtemperature',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_air_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwindspeed(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttWindSpeed event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwindspeed',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WindSpeed.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_wind_speed(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwinddirection(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttWindDirection event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwinddirection',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WindDirection.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_wind_direction(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttrelativehumidity(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttRelativeHumidity event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttrelativehumidity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RelativeHumidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_relative_humidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttbarometricpressure(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttBarometricPressure event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttbarometricpressure',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_BarometricPressure.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_barometric_pressure(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttturbidityfnu(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttTurbidityFNU event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttturbidityfnu',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_TurbidityFNU.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_turbidity_fnu(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttfdom(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttFDOM event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttfdom',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_FDOM.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_f_dom(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttreservoirstorage(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttReservoirStorage event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttreservoirstorage',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ReservoirStorage.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_reservoir_storage(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttlakeelevationngvd29(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttLakeElevationNGVD29 event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttlakeelevationngvd29',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_LakeElevationNGVD29.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwaterdepth(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttWaterDepth event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwaterdepth',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterDepth.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_water_depth(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttequipmentstatus(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttEquipmentStatus event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttequipmentstatus',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_EquipmentStatus.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_equipment_status(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqtttidallyfiltereddischarge(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttTidallyFilteredDischarge event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqtttidallyfiltereddischarge',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_TidallyFilteredDischarge.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_tidally_filtered_discharge(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwatervelocity(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttWaterVelocity event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttwatervelocity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterVelocity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_water_velocity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttestuaryelevationngvd29(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttEstuaryElevationNGVD29 event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttestuaryelevationngvd29',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_EstuaryElevationNGVD29.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttlakeelevationnavd88(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttLakeElevationNAVD88 event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttlakeelevationnavd88',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_LakeElevationNAVD88.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_lake_elevation_navd88(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttsalinity(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttSalinity event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttsalinity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Salinity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_salinity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttgateopening(kafka_emulator):
    """Test the USGSInstantaneousValuesMqttGateOpening event from the USGS.InstantaneousValues.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_mqtt_usgsinstantaneousvaluesmqttgateopening',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_GateOpening.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_mqtt_gate_opening(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_sites_amqp_usgssitesamqpsite(kafka_emulator):
    """Test the USGSSitesAmqpSite event from the USGS.Sites.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_sites_amqp_usgssitesamqpsite',  # Unique group per test
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
    producer_instance = USGSSitesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Site.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_sites_amqp_site(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_sitetimeseries_amqp_usgssitetimeseriesamqpsitetimeseries(kafka_emulator):
    """Test the USGSSiteTimeseriesAmqpSiteTimeseries event from the USGS.SiteTimeseries.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_sitetimeseries_amqp_usgssitetimeseriesamqpsitetimeseries',  # Unique group per test
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
    producer_instance = USGSSiteTimeseriesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SiteTimeseries.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_site_timeseries_amqp_site_timeseries(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpotherparameter(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpOtherParameter event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpotherparameter',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_OtherParameter.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_other_parameter(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpprecipitation(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpPrecipitation event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpprecipitation',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Precipitation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_precipitation(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpstreamflow(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpStreamflow event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpstreamflow',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Streamflow.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_streamflow(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpgageheight(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpGageHeight event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpgageheight',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_GageHeight.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_gage_height(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwatertemperature(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpWaterTemperature event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwatertemperature',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_water_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpdissolvedoxygen(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpDissolvedOxygen event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpdissolvedoxygen',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_DissolvedOxygen.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_dissolved_oxygen(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpph(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpPH event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpph',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_PH.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_p_h(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpspecificconductance(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpSpecificConductance event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpspecificconductance',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SpecificConductance.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_specific_conductance(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpturbidity(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpTurbidity event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpturbidity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Turbidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_turbidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpairtemperature(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpAirTemperature event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpairtemperature',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_air_temperature(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwindspeed(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpWindSpeed event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwindspeed',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WindSpeed.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_wind_speed(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwinddirection(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpWindDirection event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwinddirection',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WindDirection.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_wind_direction(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqprelativehumidity(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpRelativeHumidity event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqprelativehumidity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RelativeHumidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_relative_humidity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpbarometricpressure(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpBarometricPressure event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpbarometricpressure',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_BarometricPressure.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_barometric_pressure(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpturbidityfnu(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpTurbidityFNU event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpturbidityfnu',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_TurbidityFNU.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_turbidity_fnu(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpfdom(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpFDOM event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpfdom',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_FDOM.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_f_dom(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpreservoirstorage(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpReservoirStorage event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpreservoirstorage',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ReservoirStorage.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_reservoir_storage(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqplakeelevationngvd29(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpLakeElevationNGVD29 event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqplakeelevationngvd29',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_LakeElevationNGVD29.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_lake_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwaterdepth(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpWaterDepth event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwaterdepth',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterDepth.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_water_depth(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpequipmentstatus(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpEquipmentStatus event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpequipmentstatus',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_EquipmentStatus.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_equipment_status(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqptidallyfiltereddischarge(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpTidallyFilteredDischarge event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqptidallyfiltereddischarge',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_TidallyFilteredDischarge.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_tidally_filtered_discharge(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwatervelocity(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpWaterVelocity event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpwatervelocity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterVelocity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_water_velocity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpestuaryelevationngvd29(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpEstuaryElevationNGVD29 event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpestuaryelevationngvd29',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_EstuaryElevationNGVD29.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_estuary_elevation_ngvd29(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqplakeelevationnavd88(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpLakeElevationNAVD88 event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqplakeelevationnavd88',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_LakeElevationNAVD88.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_lake_elevation_navd88(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpsalinity(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpSalinity event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpsalinity',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Salinity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_salinity(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpgateopening(kafka_emulator):
    """Test the USGSInstantaneousValuesAmqpGateOpening event from the USGS.InstantaneousValues.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_usgs_instantaneousvalues_amqp_usgsinstantaneousvaluesamqpgateopening',  # Unique group per test
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
    producer_instance = USGSInstantaneousValuesAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_GateOpening.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_usgs_instantaneous_values_amqp_gate_opening(_source_uri = f'test_{i}', _agency_cd = f'test_{i}', _site_no = f'test_{i}', _parameter_cd = f'test_{i}', _timeseries_cd = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
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

    producer_instance.send_usgs_instantaneous_values_other_parameter(_source_uri = shared_key_value, _agency_cd = shared_key_value, _site_no = shared_key_value, _parameter_cd = shared_key_value, _timeseries_cd = shared_key_value, data = data1)
    producer_instance.send_usgs_instantaneous_values_precipitation(_source_uri = shared_key_value, _agency_cd = shared_key_value, _site_no = shared_key_value, _parameter_cd = shared_key_value, _timeseries_cd = shared_key_value, data = data2)
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