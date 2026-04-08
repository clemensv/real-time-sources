"""Docker end-to-end Kafka data-flow tests.

These tests build the Docker image, start the container alongside a real
Kafka broker on a shared Docker network, and verify that CloudEvents
messages arrive on the expected topic with correct Kafka keys and payloads
that conform to the source xRegistry JsonStructure schemas.

Each test validates that the container emits **both** reference data
(station / zone / site definitions) **and** telemetry data (observations,
measurements, readings, alerts).  Projects that only emit telemetry
(noaa-goes, usgs-earthquakes) are tested for telemetry only.

Projects use plain (non-SASL) Kafka connections via
``CONNECTION_STRING=BootstrapServer=host:port;EntityPath=topic``.

Run with:  pytest tests/docker_e2e/test_docker_kafka_flow.py -v --timeout=600

To persist consumed Kafka messages and container logs for manual verification,
pass ``--kafka-artifacts-dir <path>``.
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, Set

import pytest
from confluent_kafka import Consumer

_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

from helpers import (
    assert_kafka_contract,
    build_image,
    ConsumedKafkaMessage,
    project_dir_from_image,
    run_container_detached,
    wait_for_container_logs,
    write_kafka_artifacts,
    KafkaFixture,
)


# ---------------------------------------------------------------------------
# Fixtures – one per project image (module-scoped so builds are cached)
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def chmi_image():
    return build_image('chmi-hydro')

@pytest.fixture(scope='module')
def imgw_image():
    return build_image('imgw-hydro')

@pytest.fixture(scope='module')
def smhi_image():
    return build_image('smhi-hydro')

@pytest.fixture(scope='module')
def noaa_image():
    return build_image('noaa')

@pytest.fixture(scope='module')
def noaa_goes_image():
    return build_image('noaa-goes')

@pytest.fixture(scope='module')
def noaa_ndbc_image():
    return build_image('noaa-ndbc')

@pytest.fixture(scope='module')
def noaa_nws_image():
    return build_image('noaa-nws')

@pytest.fixture(scope='module')
def usgs_iv_image():
    return build_image('usgs-iv')

@pytest.fixture(scope='module')
def usgs_earthquakes_image():
    return build_image('usgs-earthquakes')

@pytest.fixture(scope='module')
def pegelonline_image():
    return build_image('pegelonline')

@pytest.fixture(scope='module')
def hubeau_image():
    return build_image('hubeau-hydrometrie')

@pytest.fixture(scope='module')
def uk_ea_image():
    return build_image('uk-ea-flood-monitoring')

@pytest.fixture(scope='module')
def rws_image():
    return build_image('rws-waterwebservices')

@pytest.fixture(scope='module')
def waterinfo_image():
    return build_image('waterinfo-vmm')

@pytest.fixture(scope='module')
def nve_image():
    return build_image('nve-hydro')

@pytest.fixture(scope='module')
def syke_image():
    return build_image('syke-hydro')

@pytest.fixture(scope='module')
def bafu_image():
    return build_image('bafu-hydro')

@pytest.fixture(scope='module')
def autobahn_image():
    return build_image('autobahn')

@pytest.fixture(scope='module')
def digitraffic_road_image():
    return build_image('digitraffic-road')

@pytest.fixture(scope='module')
def bom_australia_image():
    return build_image('bom-australia')

@pytest.fixture(scope='module')
def smhi_weather_image():
    return build_image('smhi-weather')

@pytest.fixture(scope='module')
def hko_image():
    return build_image('hko-hong-kong')

@pytest.fixture(scope='module')
def singapore_nea_image():
    return build_image('singapore-nea')

@pytest.fixture(scope='module')
def defra_aurn_image():
    return build_image('defra-aurn')

@pytest.fixture(scope='module')
def irceline_belgium_image():
    return build_image('irceline-belgium')

@pytest.fixture(scope='module')
def sensor_community_image():
    return build_image('sensor-community')

@pytest.fixture(scope='module')
def canada_aqhi_image():
    return build_image('canada-aqhi')

@pytest.fixture(scope='module')
def fmi_finland_image():
    return build_image('fmi-finland')

@pytest.fixture(scope='module')
def hongkong_epd_image():
    return build_image('hongkong-epd')

@pytest.fixture(scope='module')
def luchtmeetnet_nl_image():
    return build_image('luchtmeetnet-nl')

@pytest.fixture(scope='module')
def uba_airdata_image():
    return build_image('uba-airdata')

@pytest.fixture(scope='module')
def laqn_london_image():
    return build_image('laqn-london')

@pytest.fixture(scope='module')
def environment_canada_image():
    return build_image('environment-canada')

@pytest.fixture(scope='module')
def wikimedia_eventstreams_image():
    return build_image('wikimedia-eventstreams')

@pytest.fixture(scope='module')
def blitzortung_image():
    return build_image('blitzortung')

@pytest.fixture(scope='module')
def bfs_odl_image():
    return build_image('bfs-odl')

@pytest.fixture(scope='module')
def gios_poland_image():
    return build_image('gios-poland')

@pytest.fixture(scope='module')
def irail_image():
    return build_image('irail')

@pytest.fixture(scope='module')
def wsdot_image():
    return build_image('wsdot')


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _run_kafka_flow_test(
    kafka,
    image,
    topic: str,
    *,
    reference_types: Optional[List[str]] = None,
    telemetry_types: Optional[List[str]] = None,
    required_types: Optional[List[str]] = None,
    extra_env: Optional[Dict[str, str]] = None,
    min_messages: int = 5,
    timeout: int = 300,
):
    """Run a container against Kafka and validate keys, schemas, and event types.

    Consumes messages until both reference and telemetry events have been
    observed (or *timeout* is reached).  Many projects emit all station
    records before any observations, so a simple fixed-count approach would
    miss the telemetry data.

    Args:
        kafka: KafkaFixture instance.
        image: Docker image to run.
        topic: Kafka topic name.
        reference_types: Substrings expected in ``type`` for reference events.
            Pass *None* for projects that emit no reference data.
        telemetry_types: Substrings expected in ``type`` for telemetry events.
        extra_env: Additional environment variables for the container.
        min_messages: Minimum total messages to consume.
        timeout: Seconds to wait for all expected event categories.
    """
    project_dir = project_dir_from_image(image)
    kafka.create_topic(topic, partitions=4)
    env = {
        'CONNECTION_STRING': f'BootstrapServer={kafka.internal_address};EntityPath={topic}',
        'KAFKA_ENABLE_TLS': 'false',
    }
    if extra_env:
        env.update(extra_env)

    container = run_container_detached(image, environment=env)
    try:
        # Consume in a loop until both event categories are seen or timeout.
        consumer = Consumer({
            'bootstrap.servers': kafka.external_address,
            'group.id': f'test-{topic}',
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe([topic])
        records: List[ConsumedKafkaMessage] = []
        observed_types: Set[str] = set()
        deadline = time.time() + timeout

        def _types_satisfied() -> bool:
            ref_ok = reference_types is None or any(
                any(pat in t for pat in reference_types) for t in observed_types
            )
            tel_ok = telemetry_types is None or any(
                any(pat in t for pat in telemetry_types) for t in observed_types
            )
            required_ok = required_types is None or all(
                any(pat in t for t in observed_types) for pat in required_types
            )
            return ref_ok and tel_ok and required_ok

        try:
            while time.time() < deadline:
                if len(records) >= min_messages and _types_satisfied():
                    break
                msg = consumer.poll(1.0)
                if msg and not msg.error():
                    raw = msg.value()
                    records.append(
                        ConsumedKafkaMessage(
                            key=msg.key(),
                            value=raw,
                            partition=msg.partition(),
                            offset=msg.offset(),
                        )
                    )
                    try:
                        ev = json.loads(raw)
                        if 'type' in ev:
                            observed_types.add(ev['type'])
                    except (ValueError, TypeError):
                        pass
        finally:
            consumer.close()

        assert len(records) >= min_messages, (
            f'Expected >={min_messages} messages, got {len(records)}.\n'
            f'Container logs:\n{container.logs().decode()}'
        )
        assert_kafka_contract(project_dir, records)

        # --- Validate reference data ---
        if reference_types is not None:
            has_reference = any(
                any(pat in t for pat in reference_types) for t in observed_types
            )
            assert has_reference, (
                f'No reference events found.  Expected type containing one of '
                f'{reference_types}, but got types: {sorted(observed_types)}\n'
                f'Container logs:\n{container.logs().decode()}'
            )

        # --- Validate telemetry data ---
        if telemetry_types is not None:
            has_telemetry = any(
                any(pat in t for pat in telemetry_types) for t in observed_types
            )
            assert has_telemetry, (
                f'No telemetry events found.  Expected type containing one of '
                f'{telemetry_types}, but got types: {sorted(observed_types)}\n'
                f'Container logs:\n{container.logs().decode()}'
            )

        if required_types is not None:
            missing = [
                pat for pat in required_types
                if not any(pat in t for t in observed_types)
            ]
            assert not missing, (
                f'Missing required event families {missing}. Observed types: '
                f'{sorted(observed_types)}\n'
                f'Container logs:\n{container.logs().decode()}'
            )
    finally:
        container_logs = container.logs().decode('utf-8', errors='replace')
        write_kafka_artifacts(project_dir, topic, records, container_logs)
        container.stop(timeout=5)
        container.remove(force=True)


# ---------------------------------------------------------------------------
# CHMI Hydro (Czech Republic – water levels)
# ---------------------------------------------------------------------------

class TestCHMIHydroDockerFlow:
    TOPIC = 'test-chmi-hydro'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, chmi_image):
        _run_kafka_flow_test(
            kafka, chmi_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevelObservation'],
            extra_env={'KAFKA_TOPIC': self.TOPIC, 'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# IMGW Hydro (Poland – water levels)
# ---------------------------------------------------------------------------

class TestIMGWHydroDockerFlow:
    TOPIC = 'test-imgw-hydro'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, imgw_image):
        _run_kafka_flow_test(
            kafka, imgw_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevelObservation'],
            extra_env={'KAFKA_TOPIC': self.TOPIC, 'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# SMHI Hydro (Sweden – discharge)
# ---------------------------------------------------------------------------

class TestSMHIHydroDockerFlow:
    TOPIC = 'test-smhi-hydro'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, smhi_image):
        _run_kafka_flow_test(
            kafka, smhi_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['DischargeObservation'],
            extra_env={'KAFKA_TOPIC': self.TOPIC, 'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# NOAA (Tides & Currents – weather observations)
# ---------------------------------------------------------------------------

class TestNOAADockerFlow:
    TOPIC = 'test-noaa'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, noaa_image):
        _run_kafka_flow_test(
            kafka, noaa_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevel', 'AirTemperature', 'AirPressure',
                             'WaterTemperature', 'Wind', 'Humidity',
                             'Conductivity', 'Salinity', 'Visibility',
                             'Currents', 'Predictions'],
        )


# ---------------------------------------------------------------------------
# NOAA GOES (Space weather – telemetry only)
# ---------------------------------------------------------------------------

class TestNOAAGoesDockerFlow:
    TOPIC = 'test-noaa-goes'

    def test_emits_telemetry(self, kafka: KafkaFixture, noaa_goes_image):
        _run_kafka_flow_test(
            kafka, noaa_goes_image, self.TOPIC,
            reference_types=None,
            telemetry_types=['SpaceWeatherAlert', 'PlanetaryKIndex', 'SolarWindSummary'],
            min_messages=1,
        )


# ---------------------------------------------------------------------------
# Autobahn (Germany - motorway traffic events)
# ---------------------------------------------------------------------------

class TestAutobahnDockerFlow:
    TOPIC = 'test-autobahn'

    def test_emits_telemetry(self, kafka: KafkaFixture, autobahn_image):
        _run_kafka_flow_test(
            kafka, autobahn_image, self.TOPIC,
            reference_types=None,
            telemetry_types=[
                'Roadwork',
                'ShortTermRoadwork',
                'Closure',
                'EntryExitClosure',
                'ParkingLorry',
                'ElectricChargingStation',
                'StrongElectricChargingStation',
            ],
            extra_env={
                'KAFKA_TOPIC': self.TOPIC,
                'AUTOBAHN_POLL_INTERVAL': '5',
                'AUTOBAHN_ROADS': 'A1',
                'AUTOBAHN_RESOURCES': 'roadworks,closure,parking_lorry,electric_charging_station',
            },
            min_messages=3,
        )


# ---------------------------------------------------------------------------
# Digitraffic Road (Finland — road traffic: sensors, messages, maintenance)
# ---------------------------------------------------------------------------

class TestDigitrafficRoadDockerFlow:
    TOPIC = 'test-digitraffic-road'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, digitraffic_road_image):
        _run_kafka_flow_test(
            kafka, digitraffic_road_image, self.TOPIC,
            reference_types=[
                'TmsStation',
                'WeatherStation',
                'MaintenanceTaskType',
            ],
            telemetry_types=[
                'TmsSensorData',
                'WeatherSensorData',
                'TrafficAnnouncement',
                'RoadWork',
                'WeightRestriction',
                'ExemptedTransport',
                'MaintenanceTracking',
            ],
            extra_env={
                'KAFKA_TOPIC_SENSORS': self.TOPIC,
                'KAFKA_TOPIC_MESSAGES': self.TOPIC,
                'KAFKA_TOPIC_MAINTENANCE': self.TOPIC,
            },
            min_messages=3,
        )


# ---------------------------------------------------------------------------
# NOAA NDBC (Buoy observations)
# ---------------------------------------------------------------------------

class TestNOAANdbcDockerFlow:
    TOPIC = 'test-noaa-ndbc'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, noaa_ndbc_image):
        _run_kafka_flow_test(
            kafka, noaa_ndbc_image, self.TOPIC,
            reference_types=['BuoyStation'],
            telemetry_types=['BuoyObservation'],
        )


# ---------------------------------------------------------------------------
# NOAA NWS (Weather alerts)
# ---------------------------------------------------------------------------

class TestNOAANwsDockerFlow:
    TOPIC = 'test-noaa-nws'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, noaa_nws_image):
        _run_kafka_flow_test(
            kafka, noaa_nws_image, self.TOPIC,
            reference_types=['Zone'],
            telemetry_types=['WeatherAlert'],
        )


# ---------------------------------------------------------------------------
# USGS Instantaneous Values
# ---------------------------------------------------------------------------

class TestUSGSIVDockerFlow:
    TOPIC = 'test-usgs-iv'

    @pytest.mark.xfail(reason='USGS API polls all 50+ states; intermittent upstream timeouts')
    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, usgs_iv_image):
        _run_kafka_flow_test(
            kafka, usgs_iv_image, self.TOPIC,
            reference_types=['Site'],
            telemetry_types=['Streamflow', 'GageHeight', 'WaterTemperature',
                             'Precipitation', 'DissolvedOxygen'],
            timeout=480,
        )


# ---------------------------------------------------------------------------
# USGS Earthquakes (telemetry only)
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="Flaky: depends on real seismic activity during test window")
class TestUSGSEarthquakesDockerFlow:
    TOPIC = 'test-usgs-earthquakes'

    def test_emits_telemetry(self, kafka: KafkaFixture, usgs_earthquakes_image):
        _run_kafka_flow_test(
            kafka, usgs_earthquakes_image, self.TOPIC,
            reference_types=None,
            telemetry_types=['Earthquakes.Event'],
            min_messages=1,
        )


# ---------------------------------------------------------------------------
# Wikimedia EventStreams (telemetry only)
# ---------------------------------------------------------------------------

class TestWikimediaEventStreamsDockerFlow:
    TOPIC = 'test-wikimedia-eventstreams'

    def test_emits_telemetry(self, kafka: KafkaFixture, wikimedia_eventstreams_image):
        _run_kafka_flow_test(
            kafka, wikimedia_eventstreams_image, self.TOPIC,
            reference_types=None,
            telemetry_types=['RecentChange'],
            extra_env={'KAFKA_TOPIC': self.TOPIC},
            min_messages=1,
            timeout=180,
        )


# ---------------------------------------------------------------------------
# Blitzortung (telemetry only)
# ---------------------------------------------------------------------------

class TestBlitzortungDockerFlow:
    TOPIC = 'test-blitzortung'

    def test_emits_telemetry(self, kafka: KafkaFixture, blitzortung_image):
        _run_kafka_flow_test(
            kafka, blitzortung_image, self.TOPIC,
            reference_types=None,
            telemetry_types=['LightningStroke'],
            extra_env={'KAFKA_TOPIC': self.TOPIC},
            min_messages=1,
            timeout=180,
        )


# ---------------------------------------------------------------------------
# Pegelonline (German water levels)
# ---------------------------------------------------------------------------

class TestPegelonlineDockerFlow:
    TOPIC = 'test-pegelonline'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, pegelonline_image):
        _run_kafka_flow_test(
            kafka, pegelonline_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['CurrentMeasurement'],
        )


# ---------------------------------------------------------------------------
# Hub'Eau Hydrométrie (French water levels)
# ---------------------------------------------------------------------------

class TestHubeauDockerFlow:
    TOPIC = 'test-hubeau'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, hubeau_image):
        _run_kafka_flow_test(
            kafka, hubeau_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['Observation'],
        )


# ---------------------------------------------------------------------------
# UK Environment Agency Flood Monitoring
# ---------------------------------------------------------------------------

class TestUKEADockerFlow:
    TOPIC = 'test-uk-ea'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, uk_ea_image):
        _run_kafka_flow_test(
            kafka, uk_ea_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['Reading'],
        )


# ---------------------------------------------------------------------------
# Rijkswaterstaat Waterwebservices (Dutch water levels)
# ---------------------------------------------------------------------------

class TestRWSDockerFlow:
    TOPIC = 'test-rws'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, rws_image):
        _run_kafka_flow_test(
            kafka, rws_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevelObservation'],
        )


# ---------------------------------------------------------------------------
# iRail (Belgian railway departures)
# ---------------------------------------------------------------------------

class TestIRailDockerFlow:
    TOPIC = 'test-irail'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, irail_image):
        _run_kafka_flow_test(
            kafka, irail_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['StationBoard'],
            extra_env={'STATION_FILTER': '008814001,008821006'},
        )


# ---------------------------------------------------------------------------
# WSDOT (Washington State traffic flow)
# ---------------------------------------------------------------------------

class TestWSDOTDockerFlow:
    TOPIC = 'test-wsdot'

    @pytest.fixture(autouse=True)
    def _require_access_code(self):
        code = os.environ.get('WSDOT_ACCESS_CODE', '')
        if not code:
            pytest.skip('WSDOT_ACCESS_CODE not set')

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, wsdot_image):
        _run_kafka_flow_test(
            kafka, wsdot_image, self.TOPIC,
            reference_types=['TrafficFlowStation', 'WeatherStation'],
            telemetry_types=['TrafficFlowReading', 'TravelTimeRoute', 'MountainPassCondition',
                             'WeatherReading', 'TollRate', 'BorderCrossing', 'VesselLocation'],
            extra_env={
                'WSDOT_ACCESS_CODE': os.environ['WSDOT_ACCESS_CODE'],
                'REGION_FILTER': 'Eastern',
            },
        )


# ---------------------------------------------------------------------------
# Waterinfo VMM (Flemish water levels)
# ---------------------------------------------------------------------------

class TestWaterinfoVMMDockerFlow:
    TOPIC = 'test-waterinfo-vmm'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, waterinfo_image):
        _run_kafka_flow_test(
            kafka, waterinfo_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevelReading'],
        )


# ---------------------------------------------------------------------------
# NVE Hydro (Norway – water levels & discharge)
# ---------------------------------------------------------------------------

class TestNVEHydroDockerFlow:
    TOPIC = 'test-nve-hydro'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, nve_image):
        api_key = os.environ.get('NVE_API_KEY', '')
        assert api_key, 'NVE_API_KEY environment variable must be set'
        _run_kafka_flow_test(
            kafka, nve_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevelObservation'],
            extra_env={'NVE_API_KEY': api_key},
        )


# ---------------------------------------------------------------------------
# SYKE Hydro (Finland – water levels & discharge)
# ---------------------------------------------------------------------------

class TestSYKEHydroDockerFlow:
    TOPIC = 'test-syke-hydro'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, syke_image):
        _run_kafka_flow_test(
            kafka, syke_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevelObservation'],
        )


# ---------------------------------------------------------------------------
# BAFU Hydro (Switzerland – water levels, discharge & temperature)
# ---------------------------------------------------------------------------

class TestBAFUHydroDockerFlow:
    TOPIC = 'test-bafu-hydro'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, bafu_image):
        _run_kafka_flow_test(
            kafka, bafu_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WaterLevelObservation'],
        )


# ---------------------------------------------------------------------------
# BOM Australia (weather observations)
# ---------------------------------------------------------------------------

class TestBOMAustraliaDockerFlow:
    TOPIC = 'test-bom-australia'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, bom_australia_image):
        _run_kafka_flow_test(
            kafka, bom_australia_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WeatherObservation'],
        )


# ---------------------------------------------------------------------------
# SMHI Weather (Sweden – meteorological observations)
# ---------------------------------------------------------------------------

class TestSMHIWeatherDockerFlow:
    TOPIC = 'test-smhi-weather'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, smhi_weather_image):
        _run_kafka_flow_test(
            kafka, smhi_weather_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WeatherObservation'],
        )


# ---------------------------------------------------------------------------
# HKO Hong Kong (weather observations)
# ---------------------------------------------------------------------------

class TestHKODockerFlow:
    TOPIC = 'test-hko-hong-kong'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, hko_image):
        _run_kafka_flow_test(
            kafka, hko_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WeatherObservation'],
        )


# ---------------------------------------------------------------------------
# Singapore NEA (weather observations)
# ---------------------------------------------------------------------------

class TestSingaporeNEADockerFlow:
    TOPIC = 'test-singapore-nea'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, singapore_nea_image):
        _run_kafka_flow_test(
            kafka, singapore_nea_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WeatherObservation'],
        )


# ---------------------------------------------------------------------------
# Air Quality sources
# ---------------------------------------------------------------------------

class TestSingaporeNEAAirQualityDockerFlow:
    TOPIC = 'test-singapore-nea-airquality'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, singapore_nea_image):
        _run_kafka_flow_test(
            kafka, singapore_nea_image, self.TOPIC,
            reference_types=['Region'],
            telemetry_types=['PSIReading', 'PM25Reading'],
            required_types=['Region', 'PSIReading', 'PM25Reading'],
            extra_env={
                'KAFKA_TOPIC': self.TOPIC,
                'AIRQUALITY_TOPIC': self.TOPIC,
                'AIRQUALITY_POLLING_INTERVAL': '300',
            },
        )


# ---------------------------------------------------------------------------
# Defra AURN (UK air quality)
# ---------------------------------------------------------------------------

class TestDefraAURNDockerFlow:
    TOPIC = 'test-defra-aurn'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, defra_aurn_image):
        _run_kafka_flow_test(
            kafka, defra_aurn_image, self.TOPIC,
            reference_types=['Station', 'Timeseries'],
            telemetry_types=['Observation'],
            required_types=['Station', 'Timeseries', 'Observation'],
            extra_env={'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# IRCELINE Belgium (Belgian air quality)
# ---------------------------------------------------------------------------

class TestIrcelineBelgiumDockerFlow:
    TOPIC = 'test-irceline-belgium'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, irceline_belgium_image):
        _run_kafka_flow_test(
            kafka, irceline_belgium_image, self.TOPIC,
            reference_types=['Station', 'Timeseries'],
            telemetry_types=['Observation'],
            required_types=['Station', 'Timeseries', 'Observation'],
            extra_env={'KAFKA_TOPIC': self.TOPIC, 'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# Sensor.Community (citizen air sensors)
# ---------------------------------------------------------------------------

class TestSensorCommunityDockerFlow:
    TOPIC = 'test-sensor-community'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, sensor_community_image):
        _run_kafka_flow_test(
            kafka, sensor_community_image, self.TOPIC,
            reference_types=['SensorInfo'],
            telemetry_types=['SensorReading'],
            required_types=['SensorInfo', 'SensorReading'],
            extra_env={'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# Canada AQHI (community AQHI observations and forecasts)
# ---------------------------------------------------------------------------

class TestCanadaAQHIDockerFlow:
    TOPIC = 'test-canada-aqhi'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, canada_aqhi_image):
        _run_kafka_flow_test(
            kafka, canada_aqhi_image, self.TOPIC,
            reference_types=['Community'],
            telemetry_types=['Observation', 'Forecast'],
            required_types=['Community', 'Observation', 'Forecast'],
            extra_env={'POLLING_INTERVAL': '5', 'PROVINCES': 'ON'},
        )


# ---------------------------------------------------------------------------
# FMI Finland (hourly air quality observations)
# ---------------------------------------------------------------------------

class TestFMIFinlandDockerFlow:
    TOPIC = 'test-fmi-finland'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, fmi_finland_image):
        _run_kafka_flow_test(
            kafka, fmi_finland_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['Observation'],
            required_types=['Station', 'Observation'],
            extra_env={'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# Hong Kong EPD AQHI
# ---------------------------------------------------------------------------

class TestHongKongEPDDockerFlow:
    TOPIC = 'test-hongkong-epd'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, hongkong_epd_image):
        _run_kafka_flow_test(
            kafka, hongkong_epd_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['AQHIReading'],
            required_types=['Station', 'AQHIReading'],
            extra_env={'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# Luchtmeetnet Netherlands
# ---------------------------------------------------------------------------

class TestLuchtmeetnetNLDockerFlow:
    TOPIC = 'test-luchtmeetnet-nl'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, luchtmeetnet_nl_image):
        _run_kafka_flow_test(
            kafka, luchtmeetnet_nl_image, self.TOPIC,
            reference_types=['Station', 'Component'],
            telemetry_types=['Measurement', 'LKI'],
            required_types=['Station', 'Component', 'Measurement', 'LKI'],
            extra_env={'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# UBA AirData Germany
# ---------------------------------------------------------------------------

class TestUBAAirDataDockerFlow:
    TOPIC = 'test-uba-airdata'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, uba_airdata_image):
        _run_kafka_flow_test(
            kafka, uba_airdata_image, self.TOPIC,
            reference_types=['Station', 'Component'],
            telemetry_types=['Measure'],
            required_types=['Station', 'Component', 'Measure'],
            extra_env={'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# LAQN London
# ---------------------------------------------------------------------------

class TestLAQNLondonDockerFlow:
    TOPIC = 'test-laqn-london'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, laqn_london_image):
        _run_kafka_flow_test(
            kafka, laqn_london_image, self.TOPIC,
            reference_types=['Site', 'Species'],
            telemetry_types=['Measurement', 'DailyIndex'],
            required_types=['Site', 'Species', 'Measurement', 'DailyIndex'],
            extra_env={'POLLING_INTERVAL': '5'},
        )


# ---------------------------------------------------------------------------
# Environment Canada (SWOB weather observations)
# ---------------------------------------------------------------------------

class TestEnvironmentCanadaDockerFlow:
    TOPIC = 'test-environment-canada'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, environment_canada_image):
        _run_kafka_flow_test(
            kafka, environment_canada_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['WeatherObservation'],
        )


# ---------------------------------------------------------------------------
# BfS ODL (German gamma dose rate monitoring)
# ---------------------------------------------------------------------------

class TestBfsOdlDockerFlow:
    TOPIC = 'test-bfs-odl'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, bfs_odl_image):
        _run_kafka_flow_test(
            kafka, bfs_odl_image, self.TOPIC,
            reference_types=['Station'],
            telemetry_types=['DoseRateMeasurement'],
        )


# ---------------------------------------------------------------------------
# GIOŚ Poland (air quality)
# ---------------------------------------------------------------------------

class TestGIOSPolandDockerFlow:
    TOPIC = 'test-gios-poland'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, gios_poland_image):
        _run_kafka_flow_test(
            kafka, gios_poland_image, self.TOPIC,
            reference_types=['Station', 'Sensor'],
            telemetry_types=['Measurement', 'AirQualityIndex'],
            required_types=['Station', 'Sensor', 'Measurement', 'AirQualityIndex'],
# DWD Pollenflug (German pollen forecast)
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def dwd_pollenflug_image():
    return build_image('dwd-pollenflug')

class TestDWDPollenflugDockerFlow:
    TOPIC = 'test-dwd-pollenflug'

    def test_emits_reference_and_telemetry(self, kafka: KafkaFixture, dwd_pollenflug_image):
        _run_kafka_flow_test(
            kafka, dwd_pollenflug_image, self.TOPIC,
            reference_types=['Region'],
            telemetry_types=['PollenForecast'],
        )
