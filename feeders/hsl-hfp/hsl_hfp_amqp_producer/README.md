
# Hsl_hfp_amqp_producer - AMQP 1.0 Producer

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
- RabbitMQ (with AMQP 1.0 plugin - [setup
guide](https://github.com/xregistry/codegen/blob/main/docs/rabbitmq_amqp_setup.md))

**Note for RabbitMQ users:** RabbitMQ requires the AMQP 1.0 plugin to be enabled. See the [RabbitMQ AMQP 1.0 Setup
Guide](https://github.com/xregistry/codegen/blob/main/docs/rabbitmq_amqp_setup.md) for detailed instructions.


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



### FiHslHfpAmqpProducer

`FiHslHfpAmqpProducer` sends messages for the fi.hsl.hfp.amqp message group.

#### Quick Start

```python
from hsl_hfp_amqp_producer import FiHslHfpAmqpProducer

# Create producer
producer = FiHslHfpAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_vp(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_due(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_arr(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_dep(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_ars(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_pde(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_pas(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_wait(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_doo(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_doc(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_vja(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_vjout(
    data=VehicleEvent(...),
    content_type="application/json"
)

producer.send_tlr(
    data=TrafficLightEvent(...),
    content_type="application/json"
)

producer.send_tla(
    data=TrafficLightEvent(...),
    content_type="application/json"
)

producer.send_da(
    data=DriverBlockEvent(...),
    content_type="application/json"
)

producer.send_dout(
    data=DriverBlockEvent(...),
    content_type="application/json"
)

producer.send_ba(
    data=DriverBlockEvent(...),
    content_type="application/json"
)

producer.send_bout(
    data=DriverBlockEvent(...),
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



##### `send_vp()`
Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an ongoing public journey.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_vp_batch()`

Send multiple Vp messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_due()`
The vehicle will soon arrive at a stop.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_due_batch()`

Send multiple Due messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_arr()`
The vehicle has arrived inside a stop's radius.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_arr_batch()`

Send multiple Arr messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_dep()`
The vehicle has departed and left a stop's radius.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_dep_batch()`

Send multiple Dep messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_ars()`
The vehicle has arrived at a stop (stop-position event).

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_ars_batch()`

Send multiple Ars messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_pde()`
The vehicle is ready to depart from a stop.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_pde_batch()`

Send multiple Pde messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_pas()`
The vehicle passes through a stop without stopping.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_pas_batch()`

Send multiple Pas messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_wait()`
The vehicle is waiting at a stop.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_wait_batch()`

Send multiple Wait messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_doo()`
The doors of the vehicle have been opened.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_doo_batch()`

Send multiple Doo messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_doc()`
The doors of the vehicle have been closed.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_doc_batch()`

Send multiple Doc messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_vja()`
The vehicle signs in to a service journey (trip).

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_vja_batch()`

Send multiple Vja messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_vjout()`
The vehicle signs off from a service journey after the final stop.

**Parameters:**
- `data` (VehicleEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_vjout_batch()`

Send multiple Vjout messages in sequence.

**Parameters:**
- `data_array` (List[VehicleEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_tlr()`
The vehicle requests traffic-light priority at a junction.

**Parameters:**
- `data` (TrafficLightEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_tlr_batch()`

Send multiple Tlr messages in sequence.

**Parameters:**
- `data_array` (List[TrafficLightEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_tla()`
The vehicle receives a response to a traffic-light priority request.

**Parameters:**
- `data` (TrafficLightEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_tla_batch()`

Send multiple Tla messages in sequence.

**Parameters:**
- `data_array` (List[TrafficLightEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_da()`
A driver signs in to the vehicle.

**Parameters:**
- `data` (DriverBlockEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_da_batch()`

Send multiple Da messages in sequence.

**Parameters:**
- `data_array` (List[DriverBlockEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_dout()`
A driver signs out of the vehicle.

**Parameters:**
- `data` (DriverBlockEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_dout_batch()`

Send multiple Dout messages in sequence.

**Parameters:**
- `data_array` (List[DriverBlockEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_ba()`
A driver selects the block the vehicle will run.

**Parameters:**
- `data` (DriverBlockEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_ba_batch()`

Send multiple Ba messages in sequence.

**Parameters:**
- `data_array` (List[DriverBlockEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data



##### `send_bout()`
A driver signs out from the selected block (usually at a depot).

**Parameters:**
- `data` (DriverBlockEvent): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_bout_batch()`

Send multiple Bout messages in sequence.

**Parameters:**
- `data_array` (List[DriverBlockEvent]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `_vehicle_number` (str): Value for placeholder vehicle_number in attribute subject
- `content_type` (str): Content type of the message data




### FiHslGtfsOperatorAmqpProducer

`FiHslGtfsOperatorAmqpProducer` sends messages for the fi.hsl.gtfs.operator.amqp message group.

#### Quick Start

```python
from hsl_hfp_amqp_producer import FiHslGtfsOperatorAmqpProducer

# Create producer
producer = FiHslGtfsOperatorAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_operator(
    data=Operator(...),
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



##### `send_operator()`
Reference record describing one HSL transit operator.

**Parameters:**
- `data` (Operator): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_operator_batch()`

Send multiple Operator messages in sequence.

**Parameters:**
- `data_array` (List[Operator]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_operator_id` (str): Value for placeholder operator_id in attribute subject
- `content_type` (str): Content type of the message data




### FiHslGtfsRouteAmqpProducer

`FiHslGtfsRouteAmqpProducer` sends messages for the fi.hsl.gtfs.route.amqp message group.

#### Quick Start

```python
from hsl_hfp_amqp_producer import FiHslGtfsRouteAmqpProducer

# Create producer
producer = FiHslGtfsRouteAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_route(
    data=Route(...),
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



##### `send_route()`
Reference record describing one HSL route.

**Parameters:**
- `data` (Route): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_route_id` (str): Value for placeholder route_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_route_batch()`

Send multiple Route messages in sequence.

**Parameters:**
- `data_array` (List[Route]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_route_id` (str): Value for placeholder route_id in attribute subject
- `content_type` (str): Content type of the message data




### FiHslGtfsStopAmqpProducer

`FiHslGtfsStopAmqpProducer` sends messages for the fi.hsl.gtfs.stop.amqp message group.

#### Quick Start

```python
from hsl_hfp_amqp_producer import FiHslGtfsStopAmqpProducer

# Create producer
producer = FiHslGtfsStopAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_stop(
    data=Stop(...),
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



##### `send_stop()`
Reference record describing one HSL stop or station.

**Parameters:**
- `data` (Stop): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_stop_id` (str): Value for placeholder stop_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_stop_batch()`

Send multiple Stop messages in sequence.

**Parameters:**
- `data_array` (List[Stop]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_stop_id` (str): Value for placeholder stop_id in attribute subject
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
    def __init__(self, producer: FiHslHfpAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[VehicleEvent]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_vp,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = FiHslHfpAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [VehicleEvent(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: FiHslGtfsOperatorAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[Operator]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_operator,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = FiHslGtfsOperatorAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [Operator(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: FiHslGtfsRouteAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[Route]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_route,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = FiHslGtfsRouteAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [Route(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: FiHslGtfsStopAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[Stop]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_stop,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = FiHslGtfsStopAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [Stop(...) for _ in range(100)]
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
                    cls._instance.producer = FiHslHfpAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> FiHslHfpAmqpProducer:
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
                    cls._instance.producer = FiHslGtfsOperatorAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> FiHslGtfsOperatorAmqpProducer:
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
                    cls._instance.producer = FiHslGtfsRouteAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> FiHslGtfsRouteAmqpProducer:
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
                    cls._instance.producer = FiHslGtfsStopAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> FiHslGtfsStopAmqpProducer:
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
        self.producer: Optional[FiHslHfpAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = FiHslHfpAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: VehicleEvent, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_vp(data)
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
        self.producer: Optional[FiHslGtfsOperatorAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = FiHslGtfsOperatorAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: Operator, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_operator(data)
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
        self.producer: Optional[FiHslGtfsRouteAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = FiHslGtfsRouteAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: Route, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_route(data)
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
        self.producer: Optional[FiHslGtfsStopAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = FiHslGtfsStopAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: Stop, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_stop(data)
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


producer = FiHslHfpAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_vp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = FiHslGtfsOperatorAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_operator(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = FiHslGtfsRouteAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_route(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = FiHslGtfsStopAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_stop(
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
    producer: FiHslHfpAmqpProducer,
    data: VehicleEvent,
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
            producer.send_vp(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: FiHslGtfsOperatorAmqpProducer,
    data: Operator,
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
            producer.send_operator(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: FiHslGtfsRouteAmqpProducer,
    data: Route,
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
            producer.send_route(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: FiHslGtfsStopAmqpProducer,
    data: Stop,
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
            producer.send_stop(data)
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

    def __init__(self, producer: FiHslHfpAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: VehicleEvent):
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
            self.producer.send_vp(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: FiHslGtfsOperatorAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: Operator):
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
            self.producer.send_operator(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: FiHslGtfsRouteAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: Route):
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
            self.producer.send_route(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: FiHslGtfsStopAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: Stop):
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
            self.producer.send_stop(data)
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