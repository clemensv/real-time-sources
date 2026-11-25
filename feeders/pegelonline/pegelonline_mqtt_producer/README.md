# Pegelonline_mqtt_producer MQTT Client

This library is a generated, strongly-typed MQTT client for the `pegelonline_mqtt_producer`
message definitions. For every message group it provides a single client class that
can both **consume** (dispatch received messages to async handlers) and **produce**
(publish messages) over [paho-mqtt](https://pypi.org/project/paho-mqtt/).

The client understands two wire shapes:

- **CloudEvents** messages (those declared with `envelope: CloudEvents/1.0`) are
  produced and consumed as CloudEvents (structured or binary content mode).
- **Plain** messages (no CloudEvents envelope) are produced and consumed as the raw
  serialized message data, for interoperating with brokers that carry plain JSON.

## Installation

```bash
./install.sh   # Unix/Linux/Mac
# or
install.bat    # Windows
```

This installs the generated client package and its dependencies
(`paho-mqtt >= 2.1.0`, `cloudevents`).

## Generated clients


- `DeWsvPegelonlineMqttMqttClient` — messages in the `de.wsv.pegelonline.mqtt` message group.


## Quick start

```python
import asyncio
import paho.mqtt.client as mqtt
from pegelonline_mqtt_producer_mqtt_client.client import DeWsvPegelonlineMqttMqttClient


async def main():
    # paho-mqtt 2.x requires a callback API version; the generated client uses
    # the VERSION1 callback signatures.
    paho_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="example")

    # 'structured' or 'binary' controls CloudEvents serialization on publish.
    client = DeWsvPegelonlineMqttMqttClient(paho_client, content_mode='structured')

    # Register an async handler for received 'de.wsv.pegelonline.mqtt.Station' messages.
    async def on_de_wsv_pegelonline_mqtt_station(mqtt_message, cloud_event, data, topic_params):
        print(f"{cloud_event['type']} {data} {topic_params}")
    client.de_wsv_pegelonline_mqtt_station_async = on_de_wsv_pegelonline_mqtt_station

    await client.connect("localhost", 1883)
    await client.subscribe()            # subscribe to all message topics

    # ... publish / receive messages ...

    await client.disconnect()


asyncio.run(main())
```

## Message handlers (consuming)

Register an `async` handler on the client for each message you want to receive.
The attribute name is the message id in `snake_case` with an `_async` suffix.
Handlers are dispatched by matching the incoming topic to the message's topic
template, so `topic_params` carries the extracted URI-template placeholder values.

- **CloudEvents** message handler signature:
  `(mqtt_message, cloud_event, data, topic_params)`
- **Plain** message handler signature:
  `(mqtt_message, data, topic_params)`

Where `mqtt_message` is the raw `paho.mqtt.client.MQTTMessage`, `cloud_event` is the
parsed CloudEvent envelope (CloudEvents messages only), `data` is the deserialized,
strongly-typed payload, and `topic_params` is a `Dict[str, str]`.

## Publishing (producing)

Each message has a `publish_<message>` coroutine. Topic URI-template placeholders are
passed as keyword arguments; `data` is the typed payload. `qos` and `retain` default
to the values declared in the message's `protocoloptions` and can be overridden.

- For **CloudEvents** messages the payload is wrapped in a CloudEvent envelope using
  the client's `content_mode` ('structured' or 'binary'), and the required CloudEvents
  attributes are passed as `_<attribute>` keyword arguments.
- For **plain** messages the raw serialized `data` is published with no envelope.

## API reference


### `DeWsvPegelonlineMqttMqttClient`

Client for the `de.wsv.pegelonline.mqtt` message group.

```python
DeWsvPegelonlineMqttMqttClient(
    client: paho.mqtt.client.Client,
    topic_mappings: Optional[Dict[str, str]] = None,
    content_mode: Literal['structured', 'binary'] = 'structured',
    loop: Optional[asyncio.AbstractEventLoop] = None,
)
```

**Connection methods**

- `await connect(broker, port=1883, keepalive=60, token=None, authentication_method="OAUTH2-JWT", properties=None)`
  — connect and wait for CONNACK. Pass `token` to authenticate with an OAuth2/Entra
  JWT via MQTT v5 Enhanced Authentication (requires a paho client created with
  `protocol=mqtt.MQTTv5`).
- `await disconnect()` — stop the network loop and disconnect.
- `await subscribe(topics=None, qos=0)` — subscribe to `topics`, or to all of this
  group's message topics (URI-template placeholders replaced with `+` wildcards) when
  `topics` is `None`.
- `await unsubscribe(topics)` — unsubscribe from the given topics.

**Message handlers** (assign an `async` callable, or `None` to unset)


- `de_wsv_pegelonline_mqtt_station_async` — handles `de.wsv.pegelonline.mqtt.Station`
  (CloudEvents). Signature:
  `(mqtt_message, cloud_event, data: Station, topic_params)`.

- `de_wsv_pegelonline_mqtt_current_measurement_async` — handles `de.wsv.pegelonline.mqtt.CurrentMeasurement`
  (CloudEvents). Signature:
  `(mqtt_message, cloud_event, data: CurrentMeasurement, topic_params)`.


**Publish methods**


- `await publish_de_wsv_pegelonline_mqtt_station(feedurl, station_id, water_shortname, data: Station, topic=None, qos=None, retain=None, _time=None, content_type='application/json')`
  — publish `de.wsv.pegelonline.mqtt.Station` as a CloudEvent.

- `await publish_de_wsv_pegelonline_mqtt_current_measurement(feedurl, station_id, water_shortname, data: CurrentMeasurement, topic=None, qos=None, retain=None, _time=None, content_type='application/json')`
  — publish `de.wsv.pegelonline.mqtt.CurrentMeasurement` as a CloudEvent.


**Module-level helpers**

- `get_default_topic_mappings_de_wsv_pegelonline_mqtt() -> Dict[str, str]` — the default
  message-id → topic-template mapping for this group.
- `get_subscription_topics_de_wsv_pegelonline_mqtt(topic_mappings=None) -> List[str]` — the
  subscription topics (URI-template placeholders converted to `+` wildcards).


## Topic mappings and URI templates

Each message has a default MQTT topic taken from its `protocoloptions.topic_name`
(falling back to `topic-name`/`topic`, then the message id). Topics may contain
`{placeholder}` URI-template variables. On **publish**, placeholders are filled from
the keyword arguments. On **subscribe**, placeholders are converted to MQTT `+`
single-level wildcards, and on **receive** the concrete values are extracted from the
topic and handed to your handler as `topic_params`.

To override the defaults, pass a `topic_mappings` dictionary (message id → topic
template) to the client constructor.