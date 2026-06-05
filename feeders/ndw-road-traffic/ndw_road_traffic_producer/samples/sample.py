
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

from ndw_road_traffic_producer_kafka_producer.producer import NLNDWAVGEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWDRIPEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWMSIEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWSituationsEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWAVGMqttEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWDRIPMqttEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWMSIMqttEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWSituationsMqttEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWAVGAmqpEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWDRIPAmqpEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWMSIAmqpEventProducer
from ndw_road_traffic_producer_kafka_producer.producer import NLNDWSituationsAmqpEventProducer

# imports for the data classes for each event

from ndw_road_traffic_producer_data import PointMeasurementSite
from ndw_road_traffic_producer_data import RouteMeasurementSite
from ndw_road_traffic_producer_data import TrafficObservation
from ndw_road_traffic_producer_data import TravelTimeObservation
from ndw_road_traffic_producer_data import DripSign
from ndw_road_traffic_producer_data import DripDisplayState
from ndw_road_traffic_producer_data import MsiSign
from ndw_road_traffic_producer_data import MsiDisplayState
from ndw_road_traffic_producer_data import Roadwork
from ndw_road_traffic_producer_data import BridgeOpening
from ndw_road_traffic_producer_data import TemporaryClosure
from ndw_road_traffic_producer_data import TemporarySpeedLimit
from ndw_road_traffic_producer_data import SafetyRelatedMessage

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
        nlndwavgevent_producer = NLNDWAVGEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwavgevent_producer = NLNDWAVGEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.AVG.PointMeasurementSite ----
    # TODO: Supply event data for the NL.NDW.AVG.PointMeasurementSite event
    _point_measurement_site = PointMeasurementSite()

    # sends the 'NL.NDW.AVG.PointMeasurementSite' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_point_measurement_site(_measurement_site_id = 'TODO: replace me', data = _point_measurement_site)
    print(f"Sent 'NL.NDW.AVG.PointMeasurementSite' event: {_point_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.RouteMeasurementSite ----
    # TODO: Supply event data for the NL.NDW.AVG.RouteMeasurementSite event
    _route_measurement_site = RouteMeasurementSite()

    # sends the 'NL.NDW.AVG.RouteMeasurementSite' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_route_measurement_site(_measurement_site_id = 'TODO: replace me', data = _route_measurement_site)
    print(f"Sent 'NL.NDW.AVG.RouteMeasurementSite' event: {_route_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.TrafficObservation ----
    # TODO: Supply event data for the NL.NDW.AVG.TrafficObservation event
    _traffic_observation = TrafficObservation()

    # sends the 'NL.NDW.AVG.TrafficObservation' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_traffic_observation(_measurement_site_id = 'TODO: replace me', data = _traffic_observation)
    print(f"Sent 'NL.NDW.AVG.TrafficObservation' event: {_traffic_observation.to_json()}")

    # ---- NL.NDW.AVG.TravelTimeObservation ----
    # TODO: Supply event data for the NL.NDW.AVG.TravelTimeObservation event
    _travel_time_observation = TravelTimeObservation()

    # sends the 'NL.NDW.AVG.TravelTimeObservation' event to Kafka topic.
    await nlndwavgevent_producer.send_nl_ndw_avg_travel_time_observation(_measurement_site_id = 'TODO: replace me', data = _travel_time_observation)
    print(f"Sent 'NL.NDW.AVG.TravelTimeObservation' event: {_travel_time_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwdripevent_producer = NLNDWDRIPEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwdripevent_producer = NLNDWDRIPEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.DRIP.DripSign ----
    # TODO: Supply event data for the NL.NDW.DRIP.DripSign event
    _drip_sign = DripSign()

    # sends the 'NL.NDW.DRIP.DripSign' event to Kafka topic.
    await nlndwdripevent_producer.send_nl_ndw_drip_drip_sign(_vms_controller_id = 'TODO: replace me', _vms_index = 'TODO: replace me', data = _drip_sign)
    print(f"Sent 'NL.NDW.DRIP.DripSign' event: {_drip_sign.to_json()}")

    # ---- NL.NDW.DRIP.DripDisplayState ----
    # TODO: Supply event data for the NL.NDW.DRIP.DripDisplayState event
    _drip_display_state = DripDisplayState()

    # sends the 'NL.NDW.DRIP.DripDisplayState' event to Kafka topic.
    await nlndwdripevent_producer.send_nl_ndw_drip_drip_display_state(_vms_controller_id = 'TODO: replace me', _vms_index = 'TODO: replace me', data = _drip_display_state)
    print(f"Sent 'NL.NDW.DRIP.DripDisplayState' event: {_drip_display_state.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwmsievent_producer = NLNDWMSIEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwmsievent_producer = NLNDWMSIEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.MSI.MsiSign ----
    # TODO: Supply event data for the NL.NDW.MSI.MsiSign event
    _msi_sign = MsiSign()

    # sends the 'NL.NDW.MSI.MsiSign' event to Kafka topic.
    await nlndwmsievent_producer.send_nl_ndw_msi_msi_sign(_sign_id = 'TODO: replace me', data = _msi_sign)
    print(f"Sent 'NL.NDW.MSI.MsiSign' event: {_msi_sign.to_json()}")

    # ---- NL.NDW.MSI.MsiDisplayState ----
    # TODO: Supply event data for the NL.NDW.MSI.MsiDisplayState event
    _msi_display_state = MsiDisplayState()

    # sends the 'NL.NDW.MSI.MsiDisplayState' event to Kafka topic.
    await nlndwmsievent_producer.send_nl_ndw_msi_msi_display_state(_sign_id = 'TODO: replace me', data = _msi_display_state)
    print(f"Sent 'NL.NDW.MSI.MsiDisplayState' event: {_msi_display_state.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwsituations_event_producer = NLNDWSituationsEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwsituations_event_producer = NLNDWSituationsEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Situations.Roadwork ----
    # TODO: Supply event data for the NL.NDW.Situations.Roadwork event
    _roadwork = Roadwork()

    # sends the 'NL.NDW.Situations.Roadwork' event to Kafka topic.
    await nlndwsituations_event_producer.send_nl_ndw_situations_roadwork(_situation_record_id = 'TODO: replace me', data = _roadwork)
    print(f"Sent 'NL.NDW.Situations.Roadwork' event: {_roadwork.to_json()}")

    # ---- NL.NDW.Situations.BridgeOpening ----
    # TODO: Supply event data for the NL.NDW.Situations.BridgeOpening event
    _bridge_opening = BridgeOpening()

    # sends the 'NL.NDW.Situations.BridgeOpening' event to Kafka topic.
    await nlndwsituations_event_producer.send_nl_ndw_situations_bridge_opening(_situation_record_id = 'TODO: replace me', data = _bridge_opening)
    print(f"Sent 'NL.NDW.Situations.BridgeOpening' event: {_bridge_opening.to_json()}")

    # ---- NL.NDW.Situations.TemporaryClosure ----
    # TODO: Supply event data for the NL.NDW.Situations.TemporaryClosure event
    _temporary_closure = TemporaryClosure()

    # sends the 'NL.NDW.Situations.TemporaryClosure' event to Kafka topic.
    await nlndwsituations_event_producer.send_nl_ndw_situations_temporary_closure(_situation_record_id = 'TODO: replace me', data = _temporary_closure)
    print(f"Sent 'NL.NDW.Situations.TemporaryClosure' event: {_temporary_closure.to_json()}")

    # ---- NL.NDW.Situations.TemporarySpeedLimit ----
    # TODO: Supply event data for the NL.NDW.Situations.TemporarySpeedLimit event
    _temporary_speed_limit = TemporarySpeedLimit()

    # sends the 'NL.NDW.Situations.TemporarySpeedLimit' event to Kafka topic.
    await nlndwsituations_event_producer.send_nl_ndw_situations_temporary_speed_limit(_situation_record_id = 'TODO: replace me', data = _temporary_speed_limit)
    print(f"Sent 'NL.NDW.Situations.TemporarySpeedLimit' event: {_temporary_speed_limit.to_json()}")

    # ---- NL.NDW.Situations.SafetyRelatedMessage ----
    # TODO: Supply event data for the NL.NDW.Situations.SafetyRelatedMessage event
    _safety_related_message = SafetyRelatedMessage()

    # sends the 'NL.NDW.Situations.SafetyRelatedMessage' event to Kafka topic.
    await nlndwsituations_event_producer.send_nl_ndw_situations_safety_related_message(_situation_record_id = 'TODO: replace me', data = _safety_related_message)
    print(f"Sent 'NL.NDW.Situations.SafetyRelatedMessage' event: {_safety_related_message.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwavgmqtt_event_producer = NLNDWAVGMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwavgmqtt_event_producer = NLNDWAVGMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.AVG.PointMeasurementSite.mqtt ----
    # TODO: Supply event data for the NL.NDW.AVG.PointMeasurementSite.mqtt event
    _point_measurement_site = PointMeasurementSite()

    # sends the 'NL.NDW.AVG.PointMeasurementSite.mqtt' event to Kafka topic.
    await nlndwavgmqtt_event_producer.send_nl_ndw_avg_point_measurement_site_mqtt(_measurement_site_id = 'TODO: replace me', data = _point_measurement_site)
    print(f"Sent 'NL.NDW.AVG.PointMeasurementSite.mqtt' event: {_point_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.RouteMeasurementSite.mqtt ----
    # TODO: Supply event data for the NL.NDW.AVG.RouteMeasurementSite.mqtt event
    _route_measurement_site = RouteMeasurementSite()

    # sends the 'NL.NDW.AVG.RouteMeasurementSite.mqtt' event to Kafka topic.
    await nlndwavgmqtt_event_producer.send_nl_ndw_avg_route_measurement_site_mqtt(_measurement_site_id = 'TODO: replace me', data = _route_measurement_site)
    print(f"Sent 'NL.NDW.AVG.RouteMeasurementSite.mqtt' event: {_route_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.TrafficObservation.mqtt ----
    # TODO: Supply event data for the NL.NDW.AVG.TrafficObservation.mqtt event
    _traffic_observation = TrafficObservation()

    # sends the 'NL.NDW.AVG.TrafficObservation.mqtt' event to Kafka topic.
    await nlndwavgmqtt_event_producer.send_nl_ndw_avg_traffic_observation_mqtt(_measurement_site_id = 'TODO: replace me', data = _traffic_observation)
    print(f"Sent 'NL.NDW.AVG.TrafficObservation.mqtt' event: {_traffic_observation.to_json()}")

    # ---- NL.NDW.AVG.TravelTimeObservation.mqtt ----
    # TODO: Supply event data for the NL.NDW.AVG.TravelTimeObservation.mqtt event
    _travel_time_observation = TravelTimeObservation()

    # sends the 'NL.NDW.AVG.TravelTimeObservation.mqtt' event to Kafka topic.
    await nlndwavgmqtt_event_producer.send_nl_ndw_avg_travel_time_observation_mqtt(_measurement_site_id = 'TODO: replace me', data = _travel_time_observation)
    print(f"Sent 'NL.NDW.AVG.TravelTimeObservation.mqtt' event: {_travel_time_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwdripmqtt_event_producer = NLNDWDRIPMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwdripmqtt_event_producer = NLNDWDRIPMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.DRIP.DripSign.mqtt ----
    # TODO: Supply event data for the NL.NDW.DRIP.DripSign.mqtt event
    _drip_sign = DripSign()

    # sends the 'NL.NDW.DRIP.DripSign.mqtt' event to Kafka topic.
    await nlndwdripmqtt_event_producer.send_nl_ndw_drip_drip_sign_mqtt(_vms_controller_id = 'TODO: replace me', _vms_index = 'TODO: replace me', data = _drip_sign)
    print(f"Sent 'NL.NDW.DRIP.DripSign.mqtt' event: {_drip_sign.to_json()}")

    # ---- NL.NDW.DRIP.DripDisplayState.mqtt ----
    # TODO: Supply event data for the NL.NDW.DRIP.DripDisplayState.mqtt event
    _drip_display_state = DripDisplayState()

    # sends the 'NL.NDW.DRIP.DripDisplayState.mqtt' event to Kafka topic.
    await nlndwdripmqtt_event_producer.send_nl_ndw_drip_drip_display_state_mqtt(_vms_controller_id = 'TODO: replace me', _vms_index = 'TODO: replace me', data = _drip_display_state)
    print(f"Sent 'NL.NDW.DRIP.DripDisplayState.mqtt' event: {_drip_display_state.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwmsimqtt_event_producer = NLNDWMSIMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwmsimqtt_event_producer = NLNDWMSIMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.MSI.MsiSign.mqtt ----
    # TODO: Supply event data for the NL.NDW.MSI.MsiSign.mqtt event
    _msi_sign = MsiSign()

    # sends the 'NL.NDW.MSI.MsiSign.mqtt' event to Kafka topic.
    await nlndwmsimqtt_event_producer.send_nl_ndw_msi_msi_sign_mqtt(_sign_id = 'TODO: replace me', data = _msi_sign)
    print(f"Sent 'NL.NDW.MSI.MsiSign.mqtt' event: {_msi_sign.to_json()}")

    # ---- NL.NDW.MSI.MsiDisplayState.mqtt ----
    # TODO: Supply event data for the NL.NDW.MSI.MsiDisplayState.mqtt event
    _msi_display_state = MsiDisplayState()

    # sends the 'NL.NDW.MSI.MsiDisplayState.mqtt' event to Kafka topic.
    await nlndwmsimqtt_event_producer.send_nl_ndw_msi_msi_display_state_mqtt(_sign_id = 'TODO: replace me', data = _msi_display_state)
    print(f"Sent 'NL.NDW.MSI.MsiDisplayState.mqtt' event: {_msi_display_state.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwsituations_mqtt_event_producer = NLNDWSituationsMqttEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwsituations_mqtt_event_producer = NLNDWSituationsMqttEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Situations.Roadwork.mqtt ----
    # TODO: Supply event data for the NL.NDW.Situations.Roadwork.mqtt event
    _roadwork = Roadwork()

    # sends the 'NL.NDW.Situations.Roadwork.mqtt' event to Kafka topic.
    await nlndwsituations_mqtt_event_producer.send_nl_ndw_situations_roadwork_mqtt(_situation_record_id = 'TODO: replace me', data = _roadwork)
    print(f"Sent 'NL.NDW.Situations.Roadwork.mqtt' event: {_roadwork.to_json()}")

    # ---- NL.NDW.Situations.BridgeOpening.mqtt ----
    # TODO: Supply event data for the NL.NDW.Situations.BridgeOpening.mqtt event
    _bridge_opening = BridgeOpening()

    # sends the 'NL.NDW.Situations.BridgeOpening.mqtt' event to Kafka topic.
    await nlndwsituations_mqtt_event_producer.send_nl_ndw_situations_bridge_opening_mqtt(_situation_record_id = 'TODO: replace me', data = _bridge_opening)
    print(f"Sent 'NL.NDW.Situations.BridgeOpening.mqtt' event: {_bridge_opening.to_json()}")

    # ---- NL.NDW.Situations.TemporaryClosure.mqtt ----
    # TODO: Supply event data for the NL.NDW.Situations.TemporaryClosure.mqtt event
    _temporary_closure = TemporaryClosure()

    # sends the 'NL.NDW.Situations.TemporaryClosure.mqtt' event to Kafka topic.
    await nlndwsituations_mqtt_event_producer.send_nl_ndw_situations_temporary_closure_mqtt(_situation_record_id = 'TODO: replace me', data = _temporary_closure)
    print(f"Sent 'NL.NDW.Situations.TemporaryClosure.mqtt' event: {_temporary_closure.to_json()}")

    # ---- NL.NDW.Situations.TemporarySpeedLimit.mqtt ----
    # TODO: Supply event data for the NL.NDW.Situations.TemporarySpeedLimit.mqtt event
    _temporary_speed_limit = TemporarySpeedLimit()

    # sends the 'NL.NDW.Situations.TemporarySpeedLimit.mqtt' event to Kafka topic.
    await nlndwsituations_mqtt_event_producer.send_nl_ndw_situations_temporary_speed_limit_mqtt(_situation_record_id = 'TODO: replace me', data = _temporary_speed_limit)
    print(f"Sent 'NL.NDW.Situations.TemporarySpeedLimit.mqtt' event: {_temporary_speed_limit.to_json()}")

    # ---- NL.NDW.Situations.SafetyRelatedMessage.mqtt ----
    # TODO: Supply event data for the NL.NDW.Situations.SafetyRelatedMessage.mqtt event
    _safety_related_message = SafetyRelatedMessage()

    # sends the 'NL.NDW.Situations.SafetyRelatedMessage.mqtt' event to Kafka topic.
    await nlndwsituations_mqtt_event_producer.send_nl_ndw_situations_safety_related_message_mqtt(_situation_record_id = 'TODO: replace me', data = _safety_related_message)
    print(f"Sent 'NL.NDW.Situations.SafetyRelatedMessage.mqtt' event: {_safety_related_message.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwavgamqp_event_producer = NLNDWAVGAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwavgamqp_event_producer = NLNDWAVGAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.AVG.PointMeasurementSite.amqp ----
    # TODO: Supply event data for the NL.NDW.AVG.PointMeasurementSite.amqp event
    _point_measurement_site = PointMeasurementSite()

    # sends the 'NL.NDW.AVG.PointMeasurementSite.amqp' event to Kafka topic.
    await nlndwavgamqp_event_producer.send_nl_ndw_avg_point_measurement_site_amqp(_measurement_site_id = 'TODO: replace me', data = _point_measurement_site)
    print(f"Sent 'NL.NDW.AVG.PointMeasurementSite.amqp' event: {_point_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.RouteMeasurementSite.amqp ----
    # TODO: Supply event data for the NL.NDW.AVG.RouteMeasurementSite.amqp event
    _route_measurement_site = RouteMeasurementSite()

    # sends the 'NL.NDW.AVG.RouteMeasurementSite.amqp' event to Kafka topic.
    await nlndwavgamqp_event_producer.send_nl_ndw_avg_route_measurement_site_amqp(_measurement_site_id = 'TODO: replace me', data = _route_measurement_site)
    print(f"Sent 'NL.NDW.AVG.RouteMeasurementSite.amqp' event: {_route_measurement_site.to_json()}")

    # ---- NL.NDW.AVG.TrafficObservation.amqp ----
    # TODO: Supply event data for the NL.NDW.AVG.TrafficObservation.amqp event
    _traffic_observation = TrafficObservation()

    # sends the 'NL.NDW.AVG.TrafficObservation.amqp' event to Kafka topic.
    await nlndwavgamqp_event_producer.send_nl_ndw_avg_traffic_observation_amqp(_measurement_site_id = 'TODO: replace me', data = _traffic_observation)
    print(f"Sent 'NL.NDW.AVG.TrafficObservation.amqp' event: {_traffic_observation.to_json()}")

    # ---- NL.NDW.AVG.TravelTimeObservation.amqp ----
    # TODO: Supply event data for the NL.NDW.AVG.TravelTimeObservation.amqp event
    _travel_time_observation = TravelTimeObservation()

    # sends the 'NL.NDW.AVG.TravelTimeObservation.amqp' event to Kafka topic.
    await nlndwavgamqp_event_producer.send_nl_ndw_avg_travel_time_observation_amqp(_measurement_site_id = 'TODO: replace me', data = _travel_time_observation)
    print(f"Sent 'NL.NDW.AVG.TravelTimeObservation.amqp' event: {_travel_time_observation.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwdripamqp_event_producer = NLNDWDRIPAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwdripamqp_event_producer = NLNDWDRIPAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.DRIP.DripSign.amqp ----
    # TODO: Supply event data for the NL.NDW.DRIP.DripSign.amqp event
    _drip_sign = DripSign()

    # sends the 'NL.NDW.DRIP.DripSign.amqp' event to Kafka topic.
    await nlndwdripamqp_event_producer.send_nl_ndw_drip_drip_sign_amqp(_vms_controller_id = 'TODO: replace me', _vms_index = 'TODO: replace me', data = _drip_sign)
    print(f"Sent 'NL.NDW.DRIP.DripSign.amqp' event: {_drip_sign.to_json()}")

    # ---- NL.NDW.DRIP.DripDisplayState.amqp ----
    # TODO: Supply event data for the NL.NDW.DRIP.DripDisplayState.amqp event
    _drip_display_state = DripDisplayState()

    # sends the 'NL.NDW.DRIP.DripDisplayState.amqp' event to Kafka topic.
    await nlndwdripamqp_event_producer.send_nl_ndw_drip_drip_display_state_amqp(_vms_controller_id = 'TODO: replace me', _vms_index = 'TODO: replace me', data = _drip_display_state)
    print(f"Sent 'NL.NDW.DRIP.DripDisplayState.amqp' event: {_drip_display_state.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwmsiamqp_event_producer = NLNDWMSIAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwmsiamqp_event_producer = NLNDWMSIAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.MSI.MsiSign.amqp ----
    # TODO: Supply event data for the NL.NDW.MSI.MsiSign.amqp event
    _msi_sign = MsiSign()

    # sends the 'NL.NDW.MSI.MsiSign.amqp' event to Kafka topic.
    await nlndwmsiamqp_event_producer.send_nl_ndw_msi_msi_sign_amqp(_sign_id = 'TODO: replace me', data = _msi_sign)
    print(f"Sent 'NL.NDW.MSI.MsiSign.amqp' event: {_msi_sign.to_json()}")

    # ---- NL.NDW.MSI.MsiDisplayState.amqp ----
    # TODO: Supply event data for the NL.NDW.MSI.MsiDisplayState.amqp event
    _msi_display_state = MsiDisplayState()

    # sends the 'NL.NDW.MSI.MsiDisplayState.amqp' event to Kafka topic.
    await nlndwmsiamqp_event_producer.send_nl_ndw_msi_msi_display_state_amqp(_sign_id = 'TODO: replace me', data = _msi_display_state)
    print(f"Sent 'NL.NDW.MSI.MsiDisplayState.amqp' event: {_msi_display_state.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        nlndwsituations_amqp_event_producer = NLNDWSituationsAmqpEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        nlndwsituations_amqp_event_producer = NLNDWSituationsAmqpEventProducer(kafka_producer, topic, 'binary')

    # ---- NL.NDW.Situations.Roadwork.amqp ----
    # TODO: Supply event data for the NL.NDW.Situations.Roadwork.amqp event
    _roadwork = Roadwork()

    # sends the 'NL.NDW.Situations.Roadwork.amqp' event to Kafka topic.
    await nlndwsituations_amqp_event_producer.send_nl_ndw_situations_roadwork_amqp(_situation_record_id = 'TODO: replace me', data = _roadwork)
    print(f"Sent 'NL.NDW.Situations.Roadwork.amqp' event: {_roadwork.to_json()}")

    # ---- NL.NDW.Situations.BridgeOpening.amqp ----
    # TODO: Supply event data for the NL.NDW.Situations.BridgeOpening.amqp event
    _bridge_opening = BridgeOpening()

    # sends the 'NL.NDW.Situations.BridgeOpening.amqp' event to Kafka topic.
    await nlndwsituations_amqp_event_producer.send_nl_ndw_situations_bridge_opening_amqp(_situation_record_id = 'TODO: replace me', data = _bridge_opening)
    print(f"Sent 'NL.NDW.Situations.BridgeOpening.amqp' event: {_bridge_opening.to_json()}")

    # ---- NL.NDW.Situations.TemporaryClosure.amqp ----
    # TODO: Supply event data for the NL.NDW.Situations.TemporaryClosure.amqp event
    _temporary_closure = TemporaryClosure()

    # sends the 'NL.NDW.Situations.TemporaryClosure.amqp' event to Kafka topic.
    await nlndwsituations_amqp_event_producer.send_nl_ndw_situations_temporary_closure_amqp(_situation_record_id = 'TODO: replace me', data = _temporary_closure)
    print(f"Sent 'NL.NDW.Situations.TemporaryClosure.amqp' event: {_temporary_closure.to_json()}")

    # ---- NL.NDW.Situations.TemporarySpeedLimit.amqp ----
    # TODO: Supply event data for the NL.NDW.Situations.TemporarySpeedLimit.amqp event
    _temporary_speed_limit = TemporarySpeedLimit()

    # sends the 'NL.NDW.Situations.TemporarySpeedLimit.amqp' event to Kafka topic.
    await nlndwsituations_amqp_event_producer.send_nl_ndw_situations_temporary_speed_limit_amqp(_situation_record_id = 'TODO: replace me', data = _temporary_speed_limit)
    print(f"Sent 'NL.NDW.Situations.TemporarySpeedLimit.amqp' event: {_temporary_speed_limit.to_json()}")

    # ---- NL.NDW.Situations.SafetyRelatedMessage.amqp ----
    # TODO: Supply event data for the NL.NDW.Situations.SafetyRelatedMessage.amqp event
    _safety_related_message = SafetyRelatedMessage()

    # sends the 'NL.NDW.Situations.SafetyRelatedMessage.amqp' event to Kafka topic.
    await nlndwsituations_amqp_event_producer.send_nl_ndw_situations_safety_related_message_amqp(_situation_record_id = 'TODO: replace me', data = _safety_related_message)
    print(f"Sent 'NL.NDW.Situations.SafetyRelatedMessage.amqp' event: {_safety_related_message.to_json()}")

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