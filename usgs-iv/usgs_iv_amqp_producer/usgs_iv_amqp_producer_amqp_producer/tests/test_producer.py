
# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, missing-class-docstring

"""
Tests for usgs_iv_amqp_producer_amqp_producer
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_amqp_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_amqp_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_amqp_producer_amqp_producer/src')))

from usgs_iv_amqp_producer_amqp_producer import *
from usgs_iv_amqp_producer_data import Site
from test_usgs_iv_amqp_producer_data_site import Test_Site
from usgs_iv_amqp_producer_data import SiteTimeseries
from test_usgs_iv_amqp_producer_data_sitetimeseries import Test_SiteTimeseries
from usgs_iv_amqp_producer_data import OtherParameter
from test_usgs_iv_amqp_producer_data_otherparameter import Test_OtherParameter
from usgs_iv_amqp_producer_data import Precipitation
from test_usgs_iv_amqp_producer_data_precipitation import Test_Precipitation
from usgs_iv_amqp_producer_data import Streamflow
from test_usgs_iv_amqp_producer_data_streamflow import Test_Streamflow
from usgs_iv_amqp_producer_data import GageHeight
from test_usgs_iv_amqp_producer_data_gageheight import Test_GageHeight
from usgs_iv_amqp_producer_data import WaterTemperature
from test_usgs_iv_amqp_producer_data_watertemperature import Test_WaterTemperature
from usgs_iv_amqp_producer_data import DissolvedOxygen
from test_usgs_iv_amqp_producer_data_dissolvedoxygen import Test_DissolvedOxygen
from usgs_iv_amqp_producer_data import PH
from test_usgs_iv_amqp_producer_data_ph import Test_PH
from usgs_iv_amqp_producer_data import SpecificConductance
from test_usgs_iv_amqp_producer_data_specificconductance import Test_SpecificConductance
from usgs_iv_amqp_producer_data import Turbidity
from test_usgs_iv_amqp_producer_data_turbidity import Test_Turbidity
from usgs_iv_amqp_producer_data import AirTemperature
from test_usgs_iv_amqp_producer_data_airtemperature import Test_AirTemperature
from usgs_iv_amqp_producer_data import WindSpeed
from test_usgs_iv_amqp_producer_data_windspeed import Test_WindSpeed
from usgs_iv_amqp_producer_data import WindDirection
from test_usgs_iv_amqp_producer_data_winddirection import Test_WindDirection
from usgs_iv_amqp_producer_data import RelativeHumidity
from test_usgs_iv_amqp_producer_data_relativehumidity import Test_RelativeHumidity
from usgs_iv_amqp_producer_data import BarometricPressure
from test_usgs_iv_amqp_producer_data_barometricpressure import Test_BarometricPressure
from usgs_iv_amqp_producer_data import TurbidityFNU
from test_usgs_iv_amqp_producer_data_turbidityfnu import Test_TurbidityFNU
from usgs_iv_amqp_producer_data import FDOM
from test_usgs_iv_amqp_producer_data_fdom import Test_FDOM
from usgs_iv_amqp_producer_data import ReservoirStorage
from test_usgs_iv_amqp_producer_data_reservoirstorage import Test_ReservoirStorage
from usgs_iv_amqp_producer_data import LakeElevationNGVD29
from test_usgs_iv_amqp_producer_data_lakeelevationngvd29 import Test_LakeElevationNGVD29
from usgs_iv_amqp_producer_data import WaterDepth
from test_usgs_iv_amqp_producer_data_waterdepth import Test_WaterDepth
from usgs_iv_amqp_producer_data import EquipmentStatus
from test_usgs_iv_amqp_producer_data_equipmentstatus import Test_EquipmentStatus
from usgs_iv_amqp_producer_data import TidallyFilteredDischarge
from test_usgs_iv_amqp_producer_data_tidallyfiltereddischarge import Test_TidallyFilteredDischarge
from usgs_iv_amqp_producer_data import WaterVelocity
from test_usgs_iv_amqp_producer_data_watervelocity import Test_WaterVelocity
from usgs_iv_amqp_producer_data import EstuaryElevationNGVD29
from test_usgs_iv_amqp_producer_data_estuaryelevationngvd29 import Test_EstuaryElevationNGVD29
from usgs_iv_amqp_producer_data import LakeElevationNAVD88
from test_usgs_iv_amqp_producer_data_lakeelevationnavd88 import Test_LakeElevationNAVD88
from usgs_iv_amqp_producer_data import Salinity
from test_usgs_iv_amqp_producer_data_salinity import Test_Salinity
from usgs_iv_amqp_producer_data import GateOpening
from test_usgs_iv_amqp_producer_data_gateopening import Test_GateOpening



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

class TestUSGSSitesAmqpProducer:
    """Test cases for USGSSitesAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = USGSSitesAmqpProducer(
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
    
    def test_send_site(self, artemis_container):
        """Send and receive a Site message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Site.create_instance()

        producer = USGSSitesAmqpProducer(
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
                producer.send_site(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
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
                    assert cloud_event_payload.get("type") == "USGS.Sites.amqp.Site"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}".format(agency_cd="value", site_no="value")
        finally:
            producer.close()



class TestUSGSSiteTimeseriesAmqpProducer:
    """Test cases for USGSSiteTimeseriesAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = USGSSiteTimeseriesAmqpProducer(
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
    
    def test_send_site_timeseries(self, artemis_container):
        """Send and receive a SiteTimeseries message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_SiteTimeseries.create_instance()

        producer = USGSSiteTimeseriesAmqpProducer(
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
                producer.send_site_timeseries(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
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
                    assert cloud_event_payload.get("type") == "USGS.SiteTimeseries.amqp.SiteTimeseries"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()



class TestUSGSInstantaneousValuesAmqpProducer:
    """Test cases for USGSInstantaneousValuesAmqpProducer"""
    
    def test_producer_initialization(self, artemis_container):
        """Test that producer initializes correctly"""
        producer = USGSInstantaneousValuesAmqpProducer(
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
    
    def test_send_other_parameter(self, artemis_container):
        """Send and receive a OtherParameter message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_OtherParameter.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_other_parameter(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.OtherParameter"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_precipitation(self, artemis_container):
        """Send and receive a Precipitation message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Precipitation.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_precipitation(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.Precipitation"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_streamflow(self, artemis_container):
        """Send and receive a Streamflow message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Streamflow.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_streamflow(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.Streamflow"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_gage_height(self, artemis_container):
        """Send and receive a GageHeight message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_GageHeight.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_gage_height(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.GageHeight"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_water_temperature(self, artemis_container):
        """Send and receive a WaterTemperature message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WaterTemperature.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_water_temperature(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.WaterTemperature"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_dissolved_oxygen(self, artemis_container):
        """Send and receive a DissolvedOxygen message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_DissolvedOxygen.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_dissolved_oxygen(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.DissolvedOxygen"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_ph(self, artemis_container):
        """Send and receive a PH message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_PH.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_ph(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.pH"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_specific_conductance(self, artemis_container):
        """Send and receive a SpecificConductance message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_SpecificConductance.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_specific_conductance(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.SpecificConductance"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_turbidity(self, artemis_container):
        """Send and receive a Turbidity message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Turbidity.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_turbidity(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.Turbidity"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_air_temperature(self, artemis_container):
        """Send and receive a AirTemperature message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_AirTemperature.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_air_temperature(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.AirTemperature"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_wind_speed(self, artemis_container):
        """Send and receive a WindSpeed message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WindSpeed.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_wind_speed(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.WindSpeed"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_wind_direction(self, artemis_container):
        """Send and receive a WindDirection message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WindDirection.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_wind_direction(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.WindDirection"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_relative_humidity(self, artemis_container):
        """Send and receive a RelativeHumidity message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_RelativeHumidity.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_relative_humidity(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.RelativeHumidity"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_barometric_pressure(self, artemis_container):
        """Send and receive a BarometricPressure message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_BarometricPressure.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_barometric_pressure(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.BarometricPressure"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_turbidity_fnu(self, artemis_container):
        """Send and receive a TurbidityFNU message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TurbidityFNU.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_turbidity_fnu(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.TurbidityFNU"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_fdom(self, artemis_container):
        """Send and receive a FDOM message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_FDOM.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_fdom(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.fDOM"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_reservoir_storage(self, artemis_container):
        """Send and receive a ReservoirStorage message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_ReservoirStorage.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_reservoir_storage(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.ReservoirStorage"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_lake_elevation_ngvd29(self, artemis_container):
        """Send and receive a LakeElevationNGVD29 message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_LakeElevationNGVD29.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_lake_elevation_ngvd29(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.LakeElevationNGVD29"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_water_depth(self, artemis_container):
        """Send and receive a WaterDepth message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WaterDepth.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_water_depth(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.WaterDepth"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_equipment_status(self, artemis_container):
        """Send and receive a EquipmentStatus message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_EquipmentStatus.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_equipment_status(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.EquipmentStatus"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_tidally_filtered_discharge(self, artemis_container):
        """Send and receive a TidallyFilteredDischarge message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_TidallyFilteredDischarge.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_tidally_filtered_discharge(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.TidallyFilteredDischarge"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_water_velocity(self, artemis_container):
        """Send and receive a WaterVelocity message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_WaterVelocity.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_water_velocity(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.WaterVelocity"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_estuary_elevation_ngvd29(self, artemis_container):
        """Send and receive a EstuaryElevationNGVD29 message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_EstuaryElevationNGVD29.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_estuary_elevation_ngvd29(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.EstuaryElevationNGVD29"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_lake_elevation_navd88(self, artemis_container):
        """Send and receive a LakeElevationNAVD88 message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_LakeElevationNAVD88.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_lake_elevation_navd88(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.LakeElevationNAVD88"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_salinity(self, artemis_container):
        """Send and receive a Salinity message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_Salinity.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_salinity(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.Salinity"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()
    
    def test_send_gate_opening(self, artemis_container):
        """Send and receive a GateOpening message via ActiveMQ Artemis."""
        # Create valid test data using the test helper
        payload = Test_GateOpening.create_instance()

        producer = USGSInstantaneousValuesAmqpProducer(
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
                producer.send_gate_opening(
                    data=payload,
                    _source_uri="value",
                    _agency_cd="value",
                    _site_no="value",
                    _parameter_cd="value",
                    _timeseries_cd="value",
                    _datetime="value",
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
                    assert cloud_event_payload.get("type") == "USGS.InstantaneousValues.amqp.GateOpening"
                    # Verify data section exists (either as data or data_base64)
                    assert "data" in cloud_event_payload or "data_base64" in cloud_event_payload
                else:
                    # Verify message body is not empty
                    assert received.body is not None
                assert received.subject == "{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}".format(agency_cd="value", site_no="value", parameter_cd="value", timeseries_cd="value")
        finally:
            producer.close()

