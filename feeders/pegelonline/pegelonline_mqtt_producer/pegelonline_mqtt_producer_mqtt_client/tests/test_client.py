# pylint: disable=line-too-long, trailing-whitespace, missing-module-docstring, missing-function-docstring, missing-class-docstring, redefined-outer-name, unused-argument, broad-exception-caught, broad-exception-raised, invalid-name, trailing-newlines, wrong-import-position, import-error, no-name-in-module

import os
import sys
import pytest
import pytest_asyncio
import asyncio
import datetime
import time
import paho.mqtt.client as mqtt
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_mqtt_producer_mqtt_client/src')))

import pegelonline_mqtt_producer_data
from pegelonline_mqtt_producer_data import Station
from test_station import Test_Station
from pegelonline_mqtt_producer_data import CurrentMeasurement
from test_currentmeasurement import Test_CurrentMeasurement
from pegelonline_mqtt_producer_mqtt_client import DeWsvPegelonlineMqttMqttClient

@pytest_asyncio.fixture
async def mosquitto_broker():
    """Start Mosquitto MQTT broker in container."""
    container = DockerContainer("eclipse-mosquitto:2.0")
    container.with_exposed_ports(1883)
    container.with_command("mosquitto -c /mosquitto-no-auth.conf")
    
    container.start()
    
    try:
        # Wait for Mosquitto to start
        wait_for_logs(container, "mosquitto version .* running", timeout=10)
        await asyncio.sleep(2)  # Additional stabilization time
        
        # Get mapped port
        broker_port = container.get_exposed_port(1883)
        broker_host = "localhost"
        
        yield broker_host, broker_port
    finally:
        container.stop()

@pytest.mark.asyncio
async def test_de_wsv_pegelonline_mqtt_shared_paho_client_connect_multiplexes_py():
    """Regression for issue #485.

    Several generated clients are meant to share one paho client (one connection
    per multi-messagegroup source). Paho stores only one callback per event, so a
    later-instantiated client used to overwrite the shared ``on_connect`` and make
    an earlier client's ``connect()`` hang forever. A callback multiplexer must fan
    the CONNACK out to every instance so ``connect()`` resolves regardless of order.

    Deterministic (fake paho client, no broker): the second instance is created
    AFTER the first, then ``connect()`` on the FIRST instance must still complete.
    """
    class _FakeClient:
        def __init__(self):
            self.on_connect = None
            self.on_disconnect = None
            self.on_message = None

        def connect(self, *args, **kwargs):
            pass

        def loop_start(self):
            # Simulate the broker's CONNACK arriving on the network thread.
            if self.on_connect is not None:
                self.on_connect(self, None, {}, 0, None)

        def loop_stop(self, *args, **kwargs):
            pass

        def disconnect(self, *args, **kwargs):
            pass

    loop = asyncio.get_running_loop()
    shared = _FakeClient()
    first = DeWsvPegelonlineMqttMqttClient(shared, loop=loop)
    second = DeWsvPegelonlineMqttMqttClient(shared, loop=loop)  # would steal first's on_connect pre-fix

    mux = getattr(shared, "_xrcg_callback_multiplexer", None)
    assert mux is not None and len(mux._live()) == 2, \
        "both clients sharing one paho client must register on the callback multiplexer (#485)"

    try:
        await first.connect("broker", 1883, keepalive=5)
    except (asyncio.TimeoutError, TimeoutError):
        pytest.fail(
            "connect() on a shared-client instance timed out - a later client "
            "overwrote the shared on_connect callback (issue #485)"
        )
    assert first._connected is True



@pytest.mark.asyncio
async def test_de_wsv_pegelonline_mqtt_de_wsv_pegelonline_mqtt_station_py(mosquitto_broker):
    """Test publishing and receiving de.wsv.pegelonline.mqtt.Station message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Station.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DeWsvPegelonlineMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DeWsvPegelonlineMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_wsv_pegelonline_mqtt_station(mqtt_msg, cloud_event, data: pegelonline_mqtt_producer_data.Station, topic_params: dict):
        """Handler for de.wsv.pegelonline.mqtt.Station messages."""
        received_data.append(data)
        assert cloud_event['type'] == "de.wsv.pegelonline.Station"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_wsv_pegelonline_mqtt_station_async = on_de_wsv_pegelonline_mqtt_station
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_wsv_pegelonline_mqtt/de_wsv_pegelonline_mqtt_station"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_wsv_pegelonline_mqtt_station(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
            water_shortname=f"test_water_shortname_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json"
        )
    
    # Wait for all 5 messages to be received (with timeout)
    try:
        await asyncio.wait_for(received_event.wait(), timeout=10.0)
    except asyncio.TimeoutError:
        pytest.fail(f"Did not receive all 5 messages within timeout, got {len(received_data)}")
    
    # Verify all 5 messages received
    assert len(received_data) == 5, f"Expected 5 messages, got {len(received_data)}"
    
    # Cleanup
    await subscriber_client.disconnect()
    await publisher_client.disconnect()



@pytest.mark.asyncio
async def test_de_wsv_pegelonline_mqtt_de_wsv_pegelonline_mqtt_current_measurement_py(mosquitto_broker):
    """Test publishing and receiving de.wsv.pegelonline.mqtt.CurrentMeasurement message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_CurrentMeasurement.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = DeWsvPegelonlineMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = DeWsvPegelonlineMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_de_wsv_pegelonline_mqtt_current_measurement(mqtt_msg, cloud_event, data: pegelonline_mqtt_producer_data.CurrentMeasurement, topic_params: dict):
        """Handler for de.wsv.pegelonline.mqtt.CurrentMeasurement messages."""
        received_data.append(data)
        assert cloud_event['type'] == "de.wsv.pegelonline.CurrentMeasurement"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.de_wsv_pegelonline_mqtt_current_measurement_async = on_de_wsv_pegelonline_mqtt_current_measurement
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/de_wsv_pegelonline_mqtt/de_wsv_pegelonline_mqtt_current_measurement"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_de_wsv_pegelonline_mqtt_current_measurement(
            topic=test_topic,
            feedurl=f"test_feedurl_{i}",
            station_id=f"test_station_id_{i}",
            water_shortname=f"test_water_shortname_{i}",
            _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=test_data,
            content_type="application/json"
        )
    
    # Wait for all 5 messages to be received (with timeout)
    try:
        await asyncio.wait_for(received_event.wait(), timeout=10.0)
    except asyncio.TimeoutError:
        pytest.fail(f"Did not receive all 5 messages within timeout, got {len(received_data)}")
    
    # Verify all 5 messages received
    assert len(received_data) == 5, f"Expected 5 messages, got {len(received_data)}"
    
    # Cleanup
    await subscriber_client.disconnect()
    await publisher_client.disconnect()




@pytest.mark.asyncio
async def test_de_wsv_pegelonline_mqtt_disconnect_flushes_inflight_qos1_py():
    """Regression for issue #486.

    A short-lived ('--once') producer that publishes a QoS-1 message and then
    immediately disconnects must not drop the last-queued message. ``disconnect()``
    must wait for in-flight delivery (PUBACK) BEFORE stopping paho's network loop.

    Uses a fake paho client so the ordering is asserted deterministically without
    depending on broker/network timing.
    """
    calls = []

    class _FakeInfo:
        def __init__(self):
            self._published = False

        def wait_for_publish(self, timeout=None):
            calls.append("wait_for_publish")
            self._published = True

        def is_published(self):
            return self._published

    class _FakeClient:
        def __init__(self):
            self.on_message = None
            self.on_connect = None
            self.on_disconnect = None

        def publish(self, *args, **kwargs):
            calls.append("publish")
            return _FakeInfo()

        def disconnect(self, *args, **kwargs):
            calls.append("disconnect")

        def loop_stop(self, *args, **kwargs):
            calls.append("loop_stop")

    loop = asyncio.get_running_loop()
    client = DeWsvPegelonlineMqttMqttClient(_FakeClient(), loop=loop)

    # Simulate a QoS-1 publish still in flight, then disconnect immediately.
    client._track_inflight(client.client.publish("test/topic", b"{}", qos=1))
    await client.disconnect()

    assert "wait_for_publish" in calls, \
        "disconnect() must flush queued QoS-1 publishes before stopping the loop"
    assert calls.index("wait_for_publish") < calls.index("loop_stop"), \
        "disconnect() must wait for in-flight delivery BEFORE loop_stop()"
    assert calls.index("disconnect") < calls.index("loop_stop"), \
        "disconnect() must send DISCONNECT before stopping the loop"

