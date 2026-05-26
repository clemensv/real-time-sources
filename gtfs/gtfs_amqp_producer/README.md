
# Gtfs_amqp_producer - AMQP 1.0 Producer

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



### GeneralTransitFeedRealTimeAmqpProducer

`GeneralTransitFeedRealTimeAmqpProducer` sends messages for the GeneralTransitFeedRealTime.amqp message group.

#### Quick Start

```python
from gtfs_amqp_producer import GeneralTransitFeedRealTimeAmqpProducer

# Create producer
producer = GeneralTransitFeedRealTimeAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=VehiclePosition(...),
    content_type="application/json"
)

producer.send_amqp(
    data=TripUpdate(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Alert(...),
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

**Parameters:**
- `data` (VehiclePosition): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[VehiclePosition]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (TripUpdate): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TripUpdate]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Alert): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Alert]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data




### GeneralTransitFeedStaticAmqpProducer

`GeneralTransitFeedStaticAmqpProducer` sends messages for the GeneralTransitFeedStatic.amqp message group.

#### Quick Start

```python
from gtfs_amqp_producer import GeneralTransitFeedStaticAmqpProducer

# Create producer
producer = GeneralTransitFeedStaticAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=Agency(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Areas(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Attributions(...),
    content_type="application/json"
)

producer.send_amqp(
    data=BookingRules(...),
    content_type="application/json"
)

producer.send_amqp(
    data=FareAttributes(...),
    content_type="application/json"
)

producer.send_amqp(
    data=FareLegRules(...),
    content_type="application/json"
)

producer.send_amqp(
    data=FareMedia(...),
    content_type="application/json"
)

producer.send_amqp(
    data=FareProducts(...),
    content_type="application/json"
)

producer.send_amqp(
    data=FareRules(...),
    content_type="application/json"
)

producer.send_amqp(
    data=FareTransferRules(...),
    content_type="application/json"
)

producer.send_amqp(
    data=FeedInfo(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Frequencies(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Levels(...),
    content_type="application/json"
)

producer.send_amqp(
    data=LocationGeoJson(...),
    content_type="application/json"
)

producer.send_amqp(
    data=LocationGroups(...),
    content_type="application/json"
)

producer.send_amqp(
    data=LocationGroupStores(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Networks(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Pathways(...),
    content_type="application/json"
)

producer.send_amqp(
    data=RouteNetworks(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Routes(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Shapes(...),
    content_type="application/json"
)

producer.send_amqp(
    data=StopAreas(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Stops(...),
    content_type="application/json"
)

producer.send_amqp(
    data=StopTimes(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Timeframes(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Transfers(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Translations(...),
    content_type="application/json"
)

producer.send_amqp(
    data=Trips(...),
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

**Parameters:**
- `data` (Agency): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Agency]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Areas): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Areas]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Attributions): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Attributions]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (BookingRules): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[BookingRules]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (FareAttributes): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[FareAttributes]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (FareLegRules): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[FareLegRules]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (FareMedia): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[FareMedia]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (FareProducts): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[FareProducts]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (FareRules): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[FareRules]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (FareTransferRules): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[FareTransferRules]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (FeedInfo): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[FeedInfo]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Frequencies): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Frequencies]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Levels): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Levels]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (LocationGeoJson): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[LocationGeoJson]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (LocationGroups): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[LocationGroups]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (LocationGroupStores): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[LocationGroupStores]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Networks): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Networks]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Pathways): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Pathways]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (RouteNetworks): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[RouteNetworks]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Routes): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Routes]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Shapes): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Shapes]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (StopAreas): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[StopAreas]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Stops): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Stops]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (StopTimes): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[StopTimes]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Timeframes): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Timeframes]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Transfers): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Transfers]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Translations): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Translations]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`

**Parameters:**
- `data` (Trips): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Trips]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_agencyid` (str): Value for placeholder agencyid in attribute subject
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
    def __init__(self, producer: GeneralTransitFeedRealTimeAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[VehiclePosition]):
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
producer = GeneralTransitFeedRealTimeAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [VehiclePosition(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: GeneralTransitFeedStaticAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[Agency]):
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
producer = GeneralTransitFeedStaticAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [Agency(...) for _ in range(100)]
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
                    cls._instance.producer = GeneralTransitFeedRealTimeAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> GeneralTransitFeedRealTimeAmqpProducer:
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
                    cls._instance.producer = GeneralTransitFeedStaticAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> GeneralTransitFeedStaticAmqpProducer:
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
        self.producer: Optional[GeneralTransitFeedRealTimeAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = GeneralTransitFeedRealTimeAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: VehiclePosition, max_retries: int = 3):
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
        self.producer: Optional[GeneralTransitFeedStaticAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = GeneralTransitFeedStaticAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: Agency, max_retries: int = 3):
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


producer = GeneralTransitFeedRealTimeAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = GeneralTransitFeedStaticAmqpProducer(host="localhost", address="my-queue")

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
    producer: GeneralTransitFeedRealTimeAmqpProducer,
    data: VehiclePosition,
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
    producer: GeneralTransitFeedStaticAmqpProducer,
    data: Agency,
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

    def __init__(self, producer: GeneralTransitFeedRealTimeAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: VehiclePosition):
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

    def __init__(self, producer: GeneralTransitFeedStaticAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: Agency):
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