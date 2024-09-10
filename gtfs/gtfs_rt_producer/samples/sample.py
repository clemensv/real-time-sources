
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

from gtfs_rt_producer_kafka_producer.producer import GeneralTransitFeedRealTimeEventProducer
from gtfs_rt_producer_kafka_producer.producer import GeneralTransitFeedStaticEventProducer

# imports for the data classes for each event

from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicleposition import VehiclePosition
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripupdate import TripUpdate
from gtfs_rt_producer_data.generaltransitfeed.alert.alert import Alert
from gtfs_rt_producer_data.generaltransitfeedstatic.agency import Agency
from gtfs_rt_producer_data.generaltransitfeedstatic.areas import Areas
from gtfs_rt_producer_data.generaltransitfeedstatic.attributions import Attributions
from gtfs_rt_producer_data.generaltransitfeedstatic.bookingrules import BookingRules
from gtfs_rt_producer_data.generaltransitfeedstatic.fareattributes import FareAttributes
from gtfs_rt_producer_data.generaltransitfeedstatic.farelegrules import FareLegRules
from gtfs_rt_producer_data.generaltransitfeedstatic.faremedia import FareMedia
from gtfs_rt_producer_data.generaltransitfeedstatic.fareproducts import FareProducts
from gtfs_rt_producer_data.generaltransitfeedstatic.farerules import FareRules
from gtfs_rt_producer_data.generaltransitfeedstatic.faretransferrules import FareTransferRules
from gtfs_rt_producer_data.generaltransitfeedstatic.feedinfo import FeedInfo
from gtfs_rt_producer_data.generaltransitfeedstatic.frequencies import Frequencies
from gtfs_rt_producer_data.generaltransitfeedstatic.levels import Levels
from gtfs_rt_producer_data.generaltransitfeedstatic.locationgeojson import LocationGeoJson
from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroups import LocationGroups
from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroupstores import LocationGroupStores
from gtfs_rt_producer_data.generaltransitfeedstatic.networks import Networks
from gtfs_rt_producer_data.generaltransitfeedstatic.pathways import Pathways
from gtfs_rt_producer_data.generaltransitfeedstatic.routenetworks import RouteNetworks
from gtfs_rt_producer_data.generaltransitfeedstatic.routes import Routes
from gtfs_rt_producer_data.generaltransitfeedstatic.shapes import Shapes
from gtfs_rt_producer_data.generaltransitfeedstatic.stopareas import StopAreas
from gtfs_rt_producer_data.generaltransitfeedstatic.stops import Stops
from gtfs_rt_producer_data.generaltransitfeedstatic.stoptimes import StopTimes
from gtfs_rt_producer_data.generaltransitfeedstatic.timeframes import Timeframes
from gtfs_rt_producer_data.generaltransitfeedstatic.transfers import Transfers
from gtfs_rt_producer_data.generaltransitfeedstatic.translations import Translations
from gtfs_rt_producer_data.generaltransitfeedstatic.trips import Trips

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
        general_transit_feed_real_time_event_producer = GeneralTransitFeedRealTimeEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        general_transit_feed_real_time_event_producer = GeneralTransitFeedRealTimeEventProducer(kafka_producer, topic, 'binary')

    # ---- GeneralTransitFeed.RealTime.VehiclePosition ----
    # TODO: Supply event data for the GeneralTransitFeed.RealTime.VehiclePosition event
    _vehicle_position = VehiclePosition()

    # sends the 'GeneralTransitFeed.RealTime.VehiclePosition' event to Kafka topic.
    await general_transit_feed_real_time_event_producer.send_general_transit_feed_real_time_vehicle_position(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _vehicle_position)
    print(f"Sent 'GeneralTransitFeed.RealTime.VehiclePosition' event: {_vehicle_position.to_json()}")

    # ---- GeneralTransitFeed.RealTime.TripUpdate ----
    # TODO: Supply event data for the GeneralTransitFeed.RealTime.TripUpdate event
    _trip_update = TripUpdate()

    # sends the 'GeneralTransitFeed.RealTime.TripUpdate' event to Kafka topic.
    await general_transit_feed_real_time_event_producer.send_general_transit_feed_real_time_trip_update(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _trip_update)
    print(f"Sent 'GeneralTransitFeed.RealTime.TripUpdate' event: {_trip_update.to_json()}")

    # ---- GeneralTransitFeed.RealTime.Alert ----
    # TODO: Supply event data for the GeneralTransitFeed.RealTime.Alert event
    _alert = Alert()

    # sends the 'GeneralTransitFeed.RealTime.Alert' event to Kafka topic.
    await general_transit_feed_real_time_event_producer.send_general_transit_feed_real_time_alert(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _alert)
    print(f"Sent 'GeneralTransitFeed.RealTime.Alert' event: {_alert.to_json()}")
    if connection_string:
        # use a connection string obtained for an Event Stream from the Microsoft Fabric portal
        # or an Azure Event Hubs connection string
        general_transit_feed_static_event_producer = GeneralTransitFeedStaticEventProducer.from_connection_string(connection_string, topic, 'binary')
    else:
        # use a Kafka producer configuration provided as JSON text
        kafka_producer = KafkaProducer(json.loads(producer_config))
        general_transit_feed_static_event_producer = GeneralTransitFeedStaticEventProducer(kafka_producer, topic, 'binary')

    # ---- GeneralTransitFeed.Static.Agency ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Agency event
    _agency = Agency()

    # sends the 'GeneralTransitFeed.Static.Agency' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_agency(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _agency)
    print(f"Sent 'GeneralTransitFeed.Static.Agency' event: {_agency.to_json()}")

    # ---- GeneralTransitFeed.Static.Areas ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Areas event
    _areas = Areas()

    # sends the 'GeneralTransitFeed.Static.Areas' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_areas(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _areas)
    print(f"Sent 'GeneralTransitFeed.Static.Areas' event: {_areas.to_json()}")

    # ---- GeneralTransitFeed.Static.Attributions ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Attributions event
    _attributions = Attributions()

    # sends the 'GeneralTransitFeed.Static.Attributions' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_attributions(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _attributions)
    print(f"Sent 'GeneralTransitFeed.Static.Attributions' event: {_attributions.to_json()}")

    # ---- GeneralTransitFeed.BookingRules ----
    # TODO: Supply event data for the GeneralTransitFeed.BookingRules event
    _booking_rules = BookingRules()

    # sends the 'GeneralTransitFeed.BookingRules' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_booking_rules(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _booking_rules)
    print(f"Sent 'GeneralTransitFeed.BookingRules' event: {_booking_rules.to_json()}")

    # ---- GeneralTransitFeed.Static.FareAttributes ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.FareAttributes event
    _fare_attributes = FareAttributes()

    # sends the 'GeneralTransitFeed.Static.FareAttributes' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_fare_attributes(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _fare_attributes)
    print(f"Sent 'GeneralTransitFeed.Static.FareAttributes' event: {_fare_attributes.to_json()}")

    # ---- GeneralTransitFeed.Static.FareLegRules ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.FareLegRules event
    _fare_leg_rules = FareLegRules()

    # sends the 'GeneralTransitFeed.Static.FareLegRules' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_fare_leg_rules(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _fare_leg_rules)
    print(f"Sent 'GeneralTransitFeed.Static.FareLegRules' event: {_fare_leg_rules.to_json()}")

    # ---- GeneralTransitFeed.Static.FareMedia ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.FareMedia event
    _fare_media = FareMedia()

    # sends the 'GeneralTransitFeed.Static.FareMedia' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_fare_media(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _fare_media)
    print(f"Sent 'GeneralTransitFeed.Static.FareMedia' event: {_fare_media.to_json()}")

    # ---- GeneralTransitFeed.Static.FareProducts ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.FareProducts event
    _fare_products = FareProducts()

    # sends the 'GeneralTransitFeed.Static.FareProducts' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_fare_products(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _fare_products)
    print(f"Sent 'GeneralTransitFeed.Static.FareProducts' event: {_fare_products.to_json()}")

    # ---- GeneralTransitFeed.Static.FareRules ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.FareRules event
    _fare_rules = FareRules()

    # sends the 'GeneralTransitFeed.Static.FareRules' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_fare_rules(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _fare_rules)
    print(f"Sent 'GeneralTransitFeed.Static.FareRules' event: {_fare_rules.to_json()}")

    # ---- GeneralTransitFeed.Static.FareTransferRules ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.FareTransferRules event
    _fare_transfer_rules = FareTransferRules()

    # sends the 'GeneralTransitFeed.Static.FareTransferRules' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_fare_transfer_rules(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _fare_transfer_rules)
    print(f"Sent 'GeneralTransitFeed.Static.FareTransferRules' event: {_fare_transfer_rules.to_json()}")

    # ---- GeneralTransitFeed.Static.FeedInfo ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.FeedInfo event
    _feed_info = FeedInfo()

    # sends the 'GeneralTransitFeed.Static.FeedInfo' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_feed_info(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _feed_info)
    print(f"Sent 'GeneralTransitFeed.Static.FeedInfo' event: {_feed_info.to_json()}")

    # ---- GeneralTransitFeed.Static.Frequencies ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Frequencies event
    _frequencies = Frequencies()

    # sends the 'GeneralTransitFeed.Static.Frequencies' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_frequencies(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _frequencies)
    print(f"Sent 'GeneralTransitFeed.Static.Frequencies' event: {_frequencies.to_json()}")

    # ---- GeneralTransitFeed.Static.Levels ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Levels event
    _levels = Levels()

    # sends the 'GeneralTransitFeed.Static.Levels' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_levels(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _levels)
    print(f"Sent 'GeneralTransitFeed.Static.Levels' event: {_levels.to_json()}")

    # ---- GeneralTransitFeed.Static.LocationGeoJson ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.LocationGeoJson event
    _location_geo_json = LocationGeoJson()

    # sends the 'GeneralTransitFeed.Static.LocationGeoJson' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_location_geo_json(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _location_geo_json)
    print(f"Sent 'GeneralTransitFeed.Static.LocationGeoJson' event: {_location_geo_json.to_json()}")

    # ---- GeneralTransitFeed.Static.LocationGroups ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.LocationGroups event
    _location_groups = LocationGroups()

    # sends the 'GeneralTransitFeed.Static.LocationGroups' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_location_groups(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _location_groups)
    print(f"Sent 'GeneralTransitFeed.Static.LocationGroups' event: {_location_groups.to_json()}")

    # ---- GeneralTransitFeed.Static.LocationGroupStores ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.LocationGroupStores event
    _location_group_stores = LocationGroupStores()

    # sends the 'GeneralTransitFeed.Static.LocationGroupStores' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_location_group_stores(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _location_group_stores)
    print(f"Sent 'GeneralTransitFeed.Static.LocationGroupStores' event: {_location_group_stores.to_json()}")

    # ---- GeneralTransitFeed.Static.Networks ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Networks event
    _networks = Networks()

    # sends the 'GeneralTransitFeed.Static.Networks' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_networks(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _networks)
    print(f"Sent 'GeneralTransitFeed.Static.Networks' event: {_networks.to_json()}")

    # ---- GeneralTransitFeed.Static.Pathways ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Pathways event
    _pathways = Pathways()

    # sends the 'GeneralTransitFeed.Static.Pathways' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_pathways(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _pathways)
    print(f"Sent 'GeneralTransitFeed.Static.Pathways' event: {_pathways.to_json()}")

    # ---- GeneralTransitFeed.Static.RouteNetworks ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.RouteNetworks event
    _route_networks = RouteNetworks()

    # sends the 'GeneralTransitFeed.Static.RouteNetworks' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_route_networks(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _route_networks)
    print(f"Sent 'GeneralTransitFeed.Static.RouteNetworks' event: {_route_networks.to_json()}")

    # ---- GeneralTransitFeed.Static.Routes ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Routes event
    _routes = Routes()

    # sends the 'GeneralTransitFeed.Static.Routes' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_routes(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _routes)
    print(f"Sent 'GeneralTransitFeed.Static.Routes' event: {_routes.to_json()}")

    # ---- GeneralTransitFeed.Static.Shapes ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Shapes event
    _shapes = Shapes()

    # sends the 'GeneralTransitFeed.Static.Shapes' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_shapes(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _shapes)
    print(f"Sent 'GeneralTransitFeed.Static.Shapes' event: {_shapes.to_json()}")

    # ---- GeneralTransitFeed.Static.StopAreas ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.StopAreas event
    _stop_areas = StopAreas()

    # sends the 'GeneralTransitFeed.Static.StopAreas' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_stop_areas(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _stop_areas)
    print(f"Sent 'GeneralTransitFeed.Static.StopAreas' event: {_stop_areas.to_json()}")

    # ---- GeneralTransitFeed.Static.Stops ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Stops event
    _stops = Stops()

    # sends the 'GeneralTransitFeed.Static.Stops' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_stops(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _stops)
    print(f"Sent 'GeneralTransitFeed.Static.Stops' event: {_stops.to_json()}")

    # ---- GeneralTransitFeed.Static.StopTimes ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.StopTimes event
    _stop_times = StopTimes()

    # sends the 'GeneralTransitFeed.Static.StopTimes' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_stop_times(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _stop_times)
    print(f"Sent 'GeneralTransitFeed.Static.StopTimes' event: {_stop_times.to_json()}")

    # ---- GeneralTransitFeed.Static.Timeframes ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Timeframes event
    _timeframes = Timeframes()

    # sends the 'GeneralTransitFeed.Static.Timeframes' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_timeframes(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _timeframes)
    print(f"Sent 'GeneralTransitFeed.Static.Timeframes' event: {_timeframes.to_json()}")

    # ---- GeneralTransitFeed.Static.Transfers ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Transfers event
    _transfers = Transfers()

    # sends the 'GeneralTransitFeed.Static.Transfers' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_transfers(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _transfers)
    print(f"Sent 'GeneralTransitFeed.Static.Transfers' event: {_transfers.to_json()}")

    # ---- GeneralTransitFeed.Static.Translations ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Translations event
    _translations = Translations()

    # sends the 'GeneralTransitFeed.Static.Translations' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_translations(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _translations)
    print(f"Sent 'GeneralTransitFeed.Static.Translations' event: {_translations.to_json()}")

    # ---- GeneralTransitFeed.Static.Trips ----
    # TODO: Supply event data for the GeneralTransitFeed.Static.Trips event
    _trips = Trips()

    # sends the 'GeneralTransitFeed.Static.Trips' event to Kafka topic.
    await general_transit_feed_static_event_producer.send_general_transit_feed_static_trips(_feedurl = 'TODO: replace me', _agencyid = 'TODO: replace me', data = _trips)
    print(f"Sent 'GeneralTransitFeed.Static.Trips' event: {_trips.to_json()}")

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