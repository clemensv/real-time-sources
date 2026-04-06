

# Usgs-iv-producer Kafka Producer# Usgs-iv-producer Event Dispatcher for Apache Kafka



This module provides a type-safe Kafka producer for sending CloudEvents and plain Kafka messages.This module provides an
event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages and CloudEvents.



## Table of Contents## Table of Contents

1. [Overview](#overview)1. [Overview](#overview)

2. [What is Apache Kafka?](#what-is-apache-kafka)2. [Generated Event Dispatchers](#generated-event-dispatchers)

3. [Quick Start](#quick-start)    - USGSSitesEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    USGSSiteTimeseriesEventDispatcher,

4. [Generated Producer Classes](#generated-producer-classes)    USGSInstantaneousValuesEventDispatcher

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

- USGSSitesProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- USGSSiteTimeseriesProducersolution for event-driven applications.

It includes both plain Kafka messages and CloudEvents, offering a versatile

- USGSInstantaneousValuesProducersolution for event-driven applications.



## Generated Event Dispatchers

## What is Apache Kafka?



**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### USGSSitesEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`USGSSitesEventDispatcher` handles events for the USGS.Sites message group.

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

from usgs-iv-producer import USGSSitesProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = USGSSitesProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_usgs_sites_site(```python

    data=Site(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The USGSSitesEventDispatcher defines the following event handler hooks.

```python

producer = USGSSitesProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_sites_site_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_sites_site_async:  Callable[[ConsumerRecord, CloudEvent, Site], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.Sites.Site`: USGS site metadata.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.Site`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_sites_site_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Site) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_sites_site_async = usgs_sites_site_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.Site`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_sites_site_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Site) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_sites_site_async = usgs_sites_site_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.Site`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_sites_site_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Site) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_sites_site_async = usgs_sites_site_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_usgs_sites_site`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_sites_site(

    self,##### `_process_event`

    data: Site,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.Sites.Site` message. USGS site metadata.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Site`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_sites_site(

    data=Site(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.Sites.Site` messages in a batch.

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

await producer.send_usgs_sites_site_batch(```

    messages=[

        Site(...),Initializes the runner with a Kafka consumer.

        Site(...),

        Site(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### USGSSiteTimeseriesEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`USGSSiteTimeseriesEventDispatcher` handles events for the USGS.SiteTimeseries message group.

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

from usgs-iv-producer import USGSSitesProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = USGSSitesProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_usgs_sites_site(```python

    data=Site(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The USGSSiteTimeseriesEventDispatcher defines the following event handler hooks.

```python

producer = USGSSitesProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_sites_site_timeseries_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_sites_site_timeseries_async:  Callable[[ConsumerRecord, CloudEvent,
SiteTimeseries], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.Sites.SiteTimeseries`: USGS site timeseries metadata.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.SiteTimeseries`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_sites_site_timeseries_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SiteTimeseries) ->
None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_sites_site_timeseries_async = usgs_sites_site_timeseries_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.SiteTimeseries`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_sites_site_timeseries_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SiteTimeseries) ->
None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_sites_site_timeseries_async = usgs_sites_site_timeseries_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.SiteTimeseries`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_sites_site_timeseries_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SiteTimeseries) ->
None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_sites_site_timeseries_async = usgs_sites_site_timeseries_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_usgs_sites_site_timeseries`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_sites_site_timeseries(

    self,##### `_process_event`

    data: SiteTimeseries,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.Sites.SiteTimeseries` message. USGS site timeseries metadata.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SiteTimeseries`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_sites_site_timeseries(

    data=SiteTimeseries(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.Sites.SiteTimeseries` messages in a batch.

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

await producer.send_usgs_sites_site_timeseries_batch(```

    messages=[

        SiteTimeseries(...),Initializes the runner with a Kafka consumer.

        SiteTimeseries(...),

        SiteTimeseries(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.





**Apache Kafka** is a distributed streaming platform that:

- **Handles high-throughput** real-time data feeds with low latency

- **Provides durability** through log-based storage with configurable retention

- **Scales horizontally** across multiple brokers and partitions### USGSInstantaneousValuesEventDispatcher

- **Enables pub/sub messaging** with topic-based routing

`USGSInstantaneousValuesEventDispatcher` handles events for the USGS.InstantaneousValues message group.

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

from usgs-iv-producer import USGSSitesProducer```python

create_processor(self, bootstrap_servers: str, group_id: str, topics: List[str]) -> EventProcessorRunner

# Create producer```

producer = USGSSitesProducer(

    bootstrap_servers='localhost:9092',Creates an `EventProcessorRunner`.

    client_id='my-producer'

)Args:

- `bootstrap_servers`: The Kafka bootstrap servers.

- `group_id`: The consumer group ID.- `topics`: The list of topics to subscribe to.##### `add_consumer`:

# Send single message

await producer.send_usgs_sites_site(```python

    data=Site(...),add_consumer(self, consumer: KafkaConsumer)

    partition_key='device-123'```

)Adds a Kafka consumer to the dispatcher.



# Close producerArgs:

await producer.close()- `consumer`: The Kafka consumer.

```

#### Event Handlers

### With SSL/SASL

The USGSInstantaneousValuesEventDispatcher defines the following event handler hooks.

```python

producer = USGSSitesProducer(

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_other_parameter_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_other_parameter_async:  Callable[[ConsumerRecord, CloudEvent,
OtherParameter], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.OtherParameter`: USGS other parameter data.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.OtherParameter`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_other_parameter_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
OtherParameter) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_other_parameter_async = usgs_instantaneous_values_other_parameter_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.OtherParameter`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_other_parameter_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
OtherParameter) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_other_parameter_async =
usgs_instantaneous_values_other_parameter_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.OtherParameter`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_other_parameter_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
OtherParameter) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_other_parameter_async =
usgs_instantaneous_values_other_parameter_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_precipitation_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_precipitation_async:  Callable[[ConsumerRecord, CloudEvent,
Precipitation], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.Precipitation`: USGS precipitation data. Parameter code 00045.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.Precipitation`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_precipitation_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Precipitation) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_precipitation_async = usgs_instantaneous_values_precipitation_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.Precipitation`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_precipitation_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Precipitation) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_precipitation_async =
usgs_instantaneous_values_precipitation_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.Precipitation`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_precipitation_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Precipitation) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_precipitation_async =
usgs_instantaneous_values_precipitation_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_streamflow_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_streamflow_async:  Callable[[ConsumerRecord, CloudEvent,
Streamflow], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.Streamflow`: USGS streamflow data. Parameter code 00060.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.Streamflow`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_streamflow_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Streamflow)
-> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_streamflow_async = usgs_instantaneous_values_streamflow_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.Streamflow`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_streamflow_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Streamflow)
-> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_streamflow_async = usgs_instantaneous_values_streamflow_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.Streamflow`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_streamflow_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Streamflow)
-> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_streamflow_async =
usgs_instantaneous_values_streamflow_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_gage_height_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_gage_height_async:  Callable[[ConsumerRecord, CloudEvent,
GageHeight], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.GageHeight`: USGS gage height data. Parameter code 00065.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.GageHeight`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_gage_height_event(record: ConsumerRecord, cloud_event: CloudEvent, data: GageHeight)
-> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_gage_height_async = usgs_instantaneous_values_gage_height_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.GageHeight`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_gage_height_event(record: ConsumerRecord, cloud_event: CloudEvent, data: GageHeight)
-> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_gage_height_async =
usgs_instantaneous_values_gage_height_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.GageHeight`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_gage_height_event(record: ConsumerRecord, cloud_event: CloudEvent, data: GageHeight)
-> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_gage_height_async =
usgs_instantaneous_values_gage_height_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_water_temperature_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_water_temperature_async:  Callable[[ConsumerRecord,
CloudEvent, WaterTemperature], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.WaterTemperature`: USGS water temperature data. Parameter code
00010.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterTemperature`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterTemperature) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_water_temperature_async =
usgs_instantaneous_values_water_temperature_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterTemperature`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterTemperature) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_water_temperature_async =
usgs_instantaneous_values_water_temperature_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterTemperature`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterTemperature) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_water_temperature_async =
usgs_instantaneous_values_water_temperature_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_dissolved_oxygen_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_dissolved_oxygen_async:  Callable[[ConsumerRecord,
CloudEvent, DissolvedOxygen], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.DissolvedOxygen`: USGS dissolved oxygen data. Parameter code
00300.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.DissolvedOxygen`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_dissolved_oxygen_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
DissolvedOxygen) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_dissolved_oxygen_async =
usgs_instantaneous_values_dissolved_oxygen_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.DissolvedOxygen`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_dissolved_oxygen_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
DissolvedOxygen) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_dissolved_oxygen_async =
usgs_instantaneous_values_dissolved_oxygen_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.DissolvedOxygen`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_dissolved_oxygen_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
DissolvedOxygen) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_dissolved_oxygen_async =
usgs_instantaneous_values_dissolved_oxygen_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_p_h_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_p_h_async:  Callable[[ConsumerRecord, CloudEvent, PH],
Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.pH`: USGS pH data. Parameter code 00400.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.PH`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_p_h_event(record: ConsumerRecord, cloud_event: CloudEvent, data: PH) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_p_h_async = usgs_instantaneous_values_p_h_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.PH`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_p_h_event(record: ConsumerRecord, cloud_event: CloudEvent, data: PH) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_p_h_async = usgs_instantaneous_values_p_h_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.PH`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_p_h_event(record: ConsumerRecord, cloud_event: CloudEvent, data: PH) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_p_h_async = usgs_instantaneous_values_p_h_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_specific_conductance_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_specific_conductance_async:  Callable[[ConsumerRecord,
CloudEvent, SpecificConductance], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.SpecificConductance`: USGS specific conductance data. Parameter
code 00095.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.SpecificConductance`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_specific_conductance_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SpecificConductance) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_specific_conductance_async =
usgs_instantaneous_values_specific_conductance_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.SpecificConductance`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_specific_conductance_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SpecificConductance) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_specific_conductance_async =
usgs_instantaneous_values_specific_conductance_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.SpecificConductance`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_specific_conductance_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SpecificConductance) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_specific_conductance_async =
usgs_instantaneous_values_specific_conductance_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_turbidity_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_turbidity_async:  Callable[[ConsumerRecord, CloudEvent,
Turbidity], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.Turbidity`: USGS turbidity data. Parameter code 00076.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.Turbidity`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_turbidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Turbidity) ->
None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_turbidity_async = usgs_instantaneous_values_turbidity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.Turbidity`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_turbidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Turbidity) ->
None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_turbidity_async = usgs_instantaneous_values_turbidity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.Turbidity`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_turbidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Turbidity) ->
None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_turbidity_async =
usgs_instantaneous_values_turbidity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_air_temperature_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_air_temperature_async:  Callable[[ConsumerRecord, CloudEvent,
AirTemperature], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.AirTemperature`: USGS air temperature data. Parameter code
00020.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.AirTemperature`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_air_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AirTemperature) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_air_temperature_async = usgs_instantaneous_values_air_temperature_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.AirTemperature`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_air_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AirTemperature) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_air_temperature_async =
usgs_instantaneous_values_air_temperature_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.AirTemperature`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_air_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AirTemperature) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_air_temperature_async =
usgs_instantaneous_values_air_temperature_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_wind_speed_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_wind_speed_async:  Callable[[ConsumerRecord, CloudEvent,
WindSpeed], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.WindSpeed`: USGS wind speed data. Parameter code 00035.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.WindSpeed`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_wind_speed_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WindSpeed)
-> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_wind_speed_async = usgs_instantaneous_values_wind_speed_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.WindSpeed`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_wind_speed_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WindSpeed)
-> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_wind_speed_async = usgs_instantaneous_values_wind_speed_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.WindSpeed`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_wind_speed_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WindSpeed)
-> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_wind_speed_async =
usgs_instantaneous_values_wind_speed_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_wind_direction_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_wind_direction_async:  Callable[[ConsumerRecord, CloudEvent,
WindDirection], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.WindDirection`: USGS wind direction data. Parameter codes 00036
and 163695.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.WindDirection`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_wind_direction_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WindDirection) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_wind_direction_async = usgs_instantaneous_values_wind_direction_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.WindDirection`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_wind_direction_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WindDirection) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_wind_direction_async =
usgs_instantaneous_values_wind_direction_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.WindDirection`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_wind_direction_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WindDirection) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_wind_direction_async =
usgs_instantaneous_values_wind_direction_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_relative_humidity_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_relative_humidity_async:  Callable[[ConsumerRecord,
CloudEvent, RelativeHumidity], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.RelativeHumidity`: USGS relative humidity data. Parameter code
00052.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.RelativeHumidity`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_relative_humidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
RelativeHumidity) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_relative_humidity_async =
usgs_instantaneous_values_relative_humidity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.RelativeHumidity`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_relative_humidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
RelativeHumidity) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_relative_humidity_async =
usgs_instantaneous_values_relative_humidity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.RelativeHumidity`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_relative_humidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
RelativeHumidity) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_relative_humidity_async =
usgs_instantaneous_values_relative_humidity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_barometric_pressure_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_barometric_pressure_async:  Callable[[ConsumerRecord,
CloudEvent, BarometricPressure], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.BarometricPressure`: USGS barometric pressure data. Parameter
codes 62605 and 75969.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.BarometricPressure`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_barometric_pressure_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
BarometricPressure) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_barometric_pressure_async =
usgs_instantaneous_values_barometric_pressure_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.BarometricPressure`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_barometric_pressure_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
BarometricPressure) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_barometric_pressure_async =
usgs_instantaneous_values_barometric_pressure_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.BarometricPressure`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_barometric_pressure_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
BarometricPressure) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_barometric_pressure_async =
usgs_instantaneous_values_barometric_pressure_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_turbidity_fnu_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_turbidity_fnu_async:  Callable[[ConsumerRecord, CloudEvent,
TurbidityFNU], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.TurbidityFNU`: USGS turbidity data (FNU). Parameter code 63680.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.TurbidityFNU`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_turbidity_fnu_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
TurbidityFNU) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_turbidity_fnu_async = usgs_instantaneous_values_turbidity_fnu_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.TurbidityFNU`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_turbidity_fnu_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
TurbidityFNU) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_turbidity_fnu_async =
usgs_instantaneous_values_turbidity_fnu_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.TurbidityFNU`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_turbidity_fnu_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
TurbidityFNU) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_turbidity_fnu_async =
usgs_instantaneous_values_turbidity_fnu_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_f_dom_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_f_dom_async:  Callable[[ConsumerRecord, CloudEvent, FDOM],
Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.fDOM`: USGS dissolved organic matter fluorescence data (fDOM).
Parameter codes 32295 and 32322.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.FDOM`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_f_dom_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FDOM) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_f_dom_async = usgs_instantaneous_values_f_dom_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.FDOM`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_f_dom_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FDOM) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_f_dom_async = usgs_instantaneous_values_f_dom_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.FDOM`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_f_dom_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FDOM) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_f_dom_async = usgs_instantaneous_values_f_dom_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_reservoir_storage_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_reservoir_storage_async:  Callable[[ConsumerRecord,
CloudEvent, ReservoirStorage], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.ReservoirStorage`: USGS reservoir storage data. Parameter code
00054.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.ReservoirStorage`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_reservoir_storage_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
ReservoirStorage) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_reservoir_storage_async =
usgs_instantaneous_values_reservoir_storage_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.ReservoirStorage`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_reservoir_storage_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
ReservoirStorage) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_reservoir_storage_async =
usgs_instantaneous_values_reservoir_storage_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.ReservoirStorage`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_reservoir_storage_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
ReservoirStorage) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_reservoir_storage_async =
usgs_instantaneous_values_reservoir_storage_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_lake_elevation_ngvd29_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_lake_elevation_ngvd29_async:  Callable[[ConsumerRecord,
CloudEvent, LakeElevationNGVD29], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.LakeElevationNGVD29`: USGS lake or reservoir water surface
elevation above NGVD 1929, feet. Parameter code 62614.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.LakeElevationNGVD29`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_lake_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNGVD29) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_lake_elevation_ngvd29_async =
usgs_instantaneous_values_lake_elevation_ngvd29_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.LakeElevationNGVD29`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_lake_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNGVD29) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_lake_elevation_ngvd29_async =
usgs_instantaneous_values_lake_elevation_ngvd29_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.LakeElevationNGVD29`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_lake_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNGVD29) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_lake_elevation_ngvd29_async =
usgs_instantaneous_values_lake_elevation_ngvd29_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_water_depth_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_water_depth_async:  Callable[[ConsumerRecord, CloudEvent,
WaterDepth], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.WaterDepth`: USGS water depth data. Parameter code 72199.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterDepth`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_depth_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WaterDepth)
-> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_water_depth_async = usgs_instantaneous_values_water_depth_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterDepth`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_depth_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WaterDepth)
-> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_water_depth_async =
usgs_instantaneous_values_water_depth_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterDepth`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_depth_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WaterDepth)
-> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_water_depth_async =
usgs_instantaneous_values_water_depth_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_equipment_status_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_equipment_status_async:  Callable[[ConsumerRecord,
CloudEvent, EquipmentStatus], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.EquipmentStatus`: USGS equipment alarm status data. Parameter
code 99235.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.EquipmentStatus`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_equipment_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
EquipmentStatus) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_equipment_status_async =
usgs_instantaneous_values_equipment_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.EquipmentStatus`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_equipment_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
EquipmentStatus) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_equipment_status_async =
usgs_instantaneous_values_equipment_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.EquipmentStatus`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_equipment_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
EquipmentStatus) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_equipment_status_async =
usgs_instantaneous_values_equipment_status_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_tidally_filtered_discharge_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_tidally_filtered_discharge_async:  Callable[[ConsumerRecord,
CloudEvent, TidallyFilteredDischarge], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.TidallyFilteredDischarge`: USGS tidally filtered discharge data.
Parameter code 72137.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.TidallyFilteredDischarge`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_tidally_filtered_discharge_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: TidallyFilteredDischarge) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_tidally_filtered_discharge_async =
usgs_instantaneous_values_tidally_filtered_discharge_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.TidallyFilteredDischarge`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_tidally_filtered_discharge_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: TidallyFilteredDischarge) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_tidally_filtered_discharge_async =
usgs_instantaneous_values_tidally_filtered_discharge_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.TidallyFilteredDischarge`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_tidally_filtered_discharge_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: TidallyFilteredDischarge) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_tidally_filtered_discharge_async =
usgs_instantaneous_values_tidally_filtered_discharge_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_water_velocity_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_water_velocity_async:  Callable[[ConsumerRecord, CloudEvent,
WaterVelocity], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.WaterVelocity`: USGS water velocity data. Parameter code 72254.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterVelocity`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_velocity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterVelocity) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_water_velocity_async = usgs_instantaneous_values_water_velocity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterVelocity`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_velocity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterVelocity) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_water_velocity_async =
usgs_instantaneous_values_water_velocity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.WaterVelocity`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_water_velocity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterVelocity) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_water_velocity_async =
usgs_instantaneous_values_water_velocity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_estuary_elevation_ngvd29_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_estuary_elevation_ngvd29_async:  Callable[[ConsumerRecord,
CloudEvent, EstuaryElevationNGVD29], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.EstuaryElevationNGVD29`: USGS estuary or ocean water surface
elevation above NGVD 1929, feet. Parameter code 62619.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.EstuaryElevationNGVD29`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_estuary_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: EstuaryElevationNGVD29) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_estuary_elevation_ngvd29_async =
usgs_instantaneous_values_estuary_elevation_ngvd29_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.EstuaryElevationNGVD29`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_estuary_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: EstuaryElevationNGVD29) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_estuary_elevation_ngvd29_async =
usgs_instantaneous_values_estuary_elevation_ngvd29_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.EstuaryElevationNGVD29`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_estuary_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: EstuaryElevationNGVD29) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_estuary_elevation_ngvd29_async =
usgs_instantaneous_values_estuary_elevation_ngvd29_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_lake_elevation_navd88_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_lake_elevation_navd88_async:  Callable[[ConsumerRecord,
CloudEvent, LakeElevationNAVD88], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.LakeElevationNAVD88`: USGS lake or reservoir water surface
elevation above NAVD 1988, feet. Parameter code 62615.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.LakeElevationNAVD88`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_lake_elevation_navd88_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNAVD88) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_lake_elevation_navd88_async =
usgs_instantaneous_values_lake_elevation_navd88_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.LakeElevationNAVD88`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_lake_elevation_navd88_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNAVD88) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_lake_elevation_navd88_async =
usgs_instantaneous_values_lake_elevation_navd88_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.LakeElevationNAVD88`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_lake_elevation_navd88_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNAVD88) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_lake_elevation_navd88_async =
usgs_instantaneous_values_lake_elevation_navd88_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_salinity_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_salinity_async:  Callable[[ConsumerRecord, CloudEvent,
Salinity], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.Salinity`: USGS salinity data. Parameter code 00480.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.Salinity`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_salinity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Salinity) ->
None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_salinity_async = usgs_instantaneous_values_salinity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.Salinity`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_salinity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Salinity) ->
None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_salinity_async = usgs_instantaneous_values_salinity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.Salinity`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_salinity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Salinity) ->
None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_salinity_async = usgs_instantaneous_values_salinity_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration

    bootstrap_servers='localhost:9093',

    security_protocol='SASL_SSL',##### `usgs_instantaneous_values_gate_opening_async`

    sasl_mechanism='PLAIN',

    sasl_username='your-username',```python

    sasl_password='your-password'usgs_instantaneous_values_gate_opening_async:  Callable[[ConsumerRecord, CloudEvent,
GateOpening], Awaitable[None]]

)```

```

Asynchronous handler hook for `USGS.InstantaneousValues.GateOpening`: USGS gate opening data. Parameter code 45592.

## Generated Producer Classes

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSitesProducer- `data`: The event data of type `usgs_iv_producer_data.GateOpening`.



Producer for `USGS.Sites` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_gate_opening_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
GateOpening) -> None:

```python    # Process the event data

USGSSitesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_sites_dispatcher.usgs_instantaneous_values_gate_opening_async = usgs_instantaneous_values_gate_opening_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSSiteTimeseriesProducer- `data`: The event data of type `usgs_iv_producer_data.GateOpening`.



Producer for `USGS.SiteTimeseries` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_gate_opening_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
GateOpening) -> None:

```python    # Process the event data

USGSSiteTimeseriesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_site_timeseries_dispatcher.usgs_instantaneous_values_gate_opening_async =
usgs_instantaneous_values_gate_opening_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier- `record`: The Kafka record.

- `cloud_event`: The CloudEvent.

### USGSInstantaneousValuesProducer- `data`: The event data of type `usgs_iv_producer_data.GateOpening`.



Producer for `USGS.InstantaneousValues` message group.Example:



#### Constructor```python

async def usgs_instantaneous_values_gate_opening_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
GateOpening) -> None:

```python    # Process the event data

USGSInstantaneousValuesProducer(    await some_processing_function(record, cloud_event, data)

    bootstrap_servers: str,```

    client_id: Optional[str] = None,

    **kwargsThe handler function is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

) -> None

``````python

usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_gate_opening_async =
usgs_instantaneous_values_gate_opening_event

**Parameters:**```

- `bootstrap_servers`: Comma-separated list of broker addresses

- `client_id`: Optional client identifier

- `**kwargs`: Additional Kafka producer configuration



#### Send Methods## Internals



### Dispatchers

##### `send_usgs_instantaneous_values_other_parameter`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_other_parameter(

    self,##### `_process_event`

    data: OtherParameter,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.OtherParameter` message. USGS other parameter data.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `OtherParameter`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_other_parameter(

    data=OtherParameter(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.OtherParameter` messages in a batch.

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

await producer.send_usgs_instantaneous_values_other_parameter_batch(```

    messages=[

        OtherParameter(...),Initializes the runner with a Kafka consumer.

        OtherParameter(...),

        OtherParameter(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_precipitation`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_precipitation(

    self,##### `_process_event`

    data: Precipitation,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.Precipitation` message. USGS precipitation data. Parameter code 00045.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Precipitation`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_precipitation(

    data=Precipitation(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.Precipitation` messages in a batch.

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

await producer.send_usgs_instantaneous_values_precipitation_batch(```

    messages=[

        Precipitation(...),Initializes the runner with a Kafka consumer.

        Precipitation(...),

        Precipitation(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_streamflow`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_streamflow(

    self,##### `_process_event`

    data: Streamflow,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.Streamflow` message. USGS streamflow data. Parameter code 00060.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Streamflow`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_streamflow(

    data=Streamflow(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.Streamflow` messages in a batch.

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

await producer.send_usgs_instantaneous_values_streamflow_batch(```

    messages=[

        Streamflow(...),Initializes the runner with a Kafka consumer.

        Streamflow(...),

        Streamflow(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_gage_height`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_gage_height(

    self,##### `_process_event`

    data: GageHeight,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.GageHeight` message. USGS gage height data. Parameter code 00065.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `GageHeight`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_gage_height(

    data=GageHeight(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.GageHeight` messages in a batch.

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

await producer.send_usgs_instantaneous_values_gage_height_batch(```

    messages=[

        GageHeight(...),Initializes the runner with a Kafka consumer.

        GageHeight(...),

        GageHeight(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_water_temperature`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_water_temperature(

    self,##### `_process_event`

    data: WaterTemperature,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.WaterTemperature` message. USGS water temperature data. Parameter code
00010.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `WaterTemperature`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_water_temperature(

    data=WaterTemperature(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.WaterTemperature` messages in a batch.

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

await producer.send_usgs_instantaneous_values_water_temperature_batch(```

    messages=[

        WaterTemperature(...),Initializes the runner with a Kafka consumer.

        WaterTemperature(...),

        WaterTemperature(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_dissolved_oxygen`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_dissolved_oxygen(

    self,##### `_process_event`

    data: DissolvedOxygen,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.DissolvedOxygen` message. USGS dissolved oxygen data. Parameter code 00300.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `DissolvedOxygen`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_dissolved_oxygen(

    data=DissolvedOxygen(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.DissolvedOxygen` messages in a batch.

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

await producer.send_usgs_instantaneous_values_dissolved_oxygen_batch(```

    messages=[

        DissolvedOxygen(...),Initializes the runner with a Kafka consumer.

        DissolvedOxygen(...),

        DissolvedOxygen(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_p_h`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_p_h(

    self,##### `_process_event`

    data: PH,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.pH` message. USGS pH data. Parameter code 00400.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `PH`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_p_h(

    data=PH(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.pH` messages in a batch.

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

await producer.send_usgs_instantaneous_values_p_h_batch(```

    messages=[

        PH(...),Initializes the runner with a Kafka consumer.

        PH(...),

        PH(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_specific_conductance`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_specific_conductance(

    self,##### `_process_event`

    data: SpecificConductance,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.SpecificConductance` message. USGS specific conductance data. Parameter code
00095.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `SpecificConductance`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_specific_conductance(

    data=SpecificConductance(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.SpecificConductance` messages in a batch.

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

await producer.send_usgs_instantaneous_values_specific_conductance_batch(```

    messages=[

        SpecificConductance(...),Initializes the runner with a Kafka consumer.

        SpecificConductance(...),

        SpecificConductance(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_turbidity`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_turbidity(

    self,##### `_process_event`

    data: Turbidity,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.Turbidity` message. USGS turbidity data. Parameter code 00076.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Turbidity`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_turbidity(

    data=Turbidity(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.Turbidity` messages in a batch.

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

await producer.send_usgs_instantaneous_values_turbidity_batch(```

    messages=[

        Turbidity(...),Initializes the runner with a Kafka consumer.

        Turbidity(...),

        Turbidity(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_air_temperature`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_air_temperature(

    self,##### `_process_event`

    data: AirTemperature,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.AirTemperature` message. USGS air temperature data. Parameter code 00020.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `AirTemperature`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_air_temperature(

    data=AirTemperature(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.AirTemperature` messages in a batch.

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

await producer.send_usgs_instantaneous_values_air_temperature_batch(```

    messages=[

        AirTemperature(...),Initializes the runner with a Kafka consumer.

        AirTemperature(...),

        AirTemperature(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_wind_speed`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_wind_speed(

    self,##### `_process_event`

    data: WindSpeed,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.WindSpeed` message. USGS wind speed data. Parameter code 00035.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `WindSpeed`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_wind_speed(

    data=WindSpeed(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.WindSpeed` messages in a batch.

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

await producer.send_usgs_instantaneous_values_wind_speed_batch(```

    messages=[

        WindSpeed(...),Initializes the runner with a Kafka consumer.

        WindSpeed(...),

        WindSpeed(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_wind_direction`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_wind_direction(

    self,##### `_process_event`

    data: WindDirection,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.WindDirection` message. USGS wind direction data. Parameter codes 00036 and
163695.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `WindDirection`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_wind_direction(

    data=WindDirection(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.WindDirection` messages in a batch.

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

await producer.send_usgs_instantaneous_values_wind_direction_batch(```

    messages=[

        WindDirection(...),Initializes the runner with a Kafka consumer.

        WindDirection(...),

        WindDirection(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_relative_humidity`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_relative_humidity(

    self,##### `_process_event`

    data: RelativeHumidity,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.RelativeHumidity` message. USGS relative humidity data. Parameter code
00052.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `RelativeHumidity`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_relative_humidity(

    data=RelativeHumidity(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.RelativeHumidity` messages in a batch.

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

await producer.send_usgs_instantaneous_values_relative_humidity_batch(```

    messages=[

        RelativeHumidity(...),Initializes the runner with a Kafka consumer.

        RelativeHumidity(...),

        RelativeHumidity(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_barometric_pressure`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_barometric_pressure(

    self,##### `_process_event`

    data: BarometricPressure,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.BarometricPressure` message. USGS barometric pressure data. Parameter codes
62605 and 75969.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `BarometricPressure`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_barometric_pressure(

    data=BarometricPressure(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.BarometricPressure` messages in a batch.

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

await producer.send_usgs_instantaneous_values_barometric_pressure_batch(```

    messages=[

        BarometricPressure(...),Initializes the runner with a Kafka consumer.

        BarometricPressure(...),

        BarometricPressure(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_turbidity_fnu`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_turbidity_fnu(

    self,##### `_process_event`

    data: TurbidityFNU,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.TurbidityFNU` message. USGS turbidity data (FNU). Parameter code 63680.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TurbidityFNU`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_turbidity_fnu(

    data=TurbidityFNU(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.TurbidityFNU` messages in a batch.

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

await producer.send_usgs_instantaneous_values_turbidity_fnu_batch(```

    messages=[

        TurbidityFNU(...),Initializes the runner with a Kafka consumer.

        TurbidityFNU(...),

        TurbidityFNU(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_f_dom`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_f_dom(

    self,##### `_process_event`

    data: FDOM,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.fDOM` message. USGS dissolved organic matter fluorescence data (fDOM). Parameter
codes 32295 and 32322.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `FDOM`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_f_dom(

    data=FDOM(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.fDOM` messages in a batch.

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

await producer.send_usgs_instantaneous_values_f_dom_batch(```

    messages=[

        FDOM(...),Initializes the runner with a Kafka consumer.

        FDOM(...),

        FDOM(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_reservoir_storage`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_reservoir_storage(

    self,##### `_process_event`

    data: ReservoirStorage,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.ReservoirStorage` message. USGS reservoir storage data. Parameter code
00054.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `ReservoirStorage`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_reservoir_storage(

    data=ReservoirStorage(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.ReservoirStorage` messages in a batch.

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

await producer.send_usgs_instantaneous_values_reservoir_storage_batch(```

    messages=[

        ReservoirStorage(...),Initializes the runner with a Kafka consumer.

        ReservoirStorage(...),

        ReservoirStorage(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_lake_elevation_ngvd29`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_lake_elevation_ngvd29(

    self,##### `_process_event`

    data: LakeElevationNGVD29,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.LakeElevationNGVD29` message. USGS lake or reservoir water surface elevation
above NGVD 1929, feet. Parameter code 62614.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `LakeElevationNGVD29`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_lake_elevation_ngvd29(

    data=LakeElevationNGVD29(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.LakeElevationNGVD29` messages in a batch.

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

await producer.send_usgs_instantaneous_values_lake_elevation_ngvd29_batch(```

    messages=[

        LakeElevationNGVD29(...),Initializes the runner with a Kafka consumer.

        LakeElevationNGVD29(...),

        LakeElevationNGVD29(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_water_depth`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_water_depth(

    self,##### `_process_event`

    data: WaterDepth,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.WaterDepth` message. USGS water depth data. Parameter code 72199.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `WaterDepth`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_water_depth(

    data=WaterDepth(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.WaterDepth` messages in a batch.

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

await producer.send_usgs_instantaneous_values_water_depth_batch(```

    messages=[

        WaterDepth(...),Initializes the runner with a Kafka consumer.

        WaterDepth(...),

        WaterDepth(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_equipment_status`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_equipment_status(

    self,##### `_process_event`

    data: EquipmentStatus,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.EquipmentStatus` message. USGS equipment alarm status data. Parameter code
99235.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `EquipmentStatus`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_equipment_status(

    data=EquipmentStatus(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.EquipmentStatus` messages in a batch.

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

await producer.send_usgs_instantaneous_values_equipment_status_batch(```

    messages=[

        EquipmentStatus(...),Initializes the runner with a Kafka consumer.

        EquipmentStatus(...),

        EquipmentStatus(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_tidally_filtered_discharge`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_tidally_filtered_discharge(

    self,##### `_process_event`

    data: TidallyFilteredDischarge,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.TidallyFilteredDischarge` message. USGS tidally filtered discharge data.
Parameter code 72137.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `TidallyFilteredDischarge`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_tidally_filtered_discharge(

    data=TidallyFilteredDischarge(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.TidallyFilteredDischarge` messages in a batch.

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

await producer.send_usgs_instantaneous_values_tidally_filtered_discharge_batch(```

    messages=[

        TidallyFilteredDischarge(...),Initializes the runner with a Kafka consumer.

        TidallyFilteredDischarge(...),

        TidallyFilteredDischarge(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_water_velocity`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_water_velocity(

    self,##### `_process_event`

    data: WaterVelocity,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.WaterVelocity` message. USGS water velocity data. Parameter code 72254.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `WaterVelocity`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_water_velocity(

    data=WaterVelocity(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.WaterVelocity` messages in a batch.

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

await producer.send_usgs_instantaneous_values_water_velocity_batch(```

    messages=[

        WaterVelocity(...),Initializes the runner with a Kafka consumer.

        WaterVelocity(...),

        WaterVelocity(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_estuary_elevation_ngvd29`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_estuary_elevation_ngvd29(

    self,##### `_process_event`

    data: EstuaryElevationNGVD29,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.EstuaryElevationNGVD29` message. USGS estuary or ocean water surface elevation
above NGVD 1929, feet. Parameter code 62619.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `EstuaryElevationNGVD29`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_estuary_elevation_ngvd29(

    data=EstuaryElevationNGVD29(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.EstuaryElevationNGVD29` messages in a batch.

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

await producer.send_usgs_instantaneous_values_estuary_elevation_ngvd29_batch(```

    messages=[

        EstuaryElevationNGVD29(...),Initializes the runner with a Kafka consumer.

        EstuaryElevationNGVD29(...),

        EstuaryElevationNGVD29(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_lake_elevation_navd88`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_lake_elevation_navd88(

    self,##### `_process_event`

    data: LakeElevationNAVD88,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.LakeElevationNAVD88` message. USGS lake or reservoir water surface elevation
above NAVD 1988, feet. Parameter code 62615.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `LakeElevationNAVD88`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_lake_elevation_navd88(

    data=LakeElevationNAVD88(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.LakeElevationNAVD88` messages in a batch.

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

await producer.send_usgs_instantaneous_values_lake_elevation_navd88_batch(```

    messages=[

        LakeElevationNAVD88(...),Initializes the runner with a Kafka consumer.

        LakeElevationNAVD88(...),

        LakeElevationNAVD88(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_salinity`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_salinity(

    self,##### `_process_event`

    data: Salinity,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.Salinity` message. USGS salinity data. Parameter code 00480.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `Salinity`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_salinity(

    data=Salinity(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.Salinity` messages in a batch.

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

await producer.send_usgs_instantaneous_values_salinity_batch(```

    messages=[

        Salinity(...),Initializes the runner with a Kafka consumer.

        Salinity(...),

        Salinity(...)Args:

    ],- `consumer`: The Kafka consumer.

    partition_key='batch-001'

)#####  `__aenter__()`

```

Enters the asynchronous context and starts the processor.

### Dispatchers

##### `send_usgs_instantaneous_values_gate_opening`Dispatchers have the following protected methods:



```python### Methods:

async def send_usgs_instantaneous_values_gate_opening(

    self,##### `_process_event`

    data: GateOpening,

    partition_key: Optional[str] = None,```python

    headers: Optional[Dict[str, str]] = None,_process_event(self, record)

    topic: Optional[str] = None```

) -> None

```Processes an incoming event.



Send a single `USGS.InstantaneousValues.GateOpening` message. USGS gate opening data. Parameter code 45592.Args:

- `record`: The Kafka record.

**Parameters:**

- `data`: Message data of type `GateOpening`

- `partition_key`: Optional partition key (defaults to random partitioning)##### `_dispatch_cloud_event`

- `headers`: Optional message headers

- `topic`: Optional topic override (uses default topic if not specified)```python

_dispatch_cloud_event(self, record, cloud_event)

**Example:**```



```pythonDispatches a CloudEvent to the appropriate handler.

await producer.send_usgs_instantaneous_values_gate_opening(

    data=GateOpening(...),Args:

    partition_key='device-001',- `record`: The Kafka record.

    headers={'source': 'sensor-gateway'}- `cloud_event`: The CloudEvent.

)

```

Send multiple `USGS.InstantaneousValues.GateOpening` messages in a batch.

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

await producer.send_usgs_instantaneous_values_gate_opening_batch(```

    messages=[

        GateOpening(...),Initializes the runner with a Kafka consumer.

        GateOpening(...),

        GateOpening(...)Args:

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
