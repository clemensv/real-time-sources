# TEPCO Denki Yoho Bridge Events

This document describes the events emitted by the TEPCO Electricity Forecast bridge.

- [JP.TEPCO.Denkiyoho](#message-group-jptepcodenkiyoho)
  - [jp.tepco.denkiyoho.SupplyCapacity](#message-jptepcodenkiyohosupplycapacity)
  - [jp.tepco.denkiyoho.PeakDemandForecast](#message-jptepcodenkiyohopeakdemandforecast)
  - [jp.tepco.denkiyoho.DemandActual](#message-jptepcodenkiyohodemandactual)
  - [jp.tepco.denkiyoho.DemandForecast](#message-jptepcodenkiyohodemandforecast)

---

## Message Group: JP.TEPCO.Denkiyoho
---
### Message: jp.tepco.denkiyoho.SupplyCapacity
*Daily TEPCO Electricity Forecast supply capability reference record for the Tokyo service area.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.TEPCO.Denkiyoho.SupplyCapacity` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

#### Schema:
##### Object: SupplyCapacity
*Daily reference schema for TEPCO Electricity Forecast supply capability and daily maximum-usage summary metadata. The source CSV is Shift-JIS encoded and section 1 reports peak supply capacity, reserve margin, usage percentage, and update time for the Tokyo Electric Power Company service area.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `date` | *string* | - | `True` | Service date for TEPCO's Electricity Forecast daily CSV in local Tokyo time, normalized from the DATE column to ISO 8601 calendar-date form (YYYY-MM-DD). This date is a stable key component for all records from the same operating day. |
| `time` | *string* | - | `True` | Stable subject and Kafka key time component. Supply capacity is daily reference data rather than a point-in-time demand measurement, so the bridge sets this field to the sentinel value _supply_capacity_ while using the same jp.tepco.denkiyoho/{date}/{time} key model as demand events. |
| `peak_supply_capacity_mw` | *double* | MW | `True` | Peak-time available supply capability for the Tokyo service area shown by TEPCO as ピーク時供給力(万kW). The bridge converts the published 10,000-kilowatt unit to megawatts by multiplying the source value by 10. |
| `peak_supply_capacity_jp_unit_value` | *int32* | 10MW (万kW) | `True` | Original integer value from TEPCO's ピーク時供給力(万kW) header field. TEPCO publishes demand and supply values in 万kW, where one unit is 10,000 kilowatts, equal to 10 megawatts. |
| `peak_time_slot` | *string* | - | `True` | Local Japan Standard Time hour range from TEPCO's section 1 時間帯 column indicating the peak supply-capability time slot, normalized to an ASCII hyphen such as 13:00-14:00. |
| `peak_reserve_margin_pct` | *double* | percent (%) | `True` | Peak-time reserve margin percentage from TEPCO's section 1 ピーク時予備率(%) column for the published peak supply-capability slot. |
| `peak_usage_pct` | *double* | percent (%) | `True` | Peak-time usage percentage from TEPCO's section 1 ピーク時使用率(%) column for the published peak supply-capability slot. |
| `daily_max_usage_pct` | *double* (optional) | percent (%) | `True` | Daily maximum usage percentage from TEPCO's section 4 最大使用率(%) summary row. The field is null when that section is absent or blank in the CSV. |
| `daily_max_usage_time_slot` | *string* (optional) | - | `True` | Local Japan Standard Time hour range from TEPCO's section 4 時間帯 column for the daily maximum usage percentage, normalized to an ASCII hyphen such as 4:00-5:00. The field is null when that section is absent or blank. |
| `update_datetime` | *string* | - | `True` | Section 1 supply-capability information update timestamp converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp. TEPCO publishes the date and time in 供給力情報更新日 and 供給力情報更新時刻. |
| `update_datetime_local` | *string* | - | `True` | Section 1 supply-capability information update timestamp in Japan Standard Time serialized as an RFC 3339 timestamp with +09:00 offset, built from TEPCO's 供給力情報更新日 and 供給力情報更新時刻 columns. |
| `area_code` | *string* | - | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. |
| `area_name_jp` | *string* | - | `True` | Japanese name of the TEPCO Power Grid service area used by the Electricity Forecast page: 東京電力エリア. The page defines this as Tokyo plus Kanagawa, Saitama, Chiba, Tochigi, Gunma, Ibaraki, Yamanashi, and the portion of Shizuoka east of the Fujikawa River. |
| `area_name_en` | *string* | - | `True` | English display name for the TEPCO service territory covered by the Electricity Forecast page: TEPCO Service Area (Kanto). |
---
### Message: jp.tepco.denkiyoho.PeakDemandForecast
*Daily TEPCO Electricity Forecast maximum-demand forecast record for the Tokyo service area.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.TEPCO.Denkiyoho.PeakDemandForecast` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

#### Schema:
##### Object: PeakDemandForecast
*Daily reference schema for TEPCO Electricity Forecast section 2 peak-demand forecast metadata for the Tokyo Electric Power Company service area.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `date` | *string* | - | `True` | Operating date for TEPCO's section 2 peak-demand forecast, normalized from 予想最大電力情報更新日 with the CSV update year to ISO 8601 calendar-date form (YYYY-MM-DD). This is the stable date key component. |
| `time` | *string* | - | `True` | Stable subject and Kafka key time component for the section 2 peak-demand forecast. The bridge sets this field to the sentinel value _peak_forecast_ so the daily peak forecast shares the same jp.tepco.denkiyoho/{date}/{time} key model as the other TEPCO events without pretending to be an hourly measurement. |
| `peak_demand_forecast_mw` | *double* | MW | `True` | Forecast maximum electricity demand for the Tokyo service area from TEPCO's section 2 予想最大電力(万kW) row, converted from 万kW to megawatts by multiplying by 10. |
| `peak_demand_forecast_jp_unit_value` | *int32* | 10MW (万kW) | `True` | Original integer peak-demand forecast value from TEPCO's section 2 予想最大電力(万kW) field. |
| `peak_time_slot` | *string* | - | `True` | Local Japan Standard Time hour range from TEPCO's section 2 時間帯 column indicating when the forecast maximum demand is expected, normalized to an ASCII hyphen such as 13:00-14:00. |
| `update_datetime` | *string* | - | `True` | Section 2 peak-demand forecast information update timestamp converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp. TEPCO publishes the date and time in 予想最大電力情報更新日 and 予想最大電力情報更新時刻. |
| `update_datetime_local` | *string* | - | `True` | Section 2 peak-demand forecast information update timestamp in Japan Standard Time serialized as an RFC 3339 timestamp with +09:00 offset, built from TEPCO's 予想最大電力情報更新日 and 予想最大電力情報更新時刻 columns. |
| `area_code` | *string* | - | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. |
| `area_name_jp` | *string* | - | `True` | Japanese name of the TEPCO Power Grid service area used by the Electricity Forecast page: 東京電力エリア. The page defines this as Tokyo plus Kanagawa, Saitama, Chiba, Tochigi, Gunma, Ibaraki, Yamanashi, and the portion of Shizuoka east of the Fujikawa River. |
| `area_name_en` | *string* | - | `True` | English display name for the TEPCO service territory covered by the Electricity Forecast page: TEPCO Service Area (Kanto). |
---
### Message: jp.tepco.denkiyoho.DemandActual
*Actual electricity demand record from TEPCO Electricity Forecast for the Tokyo service area, emitted for hourly rows with section 3 context and for five-minute rows with section 5 solar context.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.TEPCO.Denkiyoho.DemandActual` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

#### Schema:
##### Object: DemandActual
*Telemetry schema for actual TEPCO electricity demand in the Tokyo Electric Power Company service area. Hourly rows from section 3 carry usage and supply-capacity context, while five-minute rows from section 5 carry solar generation context.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `date` | *string* | - | `True` | Operating date from the DATE column in TEPCO's hourly actual-demand section or five-minute actual-demand section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD). This is the first stable key component. |
| `time` | *string* | - | `True` | Local Japan Standard Time clock time from the TIME column in TEPCO's hourly or five-minute actual-demand section, normalized to zero-padded HH:MM form. This is the second stable key component. |
| `datetime` | *string* | - | `True` | Combined DATE and TIME converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp for cross-region analytics. |
| `datetime_local` | *string* | - | `True` | Combined DATE and TIME serialized as an RFC 3339 timestamp with +09:00 offset for the Japan Standard Time instant represented by the TEPCO CSV row. |
| `actual_demand_mw` | *double* | MW | `True` | Actual electricity demand for the Tokyo service area, converted to megawatts from TEPCO's 当日実績(万kW) hourly column or 当日実績(5分間隔値)(万kW) five-minute column by multiplying by 10. |
| `actual_demand_jp_unit_value` | *int32* | 10MW (万kW) | `True` | Original integer value from TEPCO's 当日実績(万kW) hourly column or 当日実績(5分間隔値)(万kW) five-minute column. Rows with 0 or blank actual-demand values are future or unavailable measurements and are skipped by the bridge. |
| `solar_generation_mw` | *double* (optional) | MW | `True` | Solar generation actual value converted to megawatts from TEPCO's section 5 太陽光発電実績(5分間隔値)(万kW) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar cell. |
| `solar_generation_jp_unit_value` | *int32* (optional) | 10MW (万kW) | `True` | Original integer solar generation actual value from TEPCO's section 5 太陽光発電実績(5分間隔値)(万kW) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar cell. |
| `solar_share_pct` | *double* (optional) | percent (%) | `True` | Solar generation percentage of electricity usage from TEPCO's section 5 太陽光発電量(電力使用量に対する割合)(%) column. The field is null for hourly section 3 rows and for five-minute rows where TEPCO publishes an empty solar-share cell. |
| `usage_pct` | *double* (optional) | percent (%) | `True` | Usage percentage from TEPCO's hourly section 3 使用率(%) column. This field is populated only for hourly-cadence DemandActual rows derived from section 3; it is null for five-minute rows derived from section 5. TEPCO may leave future-hour usage blank until actual demand is available. |
| `supply_capacity_mw` | *double* (optional) | MW | `True` | Available supply capacity converted to megawatts from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence rows derived from section 3; it is null for five-minute rows derived from section 5. |
| `supply_capacity_jp_unit_value` | *int32* (optional) | 10MW (万kW) | `True` | Original integer supply-capacity value from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence rows derived from section 3; it is null for five-minute rows derived from section 5. |
| `area_code` | *string* | - | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. |
---
### Message: jp.tepco.denkiyoho.DemandForecast
*Hourly electricity demand forecast record from TEPCO Electricity Forecast for the Tokyo service area.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.TEPCO.Denkiyoho.DemandForecast` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.tepco.denkiyoho/{date}/{time}` |

#### Schema:
##### Object: DemandForecast
*Hourly telemetry schema for TEPCO electricity demand forecasts in the Tokyo Electric Power Company service area, including usage and supply-capacity context from section 3.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `date` | *string* | - | `True` | Operating date from the DATE column in TEPCO's hourly same-day forecast section, normalized to ISO 8601 calendar-date form (YYYY-MM-DD). This is the first stable key component. |
| `time` | *string* | - | `True` | Local Japan Standard Time clock hour from the TIME column in TEPCO's hourly forecast section, normalized to zero-padded HH:MM form. This is the second stable key component. |
| `datetime` | *string* | - | `True` | Combined DATE and TIME converted from Japan Standard Time to UTC and serialized as an RFC 3339 timestamp for cross-region analytics. |
| `datetime_local` | *string* | - | `True` | Combined DATE and TIME serialized as an RFC 3339 timestamp with +09:00 offset for the Japan Standard Time instant represented by the TEPCO CSV row. |
| `forecast_demand_mw` | *double* | MW | `True` | Hourly forecast electricity demand for the Tokyo service area, converted to megawatts from TEPCO's section 3 予測値(万kW) column by multiplying by 10. |
| `forecast_demand_jp_unit_value` | *int32* | 10MW (万kW) | `True` | Original integer value from TEPCO's section 3 予測値(万kW) hourly forecast column. The bridge uses this value in forecast de-duplication so revised forecasts for the same date and hour are emitted again. |
| `usage_pct` | *double* (optional) | percent (%) | `True` | Usage percentage from TEPCO's hourly section 3 使用率(%) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3 and can be null when TEPCO leaves future-hour usage blank until actual demand is available. |
| `supply_capacity_mw` | *double* (optional) | MW | `True` | Available supply capacity converted to megawatts from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3. |
| `supply_capacity_jp_unit_value` | *int32* (optional) | 10MW (万kW) | `True` | Original integer supply-capacity value from TEPCO's hourly section 3 供給力(万kW) column. This field is populated only for hourly-cadence DemandForecast rows derived from section 3. |
| `area_code` | *string* | - | `True` | Constant service-area code TEPCO assigned by this bridge for the Tokyo Electric Power Company service area covered by the Electricity Forecast page. |
