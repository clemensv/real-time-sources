# USGS Water Services - Instantaneous Value Service Usage Guide Events

MQTT/5.0 transport variants for USGS site metadata. Topics are retained QoS-1 site info leaves under hydro/us/usgs/usgs-iv/{site_no}/info. The manifest intentionally uses existing schema field names site_no and parameter_cd rather than adding aliases.

## At a glance

- **Event types:** 28 documented event types (56 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 1 reference/catalog event type and 27 telemetry event types.
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

## Event catalog

### Site

CloudEvents type: `USGS.Sites.Site`

#### What it tells you

USGS site metadata.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}`. `{agency_cd}` is agency code; `{site_no}` is USGS site number. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/info`, retain `true`, QoS `1` |

#### Payload

`Site` payloads are JSON object. Required fields: `agency_cd`, `site_no`, `station_nm`, `site_tp_cd`, `lat_va`, `long_va`, `coord_meth_cd`, `coord_acy_cd`, `coord_datum_cd`, `dec_coord_datum_cd`, `district_cd`, `state_cd`, `county_cd`, `country_cd`, `land_net_ds`, `map_nm`, `alt_meth_cd`, `alt_datum_cd`, `huc_cd`, `basin_cd`, `topo_cd`, `instruments_cd`, `tz_cd`, `local_time_fg`, `reliability_cd`, `gw_file_cd`, `nat_aqfr_cd`, `aqfr_cd`, `aqfr_type_cd`, `depth_src_cd`, `project_no`.

- **`agency_cd`** (string, required): Agency code.
- **`site_no`** (string, required): USGS site number.
- **`station_nm`** (string, required): Station name.
- **`site_tp_cd`** (string, required): Site type code.
- **`lat_va`** (string, required): DMS latitude.
- **`long_va`** (string, required): DMS longitude.
- **`dec_lat_va`** (float, optional): Decimal latitude.
- **`dec_long_va`** (float, optional): Decimal longitude.
- **`coord_meth_cd`** (string, required): Latitude-longitude method code.
- **`coord_acy_cd`** (string, required): Coordinate accuracy code.
- **`coord_datum_cd`** (string, required): Latitude-longitude datum code.
- **`dec_coord_datum_cd`** (string, required): Decimal latitude-longitude datum code.
- **`district_cd`** (string, required): District code.
- **`state_cd`** (string, required): State code.
- **`county_cd`** (string, required): County code.
- **`country_cd`** (string, required): Country code.
- **`land_net_ds`** (string, required): Land net location description.
- **`map_nm`** (string, required): Location map name.
- **`map_scale_fc`** (float, optional): Location map scale factor.
- **`alt_va`** (float, optional): Altitude.
- **`alt_meth_cd`** (string, required): Method altitude determined code.
- **`alt_acy_va`** (float, optional): Altitude accuracy.
- **`alt_datum_cd`** (string, required): Altitude datum code.
- **`huc_cd`** (string, required): Hydrologic unit code.
- **`basin_cd`** (string, required): Drainage basin code.
- **`topo_cd`** (string, required): Topographic setting code.
- **`instruments_cd`** (string, required): Flags for instruments at site.
- **`construction_dt`** (string, optional): Date of first construction.
- **`inventory_dt`** (string, optional): Date site established or inventoried.
- **`drain_area_va`** (float, optional): Drainage area.
- **`contrib_drain_area_va`** (float, optional): Contributing drainage area.
- **`tz_cd`** (string, required): Time Zone abbreviation.
- **`local_time_fg`** (boolean, required): Site honors Daylight Savings Time flag.
- **`reliability_cd`** (string, required): Data reliability code.
- **`gw_file_cd`** (string, required): Data-other GW files code.
- **`nat_aqfr_cd`** (string, required): National aquifer code.
- **`aqfr_cd`** (string, required): Local aquifer code.
- **`aqfr_type_cd`** (string, required): Local aquifer type code.
- **`well_depth_va`** (float, optional): Well depth.
- **`hole_depth_va`** (float, optional): Hole depth.
- **`depth_src_cd`** (string, required): Source of depth data.
- **`project_no`** (string, required): Project number.
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

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Site Timeseries

CloudEvents type: `USGS.Sites.SiteTimeseries`

#### What it tells you

USGS site timeseries metadata.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is agency code; `{site_no}` is USGS site number; `{parameter_cd}` is parameter code; `{timeseries_cd}` is timeseries code. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/timeseries`, retain `true`, QoS `1` |

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

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Other Parameter

CloudEvents type: `USGS.InstantaneousValues.OtherParameter`

#### What it tells you

USGS other parameter data.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Other Parameter` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS precipitation data. Parameter code 00045.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Precipitation` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Precipitation value, inches."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS streamflow data. Parameter code 00060.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Streamflow` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Discharge value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

### Gage Height

CloudEvents type: `USGS.InstantaneousValues.GageHeight`

#### What it tells you

USGS gage height data. Parameter code 00065.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Gage Height` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Gage height value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS water temperature data. Parameter code 00010.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Water Temperature` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Water temperature value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

### Dissolved Oxygen

CloudEvents type: `USGS.InstantaneousValues.DissolvedOxygen`

#### What it tells you

USGS dissolved oxygen data. Parameter code 00300.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Dissolved Oxygen` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Dissolved oxygen value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS pH data. Parameter code 00400.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`P H` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "pH value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS specific conductance data. Parameter code 00095.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Specific Conductance` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Specific conductance value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS turbidity data. Parameter code 00076.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Turbidity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Turbidity value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS air temperature data. Parameter code 00020.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Air Temperature` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Air temperature value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS wind speed data. Parameter code 00035.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Wind Speed` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Wind speed value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS wind direction data. Parameter codes 00036 and 163695.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Wind Direction` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Wind direction value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS relative humidity data. Parameter code 00052.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Relative Humidity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Relative humidity value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS barometric pressure data. Parameter codes 62605 and 75969.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Barometric Pressure` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Barometric pressure value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS turbidity data (FNU). Parameter code 63680.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Turbidity FNU` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Turbidity value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`F DOM` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Dissolved organic matter fluorescence value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS reservoir storage data. Parameter code 00054.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Reservoir Storage` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Reservoir storage value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

### Lake Elevation NGVD29

CloudEvents type: `USGS.InstantaneousValues.LakeElevationNGVD29`

#### What it tells you

USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Lake Elevation NGVD29` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Lake elevation above NGVD 1929."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS water depth data. Parameter code 72199.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Water Depth` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Water depth value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

### Equipment Status

CloudEvents type: `USGS.InstantaneousValues.EquipmentStatus`

#### What it tells you

USGS equipment alarm status data. Parameter code 99235.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Equipment Status` payloads are JSON object. Required fields: `site_no`, `datetime`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`status`** (string, optional): {"description": "Status of equipment alarm as codes."}
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

USGS tidally filtered discharge data. Parameter code 72137.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Tidally Filtered Discharge` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Tidally filtered discharge value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS water velocity data. Parameter code 72254.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Water Velocity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Water velocity value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

### Estuary Elevation NGVD29

CloudEvents type: `USGS.InstantaneousValues.EstuaryElevationNGVD29`

#### What it tells you

USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Estuary Elevation NGVD29` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Estuary or ocean water surface elevation above NGVD 1929."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Lake Elevation NAVD88` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Lake elevation above NAVD 1988."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS salinity data. Parameter code 00480.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Salinity` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Salinity value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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

USGS gate opening data. Parameter code 45592.

#### Identity

Each event identifies the real-world resource with `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`. `{agency_cd}` is a payload field with the same name; `{site_no}` is {"description": "USGS site number."}; `{parameter_cd}` is {"description": "Parameter code."}; `{timeseries_cd}` is {"description": "Timeseries code."}. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-iv`, key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation`, retain `true`, QoS `1` |

#### Payload

`Gate Opening` payloads are JSON object. Required fields: `site_no`, `datetime`, `qualifiers`, `parameter_cd`, `timeseries_cd`.

- **`site_no`** (string, required): {"description": "USGS site number."}
- **`datetime`** (string, required): {"description": "Date and time of the measurement in ISO-8601 format."}
- **`value`** (double, optional): {"description": "Gate opening value."}
- **`exception`** (string, optional): {"description": "Exception code when the value is unavailable."}
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
