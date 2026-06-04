
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for gtfs_amqp_producer_amqp_producer
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_amqp_producer_amqp_producer/src')))

from gtfs_amqp_producer_amqp_producer import *
from gtfs_amqp_producer_data import VehiclePosition
from test_gtfs_amqp_producer_data_vehicleposition import Test_VehiclePosition
from gtfs_amqp_producer_data import TripUpdate
from test_gtfs_amqp_producer_data_tripupdate import Test_TripUpdate
from gtfs_amqp_producer_data import Alert
from test_gtfs_amqp_producer_data_alert import Test_Alert
from gtfs_amqp_producer_data import Agency
from test_gtfs_amqp_producer_data_agency import Test_Agency
from gtfs_amqp_producer_data import Areas
from test_gtfs_amqp_producer_data_areas import Test_Areas
from gtfs_amqp_producer_data import Attributions
from test_gtfs_amqp_producer_data_attributions import Test_Attributions
from gtfs_amqp_producer_data import BookingRules
from test_gtfs_amqp_producer_data_bookingrules import Test_BookingRules
from gtfs_amqp_producer_data import FareAttributes
from test_gtfs_amqp_producer_data_fareattributes import Test_FareAttributes
from gtfs_amqp_producer_data import FareLegRules
from test_gtfs_amqp_producer_data_farelegrules import Test_FareLegRules
from gtfs_amqp_producer_data import FareMedia
from test_gtfs_amqp_producer_data_faremedia import Test_FareMedia
from gtfs_amqp_producer_data import FareProducts
from test_gtfs_amqp_producer_data_fareproducts import Test_FareProducts
from gtfs_amqp_producer_data import FareRules
from test_gtfs_amqp_producer_data_farerules import Test_FareRules
from gtfs_amqp_producer_data import FareTransferRules
from test_gtfs_amqp_producer_data_faretransferrules import Test_FareTransferRules
from gtfs_amqp_producer_data import FeedInfo
from test_gtfs_amqp_producer_data_feedinfo import Test_FeedInfo
from gtfs_amqp_producer_data import Frequencies
from test_gtfs_amqp_producer_data_frequencies import Test_Frequencies
from gtfs_amqp_producer_data import Levels
from test_gtfs_amqp_producer_data_levels import Test_Levels
from gtfs_amqp_producer_data import LocationGeoJson
from test_gtfs_amqp_producer_data_locationgeojson import Test_LocationGeoJson
from gtfs_amqp_producer_data import LocationGroups
from test_gtfs_amqp_producer_data_locationgroups import Test_LocationGroups
from gtfs_amqp_producer_data import LocationGroupStores
from test_gtfs_amqp_producer_data_locationgroupstores import Test_LocationGroupStores
from gtfs_amqp_producer_data import Networks
from test_gtfs_amqp_producer_data_networks import Test_Networks
from gtfs_amqp_producer_data import Pathways
from test_gtfs_amqp_producer_data_pathways import Test_Pathways
from gtfs_amqp_producer_data import RouteNetworks
from test_gtfs_amqp_producer_data_routenetworks import Test_RouteNetworks
from gtfs_amqp_producer_data import Routes
from test_gtfs_amqp_producer_data_routes import Test_Routes
from gtfs_amqp_producer_data import Shapes
from test_gtfs_amqp_producer_data_shapes import Test_Shapes
from gtfs_amqp_producer_data import StopAreas
from test_gtfs_amqp_producer_data_stopareas import Test_StopAreas
from gtfs_amqp_producer_data import Stops
from test_gtfs_amqp_producer_data_stops import Test_Stops
from gtfs_amqp_producer_data import StopTimes
from test_gtfs_amqp_producer_data_stoptimes import Test_StopTimes
from gtfs_amqp_producer_data import Timeframes
from test_gtfs_amqp_producer_data_timeframes import Test_Timeframes
from gtfs_amqp_producer_data import Transfers
from test_gtfs_amqp_producer_data_transfers import Test_Transfers
from gtfs_amqp_producer_data import Translations
from test_gtfs_amqp_producer_data_translations import Test_Translations
from gtfs_amqp_producer_data import Trips
from test_gtfs_amqp_producer_data_trips import Test_Trips



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

class TestGeneralTransitFeedRealTimeAmqpProducer:
    """Test cases for GeneralTransitFeedRealTimeAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = GeneralTransitFeedRealTimeAmqpProducer(
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
        producer = object.__new__(GeneralTransitFeedRealTimeAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_VehiclePosition.create_instance()

        producer = GeneralTransitFeedRealTimeAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedRealTime.Vehicle.VehiclePosition.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_VehiclePosition.create_instance()

        producer = GeneralTransitFeedRealTimeAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedRealTime.Vehicle.VehiclePosition.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TripUpdate.create_instance()

        producer = GeneralTransitFeedRealTimeAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedRealTime.Trip.TripUpdate.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_TripUpdate.create_instance()

        producer = GeneralTransitFeedRealTimeAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedRealTime.Trip.TripUpdate.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Alert.create_instance()

        producer = GeneralTransitFeedRealTimeAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedRealTime.Alert.Alert.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Alert.create_instance()

        producer = GeneralTransitFeedRealTimeAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedRealTime.Alert.Alert.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]



class TestGeneralTransitFeedStaticAmqpProducer:
    """Test cases for GeneralTransitFeedStaticAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = GeneralTransitFeedStaticAmqpProducer(
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
        producer = object.__new__(GeneralTransitFeedStaticAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Agency.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Agency.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Agency.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Agency.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Areas.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Areas.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Areas.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Areas.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Attributions.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Attributions.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Attributions.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Attributions.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_BookingRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeed.BookingRules.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_BookingRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeed.BookingRules.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FareAttributes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.FareAttributes.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_FareAttributes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.FareAttributes.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FareLegRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.FareLegRules.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_FareLegRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.FareLegRules.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FareMedia.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.FareMedia.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_FareMedia.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.FareMedia.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FareProducts.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.FareProducts.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_FareProducts.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.FareProducts.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FareRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.FareRules.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_FareRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.FareRules.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FareTransferRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.FareTransferRules.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_FareTransferRules.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.FareTransferRules.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FeedInfo.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.FeedInfo.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_FeedInfo.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.FeedInfo.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Frequencies.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Frequencies.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Frequencies.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Frequencies.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Levels.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Levels.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Levels.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Levels.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_LocationGeoJson.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.LocationGeoJson.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_LocationGeoJson.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.LocationGeoJson.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_LocationGroups.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.LocationGroups.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_LocationGroups.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.LocationGroups.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_LocationGroupStores.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.LocationGroupStores.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_LocationGroupStores.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.LocationGroupStores.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Networks.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Networks.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Networks.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Networks.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Pathways.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Pathways.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Pathways.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Pathways.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RouteNetworks.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.RouteNetworks.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_RouteNetworks.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.RouteNetworks.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Routes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Routes.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Routes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Routes.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Shapes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Shapes.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Shapes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Shapes.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_StopAreas.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.StopAreas.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_StopAreas.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.StopAreas.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Stops.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Stops.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Stops.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Stops.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_StopTimes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.StopTimes.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_StopTimes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.StopTimes.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Timeframes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Timeframes.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Timeframes.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Timeframes.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Transfers.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Transfers.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Transfers.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Transfers.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Translations.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Translations.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Translations.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Translations.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
    
    def test_send_amqp(self, artemis_container):
        """Send and receive a Amqp message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Trips.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                    _agencyid="value",
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
                    assert cloud_event_payload.get("type") == "GeneralTransitFeedStatic.Trips.amqp"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agencyid}".format(agencyid="value")
                assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]
        finally:
            producer.close()

    def test_send_amqp_single_fresh_connection(self, artemis_container):
        """Send exactly one Amqp message on a fresh producer connection."""
        payload = Test_Trips.create_instance()

        producer = GeneralTransitFeedStaticAmqpProducer(
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
                _agencyid="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'GeneralTransitFeedStatic.Trips.amqp'
        assert received.body is not None
        assert received.subject == "{agencyid}".format(agencyid="value")
        assert annotations.get(symbol('x-opt-partition-key')) == str("{agencyid}".format(agencyid="value"))[:128]

