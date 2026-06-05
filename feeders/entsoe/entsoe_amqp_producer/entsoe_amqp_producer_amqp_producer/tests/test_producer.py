
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for entsoe_amqp_producer_amqp_producer
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entsoe_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entsoe_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../entsoe_amqp_producer_amqp_producer/src')))

from entsoe_amqp_producer_amqp_producer import *
from entsoe_amqp_producer_data import DayAheadPrices
from test_dayaheadprices import Test_DayAheadPrices
from entsoe_amqp_producer_data import ActualTotalLoad
from test_actualtotalload import Test_ActualTotalLoad
from entsoe_amqp_producer_data import LoadForecastMargin
from test_loadforecastmargin import Test_LoadForecastMargin
from entsoe_amqp_producer_data import GenerationForecast
from test_generationforecast import Test_GenerationForecast
from entsoe_amqp_producer_data import ReservoirFillingInformation
from test_reservoirfillinginformation import Test_ReservoirFillingInformation
from entsoe_amqp_producer_data import ActualGeneration
from test_actualgeneration import Test_ActualGeneration
from entsoe_amqp_producer_data import ActualGenerationPerType
from test_actualgenerationpertype import Test_ActualGenerationPerType
from entsoe_amqp_producer_data import WindSolarForecast
from test_windsolarforecast import Test_WindSolarForecast
from entsoe_amqp_producer_data import WindSolarGeneration
from test_windsolargeneration import Test_WindSolarGeneration
from entsoe_amqp_producer_data import InstalledGenerationCapacityPerType
from test_installedgenerationcapacitypertype import Test_InstalledGenerationCapacityPerType
from entsoe_amqp_producer_data import CrossBorderPhysicalFlows
from test_crossborderphysicalflows import Test_CrossBorderPhysicalFlows



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

class TestEuEntsoeTransparencyByDomainAmqpProducer:
    """Test cases for EuEntsoeTransparencyByDomainAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = EuEntsoeTransparencyByDomainAmqpProducer(
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
        producer = object.__new__(EuEntsoeTransparencyByDomainAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_day_ahead_prices(self, artemis_container):
        """Send and receive a DayAheadPrices message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_DayAheadPrices.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
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
                producer.send_day_ahead_prices(
                    data=payload,
                    _in_domain="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}".format(inDomain="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('event-type') == "DayAheadPrices"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
        finally:
            producer.close()

    def test_send_day_ahead_prices_single_fresh_connection(self, artemis_container):
        """Send exactly one DayAheadPrices message on a fresh producer connection."""
        payload = Test_DayAheadPrices.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_day_ahead_prices(
                data=payload,
                _in_domain="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices'
        assert received.body is not None
        assert received.subject == "{inDomain}".format(inDomain="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('event-type') == "DayAheadPrices"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
    
    def test_send_actual_total_load(self, artemis_container):
        """Send and receive a ActualTotalLoad message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ActualTotalLoad.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
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
                producer.send_actual_total_load(
                    data=payload,
                    _in_domain="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}".format(inDomain="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('event-type') == "ActualTotalLoad"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
        finally:
            producer.close()

    def test_send_actual_total_load_single_fresh_connection(self, artemis_container):
        """Send exactly one ActualTotalLoad message on a fresh producer connection."""
        payload = Test_ActualTotalLoad.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_actual_total_load(
                data=payload,
                _in_domain="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad'
        assert received.body is not None
        assert received.subject == "{inDomain}".format(inDomain="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('event-type') == "ActualTotalLoad"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
    
    def test_send_load_forecast_margin(self, artemis_container):
        """Send and receive a LoadForecastMargin message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_LoadForecastMargin.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
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
                producer.send_load_forecast_margin(
                    data=payload,
                    _in_domain="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}".format(inDomain="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('event-type') == "LoadForecastMargin"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
        finally:
            producer.close()

    def test_send_load_forecast_margin_single_fresh_connection(self, artemis_container):
        """Send exactly one LoadForecastMargin message on a fresh producer connection."""
        payload = Test_LoadForecastMargin.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_load_forecast_margin(
                data=payload,
                _in_domain="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin'
        assert received.body is not None
        assert received.subject == "{inDomain}".format(inDomain="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('event-type') == "LoadForecastMargin"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
    
    def test_send_generation_forecast(self, artemis_container):
        """Send and receive a GenerationForecast message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_GenerationForecast.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
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
                producer.send_generation_forecast(
                    data=payload,
                    _in_domain="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomain.amqp.GenerationForecast"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}".format(inDomain="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('event-type') == "GenerationForecast"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
        finally:
            producer.close()

    def test_send_generation_forecast_single_fresh_connection(self, artemis_container):
        """Send exactly one GenerationForecast message on a fresh producer connection."""
        payload = Test_GenerationForecast.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_generation_forecast(
                data=payload,
                _in_domain="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomain.amqp.GenerationForecast'
        assert received.body is not None
        assert received.subject == "{inDomain}".format(inDomain="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('event-type') == "GenerationForecast"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
    
    def test_send_reservoir_filling_information(self, artemis_container):
        """Send and receive a ReservoirFillingInformation message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ReservoirFillingInformation.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
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
                producer.send_reservoir_filling_information(
                    data=payload,
                    _in_domain="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}".format(inDomain="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('event-type') == "ReservoirFillingInformation"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
        finally:
            producer.close()

    def test_send_reservoir_filling_information_single_fresh_connection(self, artemis_container):
        """Send exactly one ReservoirFillingInformation message on a fresh producer connection."""
        payload = Test_ReservoirFillingInformation.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_reservoir_filling_information(
                data=payload,
                _in_domain="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation'
        assert received.body is not None
        assert received.subject == "{inDomain}".format(inDomain="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('event-type') == "ReservoirFillingInformation"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
    
    def test_send_actual_generation(self, artemis_container):
        """Send and receive a ActualGeneration message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ActualGeneration.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
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
                producer.send_actual_generation(
                    data=payload,
                    _in_domain="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomain.amqp.ActualGeneration"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}".format(inDomain="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('event-type') == "ActualGeneration"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]
        finally:
            producer.close()

    def test_send_actual_generation_single_fresh_connection(self, artemis_container):
        """Send exactly one ActualGeneration message on a fresh producer connection."""
        payload = Test_ActualGeneration.create_instance()

        producer = EuEntsoeTransparencyByDomainAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_actual_generation(
                data=payload,
                _in_domain="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomain.amqp.ActualGeneration'
        assert received.body is not None
        assert received.subject == "{inDomain}".format(inDomain="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('event-type') == "ActualGeneration"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}".format(inDomain="value"))[:128]



class TestEuEntsoeTransparencyByDomainPsrTypeAmqpProducer:
    """Test cases for EuEntsoeTransparencyByDomainPsrTypeAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
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
        producer = object.__new__(EuEntsoeTransparencyByDomainPsrTypeAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_actual_generation_per_type(self, artemis_container):
        """Send and receive a ActualGenerationPerType message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ActualGenerationPerType.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
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
                producer.send_actual_generation_per_type(
                    data=payload,
                    _in_domain="value",
                    _psr_type="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('psr-type') == "{psrType}".format(psrType="value")
                assert properties.get('event-type') == "ActualGenerationPerType"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]
        finally:
            producer.close()

    def test_send_actual_generation_per_type_single_fresh_connection(self, artemis_container):
        """Send exactly one ActualGenerationPerType message on a fresh producer connection."""
        payload = Test_ActualGenerationPerType.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_actual_generation_per_type(
                data=payload,
                _in_domain="value",
                _psr_type="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType'
        assert received.body is not None
        assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('psr-type') == "{psrType}".format(psrType="value")
        assert properties.get('event-type') == "ActualGenerationPerType"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]
    
    def test_send_wind_solar_forecast(self, artemis_container):
        """Send and receive a WindSolarForecast message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WindSolarForecast.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
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
                producer.send_wind_solar_forecast(
                    data=payload,
                    _in_domain="value",
                    _psr_type="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('psr-type') == "{psrType}".format(psrType="value")
                assert properties.get('event-type') == "WindSolarForecast"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]
        finally:
            producer.close()

    def test_send_wind_solar_forecast_single_fresh_connection(self, artemis_container):
        """Send exactly one WindSolarForecast message on a fresh producer connection."""
        payload = Test_WindSolarForecast.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_wind_solar_forecast(
                data=payload,
                _in_domain="value",
                _psr_type="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast'
        assert received.body is not None
        assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('psr-type') == "{psrType}".format(psrType="value")
        assert properties.get('event-type') == "WindSolarForecast"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]
    
    def test_send_wind_solar_generation(self, artemis_container):
        """Send and receive a WindSolarGeneration message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WindSolarGeneration.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
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
                producer.send_wind_solar_generation(
                    data=payload,
                    _in_domain="value",
                    _psr_type="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('psr-type') == "{psrType}".format(psrType="value")
                assert properties.get('event-type') == "WindSolarGeneration"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]
        finally:
            producer.close()

    def test_send_wind_solar_generation_single_fresh_connection(self, artemis_container):
        """Send exactly one WindSolarGeneration message on a fresh producer connection."""
        payload = Test_WindSolarGeneration.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_wind_solar_generation(
                data=payload,
                _in_domain="value",
                _psr_type="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration'
        assert received.body is not None
        assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('psr-type') == "{psrType}".format(psrType="value")
        assert properties.get('event-type') == "WindSolarGeneration"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]
    
    def test_send_installed_generation_capacity_per_type(self, artemis_container):
        """Send and receive a InstalledGenerationCapacityPerType message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_InstalledGenerationCapacityPerType.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
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
                producer.send_installed_generation_capacity_per_type(
                    data=payload,
                    _in_domain="value",
                    _psr_type="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('psr-type') == "{psrType}".format(psrType="value")
                assert properties.get('event-type') == "InstalledGenerationCapacityPerType"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]
        finally:
            producer.close()

    def test_send_installed_generation_capacity_per_type_single_fresh_connection(self, artemis_container):
        """Send exactly one InstalledGenerationCapacityPerType message on a fresh producer connection."""
        payload = Test_InstalledGenerationCapacityPerType.create_instance()

        producer = EuEntsoeTransparencyByDomainPsrTypeAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_installed_generation_capacity_per_type(
                data=payload,
                _in_domain="value",
                _psr_type="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType'
        assert received.body is not None
        assert received.subject == "{inDomain}/{psrType}".format(inDomain="value", psrType="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('psr-type') == "{psrType}".format(psrType="value")
        assert properties.get('event-type') == "InstalledGenerationCapacityPerType"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{psrType}".format(inDomain="value", psrType="value"))[:128]



class TestEuEntsoeTransparencyCrossBorderAmqpProducer:
    """Test cases for EuEntsoeTransparencyCrossBorderAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = EuEntsoeTransparencyCrossBorderAmqpProducer(
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
        producer = object.__new__(EuEntsoeTransparencyCrossBorderAmqpProducer)
        producer._sender = fake_sender
        producer._connection = fake_connection
        producer._blocking_sender_is_presettled = True

        producer._send_via_blocking_sender(Message(body=b"payload", inferred=True), timeout=7.5)

        assert len(fake_sender.calls) == 1
        assert fake_connection.wait_calls == 1
    
    def test_send_cross_border_physical_flows(self, artemis_container):
        """Send and receive a CrossBorderPhysicalFlows message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_CrossBorderPhysicalFlows.create_instance()

        producer = EuEntsoeTransparencyCrossBorderAmqpProducer(
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
                producer.send_cross_border_physical_flows(
                    data=payload,
                    _in_domain="value",
                    _out_domain="value",
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
                    assert cloud_event_payload.get("type") == "eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{inDomain}/{outDomain}".format(inDomain="value", outDomain="value")
                assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
                assert properties.get('out-domain') == "{outDomain}".format(outDomain="value")
                assert properties.get('event-type') == "CrossBorderPhysicalFlows"
                assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{outDomain}".format(inDomain="value", outDomain="value"))[:128]
        finally:
            producer.close()

    def test_send_cross_border_physical_flows_single_fresh_connection(self, artemis_container):
        """Send exactly one CrossBorderPhysicalFlows message on a fresh producer connection."""
        payload = Test_CrossBorderPhysicalFlows.create_instance()

        producer = EuEntsoeTransparencyCrossBorderAmqpProducer(
            host=artemis_container["host"],
            address=artemis_container["address"],
            port=artemis_container["port"],
            username=artemis_container["username"],
            password=artemis_container["password"],
            content_mode='binary'
        )

        try:
            producer.send_cross_border_physical_flows(
                data=payload,
                _in_domain="value",
                _out_domain="value",
                _time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                content_type="application/json"
            )
        finally:
            producer.close()

        received = _receive_single_message(artemis_container)
        properties = received.properties or {}
        annotations = received.annotations or {}
        assert properties.get('cloudEvents:type') == 'eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows'
        assert received.body is not None
        assert received.subject == "{inDomain}/{outDomain}".format(inDomain="value", outDomain="value")
        assert properties.get('in-domain') == "{inDomain}".format(inDomain="value")
        assert properties.get('out-domain') == "{outDomain}".format(outDomain="value")
        assert properties.get('event-type') == "CrossBorderPhysicalFlows"
        assert annotations.get(symbol('x-opt-partition-key')) == str("{inDomain}/{outDomain}".format(inDomain="value", outDomain="value"))[:128]

