

# Aisstream-producer Kafka Producer# Aisstream-producer Event Dispatcher for Apache Kafka



This module provides a type-safe Kafka producer for sending CloudEvents and plain Kafka messages.This module provides an
event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages and CloudEvents.



## Table of Contents## Table of Contents

1. [Overview](#overview)1. [Overview](#overview)

2. [What is Apache Kafka?](#what-is-apache-kafka)2. [Generated Event Dispatchers](#generated-event-dispatchers)

3. [Quick Start](#quick-start)    - IOAISstreamEventDispatcher

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

- IOAISstreamProducersolution for event-driven applications.



## Generated Event Dispatchers

## What is Apache Kafka?



**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### IOAISstreamEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`IOAISstreamEventDispatcher` handles events for the IO.AISstream message group.

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

from aisstream-producer import IOAISstreamProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = IOAISstreamProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_io_aisstream_position_report(```python

    data=PositionReport(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The IOAISstreamEventDispatcher defines the following event handler hooks.

```python

producer = IOAISstreamProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_position_report_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_position_report_async:  Callable[[ConsumerRecord, CloudEvent,
PositionReport], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.PositionReport`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.PositionReport`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_position_report_event(record: ConsumerRecord, cloud_event: CloudEvent, data: PositionReport) ->
None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_position_report_async = io_aisstream_position_report_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_ship_static_data_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_ship_static_data_async:  Callable[[ConsumerRecord, CloudEvent,
ShipStaticData], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.ShipStaticData`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.ShipStaticData`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_ship_static_data_event(record: ConsumerRecord, cloud_event: CloudEvent, data: ShipStaticData) ->
None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_ship_static_data_async = io_aisstream_ship_static_data_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_standard_class_bposition_report_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_standard_class_bposition_report_async:  Callable[[ConsumerRecord,
CloudEvent, StandardClassBPositionReport], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.StandardClassBPositionReport`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.StandardClassBPositionReport`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_standard_class_bposition_report_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StandardClassBPositionReport) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_standard_class_bposition_report_async =
io_aisstream_standard_class_bposition_report_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_extended_class_bposition_report_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_extended_class_bposition_report_async:  Callable[[ConsumerRecord,
CloudEvent, ExtendedClassBPositionReport], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.ExtendedClassBPositionReport`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.ExtendedClassBPositionReport`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_extended_class_bposition_report_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
ExtendedClassBPositionReport) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_extended_class_bposition_report_async =
io_aisstream_extended_class_bposition_report_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_aids_to_navigation_report_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_aids_to_navigation_report_async:  Callable[[ConsumerRecord, CloudEvent,
AidsToNavigationReport], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.AidsToNavigationReport`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.AidsToNavigationReport`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_aids_to_navigation_report_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AidsToNavigationReport) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_aids_to_navigation_report_async = io_aisstream_aids_to_navigation_report_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_static_data_report_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_static_data_report_async:  Callable[[ConsumerRecord, CloudEvent,
StaticDataReport], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.StaticDataReport`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.StaticDataReport`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_static_data_report_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StaticDataReport)
-> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_static_data_report_async = io_aisstream_static_data_report_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_base_station_report_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_base_station_report_async:  Callable[[ConsumerRecord, CloudEvent,
BaseStationReport], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.BaseStationReport`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.BaseStationReport`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_base_station_report_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
BaseStationReport) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_base_station_report_async = io_aisstream_base_station_report_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_safety_broadcast_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_safety_broadcast_message_async:  Callable[[ConsumerRecord, CloudEvent,
SafetyBroadcastMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.SafetyBroadcastMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.SafetyBroadcastMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_safety_broadcast_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SafetyBroadcastMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_safety_broadcast_message_async = io_aisstream_safety_broadcast_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_standard_search_and_rescue_aircraft_report_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_standard_search_and_rescue_aircraft_report_async:
Callable[[ConsumerRecord, CloudEvent, StandardSearchAndRescueAircraftReport], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.StandardSearchAndRescueAircraftReport`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.StandardSearchAndRescueAircraftReport`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_standard_search_and_rescue_aircraft_report_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: StandardSearchAndRescueAircraftReport) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_standard_search_and_rescue_aircraft_report_async =
io_aisstream_standard_search_and_rescue_aircraft_report_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_long_range_ais_broadcast_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_long_range_ais_broadcast_message_async:  Callable[[ConsumerRecord,
CloudEvent, LongRangeAisBroadcastMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.LongRangeAisBroadcastMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.LongRangeAisBroadcastMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_long_range_ais_broadcast_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LongRangeAisBroadcastMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_long_range_ais_broadcast_message_async =
io_aisstream_long_range_ais_broadcast_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_addressed_safety_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_addressed_safety_message_async:  Callable[[ConsumerRecord, CloudEvent,
AddressedSafetyMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.AddressedSafetyMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.AddressedSafetyMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_addressed_safety_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AddressedSafetyMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_addressed_safety_message_async = io_aisstream_addressed_safety_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_addressed_binary_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_addressed_binary_message_async:  Callable[[ConsumerRecord, CloudEvent,
AddressedBinaryMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.AddressedBinaryMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.AddressedBinaryMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_addressed_binary_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AddressedBinaryMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_addressed_binary_message_async = io_aisstream_addressed_binary_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_assigned_mode_command_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_assigned_mode_command_async:  Callable[[ConsumerRecord, CloudEvent,
AssignedModeCommand], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.AssignedModeCommand`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.AssignedModeCommand`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_assigned_mode_command_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AssignedModeCommand) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_assigned_mode_command_async = io_aisstream_assigned_mode_command_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_binary_acknowledge_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_binary_acknowledge_async:  Callable[[ConsumerRecord, CloudEvent,
BinaryAcknowledge], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.BinaryAcknowledge`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.BinaryAcknowledge`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_binary_acknowledge_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
BinaryAcknowledge) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_binary_acknowledge_async = io_aisstream_binary_acknowledge_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_binary_broadcast_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_binary_broadcast_message_async:  Callable[[ConsumerRecord, CloudEvent,
BinaryBroadcastMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.BinaryBroadcastMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.BinaryBroadcastMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_binary_broadcast_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
BinaryBroadcastMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_binary_broadcast_message_async = io_aisstream_binary_broadcast_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_channel_management_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_channel_management_async:  Callable[[ConsumerRecord, CloudEvent,
ChannelManagement], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.ChannelManagement`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.ChannelManagement`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_channel_management_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
ChannelManagement) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_channel_management_async = io_aisstream_channel_management_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_coordinated_utcinquiry_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_coordinated_utcinquiry_async:  Callable[[ConsumerRecord, CloudEvent,
CoordinatedUTCInquiry], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.CoordinatedUTCInquiry`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.CoordinatedUTCInquiry`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_coordinated_utcinquiry_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
CoordinatedUTCInquiry) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_coordinated_utcinquiry_async = io_aisstream_coordinated_utcinquiry_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_data_link_management_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_data_link_management_message_async:  Callable[[ConsumerRecord, CloudEvent,
DataLinkManagementMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.DataLinkManagementMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.DataLinkManagementMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_data_link_management_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
DataLinkManagementMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_data_link_management_message_async =
io_aisstream_data_link_management_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_gnss_broadcast_binary_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_gnss_broadcast_binary_message_async:  Callable[[ConsumerRecord,
CloudEvent, GnssBroadcastBinaryMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.GnssBroadcastBinaryMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.GnssBroadcastBinaryMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_gnss_broadcast_binary_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
GnssBroadcastBinaryMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_gnss_broadcast_binary_message_async =
io_aisstream_gnss_broadcast_binary_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_group_assignment_command_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_group_assignment_command_async:  Callable[[ConsumerRecord, CloudEvent,
GroupAssignmentCommand], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.GroupAssignmentCommand`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.GroupAssignmentCommand`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_group_assignment_command_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
GroupAssignmentCommand) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_group_assignment_command_async = io_aisstream_group_assignment_command_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_interrogation_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_interrogation_async:  Callable[[ConsumerRecord, CloudEvent,
Interrogation], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.Interrogation`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.Interrogation`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_interrogation_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Interrogation) ->
None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_interrogation_async = io_aisstream_interrogation_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_multi_slot_binary_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_multi_slot_binary_message_async:  Callable[[ConsumerRecord, CloudEvent,
MultiSlotBinaryMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.MultiSlotBinaryMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.MultiSlotBinaryMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_multi_slot_binary_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
MultiSlotBinaryMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_multi_slot_binary_message_async = io_aisstream_multi_slot_binary_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `io_aisstream_single_slot_binary_message_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'io_aisstream_single_slot_binary_message_async:  Callable[[ConsumerRecord, CloudEvent,
SingleSlotBinaryMessage], Awaitable[None]]

)```

```

Asynchronous handler hook for `IO.AISstream.SingleSlotBinaryMessage`:

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### IOAISstreamProducer- `data`: The event data of type `aisstream_producer_data.SingleSlotBinaryMessage`.



Producer for `IO.AISstream` message group.Example:



#### Constructor```python

async def io_aisstream_single_slot_binary_message_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SingleSlotBinaryMessage) -> None:

```python    # Process the event data

IOAISstreamProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

io_aisstream_dispatcher.io_aisstream_single_slot_binary_message_async = io_aisstream_single_slot_binary_message_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_io_aisstream_position_report`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_position_report(

    self,##### `_process_event`

    data: PositionReport,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.PositionReport` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `PositionReport`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_position_report(

    data=PositionReport(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.PositionReport` messages in a batch.

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

await producer.send_io_aisstream_position_report_batch(```

    messages=[

        PositionReport(...),Initializes the runner with a Kafka consumer.

        PositionReport(...),

        PositionReport(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_ship_static_data`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_ship_static_data(

    self,##### `_process_event`

    data: ShipStaticData,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.ShipStaticData` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `ShipStaticData`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_ship_static_data(

    data=ShipStaticData(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.ShipStaticData` messages in a batch.

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

await producer.send_io_aisstream_ship_static_data_batch(```

    messages=[

        ShipStaticData(...),Initializes the runner with a Kafka consumer.

        ShipStaticData(...),

        ShipStaticData(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_standard_class_bposition_report`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_standard_class_bposition_report(

    self,##### `_process_event`

    data: StandardClassBPositionReport,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.StandardClassBPositionReport` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StandardClassBPositionReport`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_standard_class_bposition_report(

    data=StandardClassBPositionReport(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.StandardClassBPositionReport` messages in a batch.

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

await producer.send_io_aisstream_standard_class_bposition_report_batch(```

    messages=[

        StandardClassBPositionReport(...),Initializes the runner with a Kafka consumer.

        StandardClassBPositionReport(...),

        StandardClassBPositionReport(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_extended_class_bposition_report`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_extended_class_bposition_report(

    self,##### `_process_event`

    data: ExtendedClassBPositionReport,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.ExtendedClassBPositionReport` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `ExtendedClassBPositionReport`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_extended_class_bposition_report(

    data=ExtendedClassBPositionReport(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.ExtendedClassBPositionReport` messages in a batch.

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

await producer.send_io_aisstream_extended_class_bposition_report_batch(```

    messages=[

        ExtendedClassBPositionReport(...),Initializes the runner with a Kafka consumer.

        ExtendedClassBPositionReport(...),

        ExtendedClassBPositionReport(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_aids_to_navigation_report`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_aids_to_navigation_report(

    self,##### `_process_event`

    data: AidsToNavigationReport,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.AidsToNavigationReport` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `AidsToNavigationReport`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_aids_to_navigation_report(

    data=AidsToNavigationReport(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.AidsToNavigationReport` messages in a batch.

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

await producer.send_io_aisstream_aids_to_navigation_report_batch(```

    messages=[

        AidsToNavigationReport(...),Initializes the runner with a Kafka consumer.

        AidsToNavigationReport(...),

        AidsToNavigationReport(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_static_data_report`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_static_data_report(

    self,##### `_process_event`

    data: StaticDataReport,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.StaticDataReport` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StaticDataReport`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_static_data_report(

    data=StaticDataReport(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.StaticDataReport` messages in a batch.

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

await producer.send_io_aisstream_static_data_report_batch(```

    messages=[

        StaticDataReport(...),Initializes the runner with a Kafka consumer.

        StaticDataReport(...),

        StaticDataReport(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_base_station_report`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_base_station_report(

    self,##### `_process_event`

    data: BaseStationReport,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.BaseStationReport` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `BaseStationReport`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_base_station_report(

    data=BaseStationReport(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.BaseStationReport` messages in a batch.

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

await producer.send_io_aisstream_base_station_report_batch(```

    messages=[

        BaseStationReport(...),Initializes the runner with a Kafka consumer.

        BaseStationReport(...),

        BaseStationReport(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_safety_broadcast_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_safety_broadcast_message(

    self,##### `_process_event`

    data: SafetyBroadcastMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.SafetyBroadcastMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SafetyBroadcastMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_safety_broadcast_message(

    data=SafetyBroadcastMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.SafetyBroadcastMessage` messages in a batch.

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

await producer.send_io_aisstream_safety_broadcast_message_batch(```

    messages=[

        SafetyBroadcastMessage(...),Initializes the runner with a Kafka consumer.

        SafetyBroadcastMessage(...),

        SafetyBroadcastMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_standard_search_and_rescue_aircraft_report`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_standard_search_and_rescue_aircraft_report(

    self,##### `_process_event`

    data: StandardSearchAndRescueAircraftReport,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.StandardSearchAndRescueAircraftReport` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StandardSearchAndRescueAircraftReport`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_standard_search_and_rescue_aircraft_report(

    data=StandardSearchAndRescueAircraftReport(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.StandardSearchAndRescueAircraftReport` messages in a batch.

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

await producer.send_io_aisstream_standard_search_and_rescue_aircraft_report_batch(```

    messages=[

        StandardSearchAndRescueAircraftReport(...),Initializes the runner with a Kafka consumer.

        StandardSearchAndRescueAircraftReport(...),

        StandardSearchAndRescueAircraftReport(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_long_range_ais_broadcast_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_long_range_ais_broadcast_message(

    self,##### `_process_event`

    data: LongRangeAisBroadcastMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.LongRangeAisBroadcastMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `LongRangeAisBroadcastMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_long_range_ais_broadcast_message(

    data=LongRangeAisBroadcastMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.LongRangeAisBroadcastMessage` messages in a batch.

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

await producer.send_io_aisstream_long_range_ais_broadcast_message_batch(```

    messages=[

        LongRangeAisBroadcastMessage(...),Initializes the runner with a Kafka consumer.

        LongRangeAisBroadcastMessage(...),

        LongRangeAisBroadcastMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_addressed_safety_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_addressed_safety_message(

    self,##### `_process_event`

    data: AddressedSafetyMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.AddressedSafetyMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `AddressedSafetyMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_addressed_safety_message(

    data=AddressedSafetyMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.AddressedSafetyMessage` messages in a batch.

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

await producer.send_io_aisstream_addressed_safety_message_batch(```

    messages=[

        AddressedSafetyMessage(...),Initializes the runner with a Kafka consumer.

        AddressedSafetyMessage(...),

        AddressedSafetyMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_addressed_binary_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_addressed_binary_message(

    self,##### `_process_event`

    data: AddressedBinaryMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.AddressedBinaryMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `AddressedBinaryMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_addressed_binary_message(

    data=AddressedBinaryMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.AddressedBinaryMessage` messages in a batch.

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

await producer.send_io_aisstream_addressed_binary_message_batch(```

    messages=[

        AddressedBinaryMessage(...),Initializes the runner with a Kafka consumer.

        AddressedBinaryMessage(...),

        AddressedBinaryMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_assigned_mode_command`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_assigned_mode_command(

    self,##### `_process_event`

    data: AssignedModeCommand,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.AssignedModeCommand` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `AssignedModeCommand`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_assigned_mode_command(

    data=AssignedModeCommand(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.AssignedModeCommand` messages in a batch.

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

await producer.send_io_aisstream_assigned_mode_command_batch(```

    messages=[

        AssignedModeCommand(...),Initializes the runner with a Kafka consumer.

        AssignedModeCommand(...),

        AssignedModeCommand(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_binary_acknowledge`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_binary_acknowledge(

    self,##### `_process_event`

    data: BinaryAcknowledge,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.BinaryAcknowledge` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `BinaryAcknowledge`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_binary_acknowledge(

    data=BinaryAcknowledge(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.BinaryAcknowledge` messages in a batch.

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

await producer.send_io_aisstream_binary_acknowledge_batch(```

    messages=[

        BinaryAcknowledge(...),Initializes the runner with a Kafka consumer.

        BinaryAcknowledge(...),

        BinaryAcknowledge(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_binary_broadcast_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_binary_broadcast_message(

    self,##### `_process_event`

    data: BinaryBroadcastMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.BinaryBroadcastMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `BinaryBroadcastMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_binary_broadcast_message(

    data=BinaryBroadcastMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.BinaryBroadcastMessage` messages in a batch.

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

await producer.send_io_aisstream_binary_broadcast_message_batch(```

    messages=[

        BinaryBroadcastMessage(...),Initializes the runner with a Kafka consumer.

        BinaryBroadcastMessage(...),

        BinaryBroadcastMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_channel_management`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_channel_management(

    self,##### `_process_event`

    data: ChannelManagement,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.ChannelManagement` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `ChannelManagement`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_channel_management(

    data=ChannelManagement(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.ChannelManagement` messages in a batch.

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

await producer.send_io_aisstream_channel_management_batch(```

    messages=[

        ChannelManagement(...),Initializes the runner with a Kafka consumer.

        ChannelManagement(...),

        ChannelManagement(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_coordinated_utcinquiry`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_coordinated_utcinquiry(

    self,##### `_process_event`

    data: CoordinatedUTCInquiry,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.CoordinatedUTCInquiry` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `CoordinatedUTCInquiry`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_coordinated_utcinquiry(

    data=CoordinatedUTCInquiry(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.CoordinatedUTCInquiry` messages in a batch.

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

await producer.send_io_aisstream_coordinated_utcinquiry_batch(```

    messages=[

        CoordinatedUTCInquiry(...),Initializes the runner with a Kafka consumer.

        CoordinatedUTCInquiry(...),

        CoordinatedUTCInquiry(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_data_link_management_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_data_link_management_message(

    self,##### `_process_event`

    data: DataLinkManagementMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.DataLinkManagementMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DataLinkManagementMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_data_link_management_message(

    data=DataLinkManagementMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.DataLinkManagementMessage` messages in a batch.

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

await producer.send_io_aisstream_data_link_management_message_batch(```

    messages=[

        DataLinkManagementMessage(...),Initializes the runner with a Kafka consumer.

        DataLinkManagementMessage(...),

        DataLinkManagementMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_gnss_broadcast_binary_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_gnss_broadcast_binary_message(

    self,##### `_process_event`

    data: GnssBroadcastBinaryMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.GnssBroadcastBinaryMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `GnssBroadcastBinaryMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_gnss_broadcast_binary_message(

    data=GnssBroadcastBinaryMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.GnssBroadcastBinaryMessage` messages in a batch.

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

await producer.send_io_aisstream_gnss_broadcast_binary_message_batch(```

    messages=[

        GnssBroadcastBinaryMessage(...),Initializes the runner with a Kafka consumer.

        GnssBroadcastBinaryMessage(...),

        GnssBroadcastBinaryMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_group_assignment_command`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_group_assignment_command(

    self,##### `_process_event`

    data: GroupAssignmentCommand,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.GroupAssignmentCommand` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `GroupAssignmentCommand`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_group_assignment_command(

    data=GroupAssignmentCommand(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.GroupAssignmentCommand` messages in a batch.

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

await producer.send_io_aisstream_group_assignment_command_batch(```

    messages=[

        GroupAssignmentCommand(...),Initializes the runner with a Kafka consumer.

        GroupAssignmentCommand(...),

        GroupAssignmentCommand(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_interrogation`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_interrogation(

    self,##### `_process_event`

    data: Interrogation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.Interrogation` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Interrogation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_interrogation(

    data=Interrogation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.Interrogation` messages in a batch.

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

await producer.send_io_aisstream_interrogation_batch(```

    messages=[

        Interrogation(...),Initializes the runner with a Kafka consumer.

        Interrogation(...),

        Interrogation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_multi_slot_binary_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_multi_slot_binary_message(

    self,##### `_process_event`

    data: MultiSlotBinaryMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.MultiSlotBinaryMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `MultiSlotBinaryMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_multi_slot_binary_message(

    data=MultiSlotBinaryMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.MultiSlotBinaryMessage` messages in a batch.

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

await producer.send_io_aisstream_multi_slot_binary_message_batch(```

    messages=[

        MultiSlotBinaryMessage(...),Initializes the runner with a Kafka consumer.

        MultiSlotBinaryMessage(...),

        MultiSlotBinaryMessage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_io_aisstream_single_slot_binary_message`Dispatchers have the following protected methods:



```python### Methods:

async def send_io_aisstream_single_slot_binary_message(

    self,##### `_process_event`

    data: SingleSlotBinaryMessage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `IO.AISstream.SingleSlotBinaryMessage` message.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SingleSlotBinaryMessage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_io_aisstream_single_slot_binary_message(

    data=SingleSlotBinaryMessage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `IO.AISstream.SingleSlotBinaryMessage` messages in a batch.

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

await producer.send_io_aisstream_single_slot_binary_message_batch(```

    messages=[

        SingleSlotBinaryMessage(...),Initializes the runner with a Kafka consumer.

        SingleSlotBinaryMessage(...),

        SingleSlotBinaryMessage(...)Args:

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
