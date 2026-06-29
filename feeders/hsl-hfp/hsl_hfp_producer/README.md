

# Hsl_hfp_producer Kafka Producer# Hsl_hfp_producer Event Dispatcher for Apache Kafka



This module provides a type-safe Kafka producer for sending CloudEvents and plain Kafka messages.This module provides an
event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages and CloudEvents.



## Table of Contents## Table of Contents

1. [Overview](#overview)1. [Overview](#overview)

2. [What is Apache Kafka?](#what-is-apache-kafka)2. [Generated Event Dispatchers](#generated-event-dispatchers)

3. [Quick Start](#quick-start)    - FiHslHfpEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsOperatorEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsRouteEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsStopEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslHfpMqttEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslHfpAmqpEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsOperatorMqttEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsOperatorAmqpEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsRouteMqttEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsRouteAmqpEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsStopMqttEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    FiHslGtfsStopAmqpEventDispatcher

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

- FiHslHfpProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsOperatorProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsRouteProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsStopProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslHfpMqttProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslHfpAmqpProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsOperatorMqttProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsOperatorAmqpProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsRouteMqttProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsRouteAmqpProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsStopMqttProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- FiHslGtfsStopAmqpProducersolution for event-driven applications.



## Generated Event Dispatchers

## What is Apache Kafka?



**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslHfpEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslHfpEventDispatcher` handles events for the fi.hsl.hfp message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslHfpEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_vp_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_vp_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.vp`: Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an ongoing
public journey.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_vp_async = fi_hsl_hfp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_due_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_due_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.due`: The vehicle will soon arrive at a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_due_async = fi_hsl_hfp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_arr_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_arr_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.arr`: The vehicle has arrived inside a stop's radius.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_arr_async = fi_hsl_hfp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_dep_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_dep_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.dep`: The vehicle has departed and left a stop's radius.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_dep_async = fi_hsl_hfp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_ars_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_ars_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.ars`: The vehicle has arrived at a stop (stop-position event).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_ars_async = fi_hsl_hfp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_pde_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_pde_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.pde`: The vehicle is ready to depart from a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_pde_async = fi_hsl_hfp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_pas_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_pas_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.pas`: The vehicle passes through a stop without stopping.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_pas_async = fi_hsl_hfp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_wait_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_wait_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.wait`: The vehicle is waiting at a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_wait_async = fi_hsl_hfp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_doo_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_doo_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.doo`: The doors of the vehicle have been opened.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_doo_async = fi_hsl_hfp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_doc_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_doc_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.doc`: The doors of the vehicle have been closed.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_doc_async = fi_hsl_hfp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_vja_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_vja_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.vja`: The vehicle signs in to a service journey (trip).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_vja_async = fi_hsl_hfp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_vjout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_vjout_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.vjout`: The vehicle signs off from a service journey after the final stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_vjout_async = fi_hsl_hfp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_tlr_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_tlr_async:  Callable[[ConsumerRecord, CloudEvent, TrafficLightEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.tlr`: The vehicle requests traffic-light priority at a junction.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_tlr_async = fi_hsl_hfp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_tla_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_tla_async:  Callable[[ConsumerRecord, CloudEvent, TrafficLightEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.tla`: The vehicle receives a response to a traffic-light priority request.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_tla_async = fi_hsl_hfp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_da_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_da_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.da`: A driver signs in to the vehicle.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_da_async = fi_hsl_hfp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_dout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_dout_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.dout`: A driver signs out of the vehicle.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_dout_async = fi_hsl_hfp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_ba_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_ba_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.ba`: A driver selects the block the vehicle will run.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_ba_async = fi_hsl_hfp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_bout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_bout_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.bout`: A driver signs out from the selected block (usually at a depot).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_bout_async = fi_hsl_hfp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_hfp_vp`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_vp(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.vp` message. Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an ongoing public
journey.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_vp(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.vp` messages in a batch.

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

await producer.send_fi_hsl_hfp_vp_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_due`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_due(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.due` message. The vehicle will soon arrive at a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_due(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.due` messages in a batch.

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

await producer.send_fi_hsl_hfp_due_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_arr`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_arr(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.arr` message. The vehicle has arrived inside a stop's radius.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_arr(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.arr` messages in a batch.

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

await producer.send_fi_hsl_hfp_arr_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_dep`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_dep(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.dep` message. The vehicle has departed and left a stop's radius.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_dep(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.dep` messages in a batch.

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

await producer.send_fi_hsl_hfp_dep_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_ars`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_ars(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.ars` message. The vehicle has arrived at a stop (stop-position event).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_ars(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.ars` messages in a batch.

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

await producer.send_fi_hsl_hfp_ars_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_pde`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_pde(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.pde` message. The vehicle is ready to depart from a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_pde(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.pde` messages in a batch.

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

await producer.send_fi_hsl_hfp_pde_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_pas`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_pas(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.pas` message. The vehicle passes through a stop without stopping.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_pas(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.pas` messages in a batch.

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

await producer.send_fi_hsl_hfp_pas_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_wait`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_wait(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.wait` message. The vehicle is waiting at a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_wait(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.wait` messages in a batch.

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

await producer.send_fi_hsl_hfp_wait_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_doo`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_doo(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.doo` message. The doors of the vehicle have been opened.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_doo(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.doo` messages in a batch.

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

await producer.send_fi_hsl_hfp_doo_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_doc`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_doc(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.doc` message. The doors of the vehicle have been closed.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_doc(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.doc` messages in a batch.

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

await producer.send_fi_hsl_hfp_doc_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_vja`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_vja(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.vja` message. The vehicle signs in to a service journey (trip).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_vja(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.vja` messages in a batch.

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

await producer.send_fi_hsl_hfp_vja_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_vjout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_vjout(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.vjout` message. The vehicle signs off from a service journey after the final stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_vjout(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.vjout` messages in a batch.

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

await producer.send_fi_hsl_hfp_vjout_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_tlr`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_tlr(

    self,##### `_process_event`

    data: TrafficLightEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.tlr` message. The vehicle requests traffic-light priority at a junction.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TrafficLightEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_tlr(

    data=TrafficLightEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.tlr` messages in a batch.

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

await producer.send_fi_hsl_hfp_tlr_batch(```

    messages=[

        TrafficLightEvent(...),Initializes the runner with a Kafka consumer.

        TrafficLightEvent(...),

        TrafficLightEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_tla`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_tla(

    self,##### `_process_event`

    data: TrafficLightEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.tla` message. The vehicle receives a response to a traffic-light priority request.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TrafficLightEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_tla(

    data=TrafficLightEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.tla` messages in a batch.

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

await producer.send_fi_hsl_hfp_tla_batch(```

    messages=[

        TrafficLightEvent(...),Initializes the runner with a Kafka consumer.

        TrafficLightEvent(...),

        TrafficLightEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_da`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_da(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.da` message. A driver signs in to the vehicle.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_da(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.da` messages in a batch.

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

await producer.send_fi_hsl_hfp_da_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_dout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_dout(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.dout` message. A driver signs out of the vehicle.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_dout(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.dout` messages in a batch.

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

await producer.send_fi_hsl_hfp_dout_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_ba`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_ba(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.ba` message. A driver selects the block the vehicle will run.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_ba(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.ba` messages in a batch.

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

await producer.send_fi_hsl_hfp_ba_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_bout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_bout(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.bout` message. A driver signs out from the selected block (usually at a depot).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_bout(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.bout` messages in a batch.

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

await producer.send_fi_hsl_hfp_bout_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsOperatorEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsOperatorEventDispatcher` handles events for the fi.hsl.gtfs.operator message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsOperatorEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_operator_operator_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_operator_operator_async:  Callable[[ConsumerRecord, CloudEvent, Operator],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.operator.Operator`: Reference record describing one HSL transit operator.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_operator_operator_async = fi_hsl_gtfs_operator_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_operator_operator`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_operator_operator(

    self,##### `_process_event`

    data: Operator,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.operator.Operator` message. Reference record describing one HSL transit operator.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Operator`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_operator_operator(

    data=Operator(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.operator.Operator` messages in a batch.

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

await producer.send_fi_hsl_gtfs_operator_operator_batch(```

    messages=[

        Operator(...),Initializes the runner with a Kafka consumer.

        Operator(...),

        Operator(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsRouteEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsRouteEventDispatcher` handles events for the fi.hsl.gtfs.route message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsRouteEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_route_route_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_route_route_async:  Callable[[ConsumerRecord, CloudEvent, Route],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.route.Route`: Reference record describing one HSL route.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_route_route_async = fi_hsl_gtfs_route_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_route_route`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_route_route(

    self,##### `_process_event`

    data: Route,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.route.Route` message. Reference record describing one HSL route.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Route`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_route_route(

    data=Route(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.route.Route` messages in a batch.

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

await producer.send_fi_hsl_gtfs_route_route_batch(```

    messages=[

        Route(...),Initializes the runner with a Kafka consumer.

        Route(...),

        Route(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsStopEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsStopEventDispatcher` handles events for the fi.hsl.gtfs.stop message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsStopEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_stop_stop_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_stop_stop_async:  Callable[[ConsumerRecord, CloudEvent, Stop],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.stop.Stop`: Reference record describing one HSL stop or station.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_stop_stop_async = fi_hsl_gtfs_stop_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_stop_stop`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_stop_stop(

    self,##### `_process_event`

    data: Stop,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.stop.Stop` message. Reference record describing one HSL stop or station.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Stop`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_stop_stop(

    data=Stop(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.stop.Stop` messages in a batch.

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

await producer.send_fi_hsl_gtfs_stop_stop_batch(```

    messages=[

        Stop(...),Initializes the runner with a Kafka consumer.

        Stop(...),

        Stop(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslHfpMqttEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslHfpMqttEventDispatcher` handles events for the fi.hsl.hfp.mqtt message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslHfpMqttEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_vp_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_vp_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.vp`: Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an
ongoing public journey.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_vp_async = fi_hsl_hfp_mqtt_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_due_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_due_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.due`: The vehicle will soon arrive at a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_due_async = fi_hsl_hfp_mqtt_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_arr_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_arr_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.arr`: The vehicle has arrived inside a stop's radius.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_arr_async = fi_hsl_hfp_mqtt_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_dep_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_dep_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.dep`: The vehicle has departed and left a stop's radius.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_dep_async = fi_hsl_hfp_mqtt_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_ars_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_ars_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.ars`: The vehicle has arrived at a stop (stop-position event).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_ars_async = fi_hsl_hfp_mqtt_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_pde_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_pde_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.pde`: The vehicle is ready to depart from a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_pde_async = fi_hsl_hfp_mqtt_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_pas_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_pas_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.pas`: The vehicle passes through a stop without stopping.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_pas_async = fi_hsl_hfp_mqtt_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_wait_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_wait_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.wait`: The vehicle is waiting at a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_wait_async = fi_hsl_hfp_mqtt_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_doo_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_doo_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.doo`: The doors of the vehicle have been opened.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_doo_async = fi_hsl_hfp_mqtt_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_doc_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_doc_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.doc`: The doors of the vehicle have been closed.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_doc_async = fi_hsl_hfp_mqtt_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_vja_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_vja_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.vja`: The vehicle signs in to a service journey (trip).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_vja_async = fi_hsl_hfp_mqtt_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_vjout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_vjout_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.vjout`: The vehicle signs off from a service journey after the final
stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_vjout_async = fi_hsl_hfp_mqtt_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_tlr_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_tlr_async:  Callable[[ConsumerRecord, CloudEvent, TrafficLightEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.tlr`: The vehicle requests traffic-light priority at a junction.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_tlr_async = fi_hsl_hfp_mqtt_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_tla_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_tla_async:  Callable[[ConsumerRecord, CloudEvent, TrafficLightEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.tla`: The vehicle receives a response to a traffic-light priority
request.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_tla_async = fi_hsl_hfp_mqtt_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_da_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_da_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.da`: A driver signs in to the vehicle.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_da_async = fi_hsl_hfp_mqtt_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_dout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_dout_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.dout`: A driver signs out of the vehicle.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_dout_async = fi_hsl_hfp_mqtt_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_ba_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_ba_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.ba`: A driver selects the block the vehicle will run.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_ba_async = fi_hsl_hfp_mqtt_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_mqtt_bout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_mqtt_bout_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.mqtt.bout`: A driver signs out from the selected block (usually at a depot).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_mqtt_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_mqtt_bout_async = fi_hsl_hfp_mqtt_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_hfp_mqtt_vp`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_vp(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.vp` message. Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an ongoing public
journey.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_vp(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.vp` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_vp_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_due`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_due(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.due` message. The vehicle will soon arrive at a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_due(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.due` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_due_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_arr`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_arr(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.arr` message. The vehicle has arrived inside a stop's radius.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_arr(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.arr` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_arr_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_dep`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_dep(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.dep` message. The vehicle has departed and left a stop's radius.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_dep(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.dep` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_dep_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_ars`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_ars(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.ars` message. The vehicle has arrived at a stop (stop-position event).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_ars(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.ars` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_ars_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_pde`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_pde(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.pde` message. The vehicle is ready to depart from a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_pde(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.pde` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_pde_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_pas`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_pas(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.pas` message. The vehicle passes through a stop without stopping.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_pas(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.pas` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_pas_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_wait`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_wait(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.wait` message. The vehicle is waiting at a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_wait(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.wait` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_wait_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_doo`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_doo(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.doo` message. The doors of the vehicle have been opened.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_doo(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.doo` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_doo_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_doc`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_doc(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.doc` message. The doors of the vehicle have been closed.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_doc(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.doc` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_doc_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_vja`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_vja(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.vja` message. The vehicle signs in to a service journey (trip).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_vja(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.vja` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_vja_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_vjout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_vjout(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.vjout` message. The vehicle signs off from a service journey after the final stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_vjout(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.vjout` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_vjout_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_tlr`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_tlr(

    self,##### `_process_event`

    data: TrafficLightEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.tlr` message. The vehicle requests traffic-light priority at a junction.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TrafficLightEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_tlr(

    data=TrafficLightEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.tlr` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_tlr_batch(```

    messages=[

        TrafficLightEvent(...),Initializes the runner with a Kafka consumer.

        TrafficLightEvent(...),

        TrafficLightEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_tla`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_tla(

    self,##### `_process_event`

    data: TrafficLightEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.tla` message. The vehicle receives a response to a traffic-light priority request.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TrafficLightEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_tla(

    data=TrafficLightEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.tla` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_tla_batch(```

    messages=[

        TrafficLightEvent(...),Initializes the runner with a Kafka consumer.

        TrafficLightEvent(...),

        TrafficLightEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_da`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_da(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.da` message. A driver signs in to the vehicle.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_da(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.da` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_da_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_dout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_dout(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.dout` message. A driver signs out of the vehicle.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_dout(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.dout` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_dout_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_ba`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_ba(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.ba` message. A driver selects the block the vehicle will run.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_ba(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.ba` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_ba_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_mqtt_bout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_mqtt_bout(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.mqtt.bout` message. A driver signs out from the selected block (usually at a depot).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_mqtt_bout(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.mqtt.bout` messages in a batch.

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

await producer.send_fi_hsl_hfp_mqtt_bout_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslHfpAmqpEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslHfpAmqpEventDispatcher` handles events for the fi.hsl.hfp.amqp message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslHfpAmqpEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_vp_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_vp_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.vp`: Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an
ongoing public journey.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vp_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_vp_async = fi_hsl_hfp_amqp_vp_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_due_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_due_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.due`: The vehicle will soon arrive at a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_due_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_due_async = fi_hsl_hfp_amqp_due_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_arr_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_arr_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.arr`: The vehicle has arrived inside a stop's radius.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_arr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_arr_async = fi_hsl_hfp_amqp_arr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_dep_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_dep_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.dep`: The vehicle has departed and left a stop's radius.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dep_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_dep_async = fi_hsl_hfp_amqp_dep_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_ars_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_ars_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.ars`: The vehicle has arrived at a stop (stop-position event).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ars_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_ars_async = fi_hsl_hfp_amqp_ars_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_pde_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_pde_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.pde`: The vehicle is ready to depart from a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pde_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_pde_async = fi_hsl_hfp_amqp_pde_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_pas_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_pas_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.pas`: The vehicle passes through a stop without stopping.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_pas_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_pas_async = fi_hsl_hfp_amqp_pas_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_wait_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_wait_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.wait`: The vehicle is waiting at a stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_wait_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_wait_async = fi_hsl_hfp_amqp_wait_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_doo_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_doo_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.doo`: The doors of the vehicle have been opened.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doo_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_doo_async = fi_hsl_hfp_amqp_doo_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_doc_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_doc_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.doc`: The doors of the vehicle have been closed.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_doc_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_doc_async = fi_hsl_hfp_amqp_doc_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_vja_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_vja_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.vja`: The vehicle signs in to a service journey (trip).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vja_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_vja_async = fi_hsl_hfp_amqp_vja_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_vjout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_vjout_async:  Callable[[ConsumerRecord, CloudEvent, VehicleEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.vjout`: The vehicle signs off from a service journey after the final
stop.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.VehicleEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_vjout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: VehicleEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_vjout_async = fi_hsl_hfp_amqp_vjout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_tlr_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_tlr_async:  Callable[[ConsumerRecord, CloudEvent, TrafficLightEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.tlr`: The vehicle requests traffic-light priority at a junction.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tlr_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_tlr_async = fi_hsl_hfp_amqp_tlr_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_tla_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_tla_async:  Callable[[ConsumerRecord, CloudEvent, TrafficLightEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.tla`: The vehicle receives a response to a traffic-light priority
request.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.TrafficLightEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_tla_event(record: ConsumerRecord, cloud_event: CloudEvent, data: TrafficLightEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_tla_async = fi_hsl_hfp_amqp_tla_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_da_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_da_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.da`: A driver signs in to the vehicle.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_da_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_da_async = fi_hsl_hfp_amqp_da_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_dout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_dout_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.dout`: A driver signs out of the vehicle.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_dout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_dout_async = fi_hsl_hfp_amqp_dout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_ba_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_ba_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.ba`: A driver selects the block the vehicle will run.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_ba_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_ba_async = fi_hsl_hfp_amqp_ba_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_hfp_amqp_bout_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_hfp_amqp_bout_async:  Callable[[ConsumerRecord, CloudEvent, DriverBlockEvent],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.hfp.amqp.bout`: A driver signs out from the selected block (usually at a depot).

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.DriverBlockEvent`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_hfp_amqp_bout_event(record: ConsumerRecord, cloud_event: CloudEvent, data: DriverBlockEvent) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_hfp_amqp_bout_async = fi_hsl_hfp_amqp_bout_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_hfp_amqp_vp`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_vp(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.vp` message. Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an ongoing public
journey.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_vp(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.vp` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_vp_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_due`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_due(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.due` message. The vehicle will soon arrive at a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_due(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.due` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_due_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_arr`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_arr(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.arr` message. The vehicle has arrived inside a stop's radius.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_arr(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.arr` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_arr_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_dep`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_dep(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.dep` message. The vehicle has departed and left a stop's radius.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_dep(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.dep` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_dep_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_ars`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_ars(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.ars` message. The vehicle has arrived at a stop (stop-position event).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_ars(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.ars` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_ars_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_pde`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_pde(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.pde` message. The vehicle is ready to depart from a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_pde(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.pde` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_pde_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_pas`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_pas(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.pas` message. The vehicle passes through a stop without stopping.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_pas(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.pas` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_pas_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_wait`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_wait(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.wait` message. The vehicle is waiting at a stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_wait(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.wait` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_wait_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_doo`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_doo(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.doo` message. The doors of the vehicle have been opened.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_doo(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.doo` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_doo_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_doc`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_doc(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.doc` message. The doors of the vehicle have been closed.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_doc(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.doc` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_doc_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_vja`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_vja(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.vja` message. The vehicle signs in to a service journey (trip).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_vja(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.vja` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_vja_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_vjout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_vjout(

    self,##### `_process_event`

    data: VehicleEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.vjout` message. The vehicle signs off from a service journey after the final stop.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `VehicleEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_vjout(

    data=VehicleEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.vjout` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_vjout_batch(```

    messages=[

        VehicleEvent(...),Initializes the runner with a Kafka consumer.

        VehicleEvent(...),

        VehicleEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_tlr`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_tlr(

    self,##### `_process_event`

    data: TrafficLightEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.tlr` message. The vehicle requests traffic-light priority at a junction.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TrafficLightEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_tlr(

    data=TrafficLightEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.tlr` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_tlr_batch(```

    messages=[

        TrafficLightEvent(...),Initializes the runner with a Kafka consumer.

        TrafficLightEvent(...),

        TrafficLightEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_tla`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_tla(

    self,##### `_process_event`

    data: TrafficLightEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.tla` message. The vehicle receives a response to a traffic-light priority request.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TrafficLightEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_tla(

    data=TrafficLightEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.tla` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_tla_batch(```

    messages=[

        TrafficLightEvent(...),Initializes the runner with a Kafka consumer.

        TrafficLightEvent(...),

        TrafficLightEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_da`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_da(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.da` message. A driver signs in to the vehicle.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_da(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.da` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_da_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_dout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_dout(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.dout` message. A driver signs out of the vehicle.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_dout(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.dout` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_dout_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_ba`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_ba(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.ba` message. A driver selects the block the vehicle will run.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_ba(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.ba` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_ba_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_fi_hsl_hfp_amqp_bout`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_hfp_amqp_bout(

    self,##### `_process_event`

    data: DriverBlockEvent,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.hfp.amqp.bout` message. A driver signs out from the selected block (usually at a depot).Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DriverBlockEvent`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_hfp_amqp_bout(

    data=DriverBlockEvent(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.hfp.amqp.bout` messages in a batch.

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

await producer.send_fi_hsl_hfp_amqp_bout_batch(```

    messages=[

        DriverBlockEvent(...),Initializes the runner with a Kafka consumer.

        DriverBlockEvent(...),

        DriverBlockEvent(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsOperatorMqttEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsOperatorMqttEventDispatcher` handles events for the fi.hsl.gtfs.operator.mqtt message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsOperatorMqttEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_operator_mqtt_operator_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_operator_mqtt_operator_async:  Callable[[ConsumerRecord, CloudEvent,
Operator], Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.operator.mqtt.Operator`: Reference record describing one HSL transit
operator.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_mqtt_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_operator_mqtt_operator_async = fi_hsl_gtfs_operator_mqtt_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_operator_mqtt_operator`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_operator_mqtt_operator(

    self,##### `_process_event`

    data: Operator,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.operator.mqtt.Operator` message. Reference record describing one HSL transit operator.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Operator`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_operator_mqtt_operator(

    data=Operator(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.operator.mqtt.Operator` messages in a batch.

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

await producer.send_fi_hsl_gtfs_operator_mqtt_operator_batch(```

    messages=[

        Operator(...),Initializes the runner with a Kafka consumer.

        Operator(...),

        Operator(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsOperatorAmqpEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsOperatorAmqpEventDispatcher` handles events for the fi.hsl.gtfs.operator.amqp message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsOperatorAmqpEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_operator_amqp_operator_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_operator_amqp_operator_async:  Callable[[ConsumerRecord, CloudEvent,
Operator], Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.operator.amqp.Operator`: Reference record describing one HSL transit
operator.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Operator`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_operator_amqp_operator_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Operator) ->
None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_operator_amqp_operator_async = fi_hsl_gtfs_operator_amqp_operator_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_operator_amqp_operator`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_operator_amqp_operator(

    self,##### `_process_event`

    data: Operator,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.operator.amqp.Operator` message. Reference record describing one HSL transit operator.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Operator`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_operator_amqp_operator(

    data=Operator(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.operator.amqp.Operator` messages in a batch.

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

await producer.send_fi_hsl_gtfs_operator_amqp_operator_batch(```

    messages=[

        Operator(...),Initializes the runner with a Kafka consumer.

        Operator(...),

        Operator(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsRouteMqttEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsRouteMqttEventDispatcher` handles events for the fi.hsl.gtfs.route.mqtt message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsRouteMqttEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_route_mqtt_route_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_route_mqtt_route_async:  Callable[[ConsumerRecord, CloudEvent, Route],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.route.mqtt.Route`: Reference record describing one HSL route.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_mqtt_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_route_mqtt_route_async = fi_hsl_gtfs_route_mqtt_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_route_mqtt_route`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_route_mqtt_route(

    self,##### `_process_event`

    data: Route,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.route.mqtt.Route` message. Reference record describing one HSL route.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Route`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_route_mqtt_route(

    data=Route(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.route.mqtt.Route` messages in a batch.

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

await producer.send_fi_hsl_gtfs_route_mqtt_route_batch(```

    messages=[

        Route(...),Initializes the runner with a Kafka consumer.

        Route(...),

        Route(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsRouteAmqpEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsRouteAmqpEventDispatcher` handles events for the fi.hsl.gtfs.route.amqp message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsRouteAmqpEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_route_amqp_route_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_route_amqp_route_async:  Callable[[ConsumerRecord, CloudEvent, Route],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.route.amqp.Route`: Reference record describing one HSL route.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Route`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_route_amqp_route_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Route) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_route_amqp_route_async = fi_hsl_gtfs_route_amqp_route_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_route_amqp_route`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_route_amqp_route(

    self,##### `_process_event`

    data: Route,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.route.amqp.Route` message. Reference record describing one HSL route.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Route`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_route_amqp_route(

    data=Route(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.route.amqp.Route` messages in a batch.

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

await producer.send_fi_hsl_gtfs_route_amqp_route_batch(```

    messages=[

        Route(...),Initializes the runner with a Kafka consumer.

        Route(...),

        Route(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsStopMqttEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsStopMqttEventDispatcher` handles events for the fi.hsl.gtfs.stop.mqtt message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsStopMqttEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_stop_mqtt_stop_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_stop_mqtt_stop_async:  Callable[[ConsumerRecord, CloudEvent, Stop],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.stop.mqtt.Stop`: Reference record describing one HSL stop or station.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_mqtt_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_stop_mqtt_stop_async = fi_hsl_gtfs_stop_mqtt_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_stop_mqtt_stop`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_stop_mqtt_stop(

    self,##### `_process_event`

    data: Stop,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.stop.mqtt.Stop` message. Reference record describing one HSL stop or station.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Stop`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_stop_mqtt_stop(

    data=Stop(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.stop.mqtt.Stop` messages in a batch.

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

await producer.send_fi_hsl_gtfs_stop_mqtt_stop_batch(```

    messages=[

        Stop(...),Initializes the runner with a Kafka consumer.

        Stop(...),

        Stop(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### FiHslGtfsStopAmqpEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`FiHslGtfsStopAmqpEventDispatcher` handles events for the fi.hsl.gtfs.stop.amqp message group.

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

from hsl_hfp_producer import FiHslHfpProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_fi_hsl_hfp_vp(```python

    data=VehicleEvent(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The FiHslGtfsStopAmqpEventDispatcher defines the following event handler hooks.

```python

producer = FiHslHfpProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `fi_hsl_gtfs_stop_amqp_stop_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'fi_hsl_gtfs_stop_amqp_stop_async:  Callable[[ConsumerRecord, CloudEvent, Stop],
Awaitable[None]]

)```

```

Asynchronous handler hook for `fi.hsl.gtfs.stop.amqp.Stop`: Reference record describing one HSL stop or station.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_mqtt_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslHfpAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.hfp.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslHfpAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_hfp_amqp_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_mqtt_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsOperatorAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.operator.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsOperatorAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_operator_amqp_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_mqtt_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsRouteAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.route.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsRouteAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_route_amqp_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopMqttProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop.mqtt` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopMqttProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_mqtt_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### FiHslGtfsStopAmqpProducer- `data`: The event data of type `hsl_hfp_producer_data.Stop`.



Producer for `fi.hsl.gtfs.stop.amqp` message group.Example:



#### Constructor```python

async def fi_hsl_gtfs_stop_amqp_stop_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Stop) -> None:

```python    # Process the event data

FiHslGtfsStopAmqpProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

fi_hsl_gtfs_stop_amqp_dispatcher.fi_hsl_gtfs_stop_amqp_stop_async = fi_hsl_gtfs_stop_amqp_stop_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_fi_hsl_gtfs_stop_amqp_stop`Dispatchers have the following protected methods:



```python### Methods:

async def send_fi_hsl_gtfs_stop_amqp_stop(

    self,##### `_process_event`

    data: Stop,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `fi.hsl.gtfs.stop.amqp.Stop` message. Reference record describing one HSL stop or station.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Stop`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_fi_hsl_gtfs_stop_amqp_stop(

    data=Stop(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `fi.hsl.gtfs.stop.amqp.Stop` messages in a batch.

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

await producer.send_fi_hsl_gtfs_stop_amqp_stop_batch(```

    messages=[

        Stop(...),Initializes the runner with a Kafka consumer.

        Stop(...),

        Stop(...)Args:

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
