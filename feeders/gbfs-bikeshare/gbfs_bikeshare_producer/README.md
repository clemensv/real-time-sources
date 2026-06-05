

# Gbfs_bikeshare_producer Kafka Producer# Gbfs_bikeshare_producer Event Dispatcher for Apache Kafka



This module provides a type-safe Kafka producer for sending CloudEvents and plain Kafka messages.This module provides an
event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages and CloudEvents.



## Table of Contents## Table of Contents

1. [Overview](#overview)1. [Overview](#overview)

2. [What is Apache Kafka?](#what-is-apache-kafka)2. [Generated Event Dispatchers](#generated-event-dispatchers)

3. [Quick Start](#quick-start)    - OrgGbfsSystemEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsStationsEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsFreeBikesEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsKafkaSystemEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsKafkaStationsEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsKafkaFreeBikesEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsMqttSystemEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsMqttStationsEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsMqttFreeBikesEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsAmqpSystemEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsAmqpStationsEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    OrgGbfsAmqpFreeBikesEventDispatcher

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

- OrgGbfsSystemProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsStationsProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsFreeBikesProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsKafkaSystemProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsKafkaStationsProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsKafkaFreeBikesProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsMqttSystemProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsMqttStationsProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsMqttFreeBikesProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsAmqpSystemProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsAmqpStationsProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- OrgGbfsAmqpFreeBikesProducersolution for event-driven applications.



## Generated Event Dispatchers

## What is Apache Kafka?



**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsSystemEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsSystemEventDispatcher` handles events for the org.gbfs.system message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsSystemEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_system_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_system_information_async:  Callable[[ConsumerRecord, CloudEvent,
SystemInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.SystemInformation`: Reference data describing one GBFS system as published in
`system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SystemInformation) ->
None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_system_information_async = org_gbfs_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_system_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_system_information(

    self,##### `_process_event`

    data: SystemInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.SystemInformation` message. Reference data describing one GBFS system as published in
`system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SystemInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_system_information(

    data=SystemInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.SystemInformation` messages in a batch.

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

await producer.send_org_gbfs_system_information_batch(```

    messages=[

        SystemInformation(...),Initializes the runner with a Kafka consumer.

        SystemInformation(...),

        SystemInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsStationsEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsStationsEventDispatcher` handles events for the org.gbfs.stations message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsStationsEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_station_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_station_information_async:  Callable[[ConsumerRecord, CloudEvent,
StationInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.StationInformation`: Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationInformation)
-> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_station_information_async = org_gbfs_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_station_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_station_status_async:  Callable[[ConsumerRecord, CloudEvent, StationStatus],
Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.StationStatus`: Real-time station availability telemetry from
`station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the
upstream `last_reported` timestamp for one GBFS station.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) -> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_station_status_async = org_gbfs_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_station_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_station_information(

    self,##### `_process_event`

    data: StationInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.StationInformation` message. Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_station_information(

    data=StationInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.StationInformation` messages in a batch.

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

await producer.send_org_gbfs_station_information_batch(```

    messages=[

        StationInformation(...),Initializes the runner with a Kafka consumer.

        StationInformation(...),

        StationInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_org_gbfs_station_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_station_status(

    self,##### `_process_event`

    data: StationStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.StationStatus` message. Real-time station availability telemetry from `station_status.json`.
Each event describes the current rentable-bike count, dock availability, operating flags, and the upstream
`last_reported` timestamp for one GBFS station.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_station_status(

    data=StationStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.StationStatus` messages in a batch.

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

await producer.send_org_gbfs_station_status_batch(```

    messages=[

        StationStatus(...),Initializes the runner with a Kafka consumer.

        StationStatus(...),

        StationStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsFreeBikesEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsFreeBikesEventDispatcher` handles events for the org.gbfs.free_bikes message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsFreeBikesEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_free_bike_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_free_bike_status_async:  Callable[[ConsumerRecord, CloudEvent,
FreeBikeStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.FreeBikeStatus`: Real-time dockless vehicle telemetry from
`free_bike_status.json` (renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location,
reservation and disablement state, optional vehicle type reference, and optional remaining range for a single rentable
vehicle that is not currently in an active trip.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_free_bike_status_async = org_gbfs_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_free_bike_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_free_bike_status(

    self,##### `_process_event`

    data: FreeBikeStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.FreeBikeStatus` message. Real-time dockless vehicle telemetry from `free_bike_status.json`
(renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location, reservation and disablement
state, optional vehicle type reference, and optional remaining range for a single rentable vehicle that is not currently
in an active trip.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FreeBikeStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_free_bike_status(

    data=FreeBikeStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.FreeBikeStatus` messages in a batch.

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

await producer.send_org_gbfs_free_bike_status_batch(```

    messages=[

        FreeBikeStatus(...),Initializes the runner with a Kafka consumer.

        FreeBikeStatus(...),

        FreeBikeStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsKafkaSystemEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsKafkaSystemEventDispatcher` handles events for the org.gbfs.kafka.system message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsKafkaSystemEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_kafka_system_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_kafka_system_information_async:  Callable[[ConsumerRecord, CloudEvent,
SystemInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.kafka.SystemInformation`: Reference data describing one GBFS system as published
in `system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_kafka_system_information_async = org_gbfs_kafka_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_kafka_system_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_kafka_system_information(

    self,##### `_process_event`

    data: SystemInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.kafka.SystemInformation` message. Reference data describing one GBFS system as published in
`system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SystemInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_kafka_system_information(

    data=SystemInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

##### `send_org_gbfs_kafka_system_information_batch`##### `_dispatch_record`



```python```python

async def send_org_gbfs_kafka_system_information_batch(_dispatch_record(self, record)

    self,```

    messages: List[SystemInformation],

    partition_key: Optional[str] = None,Dispatches a Kafka event to the appropriate handler.

    headers: Optional[Dict[str, str]] = None,

    topic: Optional[str] = NoneArgs:

) -> None- `record`: The Kafka record.

```

Send multiple `org.gbfs.kafka.SystemInformation` messages in a batch.

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

await producer.send_org_gbfs_kafka_system_information_batch(```

    messages=[

        SystemInformation(...),Initializes the runner with a Kafka consumer.

        SystemInformation(...),

        SystemInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsKafkaStationsEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsKafkaStationsEventDispatcher` handles events for the org.gbfs.kafka.stations message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsKafkaStationsEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_kafka_station_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_kafka_station_information_async:  Callable[[ConsumerRecord, CloudEvent,
StationInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.kafka.StationInformation`: Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_kafka_station_information_async = org_gbfs_kafka_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_kafka_station_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_kafka_station_status_async:  Callable[[ConsumerRecord, CloudEvent,
StationStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.kafka.StationStatus`: Real-time station availability telemetry from
`station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the
upstream `last_reported` timestamp for one GBFS station.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_kafka_station_status_async = org_gbfs_kafka_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_kafka_station_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_kafka_station_information(

    self,##### `_process_event`

    data: StationInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.kafka.StationInformation` message. Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_kafka_station_information(

    data=StationInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

##### `send_org_gbfs_kafka_station_information_batch`##### `_dispatch_record`



```python```python

async def send_org_gbfs_kafka_station_information_batch(_dispatch_record(self, record)

    self,```

    messages: List[StationInformation],

    partition_key: Optional[str] = None,Dispatches a Kafka event to the appropriate handler.

    headers: Optional[Dict[str, str]] = None,

    topic: Optional[str] = NoneArgs:

) -> None- `record`: The Kafka record.

```

Send multiple `org.gbfs.kafka.StationInformation` messages in a batch.

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

await producer.send_org_gbfs_kafka_station_information_batch(```

    messages=[

        StationInformation(...),Initializes the runner with a Kafka consumer.

        StationInformation(...),

        StationInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_org_gbfs_kafka_station_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_kafka_station_status(

    self,##### `_process_event`

    data: StationStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.kafka.StationStatus` message. Real-time station availability telemetry from
`station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the
upstream `last_reported` timestamp for one GBFS station.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_kafka_station_status(

    data=StationStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

##### `send_org_gbfs_kafka_station_status_batch`##### `_dispatch_record`



```python```python

async def send_org_gbfs_kafka_station_status_batch(_dispatch_record(self, record)

    self,```

    messages: List[StationStatus],

    partition_key: Optional[str] = None,Dispatches a Kafka event to the appropriate handler.

    headers: Optional[Dict[str, str]] = None,

    topic: Optional[str] = NoneArgs:

) -> None- `record`: The Kafka record.

```

Send multiple `org.gbfs.kafka.StationStatus` messages in a batch.

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

await producer.send_org_gbfs_kafka_station_status_batch(```

    messages=[

        StationStatus(...),Initializes the runner with a Kafka consumer.

        StationStatus(...),

        StationStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsKafkaFreeBikesEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsKafkaFreeBikesEventDispatcher` handles events for the org.gbfs.kafka.free_bikes message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsKafkaFreeBikesEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_kafka_free_bike_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_kafka_free_bike_status_async:  Callable[[ConsumerRecord, CloudEvent,
FreeBikeStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.kafka.FreeBikeStatus`: Real-time dockless vehicle telemetry from
`free_bike_status.json` (renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location,
reservation and disablement state, optional vehicle type reference, and optional remaining range for a single rentable
vehicle that is not currently in an active trip.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_kafka_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus)
-> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_kafka_free_bike_status_async = org_gbfs_kafka_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_kafka_free_bike_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_kafka_free_bike_status(

    self,##### `_process_event`

    data: FreeBikeStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.kafka.FreeBikeStatus` message. Real-time dockless vehicle telemetry from `free_bike_status.json`
(renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location, reservation and disablement
state, optional vehicle type reference, and optional remaining range for a single rentable vehicle that is not currently
in an active trip.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FreeBikeStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_kafka_free_bike_status(

    data=FreeBikeStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

##### `send_org_gbfs_kafka_free_bike_status_batch`##### `_dispatch_record`



```python```python

async def send_org_gbfs_kafka_free_bike_status_batch(_dispatch_record(self, record)

    self,```

    messages: List[FreeBikeStatus],

    partition_key: Optional[str] = None,Dispatches a Kafka event to the appropriate handler.

    headers: Optional[Dict[str, str]] = None,

    topic: Optional[str] = NoneArgs:

) -> None- `record`: The Kafka record.

```

Send multiple `org.gbfs.kafka.FreeBikeStatus` messages in a batch.

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

await producer.send_org_gbfs_kafka_free_bike_status_batch(```

    messages=[

        FreeBikeStatus(...),Initializes the runner with a Kafka consumer.

        FreeBikeStatus(...),

        FreeBikeStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsMqttSystemEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsMqttSystemEventDispatcher` handles events for the org.gbfs.mqtt.system message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsMqttSystemEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_mqtt_system_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_mqtt_system_information_async:  Callable[[ConsumerRecord, CloudEvent,
SystemInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.mqtt.SystemInformation`: Reference data describing one GBFS system as published
in `system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_mqtt_system_information_async = org_gbfs_mqtt_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_mqtt_system_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_mqtt_system_information(

    self,##### `_process_event`

    data: SystemInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.mqtt.SystemInformation` message. Reference data describing one GBFS system as published in
`system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SystemInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_mqtt_system_information(

    data=SystemInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.mqtt.SystemInformation` messages in a batch.

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

await producer.send_org_gbfs_mqtt_system_information_batch(```

    messages=[

        SystemInformation(...),Initializes the runner with a Kafka consumer.

        SystemInformation(...),

        SystemInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsMqttStationsEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsMqttStationsEventDispatcher` handles events for the org.gbfs.mqtt.stations message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsMqttStationsEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_mqtt_station_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_mqtt_station_information_async:  Callable[[ConsumerRecord, CloudEvent,
StationInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.mqtt.StationInformation`: Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_mqtt_station_information_async = org_gbfs_mqtt_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_mqtt_station_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_mqtt_station_status_async:  Callable[[ConsumerRecord, CloudEvent,
StationStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.mqtt.StationStatus`: Real-time station availability telemetry from
`station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the
upstream `last_reported` timestamp for one GBFS station.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_mqtt_station_status_async = org_gbfs_mqtt_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_mqtt_station_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_mqtt_station_information(

    self,##### `_process_event`

    data: StationInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.mqtt.StationInformation` message. Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_mqtt_station_information(

    data=StationInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.mqtt.StationInformation` messages in a batch.

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

await producer.send_org_gbfs_mqtt_station_information_batch(```

    messages=[

        StationInformation(...),Initializes the runner with a Kafka consumer.

        StationInformation(...),

        StationInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_org_gbfs_mqtt_station_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_mqtt_station_status(

    self,##### `_process_event`

    data: StationStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.mqtt.StationStatus` message. Real-time station availability telemetry from
`station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the
upstream `last_reported` timestamp for one GBFS station.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_mqtt_station_status(

    data=StationStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.mqtt.StationStatus` messages in a batch.

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

await producer.send_org_gbfs_mqtt_station_status_batch(```

    messages=[

        StationStatus(...),Initializes the runner with a Kafka consumer.

        StationStatus(...),

        StationStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsMqttFreeBikesEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsMqttFreeBikesEventDispatcher` handles events for the org.gbfs.mqtt.free_bikes message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsMqttFreeBikesEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_mqtt_free_bike_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_mqtt_free_bike_status_async:  Callable[[ConsumerRecord, CloudEvent,
FreeBikeStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.mqtt.FreeBikeStatus`: Real-time dockless vehicle telemetry from
`free_bike_status.json` (renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location,
reservation and disablement state, optional vehicle type reference, and optional remaining range for a single rentable
vehicle that is not currently in an active trip.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_mqtt_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_mqtt_free_bike_status_async = org_gbfs_mqtt_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_mqtt_free_bike_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_mqtt_free_bike_status(

    self,##### `_process_event`

    data: FreeBikeStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.mqtt.FreeBikeStatus` message. Real-time dockless vehicle telemetry from `free_bike_status.json`
(renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location, reservation and disablement
state, optional vehicle type reference, and optional remaining range for a single rentable vehicle that is not currently
in an active trip.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FreeBikeStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_mqtt_free_bike_status(

    data=FreeBikeStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.mqtt.FreeBikeStatus` messages in a batch.

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

await producer.send_org_gbfs_mqtt_free_bike_status_batch(```

    messages=[

        FreeBikeStatus(...),Initializes the runner with a Kafka consumer.

        FreeBikeStatus(...),

        FreeBikeStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsAmqpSystemEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsAmqpSystemEventDispatcher` handles events for the org.gbfs.amqp.system message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsAmqpSystemEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_amqp_system_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_amqp_system_information_async:  Callable[[ConsumerRecord, CloudEvent,
SystemInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.amqp.SystemInformation`: Reference data describing one GBFS system as published
in `system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.SystemInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_system_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SystemInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_amqp_system_information_async = org_gbfs_amqp_system_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_amqp_system_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_amqp_system_information(

    self,##### `_process_event`

    data: SystemInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.amqp.SystemInformation` message. Reference data describing one GBFS system as published in
`system_information.json`, including the public system name, operator, customer-facing URL, timezone, and support
metadata. Emitted at bridge startup and on reference refresh so consumers can join station and vehicle telemetry against
stable system metadata.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SystemInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_amqp_system_information(

    data=SystemInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.amqp.SystemInformation` messages in a batch.

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

await producer.send_org_gbfs_amqp_system_information_batch(```

    messages=[

        SystemInformation(...),Initializes the runner with a Kafka consumer.

        SystemInformation(...),

        SystemInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsAmqpStationsEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsAmqpStationsEventDispatcher` handles events for the org.gbfs.amqp.stations message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsAmqpStationsEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_amqp_station_information_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_amqp_station_information_async:  Callable[[ConsumerRecord, CloudEvent,
StationInformation], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.amqp.StationInformation`: Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationInformation`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_information_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
StationInformation) -> None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_amqp_station_information_async = org_gbfs_amqp_station_information_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_amqp_station_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_amqp_station_status_async:  Callable[[ConsumerRecord, CloudEvent,
StationStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.amqp.StationStatus`: Real-time station availability telemetry from
`station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the
upstream `last_reported` timestamp for one GBFS station.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.StationStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_station_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: StationStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_amqp_station_status_async = org_gbfs_amqp_station_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_amqp_station_information`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_amqp_station_information(

    self,##### `_process_event`

    data: StationInformation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.amqp.StationInformation` message. Reference data for one dock-based GBFS station from
`station_information.json`. The event carries the stable station identifier, public name, WGS 84 coordinates, docking
capacity, and optional address / regional context so consumers can interpret real-time availability telemetry.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationInformation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_amqp_station_information(

    data=StationInformation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.amqp.StationInformation` messages in a batch.

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

await producer.send_org_gbfs_amqp_station_information_batch(```

    messages=[

        StationInformation(...),Initializes the runner with a Kafka consumer.

        StationInformation(...),

        StationInformation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_org_gbfs_amqp_station_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_amqp_station_status(

    self,##### `_process_event`

    data: StationStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.amqp.StationStatus` message. Real-time station availability telemetry from
`station_status.json`. Each event describes the current rentable-bike count, dock availability, operating flags, and the
upstream `last_reported` timestamp for one GBFS station.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `StationStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_amqp_station_status(

    data=StationStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.amqp.StationStatus` messages in a batch.

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

await producer.send_org_gbfs_amqp_station_status_batch(```

    messages=[

        StationStatus(...),Initializes the runner with a Kafka consumer.

        StationStatus(...),

        StationStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### OrgGbfsAmqpFreeBikesEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`OrgGbfsAmqpFreeBikesEventDispatcher` handles events for the org.gbfs.amqp.free_bikes message group.

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

from gbfs_bikeshare_producer import OrgGbfsSystemProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_org_gbfs_system_information(```python

    data=SystemInformation(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The OrgGbfsAmqpFreeBikesEventDispatcher defines the following event handler hooks.

```python

producer = OrgGbfsSystemProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `org_gbfs_amqp_free_bike_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'org_gbfs_amqp_free_bike_status_async:  Callable[[ConsumerRecord, CloudEvent,
FreeBikeStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `org.gbfs.amqp.FreeBikeStatus`: Real-time dockless vehicle telemetry from
`free_bike_status.json` (renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location,
reservation and disablement state, optional vehicle type reference, and optional remaining range for a single rentable
vehicle that is not currently in an active trip.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_system_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_stations_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_free_bikes_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_system_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_stations_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsKafkaFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.kafka.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsKafkaFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_kafka_free_bikes_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_system_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_stations_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsMqttFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.mqtt.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsMqttFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_mqtt_free_bikes_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpSystemProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.system` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpSystemProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_system_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpStationsProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.stations` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpStationsProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_stations_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### OrgGbfsAmqpFreeBikesProducer- `data`: The event data of type `gbfs_bikeshare_producer_data.FreeBikeStatus`.



Producer for `org.gbfs.amqp.free_bikes` message group.Example:



#### Constructor```python

async def org_gbfs_amqp_free_bike_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FreeBikeStatus) ->
None:

```python    # Process the event data

OrgGbfsAmqpFreeBikesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

org_gbfs_amqp_free_bikes_dispatcher.org_gbfs_amqp_free_bike_status_async = org_gbfs_amqp_free_bike_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_org_gbfs_amqp_free_bike_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_org_gbfs_amqp_free_bike_status(

    self,##### `_process_event`

    data: FreeBikeStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `org.gbfs.amqp.FreeBikeStatus` message. Real-time dockless vehicle telemetry from `free_bike_status.json`
(renamed `vehicle_status.json` in GBFS v3). Each event carries the last known location, reservation and disablement
state, optional vehicle type reference, and optional remaining range for a single rentable vehicle that is not currently
in an active trip.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FreeBikeStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_org_gbfs_amqp_free_bike_status(

    data=FreeBikeStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `org.gbfs.amqp.FreeBikeStatus` messages in a batch.

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

await producer.send_org_gbfs_amqp_free_bike_status_batch(```

    messages=[

        FreeBikeStatus(...),Initializes the runner with a Kafka consumer.

        FreeBikeStatus(...),

        FreeBikeStatus(...)Args:

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
