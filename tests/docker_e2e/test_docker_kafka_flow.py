"""Docker end-to-end Kafka data-flow tests.

These tests build the Docker image, start the container alongside a real
Kafka broker on a shared Docker network, and verify that CloudEvents
messages arrive on the expected topic.

Projects use plain (non-SASL) Kafka connections via either
``CONNECTION_STRING=BootstrapServer=host:port`` or
``KAFKA_BOOTSTRAP_SERVERS`` + ``KAFKA_TOPIC`` environment variables.

Run with:  pytest tests/docker_e2e/test_docker_kafka_flow.py -v --timeout=600
"""

import json
import os
import sys
import time

import pytest

_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

from helpers import (
    assert_cloudevents,
    build_image,
    run_container_detached,
    wait_for_container_logs,
    KafkaFixture,
)


# ---------------------------------------------------------------------------
# Fixtures
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


# ---------------------------------------------------------------------------
# CHMI Hydro
# ---------------------------------------------------------------------------

class TestCHMIHydroDockerFlow:
    """Build+run the chmi-hydro container and verify Kafka output."""

    TOPIC = 'test-chmi-hydro'

    def test_emits_cloudevents(self, kafka: KafkaFixture, chmi_image):
        """Container fetches live data and sends CloudEvents to Kafka."""
        kafka.create_topic(self.TOPIC)

        container = run_container_detached(
            chmi_image,
            environment={
                'CONNECTION_STRING': f'BootstrapServer={kafka.internal_address}',
                'KAFKA_TOPIC': self.TOPIC,
                'POLLING_INTERVAL': '5',
            },
        )

        try:
            # Wait for at least a few messages (ČHMÚ has hundreds of stations)
            messages = kafka.consume_messages(
                self.TOPIC,
                min_messages=5,
                timeout=180,
            )
            assert len(messages) >= 5, (
                f'Expected >=5 messages, got {len(messages)}.\n'
                f'Container logs:\n{container.logs().decode()}'
            )
            events = assert_cloudevents(messages)
            # All events should come from the ČHMÚ source
            for ev in events:
                assert 'chmi' in ev['source'].lower() or 'opendata.chmi.cz' in ev['source']
        finally:
            container.stop(timeout=5)
            container.remove(force=True)


# ---------------------------------------------------------------------------
# IMGW Hydro
# ---------------------------------------------------------------------------

class TestIMGWHydroDockerFlow:
    """Build+run the imgw-hydro container and verify Kafka output."""

    TOPIC = 'test-imgw-hydro'

    def test_emits_cloudevents(self, kafka: KafkaFixture, imgw_image):
        """Container fetches live data and sends CloudEvents to Kafka."""
        kafka.create_topic(self.TOPIC)

        container = run_container_detached(
            imgw_image,
            environment={
                'CONNECTION_STRING': f'BootstrapServer={kafka.internal_address}',
                'KAFKA_TOPIC': self.TOPIC,
                'POLLING_INTERVAL': '5',
            },
        )

        try:
            messages = kafka.consume_messages(
                self.TOPIC,
                min_messages=5,
                timeout=180,
            )
            assert len(messages) >= 5, (
                f'Expected >=5 messages, got {len(messages)}.\n'
                f'Container logs:\n{container.logs().decode()}'
            )
            events = assert_cloudevents(messages)
            for ev in events:
                assert 'imgw' in ev['source'].lower() or 'danepubliczne.imgw' in ev['source']
        finally:
            container.stop(timeout=5)
            container.remove(force=True)


# ---------------------------------------------------------------------------
# SMHI Hydro
# ---------------------------------------------------------------------------

class TestSMHIHydroDockerFlow:
    """Build+run the smhi-hydro container and verify Kafka output."""

    TOPIC = 'test-smhi-hydro'

    def test_emits_cloudevents(self, kafka: KafkaFixture, smhi_image):
        """Container fetches live data and sends CloudEvents to Kafka."""
        kafka.create_topic(self.TOPIC)

        container = run_container_detached(
            smhi_image,
            environment={
                'CONNECTION_STRING': f'BootstrapServer={kafka.internal_address}',
                'KAFKA_TOPIC': self.TOPIC,
                'POLLING_INTERVAL': '5',
            },
        )

        try:
            messages = kafka.consume_messages(
                self.TOPIC,
                min_messages=5,
                timeout=180,
            )
            assert len(messages) >= 5, (
                f'Expected >=5 messages, got {len(messages)}.\n'
                f'Container logs:\n{container.logs().decode()}'
            )
            events = assert_cloudevents(messages)
            for ev in events:
                assert 'smhi' in ev['source'].lower() or 'opendata-download-hydroobs' in ev['source']
        finally:
            container.stop(timeout=5)
            container.remove(force=True)


# ---------------------------------------------------------------------------
# Helper for projects using KAFKA_BOOTSTRAP_SERVERS + KAFKA_TOPIC
# ---------------------------------------------------------------------------

def _run_kafka_flow_test(kafka, image, topic, source_pattern, min_messages=1, timeout=180):
    """Run a Kafka flow test for a project using CONNECTION_STRING."""
    kafka.create_topic(topic)
    container = run_container_detached(
        image,
        environment={
            'CONNECTION_STRING': f'BootstrapServer={kafka.internal_address};EntityPath={topic}',
        },
    )
    try:
        messages = kafka.consume_messages(
            topic,
            min_messages=min_messages,
            timeout=timeout,
        )
        assert len(messages) >= min_messages, (
            f'Expected >={min_messages} messages, got {len(messages)}.\n'
            f'Container logs:\n{container.logs().decode()}'
        )
        events = assert_cloudevents(messages)
        for ev in events:
            assert any(p in ev['source'].lower() for p in source_pattern), (
                f'Unexpected source: {ev["source"]}'
            )
    finally:
        container.stop(timeout=5)
        container.remove(force=True)


# ---------------------------------------------------------------------------
# NOAA (Weather observations)
# ---------------------------------------------------------------------------

class TestNOAADockerFlow:
    TOPIC = 'test-noaa'

    def test_emits_cloudevents(self, kafka: KafkaFixture, noaa_image):
        _run_kafka_flow_test(kafka, noaa_image, self.TOPIC, ['noaa', 'weather.gov'])


# ---------------------------------------------------------------------------
# NOAA GOES (Space weather)
# ---------------------------------------------------------------------------

class TestNOAAGoesDockerFlow:
    TOPIC = 'test-noaa-goes'

    def test_emits_cloudevents(self, kafka: KafkaFixture, noaa_goes_image):
        _run_kafka_flow_test(kafka, noaa_goes_image, self.TOPIC, ['noaa', 'swpc'])


# ---------------------------------------------------------------------------
# NOAA NDBC (Buoy observations)
# ---------------------------------------------------------------------------

class TestNOAANdbcDockerFlow:
    TOPIC = 'test-noaa-ndbc'

    def test_emits_cloudevents(self, kafka: KafkaFixture, noaa_ndbc_image):
        _run_kafka_flow_test(kafka, noaa_ndbc_image, self.TOPIC, ['noaa', 'ndbc'])


# ---------------------------------------------------------------------------
# NOAA NWS (Weather alerts)
# ---------------------------------------------------------------------------

class TestNOAANwsDockerFlow:
    TOPIC = 'test-noaa-nws'

    def test_emits_cloudevents(self, kafka: KafkaFixture, noaa_nws_image):
        _run_kafka_flow_test(kafka, noaa_nws_image, self.TOPIC, ['noaa', 'nws', 'weather.gov'])


# ---------------------------------------------------------------------------
# USGS Instantaneous Values
# ---------------------------------------------------------------------------

class TestUSGSIVDockerFlow:
    TOPIC = 'test-usgs-iv'

    def test_emits_cloudevents(self, kafka: KafkaFixture, usgs_iv_image):
        _run_kafka_flow_test(kafka, usgs_iv_image, self.TOPIC, ['usgs'])


# ---------------------------------------------------------------------------
# USGS Earthquakes
# ---------------------------------------------------------------------------

class TestUSGSEarthquakesDockerFlow:
    TOPIC = 'test-usgs-earthquakes'

    def test_emits_cloudevents(self, kafka: KafkaFixture, usgs_earthquakes_image):
        _run_kafka_flow_test(kafka, usgs_earthquakes_image, self.TOPIC, ['usgs', 'earthquake'])


# ---------------------------------------------------------------------------
# Pegelonline (German water levels)
# ---------------------------------------------------------------------------

class TestPegelonlineDockerFlow:
    TOPIC = 'test-pegelonline'

    def test_emits_cloudevents(self, kafka: KafkaFixture, pegelonline_image):
        _run_kafka_flow_test(kafka, pegelonline_image, self.TOPIC, ['pegelonline', 'wsv'])


# ---------------------------------------------------------------------------
# Hub'Eau Hydrométrie (French water levels)
# ---------------------------------------------------------------------------

class TestHubeauDockerFlow:
    TOPIC = 'test-hubeau'

    def test_emits_cloudevents(self, kafka: KafkaFixture, hubeau_image):
        _run_kafka_flow_test(kafka, hubeau_image, self.TOPIC, ['hubeau', 'eaufrance'])


# ---------------------------------------------------------------------------
# UK Environment Agency Flood Monitoring
# ---------------------------------------------------------------------------

class TestUKEADockerFlow:
    TOPIC = 'test-uk-ea'

    def test_emits_cloudevents(self, kafka: KafkaFixture, uk_ea_image):
        _run_kafka_flow_test(kafka, uk_ea_image, self.TOPIC, ['environment.data.gov.uk', 'flood'])


# ---------------------------------------------------------------------------
# Rijkswaterstaat Waterwebservices (Dutch water levels)
# ---------------------------------------------------------------------------

class TestRWSDockerFlow:
    TOPIC = 'test-rws'

    def test_emits_cloudevents(self, kafka: KafkaFixture, rws_image):
        _run_kafka_flow_test(kafka, rws_image, self.TOPIC, ['rws', 'waterwebservices'])


# ---------------------------------------------------------------------------
# Waterinfo VMM (Flemish water levels)
# ---------------------------------------------------------------------------

class TestWaterinfoVMMDockerFlow:
    TOPIC = 'test-waterinfo-vmm'

    def test_emits_cloudevents(self, kafka: KafkaFixture, waterinfo_image):
        _run_kafka_flow_test(kafka, waterinfo_image, self.TOPIC, ['waterinfo', 'vmm'])
