
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for hsl_hfp_amqp_producer_amqp_producer
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hsl_hfp_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hsl_hfp_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hsl_hfp_amqp_producer_amqp_producer/src')))

from hsl_hfp_amqp_producer_amqp_producer import *
from hsl_hfp_amqp_producer_data import VehicleEvent
from test_vehicleevent import Test_VehicleEvent
from hsl_hfp_amqp_producer_data import TrafficLightEvent
from test_trafficlightevent import Test_TrafficLightEvent
from hsl_hfp_amqp_producer_data import DriverBlockEvent
from test_driverblockevent import Test_DriverBlockEvent
from hsl_hfp_amqp_producer_data import Operator
from test_operator import Test_Operator
from hsl_hfp_amqp_producer_data import Route
from test_route import Test_Route
from hsl_hfp_amqp_producer_data import Stop
from test_stop import Test_Stop



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

class TestFiHslHfpAmqpProducer:
    """Test cases for FiHslHfpAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = FiHslHfpAmqpProducer(
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
        producer = object.__new__(FiHslHfpAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_vp(self, artemis_container):
        """Send and receive a Vp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_vp(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.vp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "vp"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_vp_single_fresh_connection(self, artemis_container):
        """Send exactly one Vp message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_vp(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.vp'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "vp"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_due(self, artemis_container):
        """Send and receive a Due message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_due(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.due"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "due"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_due_single_fresh_connection(self, artemis_container):
        """Send exactly one Due message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_due(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.due'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "due"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_arr(self, artemis_container):
        """Send and receive a Arr message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_arr(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.arr"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "arr"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_arr_single_fresh_connection(self, artemis_container):
        """Send exactly one Arr message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_arr(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.arr'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "arr"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_dep(self, artemis_container):
        """Send and receive a Dep message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_dep(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.dep"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "dep"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_dep_single_fresh_connection(self, artemis_container):
        """Send exactly one Dep message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_dep(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.dep'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "dep"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_ars(self, artemis_container):
        """Send and receive a Ars message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_ars(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.ars"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "ars"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_ars_single_fresh_connection(self, artemis_container):
        """Send exactly one Ars message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_ars(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.ars'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "ars"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_pde(self, artemis_container):
        """Send and receive a Pde message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_pde(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.pde"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "pde"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_pde_single_fresh_connection(self, artemis_container):
        """Send exactly one Pde message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_pde(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.pde'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "pde"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_pas(self, artemis_container):
        """Send and receive a Pas message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_pas(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.pas"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "pas"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_pas_single_fresh_connection(self, artemis_container):
        """Send exactly one Pas message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_pas(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.pas'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "pas"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_wait(self, artemis_container):
        """Send and receive a Wait message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_wait(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.wait"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "wait"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_wait_single_fresh_connection(self, artemis_container):
        """Send exactly one Wait message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_wait(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.wait'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "wait"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_doo(self, artemis_container):
        """Send and receive a Doo message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_doo(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.doo"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "doo"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_doo_single_fresh_connection(self, artemis_container):
        """Send exactly one Doo message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_doo(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.doo'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "doo"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_doc(self, artemis_container):
        """Send and receive a Doc message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_doc(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.doc"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "doc"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_doc_single_fresh_connection(self, artemis_container):
        """Send exactly one Doc message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_doc(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.doc'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "doc"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_vja(self, artemis_container):
        """Send and receive a Vja message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_vja(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.vja"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "vja"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_vja_single_fresh_connection(self, artemis_container):
        """Send exactly one Vja message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_vja(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.vja'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "vja"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_vjout(self, artemis_container):
        """Send and receive a Vjout message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_vjout(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.vjout"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "vjout"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_vjout_single_fresh_connection(self, artemis_container):
        """Send exactly one Vjout message on a fresh producer connection."""
        payload = Test_VehicleEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_vjout(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.vjout'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "vjout"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_tlr(self, artemis_container):
        """Send and receive a Tlr message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TrafficLightEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_tlr(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.tlr"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "tlr"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_tlr_single_fresh_connection(self, artemis_container):
        """Send exactly one Tlr message on a fresh producer connection."""
        payload = Test_TrafficLightEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_tlr(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.tlr'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "tlr"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_tla(self, artemis_container):
        """Send and receive a Tla message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TrafficLightEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_tla(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.tla"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "tla"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_tla_single_fresh_connection(self, artemis_container):
        """Send exactly one Tla message on a fresh producer connection."""
        payload = Test_TrafficLightEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_tla(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.tla'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "tla"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_da(self, artemis_container):
        """Send and receive a Da message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_da(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.da"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "da"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_da_single_fresh_connection(self, artemis_container):
        """Send exactly one Da message on a fresh producer connection."""
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_da(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.da'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "da"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_dout(self, artemis_container):
        """Send and receive a Dout message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_dout(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.dout"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "dout"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_dout_single_fresh_connection(self, artemis_container):
        """Send exactly one Dout message on a fresh producer connection."""
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_dout(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.dout'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "dout"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_ba(self, artemis_container):
        """Send and receive a Ba message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_ba(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.ba"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "ba"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_ba_single_fresh_connection(self, artemis_container):
        """Send exactly one Ba message on a fresh producer connection."""
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_ba(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.ba'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "ba"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
    
    def test_send_bout(self, artemis_container):
        """Send and receive a Bout message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
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
                producer.send_bout(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
                    _vehicle_number="value",
                    _transport_mode="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.hfp.bout"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
                assert properties.get('event_type') == "bout"
                assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
                assert properties.get('route_id') == "{route_id}".format(route_id="value")
                assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
                assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")
        finally:
            producer.close()

    def test_send_bout_single_fresh_connection(self, artemis_container):
        """Send exactly one Bout message on a fresh producer connection."""
        payload = Test_DriverBlockEvent.create_instance()

        producer = FiHslHfpAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_bout(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _vehicle_number="value",
                _transport_mode="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.hfp.bout'
        assert received.body is not None
        assert received.subject == "{operator_id}/{vehicle_number}".format(operator_id="value", vehicle_number="value")
        assert properties.get('event_type') == "bout"
        assert properties.get('transport_mode') == "{transport_mode}".format(transport_mode="value")
        assert properties.get('route_id') == "{route_id}".format(route_id="value")
        assert properties.get('operator_id') == "{operator_id}".format(operator_id="value")
        assert properties.get('vehicle_number') == "{vehicle_number}".format(vehicle_number="value")



class TestFiHslGtfsOperatorAmqpProducer:
    """Test cases for FiHslGtfsOperatorAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = FiHslGtfsOperatorAmqpProducer(
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
        producer = object.__new__(FiHslGtfsOperatorAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_operator(self, artemis_container):
        """Send and receive a Operator message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Operator.create_instance()

        producer = FiHslGtfsOperatorAmqpProducer(
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
                producer.send_operator(
                    data=payload,
                    _feedurl="value",
                    _operator_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.gtfs.Operator"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "operator/{operator_id}".format(operator_id="value")
        finally:
            producer.close()

    def test_send_operator_single_fresh_connection(self, artemis_container):
        """Send exactly one Operator message on a fresh producer connection."""
        payload = Test_Operator.create_instance()

        producer = FiHslGtfsOperatorAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_operator(
                data=payload,
                _feedurl="value",
                _operator_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.gtfs.Operator'
        assert received.body is not None
        assert received.subject == "operator/{operator_id}".format(operator_id="value")



class TestFiHslGtfsRouteAmqpProducer:
    """Test cases for FiHslGtfsRouteAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = FiHslGtfsRouteAmqpProducer(
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
        producer = object.__new__(FiHslGtfsRouteAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_route(self, artemis_container):
        """Send and receive a Route message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Route.create_instance()

        producer = FiHslGtfsRouteAmqpProducer(
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
                producer.send_route(
                    data=payload,
                    _feedurl="value",
                    _route_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.gtfs.Route"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "route/{route_id}".format(route_id="value")
        finally:
            producer.close()

    def test_send_route_single_fresh_connection(self, artemis_container):
        """Send exactly one Route message on a fresh producer connection."""
        payload = Test_Route.create_instance()

        producer = FiHslGtfsRouteAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_route(
                data=payload,
                _feedurl="value",
                _route_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.gtfs.Route'
        assert received.body is not None
        assert received.subject == "route/{route_id}".format(route_id="value")



class TestFiHslGtfsStopAmqpProducer:
    """Test cases for FiHslGtfsStopAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = FiHslGtfsStopAmqpProducer(
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
        producer = object.__new__(FiHslGtfsStopAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_stop(self, artemis_container):
        """Send and receive a Stop message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Stop.create_instance()

        producer = FiHslGtfsStopAmqpProducer(
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
                producer.send_stop(
                    data=payload,
                    _feedurl="value",
                    _stop_id="value",
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
                    assert cloud_event_payload.get("type") == "fi.hsl.gtfs.Stop"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "stop/{stop_id}".format(stop_id="value")
        finally:
            producer.close()

    def test_send_stop_single_fresh_connection(self, artemis_container):
        """Send exactly one Stop message on a fresh producer connection."""
        payload = Test_Stop.create_instance()

        producer = FiHslGtfsStopAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_stop(
                data=payload,
                _feedurl="value",
                _stop_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'fi.hsl.gtfs.Stop'
        assert received.body is not None
        assert received.subject == "stop/{stop_id}".format(stop_id="value")

