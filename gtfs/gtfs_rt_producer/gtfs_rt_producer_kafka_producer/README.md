
# Gtfs_rt_producer Event Dispatcher for Apache Kafka

This module provides an event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages
and CloudEvents.

## Table of Contents
1. [Overview](#overview)
2. [Generated Event Dispatchers](#generated-event-dispatchers)
    - GeneralTransitFeedRealTimeEventDispatcher,
    GeneralTransitFeedStaticEventDispatcher

3. [Internals](#internals)
    - [EventProcessorRunner](#eventprocessorrunner)
    - [_DispatcherBase](#_dispatcherbase)

## Overview

This module defines an event processing framework for Apache Kafka,
providing the necessary classes and methods to handle various types of events.
It includes both plain Kafka messages and CloudEvents, offering a versatile
solution for event-driven applications.

## Generated Event Dispatchers



### GeneralTransitFeedRealTimeEventDispatcher

`GeneralTransitFeedRealTimeEventDispatcher` handles events for the GeneralTransitFeed.RealTime message group.

#### Methods:

##### `__init__`:

```python
__init__(self)-> None
```

Initializes the dispatcher.

##### `create_processor`:

```python
create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner
```

Creates an `EventProcessorRunner`.

Args:
- `bootstrap_servers`: The Kafka bootstrap servers.
- `group_id`: The consumer group ID.
- `topics`: The list of topics to subscribe to.

##### `add_consumer`:

```python
add_consumer(self, consumer: KafkaConsumer)
```

Adds a Kafka consumer to the dispatcher.

Args:
- `consumer`: The Kafka consumer.

#### Event Handlers

The GeneralTransitFeedRealTimeEventDispatcher defines the following event handler hooks.


##### `general_transit_feed_real_time_vehicle_position_async`

```python
general_transit_feed_real_time_vehicle_position_async:  Callable[[ConsumerRecord, CloudEvent, VehiclePosition],
Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.RealTime.VehiclePosition`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeed.vehicleposition.VehiclePosition`.

Example:

```python
async def general_transit_feed_real_time_vehicle_position_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
VehiclePosition) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_real_time_dispatcher.general_transit_feed_real_time_vehicle_position_async =
general_transit_feed_real_time_vehicle_position_event
```


##### `general_transit_feed_real_time_trip_update_async`

```python
general_transit_feed_real_time_trip_update_async:  Callable[[ConsumerRecord, CloudEvent, TripUpdate], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.RealTime.TripUpdate`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeed.tripupdate.TripUpdate`.

Example:

```python
async def general_transit_feed_real_time_trip_update_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
TripUpdate) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_real_time_dispatcher.general_transit_feed_real_time_trip_update_async =
general_transit_feed_real_time_trip_update_event
```


##### `general_transit_feed_real_time_alert_async`

```python
general_transit_feed_real_time_alert_async:  Callable[[ConsumerRecord, CloudEvent, Alert], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.RealTime.Alert`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeed.alert.Alert`.

Example:

```python
async def general_transit_feed_real_time_alert_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Alert) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_real_time_dispatcher.general_transit_feed_real_time_alert_async =
general_transit_feed_real_time_alert_event
```




### GeneralTransitFeedStaticEventDispatcher

`GeneralTransitFeedStaticEventDispatcher` handles events for the GeneralTransitFeed.Static message group.

#### Methods:

##### `__init__`:

```python
__init__(self)-> None
```

Initializes the dispatcher.

##### `create_processor`:

```python
create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner
```

Creates an `EventProcessorRunner`.

Args:
- `bootstrap_servers`: The Kafka bootstrap servers.
- `group_id`: The consumer group ID.
- `topics`: The list of topics to subscribe to.

##### `add_consumer`:

```python
add_consumer(self, consumer: KafkaConsumer)
```

Adds a Kafka consumer to the dispatcher.

Args:
- `consumer`: The Kafka consumer.

#### Event Handlers

The GeneralTransitFeedStaticEventDispatcher defines the following event handler hooks.


##### `general_transit_feed_static_agency_async`

```python
general_transit_feed_static_agency_async:  Callable[[ConsumerRecord, CloudEvent, Agency], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Agency`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Agency`.

Example:

```python
async def general_transit_feed_static_agency_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Agency) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_agency_async =
general_transit_feed_static_agency_event
```


##### `general_transit_feed_static_areas_async`

```python
general_transit_feed_static_areas_async:  Callable[[ConsumerRecord, CloudEvent, Areas], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Areas`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Areas`.

Example:

```python
async def general_transit_feed_static_areas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Areas) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_areas_async = general_transit_feed_static_areas_event
```


##### `general_transit_feed_static_attributions_async`

```python
general_transit_feed_static_attributions_async:  Callable[[ConsumerRecord, CloudEvent, Attributions], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Attributions`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Attributions`.

Example:

```python
async def general_transit_feed_static_attributions_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Attributions) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_attributions_async =
general_transit_feed_static_attributions_event
```


##### `general_transit_feed_booking_rules_async`

```python
general_transit_feed_booking_rules_async:  Callable[[ConsumerRecord, CloudEvent, BookingRules], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.BookingRules`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.BookingRules`.

Example:

```python
async def general_transit_feed_booking_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data: BookingRules)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_booking_rules_async =
general_transit_feed_booking_rules_event
```


##### `general_transit_feed_static_fare_attributes_async`

```python
general_transit_feed_static_fare_attributes_async:  Callable[[ConsumerRecord, CloudEvent, FareAttributes],
Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.FareAttributes`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.FareAttributes`.

Example:

```python
async def general_transit_feed_static_fare_attributes_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareAttributes) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_fare_attributes_async =
general_transit_feed_static_fare_attributes_event
```


##### `general_transit_feed_static_fare_leg_rules_async`

```python
general_transit_feed_static_fare_leg_rules_async:  Callable[[ConsumerRecord, CloudEvent, FareLegRules], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.FareLegRules`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.FareLegRules`.

Example:

```python
async def general_transit_feed_static_fare_leg_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareLegRules) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_fare_leg_rules_async =
general_transit_feed_static_fare_leg_rules_event
```


##### `general_transit_feed_static_fare_media_async`

```python
general_transit_feed_static_fare_media_async:  Callable[[ConsumerRecord, CloudEvent, FareMedia], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.FareMedia`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.FareMedia`.

Example:

```python
async def general_transit_feed_static_fare_media_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FareMedia)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_fare_media_async =
general_transit_feed_static_fare_media_event
```


##### `general_transit_feed_static_fare_products_async`

```python
general_transit_feed_static_fare_products_async:  Callable[[ConsumerRecord, CloudEvent, FareProducts], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.FareProducts`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.FareProducts`.

Example:

```python
async def general_transit_feed_static_fare_products_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareProducts) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_fare_products_async =
general_transit_feed_static_fare_products_event
```


##### `general_transit_feed_static_fare_rules_async`

```python
general_transit_feed_static_fare_rules_async:  Callable[[ConsumerRecord, CloudEvent, FareRules], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.FareRules`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.FareRules`.

Example:

```python
async def general_transit_feed_static_fare_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FareRules)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_fare_rules_async =
general_transit_feed_static_fare_rules_event
```


##### `general_transit_feed_static_fare_transfer_rules_async`

```python
general_transit_feed_static_fare_transfer_rules_async:  Callable[[ConsumerRecord, CloudEvent, FareTransferRules],
Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.FareTransferRules`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.FareTransferRules`.

Example:

```python
async def general_transit_feed_static_fare_transfer_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareTransferRules) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_fare_transfer_rules_async =
general_transit_feed_static_fare_transfer_rules_event
```


##### `general_transit_feed_static_feed_info_async`

```python
general_transit_feed_static_feed_info_async:  Callable[[ConsumerRecord, CloudEvent, FeedInfo], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.FeedInfo`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.FeedInfo`.

Example:

```python
async def general_transit_feed_static_feed_info_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FeedInfo)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_feed_info_async =
general_transit_feed_static_feed_info_event
```


##### `general_transit_feed_static_frequencies_async`

```python
general_transit_feed_static_frequencies_async:  Callable[[ConsumerRecord, CloudEvent, Frequencies], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Frequencies`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Frequencies`.

Example:

```python
async def general_transit_feed_static_frequencies_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Frequencies) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_frequencies_async =
general_transit_feed_static_frequencies_event
```


##### `general_transit_feed_static_levels_async`

```python
general_transit_feed_static_levels_async:  Callable[[ConsumerRecord, CloudEvent, Levels], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Levels`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Levels`.

Example:

```python
async def general_transit_feed_static_levels_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Levels) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_levels_async =
general_transit_feed_static_levels_event
```


##### `general_transit_feed_static_location_geo_json_async`

```python
general_transit_feed_static_location_geo_json_async:  Callable[[ConsumerRecord, CloudEvent, LocationGeoJson],
Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.LocationGeoJson`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.LocationGeoJson`.

Example:

```python
async def general_transit_feed_static_location_geo_json_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGeoJson) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_location_geo_json_async =
general_transit_feed_static_location_geo_json_event
```


##### `general_transit_feed_static_location_groups_async`

```python
general_transit_feed_static_location_groups_async:  Callable[[ConsumerRecord, CloudEvent, LocationGroups],
Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.LocationGroups`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.LocationGroups`.

Example:

```python
async def general_transit_feed_static_location_groups_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGroups) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_location_groups_async =
general_transit_feed_static_location_groups_event
```


##### `general_transit_feed_static_location_group_stores_async`

```python
general_transit_feed_static_location_group_stores_async:  Callable[[ConsumerRecord, CloudEvent, LocationGroupStores],
Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.LocationGroupStores`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.LocationGroupStores`.

Example:

```python
async def general_transit_feed_static_location_group_stores_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGroupStores) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_location_group_stores_async =
general_transit_feed_static_location_group_stores_event
```


##### `general_transit_feed_static_networks_async`

```python
general_transit_feed_static_networks_async:  Callable[[ConsumerRecord, CloudEvent, Networks], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Networks`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Networks`.

Example:

```python
async def general_transit_feed_static_networks_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Networks) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_networks_async =
general_transit_feed_static_networks_event
```


##### `general_transit_feed_static_pathways_async`

```python
general_transit_feed_static_pathways_async:  Callable[[ConsumerRecord, CloudEvent, Pathways], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Pathways`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Pathways`.

Example:

```python
async def general_transit_feed_static_pathways_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Pathways) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_pathways_async =
general_transit_feed_static_pathways_event
```


##### `general_transit_feed_static_route_networks_async`

```python
general_transit_feed_static_route_networks_async:  Callable[[ConsumerRecord, CloudEvent, RouteNetworks],
Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.RouteNetworks`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.RouteNetworks`.

Example:

```python
async def general_transit_feed_static_route_networks_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
RouteNetworks) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_route_networks_async =
general_transit_feed_static_route_networks_event
```


##### `general_transit_feed_static_routes_async`

```python
general_transit_feed_static_routes_async:  Callable[[ConsumerRecord, CloudEvent, Routes], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Routes`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Routes`.

Example:

```python
async def general_transit_feed_static_routes_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Routes) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_routes_async =
general_transit_feed_static_routes_event
```


##### `general_transit_feed_static_shapes_async`

```python
general_transit_feed_static_shapes_async:  Callable[[ConsumerRecord, CloudEvent, Shapes], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Shapes`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Shapes`.

Example:

```python
async def general_transit_feed_static_shapes_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Shapes) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_shapes_async =
general_transit_feed_static_shapes_event
```


##### `general_transit_feed_static_stop_areas_async`

```python
general_transit_feed_static_stop_areas_async:  Callable[[ConsumerRecord, CloudEvent, StopAreas], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.StopAreas`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.StopAreas`.

Example:

```python
async def general_transit_feed_static_stop_areas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StopAreas)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_stop_areas_async =
general_transit_feed_static_stop_areas_event
```


##### `general_transit_feed_static_stops_async`

```python
general_transit_feed_static_stops_async:  Callable[[ConsumerRecord, CloudEvent, Stops], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Stops`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Stops`.

Example:

```python
async def general_transit_feed_static_stops_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stops) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_stops_async = general_transit_feed_static_stops_event
```


##### `general_transit_feed_static_stop_times_async`

```python
general_transit_feed_static_stop_times_async:  Callable[[ConsumerRecord, CloudEvent, StopTimes], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.StopTimes`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.StopTimes`.

Example:

```python
async def general_transit_feed_static_stop_times_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StopTimes)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_stop_times_async =
general_transit_feed_static_stop_times_event
```


##### `general_transit_feed_static_timeframes_async`

```python
general_transit_feed_static_timeframes_async:  Callable[[ConsumerRecord, CloudEvent, Timeframes], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Timeframes`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Timeframes`.

Example:

```python
async def general_transit_feed_static_timeframes_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Timeframes) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_timeframes_async =
general_transit_feed_static_timeframes_event
```


##### `general_transit_feed_static_transfers_async`

```python
general_transit_feed_static_transfers_async:  Callable[[ConsumerRecord, CloudEvent, Transfers], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Transfers`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Transfers`.

Example:

```python
async def general_transit_feed_static_transfers_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Transfers)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_transfers_async =
general_transit_feed_static_transfers_event
```


##### `general_transit_feed_static_translations_async`

```python
general_transit_feed_static_translations_async:  Callable[[ConsumerRecord, CloudEvent, Translations], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Translations`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Translations`.

Example:

```python
async def general_transit_feed_static_translations_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Translations) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_translations_async =
general_transit_feed_static_translations_event
```


##### `general_transit_feed_static_trips_async`

```python
general_transit_feed_static_trips_async:  Callable[[ConsumerRecord, CloudEvent, Trips], Awaitable[None]]
```

Asynchronous handler hook for `GeneralTransitFeed.Static.Trips`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `gtfs_rt_producer_data.generaltransitfeedstatic.Trips`.

Example:

```python
async def general_transit_feed_static_trips_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Trips) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
general_transit_feed_static_dispatcher.general_transit_feed_static_trips_async = general_transit_feed_static_trips_event
```




## Internals

### Dispatchers

Dispatchers have the following protected methods:

### Methods:

##### `_process_event`

```python
_process_event(self, record)
```

Processes an incoming event.

Args:
- `record`: The Kafka record.

### EventProcessorRunner

`EventProcessorRunner` is responsible for managing the event processing loop and dispatching events to the appropriate
handlers.

#### Methods

##### `__init__`

```python
__init__(consumer: KafkaConsumer)
```

Initializes the runner with a Kafka consumer.

Args:
- `consumer`: The Kafka consumer.

#####  `__aenter__()`

Enters the asynchronous context and starts the processor.

#####  `__aexit__`

```python
__aexit__(exc_type, exc_val, exc_tb)
```

Exits the asynchronous context and stops the processor.

Args:
- `exc_type`: The exception type.
- `exc_val`: The exception value.
- `exc_tb`: The exception traceback.

#####  `add_dispatcher`

```python
add_dispatcher(dispatcher: _DispatcherBase)
```

Adds a dispatcher to the runner.

Args:
- `dispatcher`: The dispatcher to add.

#####  `remove_dispatcher`

```python
remove_dispatcher(dispatcher: _DispatcherBase)
```

Removes a dispatcher from the runner.

Args:
- `dispatcher`: The dispatcher to remove.

#####  `start()`

Starts the event processor.

#####  `cancel()`

Cancels the event processing task.

#####  `create_from_config`

```python
create_from_config(cls, bootstrap_servers: str, group_id: str, topics: List[str]) -> 'EventProcessorRunner'
```

Creates a runner from configuration.

Args:
- `bootstrap_servers`: The Kafka bootstrap servers.
- `group_id`: The consumer group ID.
- `topics`: The list of topics to subscribe to.

Returns:
- An `EventProcessorRunner` instance.

### _DispatcherBase

`_DispatcherBase` is a base class for event dispatchers, handling CloudEvent detection and conversion.

#### Methods

#####  `_strkey`

```python
_strkey(key: str | bytes) -> str
```

Converts a key to a string.

Args:
- `key`: The key to convert.

#####  `_unhandled_event`

```python
_unhandled_event(self, record, cloud_event, data)
```

Default event handler.

#####  `_get_cloud_event_attribute`

```python
_get_cloud_event_attribute(record: ConsumerRecord, key: str) -> Any
```

Retrieves a CloudEvent attribute from a Kafka record.

Args:
- `record`: The Kafka record.
- `key`: The attribute key.

#####  `_is_cloud_event`

```python
_is_cloud_event(record: ConsumerRecord) -> bool
```

Checks if the Kafka record is a CloudEvent.

Args:
- `record`: The Kafka record.

#####  `_cloud_event_from_record`

```python
_cloud_event_from_record(record: ConsumerRecord) -> CloudEvent
```

Converts a Kafka record to a CloudEvent.

Args:
- `record`: The Kafka record.