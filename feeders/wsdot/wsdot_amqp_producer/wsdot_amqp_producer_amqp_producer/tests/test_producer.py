
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for wsdot_amqp_producer_amqp_producer
"""
import base64
import datetime
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from typing import Optional
from urllib.parse import quote_plus

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from proton import Message, symbol
from proton.utils import BlockingConnection

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wsdot_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wsdot_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../wsdot_amqp_producer_amqp_producer/src')))

from wsdot_amqp_producer_amqp_producer import *
from wsdot_amqp_producer_data import TrafficFlowStation
from test_trafficflowstation import Test_TrafficFlowStation
from wsdot_amqp_producer_data import TrafficFlowReading
from test_trafficflowreading import Test_TrafficFlowReading
from wsdot_amqp_producer_data import TravelTimeRoute
from test_traveltimeroute import Test_TravelTimeRoute
from wsdot_amqp_producer_data import MountainPassCondition
from test_mountainpasscondition import Test_MountainPassCondition
from wsdot_amqp_producer_data import WeatherStation
from test_weatherstation import Test_WeatherStation
from wsdot_amqp_producer_data import WeatherReading
from test_weatherreading import Test_WeatherReading
from wsdot_amqp_producer_data import TollRate
from test_tollrate import Test_TollRate
from wsdot_amqp_producer_data import CommercialVehicleRestriction
from test_commercialvehiclerestriction import Test_CommercialVehicleRestriction
from wsdot_amqp_producer_data import BorderCrossing
from test_bordercrossing import Test_BorderCrossing
from wsdot_amqp_producer_data import VesselLocation
from test_vessellocation import Test_VesselLocation
from wsdot_amqp_producer_data import RoadWeatherStation
from test_roadweatherstation import Test_RoadWeatherStation
from wsdot_amqp_producer_data import RoadWeatherReading
from test_roadweatherreading import Test_RoadWeatherReading
from wsdot_amqp_producer_data import HighwayAlert
from test_highwayalert import Test_HighwayAlert
from wsdot_amqp_producer_data import HighwayCamera
from test_highwaycamera import Test_HighwayCamera
from wsdot_amqp_producer_data import BridgeClearance
from test_bridgeclearance import Test_BridgeClearance
from wsdot_amqp_producer_data import TerminalSailingSpace
from test_terminalsailingspace import Test_TerminalSailingSpace



def _rabbitmq_queue_address(queue_name: str) -> str:
    return f"/queues/{queue_name}" if os.environ.get("RABBITMQ_VERSION", "4") != "3" else queue_name


def _declare_rabbitmq_queue(host: str, mgmt_port: int, queue_name: str):
    url = f"http://{host}:{mgmt_port}/api/queues/%2F/{queue_name}"
    payload = b'{"auto_delete": false, "durable": true, "arguments": {}}'
    auth = base64.b64encode(b"guest:guest").decode("ascii")
    last_error = None
    for _ in range(30):
        request = urllib.request.Request(
            url,
            data=payload,
            method="PUT",
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                if response.status in (201, 204):
                    return
                last_error = RuntimeError(f"RabbitMQ queue declaration returned {response.status}")
        except urllib.error.HTTPError as exc:
            if exc.code in (201, 204):
                return
            last_error = exc
        except Exception as exc:
            last_error = exc
        time.sleep(1)
    raise RuntimeError(f"Timed out declaring RabbitMQ queue {queue_name}") from last_error

ARTEMIS_BROKER_XML = """<?xml version='1.0'?>
<configuration xmlns="urn:activemq"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="urn:activemq /schema/artemis-configuration.xsd">
    <core xmlns="urn:activemq:core">
        <name>0.0.0.0</name>
        <persistence-enabled>false</persistence-enabled>
        <acceptors>
            <acceptor name="amqp">tcp://0.0.0.0:5672?protocols=AMQP;saslMechanisms=PLAIN,ANONYMOUS</acceptor>
        </acceptors>
        <security-settings>
            <security-setting match="#">
                <permission type="createNonDurableQueue" roles="amq"/>
                <permission type="deleteNonDurableQueue" roles="amq"/>
                <permission type="createDurableQueue" roles="amq"/>
                <permission type="deleteDurableQueue" roles="amq"/>
                <permission type="createAddress" roles="amq"/>
                <permission type="deleteAddress" roles="amq"/>
                <permission type="consume" roles="amq"/>
                <permission type="browse" roles="amq"/>
                <permission type="send" roles="amq"/>
                <permission type="manage" roles="amq"/>
            </security-setting>
        </security-settings>
        <address-settings>
            <address-setting match="#">
                <dead-letter-address>DLQ</dead-letter-address>
                <expiry-address>ExpiryQueue</expiry-address>
                <auto-create-queues>true</auto-create-queues>
                <auto-create-addresses>true</auto-create-addresses>
            </address-setting>
        </address-settings>
        <addresses>
            <address name="test-queue">
                <anycast>
                    <queue name="test-queue" />
                </anycast>
            </address>
        </addresses>
    </core>
</configuration>
"""

@pytest.fixture(scope="module")
def amqp_broker():
    """Create and start an AMQP broker container for testing.
    
    Uses ActiveMQ Artemis by default.
    Set AMQP_BROKER=rabbitmq environment variable to test with RabbitMQ.
    Set RABBITMQ_VERSION=3 or RABBITMQ_VERSION=4 to choose RabbitMQ version (default: 4).
    """
    broker_type = os.environ.get("AMQP_BROKER", "artemis").lower()
    
    if broker_type == "rabbitmq":
        rabbitmq_version = os.environ.get("RABBITMQ_VERSION", "4")
        image_tag = "3-management" if rabbitmq_version == "3" else "4-management"
        
        container = DockerContainer(f"rabbitmq:{image_tag}")
        container.with_bind_ports(5672, 5672)
        container.with_bind_ports(15672, 15672)
        container.with_env("RABBITMQ_DEFAULT_USER", "guest")
        container.with_env("RABBITMQ_DEFAULT_PASS", "guest")
        container.with_exposed_ports(5672, 15672)
        
        # RabbitMQ 3.x requires AMQP 1.0 plugin, RabbitMQ 4.0+ has native support
        if rabbitmq_version == "3":
            container.with_command(
                "bash", "-c", 
                "rabbitmq-plugins enable rabbitmq_amqp1_0 && docker-entrypoint.sh rabbitmq-server"
            )
        
        container.start()
        # Wait for RabbitMQ to be ready
        wait_for_logs(container, "Server startup complete", timeout=120)
        host = container.get_container_host_ip()
        if rabbitmq_version != "3":
            _declare_rabbitmq_queue(host, int(container.get_exposed_port(15672)), "test-queue")
        
        yield {
            "host": host,
            "port": int(container.get_exposed_port(5672)),
            "username": "guest",
            "password": "guest",
            "address": _rabbitmq_queue_address("test-queue")
        }
        
        container.stop()
    else:
        # Default: ActiveMQ Artemis
        # Create temp file for broker configuration
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(ARTEMIS_BROKER_XML)
            config_file = f.name
        
        try:
            container = DockerContainer("apache/activemq-artemis:latest")
            container.with_bind_ports(5672, 5672)
            container.with_env("ARTEMIS_USER", "guest")
            container.with_env("ARTEMIS_PASSWORD", "guest")
            container.with_volume_mapping(config_file, "/var/lib/artemis-instance/etc-override/broker.xml")
            container.with_exposed_ports(5672)
            
            # Wait for Artemis to be ready
            container.start()
            # Wait for broker to log that it's ready (AMQ241004 = "Artemis Server is now live")
            wait_for_logs(container, "AMQ241004", timeout=60)
            
            yield {
                "host": container.get_container_host_ip(),
                "port": int(container.get_exposed_port(5672)),
                "username": "guest",
                "password": "guest",
                "address": "test-queue"
            }
            
            container.stop()
        finally:
            if os.path.exists(config_file):
                os.unlink(config_file)

# Keep old fixture name for backwards compatibility
@pytest.fixture(scope="module")
def artemis_container(amqp_broker):
    """Alias for amqp_broker for backwards compatibility"""
    return amqp_broker

def _connection_url(host: str, port: int, username: Optional[str] = None, password: Optional[str] = None) -> str:
    if username and password:
        return f"amqp://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}"
    return f"amqp://{host}:{port}"


def _receive_single_message(config: dict, timeout: int = 30):
    connection = BlockingConnection(
        _connection_url(
            config["host"],
            config["port"],
            config.get("username"),
            config.get("password"),
        ),
        timeout=timeout,
    )
    receiver = connection.create_receiver(config["address"], credit=1)
    try:
        message = receiver.receive(timeout=timeout)
        receiver.accept()  # Explicitly accept/settle the message to remove it from the queue
        return message
    finally:
        receiver.close()
        connection.close()

class TestUsWaWsdotTrafficAmqpProducer:
    """Test cases for UsWaWsdotTrafficAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotTrafficAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotTrafficAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TrafficFlowStation.create_instance()

        producer = UsWaWsdotTrafficAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _flow_data_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.traffic.TrafficFlowStation"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{flow_data_id}".format(flow_data_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{flow_data_id}".format(flow_data_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_TrafficFlowStation.create_instance()

        producer = UsWaWsdotTrafficAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _flow_data_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.traffic.TrafficFlowStation'
        assert received.body is not None
        assert received.subject == "{flow_data_id}".format(flow_data_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{flow_data_id}".format(flow_data_id="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TrafficFlowReading.create_instance()

        producer = UsWaWsdotTrafficAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _flow_data_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.traffic.TrafficFlowReading"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{flow_data_id}".format(flow_data_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{flow_data_id}".format(flow_data_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_TrafficFlowReading.create_instance()

        producer = UsWaWsdotTrafficAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _flow_data_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.traffic.TrafficFlowReading'
        assert received.body is not None
        assert received.subject == "{flow_data_id}".format(flow_data_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{flow_data_id}".format(flow_data_id="value"))[:128]



class TestUsWaWsdotTraveltimesAmqpProducer:
    """Test cases for UsWaWsdotTraveltimesAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotTraveltimesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotTraveltimesAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TravelTimeRoute.create_instance()

        producer = UsWaWsdotTraveltimesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _travel_time_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.traveltimes.TravelTimeRoute"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{travel_time_id}".format(travel_time_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{travel_time_id}".format(travel_time_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_TravelTimeRoute.create_instance()

        producer = UsWaWsdotTraveltimesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _travel_time_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.traveltimes.TravelTimeRoute'
        assert received.body is not None
        assert received.subject == "{travel_time_id}".format(travel_time_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{travel_time_id}".format(travel_time_id="value"))[:128]



class TestUsWaWsdotMountainpassAmqpProducer:
    """Test cases for UsWaWsdotMountainpassAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotMountainpassAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotMountainpassAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_MountainPassCondition.create_instance()

        producer = UsWaWsdotMountainpassAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _mountain_pass_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.mountainpass.MountainPassCondition"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{mountain_pass_id}".format(mountain_pass_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{mountain_pass_id}".format(mountain_pass_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_MountainPassCondition.create_instance()

        producer = UsWaWsdotMountainpassAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _mountain_pass_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.mountainpass.MountainPassCondition'
        assert received.body is not None
        assert received.subject == "{mountain_pass_id}".format(mountain_pass_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{mountain_pass_id}".format(mountain_pass_id="value"))[:128]



class TestUsWaWsdotWeatherAmqpProducer:
    """Test cases for UsWaWsdotWeatherAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotWeatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotWeatherAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WeatherStation.create_instance()

        producer = UsWaWsdotWeatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _station_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.weather.WeatherStation"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_WeatherStation.create_instance()

        producer = UsWaWsdotWeatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _station_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.weather.WeatherStation'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WeatherReading.create_instance()

        producer = UsWaWsdotWeatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _station_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.weather.WeatherReading"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_WeatherReading.create_instance()

        producer = UsWaWsdotWeatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _station_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.weather.WeatherReading'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]



class TestUsWaWsdotTollsAmqpProducer:
    """Test cases for UsWaWsdotTollsAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotTollsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotTollsAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TollRate.create_instance()

        producer = UsWaWsdotTollsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _trip_name="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.tolls.TollRate"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{trip_name}".format(trip_name="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{trip_name}".format(trip_name="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_TollRate.create_instance()

        producer = UsWaWsdotTollsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _trip_name="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.tolls.TollRate'
        assert received.body is not None
        assert received.subject == "{trip_name}".format(trip_name="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{trip_name}".format(trip_name="value"))[:128]



class TestUsWaWsdotCvrestrictionsAmqpProducer:
    """Test cases for UsWaWsdotCvrestrictionsAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotCvrestrictionsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotCvrestrictionsAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_CommercialVehicleRestriction.create_instance()

        producer = UsWaWsdotCvrestrictionsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _state_route_id="value",
                    _bridge_number="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{state_route_id}/{bridge_number}".format(state_route_id="value", bridge_number="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{state_route_id}/{bridge_number}".format(state_route_id="value", bridge_number="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_CommercialVehicleRestriction.create_instance()

        producer = UsWaWsdotCvrestrictionsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _state_route_id="value",
                _bridge_number="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction'
        assert received.body is not None
        assert received.subject == "{state_route_id}/{bridge_number}".format(state_route_id="value", bridge_number="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{state_route_id}/{bridge_number}".format(state_route_id="value", bridge_number="value"))[:128]



class TestUsWaWsdotBorderAmqpProducer:
    """Test cases for UsWaWsdotBorderAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotBorderAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotBorderAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_BorderCrossing.create_instance()

        producer = UsWaWsdotBorderAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _crossing_name="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.border.BorderCrossing"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{crossing_name}".format(crossing_name="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{crossing_name}".format(crossing_name="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_BorderCrossing.create_instance()

        producer = UsWaWsdotBorderAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _crossing_name="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.border.BorderCrossing'
        assert received.body is not None
        assert received.subject == "{crossing_name}".format(crossing_name="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{crossing_name}".format(crossing_name="value"))[:128]



class TestUsWaWsdotFerriesAmqpProducer:
    """Test cases for UsWaWsdotFerriesAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotFerriesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotFerriesAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VesselLocation.create_instance()

        producer = UsWaWsdotFerriesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _vessel_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.ferries.VesselLocation"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{vessel_id}".format(vessel_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{vessel_id}".format(vessel_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_VesselLocation.create_instance()

        producer = UsWaWsdotFerriesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _vessel_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.ferries.VesselLocation'
        assert received.body is not None
        assert received.subject == "{vessel_id}".format(vessel_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{vessel_id}".format(vessel_id="value"))[:128]



class TestUsWaWsdotRoadweatherAmqpProducer:
    """Test cases for UsWaWsdotRoadweatherAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotRoadweatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotRoadweatherAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadWeatherStation.create_instance()

        producer = UsWaWsdotRoadweatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _station_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.roadweather.RoadWeatherStation"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_RoadWeatherStation.create_instance()

        producer = UsWaWsdotRoadweatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _station_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.roadweather.RoadWeatherStation'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadWeatherReading.create_instance()

        producer = UsWaWsdotRoadweatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _station_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.roadweather.RoadWeatherReading"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_RoadWeatherReading.create_instance()

        producer = UsWaWsdotRoadweatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _station_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.roadweather.RoadWeatherReading'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{station_id}".format(station_id="value"))[:128]



class TestUsWaWsdotAlertsAmqpProducer:
    """Test cases for UsWaWsdotAlertsAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotAlertsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotAlertsAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_HighwayAlert.create_instance()

        producer = UsWaWsdotAlertsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _alert_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.alerts.HighwayAlert"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{alert_id}".format(alert_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{alert_id}".format(alert_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_HighwayAlert.create_instance()

        producer = UsWaWsdotAlertsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _alert_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.alerts.HighwayAlert'
        assert received.body is not None
        assert received.subject == "{alert_id}".format(alert_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{alert_id}".format(alert_id="value"))[:128]



class TestUsWaWsdotCamerasAmqpProducer:
    """Test cases for UsWaWsdotCamerasAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotCamerasAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotCamerasAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_HighwayCamera.create_instance()

        producer = UsWaWsdotCamerasAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _camera_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.cameras.HighwayCamera"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{camera_id}".format(camera_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{camera_id}".format(camera_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_HighwayCamera.create_instance()

        producer = UsWaWsdotCamerasAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _camera_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.cameras.HighwayCamera'
        assert received.body is not None
        assert received.subject == "{camera_id}".format(camera_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{camera_id}".format(camera_id="value"))[:128]



class TestUsWaWsdotBridgeclearancesAmqpProducer:
    """Test cases for UsWaWsdotBridgeclearancesAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotBridgeclearancesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotBridgeclearancesAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_BridgeClearance.create_instance()

        producer = UsWaWsdotBridgeclearancesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _crossing_location_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.bridgeclearances.BridgeClearance"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{crossing_location_id}".format(crossing_location_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{crossing_location_id}".format(crossing_location_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_BridgeClearance.create_instance()

        producer = UsWaWsdotBridgeclearancesAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _crossing_location_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.bridgeclearances.BridgeClearance'
        assert received.body is not None
        assert received.subject == "{crossing_location_id}".format(crossing_location_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{crossing_location_id}".format(crossing_location_id="value"))[:128]



class TestUsWaWsdotFerryterminalsAmqpProducer:
    """Test cases for UsWaWsdotFerryterminalsAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UsWaWsdotFerryterminalsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"]
        )
        assert producer is not None
        assert producer.host == artemis_container["host"]
        assert producer.address == artemis_container["address"]
        assert producer.port == artemis_container["port"]
        assert producer.username == artemis_container["username"]
        producer.close()

    def test_presettled_send_waits_for_queued_delivery_to_drain(self):
        """Pre-settled sends must not return before queued deliveries are written."""

        class FakeTransport:
            def pending(self):
                return 0

        class FakeSender:
            def __init__(self):
                self.link = type("Link", (), {"queued": 1, "name": "fake-link"})()
                self.calls = []

            def send(self, amqp_msg, timeout=30.0):
                self.calls.append((amqp_msg, timeout))

        fake_sender = FakeSender()

        class FakeConnection:
            def __init__(self):
                self.conn = type("Conn", (), {"transport": FakeTransport()})()
                self.wait_calls = 0

            def wait(self, predicate, msg=None, timeout=None):
                self.wait_calls += 1
                assert not predicate()
                fake_sender.link.queued = 0
                assert predicate()

        fake_connection = FakeConnection()
        producer = object.__new__(UsWaWsdotFerryterminalsAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TerminalSailingSpace.create_instance()

        producer = UsWaWsdotFerryterminalsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='structured'
        )
        
        try:
            assert producer.host == artemis_container["host"]
            assert producer.address == artemis_container["address"]
            assert producer.port == artemis_container["port"]
            assert producer.username == artemis_container["username"]
            assert producer.content_mode == 'structured'
            # Send 5 messages to test proper message settlement and ordering
            for i in range(5):
                producer.send_amqp(
                    data=payload,
                    _feedurl="value",
                    _terminal_id="value",
                    _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}
                annotations = received.annotations or {}

                if True:
                    body = received.body
                    if isinstance(body, memoryview):
                        body_text = body.tobytes().decode('utf-8')
                    elif isinstance(body, bytes):
                        body_text = body.decode('utf-8')
                    elif isinstance(body, str):
                        body_text = body
                    elif isinstance(body, dict):
                        body_text = json.dumps(body)
                    else:
                        body_text = str(body)
                    cloud_event_payload = json.loads(body_text)
                    assert cloud_event_payload.get("type") == "us.wa.wsdot.ferryterminals.TerminalSailingSpace"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{terminal_id}".format(terminal_id="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{terminal_id}".format(terminal_id="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_TerminalSailingSpace.create_instance()

        producer = UsWaWsdotFerryterminalsAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_amqp(
                data=payload,
                _feedurl="value",
                _terminal_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'us.wa.wsdot.ferryterminals.TerminalSailingSpace'
        assert received.body is not None
        assert received.subject == "{terminal_id}".format(terminal_id="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{terminal_id}".format(terminal_id="value"))[:128]

