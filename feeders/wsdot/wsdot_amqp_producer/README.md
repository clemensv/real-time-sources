
# Wsdot_amqp_producer - AMQP 1.0 Producer

Auto-generated Python producer for sending messages via AMQP 1.0 protocol.

## Overview

This module provides a type-safe AMQP 1.0 producer for sending events with optional CloudEvents envelope format. Built
on the `python-qpid-proton` library for Python.

## What is AMQP 1.0?

**AMQP (Advanced Message Queuing Protocol) 1.0** is an open standard for business messaging that supports:
- **Protocol-level interoperability** between different platforms and vendors
- **Reliable message delivery** with settlement modes and flow control
- **Multiple messaging patterns** including queues, topics, and request-reply
- **Built-in security** with SASL authentication and TLS encryption

Use cases: Enterprise integration, IoT messaging, financial services, cloud-native applications.

**Supported AMQP 1.0 Brokers:**
- Apache ActiveMQ Artemis (native AMQP 1.0)
- Apache Qpid (native AMQP 1.0)
- Azure Service Bus (native AMQP 1.0)
- RabbitMQ (with AMQP 1.0 plugin - [setup guide](https://github.com/clemensv/xregistry-
cli/blob/main/docs/rabbitmq_amqp_setup.md))

**Note for RabbitMQ users:** RabbitMQ requires the AMQP 1.0 plugin to be enabled. See the [RabbitMQ AMQP 1.0 Setup
Guide](https://github.com/clemensv/xregistry-cli/blob/main/docs/rabbitmq_amqp_setup.md) for detailed instructions.


## Azure Entra ID (CBS) Authentication — enabled

This producer was generated with `--template-args azure_cbs_target=servicebus`,
which wires in AMQP CBS (Claims-Based Security) put-token flow for **Azure Event Hubs** and
**Azure Service Bus** using `azure-identity` token credentials.

```python
from azure.identity import DefaultAzureCredential
producer = <Group>Producer(
    host="my-namespace.servicebus.windows.net",   # EH or SB FQDN
    address="my-hub-or-queue",                    # entity path
    credential=DefaultAzureCredential(),
)
producer.send_my_event(...)
producer.close()
```

CBS audience: `https://servicebus.azure.net/.default`
(override with `--template-args azure_cbs_audience=<scope>` at code-gen time)

Required RBAC role on the entity or namespace, e.g.:
- Event Hubs: **Azure Event Hubs Data Sender**
- Service Bus: **Azure Service Bus Data Sender**

Debug logging:

```python
import logging
logging.getLogger("amqp.cbs").setLevel(logging.DEBUG)
```

**Known limitations of the v1 CBS implementation:**
- Token is acquired once at `__init__` time; there is no background refresh. Recreate the
  producer (or open a fresh one) before token expiry (~60 min for Entra ID).
- On Windows, the official `python-qpid-proton` PyPI wheel (verified on 0.40.0,
  the latest release at the time of writing) is linked against SChannel via the
  legacy `SCHANNEL_CRED` API and **cannot negotiate TLS 1.3**. Azure Service
  Bus namespaces with `minimumTlsVersion=1.3` will return
  `amqp:unauthorized-access "Invalid TLS version"` at AMQP open. Tracked
  upstream as [PROTON-2933](https://issues.apache.org/jira/browse/PROTON-2933).

  Until the upstream wheel is fixed, install the OpenSSL-backed Windows
  wheel published from `xregistry/codegen`:

  ```
  pip install --extra-index-url https://xregistry.github.io/codegen/wheels/simple/ python-qpid-proton
  ```

  pip will pick the `0.40.0+xrcgN` build automatically on Windows; Linux and
  macOS continue to install the stock `0.40.0` from PyPI.
- A reactor-based handler is used on the CBS path; the non-CBS path keeps the
  `BlockingConnection` implementation unchanged.


## Installation

```bash
pip install python-qpid-proton cloudevents azure-identity azure-core
```

### Windows: TLS 1.3 — extra index URL required

The official `python-qpid-proton` Windows wheel does not support TLS 1.3
(it links against SChannel via a deprecated API). If your AMQP broker
requires TLS 1.3 — most notably Azure Service Bus namespaces with
`minimumTlsVersion=1.3` — install with our OpenSSL-backed patched wheel:

```bash
pip install --extra-index-url https://xregistry.github.io/codegen/wheels/simple/ python-qpid-proton cloudevents azure-
identity azure-core
```

pip selects the patched wheel only on Windows (it has a strictly higher
PEP 440 local version `0.40.0+xrcgN`); Linux and macOS continue to install
the stock release from PyPI. The patched wheel will be retired as soon as
upstream proton ships a Windows wheel with TLS 1.3 support.

## Generated Producers



### UsWaWsdotTrafficAmqpProducer

`UsWaWsdotTrafficAmqpProducer` sends messages for the us.wa.wsdot.traffic.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotTrafficAmqpProducer

# Create producer
producer = UsWaWsdotTrafficAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=TrafficFlowStation(...),
    content_type="application/json"
)

producer.send_amqp(
    data=TrafficFlowReading(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Metadata for a traffic flow sensor station in the Washington State DOT network. WSDOT deploys approximately 1,400
inductive loop sensors embedded in highway pavement across four geographic regions.

**Parameters:**
- `data` (TrafficFlowStation): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_flow_data_id` (str): Value for placeholder flow_data_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TrafficFlowStation]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_flow_data_id` (str): Value for placeholder flow_data_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
A traffic flow reading from a WSDOT sensor station. Updated approximately every 90 seconds, each reading reports the
current Level of Service.

**Parameters:**
- `data` (TrafficFlowReading): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_flow_data_id` (str): Value for placeholder flow_data_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TrafficFlowReading]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_flow_data_id` (str): Value for placeholder flow_data_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotTraveltimesAmqpProducer

`UsWaWsdotTraveltimesAmqpProducer` sends messages for the us.wa.wsdot.traveltimes.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotTraveltimesAmqpProducer

# Create producer
producer = UsWaWsdotTraveltimesAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=TravelTimeRoute(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
A named travel time route monitored by WSDOT. Each route has fixed start and end points on Washington State highways
with historical average and current real-time travel times.

**Parameters:**
- `data` (TravelTimeRoute): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_travel_time_id` (str): Value for placeholder travel_time_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TravelTimeRoute]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_travel_time_id` (str): Value for placeholder travel_time_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotMountainpassAmqpProducer

`UsWaWsdotMountainpassAmqpProducer` sends messages for the us.wa.wsdot.mountainpass.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotMountainpassAmqpProducer

# Create producer
producer = UsWaWsdotMountainpassAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=MountainPassCondition(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Current conditions at a Washington State mountain pass including temperature, weather, road conditions, travel
advisories, and directional restrictions.

**Parameters:**
- `data` (MountainPassCondition): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_mountain_pass_id` (str): Value for placeholder mountain_pass_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[MountainPassCondition]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_mountain_pass_id` (str): Value for placeholder mountain_pass_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotWeatherAmqpProducer

`UsWaWsdotWeatherAmqpProducer` sends messages for the us.wa.wsdot.weather.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotWeatherAmqpProducer

# Create producer
producer = UsWaWsdotWeatherAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=WeatherStation(...),
    content_type="application/json"
)

producer.send_amqp(
    data=WeatherReading(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Metadata for a WSDOT road weather information system (RWIS) station. WSDOT operates approximately 134 stations across
Washington State highways.

**Parameters:**
- `data` (WeatherStation): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[WeatherStation]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
A current weather reading from a WSDOT road weather station including temperature, wind, precipitation, pressure,
humidity, visibility, and sky coverage.

**Parameters:**
- `data` (WeatherReading): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[WeatherReading]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotTollsAmqpProducer

`UsWaWsdotTollsAmqpProducer` sends messages for the us.wa.wsdot.tolls.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotTollsAmqpProducer

# Create producer
producer = UsWaWsdotTollsAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=TollRate(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Current toll rate for a WSDOT tolled route segment. WSDOT operates dynamic tolling on SR 99, I-405, and SR 167.

**Parameters:**
- `data` (TollRate): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_trip_name` (str): Value for placeholder trip_name in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TollRate]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_trip_name` (str): Value for placeholder trip_name in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotCvrestrictionsAmqpProducer

`UsWaWsdotCvrestrictionsAmqpProducer` sends messages for the us.wa.wsdot.cvrestrictions.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotCvrestrictionsAmqpProducer

# Create producer
producer = UsWaWsdotCvrestrictionsAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=CommercialVehicleRestriction(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
A commercial vehicle restriction on a Washington State highway bridge or road segment. Restrictions limit vehicle
weight, height, length, or width.

**Parameters:**
- `data` (CommercialVehicleRestriction): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_state_route_id` (str): Value for placeholder state_route_id in attribute subject
- `_bridge_number` (str): Value for placeholder bridge_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[CommercialVehicleRestriction]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_state_route_id` (str): Value for placeholder state_route_id in attribute subject
- `_bridge_number` (str): Value for placeholder bridge_number in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotBorderAmqpProducer

`UsWaWsdotBorderAmqpProducer` sends messages for the us.wa.wsdot.border.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotBorderAmqpProducer

# Create producer
producer = UsWaWsdotBorderAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=BorderCrossing(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Current wait time at a US-Canada border crossing lane in Washington State. Wait times are in minutes, updated
approximately every 5 minutes.

**Parameters:**
- `data` (BorderCrossing): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_crossing_name` (str): Value for placeholder crossing_name in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[BorderCrossing]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_crossing_name` (str): Value for placeholder crossing_name in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotFerriesAmqpProducer

`UsWaWsdotFerriesAmqpProducer` sends messages for the us.wa.wsdot.ferries.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotFerriesAmqpProducer

# Create producer
producer = UsWaWsdotFerriesAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=VesselLocation(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Real-time location and status of a Washington State Ferries vessel. WSF operates approximately 21 vessels across Puget
Sound routes.

**Parameters:**
- `data` (VesselLocation): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_vessel_id` (str): Value for placeholder vessel_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[VesselLocation]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_vessel_id` (str): Value for placeholder vessel_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotRoadweatherAmqpProducer

`UsWaWsdotRoadweatherAmqpProducer` sends messages for the us.wa.wsdot.roadweather.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotRoadweatherAmqpProducer

# Create producer
producer = UsWaWsdotRoadweatherAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=RoadWeatherStation(...),
    content_type="application/json"
)

producer.send_amqp(
    data=RoadWeatherReading(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Metadata for a WSDOT Scanweb road weather information system (RWIS) station, including position and elevation. WSDOT
operates roughly 105 Scanweb stations reporting pavement and atmospheric conditions across Washington State highways.

**Parameters:**
- `data` (RoadWeatherStation): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[RoadWeatherStation]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
A current Scanweb road weather reading including air temperature, humidity, wind, visibility, precipitation totals, and
per-sensor road surface and sub-surface measurements.

**Parameters:**
- `data` (RoadWeatherReading): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[RoadWeatherReading]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_station_id` (str): Value for placeholder station_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotAlertsAmqpProducer

`UsWaWsdotAlertsAmqpProducer` sends messages for the us.wa.wsdot.alerts.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotAlertsAmqpProducer

# Create producer
producer = UsWaWsdotAlertsAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=HighwayAlert(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
An active WSDOT highway alert describing an incident, construction, closure, special event, or weather impact, with
start and end roadway locations on the Washington State highway network.

**Parameters:**
- `data` (HighwayAlert): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_alert_id` (str): Value for placeholder alert_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[HighwayAlert]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_alert_id` (str): Value for placeholder alert_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotCamerasAmqpProducer

`UsWaWsdotCamerasAmqpProducer` sends messages for the us.wa.wsdot.cameras.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotCamerasAmqpProducer

# Create producer
producer = UsWaWsdotCamerasAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=HighwayCamera(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Reference catalog entry for a WSDOT highway traffic camera, including its location and a claim-check image URL. The
image bytes are not transported; consumers fetch the most recent frame from ImageURL on demand.

**Parameters:**
- `data` (HighwayCamera): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_camera_id` (str): Value for placeholder camera_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[HighwayCamera]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_camera_id` (str): Value for placeholder camera_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotBridgeclearancesAmqpProducer

`UsWaWsdotBridgeclearancesAmqpProducer` sends messages for the us.wa.wsdot.bridgeclearances.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotBridgeclearancesAmqpProducer

# Create producer
producer = UsWaWsdotBridgeclearancesAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=BridgeClearance(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Reference catalog record of the surveyed vertical clearance of a structure crossing a Washington State highway, used for
commercial vehicle routing. Largely static; refreshed periodically.

**Parameters:**
- `data` (BridgeClearance): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_crossing_location_id` (str): Value for placeholder crossing_location_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[BridgeClearance]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_crossing_location_id` (str): Value for placeholder crossing_location_id in attribute subject
- `content_type` (str): Content type of the message data




### UsWaWsdotFerryterminalsAmqpProducer

`UsWaWsdotFerryterminalsAmqpProducer` sends messages for the us.wa.wsdot.ferryterminals.amqp message group.

#### Quick Start

```python
from wsdot_amqp_producer import UsWaWsdotFerryterminalsAmqpProducer

# Create producer
producer = UsWaWsdotFerryterminalsAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=TerminalSailingSpace(...),
    content_type="application/json"
)


# Close producer
producer.close()
```

#### Configuration Options

The producer constructor accepts:

- `host` (str): AMQP broker hostname
- `address` (str): AMQP address (queue or topic name)
- `port` (int): AMQP broker port (default: 5672, for TLS typically 5671)
- `username` (Optional[str]): Username for SASL authentication
- `password` (Optional[str]): Password for SASL authentication
- `content_mode` (Literal['structured', 'binary']): CloudEvents encoding mode (default: 'structured')
  - **structured**: Entire CloudEvent as JSON in message body
  - **binary**: Event data in body, CloudEvents attributes in AMQP application properties
- `format_type` (str): Content type for structured mode (default: 'application/json')

#### Available Methods



##### `send_amqp()`
Real-time drive-up and reservable vehicle space availability for upcoming Washington State Ferries departures from a
terminal, broken down by sailing and arrival terminal.

**Parameters:**
- `data` (TerminalSailingSpace): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_terminal_id` (str): Value for placeholder terminal_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TerminalSailingSpace]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_terminal_id` (str): Value for placeholder terminal_id in attribute subject
- `content_type` (str): Content type of the message data




## AMQP Broker Compatibility

This library has been tested with:
- **Azure Service Bus** (AMQP 1.0 over TLS on port 5671)
- **Apache ActiveMQ Artemis** (AMQP 1.0 on port 5672)
- **Apache Qpid Broker-J** (AMQP 1.0 on port 5672)

## Security Considerations

- Always use TLS/SSL encryption in production (port 5671)
- Store credentials securely (environment variables, key vaults)
- Use SASL authentication mechanisms appropriate for your broker
- Consider using token-based authentication (OAuth, JWT) where supported

## Advanced Usage

### Batch Sending with Concurrency Control

Send multiple messages efficiently with rate limiting:

```python
import asyncio
from typing import List


class BatchProducer:
    def __init__(self, producer: UsWaWsdotTrafficAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[TrafficFlowStation]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotTrafficAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [TrafficFlowStation(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotTraveltimesAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[TravelTimeRoute]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotTraveltimesAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [TravelTimeRoute(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotMountainpassAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[MountainPassCondition]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotMountainpassAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [MountainPassCondition(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotWeatherAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[WeatherStation]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotWeatherAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [WeatherStation(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotTollsAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[TollRate]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotTollsAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [TollRate(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotCvrestrictionsAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[CommercialVehicleRestriction]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotCvrestrictionsAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [CommercialVehicleRestriction(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotBorderAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[BorderCrossing]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotBorderAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [BorderCrossing(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotFerriesAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[VesselLocation]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotFerriesAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [VesselLocation(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotRoadweatherAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[RoadWeatherStation]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotRoadweatherAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [RoadWeatherStation(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotAlertsAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[HighwayAlert]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotAlertsAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [HighwayAlert(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotCamerasAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[HighwayCamera]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotCamerasAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [HighwayCamera(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotBridgeclearancesAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[BridgeClearance]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotBridgeclearancesAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [BridgeClearance(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: UsWaWsdotFerryterminalsAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[TerminalSailingSpace]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_amqp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = UsWaWsdotFerryterminalsAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [TerminalSailingSpace(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


### Connection Pooling

Reuse producer connections across your application:

```python
from threading import Lock


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotTrafficAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotTrafficAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotTraveltimesAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotTraveltimesAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotMountainpassAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotMountainpassAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotWeatherAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotWeatherAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotTollsAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotTollsAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotCvrestrictionsAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotCvrestrictionsAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotBorderAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotBorderAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotFerriesAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotFerriesAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotRoadweatherAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotRoadweatherAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotAlertsAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotAlertsAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotCamerasAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotCamerasAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotBridgeclearancesAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotBridgeclearancesAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()


class ProducerPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.producer = UsWaWsdotFerryterminalsAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> UsWaWsdotFerryterminalsAmqpProducer:
        return self.producer

    def close(self):
        if self.producer:
            self.producer.close()

# Use from anywhere
pool = ProducerPool()
producer = pool.get_producer()

```

### Connection Resilience

Automatically reconnect on connection failures:

```python
import time
from typing import Optional


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotTrafficAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotTrafficAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: TrafficFlowStation, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotTraveltimesAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotTraveltimesAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: TravelTimeRoute, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotMountainpassAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotMountainpassAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: MountainPassCondition, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotWeatherAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotWeatherAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: WeatherStation, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotTollsAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotTollsAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: TollRate, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotCvrestrictionsAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotCvrestrictionsAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: CommercialVehicleRestriction, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotBorderAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotBorderAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: BorderCrossing, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotFerriesAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotFerriesAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: VesselLocation, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotRoadweatherAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotRoadweatherAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: RoadWeatherStation, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotAlertsAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotAlertsAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: HighwayAlert, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotCamerasAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotCamerasAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: HighwayCamera, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotBridgeclearancesAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotBridgeclearancesAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: BridgeClearance, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()


class ResilientProducer:
    def __init__(self, host: str, address: str, **kwargs):
        self.host = host
        self.address = address
        self.kwargs = kwargs
        self.producer: Optional[UsWaWsdotFerryterminalsAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = UsWaWsdotFerryterminalsAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: TerminalSailingSpace, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_amqp(data)
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    self._connect()  # Reconnect
                else:
                    raise Exception(f"Failed after {max_retries} attempts") from e

    def close(self):
        if self.producer:
            self.producer.close()

```

### Custom CloudEvents Attributes

Add extension attributes to CloudEvents:

```python


producer = UsWaWsdotTrafficAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotTraveltimesAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotMountainpassAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotWeatherAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotTollsAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotCvrestrictionsAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotBorderAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotFerriesAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotRoadweatherAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotAlertsAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotCamerasAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotBridgeclearancesAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = UsWaWsdotFerryterminalsAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)

```

## Error Handling

### Basic Error Handling

```python
from uamqp import errors

try:
    producer.send_message(data)
except errors.AMQPConnectionError as e:
    print(f"Connection error: {e}")
except errors.MessageException as e:
    print(f"Message error: {e}")
finally:
    producer.close()
```

### Retry with Exponential Backoff

```python
import time
from typing import Any


def send_with_retry(
    producer: UsWaWsdotTrafficAmqpProducer,
    data: TrafficFlowStation,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotTraveltimesAmqpProducer,
    data: TravelTimeRoute,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotMountainpassAmqpProducer,
    data: MountainPassCondition,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotWeatherAmqpProducer,
    data: WeatherStation,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotTollsAmqpProducer,
    data: TollRate,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotCvrestrictionsAmqpProducer,
    data: CommercialVehicleRestriction,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotBorderAmqpProducer,
    data: BorderCrossing,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotFerriesAmqpProducer,
    data: VesselLocation,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotRoadweatherAmqpProducer,
    data: RoadWeatherStation,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotAlertsAmqpProducer,
    data: HighwayAlert,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotCamerasAmqpProducer,
    data: HighwayCamera,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotBridgeclearancesAmqpProducer,
    data: BridgeClearance,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: UsWaWsdotFerryterminalsAmqpProducer,
    data: TerminalSailingSpace,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
) -> None:
    """
    Send message with exponential backoff retry.

    Args:
        producer: The producer instance
        data: Message data to send
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            producer.send_amqp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e

```

### Circuit Breaker Pattern

```python
from datetime import datetime, timedelta


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotTrafficAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: TrafficFlowStation):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotTraveltimesAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: TravelTimeRoute):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotMountainpassAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: MountainPassCondition):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotWeatherAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: WeatherStation):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotTollsAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: TollRate):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotCvrestrictionsAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: CommercialVehicleRestriction):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotBorderAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: BorderCrossing):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotFerriesAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: VesselLocation):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotRoadweatherAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: RoadWeatherStation):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotAlertsAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: HighwayAlert):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotCamerasAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: HighwayCamera):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotBridgeclearancesAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: BridgeClearance):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: UsWaWsdotFerryterminalsAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: TerminalSailingSpace):
        """Send message with circuit breaker protection."""
        # Check if circuit breaker is open
        if self.is_open:
            if datetime.now() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is open. Too many consecutive failures.")
            else:
                # Try to close the circuit
                self.is_open = False
                self.failure_count = 0

        try:
            self.producer.send_amqp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise

```

## Building and Testing

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Build package
poetry build
```

## Dependencies

- `uamqp>=1.6.10` - AMQP 1.0 client library
- `cloudevents>=1.10.1` - CloudEvents SDK
- Python 3.10+

## License

This generated code is provided as-is for use in your projects.