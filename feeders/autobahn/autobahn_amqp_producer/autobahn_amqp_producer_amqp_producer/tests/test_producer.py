
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for autobahn_amqp_producer_amqp_producer
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_amqp_producer_amqp_producer/src')))

from autobahn_amqp_producer_amqp_producer import *
from autobahn_amqp_producer_data import RoadEvent
from test_roadevent import Test_RoadEvent
from autobahn_amqp_producer_data import WarningEvent
from test_warningevent import Test_WarningEvent
from autobahn_amqp_producer_data import Webcam
from test_webcam import Test_Webcam
from autobahn_amqp_producer_data import ParkingLorry
from test_parkinglorry import Test_ParkingLorry
from autobahn_amqp_producer_data import ChargingStation
from test_chargingstation import Test_ChargingStation



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

class TestDEAutobahnAmqpProducer:
    """Test cases for DEAutobahnAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = DEAutobahnAmqpProducer(
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
        producer = object.__new__(DEAutobahnAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_roadwork_appeared(self, artemis_container):
        """Send and receive a RoadworkAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_roadwork_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.RoadworkAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_roadwork_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one RoadworkAppeared message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_roadwork_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.RoadworkAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_roadwork_updated(self, artemis_container):
        """Send and receive a RoadworkUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_roadwork_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.RoadworkUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_roadwork_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one RoadworkUpdated message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_roadwork_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.RoadworkUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_roadwork_resolved(self, artemis_container):
        """Send and receive a RoadworkResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_roadwork_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.RoadworkResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_roadwork_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one RoadworkResolved message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_roadwork_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.RoadworkResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_short_term_roadwork_appeared(self, artemis_container):
        """Send and receive a ShortTermRoadworkAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_short_term_roadwork_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ShortTermRoadworkAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_short_term_roadwork_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one ShortTermRoadworkAppeared message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_short_term_roadwork_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ShortTermRoadworkAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_short_term_roadwork_updated(self, artemis_container):
        """Send and receive a ShortTermRoadworkUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_short_term_roadwork_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ShortTermRoadworkUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_short_term_roadwork_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one ShortTermRoadworkUpdated message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_short_term_roadwork_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ShortTermRoadworkUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_short_term_roadwork_resolved(self, artemis_container):
        """Send and receive a ShortTermRoadworkResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_short_term_roadwork_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ShortTermRoadworkResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_short_term_roadwork_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one ShortTermRoadworkResolved message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_short_term_roadwork_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ShortTermRoadworkResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_closure_appeared(self, artemis_container):
        """Send and receive a ClosureAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_closure_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ClosureAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_closure_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one ClosureAppeared message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_closure_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ClosureAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_closure_updated(self, artemis_container):
        """Send and receive a ClosureUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_closure_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ClosureUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_closure_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one ClosureUpdated message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_closure_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ClosureUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_closure_resolved(self, artemis_container):
        """Send and receive a ClosureResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_closure_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ClosureResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_closure_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one ClosureResolved message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_closure_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ClosureResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_entry_exit_closure_appeared(self, artemis_container):
        """Send and receive a EntryExitClosureAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_entry_exit_closure_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.EntryExitClosureAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_entry_exit_closure_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one EntryExitClosureAppeared message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_entry_exit_closure_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.EntryExitClosureAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_entry_exit_closure_updated(self, artemis_container):
        """Send and receive a EntryExitClosureUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_entry_exit_closure_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.EntryExitClosureUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_entry_exit_closure_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one EntryExitClosureUpdated message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_entry_exit_closure_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.EntryExitClosureUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_entry_exit_closure_resolved(self, artemis_container):
        """Send and receive a EntryExitClosureResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_entry_exit_closure_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.EntryExitClosureResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_entry_exit_closure_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one EntryExitClosureResolved message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_entry_exit_closure_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.EntryExitClosureResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_warning_appeared(self, artemis_container):
        """Send and receive a WarningAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WarningEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_warning_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WarningAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_warning_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one WarningAppeared message on a fresh producer connection."""
        payload = Test_WarningEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_warning_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WarningAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_warning_updated(self, artemis_container):
        """Send and receive a WarningUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WarningEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_warning_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WarningUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_warning_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one WarningUpdated message on a fresh producer connection."""
        payload = Test_WarningEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_warning_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WarningUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_warning_resolved(self, artemis_container):
        """Send and receive a WarningResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WarningEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_warning_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WarningResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_warning_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one WarningResolved message on a fresh producer connection."""
        payload = Test_WarningEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_warning_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WarningResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_weight_limit35_restriction_appeared(self, artemis_container):
        """Send and receive a WeightLimit35RestrictionAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_weight_limit35_restriction_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WeightLimit35RestrictionAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_weight_limit35_restriction_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one WeightLimit35RestrictionAppeared message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_weight_limit35_restriction_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WeightLimit35RestrictionAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_weight_limit35_restriction_updated(self, artemis_container):
        """Send and receive a WeightLimit35RestrictionUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_weight_limit35_restriction_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WeightLimit35RestrictionUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_weight_limit35_restriction_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one WeightLimit35RestrictionUpdated message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_weight_limit35_restriction_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WeightLimit35RestrictionUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_weight_limit35_restriction_resolved(self, artemis_container):
        """Send and receive a WeightLimit35RestrictionResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_weight_limit35_restriction_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WeightLimit35RestrictionResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_weight_limit35_restriction_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one WeightLimit35RestrictionResolved message on a fresh producer connection."""
        payload = Test_RoadEvent.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_weight_limit35_restriction_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WeightLimit35RestrictionResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_webcam_appeared(self, artemis_container):
        """Send and receive a WebcamAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Webcam.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_webcam_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WebcamAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_webcam_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one WebcamAppeared message on a fresh producer connection."""
        payload = Test_Webcam.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_webcam_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WebcamAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_webcam_updated(self, artemis_container):
        """Send and receive a WebcamUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Webcam.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_webcam_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WebcamUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_webcam_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one WebcamUpdated message on a fresh producer connection."""
        payload = Test_Webcam.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_webcam_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WebcamUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_webcam_resolved(self, artemis_container):
        """Send and receive a WebcamResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Webcam.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_webcam_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.WebcamResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_webcam_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one WebcamResolved message on a fresh producer connection."""
        payload = Test_Webcam.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_webcam_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.WebcamResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_parking_lorry_appeared(self, artemis_container):
        """Send and receive a ParkingLorryAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ParkingLorry.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_parking_lorry_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ParkingLorryAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_parking_lorry_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one ParkingLorryAppeared message on a fresh producer connection."""
        payload = Test_ParkingLorry.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_parking_lorry_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ParkingLorryAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_parking_lorry_updated(self, artemis_container):
        """Send and receive a ParkingLorryUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ParkingLorry.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_parking_lorry_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ParkingLorryUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_parking_lorry_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one ParkingLorryUpdated message on a fresh producer connection."""
        payload = Test_ParkingLorry.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_parking_lorry_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ParkingLorryUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_parking_lorry_resolved(self, artemis_container):
        """Send and receive a ParkingLorryResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ParkingLorry.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_parking_lorry_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ParkingLorryResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_parking_lorry_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one ParkingLorryResolved message on a fresh producer connection."""
        payload = Test_ParkingLorry.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_parking_lorry_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ParkingLorryResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_electric_charging_station_appeared(self, artemis_container):
        """Send and receive a ElectricChargingStationAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_electric_charging_station_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ElectricChargingStationAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_electric_charging_station_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one ElectricChargingStationAppeared message on a fresh producer connection."""
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_electric_charging_station_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ElectricChargingStationAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_electric_charging_station_updated(self, artemis_container):
        """Send and receive a ElectricChargingStationUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_electric_charging_station_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ElectricChargingStationUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_electric_charging_station_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one ElectricChargingStationUpdated message on a fresh producer connection."""
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_electric_charging_station_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ElectricChargingStationUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_electric_charging_station_resolved(self, artemis_container):
        """Send and receive a ElectricChargingStationResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_electric_charging_station_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.ElectricChargingStationResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_electric_charging_station_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one ElectricChargingStationResolved message on a fresh producer connection."""
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_electric_charging_station_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.ElectricChargingStationResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_strong_electric_charging_station_appeared(self, artemis_container):
        """Send and receive a StrongElectricChargingStationAppeared message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_strong_electric_charging_station_appeared(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.StrongElectricChargingStationAppeared"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_strong_electric_charging_station_appeared_single_fresh_connection(self, artemis_container):
        """Send exactly one StrongElectricChargingStationAppeared message on a fresh producer connection."""
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_strong_electric_charging_station_appeared(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.StrongElectricChargingStationAppeared'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_strong_electric_charging_station_updated(self, artemis_container):
        """Send and receive a StrongElectricChargingStationUpdated message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_strong_electric_charging_station_updated(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.StrongElectricChargingStationUpdated"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_strong_electric_charging_station_updated_single_fresh_connection(self, artemis_container):
        """Send exactly one StrongElectricChargingStationUpdated message on a fresh producer connection."""
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_strong_electric_charging_station_updated(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.StrongElectricChargingStationUpdated'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
    
    def test_send_strong_electric_charging_station_resolved(self, artemis_container):
        """Send and receive a StrongElectricChargingStationResolved message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
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
                producer.send_strong_electric_charging_station_resolved(
                    data=payload,
                    _identifier="value",
                    _road="value",
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
                    assert cloud_event_payload.get("type") == "DE.Autobahn.amqp.StrongElectricChargingStationResolved"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{identifier}".format(identifier="value")
                assert properties.get('road') == "{road}".format(road="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]
        finally:
            producer.close()

    def test_send_strong_electric_charging_station_resolved_single_fresh_connection(self, artemis_container):
        """Send exactly one StrongElectricChargingStationResolved message on a fresh producer connection."""
        payload = Test_ChargingStation.create_instance()

        producer = DEAutobahnAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_strong_electric_charging_station_resolved(
                data=payload,
                _identifier="value",
                _road="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.Autobahn.amqp.StrongElectricChargingStationResolved'
        assert received.body is not None
        assert received.subject == "{identifier}".format(identifier="value")
        assert properties.get('road') == "{road}".format(road="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{identifier}".format(identifier="value"))[:128]

