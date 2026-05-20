# JMA Bosai Warning Events

This document describes the events emitted by the JMA Bosai weather warning and tsunami alert bridge.

- [JP.JMA.Warning](#message-group-jpjmawarning)
  - [JP.JMA.Warning.Office](#message-jpjmawarningoffice)
  - [JP.JMA.Warning.WeatherWarning](#message-jpjmawarningweatherwarning)
- [JP.JMA.Tsunami](#message-group-jpjmatsunami)
  - [JP.JMA.Tsunami.TsunamiAlert](#message-jpjmatsunamitsunamialert)

---

## Message Group: JP.JMA.Warning
---
### Message: JP.JMA.Warning.Office
*JMA Bosai warning office reference data from area.json offices.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.JMA.Warning.Office` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.warning/{office_code}/{area_code}` |

#### Schema:
##### Object: Office
*JMA warning office reference record from the Bosai area catalog offices section. These offices are the stable targetArea codes used by warning JSON endpoints and contextualize weather warning area telemetry.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `office_code` | *string* | - | `True` | Six-digit JMA Bosai office code from area.json offices. This is the first stable key component for warning reference and telemetry events. |
| `area_code` | *string* | - | `True` | Six-digit JMA Bosai office code repeated as the area component for office reference events so reference records use the same numeric warning subject and key shape as area warning telemetry. |
| `name_jp` | *string* | - | `True` | Japanese office or warning-region name from area.json offices[].name, such as 東京都 or 宗谷地方. |
| `name_en` | *string* | - | `True` | English office or warning-region name from area.json offices[].enName, such as Tokyo or Soya. |
| `parent_office_code` | *string* (optional) | - | `True` | Parent JMA regional center code from area.json offices[].parent. Null is emitted only if the upstream catalog omits a parent. |
| `office_type` | *string* | - | `True` | Normalized office class. PREFECTURE is used for standard prefectural offices, SUBREGION for Hokkaido/Okinawa-style regional warning offices, and OFFICE for other JMA issuing-office catalog entries. |
---
### Message: JP.JMA.Warning.WeatherWarning
*JMA Bosai weather warning/advisory telemetry for one forecast area within an office bulletin.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.JMA.Warning.WeatherWarning` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.warning/{office_code}/{area_code}` |

#### Schema:
##### Object: WeatherWarning
*JMA Bosai weather warning/advisory state for one office targetArea and one inner forecast area. The bridge emits one record per (office_code, area_code, report_datetime) change and includes all warning items currently published for that area.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `office_code` | *string* | - | `True` | Six-digit JMA Bosai office targetArea code used in the warning/{office_code}.json endpoint. This is the first stable key component. |
| `area_code` | *string* | - | `True` | JMA inner forecast-area code from timeSeries areas[].code. This is the second stable key component for weather warning telemetry. |
| `area_name` | *string* | - | `True` | Japanese inner forecast-area name from the warning payload when present or from area.json class catalogs when the payload only carries a code. |
| `report_datetime` | *string* | - | `True` | JMA report publication time converted to an RFC3339 UTC timestamp. JMA publishes reportDatetime with a local Japan time offset. |
| `report_datetime_local` | *string* | - | `True` | Original JMA reportDatetime timestamp preserving the upstream local offset, normally Japan Standard Time (+09:00). |
| `headline_text` | *string* (optional) | - | `True` | Japanese free-text headline from headlineText summarizing areas and hazards requiring attention. Null is emitted when JMA omits the headline. |
| `warnings` | array of [Object WarningItem](#object-warningitem) | - | `True` | All JMA warning/advisory items published for the inner area in this bulletin. WarningItem is intentionally defined inline to avoid duplicate schema definitions during Avro and producer generation. |
| `time_defines` | array of *string* | - | `True` | Time definition values from the warning timeSeries converted to RFC3339 UTC timestamps. The original JMA array describes the valid or forecast times associated with the warning area block. |

---
##### Object: WarningItem
*Single JMA warning/advisory item for an inner forecast area. JMA warning area entries may either carry a hazard code plus status, or carry only the status 発表警報・注意報はなし when no warnings or advisories are in effect.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `code` | *string* (optional) | - | `False` | JMA weather warning category code from warnings[].code when a hazard is present. Null is emitted for JMA no-warning items such as {status: 発表警報・注意報はなし} that intentionally omit a code. |
| `code_description_jp` | *string* | - | `True` | Japanese hazard name corresponding to the JMA warning code, or 発表警報・注意報はなし for the upstream no-warning status item. |
| `code_description_en` | *string* | - | `True` | English hazard name corresponding to the JMA warning code, or No warnings or advisories for the upstream no-warning status item. |
| `status` | *string* | - | `True` | Normalized status or alert class for the JMA warning item. Values preserve the documented JMA status set using Python/Avro-safe symbols; lang:ja altenums carries the original JMA labels including 発表警報・注意報はなし. |
| `severity` | *string* | - | `True` | Normalized severity derived from the JMA status text and special-warning codes. NONE represents 発表警報・注意報はなし, ADVISORY represents 注意報-level notices, WARNING represents 警報/発表/継続 items, and EMERGENCY_WARNING represents 特別警報 or special-warning category codes 32-38. |
## Message Group: JP.JMA.Tsunami
---
### Message: JP.JMA.Tsunami.TsunamiAlert
*JMA Bosai active tsunami alert telemetry from list.json enriched with detail bulletin coastal forecasts.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `JP.JMA.Tsunami.TsunamiAlert` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.tsunami/{event_id}/{serial}` |

#### Schema:
##### Object: TsunamiAlert
*Active JMA Bosai tsunami alert list entry enriched with detail bulletin data when available. The record is keyed by JMA event id and bulletin serial so issued, corrected, and cancelled alert revisions remain distinct stream events; VTSE51/VTSE52 observation station data is embedded as observations on the same alert revision for a cleaner generated top-level dataclass model.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `event_id` | *string* | - | `True` | Stable JMA tsunami event identifier copied from list.json eid and corresponding detail Head.EventID. This is the first stable key component. |
| `serial` | *integer* | - | `True` | JMA tsunami bulletin serial parsed from list.json ser or detail Head.Serial. This is the second stable key component. |
| `info_type` | *string* | - | `True` | Normalized information type derived from JMA ift text: ISSUED for 発表, CORRECTED for 訂正, and CANCELLED for 取消. |
| `report_datetime` | *string* | - | `True` | JMA tsunami report publication time converted from list.json rdt to RFC3339 UTC. |
| `report_datetime_local` | *string* | - | `True` | Original JMA tsunami report publication timestamp from list.json rdt preserving the local offset. |
| `title_jp` | *string* | - | `True` | Japanese JMA tsunami bulletin title copied from list.json ttl. |
| `title_en` | *string* | - | `True` | English tsunami title generated from the known JMA title class when no English list title is present. |
| `bulletin_type` | *string* | - | `True` | JMA tsunami product code parsed from the detail JSON filename, such as VTSE41, VTSE51, or VTSE52. |
| `detail_url` | *string* | - | `True` | Absolute URL for the JMA Bosai tsunami detail JSON referenced by list.json json. |
| `affected_coastal_regions` | array of [Object AffectedCoastalRegion](#object-affectedcoastalregion) | - | `True` | Coastal forecast regions and expected wave/arrival data parsed from VTSE41 tsunami detail bulletins. AffectedCoastalRegion is defined inline to avoid duplicate schema definitions during Avro and producer generation. |
| `observations` | array of [Object TsunamiObservation](#object-tsunamiobservation) | - | `True` | Observed tsunami station readings parsed from VTSE51/VTSE52 observed-wave detail bulletins. The bridge emits an empty array for forecast-only bulletins or when no station observations are present. |

---
##### Object: AffectedCoastalRegion
*Coastal forecast region item parsed from a JMA tsunami detail bulletin when active tsunami information is available. It preserves region identity, per-region tsunami category, expected first-arrival time, and expected maximum wave height when those fields appear in VTSE detail JSON.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `code` | *string* | - | `True` | JMA tsunami coastal forecast region code from detail bulletin area entries. |
| `name` | *string* | - | `True` | Japanese coastal forecast region name from the tsunami detail bulletin. |
| `category` | *string* | - | `True` | Per-region tsunami forecast category from VTSE41 detail bulletins, normalized from JMA 大津波警報, 津波警報, 津波注意報, or 津波予報 text. |
| `expected_max_wave_height_m` | *double* (optional) | meter (m) | `True` | Expected maximum tsunami wave height in meters parsed from JMA detail values. Null is emitted when the bulletin describes the height textually or omits it. |
| `expected_arrival_datetime` | *string* (optional) | - | `True` | Expected first tsunami arrival time converted to RFC3339 UTC when available in the detail bulletin. |
| `expected_arrival_datetime_local` | *string* (optional) | - | `True` | Original expected first tsunami arrival time from the JMA detail bulletin preserving its local offset when available. |

---
##### Object: TsunamiObservation
*Observed tsunami station measurement parsed from JMA VTSE51/VTSE52 observed-wave bulletins and embedded in the alert revision that carries the same event id and serial. Keeping observations inside TsunamiAlert preserves one generated top-level dataclass and one {event_id}/{serial} Kafka identity for all tsunami bulletin revisions.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_code` | *string* (optional) | - | `True` | JMA observation station code from the observed tsunami bulletin when the station entry exposes a code; null is emitted for text-only station entries. |
| `station_name_jp` | *string* | - | `True` | Japanese tsunami observation station name from the observed-wave bulletin. |
| `station_name_en` | *string* (optional) | - | `True` | English observation station name when supplied by JMA or mapped by the bridge; null when the upstream bulletin only contains Japanese station text. |
| `observed_max_wave_height_m` | *double* (optional) | meter (m) | `True` | Observed maximum tsunami wave height at the station in meters. Null is emitted for qualitative or not-yet-available observed-wave entries. |
| `observed_at` | *string* (optional) | - | `True` | Observed wave time converted to RFC3339 UTC when the station entry includes an observation time. |
| `observed_at_local` | *string* (optional) | - | `True` | Original observed wave time preserving the local offset when available in the station entry. |
| `arrival_status` | *string* | - | `True` | Normalized observation lifecycle for station wave entries: ESTIMATED for expected or pending arrivals, FIRST_WAVE_OBSERVED when the first wave has arrived, and MAX_WAVE_OBSERVED when a maximum wave height is reported. |
