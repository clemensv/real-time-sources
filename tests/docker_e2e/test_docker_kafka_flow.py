"""Docker end-to-end Kafka data-flow tests.

These tests build the Docker image, start the container alongside a real
Kafka broker on a shared Docker network, and verify that CloudEvents
messages arrive on the expected topic.

Only projects that support plain (non-SASL) Kafka connections are
included here.  These projects accept a ``CONNECTION_STRING`` of the
form ``BootstrapServer=host:port`` which configures the Kafka producer
without TLS or SASL.

Projects tested:
- chmi-hydro  (Czech Hydrometeorological Institute – water levels)
- imgw-hydro  (Polish IMGW – water levels)
- smhi-hydro  (Swedish SMHI – water levels)

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
