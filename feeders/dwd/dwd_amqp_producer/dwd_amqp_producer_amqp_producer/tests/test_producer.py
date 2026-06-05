
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for dwd_amqp_producer_amqp_producer
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dwd_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dwd_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dwd_amqp_producer_amqp_producer/src')))

from dwd_amqp_producer_amqp_producer import *
from dwd_amqp_producer_data import StationMetadata
from test_stationmetadata import Test_StationMetadata
from dwd_amqp_producer_data import AirTemperature10Min
from test_airtemperature10min import Test_AirTemperature10Min
from dwd_amqp_producer_data import Precipitation10Min
from test_precipitation10min import Test_Precipitation10Min
from dwd_amqp_producer_data import Wind10Min
from test_wind10min import Test_Wind10Min
from dwd_amqp_producer_data import Solar10Min
from test_solar10min import Test_Solar10Min
from dwd_amqp_producer_data import HourlyObservation
from test_hourlyobservation import Test_HourlyObservation
from dwd_amqp_producer_data import ExtremeWind10Min
from test_extremewind10min import Test_ExtremeWind10Min
from dwd_amqp_producer_data import ExtremeTemperature10Min
from test_extremetemperature10min import Test_ExtremeTemperature10Min
from dwd_amqp_producer_data import Alert
from test_alert import Test_Alert
from dwd_amqp_producer_data import RadarProductCatalog
from test_radarproductcatalog import Test_RadarProductCatalog
from dwd_amqp_producer_data import RadarFileProduct
from test_radarfileproduct import Test_RadarFileProduct
from dwd_amqp_producer_data import ForecastModelCatalog
from test_forecastmodelcatalog import Test_ForecastModelCatalog
from dwd_amqp_producer_data import IconD2ForecastFile
from test_icond2forecastfile import Test_IconD2ForecastFile



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

class TestDEDWDCDCAmqpProducer:
    """Test cases for DEDWDCDCAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = DEDWDCDCAmqpProducer(
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
        producer = object.__new__(DEDWDCDCAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_station_metadata(self, artemis_container):
        """Send and receive a StationMetadata message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_StationMetadata.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_station_metadata(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.StationMetadata"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_station_metadata_single_fresh_connection(self, artemis_container):
        """Send exactly one StationMetadata message on a fresh producer connection."""
        payload = Test_StationMetadata.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_station_metadata(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.StationMetadata'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")
    
    def test_send_air_temperature10_min(self, artemis_container):
        """Send and receive a AirTemperature10Min message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_AirTemperature10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_air_temperature10_min(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.AirTemperature10Min"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_air_temperature10_min_single_fresh_connection(self, artemis_container):
        """Send exactly one AirTemperature10Min message on a fresh producer connection."""
        payload = Test_AirTemperature10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_air_temperature10_min(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.AirTemperature10Min'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")
    
    def test_send_precipitation10_min(self, artemis_container):
        """Send and receive a Precipitation10Min message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Precipitation10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_precipitation10_min(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.Precipitation10Min"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_precipitation10_min_single_fresh_connection(self, artemis_container):
        """Send exactly one Precipitation10Min message on a fresh producer connection."""
        payload = Test_Precipitation10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_precipitation10_min(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.Precipitation10Min'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")
    
    def test_send_wind10_min(self, artemis_container):
        """Send and receive a Wind10Min message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Wind10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_wind10_min(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.Wind10Min"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_wind10_min_single_fresh_connection(self, artemis_container):
        """Send exactly one Wind10Min message on a fresh producer connection."""
        payload = Test_Wind10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_wind10_min(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.Wind10Min'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")
    
    def test_send_solar10_min(self, artemis_container):
        """Send and receive a Solar10Min message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Solar10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_solar10_min(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.Solar10Min"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_solar10_min_single_fresh_connection(self, artemis_container):
        """Send exactly one Solar10Min message on a fresh producer connection."""
        payload = Test_Solar10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_solar10_min(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.Solar10Min'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")
    
    def test_send_hourly_observation(self, artemis_container):
        """Send and receive a HourlyObservation message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_HourlyObservation.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_hourly_observation(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.HourlyObservation"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_hourly_observation_single_fresh_connection(self, artemis_container):
        """Send exactly one HourlyObservation message on a fresh producer connection."""
        payload = Test_HourlyObservation.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_hourly_observation(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.HourlyObservation'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")
    
    def test_send_extreme_wind10_min(self, artemis_container):
        """Send and receive a ExtremeWind10Min message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ExtremeWind10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_extreme_wind10_min(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.ExtremeWind10Min"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_extreme_wind10_min_single_fresh_connection(self, artemis_container):
        """Send exactly one ExtremeWind10Min message on a fresh producer connection."""
        payload = Test_ExtremeWind10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_extreme_wind10_min(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.ExtremeWind10Min'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")
    
    def test_send_extreme_temperature10_min(self, artemis_container):
        """Send and receive a ExtremeTemperature10Min message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ExtremeTemperature10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
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
                producer.send_extreme_temperature10_min(
                    data=payload,
                    _station_id="value",
                    _state="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.CDC.amqp.ExtremeTemperature10Min"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{station_id}".format(station_id="value")
                assert properties.get('state') == "{state}".format(state="value")
        finally:
            producer.close()

    def test_send_extreme_temperature10_min_single_fresh_connection(self, artemis_container):
        """Send exactly one ExtremeTemperature10Min message on a fresh producer connection."""
        payload = Test_ExtremeTemperature10Min.create_instance()

        producer = DEDWDCDCAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_extreme_temperature10_min(
                data=payload,
                _station_id="value",
                _state="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.CDC.amqp.ExtremeTemperature10Min'
        assert received.body is not None
        assert received.subject == "{station_id}".format(station_id="value")
        assert properties.get('state') == "{state}".format(state="value")



class TestDEDWDWeatherAmqpProducer:
    """Test cases for DEDWDWeatherAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = DEDWDWeatherAmqpProducer(
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
        producer = object.__new__(DEDWDWeatherAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_alert(self, artemis_container):
        """Send and receive a Alert message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Alert.create_instance()

        producer = DEDWDWeatherAmqpProducer(
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
                producer.send_alert(
                    data=payload,
                    _state="value",
                    _severity="value",
                    _identifier="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.Weather.amqp.Alert"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{state}/{severity}/{identifier}".format(state="value", severity="value", identifier="value")
        finally:
            producer.close()

    def test_send_alert_single_fresh_connection(self, artemis_container):
        """Send exactly one Alert message on a fresh producer connection."""
        payload = Test_Alert.create_instance()

        producer = DEDWDWeatherAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_alert(
                data=payload,
                _state="value",
                _severity="value",
                _identifier="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.Weather.amqp.Alert'
        assert received.body is not None
        assert received.subject == "{state}/{severity}/{identifier}".format(state="value", severity="value", identifier="value")



class TestDEDWDRadarAmqpProducer:
    """Test cases for DEDWDRadarAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = DEDWDRadarAmqpProducer(
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
        producer = object.__new__(DEDWDRadarAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_radar_product_catalog(self, artemis_container):
        """Send and receive a RadarProductCatalog message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RadarProductCatalog.create_instance()

        producer = DEDWDRadarAmqpProducer(
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
                producer.send_radar_product_catalog(
                    data=payload,
                    _kind="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.Radar.amqp.RadarProductCatalog"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{kind}".format(kind="value")
        finally:
            producer.close()

    def test_send_radar_product_catalog_single_fresh_connection(self, artemis_container):
        """Send exactly one RadarProductCatalog message on a fresh producer connection."""
        payload = Test_RadarProductCatalog.create_instance()

        producer = DEDWDRadarAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_radar_product_catalog(
                data=payload,
                _kind="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.Radar.amqp.RadarProductCatalog'
        assert received.body is not None
        assert received.subject == "{kind}".format(kind="value")
    
    def test_send_radar_file_product(self, artemis_container):
        """Send and receive a RadarFileProduct message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RadarFileProduct.create_instance()

        producer = DEDWDRadarAmqpProducer(
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
                producer.send_radar_file_product(
                    data=payload,
                    _product_type="value",
                    _file_id="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.Radar.amqp.RadarFileProduct"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{product_type}/{file_id}".format(product_type="value", file_id="value")
        finally:
            producer.close()

    def test_send_radar_file_product_single_fresh_connection(self, artemis_container):
        """Send exactly one RadarFileProduct message on a fresh producer connection."""
        payload = Test_RadarFileProduct.create_instance()

        producer = DEDWDRadarAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_radar_file_product(
                data=payload,
                _product_type="value",
                _file_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.Radar.amqp.RadarFileProduct'
        assert received.body is not None
        assert received.subject == "{product_type}/{file_id}".format(product_type="value", file_id="value")



class TestDEDWDForecastAmqpProducer:
    """Test cases for DEDWDForecastAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = DEDWDForecastAmqpProducer(
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
        producer = object.__new__(DEDWDForecastAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_forecast_model_catalog(self, artemis_container):
        """Send and receive a ForecastModelCatalog message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ForecastModelCatalog.create_instance()

        producer = DEDWDForecastAmqpProducer(
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
                producer.send_forecast_model_catalog(
                    data=payload,
                    _kind="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.Forecast.amqp.ForecastModelCatalog"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{kind}".format(kind="value")
        finally:
            producer.close()

    def test_send_forecast_model_catalog_single_fresh_connection(self, artemis_container):
        """Send exactly one ForecastModelCatalog message on a fresh producer connection."""
        payload = Test_ForecastModelCatalog.create_instance()

        producer = DEDWDForecastAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_forecast_model_catalog(
                data=payload,
                _kind="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.Forecast.amqp.ForecastModelCatalog'
        assert received.body is not None
        assert received.subject == "{kind}".format(kind="value")
    
    def test_send_icon_d2_forecast_file(self, artemis_container):
        """Send and receive a IconD2ForecastFile message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_IconD2ForecastFile.create_instance()

        producer = DEDWDForecastAmqpProducer(
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
                producer.send_icon_d2_forecast_file(
                    data=payload,
                    _variable="value",
                    _file_id="value",
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
                    assert cloud_event_payload.get("type") == "DE.DWD.Forecast.amqp.IconD2ForecastFile"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{variable}/{file_id}".format(variable="value", file_id="value")
        finally:
            producer.close()

    def test_send_icon_d2_forecast_file_single_fresh_connection(self, artemis_container):
        """Send exactly one IconD2ForecastFile message on a fresh producer connection."""
        payload = Test_IconD2ForecastFile.create_instance()

        producer = DEDWDForecastAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_icon_d2_forecast_file(
                data=payload,
                _variable="value",
                _file_id="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'DE.DWD.Forecast.amqp.IconD2ForecastFile'
        assert received.body is not None
        assert received.subject == "{variable}/{file_id}".format(variable="value", file_id="value")

