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
            return ref_ok and tel_ok

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

    def test_emits_telemetry(self, kafka: KafkaFixture, digitraffic_road_image):
        _run_kafka_flow_test(
            kafka, digitraffic_road_image, self.TOPIC,
            reference_types=None,
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
