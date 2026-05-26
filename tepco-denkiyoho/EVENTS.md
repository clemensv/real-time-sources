# TEPCO Electricity Supply & Demand (Denki Yoho) Bridge Events

MQTT 5.0 binary-mode CloudEvents variant of JP.TEPCO.Denkiyoho.

## At a glance

- **Event types:** 5 documented event types (15 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 5 telemetry event types.
- **Identity:** `jp.tepco.denkiyoho/{date}/{time}`, `{area_code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `tepco-denkiyoho`. The record key is `jp.tepco.denkiyoho/{date}/{time}`. In plain language, `jp.tepco.denkiyoho/{date}/{time}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['tepco-denkiyoho'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `energy/jp/tepco/tepco-denkiyoho/jp-tepco/supply-capacity`, `energy/jp/tepco/tepco-denkiyoho/jp-tepco/peak-demand-forecast`, `energy/jp/tepco/tepco-denkiyoho/jp-tepco/demand-actual`, `energy/jp/tepco/tepco-denkiyoho/jp-tepco/demand-forecast`, `energy/jp/tepco/tepco-denkiyoho/jp-tepco/info`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('energy/jp/tepco/tepco-denkiyoho/jp-tepco/supply-capacity', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `tepco-denkiyoho`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/tepco-denkiyoho')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Supply Capacity

CloudEvents type: `JP.TEPCO.Denkiyoho.SupplyCapacity`

#### What it tells you

Daily TEPCO Electricity Forecast supply capability reference record for the Tokyo service area. Daily reference schema for TEPCO Electricity Forecast supply capability and daily maximum-usage summary metadata. The source CSV is Shift-JIS encoded and section 1 reports peak supply capacity, reserve margin, usage percentage, and update time for the Tokyo Electric Power Company service area.

#### Identity

Each event identifies the real-world resource with `jp.tepco.denkiyoho/{date}/{time}`. `{date}` is service date for TEPCO's Electricity Forecast daily CSV in local Tokyo time, normalized from the DATE column to ISO 8601 calendar-date form (YYYY-MM-DD); `{time}` is stable subject and Kafka key time component. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tepco-denkiyoho`, key `jp.tepco.denkiyoho/{date}/{time}` |
| `MQTT/5.0` | topic `energy/jp/tepco/tepco-denkiyoho/jp-tepco/supply-capacity`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tepco-denkiyoho`, message subject `jp.tepco.denkiyoho/{date}/{time}` |

#### Payload

`Supply Capacity` payloads are JSON object. Required fields: `date`, `time`, `peak_supply_capacity_mw`, `peak_supply_capacity_jp_unit_value`, `peak_time_slot`, `peak_reserve_margin_pct`, `peak_usage_pct`, `daily_max_usage_pct`, `daily_max_usage_time_slot`, `update_datetime`, `update_datetime_local`, `area_code`, `area_name_jp`, `area_name_en`.

- **`date`** (date, required): Service date for TEPCO's Electricity Forecast daily CSV in local Tokyo time, normalized from the DATE column to ISO 8601 calendar-date form (YYYY-MM-DD). This date is a stable key component for all records from the same operating day.
- **`time`** (string, required): Stable subject and Kafka key time component. Supply capacity is daily reference data rather than a point-in-time demand measurement, so the bridge sets this field to the sentinel value _supply_capacity_ while using the same jp.tepco.denkiyoho/{date}/{time} key model as demand events. Constraints: pattern `^(([01][0-9]|2[0-3]):[0-5][0-9]|_supply_capacity_|_peak_forecast_)$`.
- **`peak_supply_capacity_mw`** (double, required, MW): Peak-time available supply capability for the Tokyo service area shown by TEPCO as ピーク時供給力(万kW). The bridge converts the published 10,000-kilowatt unit to megawatts by multiplying the source value by 10. Constraints: minimum `0`.
- **`peak_supply_capacity_jp_unit_value`** (int32, required, 10MW (万kW)): Original integer value from TEPCO's ピーク時供給力(万kW) header field. TEPCO publishes demand and supply values in 万kW, where one unit is 10,000 kilowatts, equal to 10 megawatts. Constraints: minimum `0`.
- **`peak_time_slot`** (string, required): Local Japan Standard Time hour range from TEPCO's section 1 時間帯 column indicating the peak supply-capability time slot, normalized to an ASCII hyphen such as 13:00-14:00. Constraints: pattern `^(([01]?[0-9]|2[0-3]):[0-5][0-9])-(([01]?[0-9]|2[0-3]):[0-5][0-9])$`.
- **`peak_reserve_margin_pct`** (double, required, percent (%)): Peak-time reserve margin percentage from TEPCO's section 1 ピーク時予備率(%) column for the published peak supply-capability slot. Constraints: minimum `0`, maximum `100`.
- **`peak_usage_pct`** (double, required, percent (%)): Peak-time usage percentage from TEPCO's section 1 ピーク時使用率(%) column for the published peak supply-capability slot. Constraints: minimum `0`, maximum `100`.
- **`daily_max_usage_pct`** (double or null, required, percent (%)): Daily maximum usage percentage from TEPCO's section 4 最大使用率(%) summary row. The field is null when that section is absent or blank in the CSV. Constraints: minimum `0`, maximum `100`.
- **`daily_max_usage_time_slot`** (string or null, required): Local Japan Standard Time hour range from TEPCO's section 4 時間帯 column for the daily maximum usage percentage, normalized to an ASCII hyphen such as 4:00-5:00. The field is null when that section is absent or blank. Constraints: pattern `^(([01]?[0-9]|2[0-3]):[0-5][0-9])-(([01]?[0-9]|2[0-3]):[0-5][0-9])$`.
- **`update_datetime`** (datetime, required): Section 1 supply-capability information update timestamp converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp. TEPCO publishes the date and time in 供給力情報更新日 and 供給力情報更新時刻.
- **`update_datetime_local`** (datetime, required): Section 1 supply-capability information update timestamp in Japan Standard Time serialized as an RFC 3339 timestamp with +09:00 offset, built from TEPCO's 供給力情報更新日 and 供給力情報更新時刻 columns.
- **`area_code`** (string, required): Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page.
- **`area_name_jp`** (string, required): Japanese name of the TEPCO Power Grid service area used by the Electricity Forecast page: 東京電力エリア. The page defines this as Tokyo plus Kanagawa, Saitama, Chiba, Tochigi, Gunma, Ibaraki, Yamanashi, and the portion of Shizuoka east of the Fujikawa River.
- **`area_name_en`** (string, required): English display name for the TEPCO service territory covered by the Electricity Forecast page: TEPCO Service Area (Kanto).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "date": null,
  "time": "string",
  "peak_supply_capacity_mw": 0,
  "peak_supply_capacity_jp_unit_value": 0,
  "peak_time_slot": "string",
  "peak_reserve_margin_pct": 0,
  "peak_usage_pct": 0,
  "daily_max_usage_pct": 0,
  "daily_max_usage_time_slot": "string",
  "update_datetime": "2024-01-01T00:00:00Z",
  "update_datetime_local": "2024-01-01T00:00:00Z",
  "area_code": "string",
  "area_name_jp": "string",
  "area_name_en": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Peak Demand Forecast

CloudEvents type: `JP.TEPCO.Denkiyoho.PeakDemandForecast`

#### What it tells you

Daily TEPCO Electricity Forecast maximum-demand forecast record for the Tokyo service area. Daily reference schema for TEPCO Electricity Forecast section 2 peak-demand forecast metadata for the Tokyo Electric Power Company service area.

#### Identity

Each event identifies the real-world resource with `jp.tepco.denkiyoho/{date}/{time}`. `{date}` is operating date for TEPCO's section 2 peak-demand forecast, normalized from 予想最大電力情報更新日 with the CSV update year to ISO 8601 calendar-date form (YYYY-MM-DD); `{time}` is stable subject and Kafka key time component for the section 2 peak-demand forecast. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tepco-denkiyoho`, key `jp.tepco.denkiyoho/{date}/{time}` |
| `MQTT/5.0` | topic `energy/jp/tepco/tepco-denkiyoho/jp-tepco/peak-demand-forecast`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tepco-denkiyoho`, message subject `jp.tepco.denkiyoho/{date}/{time}` |

#### Payload

`Peak Demand Forecast` payloads are JSON object. Required fields: `date`, `time`, `peak_demand_forecast_mw`, `peak_demand_forecast_jp_unit_value`, `peak_time_slot`, `update_datetime`, `update_datetime_local`, `area_code`, `area_name_jp`, `area_name_en`.

- **`date`** (date, required): Operating date for TEPCO's section 2 peak-demand forecast, normalized from 予想最大電力情報更新日 with the CSV update year to ISO 8601 calendar-date form (YYYY-MM-DD). This is the stable date key component.
- **`time`** (string, required): Stable subject and Kafka key time component for the section 2 peak-demand forecast. The bridge sets this field to the sentinel value _peak_forecast_ so the daily peak forecast shares the same jp.tepco.denkiyoho/{date}/{time} key model as the other TEPCO events without pretending to be an hourly measurement. Constraints: pattern `^(([01][0-9]|2[0-3]):[0-5][0-9]|_supply_capacity_|_peak_forecast_)$`.
- **`peak_demand_forecast_mw`** (double, required, MW): Forecast maximum electricity demand for the Tokyo service area from TEPCO's section 2 予想最大電力(万kW) row, converted from 万kW to megawatts by multiplying by 10. Constraints: minimum `0`.
- **`peak_demand_forecast_jp_unit_value`** (int32, required, 10MW (万kW)): Original integer peak-demand forecast value from TEPCO's section 2 予想最大電力(万kW) field. Constraints: minimum `0`.
- **`peak_time_slot`** (string, required): Local Japan Standard Time hour range from TEPCO's section 2 時間帯 column indicating when the forecast maximum demand is expected, normalized to an ASCII hyphen such as 13:00-14:00. Constraints: pattern `^(([01]?[0-9]|2[0-3]):[0-5][0-9])-(([01]?[0-9]|2[0-3]):[0-5][0-9])$`.
- **`update_datetime`** (datetime, required): Section 2 peak-demand forecast information update timestamp converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp. TEPCO publishes the date and time in 予想最大電力情報更新日 and 予想最大電力情報更新時刻.
- **`update_datetime_local`** (datetime, required): Section 2 peak-demand forecast information update timestamp in Japan Standard Time serialized as an RFC 3339 timestamp with +09:00 offset, built from TEPCO's 予想最大電力情報更新日 and 予想最大電力情報更新時刻 columns.
- **`area_code`** (string, required): Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page.
- **`area_name_jp`** (string, required): Japanese name of the TEPCO Power Grid service area used by the Electricity Forecast page: 東京電力エリア. The page defines this as Tokyo plus Kanagawa, Saitama, Chiba, Tochigi, Gunma, Ibaraki, Yamanashi, and the portion of Shizuoka east of the Fujikawa River.
- **`area_name_en`** (string, required): English display name for the TEPCO service territory covered by the Electricity Forecast page: TEPCO Service Area (Kanto).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "date": null,
  "time": "string",
  "peak_demand_forecast_mw": 0,
  "peak_demand_forecast_jp_unit_value": 0,
  "peak_time_slot": "string",
  "update_datetime": "2024-01-01T00:00:00Z",
  "update_datetime_local": "2024-01-01T00:00:00Z",
  "area_code": "string",
  "area_name_jp": "string",
  "area_name_en": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Demand Actual

CloudEvents type: `JP.TEPCO.Denkiyoho.DemandActual`

#### What it tells you

Actual electricity demand record from TEPCO Electricity Forecast for the Tokyo service area, emitted for hourly rows with section 3 context and for five-minute rows with section 5 solar context. Telemetry schema for actual TEPCO electricity demand in the Tokyo Electric Power Company service area. Hourly rows from section 3 carry usage and supply-capacity context, while five-minute rows from section 5 carry solar generation context.

#### Identity

Each event identifies the real-world resource with `jp.tepco.denkiyoho/{date}/{time}`. `{date}` is operating date from the DATE column in TEPCO's hourly actual-demand section or five-minute actual-demand section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD); `{time}` is local Japan Standard Time clock time from the TIME column in TEPCO's hourly or five-minute actual-demand section, normalized to zero-padded HH:MM form. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tepco-denkiyoho`, key `jp.tepco.denkiyoho/{date}/{time}` |
| `MQTT/5.0` | topic `energy/jp/tepco/tepco-denkiyoho/jp-tepco/demand-actual`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tepco-denkiyoho`, message subject `jp.tepco.denkiyoho/{date}/{time}` |

#### Payload

`Demand Actual` payloads are JSON object. Required fields: `date`, `time`, `datetime`, `datetime_local`, `actual_demand_mw`, `actual_demand_jp_unit_value`, `solar_generation_mw`, `solar_generation_jp_unit_value`, `solar_share_pct`, `usage_pct`, `supply_capacity_mw`, `supply_capacity_jp_unit_value`, `area_code`.

- **`date`** (date, required): Operating date from the DATE column in TEPCO's hourly actual-demand section or five-minute actual-demand section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD). This is the first stable key component.
- **`time`** (string, required): Local Japan Standard Time clock time from the TIME column in TEPCO's hourly or five-minute actual-demand section, normalized to zero-padded HH:MM form. This is the second stable key component. Constraints: pattern `^(([01][0-9]|2[0-3]):[0-5][0-9]|_supply_capacity_|_peak_forecast_)$`.
- **`datetime`** (datetime, required): Combined DATE and TIME converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp for cross-region analytics.
- **`datetime_local`** (datetime, required): Combined DATE and TIME serialized as an RFC 3339 timestamp with +09:00 offset for the Japan Standard Time instant represented by the TEPCO CSV row.
- **`actual_demand_mw`** (double, required, MW): Actual electricity demand for the Tokyo service area, converted to megawatts from TEPCO's 当日実績(万kW) hourly column or 当日実績(5分間隔値)(万kW) five-minute column by multiplying by 10. Constraints: minimum `0`.
- **`actual_demand_jp_unit_value`** (int32, required, 10MW (万kW)): Original integer value from TEPCO's 当日実績(万kW) hourly column or 当日実績(5分間隔値)(万kW) five-minute column. Rows with 0 or blank actual-demand values are future or unavailable measurements and are skipped by the bridge. Constraints: minimum `0`.
- **`solar_generation_mw`** (double or null, required, MW): Solar generation actual value converted to megawatts from TEPCO's section 5 太陽光発電実績(5分間隔値)(万kW) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar cell. Constraints: minimum `0`.
- **`solar_generation_jp_unit_value`** (int32 or null, required, 10MW (万kW)): Original integer solar generation actual value from TEPCO's section 5 太陽光発電実績(5分間隔値)(万kW) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar cell. Constraints: minimum `0`.
- **`solar_share_pct`** (double or null, required, percent (%)): Solar generation percentage of electricity usage from TEPCO's section 5 太陽光発電量(電力使用量に対する割合)(%) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar-share cell. Constraints: minimum `0`, maximum `100`.
- **`usage_pct`** (double or null, required, percent (%)): Usage percentage from TEPCO's hourly section 3 使用率(%) column. This field is populated only for hourly-cadence DemandActual rows derived from section 3; it is null for five-minute rows derived from section 5. TEPCO may leave future-hour usage blank until actual demand is available. Constraints: minimum `0`.
- **`supply_capacity_mw`** (double or null, required, MW): Available supply capacity converted to megawatts from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence rows derived from section 3; it is null for five-minute rows derived from section 5. Constraints: minimum `0`.
- **`supply_capacity_jp_unit_value`** (int32 or null, required, 10MW (万kW)): Original integer supply-capacity value from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence rows derived from section 3; it is null for five-minute rows derived from section 5. Constraints: minimum `0`.
- **`area_code`** (string, required): Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "date": null,
  "time": "string",
  "datetime": "2024-01-01T00:00:00Z",
  "datetime_local": "2024-01-01T00:00:00Z",
  "actual_demand_mw": 0,
  "actual_demand_jp_unit_value": 0,
  "solar_generation_mw": 0,
  "solar_generation_jp_unit_value": 0,
  "solar_share_pct": 0,
  "usage_pct": 0,
  "supply_capacity_mw": 0,
  "supply_capacity_jp_unit_value": 0,
  "area_code": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Demand Forecast

CloudEvents type: `JP.TEPCO.Denkiyoho.DemandForecast`

#### What it tells you

Hourly electricity demand forecast record from TEPCO Electricity Forecast for the Tokyo service area. Hourly telemetry schema for TEPCO electricity demand forecasts in the Tokyo Electric Power Company service area, including usage and supply-capacity context from section 3.

#### Identity

Each event identifies the real-world resource with `jp.tepco.denkiyoho/{date}/{time}`. `{date}` is operating date from the DATE column in TEPCO's hourly same-day forecast section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD); `{time}` is local Japan Standard Time clock hour from the TIME column in TEPCO's hourly forecast section, normalized to zero-padded HH:MM form. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tepco-denkiyoho`, key `jp.tepco.denkiyoho/{date}/{time}` |
| `MQTT/5.0` | topic `energy/jp/tepco/tepco-denkiyoho/jp-tepco/demand-forecast`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tepco-denkiyoho`, message subject `jp.tepco.denkiyoho/{date}/{time}` |

#### Payload

`Demand Forecast` payloads are JSON object. Required fields: `date`, `time`, `datetime`, `datetime_local`, `forecast_demand_mw`, `forecast_demand_jp_unit_value`, `usage_pct`, `supply_capacity_mw`, `supply_capacity_jp_unit_value`, `area_code`.

- **`date`** (date, required): Operating date from the DATE column in TEPCO's hourly same-day forecast section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD). This is the first stable key component.
- **`time`** (string, required): Local Japan Standard Time clock hour from the TIME column in TEPCO's hourly forecast section, normalized to zero-padded HH:MM form. This is the second stable key component. Constraints: pattern `^(([01][0-9]|2[0-3]):[0-5][0-9]|_supply_capacity_|_peak_forecast_)$`.
- **`datetime`** (datetime, required): Combined DATE and TIME converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp for cross-region analytics.
- **`datetime_local`** (datetime, required): Combined DATE and TIME serialized as an RFC 3339 timestamp with +09:00 offset for the Japan Standard Time instant represented by the TEPCO CSV row.
- **`forecast_demand_mw`** (double, required, MW): Hourly forecast electricity demand for the Tokyo service area, converted to megawatts from TEPCO's section 3 予測値(万kW) column by multiplying by 10. Constraints: minimum `0`.
- **`forecast_demand_jp_unit_value`** (int32, required, 10MW (万kW)): Original integer value from TEPCO's section 3 予測値(万kW) hourly forecast column. The bridge uses this value in forecast de-duplication so revised forecasts for the same date and hour are emitted again. Constraints: minimum `0`.
- **`usage_pct`** (double or null, required, percent (%)): Usage percentage from TEPCO's hourly section 3 使用率(%) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3 and can be null when TEPCO leaves future-hour usage blank until actual demand is available. Constraints: minimum `0`.
- **`supply_capacity_mw`** (double or null, required, MW): Available supply capacity converted to megawatts from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3. Constraints: minimum `0`.
- **`supply_capacity_jp_unit_value`** (int32 or null, required, 10MW (万kW)): Original integer supply-capacity value from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3. Constraints: minimum `0`.
- **`area_code`** (string, required): Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "date": null,
  "time": "string",
  "datetime": "2024-01-01T00:00:00Z",
  "datetime_local": "2024-01-01T00:00:00Z",
  "forecast_demand_mw": 0,
  "forecast_demand_jp_unit_value": 0,
  "usage_pct": 0,
  "supply_capacity_mw": 0,
  "supply_capacity_jp_unit_value": 0,
  "area_code": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Info

CloudEvents type: `JP.TEPCO.Denkiyoho.Info`

#### What it tells you

Retained reference information for MQTT/AMQP topic discovery. Reference information for the source, area, or event collection used by MQTT retained topics and AMQP consumers to discover the logical feed scope.

#### Identity

Each event identifies the real-world resource with `{area_code}`. `{area_code}` is electricity control area or utility service area code represented by this record when applicable. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `tepco-denkiyoho`, key `jp.tepco.denkiyoho/{date}/{time}` |
| `MQTT/5.0` | topic `energy/jp/tepco/tepco-denkiyoho/jp-tepco/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/tepco-denkiyoho`, message subject `{area_code}` |

#### Payload

`Info` payloads are JSON object. Required fields: `info_id`, `name`.

- **`info_id`** (string, required): Stable identifier for the reference information record; used as the CloudEvents subject when no more specific upstream entity exists.
- **`name`** (string, required): Human-readable name for the source, area, or event collection represented by this reference information record.
- **`country`** (string or null, optional): Lower-case ISO 3166-1 alpha-2 country code or intl when the feed spans countries.
- **`city`** (string or null, optional): City segment used in civic-events topic routing, or null when not applicable.
- **`category`** (string or null, optional): Event category segment used in topic routing, or null when not applicable.
- **`price_area`** (string or null, optional): Energy market price area or bidding zone represented by this reference record, when applicable.
- **`settlement_date`** (string or null, optional): GB settlement date for Elexon retained information topics when applicable.
- **`settlement_period`** (int32 or null, optional): GB settlement period for Elexon retained information topics when applicable.
- **`area_code`** (string or null, optional): Electricity control area or utility service area code represented by this record when applicable.
- **`segment`** (string or null, optional): Ticketmaster classification segment used for wildcard topic routing, when applicable.
- **`entity_id`** (string or null, optional): Stable upstream entity identifier for reference topics, when applicable.
- **`event_id`** (string or null, optional): Stable upstream event identifier for event-scoped reference topics, when applicable.
- **`venue_id`** (string or null, optional): Stable venue identifier for venue-scoped civic event topics, when applicable.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "info_id": "string",
  "name": "string",
  "country": "string",
  "city": "string",
  "category": "string",
  "price_area": "string",
  "settlement_date": "string",
  "settlement_period": 0,
  "area_code": "string",
  "segment": "string",
  "entity_id": "string",
  "event_id": "string",
  "venue_id": "string"
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

## References

- xRegistry manifest: [`xreg/tepco-denkiyoho.xreg.json`](xreg/tepco-denkiyoho.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
