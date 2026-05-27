
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for elexon_bmrs_amqp_producer_amqp_producer
"""
import base64
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
from proton.utils import BlockingConnection

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../elexon_bmrs_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../elexon_bmrs_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../elexon_bmrs_amqp_producer_amqp_producer/src')))

from elexon_bmrs_amqp_producer_amqp_producer import *
from elexon_bmrs_amqp_producer_data import GenerationMix
from test_elexon_bmrs_amqp_producer_data_generationmix import Test_GenerationMix
from elexon_bmrs_amqp_producer_data import DemandOutturn
from test_elexon_bmrs_amqp_producer_data_demandoutturn import Test_DemandOutturn
from elexon_bmrs_amqp_producer_data import Info
from test_elexon_bmrs_amqp_producer_data_info import Test_Info



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

class TestUKCoElexonBMRSAmqpProducer:
    """Test cases for UKCoElexonBMRSAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = UKCoElexonBMRSAmqpProducer(
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
    
    def test_send_generation_mix(self, artemis_container):
        """Send and receive a GenerationMix message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_GenerationMix.create_instance()

        producer = UKCoElexonBMRSAmqpProducer(
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
                producer.send_generation_mix(
                    data=payload,
                    _settlement_period="value",
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}

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
                    assert cloud_event_payload.get("type") == "UK.Co.Elexon.BMRS.amqp.GenerationMix"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{settlement_period}".format(settlement_period="value")
        finally:
            producer.close()
    
    def test_send_demand_outturn(self, artemis_container):
        """Send and receive a DemandOutturn message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_DemandOutturn.create_instance()

        producer = UKCoElexonBMRSAmqpProducer(
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
                producer.send_demand_outturn(
                    data=payload,
                    _settlement_period="value",
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}

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
                    assert cloud_event_payload.get("type") == "UK.Co.Elexon.BMRS.amqp.DemandOutturn"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{settlement_period}".format(settlement_period="value")
        finally:
            producer.close()
    
    def test_send_info(self, artemis_container):
        """Send and receive a Info message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Info.create_instance()

        producer = UKCoElexonBMRSAmqpProducer(
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
                producer.send_info(
                    data=payload,
                    _settlement_period="value",
                    content_type="application/json"
                )

            # Receive and verify all 5 messages
            for i in range(5):
                received = _receive_single_message(artemis_container)
                properties = received.properties or {}

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
                    assert cloud_event_payload.get("type") == "UK.Co.Elexon.BMRS.amqp.Info"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{settlement_period}".format(settlement_period="value")
        finally:
            producer.close()

