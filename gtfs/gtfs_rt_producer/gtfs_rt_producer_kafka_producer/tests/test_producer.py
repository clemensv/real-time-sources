# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_rt_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_rt_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gtfs_rt_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from gtfs_rt_producer_kafka_producer.producer import GeneralTransitFeedRealTimeEventProducer
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_vehicle_vehicleposition import Test_VehiclePosition
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_trip_tripupdate import Test_TripUpdate
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_alert_alert import Test_Alert
from gtfs_rt_producer_kafka_producer.producer import GeneralTransitFeedStaticEventProducer
from test_gtfs_rt_producer_data_generaltransitfeedstatic_agency import Test_Agency
from test_gtfs_rt_producer_data_generaltransitfeedstatic_areas import Test_Areas
from test_gtfs_rt_producer_data_generaltransitfeedstatic_attributions import Test_Attributions
from test_gtfs_rt_producer_data_generaltransitfeedstatic_bookingrules import Test_BookingRules
from test_gtfs_rt_producer_data_generaltransitfeedstatic_fareattributes import Test_FareAttributes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_farelegrules import Test_FareLegRules
from test_gtfs_rt_producer_data_generaltransitfeedstatic_faremedia import Test_FareMedia
from test_gtfs_rt_producer_data_generaltransitfeedstatic_fareproducts import Test_FareProducts
from test_gtfs_rt_producer_data_generaltransitfeedstatic_farerules import Test_FareRules
from test_gtfs_rt_producer_data_generaltransitfeedstatic_faretransferrules import Test_FareTransferRules
from test_gtfs_rt_producer_data_generaltransitfeedstatic_feedinfo import Test_FeedInfo
from test_gtfs_rt_producer_data_generaltransitfeedstatic_frequencies import Test_Frequencies
from test_gtfs_rt_producer_data_generaltransitfeedstatic_levels import Test_Levels
from test_gtfs_rt_producer_data_generaltransitfeedstatic_locationgeojson import Test_LocationGeoJson
from test_gtfs_rt_producer_data_generaltransitfeedstatic_locationgroups import Test_LocationGroups
from test_gtfs_rt_producer_data_generaltransitfeedstatic_locationgroupstores import Test_LocationGroupStores
from test_gtfs_rt_producer_data_generaltransitfeedstatic_networks import Test_Networks
from test_gtfs_rt_producer_data_generaltransitfeedstatic_pathways import Test_Pathways
from test_gtfs_rt_producer_data_generaltransitfeedstatic_routenetworks import Test_RouteNetworks
from test_gtfs_rt_producer_data_generaltransitfeedstatic_routes import Test_Routes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_shapes import Test_Shapes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_stopareas import Test_StopAreas
from test_gtfs_rt_producer_data_generaltransitfeedstatic_stops import Test_Stops
from test_gtfs_rt_producer_data_generaltransitfeedstatic_stoptimes import Test_StopTimes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_timeframes import Test_Timeframes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_transfers import Test_Transfers
from test_gtfs_rt_producer_data_generaltransitfeedstatic_translations import Test_Translations
from test_gtfs_rt_producer_data_generaltransitfeedstatic_trips import Test_Trips

@pytest.fixture(scope="module")
def kafka_emulator():
    with KafkaContainer() as kafka:
        admin_client = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic_list = [
            NewTopic("test_topic", num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(topic_list)

        yield {
            "bootstrap_servers": kafka.get_bootstrap_server(),
            "topic": "test_topic",
        }

def parse_cloudevent(msg: Message) -> CloudEvent:
    headers_dict: Dict[str, bytes] = {header[0]: header[1] for header in msg.headers()}
    message = KafkaMessage(headers=headers_dict, key=msg.key(), value=msg.value())
    if message.headers and 'content-type' in message.headers:
        content_type = message.headers['content-type'].decode()
        if content_type.startswith('application/cloudevents'):
            ce = from_structured(message)
            if 'datacontenttype' not in ce:
                ce['datacontenttype'] = 'application/json'
        else:
            ce = from_binary(message)
            ce['datacontenttype'] = message.headers['content-type'].decode()
    else:
        ce = from_binary(message)
        ce['datacontenttype'] = 'application/json'
    return ce

@pytest.mark.asyncio
async def test_generaltransitfeedrealtime_generaltransitfeedrealtimevehiclevehicleposition(kafka_emulator):
    """Test the GeneralTransitFeedRealTimeVehicleVehiclePosition event from the GeneralTransitFeedRealTime message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedRealTime.Vehicle.VehiclePosition":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedRealTimeEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_VehiclePosition.create_instance()
    await producer_instance.send_general_transit_feed_real_time_vehicle_vehicle_position(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedrealtime_generaltransitfeedrealtimetriptripupdate(kafka_emulator):
    """Test the GeneralTransitFeedRealTimeTripTripUpdate event from the GeneralTransitFeedRealTime message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedRealTime.Trip.TripUpdate":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedRealTimeEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_TripUpdate.create_instance()
    await producer_instance.send_general_transit_feed_real_time_trip_trip_update(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedrealtime_generaltransitfeedrealtimealertalert(kafka_emulator):
    """Test the GeneralTransitFeedRealTimeAlertAlert event from the GeneralTransitFeedRealTime message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedRealTime.Alert.Alert":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedRealTimeEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Alert.create_instance()
    await producer_instance.send_general_transit_feed_real_time_alert_alert(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticagency(kafka_emulator):
    """Test the GeneralTransitFeedStaticAgency event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Agency":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Agency.create_instance()
    await producer_instance.send_general_transit_feed_static_agency(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticareas(kafka_emulator):
    """Test the GeneralTransitFeedStaticAreas event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Areas":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Areas.create_instance()
    await producer_instance.send_general_transit_feed_static_areas(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticattributions(kafka_emulator):
    """Test the GeneralTransitFeedStaticAttributions event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Attributions":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Attributions.create_instance()
    await producer_instance.send_general_transit_feed_static_attributions(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedbookingrules(kafka_emulator):
    """Test the GeneralTransitFeedBookingRules event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeed.BookingRules":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_BookingRules.create_instance()
    await producer_instance.send_general_transit_feed_booking_rules(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfareattributes(kafka_emulator):
    """Test the GeneralTransitFeedStaticFareAttributes event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.FareAttributes":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_FareAttributes.create_instance()
    await producer_instance.send_general_transit_feed_static_fare_attributes(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfarelegrules(kafka_emulator):
    """Test the GeneralTransitFeedStaticFareLegRules event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.FareLegRules":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_FareLegRules.create_instance()
    await producer_instance.send_general_transit_feed_static_fare_leg_rules(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfaremedia(kafka_emulator):
    """Test the GeneralTransitFeedStaticFareMedia event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.FareMedia":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_FareMedia.create_instance()
    await producer_instance.send_general_transit_feed_static_fare_media(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfareproducts(kafka_emulator):
    """Test the GeneralTransitFeedStaticFareProducts event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.FareProducts":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_FareProducts.create_instance()
    await producer_instance.send_general_transit_feed_static_fare_products(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfarerules(kafka_emulator):
    """Test the GeneralTransitFeedStaticFareRules event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.FareRules":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_FareRules.create_instance()
    await producer_instance.send_general_transit_feed_static_fare_rules(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfaretransferrules(kafka_emulator):
    """Test the GeneralTransitFeedStaticFareTransferRules event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.FareTransferRules":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_FareTransferRules.create_instance()
    await producer_instance.send_general_transit_feed_static_fare_transfer_rules(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfeedinfo(kafka_emulator):
    """Test the GeneralTransitFeedStaticFeedInfo event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.FeedInfo":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_FeedInfo.create_instance()
    await producer_instance.send_general_transit_feed_static_feed_info(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticfrequencies(kafka_emulator):
    """Test the GeneralTransitFeedStaticFrequencies event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Frequencies":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Frequencies.create_instance()
    await producer_instance.send_general_transit_feed_static_frequencies(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticlevels(kafka_emulator):
    """Test the GeneralTransitFeedStaticLevels event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Levels":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Levels.create_instance()
    await producer_instance.send_general_transit_feed_static_levels(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticlocationgeojson(kafka_emulator):
    """Test the GeneralTransitFeedStaticLocationGeoJson event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.LocationGeoJson":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_LocationGeoJson.create_instance()
    await producer_instance.send_general_transit_feed_static_location_geo_json(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticlocationgroups(kafka_emulator):
    """Test the GeneralTransitFeedStaticLocationGroups event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.LocationGroups":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_LocationGroups.create_instance()
    await producer_instance.send_general_transit_feed_static_location_groups(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticlocationgroupstores(kafka_emulator):
    """Test the GeneralTransitFeedStaticLocationGroupStores event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.LocationGroupStores":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_LocationGroupStores.create_instance()
    await producer_instance.send_general_transit_feed_static_location_group_stores(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticnetworks(kafka_emulator):
    """Test the GeneralTransitFeedStaticNetworks event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Networks":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Networks.create_instance()
    await producer_instance.send_general_transit_feed_static_networks(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticpathways(kafka_emulator):
    """Test the GeneralTransitFeedStaticPathways event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Pathways":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Pathways.create_instance()
    await producer_instance.send_general_transit_feed_static_pathways(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticroutenetworks(kafka_emulator):
    """Test the GeneralTransitFeedStaticRouteNetworks event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.RouteNetworks":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_RouteNetworks.create_instance()
    await producer_instance.send_general_transit_feed_static_route_networks(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticroutes(kafka_emulator):
    """Test the GeneralTransitFeedStaticRoutes event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Routes":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Routes.create_instance()
    await producer_instance.send_general_transit_feed_static_routes(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticshapes(kafka_emulator):
    """Test the GeneralTransitFeedStaticShapes event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Shapes":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Shapes.create_instance()
    await producer_instance.send_general_transit_feed_static_shapes(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticstopareas(kafka_emulator):
    """Test the GeneralTransitFeedStaticStopAreas event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.StopAreas":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_StopAreas.create_instance()
    await producer_instance.send_general_transit_feed_static_stop_areas(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticstops(kafka_emulator):
    """Test the GeneralTransitFeedStaticStops event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Stops":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Stops.create_instance()
    await producer_instance.send_general_transit_feed_static_stops(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstaticstoptimes(kafka_emulator):
    """Test the GeneralTransitFeedStaticStopTimes event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.StopTimes":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_StopTimes.create_instance()
    await producer_instance.send_general_transit_feed_static_stop_times(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstatictimeframes(kafka_emulator):
    """Test the GeneralTransitFeedStaticTimeframes event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Timeframes":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Timeframes.create_instance()
    await producer_instance.send_general_transit_feed_static_timeframes(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstatictransfers(kafka_emulator):
    """Test the GeneralTransitFeedStaticTransfers event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Transfers":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Transfers.create_instance()
    await producer_instance.send_general_transit_feed_static_transfers(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstatictranslations(kafka_emulator):
    """Test the GeneralTransitFeedStaticTranslations event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Translations":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Translations.create_instance()
    await producer_instance.send_general_transit_feed_static_translations(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_generaltransitfeedstatic_generaltransitfeedstatictrips(kafka_emulator):
    """Test the GeneralTransitFeedStaticTrips event from the GeneralTransitFeedStatic message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "GeneralTransitFeedStatic.Trips":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Trips.create_instance()
    await producer_instance.send_general_transit_feed_static_trips(_feedurl = 'test', _agencyid = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()