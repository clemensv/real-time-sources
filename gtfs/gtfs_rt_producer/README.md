

# Gtfs_rt_producer Kafka Producer# Gtfs_rt_producer Event Dispatcher for Apache Kafka



This module provides a type-safe Kafka producer for sending CloudEvents and plain Kafka messages.This module provides an
event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages and CloudEvents.



## Table of Contents## Table of Contents

1. [Overview](#overview)1. [Overview](#overview)

2. [What is Apache Kafka?](#what-is-apache-kafka)2. [Generated Event Dispatchers](#generated-event-dispatchers)

3. [Quick Start](#quick-start)    - GeneralTransitFeedRealTimeEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    GeneralTransitFeedStaticEventDispatcher

4. [Generated Producer Classes](#generated-producer-classes)

5. [Configuration Options](#configuration-options)3. [Internals](#internals)

6. [Error Handling](#error-handling)    - [EventProcessorRunner](#eventprocessorrunner)

7. [Best Practices](#best-practices)    - [_DispatcherBase](#_dispatcherbase)

8. [Production-Ready Patterns](#production-ready-patterns)

## Overview

## Overview

This module defines an event processing framework for Apache Kafka,

This module provides type-safe Kafka producers for the following message groups:providing the necessary classes and
methods to handle various types of events.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- GeneralTransitFeedRealTimeProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- GeneralTransitFeedStaticProducersolution for event-driven applications.



## Generated Event Dispatchers

## What is Apache Kafka?



**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### GeneralTransitFeedRealTimeEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`GeneralTransitFeedRealTimeEventDispatcher` handles events for the GeneralTransitFeedRealTime message group.

Use cases: Event streaming, log aggregation, real-time analytics, data integration.

#### Methods:

## Quick Start

##### `__init__`:

### Installation

```python

```bash__init__(self)-> None

pip install confluent-kafka cloudevents pydantic```

```

Initializes the dispatcher.

### Basic Usage

##### `create_processor`:

```python

from gtfs_rt_producer import GeneralTransitFeedRealTimeProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = GeneralTransitFeedRealTimeProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_general_transit_feed_real_time_vehicle_vehicle_position(```python

    data=VehiclePosition(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The GeneralTransitFeedRealTimeEventDispatcher defines the following event handler hooks.

```python

producer = GeneralTransitFeedRealTimeProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_real_time_vehicle_vehicle_position_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_real_time_vehicle_vehicle_position_async:
Callable[[ConsumerRecord, CloudEvent, VehiclePosition], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedRealTime.Vehicle.VehiclePosition`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.VehiclePosition`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_real_time_vehicle_vehicle_position_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: VehiclePosition) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_real_time_vehicle_vehicle_position_async =
general_transit_feed_real_time_vehicle_vehicle_position_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.VehiclePosition`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_real_time_vehicle_vehicle_position_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: VehiclePosition) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_real_time_vehicle_vehicle_position_async =
general_transit_feed_real_time_vehicle_vehicle_position_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_real_time_trip_trip_update_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_real_time_trip_trip_update_async:  Callable[[ConsumerRecord,
CloudEvent, TripUpdate], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedRealTime.Trip.TripUpdate`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.TripUpdate`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_real_time_trip_trip_update_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
TripUpdate) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_real_time_trip_trip_update_async =
general_transit_feed_real_time_trip_trip_update_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.TripUpdate`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_real_time_trip_trip_update_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
TripUpdate) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_real_time_trip_trip_update_async =
general_transit_feed_real_time_trip_trip_update_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_real_time_alert_alert_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_real_time_alert_alert_async:  Callable[[ConsumerRecord,
CloudEvent, Alert], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedRealTime.Alert.Alert`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Alert`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_real_time_alert_alert_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Alert)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_real_time_alert_alert_async =
general_transit_feed_real_time_alert_alert_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Alert`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_real_time_alert_alert_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Alert)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_real_time_alert_alert_async =
general_transit_feed_real_time_alert_alert_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_general_transit_feed_real_time_vehicle_vehicle_position`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_real_time_vehicle_vehicle_position(

    self,##### `_process_event`

    data: VehiclePosition,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedRealTime.Vehicle.VehiclePosition` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehiclePosition`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_real_time_vehicle_vehicle_position(

    data=VehiclePosition(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedRealTime.Vehicle.VehiclePosition` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_real_time_vehicle_vehicle_position_batch(```

    messages=[

        VehiclePosition(...),Initializes the runner with a Kafka consumer.

        VehiclePosition(...),

        VehiclePosition(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_real_time_trip_trip_update`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_real_time_trip_trip_update(

    self,##### `_process_event`

    data: TripUpdate,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedRealTime.Trip.TripUpdate` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TripUpdate`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_real_time_trip_trip_update(

    data=TripUpdate(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedRealTime.Trip.TripUpdate` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_real_time_trip_trip_update_batch(```

    messages=[

        TripUpdate(...),Initializes the runner with a Kafka consumer.

        TripUpdate(...),

        TripUpdate(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_real_time_alert_alert`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_real_time_alert_alert(

    self,##### `_process_event`

    data: Alert,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedRealTime.Alert.Alert` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Alert`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_real_time_alert_alert(

    data=Alert(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedRealTime.Alert.Alert` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_real_time_alert_alert_batch(```

    messages=[

        Alert(...),Initializes the runner with a Kafka consumer.

        Alert(...),

        Alert(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### GeneralTransitFeedStaticEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`GeneralTransitFeedStaticEventDispatcher` handles events for the GeneralTransitFeedStatic message group.

Use cases: Event streaming, log aggregation, real-time analytics, data integration.

#### Methods:

## Quick Start

##### `__init__`:

### Installation

```python

```bash__init__(self)-> None

pip install confluent-kafka cloudevents pydantic```

```

Initializes the dispatcher.

### Basic Usage

##### `create_processor`:

```python

from gtfs_rt_producer import GeneralTransitFeedRealTimeProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = GeneralTransitFeedRealTimeProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_general_transit_feed_real_time_vehicle_vehicle_position(```python

    data=VehiclePosition(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The GeneralTransitFeedStaticEventDispatcher defines the following event handler hooks.

```python

producer = GeneralTransitFeedRealTimeProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_agency_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_agency_async:  Callable[[ConsumerRecord, CloudEvent,
Agency], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Agency`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Agency`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_agency_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Agency) ->
None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_agency_async =
general_transit_feed_static_agency_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Agency`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_agency_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Agency) ->
None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_agency_async =
general_transit_feed_static_agency_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_areas_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_areas_async:  Callable[[ConsumerRecord, CloudEvent, Areas],
Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Areas`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Areas`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_areas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Areas) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_areas_async =
general_transit_feed_static_areas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Areas`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_areas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Areas) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_areas_async = general_transit_feed_static_areas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_attributions_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_attributions_async:  Callable[[ConsumerRecord, CloudEvent,
Attributions], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Attributions`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Attributions`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_attributions_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Attributions) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_attributions_async =
general_transit_feed_static_attributions_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Attributions`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_attributions_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Attributions) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_attributions_async =
general_transit_feed_static_attributions_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_booking_rules_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_booking_rules_async:  Callable[[ConsumerRecord, CloudEvent,
BookingRules], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeed.BookingRules`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.BookingRules`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_booking_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data: BookingRules)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_booking_rules_async =
general_transit_feed_booking_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.BookingRules`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_booking_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data: BookingRules)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_booking_rules_async =
general_transit_feed_booking_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_fare_attributes_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_fare_attributes_async:  Callable[[ConsumerRecord,
CloudEvent, FareAttributes], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.FareAttributes`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.FareAttributes`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_attributes_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareAttributes) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_fare_attributes_async =
general_transit_feed_static_fare_attributes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.FareAttributes`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_attributes_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareAttributes) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_fare_attributes_async =
general_transit_feed_static_fare_attributes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_fare_leg_rules_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_fare_leg_rules_async:  Callable[[ConsumerRecord,
CloudEvent, FareLegRules], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.FareLegRules`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.FareLegRules`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_leg_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareLegRules) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_fare_leg_rules_async =
general_transit_feed_static_fare_leg_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.FareLegRules`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_leg_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareLegRules) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_fare_leg_rules_async =
general_transit_feed_static_fare_leg_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_fare_media_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_fare_media_async:  Callable[[ConsumerRecord, CloudEvent,
FareMedia], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.FareMedia`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.FareMedia`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_media_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FareMedia)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_fare_media_async =
general_transit_feed_static_fare_media_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.FareMedia`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_media_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FareMedia)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_fare_media_async =
general_transit_feed_static_fare_media_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_fare_products_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_fare_products_async:  Callable[[ConsumerRecord, CloudEvent,
FareProducts], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.FareProducts`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.FareProducts`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_products_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareProducts) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_fare_products_async =
general_transit_feed_static_fare_products_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.FareProducts`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_products_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareProducts) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_fare_products_async =
general_transit_feed_static_fare_products_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_fare_rules_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_fare_rules_async:  Callable[[ConsumerRecord, CloudEvent,
FareRules], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.FareRules`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.FareRules`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FareRules)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_fare_rules_async =
general_transit_feed_static_fare_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.FareRules`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FareRules)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_fare_rules_async =
general_transit_feed_static_fare_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_fare_transfer_rules_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_fare_transfer_rules_async:  Callable[[ConsumerRecord,
CloudEvent, FareTransferRules], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.FareTransferRules`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.FareTransferRules`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_transfer_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareTransferRules) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_fare_transfer_rules_async =
general_transit_feed_static_fare_transfer_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.FareTransferRules`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_fare_transfer_rules_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
FareTransferRules) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_fare_transfer_rules_async =
general_transit_feed_static_fare_transfer_rules_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_feed_info_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_feed_info_async:  Callable[[ConsumerRecord, CloudEvent,
FeedInfo], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.FeedInfo`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.FeedInfo`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_feed_info_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FeedInfo)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_feed_info_async =
general_transit_feed_static_feed_info_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.FeedInfo`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_feed_info_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FeedInfo)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_feed_info_async =
general_transit_feed_static_feed_info_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_frequencies_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_frequencies_async:  Callable[[ConsumerRecord, CloudEvent,
Frequencies], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Frequencies`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Frequencies`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_frequencies_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Frequencies) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_frequencies_async =
general_transit_feed_static_frequencies_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Frequencies`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_frequencies_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Frequencies) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_frequencies_async =
general_transit_feed_static_frequencies_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_levels_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_levels_async:  Callable[[ConsumerRecord, CloudEvent,
Levels], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Levels`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Levels`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_levels_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Levels) ->
None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_levels_async =
general_transit_feed_static_levels_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Levels`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_levels_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Levels) ->
None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_levels_async =
general_transit_feed_static_levels_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_location_geo_json_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_location_geo_json_async:  Callable[[ConsumerRecord,
CloudEvent, LocationGeoJson], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.LocationGeoJson`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.LocationGeoJson`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_location_geo_json_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGeoJson) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_location_geo_json_async =
general_transit_feed_static_location_geo_json_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.LocationGeoJson`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_location_geo_json_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGeoJson) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_location_geo_json_async =
general_transit_feed_static_location_geo_json_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_location_groups_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_location_groups_async:  Callable[[ConsumerRecord,
CloudEvent, LocationGroups], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.LocationGroups`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.LocationGroups`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_location_groups_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGroups) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_location_groups_async =
general_transit_feed_static_location_groups_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.LocationGroups`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_location_groups_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGroups) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_location_groups_async =
general_transit_feed_static_location_groups_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_location_group_stores_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_location_group_stores_async:  Callable[[ConsumerRecord,
CloudEvent, LocationGroupStores], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.LocationGroupStores`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.LocationGroupStores`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_location_group_stores_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGroupStores) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_location_group_stores_async =
general_transit_feed_static_location_group_stores_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.LocationGroupStores`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_location_group_stores_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LocationGroupStores) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_location_group_stores_async =
general_transit_feed_static_location_group_stores_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_networks_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_networks_async:  Callable[[ConsumerRecord, CloudEvent,
Networks], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Networks`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Networks`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_networks_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Networks) ->
None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_networks_async =
general_transit_feed_static_networks_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Networks`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_networks_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Networks) ->
None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_networks_async =
general_transit_feed_static_networks_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_pathways_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_pathways_async:  Callable[[ConsumerRecord, CloudEvent,
Pathways], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Pathways`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Pathways`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_pathways_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Pathways) ->
None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_pathways_async =
general_transit_feed_static_pathways_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Pathways`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_pathways_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Pathways) ->
None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_pathways_async =
general_transit_feed_static_pathways_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_route_networks_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_route_networks_async:  Callable[[ConsumerRecord,
CloudEvent, RouteNetworks], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.RouteNetworks`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.RouteNetworks`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_route_networks_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
RouteNetworks) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_route_networks_async =
general_transit_feed_static_route_networks_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.RouteNetworks`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_route_networks_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
RouteNetworks) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_route_networks_async =
general_transit_feed_static_route_networks_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_routes_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_routes_async:  Callable[[ConsumerRecord, CloudEvent,
Routes], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Routes`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Routes`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_routes_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Routes) ->
None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_routes_async =
general_transit_feed_static_routes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Routes`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_routes_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Routes) ->
None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_routes_async =
general_transit_feed_static_routes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_shapes_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_shapes_async:  Callable[[ConsumerRecord, CloudEvent,
Shapes], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Shapes`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Shapes`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_shapes_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Shapes) ->
None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_shapes_async =
general_transit_feed_static_shapes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Shapes`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_shapes_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Shapes) ->
None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_shapes_async =
general_transit_feed_static_shapes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_stop_areas_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_stop_areas_async:  Callable[[ConsumerRecord, CloudEvent,
StopAreas], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.StopAreas`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.StopAreas`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_stop_areas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StopAreas)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_stop_areas_async =
general_transit_feed_static_stop_areas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.StopAreas`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_stop_areas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StopAreas)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_stop_areas_async =
general_transit_feed_static_stop_areas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_stops_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_stops_async:  Callable[[ConsumerRecord, CloudEvent, Stops],
Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Stops`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Stops`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_stops_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stops) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_stops_async =
general_transit_feed_static_stops_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Stops`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_stops_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stops) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_stops_async = general_transit_feed_static_stops_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_stop_times_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_stop_times_async:  Callable[[ConsumerRecord, CloudEvent,
StopTimes], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.StopTimes`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.StopTimes`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_stop_times_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StopTimes)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_stop_times_async =
general_transit_feed_static_stop_times_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.StopTimes`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_stop_times_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StopTimes)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_stop_times_async =
general_transit_feed_static_stop_times_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_timeframes_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_timeframes_async:  Callable[[ConsumerRecord, CloudEvent,
Timeframes], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Timeframes`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Timeframes`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_timeframes_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Timeframes) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_timeframes_async =
general_transit_feed_static_timeframes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Timeframes`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_timeframes_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Timeframes) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_timeframes_async =
general_transit_feed_static_timeframes_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_transfers_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_transfers_async:  Callable[[ConsumerRecord, CloudEvent,
Transfers], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Transfers`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Transfers`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_transfers_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Transfers)
-> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_transfers_async =
general_transit_feed_static_transfers_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Transfers`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_transfers_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Transfers)
-> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_transfers_async =
general_transit_feed_static_transfers_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_translations_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_translations_async:  Callable[[ConsumerRecord, CloudEvent,
Translations], Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Translations`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Translations`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_translations_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Translations) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_translations_async =
general_transit_feed_static_translations_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Translations`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_translations_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Translations) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_translations_async =
general_transit_feed_static_translations_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `general_transit_feed_static_trips_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'general_transit_feed_static_trips_async:  Callable[[ConsumerRecord, CloudEvent, Trips],
Awaitable[None]]

)```

```

Asynchronous handler hook for `GeneralTransitFeedStatic.Trips`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedRealTimeProducer- `data`: The event data of type `gtfs_rt_producer_data.Trips`.



Producer for `GeneralTransitFeedRealTime` message group.Example:



#### Constructor```python

async def general_transit_feed_static_trips_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Trips) -> None:

```python    # Process the event data

GeneralTransitFeedRealTimeProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_real_time_dispatcher.general_transit_feed_static_trips_async =
general_transit_feed_static_trips_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### GeneralTransitFeedStaticProducer- `data`: The event data of type `gtfs_rt_producer_data.Trips`.



Producer for `GeneralTransitFeedStatic` message group.Example:



#### Constructor```python

async def general_transit_feed_static_trips_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Trips) -> None:

```python    # Process the event data

GeneralTransitFeedStaticProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

general_transit_feed_static_dispatcher.general_transit_feed_static_trips_async = general_transit_feed_static_trips_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_general_transit_feed_static_agency`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_agency(

    self,##### `_process_event`

    data: Agency,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Agency` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Agency`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_agency(

    data=Agency(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Agency` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_agency_batch(```

    messages=[

        Agency(...),Initializes the runner with a Kafka consumer.

        Agency(...),

        Agency(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_areas`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_areas(

    self,##### `_process_event`

    data: Areas,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Areas` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Areas`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_areas(

    data=Areas(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Areas` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_areas_batch(```

    messages=[

        Areas(...),Initializes the runner with a Kafka consumer.

        Areas(...),

        Areas(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_attributions`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_attributions(

    self,##### `_process_event`

    data: Attributions,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Attributions` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Attributions`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_attributions(

    data=Attributions(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Attributions` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_attributions_batch(```

    messages=[

        Attributions(...),Initializes the runner with a Kafka consumer.

        Attributions(...),

        Attributions(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_booking_rules`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_booking_rules(

    self,##### `_process_event`

    data: BookingRules,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeed.BookingRules` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `BookingRules`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_booking_rules(

    data=BookingRules(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeed.BookingRules` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_booking_rules_batch(```

    messages=[

        BookingRules(...),Initializes the runner with a Kafka consumer.

        BookingRules(...),

        BookingRules(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_fare_attributes`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_fare_attributes(

    self,##### `_process_event`

    data: FareAttributes,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.FareAttributes` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FareAttributes`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_fare_attributes(

    data=FareAttributes(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.FareAttributes` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_fare_attributes_batch(```

    messages=[

        FareAttributes(...),Initializes the runner with a Kafka consumer.

        FareAttributes(...),

        FareAttributes(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_fare_leg_rules`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_fare_leg_rules(

    self,##### `_process_event`

    data: FareLegRules,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.FareLegRules` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FareLegRules`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_fare_leg_rules(

    data=FareLegRules(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.FareLegRules` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_fare_leg_rules_batch(```

    messages=[

        FareLegRules(...),Initializes the runner with a Kafka consumer.

        FareLegRules(...),

        FareLegRules(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_fare_media`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_fare_media(

    self,##### `_process_event`

    data: FareMedia,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.FareMedia` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FareMedia`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_fare_media(

    data=FareMedia(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.FareMedia` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_fare_media_batch(```

    messages=[

        FareMedia(...),Initializes the runner with a Kafka consumer.

        FareMedia(...),

        FareMedia(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_fare_products`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_fare_products(

    self,##### `_process_event`

    data: FareProducts,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.FareProducts` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FareProducts`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_fare_products(

    data=FareProducts(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.FareProducts` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_fare_products_batch(```

    messages=[

        FareProducts(...),Initializes the runner with a Kafka consumer.

        FareProducts(...),

        FareProducts(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_fare_rules`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_fare_rules(

    self,##### `_process_event`

    data: FareRules,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.FareRules` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FareRules`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_fare_rules(

    data=FareRules(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.FareRules` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_fare_rules_batch(```

    messages=[

        FareRules(...),Initializes the runner with a Kafka consumer.

        FareRules(...),

        FareRules(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_fare_transfer_rules`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_fare_transfer_rules(

    self,##### `_process_event`

    data: FareTransferRules,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.FareTransferRules` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FareTransferRules`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_fare_transfer_rules(

    data=FareTransferRules(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.FareTransferRules` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_fare_transfer_rules_batch(```

    messages=[

        FareTransferRules(...),Initializes the runner with a Kafka consumer.

        FareTransferRules(...),

        FareTransferRules(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_feed_info`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_feed_info(

    self,##### `_process_event`

    data: FeedInfo,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.FeedInfo` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FeedInfo`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_feed_info(

    data=FeedInfo(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.FeedInfo` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_feed_info_batch(```

    messages=[

        FeedInfo(...),Initializes the runner with a Kafka consumer.

        FeedInfo(...),

        FeedInfo(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_frequencies`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_frequencies(

    self,##### `_process_event`

    data: Frequencies,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Frequencies` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Frequencies`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_frequencies(

    data=Frequencies(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Frequencies` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_frequencies_batch(```

    messages=[

        Frequencies(...),Initializes the runner with a Kafka consumer.

        Frequencies(...),

        Frequencies(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_levels`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_levels(

    self,##### `_process_event`

    data: Levels,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Levels` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Levels`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_levels(

    data=Levels(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Levels` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_levels_batch(```

    messages=[

        Levels(...),Initializes the runner with a Kafka consumer.

        Levels(...),

        Levels(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_location_geo_json`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_location_geo_json(

    self,##### `_process_event`

    data: LocationGeoJson,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.LocationGeoJson` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `LocationGeoJson`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_location_geo_json(

    data=LocationGeoJson(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.LocationGeoJson` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_location_geo_json_batch(```

    messages=[

        LocationGeoJson(...),Initializes the runner with a Kafka consumer.

        LocationGeoJson(...),

        LocationGeoJson(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_location_groups`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_location_groups(

    self,##### `_process_event`

    data: LocationGroups,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.LocationGroups` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `LocationGroups`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_location_groups(

    data=LocationGroups(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.LocationGroups` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_location_groups_batch(```

    messages=[

        LocationGroups(...),Initializes the runner with a Kafka consumer.

        LocationGroups(...),

        LocationGroups(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_location_group_stores`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_location_group_stores(

    self,##### `_process_event`

    data: LocationGroupStores,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.LocationGroupStores` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `LocationGroupStores`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_location_group_stores(

    data=LocationGroupStores(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.LocationGroupStores` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_location_group_stores_batch(```

    messages=[

        LocationGroupStores(...),Initializes the runner with a Kafka consumer.

        LocationGroupStores(...),

        LocationGroupStores(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_networks`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_networks(

    self,##### `_process_event`

    data: Networks,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Networks` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Networks`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_networks(

    data=Networks(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Networks` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_networks_batch(```

    messages=[

        Networks(...),Initializes the runner with a Kafka consumer.

        Networks(...),

        Networks(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_pathways`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_pathways(

    self,##### `_process_event`

    data: Pathways,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Pathways` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Pathways`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_pathways(

    data=Pathways(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Pathways` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_pathways_batch(```

    messages=[

        Pathways(...),Initializes the runner with a Kafka consumer.

        Pathways(...),

        Pathways(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_route_networks`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_route_networks(

    self,##### `_process_event`

    data: RouteNetworks,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.RouteNetworks` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `RouteNetworks`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_route_networks(

    data=RouteNetworks(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.RouteNetworks` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_route_networks_batch(```

    messages=[

        RouteNetworks(...),Initializes the runner with a Kafka consumer.

        RouteNetworks(...),

        RouteNetworks(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_routes`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_routes(

    self,##### `_process_event`

    data: Routes,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Routes` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Routes`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_routes(

    data=Routes(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Routes` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_routes_batch(```

    messages=[

        Routes(...),Initializes the runner with a Kafka consumer.

        Routes(...),

        Routes(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_shapes`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_shapes(

    self,##### `_process_event`

    data: Shapes,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Shapes` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Shapes`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_shapes(

    data=Shapes(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Shapes` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_shapes_batch(```

    messages=[

        Shapes(...),Initializes the runner with a Kafka consumer.

        Shapes(...),

        Shapes(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_stop_areas`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_stop_areas(

    self,##### `_process_event`

    data: StopAreas,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.StopAreas` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StopAreas`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_stop_areas(

    data=StopAreas(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.StopAreas` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_stop_areas_batch(```

    messages=[

        StopAreas(...),Initializes the runner with a Kafka consumer.

        StopAreas(...),

        StopAreas(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_stops`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_stops(

    self,##### `_process_event`

    data: Stops,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Stops` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Stops`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_stops(

    data=Stops(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Stops` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_stops_batch(```

    messages=[

        Stops(...),Initializes the runner with a Kafka consumer.

        Stops(...),

        Stops(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_stop_times`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_stop_times(

    self,##### `_process_event`

    data: StopTimes,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.StopTimes` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StopTimes`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_stop_times(

    data=StopTimes(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.StopTimes` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_stop_times_batch(```

    messages=[

        StopTimes(...),Initializes the runner with a Kafka consumer.

        StopTimes(...),

        StopTimes(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_timeframes`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_timeframes(

    self,##### `_process_event`

    data: Timeframes,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Timeframes` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Timeframes`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_timeframes(

    data=Timeframes(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Timeframes` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_timeframes_batch(```

    messages=[

        Timeframes(...),Initializes the runner with a Kafka consumer.

        Timeframes(...),

        Timeframes(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_transfers`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_transfers(

    self,##### `_process_event`

    data: Transfers,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Transfers` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Transfers`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_transfers(

    data=Transfers(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Transfers` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_transfers_batch(```

    messages=[

        Transfers(...),Initializes the runner with a Kafka consumer.

        Transfers(...),

        Transfers(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_translations`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_translations(

    self,##### `_process_event`

    data: Translations,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Translations` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Translations`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_translations(

    data=Translations(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Translations` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_translations_batch(```

    messages=[

        Translations(...),Initializes the runner with a Kafka consumer.

        Translations(...),

        Translations(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_general_transit_feed_static_trips`Dispatchers have the following protected methods:



```python### Methods:

async def send_general_transit_feed_static_trips(

    self,##### `_process_event`

    data: Trips,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `GeneralTransitFeedStatic.Trips` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Trips`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_general_transit_feed_static_trips(

    data=Trips(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `GeneralTransitFeedStatic.Trips` messages in a batch.

### EventProcessorRunner

**Parameters:**

- `messages`: List of message data`EventProcessorRunner` is responsible for managing the event processing loop and
dispatching events to the appropriate handlers.

- `partition_key`: Optional partition key for all messages

- `headers`: Optional headers for all messages#### Methods

- `topic`: Optional topic override

##### `__init__`

**Example:**

```python

```python__init__(consumer: KafkaConsumer)

await producer.send_general_transit_feed_static_trips_batch(```

    messages=[

        Trips(...),Initializes the runner with a Kafka consumer.

        Trips(...),

        Trips(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.



#####  `__aexit__`



## Configuration Options```python

__aexit__(exc_type, exc_val, exc_tb)

### Partition Keys```



Control message distribution across partitions:Exits the asynchronous context and stops the processor.



```pythonArgs:

# Same key goes to same partition (maintains order)- `exc_type`: The exception type.

await producer.send_message(data, partition_key='device-123')- `exc_val`: The exception value.

- `exc_tb`: The exception traceback.

# Random partition assignment

await producer.send_message(data)#####  `add_dispatcher`

```

```python

### Custom Headersadd_dispatcher(dispatcher: _DispatcherBase)

```

Add application-specific metadata:

Adds a dispatcher to the runner.

```python

await producer.send_message(Args:

    data,- `dispatcher`: The dispatcher to add.

    headers={

        'priority': 'high',#####  `remove_dispatcher`

        'source': 'device-gateway',

        'correlation-id': str(uuid.uuid4())```python

    }remove_dispatcher(dispatcher: _DispatcherBase)

)```

```

Removes a dispatcher from the runner.

### Producer Configuration

Args:

```python- `dispatcher`: The dispatcher to remove.

producer = Producer(

    bootstrap_servers='localhost:9092',#####  `start()`

    # Performance tuning

    acks='all',  # Wait for all replicasStarts the event processor.

    compression_type='gzip',  # Compress messages

    linger_ms=10,  # Batch delay#####  `cancel()`

    batch_size=16384,  # Batch size in bytes

    max_in_flight_requests_per_connection=5,Cancels the event processing task.

    # Reliability

    enable_idempotence=True,  # Exactly-once semantics#####  `create_from_config`

    retries=10,  # Retry on transient failures

    # Timeouts```python

    request_timeout_ms=30000,create_from_config(cls, bootstrap_servers: str, group_id: str, topics: List[str]) ->
'EventProcessorRunner'

    delivery_timeout_ms=120000```

)

```Creates a runner from configuration.



## Error HandlingArgs:

- `bootstrap_servers`: The Kafka bootstrap servers.

```python- `group_id`: The consumer group ID.

from confluent_kafka import KafkaException- `topics`: The list of topics to subscribe to.



try:Returns:

    await producer.send_message(data)- An `EventProcessorRunner` instance.

except KafkaException as e:

    print(f"Failed to send message: {e}")### _DispatcherBase

    # Handle error (retry, log, alert, etc.)

````_DispatcherBase` is a base class for event dispatchers, handling CloudEvent detection and conversion.



## Best Practices#### Methods



1. **Reuse producer instances** - create once, use multiple times#####  `_strkey`

2. **Use partition keys** for ordered processing of related events

3. **Enable idempotence** for exactly-once delivery semantics```python

4. **Configure batching** to optimize throughput (linger_ms, batch_size)_strkey(key: str | bytes) -> str

5. **Use compression** to reduce network bandwidth (gzip, snappy, lz4)```

6. **Monitor lag** and throughput metrics

7. **Implement retry logic** with exponential backoffConverts a key to a string.



## Production-Ready PatternsArgs:

- `key`: The key to convert.

Enterprise-grade patterns for building reliable Kafka producers in Python.

#####  `_unhandled_event`

### 1. Managed Kafka Producer Pool

```python

Singleton producer pool with lifecycle management._unhandled_event(self, record, cloud_event, data)

```

```python

from confluent_kafka import ProducerDefault event handler.

from typing import Dict, Optional

import atexit#####  `_get_cloud_event_attribute`

import signal

```python

class KafkaProducerPool:_get_cloud_event_attribute(record: ConsumerRecord, key: str) -> Any

    """Singleton pool for managing Kafka producers."""```



    _producers: Dict[str, Producer] = {}Retrieves a CloudEvent attribute from a Kafka record.



    @classmethodArgs:

    def get_producer(- `record`: The Kafka record.

        cls,- `key`: The attribute key.

        bootstrap_servers: str,

        client_id: str = 'default',#####  `_is_cloud_event`

        **config

    ) -> Producer:```python

        """Get or create a producer from the pool."""_is_cloud_event(record: ConsumerRecord) -> bool

        key = f"{bootstrap_servers}-{client_id}"```



        if key not in cls._producers:Checks if the Kafka record is a CloudEvent.

            print(f"Creating new Kafka producer: {client_id}")

            Args:

            producer_config = {- `record`: The Kafka record.

                'bootstrap.servers': bootstrap_servers,

                'client.id': client_id,#####  `_cloud_event_from_record`

                'enable.idempotence': True,

                'acks': 'all',```python

                'compression.type': 'gzip',_cloud_event_from_record(record: ConsumerRecord) -> CloudEvent

                **config```

            }

            Converts a Kafka record to a CloudEvent.

            cls._producers[key] = Producer(producer_config)

        Args:

        return cls._producers[key]- `record`: The Kafka record.


    @classmethod
    def close_all(cls) -> None:
        """Close all producers in the pool."""
        print(f"Closing {len(cls._producers)} Kafka producers...")

        for key, producer in cls._producers.items():
            try:
                producer.flush(timeout=30)
                print(f"Flushed producer: {key}")
            except Exception as e:
                print(f"Error flushing producer {key}: {e}")

        cls._producers.clear()
        print("All producers closed")

# Setup graceful shutdown
def _shutdown_handler(signum, frame):
    KafkaProducerPool.close_all()
    exit(0)

signal.signal(signal.SIGTERM, _shutdown_handler)
signal.signal(signal.SIGINT, _shutdown_handler)
atexit.register(KafkaProducerPool.close_all)
```

### 2. Batch Producer with Automatic Flushing

Automatically batch messages for optimal throughput.

```python
import asyncio
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import time

@dataclass
class BatchConfig:
    max_batch_size: int = 100
    linger_ms: int = 100
    max_batch_bytes: int = 256 * 1024  # 256 KB

class BatchKafkaProducer:
    """Kafka producer with automatic batching."""

    def __init__(
        self,
        producer: Producer,
        config: Optional[BatchConfig] = None
    ):
        self.producer = producer
        self.config = config or BatchConfig()
        self.pending_messages: List[Dict[str, Any]] = []
        self.flush_task: Optional[asyncio.Task] = None
        self.lock = asyncio.Lock()

    async def send(
        self,
        topic: str,
        value: bytes,
        key: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Send a message with automatic batching."""
        async with self.lock:
            self.pending_messages.append({
                'topic': topic,
                'value': value,
                'key': key,
                'headers': headers
            })

            # Size-based trigger
            if len(self.pending_messages) >= self.config.max_batch_size:
                await self._flush()
                return

            # Time-based trigger
            if not self.flush_task or self.flush_task.done():
                self.flush_task = asyncio.create_task(
                    self._scheduled_flush()
                )

    async def _scheduled_flush(self) -> None:
        """Flush after linger time."""
        await asyncio.sleep(self.config.linger_ms / 1000)
        async with self.lock:
            await self._flush()

    async def _flush(self) -> None:
        """Flush pending messages."""
        if not self.pending_messages:
            return

        messages = self.pending_messages[:]
        self.pending_messages.clear()

        print(f"Flushing batch of {len(messages)} messages")

        # Send all messages
        for msg in messages:
            self.producer.produce(
                msg['topic'],
                value=msg['value'],
                key=msg['key'],
                headers=msg.get('headers')
            )

        # Poll to trigger delivery callbacks
        self.producer.poll(0)

        print(f"Batch flushed: {len(messages)} messages")

    async def close(self) -> None:
        """Close and flush remaining messages."""
        async with self.lock:
            await self._flush()

        # Wait for all messages to be delivered
        self.producer.flush(timeout=30)
```

### 3. Retry Logic with Exponential Backoff

Handle transient failures with configurable retry.

```python
from dataclasses import dataclass
from typing import Optional
import asyncio

@dataclass
class RetryConfig:
    max_attempts: int = 5
    initial_delay_ms: int = 500
    max_delay_ms: int = 30000
    backoff_multiplier: float = 2.0

class RetryableKafkaProducer:
    """Kafka producer with retry logic."""

    def __init__(
        self,
        producer: Producer,
        config: Optional[RetryConfig] = None
    ):
        self.producer = producer
        self.config = config or RetryConfig()

    async def send_with_retry(
        self,
        topic: str,
        value: bytes,
        key: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Send message with exponential backoff retry."""
        attempt = 0

        while attempt < self.config.max_attempts:
            try:
                # Produce message
                self.producer.produce(
                    topic,
                    value=value,
                    key=key,
                    headers=headers
                )

                # Poll to trigger callbacks
                self.producer.poll(0)

                return  # Success

            except BufferError as e:
                # Queue is full - retriable
                attempt += 1

                if attempt < self.config.max_attempts:
                    delay = min(
                        self.config.initial_delay_ms * (self.config.backoff_multiplier ** (attempt - 1)),
                        self.config.max_delay_ms
                    ) / 1000

                    print(f"Retry attempt {attempt}/{self.config.max_attempts} after {delay}s")
                    await asyncio.sleep(delay)
                else:
                    print("Max retries exceeded")
                    raise

            except Exception as e:
                # Non-retriable error
                print(f"Non-retriable error: {e}")
                raise

    @staticmethod
    def is_retriable_error(error: Exception) -> bool:
        """Check if error is retriable."""
        retriable_errors = [
            'BROKER_NOT_AVAILABLE',
            'NETWORK_EXCEPTION',
            'REQUEST_TIMED_OUT',
            'NOT_LEADER_FOR_PARTITION'
        ]

        error_str = str(error)
        return any(err in error_str for err in retriable_errors)
```

### 4. Circuit Breaker Pattern

Protect Kafka broker from being overwhelmed during failures.

```python
from enum import Enum
from dataclasses import dataclass
import time

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout_ms: int = 60000

class CircuitBreakerKafkaProducer:
    """Kafka producer with circuit breaker."""

    def __init__(
        self,
        producer: Producer,
        config: Optional[CircuitBreakerConfig] = None
    ):
        self.producer = producer
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.successes = 0
        self.last_failure_time = 0
        self.fallback_queue: List[Dict[str, Any]] = []

    async def send(
        self,
        topic: str,
        value: bytes,
        key: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Send message with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            elapsed = (time.time() * 1000) - self.last_failure_time

            if elapsed > self.config.timeout_ms:
                print("Circuit breaker transitioning to HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self.successes = 0
            else:
                print("Circuit breaker is OPEN, queuing message")
                self.fallback_queue.append({
                    'topic': topic,
                    'value': value,
                    'key': key,
                    'headers': headers
                })
                return

        try:
            self.producer.produce(topic, value=value, key=key, headers=headers)
            self.producer.poll(0)
            self._on_success()

            # Flush fallback queue on recovery
            if self.state == CircuitState.CLOSED and self.fallback_queue:
                await self._flush_fallback_queue()

        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        """Handle successful send."""
        self.failures = 0

        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1

            if self.successes >= self.config.success_threshold:
                print("Circuit breaker transitioning to CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0

    def _on_failure(self) -> None:
        """Handle failed send."""
        self.failures += 1
        self.last_failure_time = time.time() * 1000

        if self.failures >= self.config.failure_threshold:
            print("Circuit breaker transitioning to OPEN")
            self.state = CircuitState.OPEN
            self.failures = 0

    async def _flush_fallback_queue(self) -> None:
        """Flush messages from fallback queue."""
        print(f"Flushing {len(self.fallback_queue)} queued messages...")

        queue = self.fallback_queue[:]
        self.fallback_queue.clear()

        for msg in queue:
            try:
                await self.send(
                    msg['topic'],
                    msg['value'],
                    msg['key'],
                    msg['headers']
                )
            except Exception as e:
                print(f"Failed to flush message: {e}")
                self.fallback_queue.append(msg)

    def get_state(self) -> CircuitState:
        """Get current circuit breaker state."""
        return self.state
```

### 5. Rate Limiting

Control send rate to prevent broker overload.

```python
import asyncio
import time

class RateLimitedKafkaProducer:
    """Kafka producer with token bucket rate limiting."""

    def __init__(
        self,
        producer: Producer,
        messages_per_second: int
    ):
        self.producer = producer
        self.tokens_per_second = messages_per_second
        self.available_tokens = float(messages_per_second)
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

        # Start refill task
        asyncio.create_task(self._refill_tokens())

    async def _refill_tokens(self) -> None:
        """Periodically refill tokens."""
        while True:
            await asyncio.sleep(0.1)  # 100ms

            async with self.lock:
                now = time.time()
                elapsed = now - self.last_refill
                tokens_to_add = elapsed * self.tokens_per_second

                self.available_tokens = min(
                    self.available_tokens + tokens_to_add,
                    self.tokens_per_second
                )

                self.last_refill = now

    async def _acquire_token(self) -> None:
        """Acquire a token (blocks if none available)."""
        while True:
            async with self.lock:
                if self.available_tokens >= 1:
                    self.available_tokens -= 1
                    return

            await asyncio.sleep(0.05)  # 50ms

    async def send(
        self,
        topic: str,
        value: bytes,
        key: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Send message with rate limiting."""
        await self._acquire_token()

        self.producer.produce(topic, value=value, key=key, headers=headers)
        self.producer.poll(0)

    def get_available_tokens(self) -> float:
        """Get current token count."""
        return self.available_tokens
```

### 6. OpenTelemetry Observability

Instrument Kafka producer with distributed tracing and metrics.

```python
from opentelemetry import trace, metrics
from opentelemetry.trace import Status, StatusCode
import time

tracer = trace.get_tracer("kafka-producer")
meter = metrics.get_meter("kafka-producer")

messages_sent = meter.create_counter(
    "kafka.messages.sent",
    description="Number of messages sent"
)

send_duration = meter.create_histogram(
    "kafka.send.duration",
    description="Message send duration in milliseconds"
)

class ObservableKafkaProducer:
    """Kafka producer with OpenTelemetry instrumentation."""

    def __init__(self, producer: Producer):
        self.producer = producer

    async def send(
        self,
        topic: str,
        value: bytes,
        key: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Send message with tracing and metrics."""
        with tracer.start_as_current_span(
            "kafka.send",
            kind=trace.SpanKind.PRODUCER,
            attributes={
                "messaging.system": "kafka",
                "messaging.destination": topic,
                "messaging.protocol": "kafka",
                "messaging.message_payload_size_bytes": len(value)
            }
        ) as span:
            start_time = time.time()

            try:
                # Inject trace context into headers
                headers_dict = headers or {}
                from opentelemetry.propagate import inject
                inject(headers_dict)

                # Send message
                self.producer.produce(
                    topic,
                    value=value,
                    key=key,
                    headers=list(headers_dict.items()) if headers_dict else None
                )

                self.producer.poll(0)

                # Record success
                span.set_status(Status(StatusCode.OK))

                duration_ms = (time.time() - start_time) * 1000

                messages_sent.add(1, {"topic": topic, "status": "success"})
                send_duration.record(duration_ms, {"topic": topic})

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))

                messages_sent.add(1, {"topic": topic, "status": "error"})

                raise
```

### 7. Graceful Shutdown

Ensure all messages are sent before shutdown.

```python
import asyncio
import signal
import atexit

class GracefulKafkaProducer:
    """Kafka producer with graceful shutdown."""

    def __init__(self, producer: Producer):
        self.producer = producer
        self.pending_sends = 0
        self.is_shutting_down = False
        self.lock = asyncio.Lock()

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._shutdown_handler)
        signal.signal(signal.SIGINT, self._shutdown_handler)
        atexit.register(self._shutdown)

    async def send(
        self,
        topic: str,
        value: bytes,
        key: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Send message with pending count tracking."""
        if self.is_shutting_down:
            raise RuntimeError("Producer is shutting down")

        async with self.lock:
            self.pending_sends += 1

        try:
            self.producer.produce(topic, value=value, key=key, headers=headers)
            self.producer.poll(0)
        finally:
            async with self.lock:
                self.pending_sends -= 1

    def _shutdown_handler(self, signum, frame):
        """Handle shutdown signals."""
        asyncio.create_task(self._shutdown())

    async def _shutdown(self) -> None:
        """Graceful shutdown."""
        if self.is_shutting_down:
            return

        print("Initiating graceful shutdown...")
        self.is_shutting_down = True

        # Wait for pending sends (up to 30 seconds)
        timeout = 30
        elapsed = 0

        while self.pending_sends > 0 and elapsed < timeout:
            print(f"Waiting for {self.pending_sends} pending sends...")
            await asyncio.sleep(1)
            elapsed += 1

        if self.pending_sends > 0:
            print(f"Warning: {self.pending_sends} messages not sent")
        else:
            print("All messages sent")

        # Flush remaining messages
        self.producer.flush(timeout=30)
        print("Kafka producer closed")

    def get_pending_count(self) -> int:
        """Get pending send count."""
        return self.pending_sends
```

### Integration Example

```python
import asyncio
from confluent_kafka import Producer

async def main():
    # 1. Get producer from pool
    producer = KafkaProducerPool.get_producer(
        bootstrap_servers='localhost:9092',
        client_id='my-app'
    )

    # 2. Initialize patterns
    batch_producer = BatchKafkaProducer(producer, BatchConfig(
        max_batch_size=100,
        linger_ms=100
    ))

    retry_producer = RetryableKafkaProducer(producer, RetryConfig(
        max_attempts=5,
        initial_delay_ms=500
    ))

    circuit_breaker = CircuitBreakerKafkaProducer(producer, CircuitBreakerConfig(
        failure_threshold=5,
        timeout_ms=60000
    ))

    rate_limiter = RateLimitedKafkaProducer(producer, messages_per_second=1000)

    observable = ObservableKafkaProducer(producer)

    graceful = GracefulKafkaProducer(producer)

    # 3. Send messages with patterns
    message = b'{"temperature": 25.5, "humidity": 60}'

    # Batch sending
    await batch_producer.send('sensor-data', message, key=b'device-001')

    # With retry
    await retry_producer.send_with_retry('sensor-data', message)

    # Circuit breaker
    await circuit_breaker.send('sensor-data', message)

    # Rate limited
    await rate_limiter.send('sensor-data', message)

    # Observable
    await observable.send('sensor-data', message)

    # Graceful (handles signals)
    await graceful.send('sensor-data', message)

    # Flush batch
    await batch_producer.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### Dependencies

Add these packages to your `requirements.txt`:

```
confluent-kafka>=2.3.0
cloudevents>=1.10.0
pydantic>=2.5.0
opentelemetry-api>=1.21.0
pybreaker>=1.0.0
tenacity>=8.2.0
```
