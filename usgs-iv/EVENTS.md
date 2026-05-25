# USGS Water Services - Instantaneous Value Service Usage Guide Events

USGS Instantaneous Values publishes instantaneous water observations such as gauge height, discharge, and temperature from the U.S. Geological Survey (USGS) Water Services API for United States streamgages and other monitoring sites. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 28 documented event types (84 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 3 reference/catalog event types and 25 telemetry event types.
- **Identity:** `{agency_cd}/{site_no}`, `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `usgs-iv`. The record key is `{agency_cd}/{site_no}`, `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['usgs-iv'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/us/usgs/usgs-iv/+/info`, `hydro/us/usgs/usgs-iv/+/+/+/timeseries`, `hydro/us/usgs/usgs-iv/+/+/+/observation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/us/usgs/usgs-iv/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `usgs-iv`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/usgs-iv')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Site

CloudEvents type: `USGS.Sites.Site`

#### What it tells you

A reference record for one United States streamgages and other monitoring site published by the U.S. Geological Survey (USGS) Water Services API. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}`. `{agency_cd}` is USGS or partner agency code for the site; `{site_no}` is USGS site number within the agency. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}` |

#### Payload

`Site` payloads are JSON object. Required fields: `agency_cd`, `site_no`, `station_nm`, `site_tp_cd`, `lat_va`, `long_va`, `coord_meth_cd`, `coord_acy_cd`, `coord_datum_cd`, `dec_coord_datum_cd`, `district_cd`, `state_cd`, `county_cd`, `country_cd`, `land_net_ds`, `map_nm`, `alt_meth_cd`, `alt_datum_cd`, `huc_cd`, `basin_cd`, `topo_cd`, `instruments_cd`, `tz_cd`, `local_time_fg`, `reliability_cd`, `gw_file_cd`, `nat_aqfr_cd`, `aqfr_cd`, `aqfr_type_cd`, `depth_src_cd`, `project_no`.

- **`agency_cd`** (string, required): USGS or partner agency code for the site. Combined with `site_no`, it forms the stable site identity used in CloudEvents subjects and transport keys.
- **`site_no`** (string, required): USGS site number within the agency. Combined with `agency_cd`, it uniquely identifies the monitoring location.
- **`station_nm`** (string, required): Human-readable site name published by USGS. Use `agency_cd` and `site_no` for stable joins because names can change.
- **`site_tp_cd`** (string, required): USGS site-type code describing the kind of monitoring location, such as stream, lake, well, or atmospheric site.
- **`lat_va`** (string, required): Latitude in degrees-minutes-seconds text as published by USGS.
- **`long_va`** (string, required): Longitude in degrees-minutes-seconds text as published by USGS.
- **`dec_lat_va`** (float or null, optional): Latitude in decimal degrees when USGS provides decimal coordinates.
- **`dec_long_va`** (float or null, optional): Longitude in decimal degrees when USGS provides decimal coordinates.
- **`coord_meth_cd`** (string, required): USGS method code describing how the latitude and longitude were determined.
- **`coord_acy_cd`** (string, required): USGS accuracy code for the published coordinates.
- **`coord_datum_cd`** (string, required): Horizontal datum code for the degrees-minutes-seconds coordinates.
- **`dec_coord_datum_cd`** (string, required): Horizontal datum code for the decimal coordinates.
- **`district_cd`** (string, required): USGS district code responsible for or associated with the site.
- **`state_cd`** (string, required): FIPS state code for the site location.
- **`county_cd`** (string, required): FIPS county code for the site location.
- **`country_cd`** (string, required): Country code for the site location.
- **`land_net_ds`** (string, required): Land net location description.
- **`map_nm`** (string, required): Location map name.
- **`map_scale_fc`** (float or null, optional): Location map scale factor.
- **`alt_va`** (float or null, optional): Altitude.
- **`alt_meth_cd`** (string, required): Method altitude determined code.
- **`alt_acy_va`** (float or null, optional): Altitude accuracy.
- **`alt_datum_cd`** (string, required): Altitude datum code.
- **`huc_cd`** (string, required): Hydrologic Unit Code identifying the watershed containing the site.
- **`basin_cd`** (string, required): Drainage basin code.
- **`topo_cd`** (string, required): Topographic setting code.
- **`instruments_cd`** (string, required): USGS code summarizing the instrumentation installed at the site.
- **`construction_dt`** (string or null, optional): Date of first construction.
- **`inventory_dt`** (string or null, optional): Date site established or inventoried.
- **`drain_area_va`** (float or null, optional): Drainage area.
- **`contrib_drain_area_va`** (float or null, optional): Contributing drainage area.
- **`tz_cd`** (string, required): Time-zone code used for local timestamps at the site.
- **`local_time_fg`** (boolean, required): Flag indicating whether timestamps are reported in the site local time zone.
- **`reliability_cd`** (string, required): USGS reliability code describing the expected reliability of the site data.
- **`gw_file_cd`** (string, required): Data-other GW files code.
- **`nat_aqfr_cd`** (string, required): National aquifer code.
- **`aqfr_cd`** (string, required): Local aquifer code.
- **`aqfr_type_cd`** (string, required): Local aquifer type code.
- **`well_depth_va`** (float or null, optional): Well depth.
- **`hole_depth_va`** (float or null, optional): Hole depth.
- **`depth_src_cd`** (string, required): Source of depth data.
- **`project_no`** (string, required): USGS project number associated with the site, when provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "agency_cd": "string",
  "site_no": "string",
  "station_nm": "string",
  "site_tp_cd": "string",
  "lat_va": "string",
  "long_va": "string",
  "dec_lat_va": 0,
  "dec_long_va": 0,
  "coord_meth_cd": "string",
  "coord_acy_cd": "string",
  "coord_datum_cd": "string",
  "dec_coord_datum_cd": "string",
  "district_cd": "string",
  "state_cd": "string",
  "county_cd": "string",
  "country_cd": "string",
  "land_net_ds": "string",
  "map_nm": "string",
  "map_scale_fc": 0,
  "alt_va": 0,
  "alt_meth_cd": "string",
  "alt_acy_va": 0,
  "alt_datum_cd": "string",
  "huc_cd": "string",
  "basin_cd": "string",
  "topo_cd": "string",
  "instruments_cd": "string",
  "construction_dt": "string",
  "inventory_dt": "string",
  "drain_area_va": 0,
  "contrib_drain_area_va": 0,
  "tz_cd": "string",
  "local_time_fg": false,
  "reliability_cd": "string",
  "gw_file_cd": "string",
  "nat_aqfr_cd": "string",
  "aqfr_cd": "string",
  "aqfr_type_cd": "string",
  "well_depth_va": 0,
  "hole_depth_va": 0,
  "depth_src_cd": "string",
  "project_no": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Site Timeseries

CloudEvents type: `USGS.Sites.SiteTimeseries`

#### What it tells you

A reference record for one United States streamgages and other monitoring site published by the U.S. Geological Survey (USGS) Water Services API. It fires when the bridge publishes or refreshes the station catalog so consumers can interpret measurement events.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is agency code; `{site_no}` is USGS site number; `{parameter_cd}` is parameter code; `{timeseries_cd}` is timeseries code. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/timeseries`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Site Timeseries` payloads are JSON object. Required fields: `agency_cd`, `site_no`, `parameter_cd`, `timeseries_cd`, `description`.

- **`agency_cd`** (string, required): Agency code.
- **`site_no`** (string, required): USGS site number.
- **`parameter_cd`** (string, required): Parameter code.
- **`timeseries_cd`** (string, required): Timeseries code.
- **`description`** (string, required): Description.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "agency_cd": "string",
  "site_no": "string",
  "parameter_cd": "string",
  "timeseries_cd": "string",
  "description": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Other Parameter

CloudEvents type: `USGS.InstantaneousValues.OtherParameter`

#### What it tells you

A other parameter event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Other Parameter` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Precipitation

CloudEvents type: `USGS.InstantaneousValues.Precipitation`

#### What it tells you

A precipitation event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Precipitation` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Precipitation value, inches."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Streamflow

CloudEvents type: `USGS.InstantaneousValues.Streamflow`

#### What it tells you

A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Streamflow` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Discharge value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Gage Height

CloudEvents type: `USGS.InstantaneousValues.GageHeight`

#### What it tells you

A gage height event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Gage Height` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Gage height value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Water Temperature

CloudEvents type: `USGS.InstantaneousValues.WaterTemperature`

#### What it tells you

A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Water Temperature` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Water temperature value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Dissolved Oxygen

CloudEvents type: `USGS.InstantaneousValues.DissolvedOxygen`

#### What it tells you

A dissolved oxygen event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Dissolved Oxygen` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Dissolved oxygen value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### P H

CloudEvents type: `USGS.InstantaneousValues.pH`

#### What it tells you

A p h event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`P H` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "pH value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Specific Conductance

CloudEvents type: `USGS.InstantaneousValues.SpecificConductance`

#### What it tells you

A specific conductance event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Specific Conductance` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Specific conductance value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Turbidity

CloudEvents type: `USGS.InstantaneousValues.Turbidity`

#### What it tells you

A turbidity event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Turbidity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Turbidity value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Air Temperature

CloudEvents type: `USGS.InstantaneousValues.AirTemperature`

#### What it tells you

A air temperature event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Air Temperature` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Air temperature value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Wind Speed

CloudEvents type: `USGS.InstantaneousValues.WindSpeed`

#### What it tells you

A wind speed event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Wind Speed` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Wind speed value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Wind Direction

CloudEvents type: `USGS.InstantaneousValues.WindDirection`

#### What it tells you

A wind direction event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Wind Direction` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Wind direction value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Relative Humidity

CloudEvents type: `USGS.InstantaneousValues.RelativeHumidity`

#### What it tells you

A relative humidity event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Relative Humidity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Relative humidity value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Barometric Pressure

CloudEvents type: `USGS.InstantaneousValues.BarometricPressure`

#### What it tells you

A barometric pressure event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Barometric Pressure` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Barometric pressure value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Turbidity FNU

CloudEvents type: `USGS.InstantaneousValues.TurbidityFNU`

#### What it tells you

A turbidity f n u event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Turbidity FNU` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Turbidity value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### F DOM

CloudEvents type: `USGS.InstantaneousValues.fDOM`

#### What it tells you

A f d o m event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`F DOM` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Dissolved organic matter fluorescence value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Reservoir Storage

CloudEvents type: `USGS.InstantaneousValues.ReservoirStorage`

#### What it tells you

A current reservoir record from the U.S. Geological Survey (USGS) Water Services API. It reports the latest storage, elevation, capacity, or related reservoir status available for one reservoir.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Reservoir Storage` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Reservoir storage value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Lake Elevation NGVD29

CloudEvents type: `USGS.InstantaneousValues.LakeElevationNGVD29`

#### What it tells you

A lake elevation n g v d29 event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Lake Elevation NGVD29` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Lake elevation above NGVD 1929."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Water Depth

CloudEvents type: `USGS.InstantaneousValues.WaterDepth`

#### What it tells you

A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Water Depth` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Water depth value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Equipment Status

CloudEvents type: `USGS.InstantaneousValues.EquipmentStatus`

#### What it tells you

A equipment status event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Equipment Status` payloads are JSON object. Required fields: `site_no`, `datetime`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`status`** (string or null, optional): {"description": "Status of equipment alarm as codes."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "status": "string",
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Tidally Filtered Discharge

CloudEvents type: `USGS.InstantaneousValues.TidallyFilteredDischarge`

#### What it tells you

A tidally filtered discharge event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Tidally Filtered Discharge` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Tidally filtered discharge value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Water Velocity

CloudEvents type: `USGS.InstantaneousValues.WaterVelocity`

#### What it tells you

A current measurement from the U.S. Geological Survey (USGS) Water Services API for one monitoring site. It carries instantaneous water observations such as gauge height, discharge, and temperature when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Water Velocity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Water velocity value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Estuary Elevation NGVD29

CloudEvents type: `USGS.InstantaneousValues.EstuaryElevationNGVD29`

#### What it tells you

A estuary elevation n g v d29 event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Estuary Elevation NGVD29` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Estuary or ocean water surface elevation above NGVD 1929."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Lake Elevation NAVD88

CloudEvents type: `USGS.InstantaneousValues.LakeElevationNAVD88`

#### What it tells you

A lake elevation n a v d88 event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Lake Elevation NAVD88` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Lake elevation above NAVD 1988."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Salinity

CloudEvents type: `USGS.InstantaneousValues.Salinity`

#### What it tells you

A salinity event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Salinity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Salinity value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Gate Opening

CloudEvents type: `USGS.InstantaneousValues.GateOpening`

#### What it tells you

A gate opening event from the U.S. Geological Survey (USGS) Water Services API. It represents source data for United States streamgages and other monitoring sites as published by the upstream feed.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-iv`, message subject `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Payload

`Gate Opening` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double or null, optional): {"description": "Gate opening value."}
- **`exception`** (string or null, optional): {"description": "Exception code when the value is unavailable."}
- **`qualifiers`** (array of string, required): {"description": "Qualifiers for the measurement."}
- **`parameter_cd`** (string, required): {"description": "Parameter code."}
- **`timeseries_cd`** (string, required): {"description": "Timeseries code."}
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_no": "string",
  "datetime": "string",
  "value": 0,
  "exception": "string",
  "qualifiers": [
    "string"
  ],
  "parameter_cd": "string",
  "timeseries_cd": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/usgs_iv.xreg.json`](xreg/usgs_iv.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- USGS Water Services: <https://waterservices.usgs.gov/>
- ![Deploy AMQP to Azure Service Bus: <https://aka.ms/deploytoazurebutton>
