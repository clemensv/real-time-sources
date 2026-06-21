
"""
This is sample code to produce events to Apache Kafka with the producer clients
contained in this project. You will still need to supply event data in the
marked
placews below before the program can be run.

The script gets the configuration from the command line or uses the environment
variables. The following environment variables are recognized:

- KAFKA_PRODUCER_CONFIG: The Kafka producer configuration.
- KAFKA_TOPICS: The Kafka topics to send events to.
- FABRIC_CONNECTION_STRING: A Microsoft Fabric or Azure Event Hubs connection
string.

Alternatively, you can pass the configuration as command-line arguments.

- `--producer-config`: The Kafka producer configuration.
- `--topics`: The Kafka topics to send events to.
- `-c` or `--connection-string`: The Microsoft Fabric or Azure Event Hubs
connection string.
"""

import argparse
import os
import asyncio
import json
import uuid
from typing import Optional
from datetime import datetime
from confluent_kafka import Producer as KafkaProducer

# imports the producer clients for the message group(s)

from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsAlertsEventProducer
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsZonesEventProducer
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsAlertsKafkaEventProducer
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsZonesKafkaEventProducer
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsAlertsMqttEventProducer
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsZonesMqttEventProducer
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsAlertsAmqpEventProducer
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsZonesAmqpEventProducer

# imports for the data classes for each event

from cap_alerts_producer_data import CapAlert
from cap_alerts_producer_data import CapZone

async def main(connection_string: Optional[str], producer_config: Optional[str], topic: Optional[str]):
    """
    Main function to produce events to Apache Kafka

    Args:
        connection_string (Optional[str]): The Fabric connection string
        producer_config (Optional[str]): The Kafka producer configuration
        topic (Optional[str]): The Kafka topic to send events to
    """
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_alerts_event_producer = OrgOasisCapAlertsAlertsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_alerts_event_producer = OrgOasisCapAlertsAlertsEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.CapAlert ----
    # TODO: Supply event data for the org.oasis.cap.alerts.CapAlert event
    _cap_alert = CapAlert()

    # sends the 'org.oasis.cap.alerts.CapAlert' event to Kafka topic.
    await org_oasis_cap_alerts_alerts_event_producer.send_org_oasis_cap_alerts_cap_alert(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _identifier = 'TODO: replace me', data = _cap_alert)
    print(f"Sent 'org.oasis.cap.alerts.CapAlert' event: {_cap_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_zones_event_producer = OrgOasisCapAlertsZonesEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_zones_event_producer = OrgOasisCapAlertsZonesEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.CapZone ----
    # TODO: Supply event data for the org.oasis.cap.alerts.CapZone event
    _cap_zone = CapZone()

    # sends the 'org.oasis.cap.alerts.CapZone' event to Kafka topic.
    await org_oasis_cap_alerts_zones_event_producer.send_org_oasis_cap_alerts_cap_zone(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _zone_id = 'TODO: replace me', data = _cap_zone)
    print(f"Sent 'org.oasis.cap.alerts.CapZone' event: {_cap_zone.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_alerts_kafka_event_producer = OrgOasisCapAlertsAlertsKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_alerts_kafka_event_producer = OrgOasisCapAlertsAlertsKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.kafka.CapAlert ----
    # TODO: Supply event data for the org.oasis.cap.alerts.kafka.CapAlert event
    _cap_alert = CapAlert()

    # sends the 'org.oasis.cap.alerts.kafka.CapAlert' event to Kafka topic.
    await org_oasis_cap_alerts_alerts_kafka_event_producer.send_org_oasis_cap_alerts_kafka_cap_alert(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _identifier = 'TODO: replace me', data = _cap_alert)
    print(f"Sent 'org.oasis.cap.alerts.kafka.CapAlert' event: {_cap_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_zones_kafka_event_producer = OrgOasisCapAlertsZonesKafkaEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_zones_kafka_event_producer = OrgOasisCapAlertsZonesKafkaEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.kafka.CapZone ----
    # TODO: Supply event data for the org.oasis.cap.alerts.kafka.CapZone event
    _cap_zone = CapZone()

    # sends the 'org.oasis.cap.alerts.kafka.CapZone' event to Kafka topic.
    await org_oasis_cap_alerts_zones_kafka_event_producer.send_org_oasis_cap_alerts_kafka_cap_zone(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _zone_id = 'TODO: replace me', data = _cap_zone)
    print(f"Sent 'org.oasis.cap.alerts.kafka.CapZone' event: {_cap_zone.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_alerts_mqtt_event_producer = OrgOasisCapAlertsAlertsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_alerts_mqtt_event_producer = OrgOasisCapAlertsAlertsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.mqtt.CapAlert ----
    # TODO: Supply event data for the org.oasis.cap.alerts.mqtt.CapAlert event
    _cap_alert = CapAlert()

    # sends the 'org.oasis.cap.alerts.mqtt.CapAlert' event to Kafka topic.
    await org_oasis_cap_alerts_alerts_mqtt_event_producer.send_org_oasis_cap_alerts_mqtt_cap_alert(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _identifier = 'TODO: replace me', data = _cap_alert)
    print(f"Sent 'org.oasis.cap.alerts.mqtt.CapAlert' event: {_cap_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_zones_mqtt_event_producer = OrgOasisCapAlertsZonesMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_zones_mqtt_event_producer = OrgOasisCapAlertsZonesMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.mqtt.CapZone ----
    # TODO: Supply event data for the org.oasis.cap.alerts.mqtt.CapZone event
    _cap_zone = CapZone()

    # sends the 'org.oasis.cap.alerts.mqtt.CapZone' event to Kafka topic.
    await org_oasis_cap_alerts_zones_mqtt_event_producer.send_org_oasis_cap_alerts_mqtt_cap_zone(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _zone_id = 'TODO: replace me', data = _cap_zone)
    print(f"Sent 'org.oasis.cap.alerts.mqtt.CapZone' event: {_cap_zone.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_alerts_amqp_event_producer = OrgOasisCapAlertsAlertsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_alerts_amqp_event_producer = OrgOasisCapAlertsAlertsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.amqp.CapAlert ----
    # TODO: Supply event data for the org.oasis.cap.alerts.amqp.CapAlert event
    _cap_alert = CapAlert()

    # sends the 'org.oasis.cap.alerts.amqp.CapAlert' event to Kafka topic.
    await org_oasis_cap_alerts_alerts_amqp_event_producer.send_org_oasis_cap_alerts_amqp_cap_alert(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _identifier = 'TODO: replace me', data = _cap_alert)
    print(f"Sent 'org.oasis.cap.alerts.amqp.CapAlert' event: {_cap_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_oasis_cap_alerts_zones_amqp_event_producer = OrgOasisCapAlertsZonesAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_oasis_cap_alerts_zones_amqp_event_producer = OrgOasisCapAlertsZonesAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.oasis.cap.alerts.amqp.CapZone ----
    # TODO: Supply event data for the org.oasis.cap.alerts.amqp.CapZone event
    _cap_zone = CapZone()

    # sends the 'org.oasis.cap.alerts.amqp.CapZone' event to Kafka topic.
    await org_oasis_cap_alerts_zones_amqp_event_producer.send_org_oasis_cap_alerts_amqp_cap_zone(_provider_url = 'TODO: replace me', _cap_source_id = 'TODO: replace me', _zone_id = 'TODO: replace me', data = _cap_zone)
    print(f"Sent 'org.oasis.cap.alerts.amqp.CapZone' event: {_cap_zone.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c', '--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))