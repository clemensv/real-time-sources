
# Usgs_iv_producer Event Dispatcher for Apache Kafka

This module provides an event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages
and CloudEvents.

## Table of Contents
1. [Overview](#overview)
2. [Generated Event Dispatchers](#generated-event-dispatchers)
    - USGSInstantaneousValuesEventDispatcher

3. [Internals](#internals)
    - [EventProcessorRunner](#eventprocessorrunner)
    - [_DispatcherBase](#_dispatcherbase)

## Overview

This module defines an event processing framework for Apache Kafka,
providing the necessary classes and methods to handle various types of events.
It includes both plain Kafka messages and CloudEvents, offering a versatile
solution for event-driven applications.

## Generated Event Dispatchers



### USGSInstantaneousValuesEventDispatcher

`USGSInstantaneousValuesEventDispatcher` handles events for the USGS.InstantaneousValues message group.

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

The USGSInstantaneousValuesEventDispatcher defines the following event handler hooks.


##### `usgs_instantaneous_values_streamflow_async`

```python
usgs_instantaneous_values_streamflow_async:  Callable[[ConsumerRecord, CloudEvent, Streamflow], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.Streamflow`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_producer_data.usgs.instantaneousvalues.Streamflow`.

Example:

```python
async def usgs_instantaneous_values_streamflow_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Streamflow)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_streamflow_async =
usgs_instantaneous_values_streamflow_event
```


##### `usgs_instantaneous_values_gage_height_async`

```python
usgs_instantaneous_values_gage_height_async:  Callable[[ConsumerRecord, CloudEvent, GageHeight], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.GageHeight`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_producer_data.usgs.instantaneousvalues.GageHeight`.

Example:

```python
async def usgs_instantaneous_values_gage_height_event(record: ConsumerRecord, cloud_event: CloudEvent, data: GageHeight)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_gage_height_async =
usgs_instantaneous_values_gage_height_event
```


##### `usgs_instantaneous_values_water_temperature_async`

```python
usgs_instantaneous_values_water_temperature_async:  Callable[[ConsumerRecord, CloudEvent, WaterTemperature],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.WaterTemperature`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_producer_data.usgs.instantaneousvalues.WaterTemperature`.

Example:

```python
async def usgs_instantaneous_values_water_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterTemperature) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_water_temperature_async =
usgs_instantaneous_values_water_temperature_event
```


##### `usgs_instantaneous_values_dissolved_oxygen_async`

```python
usgs_instantaneous_values_dissolved_oxygen_async:  Callable[[ConsumerRecord, CloudEvent, DissolvedOxygen],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.DissolvedOxygen`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_producer_data.usgs.instantaneousvalues.DissolvedOxygen`.

Example:

```python
async def usgs_instantaneous_values_dissolved_oxygen_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
DissolvedOxygen) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_dissolved_oxygen_async =
usgs_instantaneous_values_dissolved_oxygen_event
```


##### `usgs_instantaneous_values_p_h_async`

```python
usgs_instantaneous_values_p_h_async:  Callable[[ConsumerRecord, CloudEvent, PH], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.pH`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_producer_data.usgs.instantaneousvalues.PH`.

Example:

```python
async def usgs_instantaneous_values_p_h_event(record: ConsumerRecord, cloud_event: CloudEvent, data: PH) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_p_h_async = usgs_instantaneous_values_p_h_event
```


##### `usgs_instantaneous_values_specific_conductance_async`

```python
usgs_instantaneous_values_specific_conductance_async:  Callable[[ConsumerRecord, CloudEvent, SpecificConductance],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.SpecificConductance`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_producer_data.usgs.instantaneousvalues.SpecificConductance`.

Example:

```python
async def usgs_instantaneous_values_specific_conductance_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
SpecificConductance) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_specific_conductance_async =
usgs_instantaneous_values_specific_conductance_event
```


##### `usgs_instantaneous_values_turbidity_async`

```python
usgs_instantaneous_values_turbidity_async:  Callable[[ConsumerRecord, CloudEvent, Turbidity], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.Turbidity`:

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_producer_data.usgs.instantaneousvalues.Turbidity`.

Example:

```python
async def usgs_instantaneous_values_turbidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Turbidity) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_turbidity_async =
usgs_instantaneous_values_turbidity_event
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