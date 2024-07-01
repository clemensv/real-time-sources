
# Rssbridge_producer Event Dispatcher for Apache Kafka

This module provides an event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages
and CloudEvents.

## Table of Contents
1. [Overview](#overview)
2. [Generated Event Dispatchers](#generated-event-dispatchers)
    - MicrosoftOpenDataRssFeedsEventDispatcher

3. [Internals](#internals)
    - [EventProcessorRunner](#eventprocessorrunner)
    - [_DispatcherBase](#_dispatcherbase)

## Overview

This module defines an event processing framework for Apache Kafka,
providing the necessary classes and methods to handle various types of events.
It includes both plain Kafka messages and CloudEvents, offering a versatile
solution for event-driven applications.

## Generated Event Dispatchers



### MicrosoftOpenDataRssFeedsEventDispatcher

`MicrosoftOpenDataRssFeedsEventDispatcher` handles events for the Microsoft.OpenData.RssFeeds message group.

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

The MicrosoftOpenDataRssFeedsEventDispatcher defines the following event handler hooks.


##### `microsoft_open_data_rss_feeds_feed_item_async`

```python
microsoft_open_data_rss_feeds_feed_item_async:  Callable[[ConsumerRecord, CloudEvent, FeedItem], Awaitable[None]]
```

Asynchronous handler hook for `Microsoft.OpenData.RssFeeds.FeedItem`: A new item has been added to the RSS feed.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `rssbridge_producer_data.microsoft.opendata.rssfeeds.FeedItem`.

Example:

```python
async def microsoft_open_data_rss_feeds_feed_item_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FeedItem)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
microsoft_open_data_rss_feeds_dispatcher.microsoft_open_data_rss_feeds_feed_item_async =
microsoft_open_data_rss_feeds_feed_item_event
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