
# Ndw_road_traffic_amqp_producer - AMQP 1.0 Producer

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



### NLNDWAVGAmqpProducer

`NLNDWAVGAmqpProducer` sends messages for the NL.NDW.AVG.amqp message group.

#### Quick Start

```python
from ndw_road_traffic_amqp_producer import NLNDWAVGAmqpProducer

# Create producer
producer = NLNDWAVGAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=PointMeasurementSite(...),
    content_type="application/json"
)

producer.send_amqp(
    data=RouteMeasurementSite(...),
    content_type="application/json"
)

producer.send_amqp(
    data=TrafficObservation(...),
    content_type="application/json"
)

producer.send_amqp(
    data=TravelTimeObservation(...),
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
Reference record for a point measurement site from the Dutch NDW DATEX II measurement_current feed. Contains location,
sensor technology type, and lane configuration for a fixed inductive-loop or microwave sensor.

**Parameters:**
- `data` (PointMeasurementSite): The message data object
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[PointMeasurementSite]): Array of message data objects
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Reference record for a route (section) measurement site from the Dutch NDW DATEX II measurement_current feed. Covers a
road segment between two coordinates used for travel time computation.

**Parameters:**
- `data` (RouteMeasurementSite): The message data object
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[RouteMeasurementSite]): Array of message data objects
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Aggregated traffic speed and flow observation from the Dutch NDW DATEX II trafficspeed feed. Each record represents one
measurement site with speed averaged and flow summed across all reporting lanes.

**Parameters:**
- `data` (TrafficObservation): The message data object
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TrafficObservation]): Array of message data objects
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Travel time observation for a road segment from the Dutch NDW DATEX II traveltime feed. Contains the actual measured
travel time and the static free-flow reference time for a route measurement site.

**Parameters:**
- `data` (TravelTimeObservation): The message data object
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TravelTimeObservation]): Array of message data objects
- `_measurement_site_id` (str): Value for placeholder measurement_site_id in attribute subject
- `content_type` (str): Content type of the message data




### NLNDWDRIPAmqpProducer

`NLNDWDRIPAmqpProducer` sends messages for the NL.NDW.DRIP.amqp message group.

#### Quick Start

```python
from ndw_road_traffic_amqp_producer import NLNDWDRIPAmqpProducer

# Create producer
producer = NLNDWDRIPAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=DripSign(...),
    content_type="application/json"
)

producer.send_amqp(
    data=DripDisplayState(...),
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
Reference record for a Dynamic Route Information Panel (DRIP) sign from the Dutch NDW DATEX II
dynamische_route_informatie_paneel feed. Describes the physical installation, location, and type of an individual VMS
sign unit.

**Parameters:**
- `data` (DripSign): The message data object
- `_vms_controller_id` (str): Value for placeholder vms_controller_id in attribute subject
- `_vms_index` (str): Value for placeholder vms_index in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[DripSign]): Array of message data objects
- `_vms_controller_id` (str): Value for placeholder vms_controller_id in attribute subject
- `_vms_index` (str): Value for placeholder vms_index in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Current display state of a Dynamic Route Information Panel (DRIP) sign from the Dutch NDW DATEX II
dynamische_route_informatie_paneel feed. Captures the active text, pictogram codes, and operational state of the sign.

**Parameters:**
- `data` (DripDisplayState): The message data object
- `_vms_controller_id` (str): Value for placeholder vms_controller_id in attribute subject
- `_vms_index` (str): Value for placeholder vms_index in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[DripDisplayState]): Array of message data objects
- `_vms_controller_id` (str): Value for placeholder vms_controller_id in attribute subject
- `_vms_index` (str): Value for placeholder vms_index in attribute subject
- `content_type` (str): Content type of the message data




### NLNDWMSIAmqpProducer

`NLNDWMSIAmqpProducer` sends messages for the NL.NDW.MSI.amqp message group.

#### Quick Start

```python
from ndw_road_traffic_amqp_producer import NLNDWMSIAmqpProducer

# Create producer
producer = NLNDWMSIAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=MsiSign(...),
    content_type="application/json"
)

producer.send_amqp(
    data=MsiDisplayState(...),
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
Reference record for a Matrix Signal Installation (MSI) sign from the Dutch NDW DATEX II Matrixsignaalinformatie feed.
Describes the physical location, lane assignment, and type of a matrix signal sign above a motorway lane.

**Parameters:**
- `data` (MsiSign): The message data object
- `_sign_id` (str): Value for placeholder sign_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[MsiSign]): Array of message data objects
- `_sign_id` (str): Value for placeholder sign_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Current display state of a Matrix Signal Installation (MSI) sign from the Dutch NDW DATEX II Matrixsignaalinformatie
feed. Captures the displayed image code, operational state, and any speed limit shown.

**Parameters:**
- `data` (MsiDisplayState): The message data object
- `_sign_id` (str): Value for placeholder sign_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[MsiDisplayState]): Array of message data objects
- `_sign_id` (str): Value for placeholder sign_id in attribute subject
- `content_type` (str): Content type of the message data




### NLNDWSituationsAmqpProducer

`NLNDWSituationsAmqpProducer` sends messages for the NL.NDW.Situations.amqp message group.

#### Quick Start

```python
from ndw_road_traffic_amqp_producer import NLNDWSituationsAmqpProducer

# Create producer
producer = NLNDWSituationsAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_amqp(
    data=Roadwork(...),
    content_type="application/json"
)

producer.send_amqp(
    data=BridgeOpening(...),
    content_type="application/json"
)

producer.send_amqp(
    data=TemporaryClosure(...),
    content_type="application/json"
)

producer.send_amqp(
    data=TemporarySpeedLimit(...),
    content_type="application/json"
)

producer.send_amqp(
    data=SafetyRelatedMessage(...),
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
Road construction or maintenance work event from the Dutch NDW DATEX II planningsfeed_wegwerkzaamheden_en_evenementen
feed. Represents a planned or active roadwork situation on the Dutch national road network.

**Parameters:**
- `data` (Roadwork): The message data object
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[Roadwork]): Array of message data objects
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Bridge opening event from the Dutch NDW DATEX II planningsfeed_brugopeningen feed. Represents a scheduled or active
bridge opening that causes temporary road closure.

**Parameters:**
- `data` (BridgeOpening): The message data object
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[BridgeOpening]): Array of message data objects
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Temporary road closure from the Dutch NDW DATEX II tijdelijke_verkeersmaatregelen_afsluitingen feed. Represents a
temporary closure of a road section or lane on the Dutch national road network.

**Parameters:**
- `data` (TemporaryClosure): The message data object
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TemporaryClosure]): Array of message data objects
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Temporary speed limit measure from the Dutch NDW DATEX II tijdelijke_verkeersmaatregelen_maximum_snelheden feed.
Represents a temporary reduction in maximum speed on a section of the national road network.

**Parameters:**
- `data` (TemporarySpeedLimit): The message data object
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[TemporarySpeedLimit]): Array of message data objects
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_amqp()`
Safety-related traffic information message from the Dutch NDW DATEX II veiligheidsgerelateerde_berichten_srti feed.
Contains urgent safety alerts and hazard notifications on the national road network.

**Parameters:**
- `data` (SafetyRelatedMessage): The message data object
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_amqp_batch()`

Send multiple Amqp messages in sequence.

**Parameters:**
- `data_array` (List[SafetyRelatedMessage]): Array of message data objects
- `_situation_record_id` (str): Value for placeholder situation_record_id in attribute subject
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
    def __init__(self, producer: NLNDWAVGAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[PointMeasurementSite]):
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
producer = NLNDWAVGAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [PointMeasurementSite(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: NLNDWDRIPAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[DripSign]):
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
producer = NLNDWDRIPAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [DripSign(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: NLNDWMSIAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[MsiSign]):
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
producer = NLNDWMSIAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [MsiSign(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: NLNDWSituationsAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[Roadwork]):
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
producer = NLNDWSituationsAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [Roadwork(...) for _ in range(100)]
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
                    cls._instance.producer = NLNDWAVGAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> NLNDWAVGAmqpProducer:
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
                    cls._instance.producer = NLNDWDRIPAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> NLNDWDRIPAmqpProducer:
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
                    cls._instance.producer = NLNDWMSIAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> NLNDWMSIAmqpProducer:
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
                    cls._instance.producer = NLNDWSituationsAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> NLNDWSituationsAmqpProducer:
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
        self.producer: Optional[NLNDWAVGAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = NLNDWAVGAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: PointMeasurementSite, max_retries: int = 3):
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
        self.producer: Optional[NLNDWDRIPAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = NLNDWDRIPAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: DripSign, max_retries: int = 3):
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
        self.producer: Optional[NLNDWMSIAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = NLNDWMSIAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: MsiSign, max_retries: int = 3):
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
        self.producer: Optional[NLNDWSituationsAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = NLNDWSituationsAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: Roadwork, max_retries: int = 3):
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


producer = NLNDWAVGAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = NLNDWDRIPAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = NLNDWMSIAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_amqp(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = NLNDWSituationsAmqpProducer(host="localhost", address="my-queue")

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
    producer: NLNDWAVGAmqpProducer,
    data: PointMeasurementSite,
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
    producer: NLNDWDRIPAmqpProducer,
    data: DripSign,
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
    producer: NLNDWMSIAmqpProducer,
    data: MsiSign,
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
    producer: NLNDWSituationsAmqpProducer,
    data: Roadwork,
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

    def __init__(self, producer: NLNDWAVGAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: PointMeasurementSite):
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

    def __init__(self, producer: NLNDWDRIPAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: DripSign):
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

    def __init__(self, producer: NLNDWMSIAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: MsiSign):
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

    def __init__(self, producer: NLNDWSituationsAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: Roadwork):
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