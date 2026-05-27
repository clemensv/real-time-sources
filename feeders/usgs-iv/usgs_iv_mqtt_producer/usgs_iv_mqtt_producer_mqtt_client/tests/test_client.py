# pylint: disable=line-too-long, trailing-whitespace, missing-module-docstring, missing-function-docstring, missing-class-docstring, redefined-outer-name, unused-argument, broad-exception-caught, broad-exception-raised, invalid-name, trailing-newlines, wrong-import-position, import-error, no-name-in-module

import os
import sys
import pytest
import pytest_asyncio
import asyncio
import time
import paho.mqtt.client as mqtt
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_mqtt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_mqtt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_mqtt_producer_mqtt_client/src')))

import usgs_iv_mqtt_producer_data
from usgs_iv_mqtt_producer_data import Site
from test_site import Test_Site
from usgs_iv_mqtt_producer_data import SiteTimeseries
from test_sitetimeseries import Test_SiteTimeseries
from usgs_iv_mqtt_producer_data import OtherParameter
from test_otherparameter import Test_OtherParameter
from usgs_iv_mqtt_producer_data import Precipitation
from test_precipitation import Test_Precipitation
from usgs_iv_mqtt_producer_data import Streamflow
from test_streamflow import Test_Streamflow
from usgs_iv_mqtt_producer_data import GageHeight
from test_gageheight import Test_GageHeight
from usgs_iv_mqtt_producer_data import WaterTemperature
from test_watertemperature import Test_WaterTemperature
from usgs_iv_mqtt_producer_data import DissolvedOxygen
from test_dissolvedoxygen import Test_DissolvedOxygen
from usgs_iv_mqtt_producer_data import PH
from test_ph import Test_PH
from usgs_iv_mqtt_producer_data import SpecificConductance
from test_specificconductance import Test_SpecificConductance
from usgs_iv_mqtt_producer_data import Turbidity
from test_turbidity import Test_Turbidity
from usgs_iv_mqtt_producer_data import AirTemperature
from test_airtemperature import Test_AirTemperature
from usgs_iv_mqtt_producer_data import WindSpeed
from test_windspeed import Test_WindSpeed
from usgs_iv_mqtt_producer_data import WindDirection
from test_winddirection import Test_WindDirection
from usgs_iv_mqtt_producer_data import RelativeHumidity
from test_relativehumidity import Test_RelativeHumidity
from usgs_iv_mqtt_producer_data import BarometricPressure
from test_barometricpressure import Test_BarometricPressure
from usgs_iv_mqtt_producer_data import TurbidityFNU
from test_turbidityfnu import Test_TurbidityFNU
from usgs_iv_mqtt_producer_data import FDOM
from test_fdom import Test_FDOM
from usgs_iv_mqtt_producer_data import ReservoirStorage
from test_reservoirstorage import Test_ReservoirStorage
from usgs_iv_mqtt_producer_data import LakeElevationNGVD29
from test_lakeelevationngvd29 import Test_LakeElevationNGVD29
from usgs_iv_mqtt_producer_data import WaterDepth
from test_waterdepth import Test_WaterDepth
from usgs_iv_mqtt_producer_data import EquipmentStatus
from test_equipmentstatus import Test_EquipmentStatus
from usgs_iv_mqtt_producer_data import TidallyFilteredDischarge
from test_tidallyfiltereddischarge import Test_TidallyFilteredDischarge
from usgs_iv_mqtt_producer_data import WaterVelocity
from test_watervelocity import Test_WaterVelocity
from usgs_iv_mqtt_producer_data import EstuaryElevationNGVD29
from test_estuaryelevationngvd29 import Test_EstuaryElevationNGVD29
from usgs_iv_mqtt_producer_data import LakeElevationNAVD88
from test_lakeelevationnavd88 import Test_LakeElevationNAVD88
from usgs_iv_mqtt_producer_data import Salinity
from test_salinity import Test_Salinity
from usgs_iv_mqtt_producer_data import GateOpening
from test_gateopening import Test_GateOpening
from usgs_iv_mqtt_producer_mqtt_client import USGSSitesMqttMqttClient
from usgs_iv_mqtt_producer_mqtt_client import USGSSiteTimeseriesMqttMqttClient
from usgs_iv_mqtt_producer_mqtt_client import USGSInstantaneousValuesMqttMqttClient

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
async def test_usgs_sites_mqtt_usgs_sites_mqtt_site_py(mosquitto_broker):
    """Test publishing and receiving USGS.Sites.mqtt.Site message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Site.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSSitesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSSitesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_sites_mqtt_site(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.Site, topic_params: dict):
        """Handler for USGS.Sites.mqtt.Site messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.Sites.Site"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_sites_mqtt_site_async = on_usgs_sites_mqtt_site
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_sites_mqtt/usgs_sites_mqtt_site"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_sites_mqtt_site(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
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
async def test_usgs_sitetimeseries_mqtt_usgs_site_timeseries_mqtt_site_timeseries_py(mosquitto_broker):
    """Test publishing and receiving USGS.SiteTimeseries.mqtt.SiteTimeseries message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SiteTimeseries.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSSiteTimeseriesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSSiteTimeseriesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_site_timeseries_mqtt_site_timeseries(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.SiteTimeseries, topic_params: dict):
        """Handler for USGS.SiteTimeseries.mqtt.SiteTimeseries messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.Sites.SiteTimeseries"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_site_timeseries_mqtt_site_timeseries_async = on_usgs_site_timeseries_mqtt_site_timeseries
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_sitetimeseries_mqtt/usgs_site_timeseries_mqtt_site_timeseries"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_site_timeseries_mqtt_site_timeseries(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_other_parameter_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.OtherParameter message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_OtherParameter.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_other_parameter(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.OtherParameter, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.OtherParameter messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.OtherParameter"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_other_parameter_async = on_usgs_instantaneous_values_mqtt_other_parameter
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_other_parameter"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_other_parameter(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_precipitation_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.Precipitation message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Precipitation.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_precipitation(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.Precipitation, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.Precipitation messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.Precipitation"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_precipitation_async = on_usgs_instantaneous_values_mqtt_precipitation
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_precipitation"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_precipitation(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_streamflow_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.Streamflow message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Streamflow.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_streamflow(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.Streamflow, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.Streamflow messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.Streamflow"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_streamflow_async = on_usgs_instantaneous_values_mqtt_streamflow
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_streamflow"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_streamflow(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_gage_height_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.GageHeight message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GageHeight.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_gage_height(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.GageHeight, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.GageHeight messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.GageHeight"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_gage_height_async = on_usgs_instantaneous_values_mqtt_gage_height
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_gage_height"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_gage_height(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_water_temperature_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.WaterTemperature message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WaterTemperature.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_water_temperature(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.WaterTemperature, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.WaterTemperature messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.WaterTemperature"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_water_temperature_async = on_usgs_instantaneous_values_mqtt_water_temperature
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_water_temperature"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_water_temperature(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_dissolved_oxygen_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.DissolvedOxygen message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_DissolvedOxygen.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_dissolved_oxygen(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.DissolvedOxygen, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.DissolvedOxygen messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.DissolvedOxygen"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_dissolved_oxygen_async = on_usgs_instantaneous_values_mqtt_dissolved_oxygen
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_dissolved_oxygen"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_dissolved_oxygen(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_p_h_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.pH message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_PH.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_p_h(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.PH, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.pH messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.pH"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_p_h_async = on_usgs_instantaneous_values_mqtt_p_h
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_p_h"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_p_h(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_specific_conductance_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.SpecificConductance message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_SpecificConductance.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_specific_conductance(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.SpecificConductance, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.SpecificConductance messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.SpecificConductance"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_specific_conductance_async = on_usgs_instantaneous_values_mqtt_specific_conductance
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_specific_conductance"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_specific_conductance(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_turbidity_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.Turbidity message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Turbidity.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_turbidity(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.Turbidity, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.Turbidity messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.Turbidity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_turbidity_async = on_usgs_instantaneous_values_mqtt_turbidity
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_turbidity"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_turbidity(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_air_temperature_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.AirTemperature message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_AirTemperature.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_air_temperature(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.AirTemperature, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.AirTemperature messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.AirTemperature"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_air_temperature_async = on_usgs_instantaneous_values_mqtt_air_temperature
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_air_temperature"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_air_temperature(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_wind_speed_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.WindSpeed message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WindSpeed.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_wind_speed(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.WindSpeed, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.WindSpeed messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.WindSpeed"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_wind_speed_async = on_usgs_instantaneous_values_mqtt_wind_speed
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_wind_speed"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_wind_speed(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_wind_direction_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.WindDirection message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WindDirection.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_wind_direction(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.WindDirection, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.WindDirection messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.WindDirection"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_wind_direction_async = on_usgs_instantaneous_values_mqtt_wind_direction
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_wind_direction"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_wind_direction(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_relative_humidity_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.RelativeHumidity message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_RelativeHumidity.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_relative_humidity(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.RelativeHumidity, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.RelativeHumidity messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.RelativeHumidity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_relative_humidity_async = on_usgs_instantaneous_values_mqtt_relative_humidity
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_relative_humidity"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_relative_humidity(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_barometric_pressure_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.BarometricPressure message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_BarometricPressure.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_barometric_pressure(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.BarometricPressure, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.BarometricPressure messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.BarometricPressure"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_barometric_pressure_async = on_usgs_instantaneous_values_mqtt_barometric_pressure
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_barometric_pressure"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_barometric_pressure(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_turbidity_fnu_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.TurbidityFNU message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TurbidityFNU.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_turbidity_fnu(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.TurbidityFNU, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.TurbidityFNU messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.TurbidityFNU"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_turbidity_fnu_async = on_usgs_instantaneous_values_mqtt_turbidity_fnu
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_turbidity_fnu"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_turbidity_fnu(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_f_dom_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.fDOM message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_FDOM.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_f_dom(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.FDOM, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.fDOM messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.fDOM"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_f_dom_async = on_usgs_instantaneous_values_mqtt_f_dom
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_f_dom"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_f_dom(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_reservoir_storage_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.ReservoirStorage message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_ReservoirStorage.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_reservoir_storage(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.ReservoirStorage, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.ReservoirStorage messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.ReservoirStorage"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_reservoir_storage_async = on_usgs_instantaneous_values_mqtt_reservoir_storage
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_reservoir_storage"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_reservoir_storage(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.LakeElevationNGVD29 message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LakeElevationNGVD29.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.LakeElevationNGVD29, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.LakeElevationNGVD29 messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.LakeElevationNGVD29"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_async = on_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_lake_elevation_ngvd29"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_lake_elevation_ngvd29(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_water_depth_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.WaterDepth message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WaterDepth.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_water_depth(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.WaterDepth, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.WaterDepth messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.WaterDepth"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_water_depth_async = on_usgs_instantaneous_values_mqtt_water_depth
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_water_depth"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_water_depth(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_equipment_status_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.EquipmentStatus message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_EquipmentStatus.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_equipment_status(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.EquipmentStatus, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.EquipmentStatus messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.EquipmentStatus"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_equipment_status_async = on_usgs_instantaneous_values_mqtt_equipment_status
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_equipment_status"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_equipment_status(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_tidally_filtered_discharge_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_TidallyFilteredDischarge.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_tidally_filtered_discharge(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.TidallyFilteredDischarge, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.TidallyFilteredDischarge"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_tidally_filtered_discharge_async = on_usgs_instantaneous_values_mqtt_tidally_filtered_discharge
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_tidally_filtered_discharge"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_tidally_filtered_discharge(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_water_velocity_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.WaterVelocity message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_WaterVelocity.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_water_velocity(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.WaterVelocity, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.WaterVelocity messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.WaterVelocity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_water_velocity_async = on_usgs_instantaneous_values_mqtt_water_velocity
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_water_velocity"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_water_velocity(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29 message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_EstuaryElevationNGVD29.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.EstuaryElevationNGVD29, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29 messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.EstuaryElevationNGVD29"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_async = on_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_lake_elevation_navd88_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.LakeElevationNAVD88 message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_LakeElevationNAVD88.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_lake_elevation_navd88(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.LakeElevationNAVD88, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.LakeElevationNAVD88 messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.LakeElevationNAVD88"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_lake_elevation_navd88_async = on_usgs_instantaneous_values_mqtt_lake_elevation_navd88
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_lake_elevation_navd88"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_lake_elevation_navd88(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_salinity_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.Salinity message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_Salinity.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_salinity(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.Salinity, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.Salinity messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.Salinity"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_salinity_async = on_usgs_instantaneous_values_mqtt_salinity
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_salinity"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_salinity(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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
async def test_usgs_instantaneousvalues_mqtt_usgs_instantaneous_values_mqtt_gate_opening_py(mosquitto_broker):
    """Test publishing and receiving USGS.InstantaneousValues.mqtt.GateOpening message via MQTT."""
    broker_host, broker_port = mosquitto_broker
    # Create valid test data using the test helper
    test_data = Test_GateOpening.create_instance()
    
    # Create subscriber client
    subscriber_mqtt = mqtt.Client(client_id="test_subscriber")
    loop = asyncio.get_running_loop()
    subscriber_client = USGSInstantaneousValuesMqttMqttClient(subscriber_mqtt, content_mode='structured', loop=loop)
    
    # Create publisher client
    publisher_mqtt = mqtt.Client(client_id="test_publisher")
    publisher_client = USGSInstantaneousValuesMqttMqttClient(publisher_mqtt, content_mode='structured', loop=loop)
    
    # Track received messages (expecting 5)
    received_data = []
    received_event = asyncio.Event()
    
    async def on_usgs_instantaneous_values_mqtt_gate_opening(mqtt_msg, cloud_event, data: usgs_iv_mqtt_producer_data.GateOpening, topic_params: dict):
        """Handler for USGS.InstantaneousValues.mqtt.GateOpening messages."""
        received_data.append(data)
        assert cloud_event['type'] == "USGS.InstantaneousValues.GateOpening"
        if len(received_data) >= 5:
            received_event.set()
    
    # Register handler
    subscriber_client.usgs_instantaneous_values_mqtt_gate_opening_async = on_usgs_instantaneous_values_mqtt_gate_opening
    
    # Connect both clients
    await subscriber_client.connect(broker_host, broker_port)
    await publisher_client.connect(broker_host, broker_port)
    
    # Subscribe to topic
    test_topic = "test/usgs_instantaneousvalues_mqtt/usgs_instantaneous_values_mqtt_gate_opening"
    await subscriber_client.subscribe([test_topic])
    
    # Wait for subscription to be active
    await asyncio.sleep(1)
    
    # Publish 5 messages to test message settlement and ordering
    for i in range(5):
        await publisher_client.publish_usgs_instantaneous_values_mqtt_gate_opening(
            topic=test_topic,
            source_uri=f"test_source_uri_{i}",
            agency_cd=f"test_agency_cd_{i}",
            site_no=f"test_site_no_{i}",
            parameter_cd=f"test_parameter_cd_{i}",
            timeseries_cd=f"test_timeseries_cd_{i}",
            datetime=f"test_datetime_{i}",
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


