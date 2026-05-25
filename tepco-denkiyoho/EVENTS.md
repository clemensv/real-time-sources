# TEPCO Electricity Supply & Demand (Denki Yoho) Bridge Events

This source polls Tokyo Electric Power Company (TEPCO) Electricity Forecast (でんき予報) open data and emits CloudEvents to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `JP.TEPCO.Denkiyoho.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.TEPCO.Denkiyoho`](#messagegroup-jptepcodenkiyoho) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `tepco-denkiyoho` |
| Kafka key | `jp.tepco.denkiyoho/{date}/{time}` |
| Deployed | False |

## Messagegroups

### Messagegroup `JP.TEPCO.Denkiyoho`
<a id="messagegroup-jptepcodenkiyoho"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.TEPCO.Denkiyoho.Kafka` (KAFKA) |
| Messages | 4 |

#### Message `jp.tepco.denkiyoho.SupplyCapacity`
<a id="message-jptepcodenkiyohosupplycapacity"></a>

Daily TEPCO Electricity Forecast supply capability reference record for the Tokyo service area.

| Field | Value |
| --- | --- |
| Name | SupplyCapacity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.tepco.denkiyoho.jstruct/schemas/jp.tepco.denkiyoho.SupplyCapacity`](#schema-jptepcodenkiyohosupplycapacity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.TEPCO.Denkiyoho.SupplyCapacity` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.TEPCO.Denkiyoho.Kafka` | `KAFKA` | topic `tepco-denkiyoho`; key `jp.tepco.denkiyoho/{date}/{time}` |

#### Message `jp.tepco.denkiyoho.PeakDemandForecast`
<a id="message-jptepcodenkiyohopeakdemandforecast"></a>

Daily TEPCO Electricity Forecast maximum-demand forecast record for the Tokyo service area.

| Field | Value |
| --- | --- |
| Name | PeakDemandForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.tepco.denkiyoho.jstruct/schemas/jp.tepco.denkiyoho.PeakDemandForecast`](#schema-jptepcodenkiyohopeakdemandforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.TEPCO.Denkiyoho.PeakDemandForecast` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.TEPCO.Denkiyoho.Kafka` | `KAFKA` | topic `tepco-denkiyoho`; key `jp.tepco.denkiyoho/{date}/{time}` |

#### Message `jp.tepco.denkiyoho.DemandActual`
<a id="message-jptepcodenkiyohodemandactual"></a>

Actual electricity demand record from TEPCO Electricity Forecast for the Tokyo service area, emitted for hourly rows with section 3 context and for five-minute rows with section 5 solar context.

| Field | Value |
| --- | --- |
| Name | DemandActual |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.tepco.denkiyoho.jstruct/schemas/jp.tepco.denkiyoho.DemandActual`](#schema-jptepcodenkiyohodemandactual) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.TEPCO.Denkiyoho.DemandActual` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.TEPCO.Denkiyoho.Kafka` | `KAFKA` | topic `tepco-denkiyoho`; key `jp.tepco.denkiyoho/{date}/{time}` |

#### Message `jp.tepco.denkiyoho.DemandForecast`
<a id="message-jptepcodenkiyohodemandforecast"></a>

Hourly electricity demand forecast record from TEPCO Electricity Forecast for the Tokyo service area.

| Field | Value |
| --- | --- |
| Name | DemandForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.tepco.denkiyoho.jstruct/schemas/jp.tepco.denkiyoho.DemandForecast`](#schema-jptepcodenkiyohodemandforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.TEPCO.Denkiyoho.DemandForecast` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.TEPCO.Denkiyoho.Kafka` | `KAFKA` | topic `tepco-denkiyoho`; key `jp.tepco.denkiyoho/{date}/{time}` |

## Schemagroups

### Schemagroup `jp.tepco.denkiyoho.jstruct`
<a id="schemagroup-jptepcodenkiyohojstruct"></a>

#### Schema `jp.tepco.denkiyoho.SupplyCapacity`
<a id="schema-jptepcodenkiyohosupplycapacity"></a>

| Field | Value |
| --- | --- |
| Name | SupplyCapacity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.tepco.co.jp/schemas/denkiyoho/SupplyCapacity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/jp/tepco/denkiyoho/SupplyCapacity` |
| Type | `object` |

###### Object `SupplyCapacity`
<a id="schema-node-supplycapacity"></a>

Daily reference schema for TEPCO Electricity Forecast supply capability and daily maximum-usage summary metadata. The source CSV is Shift-JIS encoded and section 1 reports peak supply capacity, reserve margin, usage percentage, and update time for the Tokyo Electric Power Company service area.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `date` | `date` | `True` | Service date for TEPCO's Electricity Forecast daily CSV in local Tokyo time, normalized from the DATE column to ISO 8601 calendar-date form (YYYY-MM-DD). This date is a stable key component for all records from the same operating day. | - | - | - |
| `time` | `string` | `True` | Stable subject and Kafka key time component. Supply capacity is daily reference data rather than a point-in-time demand measurement, so the bridge sets this field to the sentinel value _supply_capacity_ while using the same jp.tepco.denkiyoho/{date}/{time} key model as demand events. | - | pattern=`^(([01][0-9]\\|2[0-3]):[0-5][0-9]\\|_supply_capacity_\\|_peak_forecast_)$` | - |
| `peak_supply_capacity_mw` | `double` | `True` | Peak-time available supply capability for the Tokyo service area shown by TEPCO as ピーク時供給力(万kW). The bridge converts the published 10,000-kilowatt unit to megawatts by multiplying the source value by 10. | unit=`MW` symbol=`MW` | minimum=`0` | - |
| `peak_supply_capacity_jp_unit_value` | `int32` | `True` | Original integer value from TEPCO's ピーク時供給力(万kW) header field. TEPCO publishes demand and supply values in 万kW, where one unit is 10,000 kilowatts, equal to 10 megawatts. | unit=`10MW` symbol=`万kW` | minimum=`0` | - |
| `peak_time_slot` | `string` | `True` | Local Japan Standard Time hour range from TEPCO's section 1 時間帯 column indicating the peak supply-capability time slot, normalized to an ASCII hyphen such as 13:00-14:00. | - | pattern=`^(([01]?[0-9]\\|2[0-3]):[0-5][0-9])-(([01]?[0-9]\\|2[0-3]):[0-5][0-9])$` | - |
| `peak_reserve_margin_pct` | `double` | `True` | Peak-time reserve margin percentage from TEPCO's section 1 ピーク時予備率(%) column for the published peak supply-capability slot. | unit=`percent` symbol=`%` | maximum=`100`<br>minimum=`0` | - |
| `peak_usage_pct` | `double` | `True` | Peak-time usage percentage from TEPCO's section 1 ピーク時使用率(%) column for the published peak supply-capability slot. | unit=`percent` symbol=`%` | maximum=`100`<br>minimum=`0` | - |
| `daily_max_usage_pct` | `union` | `True` | Daily maximum usage percentage from TEPCO's section 4 最大使用率(%) summary row. The field is null when that section is absent or blank in the CSV. | unit=`percent` symbol=`%` | maximum=`100`<br>minimum=`0` | - |
| `daily_max_usage_time_slot` | `union` | `True` | Local Japan Standard Time hour range from TEPCO's section 4 時間帯 column for the daily maximum usage percentage, normalized to an ASCII hyphen such as 4:00-5:00. The field is null when that section is absent or blank. | - | pattern=`^(([01]?[0-9]\\|2[0-3]):[0-5][0-9])-(([01]?[0-9]\\|2[0-3]):[0-5][0-9])$` | - |
| `update_datetime` | `datetime` | `True` | Section 1 supply-capability information update timestamp converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp. TEPCO publishes the date and time in 供給力情報更新日 and 供給力情報更新時刻. | - | - | - |
| `update_datetime_local` | `datetime` | `True` | Section 1 supply-capability information update timestamp in Japan Standard Time serialized as an RFC 3339 timestamp with +09:00 offset, built from TEPCO's 供給力情報更新日 and 供給力情報更新時刻 columns. | - | - | - |
| `area_code` | `string` | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. | - | - | - |
| `area_name_jp` | `string` | `True` | Japanese name of the TEPCO Power Grid service area used by the Electricity Forecast page: 東京電力エリア. The page defines this as Tokyo plus Kanagawa, Saitama, Chiba, Tochigi, Gunma, Ibaraki, Yamanashi, and the portion of Shizuoka east of the Fujikawa River. | - | - | - |
| `area_name_en` | `string` | `True` | English display name for the TEPCO service territory covered by the Electricity Forecast page: TEPCO Service Area (Kanto). | - | - | - |

#### Schema `jp.tepco.denkiyoho.PeakDemandForecast`
<a id="schema-jptepcodenkiyohopeakdemandforecast"></a>

| Field | Value |
| --- | --- |
| Name | PeakDemandForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.tepco.co.jp/schemas/denkiyoho/PeakDemandForecast` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/jp/tepco/denkiyoho/PeakDemandForecast` |
| Type | `object` |

###### Object `PeakDemandForecast`
<a id="schema-node-peakdemandforecast"></a>

Daily reference schema for TEPCO Electricity Forecast section 2 peak-demand forecast metadata for the Tokyo Electric Power Company service area.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `date` | `date` | `True` | Operating date for TEPCO's section 2 peak-demand forecast, normalized from 予想最大電力情報更新日 with the CSV update year to ISO 8601 calendar-date form (YYYY-MM-DD). This is the stable date key component. | - | - | - |
| `time` | `string` | `True` | Stable subject and Kafka key time component for the section 2 peak-demand forecast. The bridge sets this field to the sentinel value _peak_forecast_ so the daily peak forecast shares the same jp.tepco.denkiyoho/{date}/{time} key model as the other TEPCO events without pretending to be an hourly measurement. | - | pattern=`^(([01][0-9]\\|2[0-3]):[0-5][0-9]\\|_supply_capacity_\\|_peak_forecast_)$` | - |
| `peak_demand_forecast_mw` | `double` | `True` | Forecast maximum electricity demand for the Tokyo service area from TEPCO's section 2 予想最大電力(万kW) row, converted from 万kW to megawatts by multiplying by 10. | unit=`MW` symbol=`MW` | minimum=`0` | - |
| `peak_demand_forecast_jp_unit_value` | `int32` | `True` | Original integer peak-demand forecast value from TEPCO's section 2 予想最大電力(万kW) field. | unit=`10MW` symbol=`万kW` | minimum=`0` | - |
| `peak_time_slot` | `string` | `True` | Local Japan Standard Time hour range from TEPCO's section 2 時間帯 column indicating when the forecast maximum demand is expected, normalized to an ASCII hyphen such as 13:00-14:00. | - | pattern=`^(([01]?[0-9]\\|2[0-3]):[0-5][0-9])-(([01]?[0-9]\\|2[0-3]):[0-5][0-9])$` | - |
| `update_datetime` | `datetime` | `True` | Section 2 peak-demand forecast information update timestamp converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp. TEPCO publishes the date and time in 予想最大電力情報更新日 and 予想最大電力情報更新時刻. | - | - | - |
| `update_datetime_local` | `datetime` | `True` | Section 2 peak-demand forecast information update timestamp in Japan Standard Time serialized as an RFC 3339 timestamp with +09:00 offset, built from TEPCO's 予想最大電力情報更新日 and 予想最大電力情報更新時刻 columns. | - | - | - |
| `area_code` | `string` | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. | - | - | - |
| `area_name_jp` | `string` | `True` | Japanese name of the TEPCO Power Grid service area used by the Electricity Forecast page: 東京電力エリア. The page defines this as Tokyo plus Kanagawa, Saitama, Chiba, Tochigi, Gunma, Ibaraki, Yamanashi, and the portion of Shizuoka east of the Fujikawa River. | - | - | - |
| `area_name_en` | `string` | `True` | English display name for the TEPCO service territory covered by the Electricity Forecast page: TEPCO Service Area (Kanto). | - | - | - |

#### Schema `jp.tepco.denkiyoho.DemandActual`
<a id="schema-jptepcodenkiyohodemandactual"></a>

| Field | Value |
| --- | --- |
| Name | DemandActual |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.tepco.co.jp/schemas/denkiyoho/DemandActual` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/jp/tepco/denkiyoho/DemandActual` |
| Type | `object` |

###### Object `DemandActual`
<a id="schema-node-demandactual"></a>

Telemetry schema for actual TEPCO electricity demand in the Tokyo Electric Power Company service area. Hourly rows from section 3 carry usage and supply-capacity context, while five-minute rows from section 5 carry solar generation context.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `date` | `date` | `True` | Operating date from the DATE column in TEPCO's hourly actual-demand section or five-minute actual-demand section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD). This is the first stable key component. | - | - | - |
| `time` | `string` | `True` | Local Japan Standard Time clock time from the TIME column in TEPCO's hourly or five-minute actual-demand section, normalized to zero-padded HH:MM form. This is the second stable key component. | - | pattern=`^(([01][0-9]\\|2[0-3]):[0-5][0-9]\\|_supply_capacity_\\|_peak_forecast_)$` | - |
| `datetime` | `datetime` | `True` | Combined DATE and TIME converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp for cross-region analytics. | - | - | - |
| `datetime_local` | `datetime` | `True` | Combined DATE and TIME serialized as an RFC 3339 timestamp with +09:00 offset for the Japan Standard Time instant represented by the TEPCO CSV row. | - | - | - |
| `actual_demand_mw` | `double` | `True` | Actual electricity demand for the Tokyo service area, converted to megawatts from TEPCO's 当日実績(万kW) hourly column or 当日実績(5分間隔値)(万kW) five-minute column by multiplying by 10. | unit=`MW` symbol=`MW` | minimum=`0` | - |
| `actual_demand_jp_unit_value` | `int32` | `True` | Original integer value from TEPCO's 当日実績(万kW) hourly column or 当日実績(5分間隔値)(万kW) five-minute column. Rows with 0 or blank actual-demand values are future or unavailable measurements and are skipped by the bridge. | unit=`10MW` symbol=`万kW` | minimum=`0` | - |
| `solar_generation_mw` | `union` | `True` | Solar generation actual value converted to megawatts from TEPCO's section 5 太陽光発電実績(5分間隔値)(万kW) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar cell. | unit=`MW` symbol=`MW` | minimum=`0` | - |
| `solar_generation_jp_unit_value` | `union` | `True` | Original integer solar generation actual value from TEPCO's section 5 太陽光発電実績(5分間隔値)(万kW) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar cell. | unit=`10MW` symbol=`万kW` | minimum=`0` | - |
| `solar_share_pct` | `union` | `True` | Solar generation percentage of electricity usage from TEPCO's section 5 太陽光発電量(電力使用量に対する割合)(%) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar-share cell. | unit=`percent` symbol=`%` | maximum=`100`<br>minimum=`0` | - |
| `usage_pct` | `union` | `True` | Usage percentage from TEPCO's hourly section 3 使用率(%) column. This field is populated only for hourly-cadence DemandActual rows derived from section 3; it is null for five-minute rows derived from section 5. TEPCO may leave future-hour usage blank until actual demand is available. | unit=`percent` symbol=`%` | minimum=`0` | - |
| `supply_capacity_mw` | `union` | `True` | Available supply capacity converted to megawatts from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence rows derived from section 3; it is null for five-minute rows derived from section 5. | unit=`MW` symbol=`MW` | minimum=`0` | - |
| `supply_capacity_jp_unit_value` | `union` | `True` | Original integer supply-capacity value from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence rows derived from section 3; it is null for five-minute rows derived from section 5. | unit=`10MW` symbol=`万kW` | minimum=`0` | - |
| `area_code` | `string` | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. | - | - | - |

#### Schema `jp.tepco.denkiyoho.DemandForecast`
<a id="schema-jptepcodenkiyohodemandforecast"></a>

| Field | Value |
| --- | --- |
| Name | DemandForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.tepco.co.jp/schemas/denkiyoho/DemandForecast` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/jp/tepco/denkiyoho/DemandForecast` |
| Type | `object` |

###### Object `DemandForecast`
<a id="schema-node-demandforecast"></a>

Hourly telemetry schema for TEPCO electricity demand forecasts in the Tokyo Electric Power Company service area, including usage and supply-capacity context from section 3.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `date` | `date` | `True` | Operating date from the DATE column in TEPCO's hourly same-day forecast section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD). This is the first stable key component. | - | - | - |
| `time` | `string` | `True` | Local Japan Standard Time clock hour from the TIME column in TEPCO's hourly forecast section, normalized to zero-padded HH:MM form. This is the second stable key component. | - | pattern=`^(([01][0-9]\\|2[0-3]):[0-5][0-9]\\|_supply_capacity_\\|_peak_forecast_)$` | - |
| `datetime` | `datetime` | `True` | Combined DATE and TIME converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp for cross-region analytics. | - | - | - |
| `datetime_local` | `datetime` | `True` | Combined DATE and TIME serialized as an RFC 3339 timestamp with +09:00 offset for the Japan Standard Time instant represented by the TEPCO CSV row. | - | - | - |
| `forecast_demand_mw` | `double` | `True` | Hourly forecast electricity demand for the Tokyo service area, converted to megawatts from TEPCO's section 3 予測値(万kW) column by multiplying by 10. | unit=`MW` symbol=`MW` | minimum=`0` | - |
| `forecast_demand_jp_unit_value` | `int32` | `True` | Original integer value from TEPCO's section 3 予測値(万kW) hourly forecast column. The bridge uses this value in forecast de-duplication so revised forecasts for the same date and hour are emitted again. | unit=`10MW` symbol=`万kW` | minimum=`0` | - |
| `usage_pct` | `union` | `True` | Usage percentage from TEPCO's hourly section 3 使用率(%) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3 and can be null when TEPCO leaves future-hour usage blank until actual demand is available. | unit=`percent` symbol=`%` | minimum=`0` | - |
| `supply_capacity_mw` | `union` | `True` | Available supply capacity converted to megawatts from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3. | unit=`MW` symbol=`MW` | minimum=`0` | - |
| `supply_capacity_jp_unit_value` | `union` | `True` | Original integer supply-capacity value from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3. | unit=`10MW` symbol=`万kW` | minimum=`0` | - |
| `area_code` | `string` | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. | - | - | - |

### Schemagroup `jp.tepco.denkiyoho.avro`
<a id="schemagroup-jptepcodenkiyohoavro"></a>

#### Schema `jp.tepco.denkiyoho.SupplyCapacity`
<a id="schema-jptepcodenkiyohosupplycapacity"></a>


##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SupplyCapacity |
| Namespace | jp.tepco.denkiyoho |
| Type | `record` |
| Doc | Daily reference schema for TEPCO Electricity Forecast supply capability and maximum usage summary. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `date` | `string` | Service date in ISO 8601 calendar-date form. | `-` |
| `time` | `string` | Stable key time component; supply capacity uses _supply_capacity_. | `-` |
| `peak_supply_capacity_mw` | `double` | Peak-time available supply capability converted from 万kW to MW. | `-` |
| `peak_supply_capacity_jp_unit_value` | `int` | Original peak supply capability value in 万kW. | `-` |
| `peak_time_slot` | `string` | Peak supply-capability time slot. | `-` |
| `peak_reserve_margin_pct` | `double` | Peak-time reserve margin percentage. | `-` |
| `peak_usage_pct` | `double` | Peak-time usage percentage. | `-` |
| `daily_max_usage_pct` | `null` \| `double` | Daily maximum usage percentage. | `-` |
| `daily_max_usage_time_slot` | `null` \| `string` | Time slot for the daily maximum usage percentage. | `-` |
| `update_datetime` | `string` | Supply-capability update timestamp converted to UTC RFC 3339. | `-` |
| `update_datetime_local` | `string` | Supply-capability update timestamp in JST RFC 3339. | `-` |
| `area_code` | `string` | Constant TEPCO area code. | `-` |
| `area_name_jp` | `string` | Japanese TEPCO service area name. | `-` |
| `area_name_en` | `string` | English TEPCO service area name. | `-` |

#### Schema `jp.tepco.denkiyoho.PeakDemandForecast`
<a id="schema-jptepcodenkiyohopeakdemandforecast"></a>


##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | PeakDemandForecast |
| Namespace | jp.tepco.denkiyoho |
| Type | `record` |
| Doc | Daily peak demand forecast record from TEPCO Electricity Forecast. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `date` | `string` | Operating date in ISO 8601 calendar-date form. | `-` |
| `time` | `string` | Stable key time component; peak demand forecast uses _peak_forecast_. | `-` |
| `peak_demand_forecast_mw` | `double` | Forecast maximum demand converted from 万kW to MW. | `-` |
| `peak_demand_forecast_jp_unit_value` | `int` | Original forecast maximum demand value in 万kW. | `-` |
| `peak_time_slot` | `string` | Forecast maximum-demand time slot. | `-` |
| `update_datetime` | `string` | Peak-demand forecast update timestamp converted to UTC RFC 3339. | `-` |
| `update_datetime_local` | `string` | Peak-demand forecast update timestamp in JST RFC 3339. | `-` |
| `area_code` | `string` | Constant TEPCO area code. | `-` |
| `area_name_jp` | `string` | Japanese TEPCO service area name. | `-` |
| `area_name_en` | `string` | English TEPCO service area name. | `-` |

#### Schema `jp.tepco.denkiyoho.DemandActual`
<a id="schema-jptepcodenkiyohodemandactual"></a>


##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DemandActual |
| Namespace | jp.tepco.denkiyoho |
| Type | `record` |
| Doc | Actual electricity demand record from TEPCO Electricity Forecast. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `date` | `string` | Operating date in ISO 8601 calendar-date form. | `-` |
| `time` | `string` | JST HH:MM clock time and stable key component. | `-` |
| `datetime` | `string` | Measurement timestamp converted to UTC RFC 3339. | `-` |
| `datetime_local` | `string` | Measurement timestamp in JST RFC 3339. | `-` |
| `actual_demand_mw` | `double` | Actual electricity demand converted from 万kW to MW. | `-` |
| `actual_demand_jp_unit_value` | `int` | Original actual demand value in 万kW. | `-` |
| `solar_generation_mw` | `null` \| `double` | Solar generation converted from 万kW to MW for five-minute rows. | `-` |
| `solar_generation_jp_unit_value` | `null` \| `int` | Original solar generation value in 万kW for five-minute rows. | `-` |
| `solar_share_pct` | `null` \| `double` | Solar generation percentage of electricity usage for five-minute rows. | `-` |
| `usage_pct` | `null` \| `double` | Usage percentage for hourly rows. | `-` |
| `supply_capacity_mw` | `null` \| `double` | Supply capacity converted from 万kW to MW for hourly rows. | `-` |
| `supply_capacity_jp_unit_value` | `null` \| `int` | Original supply capacity value in 万kW for hourly rows. | `-` |
| `area_code` | `string` | Constant TEPCO area code. | `-` |

#### Schema `jp.tepco.denkiyoho.DemandForecast`
<a id="schema-jptepcodenkiyohodemandforecast"></a>


##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DemandForecast |
| Namespace | jp.tepco.denkiyoho |
| Type | `record` |
| Doc | Hourly forecast electricity demand record from TEPCO Electricity Forecast. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `date` | `string` | Operating date in ISO 8601 calendar-date form. | `-` |
| `time` | `string` | JST HH:MM clock time and stable key component. | `-` |
| `datetime` | `string` | Forecast timestamp converted to UTC RFC 3339. | `-` |
| `datetime_local` | `string` | Forecast timestamp in JST RFC 3339. | `-` |
| `forecast_demand_mw` | `double` | Forecast demand converted from 万kW to MW. | `-` |
| `forecast_demand_jp_unit_value` | `int` | Original forecast demand value in 万kW. | `-` |
| `usage_pct` | `null` \| `double` | Usage percentage for hourly rows. | `-` |
| `supply_capacity_mw` | `null` \| `double` | Supply capacity converted from 万kW to MW for hourly rows. | `-` |
| `supply_capacity_jp_unit_value` | `null` \| `int` | Original supply capacity value in 万kW for hourly rows. | `-` |
| `area_code` | `string` | Constant TEPCO area code. | `-` |
