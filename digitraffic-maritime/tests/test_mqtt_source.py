"""Tests for the MQTT source."""

import json
from unittest.mock import MagicMock, patch

from digitraffic_maritime.mqtt_source import (
    MQTTSource, DIGITRAFFIC_MQTT_HOST, DIGITRAFFIC_MQTT_PORT,
    TOPIC_LOCATION, TOPIC_METADATA,
)


class TestTopicBuilding:
    def test_default_subscribes_both(self):
        src = MQTTSource()
        topics = src._get_topics()
        assert TOPIC_LOCATION in topics
        assert TOPIC_METADATA in topics
        assert len(topics) == 2

    def test_location_only(self):
        src = MQTTSource(subscribe_locations=True, subscribe_metadata=False)
        topics = src._get_topics()
        assert topics == [TOPIC_LOCATION]

    def test_metadata_only(self):
        src = MQTTSource(subscribe_locations=False, subscribe_metadata=True)
        topics = src._get_topics()
        assert topics == [TOPIC_METADATA]

    def test_mmsi_filter_creates_specific_topics(self):
        src = MQTTSource(mmsi_filter={230629000, 219598000})
        topics = src._get_topics()
        assert "vessels-v2/230629000/location" in topics
        assert "vessels-v2/230629000/metadata" in topics
        assert "vessels-v2/219598000/location" in topics
        assert "vessels-v2/219598000/metadata" in topics
        assert len(topics) == 4

    def test_mmsi_filter_location_only(self):
        src = MQTTSource(
            subscribe_locations=True, subscribe_metadata=False,
            mmsi_filter={230629000},
        )
        topics = src._get_topics()
        assert topics == ["vessels-v2/230629000/location"]

    def test_default_host_and_port(self):
        src = MQTTSource()
        assert src.host == DIGITRAFFIC_MQTT_HOST
        assert src.port == DIGITRAFFIC_MQTT_PORT
