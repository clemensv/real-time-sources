# USGS Water Data Events

Native USGS continuous water observations and their monitoring-location, time-series and parameter references. Consumers receive exact observation values, provisional status, sensor qualifiers, threshold history and acknowledged corrections on Kafka, MQTT or AMQP.

## At a glance

- **Event types:** 4 documented event types (16 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 4 telemetry event types.
- **Identity:** `{time_series_id}` identifies the resource each event is about.
- **Operations:** The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `usgs-waterdata`. The record key is `{time_series_id}`. In plain language, `{time_series_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['usgs-waterdata'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `hydro/us/usgs/waterdata/+/observation`, `hydro/us/usgs/waterdata/+/time-series`, `hydro/us/usgs/waterdata/+/monitoring-location`, `hydro/us/usgs/waterdata/+/parameter`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hydro/us/usgs/waterdata/+/observation', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `usgs-waterdata`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/usgs-waterdata')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Continuous Observation

CloudEvents type: `USGS.WaterData.ContinuousObservation`

#### What it tells you

Native USGS continuous observation, including approval, qualifier, method category and exact value text. Corrections are events for the same series and observation instant when scientific content changes.

#### Identity

Each event identifies the real-world resource with `{time_series_id}`. `{time_series_id}` is native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-waterdata`, key `{time_series_id}` |
| `MQTT/5.0` | topic `hydro/us/usgs/waterdata/{time_series_id}/observation`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/usgs-waterdata`, message subject `{time_series_id}` |

#### Payload

`Continuous Observation` payloads are JSON object. Required fields: `time_series_id`, `time`.

- **`time_series_id`** (string, required): Native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. Never a legacy numeric NWIS TS_ID. Constraints: minLength `1`.
- **`monitoring_location_id`** (string or null, optional): A unique identifier representing a single monitoring location. This corresponds to the `id` field in the `monitoring-locations` endpoint. Monitoring location IDs are created by combining the agency code of the agency responsible for the monitoring location (e.g. USGS) with the ID number of the monitoring location (e.g. 02238500), separated by a hyphen (e.g. USGS-02238500). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`parameter_code`** (string or null, optional): Parameter codes are 5-digit codes used to identify the constituent measured and the units of measure. A complete list of parameter codes and associated groupings can be found at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema. Constraints: pattern `^[0-9]{5}$`.
- **`statistic_id`** (string or null, optional): A code corresponding to the statistic an observation represents. Example codes include 00001 (max), 00002 (min), and 00003 (mean). A complete list of codes and their descriptions can be found at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/statistic-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/statistic-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`time`** (datetime, required): The date an observation represents. You can query this field using date-times or intervals, adhering to RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded or half-bounded (double-dots at start or end). Examples: - A date-time: "2018-02-12T23:20:50Z" - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z" - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or "../2018-03-18T12:31:12Z" - Duration objects: "P1M" for data from the past month or "PT36H" for the last 36 hours Only features that have a `time` that intersects the value of datetime are selected. If a feature has multiple temporal properties, it is the decision of the server whether only a single temporal property is used to determine the extent or all relevant temporal properties. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`value`** (string or null, optional): The value of the observation. Values are transmitted as strings in the JSON response format in order to preserve precision. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`unit_of_measure`** (string or null, optional): A human-readable description of the units of measurement associated with an observation. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`approval_status`** (string or null, optional): Some of the data that you have obtained from this U.S. Geological Survey database may not have received Director's approval. Any such data values are qualified as provisional and are subject to revision. Provisional data are released on the condition that neither the USGS nor the United States Government may be held liable for any damages resulting from its use. This field reflects the approval status of each record, and is either "Approved", meaining processing review has been completed and the data is approved for publication, or "Provisional" and subject to revision. For more information about provisional data, go to [https://waterdata.usgs.gov/provisional-data-statement/](https://waterdata.usgs.gov/provisional-data-statement/). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`qualifier`** (string or null, optional): This field indicates any qualifiers associated with an observation, for instance if a sensor may have been impacted by ice or if values were estimated. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`last_modified`** (datetime or null, optional): The last time a record was refreshed in our database. This may happen due to regular operational processes and does not necessarily indicate anything about the measurement has changed. You can query this field using date-times or intervals, adhering to RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded or half-bounded (double-dots at start or end). Examples: - A date-time: "2018-02-12T23:20:50Z" - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z" - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or "../2018-03-18T12:31:12Z" - Duration objects: "P1M" for data from the past month or "PT36H" for the last 36 hours Only features that have a `last_modified` that intersects the value of datetime are selected. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`method_category`** (string or null, optional): The RLMS method category code classifying the method in effect for this interval. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/continuous/schema.
- **`geometry`** (object, optional): OGC feature geometry; null when the reference collection has no geometry. See [geometry](#payload-usgs-waterdata-continuousobservation-geometry).
- **`feature_id`** (string or null, optional): OGC continuous feature id from the outer Feature; a database record identifier, not the series identity or dedupe key.
##### geometry
<a id="payload-usgs-waterdata-continuousobservation-geometry"></a>

OGC GeoJSON Point in EPSG:4326; coordinates are longitude then latitude in decimal degrees. The original survey datum remains on the monitoring-location reference.

- **`type`** (string, required): GeoJSON geometry discriminator; monitoring locations use Point.
- **`coordinates`** (array of double, required): Longitude and latitude in decimal degrees, in that order.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_series_id": "string",
  "monitoring_location_id": "string",
  "parameter_code": "string",
  "statistic_id": "string",
  "time": "2024-01-01T00:00:00Z",
  "value": "string",
  "unit_of_measure": "string",
  "approval_status": "string",
  "qualifier": "string",
  "last_modified": "2024-01-01T00:00:00Z",
  "method_category": "string",
  "geometry": {
    "type": "Point",
    "coordinates": [
      0
    ]
  },
  "feature_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Time Series

CloudEvents type: `USGS.WaterData.TimeSeries`

#### What it tells you

Reference metadata for one native instantaneous Points time series. Only computation_identifier=Instantaneous and computation_period_identifier=Points are emitted; other OGC products are out of scope.

#### Identity

Each event identifies the real-world resource with `{time_series_id}`. `{time_series_id}` is native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-waterdata`, key `{time_series_id}` |
| `MQTT/5.0` | topic `hydro/us/usgs/waterdata/{time_series_id}/time-series`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/usgs-waterdata`, message subject `{time_series_id}` |

#### Payload

`Time Series` payloads are JSON object. Required fields: `thresholds`, `time_series_id`.

- **`unit_of_measure`** (string or null, optional): A human-readable description of the units of measurement associated with an observation. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`parameter_name`** (string or null, optional): A human-understandable name corresponding to `parameter_code`. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`parameter_code`** (string or null, optional): Parameter codes are 5-digit codes used to identify the constituent measured and the units of measure. A complete list of parameter codes and associated groupings can be found at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`statistic_id`** (string or null, optional): A code corresponding to the statistic an observation represents. Example codes include 00001 (max), 00002 (min), and 00003 (mean). A complete list of codes and their descriptions can be found at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/statistic-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/statistic-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`last_modified`** (string or null, optional): The last time a record was refreshed in our database. This may happen due to regular operational processes and does not necessarily indicate anything about the measurement has changed. You can query this field using date-times or intervals, adhering to RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded or half-bounded (double-dots at start or end). Examples: - A date-time: "2018-02-12T23:20:50Z" - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z" - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or "../2018-03-18T12:31:12Z" - Duration objects: "P1M" for data from the past month or "PT36H" for the last 36 hours Only features that have a `last_modified` that intersects the value of datetime are selected. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema. The live metadata API omits a timezone on some values; the original text is retained without assigning an unreported offset.
- **`begin`** (datetime or null, optional): The datetime of the earliest observation in the time series. Together with `end`, this field represents the period of record of a time series. Note that some time series may have large gaps in their collection record. You can query this field using date-times or intervals, adhering to RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded or half-bounded (double-dots at start or end). Examples: - A date-time: "2018-02-12T23:20:50Z" - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z" - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or "../2018-03-18T12:31:12Z" - Duration objects: "P1M" for data from the past month or "PT36H" for the last 36 hours Only features that have a `begin` that intersects the value of datetime are selected. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`end`** (datetime or null, optional): The datetime of the most recent observation in the time series. Data returned by this endpoint updates at most once per day, and potentially less frequently than that, and as such there may be more recent observations within a time series than the time series `end` value reflects. Together with `begin`, this field represents the period of record of a time series. It is additionally used to determine whether a time series is "active". You can query this field using date-times or intervals, adhering to RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded or half-bounded (double-dots at start or end). Examples: - A date-time: "2018-02-12T23:20:50Z" - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z" - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or "../2018-03-18T12:31:12Z" - Duration objects: "P1M" for data from the past month or "PT36H" for the last 36 hours Only features that have a `end` that intersects the value of datetime are selected. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`computation_period_identifier`** (string or null, optional): Indicates the period of data used for any statistical computations. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`computation_identifier`** (string or null, optional): Indicates the computation performed to calculate this time series. Values of "Instantaneous" reflect point measurements. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`thresholds`** (array of object, required): Thresholds represent known numeric limits for a time series, for example the historic maximum value for a parameter or a level below which a sensor is non-operative. These thresholds are sometimes used to automatically determine if an observation is erroneous due to sensor error, and therefore shouldn't be included in the time series. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema. Modeled from the live array, including effective periods; not the incorrect published string.
- **`sublocation_identifier`** (string or null, optional): An optional human-readable identifier used to specify where measurements are recorded at a monitoring location. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`primary`** (string or null, optional): A flag identifying if the time series is a "primary" time series. "Primary" time series (which have this flag) are standard observations which undergo [Bureau review and approval processes](https://www.usgs.gov/survey-manual/5028-fundamental-science-practices-review-and-approval-scientific-data-release). Non-primary time series, which will have missing values for "primary", are provisional datasets made available to meet the need for timely best science and to assist with daily operations which need real-time information. Non-primary time series data are only retained by this system for 120 days. See the [USGS Provisional Data Statement](https://waterdata.usgs.gov/provisional-data-statement/) for more information. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`monitoring_location_id`** (string or null, optional): A unique identifier representing a single monitoring location. This corresponds to the `id` field in the `monitoring-locations` endpoint. Monitoring location IDs are created by combining the agency code of the agency responsible for the monitoring location (e.g. USGS) with the ID number of the monitoring location (e.g. 02238500), separated by a hyphen (e.g. USGS-02238500). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`web_description`** (string or null, optional): An optional description of the time series. WDFN and other USGS data dissemination products use this field, in combination with sublocation_identifier, to distinguish the differences between multiple time series for the same parameter code, statistic code, and monitoring location. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`parameter_description`** (string or null, optional): A description of what the parameter code represents, as used by WDFN and other USGS data dissemination products. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`parent_time_series_id`** (string or null, optional): The unique identifier representing the parent or "upchain" time series that a daily values time series is generated from. Daily values time series have one and only one parent time series. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`data_gap_interval`** (duration or null, optional): The time interval threshold used for gap detection in the time series. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`statistics_begin`** (string or null, optional): When this field is populated, WDFN does not include data before this year when computing statistics. If the field is not populated, the full period of record is used. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/time-series-metadata/schema.
- **`time_series_id`** (string, required): Native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. Never a legacy numeric NWIS TS_ID. Constraints: minLength `1`.
- **`geometry`** (object, optional): OGC feature geometry; null when the reference collection has no geometry. See [geometry](#payload-usgs-waterdata-timeseries-geometry).
##### geometry
<a id="payload-usgs-waterdata-timeseries-geometry"></a>

OGC GeoJSON Point in EPSG:4326; coordinates are longitude then latitude in decimal degrees. The original survey datum remains on the monitoring-location reference.

- **`type`** (string, required): GeoJSON geometry discriminator; monitoring locations use Point.
- **`coordinates`** (array of double, required): Longitude and latitude in decimal degrees, in that order.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "unit_of_measure": "string",
  "parameter_name": "string",
  "parameter_code": "string",
  "statistic_id": "string",
  "last_modified": "string",
  "begin": "2024-01-01T00:00:00Z",
  "end": "2024-01-01T00:00:00Z",
  "computation_period_identifier": "string",
  "computation_identifier": "string",
  "thresholds": [
    {
      "name": "string",
      "type": "string",
      "periods": [
        {
          "start_time": "2024-01-01T00:00:00Z",
          "end_time": "2024-01-01T00:00:00Z",
          "applied_time": "2024-01-01T00:00:00Z",
          "comments": "string",
          "suppress_data": false,
          "reference_value": 0,
          "secondary_reference_value": 0
        }
      ],
      "severity": 0,
      "description": "string",
      "display_color": "string",
      "reference_code": "string",
      "processing_order": "string"
    }
  ],
  "sublocation_identifier": "string",
  "primary": "string",
  "monitoring_location_id": "string",
  "web_description": "string",
  "parameter_description": "string",
  "parent_time_series_id": "string",
  "data_gap_interval": null,
  "statistics_begin": "string",
  "time_series_id": "string",
  "geometry": {
    "type": "Point",
    "coordinates": [
      0
    ]
  }
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Monitoring Location

CloudEvents type: `USGS.WaterData.MonitoringLocation`

#### What it tells you

MonitoringLocation reference attached to each native series that uses it. The time_series_id attachment is the existing relationship from time-series-metadata, not a new property claimed on the upstream resource.

#### Identity

Each event identifies the real-world resource with `{time_series_id}`. `{time_series_id}` is native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-waterdata`, key `{time_series_id}` |
| `MQTT/5.0` | topic `hydro/us/usgs/waterdata/{time_series_id}/monitoring-location`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/usgs-waterdata`, message subject `{time_series_id}` |

#### Payload

`Monitoring Location` payloads are JSON object. Required fields: `time_series_id`, `location`.

- **`time_series_id`** (string, required): Native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. Never a legacy numeric NWIS TS_ID. Constraints: minLength `1`.
- **`location`** (object, required): Complete monitoring-locations properties plus its OGC geometry. See [location](#payload-usgs-waterdata-monitoringlocation-location).
##### location
<a id="payload-usgs-waterdata-monitoringlocation-location"></a>

Complete selected USGS monitoring-locations resource properties and geometry.

- **`id`** (string or null, optional): A unique identifier representing a single monitoring location. This corresponds to the `monitoring_location_id` field in other endpoints. Monitoring location IDs are created by combining the agency code of the agency responsible for the monitoring location (e.g. USGS) with the ID number of the monitoring location (e.g. 02238500), separated by a hyphen (e.g. USGS-02238500). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`agency_code`** (string or null, optional): The agency that is reporting the data. Agency codes are fixed values assigned by the National Water Information System (NWIS). A list of agency codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/agency-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/agency-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`agency_name`** (string or null, optional): The name of the agency that is reporting the data. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`monitoring_location_number`** (string or null, optional): Each monitoring location in the USGS data base has a unique 8- to 15-digit identification number. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`monitoring_location_name`** (string or null, optional): This is the official name of the monitoring location in the database. For well information this can be a district-assigned local number. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`district_code`** (string or null, optional): The Water Science Centers (WSCs) across the United States use the FIPS state code as the district code. In some case, monitoring locations and samples may be managed by a water science center that is adjacent to the state in which the monitoring location actually resides. For example a monitoring location may have a district code of 30 which translates to Montana, but the state code could be 56 for Wyoming because that is where the monitoring location actually is located. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`country_code`** (string or null, optional): The code for the country in which the monitoring location is located. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`country_name`** (string or null, optional): The name of the country in which the monitoring location is located. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`state_code`** (string or null, optional): State code. A [two-digit ANSI code](https://www2.census.gov/geo/docs/reference/state.txt) (formerly FIPS code) as defined by the American National Standards Institute, to define States and equivalents. A three-digit ANSI code is used to define counties and county equivalents. [A lookup table is available.](https://www.census.gov/library/reference/code-lists/ansi.html#states) The only countries with political subdivisions other than the US are Mexico and Canada. The Mexican states have US state codes ranging from 81-86 and Canadian provinces have state codes ranging from 90-98. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`state_name`** (string or null, optional): The name of the state or state equivalent in which the monitoring location is located. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`county_code`** (string or null, optional): The code for the county or county equivalent (parish, borough, etc.) in which the monitoring location is located. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/counties/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/counties/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`county_name`** (string or null, optional): The name of the county or county equivalent (parish, borough, etc.) in which the monitoring location is located. [A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/counties/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/counties/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`minor_civil_division_code`** (string or null, optional): Codes for primary governmental or administrative divisions of the county or county equivalent in which the monitoring location is located. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`site_type_code`** (string or null, optional): A code describing the hydrologic setting of the monitoring location. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/site-types/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/site-types/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`site_type`** (string or null, optional): A description of the hydrologic setting of the monitoring location. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/site-types/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/site-types/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`hydrologic_unit_code`** (string or null, optional): The hydrologic unit code (HUC) for the monitoring location. Supports prefix matching — querying with a shorter HUC (e.g. "04") matches all locations within that hydrologic region. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`basin_code`** (string or null, optional): The Basin Code or "drainage basin code" is a two-digit code that further subdivides the 8-digit hydrologic-unit code. The drainage basin code is defined by the USGS State Office where the monitoring location is located. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`altitude`** (double or null, optional, ft): Altitude of the monitoring location referenced to the specified Vertical Datum. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`altitude_accuracy`** (double or null, optional, ft): Accuracy of the altitude, in feet. An accuracy of +/- 0.1 foot would be entered as “.1”. Many altitudes are interpolated from the contours on topographic maps; accuracies determined in this way are generally entered as one-half of the contour interval. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`altitude_method_code`** (string or null, optional): Codes representing the method used to measure altitude. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`altitude_method_name`** (string or null, optional): The name of the method used to measure altitude. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`vertical_datum`** (string or null, optional): The datum used to determine altitude and vertical position at the monitoring location. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/altitude-datums/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/altitude-datums/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`vertical_datum_name`** (string or null, optional): The datum used to determine altitude and vertical position at the monitoring location. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/altitude-datums/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/altitude-datums/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`horizontal_positional_accuracy_code`** (string or null, optional): Indicates the accuracy of the latitude longitude values. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-accuracy-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-accuracy-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`horizontal_positional_accuracy`** (string or null, optional): Indicates the accuracy of the latitude longitude values. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-accuracy-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-accuracy-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`horizontal_position_method_code`** (string or null, optional): Indicates the method used to determine latitude longitude values. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-method-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-method-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`horizontal_position_method_name`** (string or null, optional): Indicates the method used to determine latitude longitude values. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-method-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-method-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`original_horizontal_datum`** (string or null, optional): Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System 1984. This field indicates the original datum used to determine coordinates before they were converted. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-datum-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-datum-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`original_horizontal_datum_name`** (string or null, optional): Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System 1984. This field indicates the original datum used to determine coordinates before they were converted. A list of codes is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-datum-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/coordinate-datum-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`drainage_area`** (double or null, optional, mi^2 (mi²)): The area enclosed by a topographic divide from which direct surface runoff from precipitation normally drains by gravity into the stream above that point. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`contributing_drainage_area`** (double or null, optional, mi^2 (mi²)): The contributing drainage area of a lake, stream, wetland, or estuary monitoring location, in square miles. This item should be present only if the contributing area is different from the total drainage area. This situation can occur when part of the drainage area consists of very porous soil or depressions that either allow all runoff to enter the groundwater or traps the water in ponds so that rainfall does not contribute to runoff. A transbasin diversion can also affect the total drainage area. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`time_zone_abbreviation`** (string or null, optional): A short code describing the time zone used by a monitoring location. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`uses_daylight_savings`** (string or null, optional): A flag indicating whether or not a monitoring location uses daylight savings. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`construction_date`** (string or null, optional): Date the well was completed. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema. Preserved as upstream text because partial dates can occur.
- **`aquifer_code`** (string or null, optional): Local aquifers in the USGS water resources data base are identified by a geohydrologic unit code (a three-digit number related to the age of the formation, followed by a 4 or 5 character abbreviation for the geologic unit or aquifer name). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`national_aquifer_code`** (string or null, optional): National aquifers are the principal aquifers or aquifer systems in the United States, defined as regionally extensive aquifers or aquifer systems that have the potential to be used as a source of potable water. Not all groundwater monitoring locations can be associated with a National Aquifer. Such monitoring locations will not be retrieved using this search criteria. A list of National aquifer codes and names is available at [https://api.waterdata.usgs.gov/ogcapi/v1/collections/national-aquifer-codes/items](https://api.waterdata.usgs.gov/ogcapi/v1/collections/national-aquifer-codes/items). Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`aquifer_type_code`** (string or null, optional): Describes the confinement status of an aquifer at the monitoring location. A confined aquifer is an aquifer below the land surface that is saturated with water. A water table--or unconfined--aquifer is an aquifer whose upper water surface (water table) is at atmospheric pressure, and thus is able to rise and fall. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`well_constructed_depth`** (double or null, optional, ft): The depth of the finished well, in feet below land surface datum. Note: Not all groundwater monitoring locations have information on Well Depth. Such monitoring locations will not be retrieved using this search criteria. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`hole_constructed_depth`** (double or null, optional, ft): The total depth to which the hole is drilled, in feet below land surface datum. Note: Not all groundwater monitoring locations have information on Hole Depth. Such monitoring locations will not be retrieved using this search criteria. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`depth_source_code`** (string or null, optional): A code indicating the source of water-level data. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`revision_note`** (string or null, optional): Approved water data are considered published record, but on occasion changes or deletions (revisions) must be made to data after they are approved. Data revisions are rare because of USGS quality assurance practices, including documentation of all data before they are officially approved. This field contains text explanations for data revisions at this monitoring location. Changes to data also are indicated with revision qualifier codes alongside the data. Text explanations before 2017 are not necessarily available online, but can be requested. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`revision_created`** (datetime or null, optional): The date a revision statement was created. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`revision_modified`** (datetime or null, optional): The most recent date a revision statement was modified. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/schema.
- **`geometry`** (object, optional): OGC feature geometry; null when the reference collection has no geometry. See [geometry](#payload-usgs-waterdata-monitoringlocation-location-geometry).
##### geometry
<a id="payload-usgs-waterdata-monitoringlocation-geometry"></a>

OGC GeoJSON Point in EPSG:4326; coordinates are longitude then latitude in decimal degrees. The original survey datum remains on the monitoring-location reference.

- **`type`** (string, required): GeoJSON geometry discriminator; monitoring locations use Point.
- **`coordinates`** (array of double, required): Longitude and latitude in decimal degrees, in that order.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_series_id": "string",
  "location": {
    "id": "string",
    "agency_code": "string",
    "agency_name": "string",
    "monitoring_location_number": "string",
    "monitoring_location_name": "string",
    "district_code": "string",
    "country_code": "string",
    "country_name": "string",
    "state_code": "string",
    "state_name": "string",
    "county_code": "string",
    "county_name": "string",
    "minor_civil_division_code": "string",
    "site_type_code": "string",
    "site_type": "string",
    "hydrologic_unit_code": "string",
    "basin_code": "string",
    "altitude": 0,
    "altitude_accuracy": 0,
    "altitude_method_code": "string",
    "altitude_method_name": "string",
    "vertical_datum": "string",
    "vertical_datum_name": "string",
    "horizontal_positional_accuracy_code": "string",
    "horizontal_positional_accuracy": "string",
    "horizontal_position_method_code": "string",
    "horizontal_position_method_name": "string",
    "original_horizontal_datum": "string",
    "original_horizontal_datum_name": "string",
    "drainage_area": 0,
    "contributing_drainage_area": 0,
    "time_zone_abbreviation": "string",
    "uses_daylight_savings": "string",
    "construction_date": "string",
    "aquifer_code": "string",
    "national_aquifer_code": "string",
    "aquifer_type_code": "string",
    "well_constructed_depth": 0,
    "hole_constructed_depth": 0,
    "depth_source_code": "string",
    "revision_note": "string",
    "revision_created": "2024-01-01T00:00:00Z",
    "revision_modified": "2024-01-01T00:00:00Z",
    "geometry": {
      "type": "Point",
      "coordinates": [
        0
      ]
    }
  }
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Parameter

CloudEvents type: `USGS.WaterData.Parameter`

#### What it tells you

Parameter reference attached to each native series that uses it. The time_series_id attachment is the existing relationship from time-series-metadata, not a new property claimed on the upstream resource.

#### Identity

Each event identifies the real-world resource with `{time_series_id}`. `{time_series_id}` is native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-waterdata`, key `{time_series_id}` |
| `MQTT/5.0` | topic `hydro/us/usgs/waterdata/{time_series_id}/parameter`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/usgs-waterdata`, message subject `{time_series_id}` |

#### Payload

`Parameter` payloads are JSON object. Required fields: `time_series_id`, `parameter`.

- **`time_series_id`** (string, required): Native opaque USGS time-series identifier, equal to time-series-metadata.id and continuous.time_series_id. Never a legacy numeric NWIS TS_ID. Constraints: minLength `1`.
- **`parameter`** (object, required): Complete parameter-codes properties plus its OGC geometry. See [parameter](#payload-usgs-waterdata-parameter-parameter).
##### parameter
<a id="payload-usgs-waterdata-parameter-parameter"></a>

Complete selected USGS parameter-codes resource properties and geometry.

- **`id`** (string or null, optional): Parameter code. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema. Constraints: pattern `^[0-9]{5}$`.
- **`parameter_name`** (string or null, optional): Parameter short name. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`unit_of_measure`** (string or null, optional): Parameter reporting units defined to cooperate with descriptions by USEPA. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`parameter_group_code`** (string or null, optional): Categorical groupings of parameters by water-quality data type for display and report ordering Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`parameter_description`** (string or null, optional): Parameter description. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`medium`** (string or null, optional): Parameter medium. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`statistical_basis`** (string or null, optional): Parameter statistical basis. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`time_basis`** (string or null, optional): Parameter time basis. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`weight_basis`** (string or null, optional): Parameter weight basis. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`particle_size_basis`** (string or null, optional): Parameter particle-size basis. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`sample_fraction`** (string or null, optional): Parameter fraction. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`temperature_basis`** (string or null, optional): Parameter temperature basis. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`epa_equivalence`** (string or null, optional): Indicates the relationship of the USGS parameter code to the EPA code. Source: https://api.waterdata.usgs.gov/ogcapi/v1/collections/parameter-codes/schema.
- **`geometry`** (object, optional): OGC feature geometry; null when the reference collection has no geometry. See [geometry](#payload-usgs-waterdata-parameter-parameter-geometry).
##### geometry
<a id="payload-usgs-waterdata-parameter-geometry"></a>

OGC GeoJSON Point in EPSG:4326; coordinates are longitude then latitude in decimal degrees. The original survey datum remains on the monitoring-location reference.

- **`type`** (string, required): GeoJSON geometry discriminator; monitoring locations use Point.
- **`coordinates`** (array of double, required): Longitude and latitude in decimal degrees, in that order.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "time_series_id": "string",
  "parameter": {
    "id": "string",
    "parameter_name": "string",
    "unit_of_measure": "string",
    "parameter_group_code": "string",
    "parameter_description": "string",
    "medium": "string",
    "statistical_basis": "string",
    "time_basis": "string",
    "weight_basis": "string",
    "particle_size_basis": "string",
    "sample_fraction": "string",
    "temperature_basis": "string",
    "epa_equivalence": "string",
    "geometry": {
      "type": "Point",
      "coordinates": [
        0
      ]
    }
  }
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

- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/usgs-waterdata.xreg.json`](xreg/usgs-waterdata.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Upstream API: <https://api.waterdata.usgs.gov/ogcapi/v1>
- Deploy Service Bus: <https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-amqp>
- OGC API documentation / collections: <https://api.waterdata.usgs.gov/ogcapi/v1/collections>
- API keys and request limits: <https://api.waterdata.usgs.gov/docs/ogcapi/keys/>
