<!-- xreg-generator:hand-maintained — hand-polished beyond tools/printdoc.py output (CloudEvents envelope tables). tools/generate-events-md.ps1 skips this file. To refresh from the manifest: remove this line, regenerate, then re-apply the hand sections. -->
# ERDDAP Events

CloudEvents emitted by the generalized ERDDAP tabledap feeder.

## At a glance

- **Event types:** 3 documented event types (12 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 2 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{erddap_id}/{dataset_id}`, `{erddap_id}/{dataset_id}/{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `erddap`. The record key is `{erddap_id}/{dataset_id}`, `{erddap_id}/{dataset_id}/{station_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['erddap'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `marine/global/erddap/+/+/dataset`, `marine/global/erddap/+/+/+/station`, `marine/global/erddap/+/+/+/observation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('marine/global/erddap/+/+/dataset', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `erddap`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/erddap')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Dataset Metadata

CloudEvents type: `org.erddap.DatasetMetadata`

#### What it tells you

Reference data describing one configured ERDDAP tabledap dataset, emitted at startup and on metadata refresh so consumers can interpret station and observation events without making out-of-band ERDDAP info requests.

#### Identity

Each event identifies the real-world resource with `{erddap_id}/{dataset_id}`. `{erddap_id}` is stable, operator-assigned identifier for the configured ERDDAP server instance; `{dataset_id}` is ERDDAP datasetID from the tabledap catalog and request path. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `erddap`, key `{erddap_id}/{dataset_id}` |
| `MQTT/5.0` | topic `marine/global/erddap/{erddap_id}/{dataset_id}/dataset`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/erddap`, message subject `{erddap_id}/{dataset_id}` |

#### Payload

`Dataset Metadata` payloads are JSON object. Required fields: `erddap_id`, `dataset_id`, `base_url`, `info_url`, `time_variable`, `global_attributes`, `variables`.

- **`erddap_id`** (string, required): Stable, operator-assigned identifier for the configured ERDDAP server instance. ERDDAP dataset identifiers are only unique within one server, so consumers use this value with dataset_id and station_id as the global identity. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`dataset_id`** (string, required): ERDDAP datasetID from the tabledap catalog and request path. It is stable within the ERDDAP server and is used with erddap_id and station_id in CloudEvents subjects, Kafka keys, MQTT topics, and AMQP subjects. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`base_url`** (uri, required): Base URL of the ERDDAP server ending at /erddap. It is the documented root for allDatasets, info, and tabledap requests and is included so consumers can trace every event back to the source server.
- **`title`** (string or null, optional): Dataset title from allDatasets and the NC_GLOBAL title attribute, for example '(41024 / SUN2) Sunset Nearshore Met and Water, NC'. Nullable only when a server omits titles.
- **`cdm_data_type`** (string or null, optional): ERDDAP cdm_data_type catalog value. This feeder keeps TimeSeries and TimeSeriesProfile tabledap datasets and documents griddap as out of scope.
- **`min_time`** (string or null, optional): Earliest time advertised by allDatasets for this tabledap dataset, in UTC, when the server exposes it. Used by consumers to understand historical coverage. Encoded as an RFC 3339 UTC string in the payload for generated Avro/Python round-trip stability; the CloudEvents envelope time remains a native event timestamp.
- **`max_time`** (string or null, optional): Latest time advertised by allDatasets for this tabledap dataset, in UTC, when the server exposes it. Used by operators to detect stale datasets. Encoded as an RFC 3339 UTC string in the payload for generated Avro/Python round-trip stability; the CloudEvents envelope time remains a native event timestamp.
- **`info_url`** (uri, required): ERDDAP info endpoint URL used to build this metadata event.
- **`time_variable`** (string, required): Name of the ERDDAP time column selected for polling. The generalized feeder currently uses the standard tabledap time variable.
- **`station_id_variable`** (string or null, optional): Variable whose metadata declares cf_role=timeseries_id. Null for single-station fallback datasets where station_id is consistently set to dataset_id.
- **`global_attributes`** (map, required): NC_GLOBAL attributes from the ERDDAP info table, stringified as name-to-value pairs. They include provider, licence, conventions, summary, contributor, and update metadata when published.
- **`variables`** (array of object, required): Variables advertised by the ERDDAP info table, including units and CF/IOOS metadata used to normalize observations.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "erddap_id": "string",
  "dataset_id": "string",
  "base_url": "string",
  "title": "string",
  "cdm_data_type": "string",
  "min_time": "string",
  "max_time": "string",
  "info_url": "string",
  "time_variable": "string",
  "station_id_variable": "string",
  "global_attributes": null,
  "variables": [
    {
      "name": "string",
      "data_type": "string",
      "unit": "string",
      "long_name": "string",
      "standard_name": "string",
      "ioos_category": "string",
      "cf_role": "string"
    }
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Station Metadata

CloudEvents type: `org.erddap.StationMetadata`

#### What it tells you

Reference data describing one station or platform identity within a configured ERDDAP tabledap TimeSeries dataset. It is derived from the dataset's cf_role=timeseries_id variable and representative coordinate columns, and is emitted before observations.

#### Identity

Each event identifies the real-world resource with `{erddap_id}/{dataset_id}/{station_id}`. `{erddap_id}` is stable, operator-assigned identifier for the configured ERDDAP server instance; `{dataset_id}` is ERDDAP datasetID from the tabledap catalog and request path; `{station_id}` is stable station or platform identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `erddap`, key `{erddap_id}/{dataset_id}/{station_id}` |
| `MQTT/5.0` | topic `marine/global/erddap/{erddap_id}/{dataset_id}/{station_id}/station`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/erddap`, message subject `{erddap_id}/{dataset_id}/{station_id}` |

#### Payload

`Station Metadata` payloads are JSON object. Required fields: `erddap_id`, `dataset_id`, `base_url`, `station_id`, `attributes`.

- **`erddap_id`** (string, required): Stable, operator-assigned identifier for the configured ERDDAP server instance. ERDDAP dataset identifiers are only unique within one server, so consumers use this value with dataset_id and station_id as the global identity. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`dataset_id`** (string, required): ERDDAP datasetID from the tabledap catalog and request path. It is stable within the ERDDAP server and is used with erddap_id and station_id in CloudEvents subjects, Kafka keys, MQTT topics, and AMQP subjects. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`base_url`** (uri, required): Base URL of the ERDDAP server ending at /erddap. It is the documented root for allDatasets, info, and tabledap requests and is included so consumers can trace every event back to the source server.
- **`station_id`** (string, required): Stable station or platform identifier. For TimeSeries datasets this is read from the variable whose ERDDAP metadata declares cf_role=timeseries_id; for single-station datasets where rows carry null station values, the bridge falls back to the datasetID consistently. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`station_name`** (string or null, optional): Human-readable station or platform label from the timeseries_id variable long_name, station attributes, or dataset title. It is descriptive and never used as a key.
- **`station_id_variable`** (string or null, optional): ERDDAP variable name that supplied station_id through cf_role=timeseries_id, or null when the bridge uses the datasetID fallback for a single-station dataset.
- **`latitude`** (double or null, optional): WGS 84 latitude in decimal degrees north from ERDDAP latitude or station metadata. Nullable because some generic tabledap datasets do not expose a latitude column in every query result.
- **`longitude`** (double or null, optional): WGS 84 longitude in decimal degrees east from ERDDAP longitude or station metadata. Nullable because some generic tabledap datasets do not expose a longitude column in every query result.
- **`depth`** (double or null, optional): Vertical coordinate in metres when ERDDAP exposes depth or z metadata. Nullable because surface stations and many time-series datasets omit a vertical coordinate.
- **`attributes`** (map, required): Station-related ERDDAP attributes, including cf_role, ioos_code, short_name, type, long_name, and any other metadata attached to the station identifier variable.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "erddap_id": "string",
  "dataset_id": "string",
  "base_url": "string",
  "station_id": "string",
  "station_name": "string",
  "station_id_variable": "string",
  "latitude": 0,
  "longitude": 0,
  "depth": 0,
  "attributes": null
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Observation

CloudEvents type: `org.erddap.Observation`

#### What it tells you

A normalized ERDDAP tabledap observation row for one station or platform at one timestamp. It carries common coordinates and a dataset-specific measurement map whose per-variable units and metadata come from the ERDDAP info endpoint.

#### Identity

Each event identifies the real-world resource with `{erddap_id}/{dataset_id}/{station_id}`. `{erddap_id}` is stable, operator-assigned identifier for the configured ERDDAP server instance; `{dataset_id}` is ERDDAP datasetID from the tabledap catalog and request path; `{station_id}` is stable station or platform identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `erddap`, key `{erddap_id}/{dataset_id}/{station_id}` |
| `MQTT/5.0` | topic `marine/global/erddap/{erddap_id}/{dataset_id}/{station_id}/observation`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/erddap`, message subject `{erddap_id}/{dataset_id}/{station_id}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `erddap_id`, `dataset_id`, `base_url`, `station_id`, `time`, `measurements`.

- **`erddap_id`** (string, required): Stable, operator-assigned identifier for the configured ERDDAP server instance. ERDDAP dataset identifiers are only unique within one server, so consumers use this value with dataset_id and station_id as the global identity. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`dataset_id`** (string, required): ERDDAP datasetID from the tabledap catalog and request path. It is stable within the ERDDAP server and is used with erddap_id and station_id in CloudEvents subjects, Kafka keys, MQTT topics, and AMQP subjects. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`base_url`** (uri, required): Base URL of the ERDDAP server ending at /erddap. It is the documented root for allDatasets, info, and tabledap requests and is included so consumers can trace every event back to the source server.
- **`station_id`** (string, required): Stable station or platform identifier. For TimeSeries datasets this is read from the variable whose ERDDAP metadata declares cf_role=timeseries_id; for single-station datasets where rows carry null station values, the bridge falls back to the datasetID consistently. The feeder normalizes or requires this identity segment to contain only letters, digits, underscore, hyphen, and dot so Kafka keys, CloudEvents subjects, MQTT topics, and AMQP subjects remain unambiguous. Constraints: pattern `^[A-Za-z0-9_.-]+$`.
- **`time`** (string, required): Observation timestamp in UTC from the ERDDAP time column. tabledap returns ISO-8601 strings for JSON responses, and the bridge emits an RFC 3339 datetime so consumers can order and window observations. Encoded as an RFC 3339 UTC string in the payload for generated Avro/Python round-trip stability; the CloudEvents envelope time remains a native event timestamp.
- **`latitude`** (double or null, optional): WGS 84 latitude in decimal degrees north from ERDDAP latitude or station metadata. Nullable because some generic tabledap datasets do not expose a latitude column in every query result.
- **`longitude`** (double or null, optional): WGS 84 longitude in decimal degrees east from ERDDAP longitude or station metadata. Nullable because some generic tabledap datasets do not expose a longitude column in every query result.
- **`depth`** (double or null, optional): Vertical coordinate in metres when ERDDAP exposes depth or z metadata. Nullable because surface stations and many time-series datasets omit a vertical coordinate.
- **`measurements`** (map, required): Map of selected ERDDAP variable name to normalized value and variable metadata. This preserves heterogeneous dataset-specific measurements without inventing fixed units in the contract.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "erddap_id": "string",
  "dataset_id": "string",
  "base_url": "string",
  "station_id": "string",
  "time": "string",
  "latitude": 0,
  "longitude": 0,
  "depth": 0,
  "measurements": null
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

All payloads documented here are JSON. MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`xreg/erddap.xreg.json`](xreg/erddap.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
