
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

from datex2_producer_kafka_producer.producer import OrgDatex2MeasuredEventProducer
from datex2_producer_kafka_producer.producer import OrgDatex2SituationEventProducer
from datex2_producer_kafka_producer.producer import OrgDatex2MeasuredMqttEventProducer
from datex2_producer_kafka_producer.producer import OrgDatex2SituationMqttEventProducer
from datex2_producer_kafka_producer.producer import OrgDatex2SituationAmqpEventProducer
from datex2_producer_kafka_producer.producer import OrgDatex2MeasuredSiteAmqpEventProducer
from datex2_producer_kafka_producer.producer import OrgDatex2TrafficMeasurementAmqpEventProducer

# imports for the data classes for each event

from datex2_producer_data import MeasurementSite
from datex2_producer_data import TrafficMeasurement
from datex2_producer_data import SituationRecord

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
        org_datex2_measured_event_producer = OrgDatex2MeasuredEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_datex2_measured_event_producer = OrgDatex2MeasuredEventProducer(kafka_producer, topic, 'binary')

    # ---- org.datex2.measured.MeasurementSite ----
    # TODO: Supply event data for the org.datex2.measured.MeasurementSite event
    _measurement_site = MeasurementSite()

    # sends the 'org.datex2.measured.MeasurementSite' event to Kafka topic.
    await org_datex2_measured_event_producer.send_org_datex2_measured_measurement_site(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _measurement_site_id = 'TODO: replace me', data = _measurement_site)
    print(f"Sent 'org.datex2.measured.MeasurementSite' event: {_measurement_site.to_json()}")

    # ---- org.datex2.measured.TrafficMeasurement ----
    # TODO: Supply event data for the org.datex2.measured.TrafficMeasurement event
    _traffic_measurement = TrafficMeasurement()

    # sends the 'org.datex2.measured.TrafficMeasurement' event to Kafka topic.
    await org_datex2_measured_event_producer.send_org_datex2_measured_traffic_measurement(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _measurement_site_id = 'TODO: replace me', data = _traffic_measurement)
    print(f"Sent 'org.datex2.measured.TrafficMeasurement' event: {_traffic_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_datex2_situation_event_producer = OrgDatex2SituationEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_datex2_situation_event_producer = OrgDatex2SituationEventProducer(kafka_producer, topic, 'binary')

    # ---- org.datex2.situation.SituationRecord ----
    # TODO: Supply event data for the org.datex2.situation.SituationRecord event
    _situation_record = SituationRecord()

    # sends the 'org.datex2.situation.SituationRecord' event to Kafka topic.
    await org_datex2_situation_event_producer.send_org_datex2_situation_situation_record(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _situation_record_id = 'TODO: replace me', data = _situation_record)
    print(f"Sent 'org.datex2.situation.SituationRecord' event: {_situation_record.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_datex2_measured_mqtt_event_producer = OrgDatex2MeasuredMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_datex2_measured_mqtt_event_producer = OrgDatex2MeasuredMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.datex2.measured.MeasurementSite.mqtt ----
    # TODO: Supply event data for the org.datex2.measured.MeasurementSite.mqtt event
    _measurement_site = MeasurementSite()

    # sends the 'org.datex2.measured.MeasurementSite.mqtt' event to Kafka topic.
    await org_datex2_measured_mqtt_event_producer.send_org_datex2_measured_measurement_site_mqtt(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _measurement_site_id = 'TODO: replace me', data = _measurement_site)
    print(f"Sent 'org.datex2.measured.MeasurementSite.mqtt' event: {_measurement_site.to_json()}")

    # ---- org.datex2.measured.TrafficMeasurement.mqtt ----
    # TODO: Supply event data for the org.datex2.measured.TrafficMeasurement.mqtt event
    _traffic_measurement = TrafficMeasurement()

    # sends the 'org.datex2.measured.TrafficMeasurement.mqtt' event to Kafka topic.
    await org_datex2_measured_mqtt_event_producer.send_org_datex2_measured_traffic_measurement_mqtt(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _measurement_site_id = 'TODO: replace me', data = _traffic_measurement)
    print(f"Sent 'org.datex2.measured.TrafficMeasurement.mqtt' event: {_traffic_measurement.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_datex2_situation_mqtt_event_producer = OrgDatex2SituationMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_datex2_situation_mqtt_event_producer = OrgDatex2SituationMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- org.datex2.situation.SituationRecord.mqtt ----
    # TODO: Supply event data for the org.datex2.situation.SituationRecord.mqtt event
    _situation_record = SituationRecord()

    # sends the 'org.datex2.situation.SituationRecord.mqtt' event to Kafka topic.
    await org_datex2_situation_mqtt_event_producer.send_org_datex2_situation_situation_record_mqtt(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _situation_record_id = 'TODO: replace me', data = _situation_record)
    print(f"Sent 'org.datex2.situation.SituationRecord.mqtt' event: {_situation_record.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_datex2_situation_amqp_event_producer = OrgDatex2SituationAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_datex2_situation_amqp_event_producer = OrgDatex2SituationAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.datex2.situation.SituationRecord.amqp ----
    # TODO: Supply event data for the org.datex2.situation.SituationRecord.amqp event
    _situation_record = SituationRecord()

    # sends the 'org.datex2.situation.SituationRecord.amqp' event to Kafka topic.
    await org_datex2_situation_amqp_event_producer.send_org_datex2_situation_situation_record_amqp(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _situation_record_id = 'TODO: replace me', data = _situation_record)
    print(f"Sent 'org.datex2.situation.SituationRecord.amqp' event: {_situation_record.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_datex2_measured_site_amqp_event_producer = OrgDatex2MeasuredSiteAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_datex2_measured_site_amqp_event_producer = OrgDatex2MeasuredSiteAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.datex2.measured.MeasurementSite.amqp ----
    # TODO: Supply event data for the org.datex2.measured.MeasurementSite.amqp event
    _measurement_site = MeasurementSite()

    # sends the 'org.datex2.measured.MeasurementSite.amqp' event to Kafka topic.
    await org_datex2_measured_site_amqp_event_producer.send_org_datex2_measured_measurement_site_amqp(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _measurement_site_id = 'TODO: replace me', data = _measurement_site)
    print(f"Sent 'org.datex2.measured.MeasurementSite.amqp' event: {_measurement_site.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        org_datex2_traffic_measurement_amqp_event_producer = OrgDatex2TrafficMeasurementAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        org_datex2_traffic_measurement_amqp_event_producer = OrgDatex2TrafficMeasurementAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- org.datex2.measured.TrafficMeasurement.amqp ----
    # TODO: Supply event data for the org.datex2.measured.TrafficMeasurement.amqp event
    _traffic_measurement = TrafficMeasurement()

    # sends the 'org.datex2.measured.TrafficMeasurement.amqp' event to Kafka topic.
    await org_datex2_traffic_measurement_amqp_event_producer.send_org_datex2_measured_traffic_measurement_amqp(_feed_url = 'TODO: replace me', _supplier_id = 'TODO: replace me', _measurement_site_id = 'TODO: replace me', data = _traffic_measurement)
    print(f"Sent 'org.datex2.measured.TrafficMeasurement.amqp' event: {_traffic_measurement.to_json()}")

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