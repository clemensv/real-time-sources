
# Open_charge_map_amqp_producer - AMQP 1.0 Producer

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



### IOOpenChargeMapLocationsAmqpProducer

`IOOpenChargeMapLocationsAmqpProducer` sends messages for the IO.OpenChargeMap.locations.amqp message group.

#### Quick Start

```python
from open_charge_map_amqp_producer import IOOpenChargeMapLocationsAmqpProducer

# Create producer
producer = IOOpenChargeMapLocationsAmqpProducer(
    host="localhost",
    address="my-queue",
    port=5672,
    username="guest",
    password="guest"
)

# Send a message

producer.send_charging_location(
    data=ChargingLocation(...),
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



##### `send_charging_location()`
Near-real-time charging-location record for one Open Charge Map point of interest, keyed by the stable OCM POI id.
Emitted at startup for the configured scope and thereafter whenever the record's `DateLastStatusUpdate` advances.

**Parameters:**
- `data` (ChargingLocation): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_poi_id` (str): Value for placeholder poi_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_charging_location_batch()`

Send multiple ChargingLocation messages in sequence.

**Parameters:**
- `data_array` (List[ChargingLocation]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_poi_id` (str): Value for placeholder poi_id in attribute subject
- `content_type` (str): Content type of the message data




### IOOpenChargeMapReferenceAmqpProducer

`IOOpenChargeMapReferenceAmqpProducer` sends messages for the IO.OpenChargeMap.reference.amqp message group.

#### Quick Start

```python
from open_charge_map_amqp_producer import IOOpenChargeMapReferenceAmqpProducer

# Create producer
producer = IOOpenChargeMapReferenceAmqpProducer(
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

producer.send_connection_type(
    data=ConnectionType(...),
    content_type="application/json"
)

producer.send_current_type(
    data=CurrentType(...),
    content_type="application/json"
)

producer.send_charger_type(
    data=ChargerType(...),
    content_type="application/json"
)

producer.send_country(
    data=Country(...),
    content_type="application/json"
)

producer.send_data_provider(
    data=DataProvider(...),
    content_type="application/json"
)

producer.send_status_type(
    data=StatusType(...),
    content_type="application/json"
)

producer.send_usage_type(
    data=UsageType(...),
    content_type="application/json"
)

producer.send_submission_status_type(
    data=SubmissionStatusType(...),
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
Open Charge Map Operator reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all
lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (Operator): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_operator_batch()`

Send multiple Operator messages in sequence.

**Parameters:**
- `data_array` (List[Operator]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_connection_type()`
Open Charge Map ConnectionType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all
lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (ConnectionType): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_connection_type_batch()`

Send multiple ConnectionType messages in sequence.

**Parameters:**
- `data_array` (List[ConnectionType]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_current_type()`
Open Charge Map CurrentType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all
lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (CurrentType): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_current_type_batch()`

Send multiple CurrentType messages in sequence.

**Parameters:**
- `data_array` (List[CurrentType]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_charger_type()`
Open Charge Map ChargerType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all
lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (ChargerType): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_charger_type_batch()`

Send multiple ChargerType messages in sequence.

**Parameters:**
- `data_array` (List[ChargerType]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_country()`
Open Charge Map Country reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all lookup
entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference refresh.

**Parameters:**
- `data` (Country): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_country_batch()`

Send multiple Country messages in sequence.

**Parameters:**
- `data_array` (List[Country]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_data_provider()`
Open Charge Map DataProvider reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all
lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (DataProvider): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_data_provider_batch()`

Send multiple DataProvider messages in sequence.

**Parameters:**
- `data_array` (List[DataProvider]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_status_type()`
Open Charge Map StatusType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all
lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (StatusType): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_status_type_batch()`

Send multiple StatusType messages in sequence.

**Parameters:**
- `data_array` (List[StatusType]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_usage_type()`
Open Charge Map UsageType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}` so all
lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (UsageType): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_usage_type_batch()`

Send multiple UsageType messages in sequence.

**Parameters:**
- `data_array` (List[UsageType]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data



##### `send_submission_status_type()`
Open Charge Map SubmissionStatusType reference catalog entity, keyed by the composite `{reference_type}/{reference_id}`
so all lookup entities share one identity shape on the reference topic. Emitted at startup and on the periodic reference
refresh.

**Parameters:**
- `data` (SubmissionStatusType): The message data object
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
- `content_type` (str): Content type of the message data (default: 'application/json')

##### `send_submission_status_type_batch()`

Send multiple SubmissionStatusType messages in sequence.

**Parameters:**
- `data_array` (List[SubmissionStatusType]): Array of message data objects
- `_feedurl` (str): Value for placeholder feedurl in attribute source
- `_reference_type` (str): Value for placeholder reference_type in attribute subject
- `_reference_id` (str): Value for placeholder reference_id in attribute subject
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
    def __init__(self, producer: IOOpenChargeMapLocationsAmqpProducer, max_concurrency: int = 10):
        self.producer = producer
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def send_batch_async(self, data_array: List[ChargingLocation]):
        """Send multiple messages with concurrency control."""
        async def send_one(data):
            async with self.semaphore:
                await asyncio.to_thread(
                    self.producer.send_charging_location,
                    data
                )

        tasks = [send_one(data) for data in data_array]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
producer = IOOpenChargeMapLocationsAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [ChargingLocation(...) for _ in range(100)]
asyncio.run(batch_producer.send_batch_async(data_list))
```


class BatchProducer:
    def __init__(self, producer: IOOpenChargeMapReferenceAmqpProducer, max_concurrency: int = 10):
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
producer = IOOpenChargeMapReferenceAmqpProducer(host="localhost", address="my-queue")
batch_producer = BatchProducer(producer, max_concurrency=20)

data_list = [Operator(...) for _ in range(100)]
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
                    cls._instance.producer = IOOpenChargeMapLocationsAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> IOOpenChargeMapLocationsAmqpProducer:
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
                    cls._instance.producer = IOOpenChargeMapReferenceAmqpProducer(
                        host="localhost",
                        address="my-queue",
                        username="guest",
                        password="guest"
                    )
        return cls._instance

    def get_producer(self) -> IOOpenChargeMapReferenceAmqpProducer:
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
        self.producer: Optional[IOOpenChargeMapLocationsAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = IOOpenChargeMapLocationsAmqpProducer(
            host=self.host,
            address=self.address,
            **self.kwargs
        )

    def send_with_retry(self, data: ChargingLocation, max_retries: int = 3):
        """Send message with automatic retry on connection failure."""
        for attempt in range(max_retries):
            try:
                self.producer.send_charging_location(data)
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
        self.producer: Optional[IOOpenChargeMapReferenceAmqpProducer] = None
        self._connect()

    def _connect(self):
        """Establish connection to AMQP broker."""
        if self.producer:
            try:
                self.producer.close()
            except:
                pass

        self.producer = IOOpenChargeMapReferenceAmqpProducer(
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

```

### Custom CloudEvents Attributes

Add extension attributes to CloudEvents:

```python


producer = IOOpenChargeMapLocationsAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_charging_location(
    data=data,
    _tenant="contoso",           # Custom extension attribute
    _deviceid="device-001",      # Custom extension attribute
    _region="us-west-2",         # Custom extension attribute
    _priority="high",            # Custom extension attribute
    content_type="application/json"
)


producer = IOOpenChargeMapReferenceAmqpProducer(host="localhost", address="my-queue")

# CloudEvents extension attributes can be added via metadata
producer.send_operator(
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
    producer: IOOpenChargeMapLocationsAmqpProducer,
    data: ChargingLocation,
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
            producer.send_charging_location(data)
            return  # Success
        except errors.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                delay = min(initial_delay * (2 ** attempt), max_delay)
                print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise Exception(f"Failed after {max_retries} attempts") from e


def send_with_retry(
    producer: IOOpenChargeMapReferenceAmqpProducer,
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

```

### Circuit Breaker Pattern

```python
from datetime import datetime, timedelta


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: IOOpenChargeMapLocationsAmqpProducer, threshold: int = 5, timeout: int = 60):
        self.producer = producer
        self.threshold = threshold
        self.timeout = timedelta(seconds=timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def send(self, data: ChargingLocation):
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
            self.producer.send_charging_location(data)
            self.failure_count = 0  # Reset on success
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.threshold:
                self.is_open = True
            raise


class CircuitBreakerProducer:
    """Producer with circuit breaker to prevent cascading failures."""

    def __init__(self, producer: IOOpenChargeMapReferenceAmqpProducer, threshold: int = 5, timeout: int = 60):
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