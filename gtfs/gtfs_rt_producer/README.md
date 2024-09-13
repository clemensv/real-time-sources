
# Gtfs_rt_producer Apache Kafka Consumer SDK for Python

This is the Gtfs_rt_producer Apache Kafka Consumer SDK for Python. It was
generated from the xRegistry CLI tool based on message catalog definitions for
"GeneralTransitFeedRealTime", "GeneralTransitFeedStatic".

## Quick Install

To get started quickly, the main package can be installed with the `install.sh`
script (or `install.bat` on Windows) in the root of the repository.

### Contents

The repository contains two projects.
* The `gtfs_rt_producer_kafka_consumer` project is the main project that
contains the Kafka consumer client code.
* The `gtfs_rt_producer_data` project contains the data classes for the event
payload data.

The classes defined in `gtfs_rt_producer_kafka_consumer` are documented in the
project [README](./gtfs_rt_producer_kafka_consumer/README.md).

The `gtfs_rt_producer_kafka_consumer` project depends on the
`gtfs_rt_producer_data` project.

If you want to install the consumer project, you can run the following command:

```bash
pip install ./gtfs_rt_producer_kafka_consumer
```

This will install both packages. If you only want to install the data project,
you can run the following command:

```bash
pip install ./gtfs_rt_producer_data
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
pip install ./gtfs_rt_producer_kafka_producer
pytest ./gtfs_rt_producer_kafka_producer/tests ./gtfs_rt_producer_data/tests
```

## Usage

The sample code in [samples/sample.py](samples/sample.py) demonstrates how to
use the Kafka consumer client to receive messages from a Kafka topic.

In your code, you create handler functions for each message type that you want
to process. The handler functions are called when a message of that type is
received. Example:

```python
async def handle_general_transit_feed_real_time_vehicle_vehicle_position(record,
cloud_event,
general_transit_feed_real_time_vehicle_vehicle_position_event_data):
    """ Handles the GeneralTransitFeedRealTime.Vehicle.VehiclePosition event """
    print(f"GeneralTransitFeedRealTime.Vehicle.VehiclePosition:
{general_transit_feed_real_time_vehicle_vehicle_position_event_data.asdict()}")
    await some_processing_function(record, cloud_event,
general_transit_feed_real_time_vehicle_vehicle_position_event_data)
```

The handler functions are then assigned to the event dispatcher for the message
group. The event dispatcher is responsible for calling the appropriate handler
function when a message is received. Example:

```python
general_transit_feed_real_time_dispatcher =
GeneralTransitFeedRealTimeEventDispatcher()
general_transit_feed_real_time_dispatcher.general_transit_feed_real_time_vehicle
_vehicle_position_async =
general_transit_feed_real_time_vehicle_vehicle_position_event
```

You can create an event processor and add the event dispatcher to it. The event
processor is responsible for receiving messages from the Kafka topic and will
hand them to the dispatcher for processing.

The required parameters for the `create` method are:
* `bootstrap_servers`: The Kafka bootstrap servers.
* `group_id`: The consumer group ID.
* `topics`: The list of topics to subscribe to.

The example below shows how to create an event processor and then wait for a
signal to stop the processor:

```python
event_processor = EventStreamProcessor.create(
    bootstrap_servers,
    group_id,
    topics,
)
event_processor.add_dispatcher(general_transit_feed_real_time_dispatcher)
event_processor.add_dispatcher(general_transit_feed_static_dispatcher)
async with event_processor:
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, lambda: stop_event.set())
    loop.add_signal_handler(signal.SIGINT, lambda: stop_event.set())
    await stop_event.wait()
```