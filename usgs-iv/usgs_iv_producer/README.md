
# Usgs-iv-producer Event Dispatcher for Apache Kafka

This module provides an event dispatcher for processing events from Apache Kafka. It supports both plain Kafka messages
and CloudEvents.

## Table of Contents
1. [Overview](#overview)
2. [Generated Event Dispatchers](#generated-event-dispatchers)
    - USGSSitesEventDispatcher,
    USGSInstantaneousValuesEventDispatcher

3. [Internals](#internals)
    - [EventProcessorRunner](#eventprocessorrunner)
    - [_DispatcherBase](#_dispatcherbase)

## Overview

This module defines an event processing framework for Apache Kafka,
providing the necessary classes and methods to handle various types of events.
It includes both plain Kafka messages and CloudEvents, offering a versatile
solution for event-driven applications.

## Generated Event Dispatchers



### USGSSitesEventDispatcher

`USGSSitesEventDispatcher` handles events for the USGS.Sites message group.

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

The USGSSitesEventDispatcher defines the following event handler hooks.


##### `usgs_sites_site_async`

```python
usgs_sites_site_async:  Callable[[ConsumerRecord, CloudEvent, Site], Awaitable[None]]
```

Asynchronous handler hook for `USGS.Sites.Site`: USGS site metadata.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.sites.Site`.

Example:

```python
async def usgs_sites_site_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Site) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_sites_dispatcher.usgs_sites_site_async = usgs_sites_site_event
```


##### `usgs_sites_site_timeseries_async`

```python
usgs_sites_site_timeseries_async:  Callable[[ConsumerRecord, CloudEvent, SiteTimeseries], Awaitable[None]]
```

Asynchronous handler hook for `USGS.Sites.SiteTimeseries`: USGS site timeseries metadata.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.sites.SiteTimeseries`.

Example:

```python
async def usgs_sites_site_timeseries_event(record: ConsumerRecord, cloud_event: CloudEvent, data: SiteTimeseries) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_sites_dispatcher.usgs_sites_site_timeseries_async = usgs_sites_site_timeseries_event
```




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


##### `usgs_instantaneous_values_other_parameter_async`

```python
usgs_instantaneous_values_other_parameter_async:  Callable[[ConsumerRecord, CloudEvent, OtherParameter],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.OtherParameter`: USGS other parameter data.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.OtherParameter`.

Example:

```python
async def usgs_instantaneous_values_other_parameter_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
OtherParameter) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_other_parameter_async =
usgs_instantaneous_values_other_parameter_event
```


##### `usgs_instantaneous_values_precipitation_async`

```python
usgs_instantaneous_values_precipitation_async:  Callable[[ConsumerRecord, CloudEvent, Precipitation], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.Precipitation`: USGS precipitation data. Parameter code 00045.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.Precipitation`.

Example:

```python
async def usgs_instantaneous_values_precipitation_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
Precipitation) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_precipitation_async =
usgs_instantaneous_values_precipitation_event
```


##### `usgs_instantaneous_values_streamflow_async`

```python
usgs_instantaneous_values_streamflow_async:  Callable[[ConsumerRecord, CloudEvent, Streamflow], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.Streamflow`: USGS streamflow data. Parameter code 00060.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.Streamflow`.

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

Asynchronous handler hook for `USGS.InstantaneousValues.GageHeight`: USGS gage height data. Parameter code 00065.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.GageHeight`.

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

Asynchronous handler hook for `USGS.InstantaneousValues.WaterTemperature`: USGS water temperature data. Parameter code
00010.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.WaterTemperature`.

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

Asynchronous handler hook for `USGS.InstantaneousValues.DissolvedOxygen`: USGS dissolved oxygen data. Parameter code
00300.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.DissolvedOxygen`.

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

Asynchronous handler hook for `USGS.InstantaneousValues.pH`: USGS pH data. Parameter code 00400.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.PH`.

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

Asynchronous handler hook for `USGS.InstantaneousValues.SpecificConductance`: USGS specific conductance data. Parameter
code 00095.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.SpecificConductance`.

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

Asynchronous handler hook for `USGS.InstantaneousValues.Turbidity`: USGS turbidity data. Parameter code 00076.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.Turbidity`.

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


##### `usgs_instantaneous_values_air_temperature_async`

```python
usgs_instantaneous_values_air_temperature_async:  Callable[[ConsumerRecord, CloudEvent, AirTemperature],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.AirTemperature`: USGS air temperature data. Parameter code
00020.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.AirTemperature`.

Example:

```python
async def usgs_instantaneous_values_air_temperature_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
AirTemperature) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_air_temperature_async =
usgs_instantaneous_values_air_temperature_event
```


##### `usgs_instantaneous_values_wind_speed_async`

```python
usgs_instantaneous_values_wind_speed_async:  Callable[[ConsumerRecord, CloudEvent, WindSpeed], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.WindSpeed`: USGS wind speed data. Parameter code 00035.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.WindSpeed`.

Example:

```python
async def usgs_instantaneous_values_wind_speed_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WindSpeed)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_wind_speed_async =
usgs_instantaneous_values_wind_speed_event
```


##### `usgs_instantaneous_values_wind_direction_async`

```python
usgs_instantaneous_values_wind_direction_async:  Callable[[ConsumerRecord, CloudEvent, WindDirection], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.WindDirection`: USGS wind direction data. Parameter codes 00036
and 163695.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.WindDirection`.

Example:

```python
async def usgs_instantaneous_values_wind_direction_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WindDirection) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_wind_direction_async =
usgs_instantaneous_values_wind_direction_event
```


##### `usgs_instantaneous_values_relative_humidity_async`

```python
usgs_instantaneous_values_relative_humidity_async:  Callable[[ConsumerRecord, CloudEvent, RelativeHumidity],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.RelativeHumidity`: USGS relative humidity data. Parameter code
00052.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.RelativeHumidity`.

Example:

```python
async def usgs_instantaneous_values_relative_humidity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
RelativeHumidity) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_relative_humidity_async =
usgs_instantaneous_values_relative_humidity_event
```


##### `usgs_instantaneous_values_barometric_pressure_async`

```python
usgs_instantaneous_values_barometric_pressure_async:  Callable[[ConsumerRecord, CloudEvent, BarometricPressure],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.BarometricPressure`: USGS barometric pressure data. Parameter
codes 62605 and 75969.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.BarometricPressure`.

Example:

```python
async def usgs_instantaneous_values_barometric_pressure_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
BarometricPressure) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_barometric_pressure_async =
usgs_instantaneous_values_barometric_pressure_event
```


##### `usgs_instantaneous_values_turbidity_fnu_async`

```python
usgs_instantaneous_values_turbidity_fnu_async:  Callable[[ConsumerRecord, CloudEvent, TurbidityFNU], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.TurbidityFNU`: USGS turbidity data (FNU). Parameter code 63680.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.TurbidityFNU`.

Example:

```python
async def usgs_instantaneous_values_turbidity_fnu_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
TurbidityFNU) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_turbidity_fnu_async =
usgs_instantaneous_values_turbidity_fnu_event
```


##### `usgs_instantaneous_values_f_dom_async`

```python
usgs_instantaneous_values_f_dom_async:  Callable[[ConsumerRecord, CloudEvent, FDOM], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.fDOM`: USGS dissolved organic matter fluorescence data (fDOM).
Parameter codes 32295 and 32322.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.FDOM`.

Example:

```python
async def usgs_instantaneous_values_f_dom_event(record: ConsumerRecord, cloud_event: CloudEvent, data: FDOM) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_f_dom_async = usgs_instantaneous_values_f_dom_event
```


##### `usgs_instantaneous_values_reservoir_storage_async`

```python
usgs_instantaneous_values_reservoir_storage_async:  Callable[[ConsumerRecord, CloudEvent, ReservoirStorage],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.ReservoirStorage`: USGS reservoir storage data. Parameter code
00054.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.ReservoirStorage`.

Example:

```python
async def usgs_instantaneous_values_reservoir_storage_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
ReservoirStorage) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_reservoir_storage_async =
usgs_instantaneous_values_reservoir_storage_event
```


##### `usgs_instantaneous_values_lake_elevation_ngvd29_async`

```python
usgs_instantaneous_values_lake_elevation_ngvd29_async:  Callable[[ConsumerRecord, CloudEvent, LakeElevationNGVD29],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.LakeElevationNGVD29`: USGS lake or reservoir water surface
elevation above NGVD 1929, feet. Parameter code 62614.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.LakeElevationNGVD29`.

Example:

```python
async def usgs_instantaneous_values_lake_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNGVD29) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_lake_elevation_ngvd29_async =
usgs_instantaneous_values_lake_elevation_ngvd29_event
```


##### `usgs_instantaneous_values_water_depth_async`

```python
usgs_instantaneous_values_water_depth_async:  Callable[[ConsumerRecord, CloudEvent, WaterDepth], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.WaterDepth`: USGS water depth data. Parameter code 72199.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.WaterDepth`.

Example:

```python
async def usgs_instantaneous_values_water_depth_event(record: ConsumerRecord, cloud_event: CloudEvent, data: WaterDepth)
-> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_water_depth_async =
usgs_instantaneous_values_water_depth_event
```


##### `usgs_instantaneous_values_equipment_status_async`

```python
usgs_instantaneous_values_equipment_status_async:  Callable[[ConsumerRecord, CloudEvent, EquipmentStatus],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.EquipmentStatus`: USGS equipment alarm status data. Parameter
code 99235.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.EquipmentStatus`.

Example:

```python
async def usgs_instantaneous_values_equipment_status_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
EquipmentStatus) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_equipment_status_async =
usgs_instantaneous_values_equipment_status_event
```


##### `usgs_instantaneous_values_tidally_filtered_discharge_async`

```python
usgs_instantaneous_values_tidally_filtered_discharge_async:  Callable[[ConsumerRecord, CloudEvent,
TidallyFilteredDischarge], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.TidallyFilteredDischarge`: USGS tidally filtered discharge data.
Parameter code 72137.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.TidallyFilteredDischarge`.

Example:

```python
async def usgs_instantaneous_values_tidally_filtered_discharge_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: TidallyFilteredDischarge) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_tidally_filtered_discharge_async =
usgs_instantaneous_values_tidally_filtered_discharge_event
```


##### `usgs_instantaneous_values_water_velocity_async`

```python
usgs_instantaneous_values_water_velocity_async:  Callable[[ConsumerRecord, CloudEvent, WaterVelocity], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.WaterVelocity`: USGS water velocity data. Parameter code 72254.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.WaterVelocity`.

Example:

```python
async def usgs_instantaneous_values_water_velocity_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
WaterVelocity) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_water_velocity_async =
usgs_instantaneous_values_water_velocity_event
```


##### `usgs_instantaneous_values_estuary_elevation_ngvd29_async`

```python
usgs_instantaneous_values_estuary_elevation_ngvd29_async:  Callable[[ConsumerRecord, CloudEvent,
EstuaryElevationNGVD29], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.EstuaryElevationNGVD29`: USGS estuary or ocean water surface
elevation above NGVD 1929, feet. Parameter code 62619.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.EstuaryElevationNGVD29`.

Example:

```python
async def usgs_instantaneous_values_estuary_elevation_ngvd29_event(record: ConsumerRecord, cloud_event: CloudEvent,
data: EstuaryElevationNGVD29) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_estuary_elevation_ngvd29_async =
usgs_instantaneous_values_estuary_elevation_ngvd29_event
```


##### `usgs_instantaneous_values_lake_elevation_navd88_async`

```python
usgs_instantaneous_values_lake_elevation_navd88_async:  Callable[[ConsumerRecord, CloudEvent, LakeElevationNAVD88],
Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.LakeElevationNAVD88`: USGS lake or reservoir water surface
elevation above NAVD 1988, feet. Parameter code 62615.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.LakeElevationNAVD88`.

Example:

```python
async def usgs_instantaneous_values_lake_elevation_navd88_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
LakeElevationNAVD88) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_lake_elevation_navd88_async =
usgs_instantaneous_values_lake_elevation_navd88_event
```


##### `usgs_instantaneous_values_salinity_async`

```python
usgs_instantaneous_values_salinity_async:  Callable[[ConsumerRecord, CloudEvent, Salinity], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.Salinity`: USGS salinity data. Parameter code 00480.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.Salinity`.

Example:

```python
async def usgs_instantaneous_values_salinity_event(record: ConsumerRecord, cloud_event: CloudEvent, data: Salinity) ->
None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_salinity_async = usgs_instantaneous_values_salinity_event
```


##### `usgs_instantaneous_values_gate_opening_async`

```python
usgs_instantaneous_values_gate_opening_async:  Callable[[ConsumerRecord, CloudEvent, GateOpening], Awaitable[None]]
```

Asynchronous handler hook for `USGS.InstantaneousValues.GateOpening`: USGS gate opening data. Parameter code 45592.

The assigned handler must be a coroutine (`async def`) that accepts the following parameters:

- `record`: The Kafka record.
- `cloud_event`: The CloudEvent.
- `data`: The event data of type `usgs-iv-producer_data.usgs.instantaneousvalues.GateOpening`.

Example:

```python
async def usgs_instantaneous_values_gate_opening_event(record: ConsumerRecord, cloud_event: CloudEvent, data:
GateOpening) -> None:
    # Process the event data
    await some_processing_function(record, cloud_event, data)
```

The handler function is then assigned to the event dispatcher for the message group. The event dispatcher is responsible
for calling the appropriate handler function when a message is received. Example:

```python
usgs_instantaneous_values_dispatcher.usgs_instantaneous_values_gate_opening_async =
usgs_instantaneous_values_gate_opening_event
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