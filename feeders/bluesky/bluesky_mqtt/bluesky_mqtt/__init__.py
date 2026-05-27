"""Bluesky AT Protocol firehose -> MQTT/UNS bridge.

Non-retained, QoS-0 publishing into the UNS topic family
`social/intl/bluesky/bluesky/{collection}/{lang}/{did}/{event}`.

This sibling package re-uses the upstream connection / record-parsing logic
from the legacy ``bluesky`` Kafka package and republishes the events as
MQTT-5 binary-mode CloudEvents.
"""
