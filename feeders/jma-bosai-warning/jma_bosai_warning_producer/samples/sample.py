
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

from jma_bosai_warning_producer_kafka_producer.producer import JPJMAWarningEventProducer
from jma_bosai_warning_producer_kafka_producer.producer import JPJMATsunamiEventProducer
from jma_bosai_warning_producer_kafka_producer.producer import JPJMAWarningMqttEventProducer
from jma_bosai_warning_producer_kafka_producer.producer import JPJMAWarningAmqpEventProducer

# imports for the data classes for each event

from jma_bosai_warning_producer_data.office import Office
from jma_bosai_warning_producer_data.weatherwarning import WeatherWarning
from jma_bosai_warning_producer_data.tsunamialert import TsunamiAlert

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
        jpjmawarning_event_producer = JPJMAWarningEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpjmawarning_event_producer = JPJMAWarningEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.JMA.Warning.Office ----
    # TODO: Supply event data for the JP.JMA.Warning.Office event
    _office = Office()

    # sends the 'JP.JMA.Warning.Office' event to Kafka topic.
    await jpjmawarning_event_producer.send_jp_jma_warning_office(_feedurl = 'TODO: replace me', _office_code = 'TODO: replace me', _area_code = 'TODO: replace me', data = _office)
    print(f"Sent 'JP.JMA.Warning.Office' event: {_office.to_json()}")

    # ---- JP.JMA.Warning.WeatherWarning ----
    # TODO: Supply event data for the JP.JMA.Warning.WeatherWarning event
    _weather_warning = WeatherWarning()

    # sends the 'JP.JMA.Warning.WeatherWarning' event to Kafka topic.
    await jpjmawarning_event_producer.send_jp_jma_warning_weather_warning(_feedurl = 'TODO: replace me', _office_code = 'TODO: replace me', _area_code = 'TODO: replace me', data = _weather_warning)
    print(f"Sent 'JP.JMA.Warning.WeatherWarning' event: {_weather_warning.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpjmatsunami_event_producer = JPJMATsunamiEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpjmatsunami_event_producer = JPJMATsunamiEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.JMA.Tsunami.TsunamiAlert ----
    # TODO: Supply event data for the JP.JMA.Tsunami.TsunamiAlert event
    _tsunami_alert = TsunamiAlert()

    # sends the 'JP.JMA.Tsunami.TsunamiAlert' event to Kafka topic.
    await jpjmatsunami_event_producer.send_jp_jma_tsunami_tsunami_alert(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', _serial = 'TODO: replace me', data = _tsunami_alert)
    print(f"Sent 'JP.JMA.Tsunami.TsunamiAlert' event: {_tsunami_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpjmawarning_mqtt_event_producer = JPJMAWarningMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpjmawarning_mqtt_event_producer = JPJMAWarningMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.JMA.Warning.mqtt.Office ----
    # TODO: Supply event data for the JP.JMA.Warning.mqtt.Office event
    _office = Office()

    # sends the 'JP.JMA.Warning.mqtt.Office' event to Kafka topic.
    await jpjmawarning_mqtt_event_producer.send_jp_jma_warning_mqtt_office(_feedurl = 'TODO: replace me', _office_code = 'TODO: replace me', _area_code = 'TODO: replace me', data = _office)
    print(f"Sent 'JP.JMA.Warning.mqtt.Office' event: {_office.to_json()}")

    # ---- JP.JMA.Warning.mqtt.WeatherWarning ----
    # TODO: Supply event data for the JP.JMA.Warning.mqtt.WeatherWarning event
    _weather_warning = WeatherWarning()

    # sends the 'JP.JMA.Warning.mqtt.WeatherWarning' event to Kafka topic.
    await jpjmawarning_mqtt_event_producer.send_jp_jma_warning_mqtt_weather_warning(_feedurl = 'TODO: replace me', _office_code = 'TODO: replace me', _area_code = 'TODO: replace me', data = _weather_warning)
    print(f"Sent 'JP.JMA.Warning.mqtt.WeatherWarning' event: {_weather_warning.to_json()}")

    # ---- JP.JMA.Warning.mqtt.TsunamiAlert ----
    # TODO: Supply event data for the JP.JMA.Warning.mqtt.TsunamiAlert event
    _tsunami_alert = TsunamiAlert()

    # sends the 'JP.JMA.Warning.mqtt.TsunamiAlert' event to Kafka topic.
    await jpjmawarning_mqtt_event_producer.send_jp_jma_warning_mqtt_tsunami_alert(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', _serial = 'TODO: replace me', data = _tsunami_alert)
    print(f"Sent 'JP.JMA.Warning.mqtt.TsunamiAlert' event: {_tsunami_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        jpjmawarning_amqp_event_producer = JPJMAWarningAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        jpjmawarning_amqp_event_producer = JPJMAWarningAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- JP.JMA.Warning.amqp.Office ----
    # TODO: Supply event data for the JP.JMA.Warning.amqp.Office event
    _office = Office()

    # sends the 'JP.JMA.Warning.amqp.Office' event to Kafka topic.
    await jpjmawarning_amqp_event_producer.send_jp_jma_warning_amqp_office(_feedurl = 'TODO: replace me', _office_code = 'TODO: replace me', _area_code = 'TODO: replace me', data = _office)
    print(f"Sent 'JP.JMA.Warning.amqp.Office' event: {_office.to_json()}")

    # ---- JP.JMA.Warning.amqp.WeatherWarning ----
    # TODO: Supply event data for the JP.JMA.Warning.amqp.WeatherWarning event
    _weather_warning = WeatherWarning()

    # sends the 'JP.JMA.Warning.amqp.WeatherWarning' event to Kafka topic.
    await jpjmawarning_amqp_event_producer.send_jp_jma_warning_amqp_weather_warning(_feedurl = 'TODO: replace me', _office_code = 'TODO: replace me', _area_code = 'TODO: replace me', data = _weather_warning)
    print(f"Sent 'JP.JMA.Warning.amqp.WeatherWarning' event: {_weather_warning.to_json()}")

    # ---- JP.JMA.Warning.amqp.TsunamiAlert ----
    # TODO: Supply event data for the JP.JMA.Warning.amqp.TsunamiAlert event
    _tsunami_alert = TsunamiAlert()

    # sends the 'JP.JMA.Warning.amqp.TsunamiAlert' event to Kafka topic.
    await jpjmawarning_amqp_event_producer.send_jp_jma_warning_amqp_tsunami_alert(_feedurl = 'TODO: replace me', _event_id = 'TODO: replace me', _serial = 'TODO: replace me', data = _tsunami_alert)
    print(f"Sent 'JP.JMA.Warning.amqp.TsunamiAlert' event: {_tsunami_alert.to_json()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument('--producer-config', default=os.getenv('KAFKA_PRODUCER_CONFIG'), help='Kafka producer config (JSON)', required=False)
    parser.add_argument('--topics', default=os.getenv('KAFKA_TOPICS'), help='Kafka topics to send events to', required=False)
    parser.add_argument('-c|--connection-string', dest='connection_string', default=os.getenv('FABRIC_CONNECTION_STRING'), help='Fabric connection string', required=False)

    args = parser.parse_args()

    asyncio.run(main(
        args.connection_string,
        args.producer_config,
        args.topics
    ))