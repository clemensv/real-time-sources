
# Mode_s_producer Apache Kafka Producer SDK for Python

This is the Mode_s_producer Apache Kafka Producer SDK for Python. It was
generated from the xRegistry CLI tool based on message catalog messages for
"Mode_S".

## Quick Install

To get started quickly, the main package can be installed with the `install.sh`
script (or `install.bat` on Windows) in the root of the repository.

### Contents

The repository contains two projects.
* The `mode_s_producer_kafka_producer` project is the main project that contains
the Kafka producer client code.
* The `mode_s_producer_data` project contains the data classes for the event
payload data.

The classes defined in `mode_s_producer_kafka_producer` are documented in the
project [README](./mode_s_producer_kafka_producer/README.md).

The `mode_s_producer_kafka_producer` project depends on the
`mode_s_producer_data` project.

If you want to install the producer project, you can run the following command:

```bash
pip install ./mode_s_producer_kafka_producer
```

This will install both packages. If you only want to install the data project,
you can run the following command:

```bash
pip install ./mode_s_producer_data
```

## Build and Test

The SDK comes with a full test suite for the data classes and the dispatchers
that uses the `pytest` framework and Docker containers to run the tests.

If you have Docker installed and if you have `make`, you can run the tests with
the following command:

```bash
make test
```

If you don't have `make` installed, you can run the following commands:

```bash
pip install ./mode_s_producer_kafka_producer
pytest ./mode_s_producer_kafka_producer/tests ./mode_s_producer_data/tests
```

## Usage

The sample code in [samples/sample.py](samples/sample.py) demonstrates how to
use the Kafka producer client to receive messages from a Kafka topic.

In your code, you create handler functions for each message type that you want
to process. The handler functions are called when a message of that type is
received. Example:

```python
async def handle_mode_s_messages(record, cloud_event,
mode_s_messages_event_data):
    """ Handles the Mode_S.Messages event """
    print(f"Mode_S.Messages: {mode_s_messages_event_data.asdict()}")
    await some_processing_function(record, cloud_event,
mode_s_messages_event_data)
```

The handler functions are then assigned to the event dispatcher for the message
group. The event dispatcher is responsible for calling the appropriate handler
function when a message is received. Example:

```python
mode_s_dispatcher = ModeSEventDispatcher()
mode_s_dispatcher.mode_s_messages_async = mode_s_messages_event
```

You can then create an event processor directly from the event dispatcher. The
event processor is responsible for receiving messages from the Kafka topic and
will hand them to the dispatcher for processing.

The required parameters for the `create_processor` method are:
* `bootstrap_servers`: The Kafka bootstrap servers.
* `group_id`: The producer group ID.
* `topics`: The list of topics to subscribe to.

The example below shows how to create an event processor and then wait for a
signal to stop the processor:

```python
async with dispatcher.create_processor(
            bootstrap_servers,
            group_id,
            topics,
        ) as processor_runner:
            stop_event = asyncio.Event()
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGTERM, lambda: stop_event.set())
            loop.add_signal_handler(signal.SIGINT, lambda: stop_event.set())
            await stop_event.wait()
```