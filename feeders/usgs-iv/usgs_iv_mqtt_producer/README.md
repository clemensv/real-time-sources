# Usgs_iv_mqtt_producer MQTT Client

This library provides MQTT producer and consumer functionality for the usgs_iv_mqtt_producer message definitions.

# Usgs_iv_mqtt_producer Event Dispatcher for Azure Event Hubs

## Installation

This module provides an event dispatcher for processing events from Azure Event Hubs. It supports both plain AMQP
messages and CloudEvents.

```bash

./install.sh  # Unix/Linux/Mac## Table of Contents

# or1. [Overview](#overview)

install.bat  # Windows2. [Generated Event Dispatchers](#generated-event-dispatchers)

```    - USGSSitesMqttEventDispatcher,

    USGSSiteTimeseriesMqttEventDispatcher,

    USGSInstantaneousValuesMqttEventDispatcher



## Quick Start3. [Internals](#internals)

    - [EventProcessorRunner](#eventprocessorrunner)

### Publishing Messages    - [_DispatcherBase](#_dispatcherbase)



```python## Overview

import paho.mqtt.client as mqtt

from usgs_iv_mqtt_producer_mqtt_client import *This module defines an event processing framework for Azure Event Hubs,

providing the necessary classes and methods to handle various types of events.

# Create MQTT client and wrapperIt includes both plain AMQP messages and CloudEvents, offering a versatile

mqtt_client = mqtt.Client(client_id="publisher")solution for event-driven applications.## Generated Event Dispatchers

client = USGSSitesMqttMqttClient(mqtt_client, content_mode='structured')

# Connect to broker

await client.connect("mqtt.example.com", 1883)### USGSSitesMqttEventDispatcher



# Publish message`USGSSitesMqttEventDispatcher` handles events for the USGS.Sites.mqtt message group.

await client.publish_message(

    topic="my/topic",#### Methods:

    # ... CloudEvents attributes

    data=data_object##### `__init__`:

)

```python

await client.disconnect()__init__(self)-> None

``````



### Subscribing to MessagesInitializes the dispatcher.



```python##### `create_processor`:

import paho.mqtt.client as mqtt

import asyncio```python

from usgs_iv_mqtt_producer_mqtt_client import *create_processor(self, consumer_group_name: str,
eventhubs_fully_qualified_namespace: str, eventhub_name: str, blob_account_url: str, blob_container_name: str,
credential) -> EventProcessorRunner`

```

# Create MQTT client and wrapper

mqtt_client = mqtt.Client(client_id="subscriber")Creates an `EventProcessorRunner`.Args:- `consumer_group_name`: The
name of the consumer group.- `eventhubs_fully_qualified_namespace`: The fully qualified namespace of the Event Hub.

client = USGSSitesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the Event
Hub.Args:- `consumer_group_name`: The name of the consumer group.- `eventhubs_fully_qualified_namespace`: The fully
qualified namespace of the Event Hub.

client = USGSSiteTimeseriesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the
Event Hub.Args:- `consumer_group_name`: The name of the consumer group.- `eventhubs_fully_qualified_namespace`: The
fully qualified namespace of the Event Hub.

client = USGSInstantaneousValuesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the
Event Hub.- `blob_account_url`: The URL of the Azure Storage account.

- `blob_container_name`: The name of the blob container to store checkpoints.

# Define message handler- `credential`: The credential to use for authentication.

async def on_message(mqtt_msg, cloud_event, data):

    print(f"Received: {data}")##### `create_processor_from_connection_strings`



# Register handler```python

client.message_handler_async = on_message`create_processor_from_connection_strings(self, consumer_group_name: str,
connection_str: str, eventhub_name: str, blob_conn_str: str, checkpoint_container: str) -> EventProcessorRunner`

```

# Connect and subscribe

await client.connect("mqtt.example.com", 1883)Creates an `EventProcessorRunner` from connection strings.

await client.subscribe(["my/topic/#"])

Args:

# Keep running- `consumer_group_name`: The name of the consumer group.

try:- `connection_str`: The connection string for the Event Hub.

    while True:- `eventhub_name`: The name of the Event Hub.

        await asyncio.sleep(1)- `blob_conn_str`: The connection string for the Azure Storage account.

finally:- `checkpoint_container`: The name of the blob container to store checkpoints.

    await client.disconnect()

```#### Event Handlers



## BuildThe USGSSitesMqttEventDispatcher defines the following event handler hooks.



```bash

make build

```##### `usgs_sites_mqtt_site_async`



## Test```python

usgs_sites_mqtt_site_async:  Callable[[PartitionContext, EventData, CloudEvent, Site], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.Sites.mqtt.Site`: USGS site metadata.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.Site`.

Example:

```python
async def usgs_sites_mqtt_site_event(partition_context: PartitionContext, event: EventData, cloud_event: CloudEvent,
data: Site) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_sites_mqtt_dispatcher.usgs_sites_mqtt_site_async = usgs_sites_mqtt_site_event
```


## Generated Event Dispatchers

client = USGSSiteTimeseriesMqttMqttClient(mqtt_client, content_mode='structured')

# Connect to broker

await client.connect("mqtt.example.com", 1883)### USGSSiteTimeseriesMqttEventDispatcher



# Publish message`USGSSiteTimeseriesMqttEventDispatcher` handles events for the USGS.SiteTimeseries.mqtt message group.

await client.publish_message(

    topic="my/topic",#### Methods:

    # ... CloudEvents attributes

    data=data_object##### `__init__`:

)

```python

await client.disconnect()__init__(self)-> None

``````



### Subscribing to MessagesInitializes the dispatcher.



```python##### `create_processor`:

import paho.mqtt.client as mqtt

import asyncio```python

from usgs_iv_mqtt_producer_mqtt_client import *create_processor(self, consumer_group_name: str,
eventhubs_fully_qualified_namespace: str, eventhub_name: str, blob_account_url: str, blob_container_name: str,
credential) -> EventProcessorRunner`

```

# Create MQTT client and wrapper

mqtt_client = mqtt.Client(client_id="subscriber")Creates an `EventProcessorRunner`.Args:- `consumer_group_name`: The
name of the consumer group.- `eventhubs_fully_qualified_namespace`: The fully qualified namespace of the Event Hub.

client = USGSSitesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the Event
Hub.Args:- `consumer_group_name`: The name of the consumer group.- `eventhubs_fully_qualified_namespace`: The fully
qualified namespace of the Event Hub.

client = USGSSiteTimeseriesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the
Event Hub.Args:- `consumer_group_name`: The name of the consumer group.- `eventhubs_fully_qualified_namespace`: The
fully qualified namespace of the Event Hub.

client = USGSInstantaneousValuesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the
Event Hub.- `blob_account_url`: The URL of the Azure Storage account.

- `blob_container_name`: The name of the blob container to store checkpoints.

# Define message handler- `credential`: The credential to use for authentication.

async def on_message(mqtt_msg, cloud_event, data):

    print(f"Received: {data}")##### `create_processor_from_connection_strings`



# Register handler```python

client.message_handler_async = on_message`create_processor_from_connection_strings(self, consumer_group_name: str,
connection_str: str, eventhub_name: str, blob_conn_str: str, checkpoint_container: str) -> EventProcessorRunner`

```

# Connect and subscribe

await client.connect("mqtt.example.com", 1883)Creates an `EventProcessorRunner` from connection strings.

await client.subscribe(["my/topic/#"])

Args:

# Keep running- `consumer_group_name`: The name of the consumer group.

try:- `connection_str`: The connection string for the Event Hub.

    while True:- `eventhub_name`: The name of the Event Hub.

        await asyncio.sleep(1)- `blob_conn_str`: The connection string for the Azure Storage account.

finally:- `checkpoint_container`: The name of the blob container to store checkpoints.

    await client.disconnect()

```#### Event Handlers



## BuildThe USGSSiteTimeseriesMqttEventDispatcher defines the following event handler hooks.



```bash

make build

```##### `usgs_site_timeseries_mqtt_site_timeseries_async`



## Test```python

usgs_site_timeseries_mqtt_site_timeseries_async:  Callable[[PartitionContext, EventData, CloudEvent, SiteTimeseries],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.SiteTimeseries.mqtt.SiteTimeseries`: USGS site timeseries metadata.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.SiteTimeseries`.

Example:

```python
async def usgs_site_timeseries_mqtt_site_timeseries_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: SiteTimeseries) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_site_timeseries_mqtt_dispatcher.usgs_site_timeseries_mqtt_site_timeseries_async =
usgs_site_timeseries_mqtt_site_timeseries_event
```


## Generated Event Dispatchers

client = USGSInstantaneousValuesMqttMqttClient(mqtt_client, content_mode='structured')

# Connect to broker

await client.connect("mqtt.example.com", 1883)### USGSInstantaneousValuesMqttEventDispatcher



# Publish message`USGSInstantaneousValuesMqttEventDispatcher` handles events for the USGS.InstantaneousValues.mqtt
message group.

await client.publish_message(

    topic="my/topic",#### Methods:

    # ... CloudEvents attributes

    data=data_object##### `__init__`:

)

```python

await client.disconnect()__init__(self)-> None

``````



### Subscribing to MessagesInitializes the dispatcher.



```python##### `create_processor`:

import paho.mqtt.client as mqtt

import asyncio```python

from usgs_iv_mqtt_producer_mqtt_client import *create_processor(self, consumer_group_name: str,
eventhubs_fully_qualified_namespace: str, eventhub_name: str, blob_account_url: str, blob_container_name: str,
credential) -> EventProcessorRunner`

```

# Create MQTT client and wrapper

mqtt_client = mqtt.Client(client_id="subscriber")Creates an `EventProcessorRunner`.Args:- `consumer_group_name`: The
name of the consumer group.- `eventhubs_fully_qualified_namespace`: The fully qualified namespace of the Event Hub.

client = USGSSitesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the Event
Hub.Args:- `consumer_group_name`: The name of the consumer group.- `eventhubs_fully_qualified_namespace`: The fully
qualified namespace of the Event Hub.

client = USGSSiteTimeseriesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the
Event Hub.Args:- `consumer_group_name`: The name of the consumer group.- `eventhubs_fully_qualified_namespace`: The
fully qualified namespace of the Event Hub.

client = USGSInstantaneousValuesMqttMqttClient(mqtt_client, content_mode='structured')- `eventhub_name`: The name of the
Event Hub.- `blob_account_url`: The URL of the Azure Storage account.

- `blob_container_name`: The name of the blob container to store checkpoints.

# Define message handler- `credential`: The credential to use for authentication.

async def on_message(mqtt_msg, cloud_event, data):

    print(f"Received: {data}")##### `create_processor_from_connection_strings`



# Register handler```python

client.message_handler_async = on_message`create_processor_from_connection_strings(self, consumer_group_name: str,
connection_str: str, eventhub_name: str, blob_conn_str: str, checkpoint_container: str) -> EventProcessorRunner`

```

# Connect and subscribe

await client.connect("mqtt.example.com", 1883)Creates an `EventProcessorRunner` from connection strings.

await client.subscribe(["my/topic/#"])

Args:

# Keep running- `consumer_group_name`: The name of the consumer group.

try:- `connection_str`: The connection string for the Event Hub.

    while True:- `eventhub_name`: The name of the Event Hub.

        await asyncio.sleep(1)- `blob_conn_str`: The connection string for the Azure Storage account.

finally:- `checkpoint_container`: The name of the blob container to store checkpoints.

    await client.disconnect()

```#### Event Handlers



## BuildThe USGSInstantaneousValuesMqttEventDispatcher defines the following event handler hooks.



```bash

make build

```##### `usgs_instantaneous_values_mqtt_other_parameter_async`



## Test```python

usgs_instantaneous_values_mqtt_other_parameter_async:  Callable[[PartitionContext, EventData, CloudEvent,
OtherParameter], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.OtherParameter`: USGS other parameter data.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.OtherParameter`.

Example:

```python
async def usgs_instantaneous_values_mqtt_other_parameter_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: OtherParameter) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_other_parameter_async =
usgs_instantaneous_values_mqtt_other_parameter_event
```



make build

```##### `usgs_instantaneous_values_mqtt_precipitation_async`



## Test```python

usgs_instantaneous_values_mqtt_precipitation_async:  Callable[[PartitionContext, EventData, CloudEvent, Precipitation],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.Precipitation`: USGS precipitation data. Parameter code
00045.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.Precipitation`.

Example:

```python
async def usgs_instantaneous_values_mqtt_precipitation_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: Precipitation) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_precipitation_async =
usgs_instantaneous_values_mqtt_precipitation_event
```



make build

```##### `usgs_instantaneous_values_mqtt_streamflow_async`



## Test```python

usgs_instantaneous_values_mqtt_streamflow_async:  Callable[[PartitionContext, EventData, CloudEvent, Streamflow],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.Streamflow`: USGS streamflow data. Parameter code 00060.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.Streamflow`.

Example:

```python
async def usgs_instantaneous_values_mqtt_streamflow_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: Streamflow) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_streamflow_async =
usgs_instantaneous_values_mqtt_streamflow_event
```



make build

```##### `usgs_instantaneous_values_mqtt_gage_height_async`



## Test```python

usgs_instantaneous_values_mqtt_gage_height_async:  Callable[[PartitionContext, EventData, CloudEvent, GageHeight],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.GageHeight`: USGS gage height data. Parameter code
00065.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.GageHeight`.

Example:

```python
async def usgs_instantaneous_values_mqtt_gage_height_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: GageHeight) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_gage_height_async =
usgs_instantaneous_values_mqtt_gage_height_event
```



make build

```##### `usgs_instantaneous_values_mqtt_water_temperature_async`



## Test```python

usgs_instantaneous_values_mqtt_water_temperature_async:  Callable[[PartitionContext, EventData, CloudEvent,
WaterTemperature], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.WaterTemperature`: USGS water temperature data.
Parameter code 00010.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.WaterTemperature`.

Example:

```python
async def usgs_instantaneous_values_mqtt_water_temperature_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: WaterTemperature) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_water_temperature_async =
usgs_instantaneous_values_mqtt_water_temperature_event
```



make build

```##### `usgs_instantaneous_values_mqtt_dissolved_oxygen_async`



## Test```python

usgs_instantaneous_values_mqtt_dissolved_oxygen_async:  Callable[[PartitionContext, EventData, CloudEvent,
DissolvedOxygen], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.DissolvedOxygen`: USGS dissolved oxygen data. Parameter
code 00300.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.DissolvedOxygen`.

Example:

```python
async def usgs_instantaneous_values_mqtt_dissolved_oxygen_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: DissolvedOxygen) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_dissolved_oxygen_async =
usgs_instantaneous_values_mqtt_dissolved_oxygen_event
```



make build

```##### `usgs_instantaneous_values_mqtt_p_h_async`



## Test```python

usgs_instantaneous_values_mqtt_p_h_async:  Callable[[PartitionContext, EventData, CloudEvent, PH], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.pH`: USGS pH data. Parameter code 00400.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.PH`.

Example:

```python
async def usgs_instantaneous_values_mqtt_p_h_event(partition_context: PartitionContext, event: EventData, cloud_event:
CloudEvent, data: PH) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_p_h_async =
usgs_instantaneous_values_mqtt_p_h_event
```



make build

```##### `usgs_instantaneous_values_mqtt_specific_conductance_async`



## Test```python

usgs_instantaneous_values_mqtt_specific_conductance_async:  Callable[[PartitionContext, EventData, CloudEvent,
SpecificConductance], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.SpecificConductance`: USGS specific conductance data.
Parameter code 00095.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.SpecificConductance`.

Example:

```python
async def usgs_instantaneous_values_mqtt_specific_conductance_event(partition_context: PartitionContext, event:
EventData, cloud_event: CloudEvent, data: SpecificConductance) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_specific_conductance_async =
usgs_instantaneous_values_mqtt_specific_conductance_event
```



make build

```##### `usgs_instantaneous_values_mqtt_turbidity_async`



## Test```python

usgs_instantaneous_values_mqtt_turbidity_async:  Callable[[PartitionContext, EventData, CloudEvent, Turbidity],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.Turbidity`: USGS turbidity data. Parameter code 00076.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.Turbidity`.

Example:

```python
async def usgs_instantaneous_values_mqtt_turbidity_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: Turbidity) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_turbidity_async =
usgs_instantaneous_values_mqtt_turbidity_event
```



make build

```##### `usgs_instantaneous_values_mqtt_air_temperature_async`



## Test```python

usgs_instantaneous_values_mqtt_air_temperature_async:  Callable[[PartitionContext, EventData, CloudEvent,
AirTemperature], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.AirTemperature`: USGS air temperature data. Parameter
code 00020.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.AirTemperature`.

Example:

```python
async def usgs_instantaneous_values_mqtt_air_temperature_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: AirTemperature) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_air_temperature_async =
usgs_instantaneous_values_mqtt_air_temperature_event
```



make build

```##### `usgs_instantaneous_values_mqtt_wind_speed_async`



## Test```python

usgs_instantaneous_values_mqtt_wind_speed_async:  Callable[[PartitionContext, EventData, CloudEvent, WindSpeed],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.WindSpeed`: USGS wind speed data. Parameter code 00035.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.WindSpeed`.

Example:

```python
async def usgs_instantaneous_values_mqtt_wind_speed_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: WindSpeed) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_wind_speed_async =
usgs_instantaneous_values_mqtt_wind_speed_event
```



make build

```##### `usgs_instantaneous_values_mqtt_wind_direction_async`



## Test```python

usgs_instantaneous_values_mqtt_wind_direction_async:  Callable[[PartitionContext, EventData, CloudEvent, WindDirection],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.WindDirection`: USGS wind direction data. Parameter
codes 00036 and 163695.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.WindDirection`.

Example:

```python
async def usgs_instantaneous_values_mqtt_wind_direction_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: WindDirection) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_wind_direction_async =
usgs_instantaneous_values_mqtt_wind_direction_event
```



make build

```##### `usgs_instantaneous_values_mqtt_relative_humidity_async`



## Test```python

usgs_instantaneous_values_mqtt_relative_humidity_async:  Callable[[PartitionContext, EventData, CloudEvent,
RelativeHumidity], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.RelativeHumidity`: USGS relative humidity data.
Parameter code 00052.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.RelativeHumidity`.

Example:

```python
async def usgs_instantaneous_values_mqtt_relative_humidity_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: RelativeHumidity) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_relative_humidity_async =
usgs_instantaneous_values_mqtt_relative_humidity_event
```



make build

```##### `usgs_instantaneous_values_mqtt_barometric_pressure_async`



## Test```python

usgs_instantaneous_values_mqtt_barometric_pressure_async:  Callable[[PartitionContext, EventData, CloudEvent,
BarometricPressure], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.BarometricPressure`: USGS barometric pressure data.
Parameter codes 62605 and 75969.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.BarometricPressure`.

Example:

```python
async def usgs_instantaneous_values_mqtt_barometric_pressure_event(partition_context: PartitionContext, event:
EventData, cloud_event: CloudEvent, data: BarometricPressure) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_barometric_pressure_async =
usgs_instantaneous_values_mqtt_barometric_pressure_event
```



make build

```##### `usgs_instantaneous_values_mqtt_turbidity_fnu_async`



## Test```python

usgs_instantaneous_values_mqtt_turbidity_fnu_async:  Callable[[PartitionContext, EventData, CloudEvent, TurbidityFNU],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.TurbidityFNU`: USGS turbidity data (FNU). Parameter code
63680.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.TurbidityFNU`.

Example:

```python
async def usgs_instantaneous_values_mqtt_turbidity_fnu_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: TurbidityFNU) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_turbidity_fnu_async =
usgs_instantaneous_values_mqtt_turbidity_fnu_event
```



make build

```##### `usgs_instantaneous_values_mqtt_f_dom_async`



## Test```python

usgs_instantaneous_values_mqtt_f_dom_async:  Callable[[PartitionContext, EventData, CloudEvent, FDOM], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.fDOM`: USGS dissolved organic matter fluorescence data
(fDOM). Parameter codes 32295 and 32322.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.FDOM`.

Example:

```python
async def usgs_instantaneous_values_mqtt_f_dom_event(partition_context: PartitionContext, event: EventData, cloud_event:
CloudEvent, data: FDOM) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_f_dom_async =
usgs_instantaneous_values_mqtt_f_dom_event
```



make build

```##### `usgs_instantaneous_values_mqtt_reservoir_storage_async`



## Test```python

usgs_instantaneous_values_mqtt_reservoir_storage_async:  Callable[[PartitionContext, EventData, CloudEvent,
ReservoirStorage], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.ReservoirStorage`: USGS reservoir storage data.
Parameter code 00054.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.ReservoirStorage`.

Example:

```python
async def usgs_instantaneous_values_mqtt_reservoir_storage_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: ReservoirStorage) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_reservoir_storage_async =
usgs_instantaneous_values_mqtt_reservoir_storage_event
```



make build

```##### `usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_async`



## Test```python

usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_async:  Callable[[PartitionContext, EventData, CloudEvent,
LakeElevationNGVD29], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.LakeElevationNGVD29`: USGS lake or reservoir water
surface elevation above NGVD 1929, feet. Parameter code 62614.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.LakeElevationNGVD29`.

Example:

```python
async def usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_event(partition_context: PartitionContext, event:
EventData, cloud_event: CloudEvent, data: LakeElevationNGVD29) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_async =
usgs_instantaneous_values_mqtt_lake_elevation_ngvd29_event
```



make build

```##### `usgs_instantaneous_values_mqtt_water_depth_async`



## Test```python

usgs_instantaneous_values_mqtt_water_depth_async:  Callable[[PartitionContext, EventData, CloudEvent, WaterDepth],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.WaterDepth`: USGS water depth data. Parameter code
72199.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.WaterDepth`.

Example:

```python
async def usgs_instantaneous_values_mqtt_water_depth_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: WaterDepth) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_water_depth_async =
usgs_instantaneous_values_mqtt_water_depth_event
```



make build

```##### `usgs_instantaneous_values_mqtt_equipment_status_async`



## Test```python

usgs_instantaneous_values_mqtt_equipment_status_async:  Callable[[PartitionContext, EventData, CloudEvent,
EquipmentStatus], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.EquipmentStatus`: USGS equipment alarm status data.
Parameter code 99235.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.EquipmentStatus`.

Example:

```python
async def usgs_instantaneous_values_mqtt_equipment_status_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: EquipmentStatus) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_equipment_status_async =
usgs_instantaneous_values_mqtt_equipment_status_event
```



make build

```##### `usgs_instantaneous_values_mqtt_tidally_filtered_discharge_async`



## Test```python

usgs_instantaneous_values_mqtt_tidally_filtered_discharge_async:  Callable[[PartitionContext, EventData, CloudEvent,
TidallyFilteredDischarge], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge`: USGS tidally filtered
discharge data. Parameter code 72137.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.TidallyFilteredDischarge`.

Example:

```python
async def usgs_instantaneous_values_mqtt_tidally_filtered_discharge_event(partition_context: PartitionContext, event:
EventData, cloud_event: CloudEvent, data: TidallyFilteredDischarge) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_tidally_filtered_discharge_async =
usgs_instantaneous_values_mqtt_tidally_filtered_discharge_event
```



make build

```##### `usgs_instantaneous_values_mqtt_water_velocity_async`



## Test```python

usgs_instantaneous_values_mqtt_water_velocity_async:  Callable[[PartitionContext, EventData, CloudEvent, WaterVelocity],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.WaterVelocity`: USGS water velocity data. Parameter code
72254.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.WaterVelocity`.

Example:

```python
async def usgs_instantaneous_values_mqtt_water_velocity_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: WaterVelocity) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_water_velocity_async =
usgs_instantaneous_values_mqtt_water_velocity_event
```



make build

```##### `usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_async`



## Test```python

usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_async:  Callable[[PartitionContext, EventData, CloudEvent,
EstuaryElevationNGVD29], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29`: USGS estuary or ocean water
surface elevation above NGVD 1929, feet. Parameter code 62619.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.EstuaryElevationNGVD29`.

Example:

```python
async def usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_event(partition_context: PartitionContext, event:
EventData, cloud_event: CloudEvent, data: EstuaryElevationNGVD29) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_async =
usgs_instantaneous_values_mqtt_estuary_elevation_ngvd29_event
```



make build

```##### `usgs_instantaneous_values_mqtt_lake_elevation_navd88_async`



## Test```python

usgs_instantaneous_values_mqtt_lake_elevation_navd88_async:  Callable[[PartitionContext, EventData, CloudEvent,
LakeElevationNAVD88], Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.LakeElevationNAVD88`: USGS lake or reservoir water
surface elevation above NAVD 1988, feet. Parameter code 62615.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.LakeElevationNAVD88`.

Example:

```python
async def usgs_instantaneous_values_mqtt_lake_elevation_navd88_event(partition_context: PartitionContext, event:
EventData, cloud_event: CloudEvent, data: LakeElevationNAVD88) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_lake_elevation_navd88_async =
usgs_instantaneous_values_mqtt_lake_elevation_navd88_event
```



make build

```##### `usgs_instantaneous_values_mqtt_salinity_async`



## Test```python

usgs_instantaneous_values_mqtt_salinity_async:  Callable[[PartitionContext, EventData, CloudEvent, Salinity],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.Salinity`: USGS salinity data. Parameter code 00480.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.Salinity`.

Example:

```python
async def usgs_instantaneous_values_mqtt_salinity_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: Salinity) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_salinity_async =
usgs_instantaneous_values_mqtt_salinity_event
```



make build

```##### `usgs_instantaneous_values_mqtt_gate_opening_async`



## Test```python

usgs_instantaneous_values_mqtt_gate_opening_async:  Callable[[PartitionContext, EventData, CloudEvent, GateOpening],
Awaitable[None]]

```bash```

make test

```Asynchronous handler hook for `USGS.InstantaneousValues.mqtt.GateOpening`: USGS gate opening data. Parameter code
45592.


The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `partition_context`: The partition context.
- `event`: The event data.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs_iv_mqtt_producer_data.GateOpening`.

Example:

```python
async def usgs_instantaneous_values_mqtt_gate_opening_event(partition_context: PartitionContext, event: EventData,
cloud_event: CloudEvent, data: GateOpening) -> None:
    # Process the event data
    await partition_context.update_checkpoint(event)
```

The handler functions is then assigned to the event dispatcher for the message group. The event dispatcher is
responsible for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_mqtt_dispatcher.usgs_instantaneous_values_mqtt_gate_opening_async =
usgs_instantaneous_values_mqtt_gate_opening_event
```




## Internals

### Dispatchers

Dispatchers have the following protected methods:

### Methods:

##### `_process_event`

```python
_process_event(self, partition_context, event)
```

Processes an incoming event.

Args:
- `partition_context`: The partition context.
- `event`: The event data.

### EventProcessorRunner

`EventProcessorRunner` is responsible for managing the event processing loop and dispatching events to the appropriate
handlers.

#### Methods

##### `__init__`

```python
__init__(client: EventHubConsumerClient)
```

Initializes the runner with an Event Hub consumer client.

Args:
- `client`: The Event Hub consumer client.

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

Starts the event processor

#####  `cancel()`

Cancels the event processing task.

#####  `create_from_connection_strings`

```python
create_from_connection_strings(cls, consumer_group_name: str, connection_str: str, eventhub_name: str, blob_conn_str:
str, checkpoint_container: str) -> 'EventProcessorRunner'
```

Creates a runner from connection strings.

Args:
- `consumer_group_name`: The name of the consumer group.
- `connection_str`: The connection string for the Event Hub.
- `eventhub_name`: The name of the Event Hub.
- `blob_conn_str`: The connection string for the Azure Storage account.
- `checkpoint_container`: The name of the blob container to store checkpoints.

Returns:
- An `EventProcessorRunner` instance.

#####  `create`

```python
create(cls, consumer_group_name: str, eventhubs_fully_qualified_namespace: str, eventhub_name: str, blob_account_url:
str, blob_container_name: str, credential) -> 'EventProcessorRunner'
```

Creates a runner from fully qualified namespace and credentials.

Args:
- `consumer_group_name`: The name of the consumer group.
- `eventhubs_fully_qualified_namespace`: The fully qualified namespace of the Event Hub.
- `eventhub_name`: The name of the Event Hub.
- `blob_account_url`: The URL of the Azure Storage account.
- `blob_container_name`: The name of the blob container to store checkpoints.
- `credential`: The credential to use for authentication.

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
_unhandled_event(self, _cx, _e, _ce, de)
```

Default event handler.

#####  `_get_cloud_event_attribute`

```python
_get_cloud_event_attribute(event_data: EventData, key: str) -> Any
```

Retrieves a CloudEvent attribute from event data.

Args:
- `event_data`: The event data.
- `key`: The attribute key.



#####  `_is_cloud_event`

```python
_is_cloud_event(event_data: EventData) -> bool
```

Checks if the event data is a CloudEvent

Args:
- `event_data`: The event data.

#####  `_cloud_event_from_event_data`:

```python
_cloud_event_from_event_data(event_data: EventData) -> CloudEvent
```

Converts event data to a CloudEvent.

Args:
- `event_data`: The event data.

## Production-Ready Patterns

This section provides best-practice patterns for building production-grade Azure Event Hubs consumers in Python.

### 1. Connection Management with EventProcessorClient Pooling

Maintain long-lived EventProcessorClient instances with proper lifecycle management.

```python
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from azure.identity.aio import DefaultAzureCredential
from typing import Dict, Optional
import asyncio

class EventHubsConnectionPool:
    """
    Manages Event Hubs consumer connections with automatic retry and health checks.
    Uses async context managers for proper resource cleanup.
    """
    _lock: asyncio.Lock = asyncio.Lock()
    _clients: Dict[str, EventHubConsumerClient] = {}

    @classmethod
    async def get_client(
        cls,
        fully_qualified_namespace: str,
        eventhub_name: str,
        consumer_group: str,
        credential: Optional[DefaultAzureCredential] = None
    ) -> EventHubConsumerClient:
        """
        Get or create an Event Hubs consumer client.
        Reuses existing connections for the same Event Hub and consumer group.
        """
        key = f"{fully_qualified_namespace}/{eventhub_name}/{consumer_group}"

        async with cls._lock:
            if key not in cls._clients:
                if credential is None:
                    credential = DefaultAzureCredential()

                cls._clients[key] = EventHubConsumerClient(
                    fully_qualified_namespace=fully_qualified_namespace,
                    eventhub_name=eventhub_name,
                    consumer_group=consumer_group,
                    credential=credential,
                    # Production settings
                    retry_total=3,
                    retry_backoff_factor=0.8,
                    retry_backoff_max=60,
                )

        return cls._clients[key]

    @classmethod
    async def close_all(cls):
        """Close all Event Hubs clients gracefully."""
        async with cls._lock:
            await asyncio.gather(
                *[client.close() for client in cls._clients.values()],
                return_exceptions=True
            )
            cls._clients.clear()
```

### 2. Retry Logic with Azure SDK Built-in Policies

Leverage Azure SDK's built-in retry policies and extend with custom logic.

```python
from azure.core.exceptions import (
    ServiceRequestError, ServiceResponseError,
    HttpResponseError, AzureError
)
from tenacity import (
    retry, stop_after_attempt, wait_exponential,
    retry_if_exception_type, before_sleep_log
)
import logging

logger = logging.getLogger(__name__)

# Transient Azure errors that should trigger retries
RETRIABLE_AZURE_ERRORS = (
    ServiceRequestError,  # Network failures
    ServiceResponseError,  # Transient service errors
)

@retry(
    retry=retry_if_exception_type(RETRIABLE_AZURE_ERRORS),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def process_event_with_retry(partition_context, event, handler):
    """
    Process Event Hubs event with automatic retry on transient failures.
    Uses Polly-style exponential backoff.
    """
    try:
        await handler(partition_context, event)
        await partition_context.update_checkpoint(event)
    except HttpResponseError as e:
        # Check if error is retriable based on status code
        if e.status_code in {408, 429, 500, 502, 503, 504}:
            logger.warning(f"Retriable HTTP error {e.status_code}, will retry")
            raise
        else:
            # Non-retriable HTTP error, fail fast
            logger.error(f"Non-retriable HTTP error {e.status_code}")
            raise
    except Exception as e:
        logger.exception(f"Error processing event: {e}")
        raise
```

### 3. Circuit Breaker for Downstream Dependencies

Protect downstream services with circuit breaker pattern using `pybreaker`.

```python
import pybreaker
from azure.eventhub import PartitionContext, EventData
from typing import Callable

# Circuit breaker for downstream HTTP API
downstream_breaker = pybreaker.CircuitBreaker(
    fail_max=5,  # Trip after 5 failures
    timeout_duration=60,  # Stay open for 60 seconds
    exclude=[ValueError, KeyError],  # Don't count validation errors
    name='downstream_dependency'
)

class CircuitBreakerEventProcessor:
    """Event Hubs processor with circuit breaker for downstream calls."""

    def __init__(self):
        self.breaker = downstream_breaker
        self.fallback_enabled = True

    async def process_with_circuit_breaker(
        self,
        partition_context: PartitionContext,
        event: EventData,
        handler: Callable
    ):
        """
        Process event with circuit breaker protection.
        Falls back to logging when circuit is open.
        """
        try:
            await self.breaker.call_async(handler, partition_context, event)
            await partition_context.update_checkpoint(event)

        except pybreaker.CircuitBreakerError:
            logger.error(
                f"Circuit breaker OPEN for partition {partition_context.partition_id}, "
                f"event sequence {event.sequence_number}"
            )

            if self.fallback_enabled:
                # Fallback: checkpoint anyway to avoid reprocessing
                await partition_context.update_checkpoint(event)
                await self.log_to_fallback_storage(event)
            else:
                raise

        except Exception as e:
            logger.exception(f"Error processing event: {e}")
            raise

    async def log_to_fallback_storage(self, event: EventData):
        """Log event to fallback storage when downstream is unavailable."""
        # Implement fallback logic (e.g., write to blob storage)
        pass
```

### 4. Batch Processing with Checkpointing

Process events in batches for improved throughput while maintaining reliable checkpointing.

```python
import asyncio
from typing import List
from datetime import datetime, timedelta

class BatchEventProcessor:
    """
    Batches Event Hubs events for efficient bulk processing.
    Checkpoints after successful batch processing.
    """
    def __init__(self, batch_size: int = 100, batch_timeout_seconds: float = 5.0):
        self.batch_size = batch_size
        self.batch_timeout = timedelta(seconds=batch_timeout_seconds)
        self.batch: List[tuple[PartitionContext, EventData]] = []
        self.last_flush = datetime.now()
        self._lock = asyncio.Lock()

    async def add_event(
        self,
        partition_context: PartitionContext,
        event: EventData,
        handler: Callable
    ):
        """
        Add event to batch. Flushes when batch size or timeout threshold reached.
        """
        async with self._lock:
            self.batch.append((partition_context, event))

            should_flush = (
                len(self.batch) >= self.batch_size or
                datetime.now() - self.last_flush >= self.batch_timeout
            )

            if should_flush:
                await self.flush_batch(handler)

    async def flush_batch(self, handler: Callable):
        """Process and checkpoint current batch."""
        if not self.batch:
            return

        try:
            # Extract events for batch processing
            events = [event for _, event in self.batch]

            # Process batch (e.g., bulk database insert)
            await handler(events)

            # Checkpoint the last event in the batch
            last_partition_context, last_event = self.batch[-1]
            await last_partition_context.update_checkpoint(last_event)

            logger.info(
                f"Processed batch of {len(self.batch)} events, "
                f"last sequence: {last_event.sequence_number}"
            )

        except Exception as e:
            logger.exception(f"Batch processing failed: {e}")
            # Don't checkpoint on failure to allow retry
            raise
        finally:
            self.batch.clear()
            self.last_flush = datetime.now()

    async def close(self, handler: Callable):
        """Flush remaining events on shutdown."""
        async with self._lock:
            if self.batch:
                await self.flush_batch(handler)
```

### 5. Dead Letter Queue (DLQ) Pattern

Route unprocessable events to a separate Event Hub for later analysis.

```python
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData as ProducerEventData
from datetime import datetime

class DLQEventProcessor:
    """
    Event Hubs processor with DLQ support.
    Routes failed events to a dedicated DLQ Event Hub after retries.
    """
    def __init__(
        self,
        dlq_producer: EventHubProducerClient,
        max_retries: int = 3
    ):
        self.dlq_producer = dlq_producer
        self.max_retries = max_retries

    async def process_with_dlq(
        self,
        partition_context: PartitionContext,
        event: EventData,
        handler: Callable
    ):
        """Process event with automatic DLQ routing on failure."""
        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
            try:
                await handler(partition_context, event)
                await partition_context.update_checkpoint(event)
                return  # Success

            except Exception as e:
                retry_count += 1
                last_error = e
                logger.warning(
                    f"Retry {retry_count}/{self.max_retries} for event "
                    f"sequence {event.sequence_number}: {e}"
                )

                if retry_count < self.max_retries:
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff

        # Exhausted retries, send to DLQ
        await self.send_to_dlq(partition_context, event, last_error)

        # Checkpoint to avoid reprocessing
        await partition_context.update_checkpoint(event)

    async def send_to_dlq(
        self,
        partition_context: PartitionContext,
        event: EventData,
        error: Exception
    ):
        """Send event to DLQ Event Hub with rich metadata."""
        dlq_event = ProducerEventData(event.body_as_str())

        # Preserve original properties
        dlq_event.properties.update(event.properties)

        # Add DLQ metadata
        dlq_event.properties.update({
            'dlq_reason': 'processing_failed',
            'dlq_timestamp': datetime.utcnow().isoformat(),
            'original_partition': partition_context.partition_id,
            'original_sequence': event.sequence_number,
            'original_offset': event.offset,
            'original_enqueued_time': event.enqueued_time.isoformat() if event.enqueued_time else None,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'retry_count': self.max_retries
        })

        async with self.dlq_producer:
            await self.dlq_producer.send_batch([dlq_event])

        logger.error(
            f"Event sent to DLQ: partition={partition_context.partition_id}, "
            f"sequence={event.sequence_number}, error={error}"
        )
```

### 6. OpenTelemetry Observability with Application Insights

Instrument Event Hubs consumer with distributed tracing and metrics.

```python
from opentelemetry import trace, metrics
from opentelemetry.trace import Status, StatusCode
from opentelemetry.propagate import extract
from azure.monitor.opentelemetry import configure_azure_monitor
import time

# Configure Application Insights
configure_azure_monitor(connection_string="InstrumentationKey=...")

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Metrics
events_processed = meter.create_counter(
    "eventhubs.events.processed",
    description="Total events processed",
    unit="1"
)
processing_duration = meter.create_histogram(
    "eventhubs.event.processing.duration",
    description="Event processing duration",
    unit="ms"
)
consumer_lag = meter.create_observable_gauge(
    "eventhubs.consumer.lag",
    description="Consumer lag (seconds behind)",
    unit="s"
)

class ObservableEventProcessor:
    """Event Hubs processor with OpenTelemetry tracing and Application Insights."""

    async def process_with_tracing(
        self,
        partition_context: PartitionContext,
        event: EventData,
        handler: Callable
    ):
        """Process event with distributed tracing."""
        # Extract trace context from Event Hubs properties
        ctx = extract(event.properties)

        with tracer.start_as_current_span(
            "eventhubs.process",
            context=ctx,
            kind=trace.SpanKind.CONSUMER
        ) as span:
            span.set_attribute("messaging.system", "eventhubs")
            span.set_attribute("messaging.destination", partition_context.eventhub_name)
            span.set_attribute("messaging.eventhubs.partition_id", partition_context.partition_id)
            span.set_attribute("messaging.eventhubs.sequence_number", event.sequence_number)
            span.set_attribute("messaging.eventhubs.offset", event.offset)

            # Calculate lag
            if event.enqueued_time:
                lag_seconds = (datetime.now(event.enqueued_time.tzinfo) - event.enqueued_time).total_seconds()
                span.set_attribute("messaging.eventhubs.lag_seconds", lag_seconds)

            start_time = time.monotonic()
            try:
                await handler(partition_context, event)
                await partition_context.update_checkpoint(event)

                # Record success metrics
                duration_ms = (time.monotonic() - start_time) * 1000
                processing_duration.record(duration_ms, {
                    "partition_id": partition_context.partition_id,
                    "status": "success"
                })
                events_processed.add(1, {
                    "partition_id": partition_context.partition_id,
                    "status": "success"
                })

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                events_processed.add(1, {
                    "partition_id": partition_context.partition_id,
                    "status": "error"
                })
                raise
```

### 7. Backpressure Control

Prevent memory exhaustion with semaphore-based concurrency control.

```python
import asyncio

class BackpressureController:
    """
    Controls backpressure for Event Hubs processing.
    Limits concurrent event processing to prevent memory exhaustion.
    """
    def __init__(self, max_concurrent: int = 100):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.in_flight = 0
        self._lock = asyncio.Lock()

    async def process_with_backpressure(
        self,
        partition_context: PartitionContext,
        event: EventData,
        handler: Callable
    ):
        """
        Process event with backpressure control.
        Blocks when max concurrent limit reached.
        """
        async with self.semaphore:
            async with self._lock:
                self.in_flight += 1

            try:
                await handler(partition_context, event)
                await partition_context.update_checkpoint(event)
            finally:
                async with self._lock:
                    self.in_flight -= 1

    def get_metrics(self) -> dict:
        """Get current backpressure metrics."""
        return {
            "in_flight": self.in_flight,
            "available_slots": self.semaphore._value
        }
```

### 8. Graceful Shutdown

Ensure clean shutdown with proper checkpointing and resource cleanup.

```python
import signal
import asyncio
from azure.eventhub.aio import EventHubConsumerClient

class GracefulEventHubsConsumer:
    """Event Hubs consumer with graceful shutdown support."""

    def __init__(self, client: EventHubConsumerClient):
        self.client = client
        self.shutdown_event = asyncio.Event()
        self.processing_tasks = set()

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        self.shutdown_event.set()

    async def process_events(self, handler: Callable):
        """
        Process events with graceful shutdown.
        Waits for in-flight events before closing.
        """
        async def on_event(partition_context, event):
            """Wrapper to track processing tasks."""
            if self.shutdown_event.is_set():
                logger.info("Shutdown initiated, skipping new events")
                return

            task = asyncio.create_task(self._process_event(partition_context, event, handler))
            self.processing_tasks.add(task)
            task.add_done_callback(self.processing_tasks.discard)

        async def on_error(partition_context, error):
            """Error handler for Event Hubs client."""
            logger.error(f"Error in partition {partition_context.partition_id}: {error}")

        try:
            # Start receiving events
            async with self.client:
                await self.client.receive(
                    on_event=on_event,
                    on_error=on_error,
                    starting_position="-1"  # From beginning
                )

                # Wait for shutdown signal
                await self.shutdown_event.wait()

            # Wait for in-flight events
            logger.info(f"Waiting for {len(self.processing_tasks)} in-flight events")
            if self.processing_tasks:
                await asyncio.gather(*self.processing_tasks, return_exceptions=True)

            logger.info("All events processed, shutdown complete")

        finally:
            await self.client.close()

    async def _process_event(
        self,
        partition_context: PartitionContext,
        event: EventData,
        handler: Callable
    ):
        """Process individual event with error handling."""
        try:
            await handler(partition_context, event)
            await partition_context.update_checkpoint(event)
        except Exception as e:
            logger.exception(f"Error processing event: {e}")
```

### Configuration Best Practices

```python
from azure.eventhub.aio import EventHubConsumerClient
from azure.identity.aio import DefaultAzureCredential
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

# Production-grade Event Hubs consumer configuration
async def create_production_consumer():
    """Create Event Hubs consumer with production settings."""

    # Use managed identity in production
    credential = DefaultAzureCredential()

    # Checkpoint store for distributed processing
    checkpoint_store = BlobCheckpointStore(
        blob_account_url="https://<storage-account>.blob.core.windows.net",
        container_name="eventhubs-checkpoints",
        credential=credential
    )

    client = EventHubConsumerClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        eventhub_name="<eventhub-name>",
        consumer_group="$Default",
        checkpoint_store=checkpoint_store,
        credential=credential,

        # Retry configuration
        retry_total=3,
        retry_backoff_factor=0.8,
        retry_backoff_max=60,

        # Prefetch for throughput
        prefetch=300,

        # Load balancing interval
        load_balancing_interval=30.0
    )

    return client
```

### Integration Example

```python
import asyncio
from azure.eventhub.aio import EventHubConsumerClient, EventHubProducerClient
from azure.identity.aio import DefaultAzureCredential

async def main():
    """Complete integration example with all patterns."""
    credential = DefaultAzureCredential()

    # Create consumer
    consumer = await create_production_consumer()

    # Create DLQ producer
    dlq_producer = EventHubProducerClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        eventhub_name="<dlq-eventhub>",
        credential=credential
    )

    # Initialize components
    graceful_consumer = GracefulEventHubsConsumer(consumer)
    observable_processor = ObservableEventProcessor()
    dlq_processor = DLQEventProcessor(dlq_producer, max_retries=3)
    batch_processor = BatchEventProcessor(batch_size=100, batch_timeout_seconds=5.0)
    backpressure = BackpressureController(max_concurrent=100)

    async def process_event(partition_context, event):
        """Combined event processing with all patterns."""
        # Backpressure control
        await backpressure.process_with_backpressure(
            partition_context, event, business_logic
        )

        # Observability
        await observable_processor.process_with_tracing(
            partition_context, event, business_logic
        )

        # DLQ on failure
        await dlq_processor.process_with_dlq(
            partition_context, event, business_logic
        )

    async def business_logic(partition_context, event):
        """Your business logic here."""
        data = event.body_as_json()
        # Process data
        await process_business_logic(data)

    # Start processing with graceful shutdown
    await graceful_consumer.process_events(process_event)

if __name__ == '__main__':
    asyncio.run(main())
```
