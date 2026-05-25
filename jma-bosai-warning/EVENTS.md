# JMA Bosai Weather Warnings + Tsunami Alerts Events

MQTT/5.0 transport variant for JMA Bosai weather warnings. Retained QoS-1 office reference records and non-retained QoS-1 warning events route by Romanized prefecture, severity, issuing office code, forecast area code, and fixed event name under alerts/jp/jma/jma-bosai-warning/... so wildcard subscribers can follow one prefecture, severity, office, or area without parsing Japanese administrative names.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 3 |
| Messagegroups | 3 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `JP.JMA.Warning.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.JMA.Warning`](#messagegroup-jpjmawarning) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `jma-bosai-warning` |
| Kafka key | `jp.jma.warning/{office_code}/{area_code}` |
| Deployed | False |

### Endpoint `JP.JMA.Tsunami.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.JMA.Tsunami`](#messagegroup-jpjmatsunami) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `jma-bosai-tsunami` |
| Kafka key | `jp.jma.tsunami/{event_id}/{serial}` |
| Deployed | False |

### Endpoint `JP.JMA.Warning.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`JP.JMA.Warning.mqtt`](#messagegroup-jpjmawarningmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `JP.JMA.Warning`
<a id="messagegroup-jpjmawarning"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.JMA.Warning.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `JP.JMA.Warning.Office`
<a id="message-jpjmawarningoffice"></a>

JMA Bosai warning office reference data from area.json offices.

| Field | Value |
| --- | --- |
| Name | Office |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Warning.jstruct/schemas/JP.JMA.Warning.Office`](#schema-jpjmawarningoffice) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Warning.Office` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.warning/{office_code}/{area_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Warning.Kafka` | `KAFKA` | topic `jma-bosai-warning`; key `jp.jma.warning/{office_code}/{area_code}` |

#### Message `JP.JMA.Warning.WeatherWarning`
<a id="message-jpjmawarningweatherwarning"></a>

JMA Bosai weather warning/advisory telemetry for one forecast area within an office bulletin.

| Field | Value |
| --- | --- |
| Name | WeatherWarning |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Warning.jstruct/schemas/JP.JMA.Warning.WeatherWarning`](#schema-jpjmawarningweatherwarning) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Warning.WeatherWarning` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.warning/{office_code}/{area_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Warning.Kafka` | `KAFKA` | topic `jma-bosai-warning`; key `jp.jma.warning/{office_code}/{area_code}` |

### Messagegroup `JP.JMA.Tsunami`
<a id="messagegroup-jpjmatsunami"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.JMA.Tsunami.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `JP.JMA.Tsunami.TsunamiAlert`
<a id="message-jpjmatsunamitsunamialert"></a>

JMA Bosai active tsunami alert telemetry from list.json enriched with detail bulletin coastal forecasts.

| Field | Value |
| --- | --- |
| Name | TsunamiAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Tsunami.jstruct/schemas/JP.JMA.Tsunami.TsunamiAlert`](#schema-jpjmatsunamitsunamialert) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Tsunami.TsunamiAlert` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.tsunami/{event_id}/{serial}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Tsunami.Kafka` | `KAFKA` | topic `jma-bosai-tsunami`; key `jp.jma.tsunami/{event_id}/{serial}` |

### Messagegroup `JP.JMA.Warning.mqtt`
<a id="messagegroup-jpjmawarningmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for JMA Bosai weather warnings. Retained QoS-1 office reference records and non-retained QoS-1 warning events route by Romanized prefecture, severity, issuing office code, forecast area code, and fixed event name under alerts/jp/jma/jma-bosai-warning/... so wildcard subscribers can follow one prefecture, severity, office, or area without parsing Japanese administrative names. |
| Transport bindings | `JP.JMA.Warning.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `JP.JMA.Warning.mqtt.Office`
<a id="message-jpjmawarningmqttoffice"></a>

JMA Bosai warning office reference data from area.json offices.

| Field | Value |
| --- | --- |
| Name | Office |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Warning.jstruct/schemas/JP.JMA.Warning.Office`](#schema-jpjmawarningoffice) |
| Base message chain | `/messagegroups/JP.JMA.Warning/messages/JP.JMA.Warning.Office` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Warning.Office` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.warning/{office_code}/{area_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Warning.Mqtt` | `MQTT/5.0` | topic `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/{event}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/{event}` |
| QoS | 1 |
| Retain | True |

#### Message `JP.JMA.Warning.mqtt.WeatherWarning`
<a id="message-jpjmawarningmqttweatherwarning"></a>

JMA Bosai weather warning/advisory telemetry for one forecast area within an office bulletin.

| Field | Value |
| --- | --- |
| Name | WeatherWarning |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Warning.jstruct/schemas/JP.JMA.Warning.WeatherWarning`](#schema-jpjmawarningweatherwarning) |
| Base message chain | `/messagegroups/JP.JMA.Warning/messages/JP.JMA.Warning.WeatherWarning` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Warning.WeatherWarning` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.warning/{office_code}/{area_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Warning.Mqtt` | `MQTT/5.0` | topic `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/{event}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/{event}` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `JP.JMA.Warning.jstruct`
<a id="schemagroup-jpjmawarningjstruct"></a>

#### Schema `JP.JMA.Warning.Office`
<a id="schema-jpjmawarningoffice"></a>

| Field | Value |
| --- | --- |
| Name | Office |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/warning/Office` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| Type | `object` |

###### Object `Office`
<a id="schema-node-office"></a>

JMA warning office reference record from the Bosai area catalog offices section. These offices are the stable targetArea codes used by warning JSON endpoints and contextualize weather warning area telemetry.

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/warning/Office` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `office_code` | `string` | `True` | Six-digit JMA Bosai office code from area.json offices. This is the first stable key component for warning reference and telemetry events. | altnames=`{"jma-bosai": "offices key"}` | pattern=`^[0-9]{6}$` | - |
| `area_code` | `string` | `True` | Six-digit JMA Bosai office code repeated as the area component for office reference events so reference records use the same numeric warning subject and key shape as area warning telemetry. | - | pattern=`^[0-9]{6,7}$` | - |
| `name_jp` | `string` | `True` | Japanese office or warning-region name from area.json offices[].name, such as 東京都 or 宗谷地方. | - | - | - |
| `name_en` | `string` | `True` | English office or warning-region name from area.json offices[].enName, such as Tokyo or Soya. | - | - | - |
| `parent_office_code` | `union` | `True` | Parent JMA regional center code from area.json offices[].parent. Null is emitted only if the upstream catalog omits a parent. | - | pattern=`^[0-9]{6}$` | - |
| `office_type` | enum `['PREFECTURE', 'SUBREGION', 'OFFICE']` | `True` | Normalized office class. PREFECTURE is used for standard prefectural offices, SUBREGION for Hokkaido/Okinawa-style regional warning offices, and OFFICE for other JMA issuing-office catalog entries. | - | - | - |
| `prefecture` | `string` | `True` | ASCII-safe Romanized prefecture or JMA warning subregion slug derived from the JMA office code/name for MQTT topic routing. Japanese administrative names are preserved separately in name_jp/area_name. | - | pattern=`^[a-z0-9][a-z0-9-]*$` | - |
| `severity` | enum `['REFERENCE', 'NONE', 'ADVISORY', 'WARNING', 'EMERGENCY_WARNING']` | `True` | MQTT topic severity axis. Office REFERENCE records emit REFERENCE; weather warning records emit the highest normalized active warning severity. | - | - | - |
| `event` | enum `['office']` | `True` | Fixed MQTT topic event segment for retained office reference records. | - | - | - |

#### Schema `JP.JMA.Warning.WeatherWarning`
<a id="schema-jpjmawarningweatherwarning"></a>

| Field | Value |
| --- | --- |
| Name | WeatherWarning |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/warning/WeatherWarning` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| Type | `object` |

###### Object `WeatherWarning`
<a id="schema-node-weatherwarning"></a>

JMA Bosai weather warning/advisory state for one office targetArea and one inner forecast area. The bridge emits one record per (office_code, area_code, report_datetime) change and includes all warning items currently published for that area.

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/warning/WeatherWarning` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `prefecture` | `string` | `True` | ASCII-safe Romanized prefecture or JMA warning subregion slug derived from the JMA office code/name for MQTT topic routing. Japanese administrative names are preserved separately in name_jp/area_name. | - | pattern=`^[a-z0-9][a-z0-9-]*$` | - |
| `severity` | enum `['REFERENCE', 'NONE', 'ADVISORY', 'WARNING', 'EMERGENCY_WARNING']` | `True` | MQTT topic severity axis. Weather warning records emit the highest normalized warning severity present in the area bulletin; retained office REFERENCE records use REFERENCE on the same shared axis. | - | - | - |
| `office_code` | `string` | `True` | Six-digit JMA Bosai office targetArea code used in the warning/{office_code}.json endpoint. This is the first stable key component. | altnames=`{"jma-bosai": "targetArea"}` | pattern=`^[0-9]{6}$` | - |
| `area_code` | `string` | `True` | JMA inner forecast-area code from timeSeries areas[].code. This is the second stable key component for weather warning telemetry. | altnames=`{"jma-bosai": "timeSeries[].areas[].code"}` | pattern=`^[0-9]{6,7}$` | - |
| `event` | enum `['warning']` | `True` | Fixed MQTT topic event segment for JMA Bosai weather warning state records. | - | - | - |
| `area_name` | `string` | `True` | Japanese inner forecast-area name from the warning payload when present or from area.json class catalogs when the payload only carries a code. | - | - | - |
| `report_datetime` | `datetime` | `True` | JMA report publication time converted to an RFC3339 UTC timestamp. JMA publishes reportDatetime with a local Japan time offset. | altnames=`{"jma-bosai": "reportDatetime"}` | - | - |
| `report_datetime_local` | `datetime` | `True` | Original JMA reportDatetime timestamp preserving the upstream local offset, normally Japan Standard Time (+09:00). | altnames=`{"jma-bosai": "reportDatetime"}` | - | - |
| `headline_text` | `union` | `True` | Japanese free-text headline from headlineText summarizing areas and hazards requiring attention. Null is emitted when JMA omits the headline. | altnames=`{"jma-bosai": "headlineText"}` | - | - |
| `warnings` | array of [object `WarningItem`](#schema-node-warningitem) | `True` | All JMA warning/advisory items published for the inner area in this bulletin. WarningItem is intentionally defined inline to avoid duplicate schema definitions during Avro and producer generation. | altnames=`{"jma-bosai": "warnings"}` | - | - |
| `time_defines` | array of `datetime` | `True` | Time definition values from the warning timeSeries converted to RFC3339 UTC timestamps. The original JMA array describes the valid or forecast times associated with the warning area block. | altnames=`{"jma-bosai": "timeSeries[].timeDefines"}` | - | - |

###### Object `WarningItem`
<a id="schema-node-warningitem"></a>

Single JMA warning/advisory item for an inner forecast area. JMA warning area entries may either carry a hazard code plus status, or carry only the status 発表警報・注意報はなし when no warnings or advisories are in effect.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `code` | `union` | `False` | JMA weather warning category code from warnings[].code when a hazard is present. Null is emitted for JMA no-warning items such as {status: 発表警報・注意報はなし} that intentionally omit a code. | altnames=`{"jma-bosai": "warnings[].code"}`<br>altenums=`{"english_label": {"03": "Heavy rain", "04": "Flood", "05": "Storm", "06": "Snow storm", "07": "Heavy snow", "08": "High waves", "10": "Thunderstorm", "12": "Strong wind", "13": "Snow and wind", "14": "Dense fog", "15": "Dry air", "16": "Avalanche", "17": "Ice accretion", "18": "Snow accretion", "19": "Snow melt", "20": "Storm surge", "21": "Low temperature", "22": "Frost", "23": "Ice and snow accretion", "24": "Heavy rain and flood", "25": "Heavy rain and strong wind", "32": "Emergency heavy rain warning", "33": "Emergency heavy snow warning", "35": "Emergency storm warning", "36": "Emergency snow storm warning", "37": "Emergency high wave warning", "38": "Emergency storm surge warning", "W": "Advisory or warning aggregate"}, "jma_label": {"03": "大雨", "04": "洪水", "05": "暴風", "06": "暴風雪", "07": "大雪", "08": "波浪", "10": "雷", "12": "強風", "13": "風雪", "14": "濃霧", "15": "乾燥", "16": "なだれ", "17": "着氷", "18": "着雪", "19": "融雪", "20": "高潮", "21": "低温", "22": "霜", "23": "着氷・着雪", "24": "大雨・洪水", "25": "大雨・強風", "32": "大雨特別警報", "33": "大雪特別警報", "35": "暴風特別警報", "36": "暴風雪特別警報", "37": "波浪特別警報", "38": "高潮特別警報", "W": "注意報・警報"}}` | pattern=`^(03\\|04\\|05\\|06\\|07\\|08\\|10\\|12\\|13\\|14\\|15\\|16\\|17\\|18\\|19\\|20\\|21\\|22\\|23\\|24\\|25\\|32\\|33\\|35\\|36\\|37\\|38\\|W)$` | - |
| `code_description_jp` | `string` | `True` | Japanese hazard name corresponding to the JMA warning code, or 発表警報・注意報はなし for the upstream no-warning status item. | - | - | - |
| `code_description_en` | `string` | `True` | English hazard name corresponding to the JMA warning code, or No warnings or advisories for the upstream no-warning status item. | - | - | - |
| `status` | enum `['ISSUED', 'CONTINUED', 'CANCELLED', 'NO_WARNINGS_OR_ADVISORIES', 'WARNING', 'ADVISORY', 'EMERGENCY_WARNING']` | `True` | Normalized status or alert class for the JMA warning item. Values preserve the documented JMA status set using Python/Avro-safe symbols; lang:ja altenums carries the original JMA labels including 発表警報・注意報はなし. | altenums=`{"lang:en": {"ADVISORY": "Advisory", "CANCELLED": "Cancelled", "CONTINUED": "Continued", "EMERGENCY_WARNING": "Emergency Warning", "ISSUED": "Issued", "NO_WARNINGS_OR_ADVISORIES": "No warnings or advisories", "WARNING": "Warning"}, "lang:ja": {"ADVISORY": "注意報", "CANCELLED": "解除", "CONTINUED": "継続", "EMERGENCY_WARNING": "特別警報", "ISSUED": "発表", "NO_WARNINGS_OR_ADVISORIES": "発表警報・注意報はなし", "WARNING": "警報"}}` | - | - |
| `severity` | enum `['NONE', 'ADVISORY', 'WARNING', 'EMERGENCY_WARNING']` | `True` | Normalized severity derived from the JMA status text and special-warning codes. NONE represents 発表警報・注意報はなし, ADVISORY represents 注意報-level notices, WARNING represents 警報/発表/継続 items, and EMERGENCY_WARNING represents 特別警報 or special-warning category codes 32-38. | - | - | - |

### Schemagroup `JP.JMA.Tsunami.jstruct`
<a id="schemagroup-jpjmatsunamijstruct"></a>

#### Schema `JP.JMA.Tsunami.TsunamiAlert`
<a id="schema-jpjmatsunamitsunamialert"></a>

| Field | Value |
| --- | --- |
| Name | TsunamiAlert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/warning/TsunamiAlert` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| Type | `object` |

###### Object `TsunamiAlert`
<a id="schema-node-tsunamialert"></a>

Active JMA Bosai tsunami alert list entry enriched with detail bulletin data when available. The record is keyed by JMA event id and bulletin serial so issued, corrected, and cancelled alert revisions remain distinct stream events; VTSE51/VTSE52 observation station data is embedded as observations on the same alert revision for a cleaner generated top-level dataclass model.

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/warning/TsunamiAlert` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `True` | Stable JMA tsunami event identifier copied from list.json eid and corresponding detail Head.EventID. This is the first stable key component. | altnames=`{"jma-bosai": "eid"}` | pattern=`^[0-9]{14}$` | - |
| `serial` | `integer` | `True` | JMA tsunami bulletin serial parsed from list.json ser or detail Head.Serial. This is the second stable key component. | altnames=`{"jma-bosai": "ser"}` | minimum=`0` | - |
| `info_type` | enum `['ISSUED', 'CORRECTED', 'CANCELLED']` | `True` | Normalized information type derived from JMA ift text: ISSUED for 発表, CORRECTED for 訂正, and CANCELLED for 取消. | altnames=`{"jma-bosai": "ift"}`<br>altenums=`{"jma_label": {"CANCELLED": "取消", "CORRECTED": "訂正", "ISSUED": "発表"}}` | - | - |
| `report_datetime` | `datetime` | `True` | JMA tsunami report publication time converted from list.json rdt to RFC3339 UTC. | altnames=`{"jma-bosai": "rdt"}` | - | - |
| `report_datetime_local` | `datetime` | `True` | Original JMA tsunami report publication timestamp from list.json rdt preserving the local offset. | altnames=`{"jma-bosai": "rdt"}` | - | - |
| `title_jp` | `string` | `True` | Japanese JMA tsunami bulletin title copied from list.json ttl. | - | - | - |
| `title_en` | `string` | `True` | English tsunami title generated from the known JMA title class when no English list title is present. | - | - | - |
| `bulletin_type` | `string` | `True` | JMA tsunami product code parsed from the detail JSON filename, such as VTSE41, VTSE51, or VTSE52. | altnames=`{"jma-bosai": "json"}` | - | - |
| `detail_url` | `uri` | `True` | Absolute URL for the JMA Bosai tsunami detail JSON referenced by list.json json. | altnames=`{"jma-bosai": "json"}` | - | - |
| `affected_coastal_regions` | array of [object `AffectedCoastalRegion`](#schema-node-affectedcoastalregion) | `True` | Coastal forecast regions and expected wave/arrival data parsed from VTSE41 tsunami detail bulletins. AffectedCoastalRegion is defined inline to avoid duplicate schema definitions during Avro and producer generation. | - | - | - |
| `observations` | array of [object `TsunamiObservation`](#schema-node-tsunamiobservation) | `True` | Observed tsunami station readings parsed from VTSE51/VTSE52 observed-wave detail bulletins. The bridge emits an empty array for forecast-only bulletins or when no station observations are present. | - | - | - |

###### Object `AffectedCoastalRegion`
<a id="schema-node-affectedcoastalregion"></a>

Coastal forecast region item parsed from a JMA tsunami detail bulletin when active tsunami information is available. It preserves region identity, per-region tsunami category, expected first-arrival time, and expected maximum wave height when those fields appear in VTSE detail JSON.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `code` | `string` | `True` | JMA tsunami coastal forecast region code from detail bulletin area entries. | - | pattern=`^[0-9]{3,7}$` | - |
| `name` | `string` | `True` | Japanese coastal forecast region name from the tsunami detail bulletin. | - | - | - |
| `category` | enum `['MAJOR_WARNING', 'WARNING', 'ADVISORY', 'FORECAST']` | `True` | Per-region tsunami forecast category from VTSE41 detail bulletins, normalized from JMA 大津波警報, 津波警報, 津波注意報, or 津波予報 text. | altenums=`{"lang:ja": {"ADVISORY": "津波注意報", "FORECAST": "津波予報", "MAJOR_WARNING": "大津波警報", "WARNING": "津波警報"}}` | - | - |
| `expected_max_wave_height_m` | `union` | `True` | Expected maximum tsunami wave height in meters parsed from JMA detail values. Null is emitted when the bulletin describes the height textually or omits it. | unit=`meter` symbol=`m` | minimum=`0` | - |
| `expected_arrival_datetime` | `union` | `True` | Expected first tsunami arrival time converted to RFC3339 UTC when available in the detail bulletin. | - | - | - |
| `expected_arrival_datetime_local` | `union` | `True` | Original expected first tsunami arrival time from the JMA detail bulletin preserving its local offset when available. | - | - | - |

###### Object `TsunamiObservation`
<a id="schema-node-tsunamiobservation"></a>

Observed tsunami station measurement parsed from JMA VTSE51/VTSE52 observed-wave bulletins and embedded in the alert revision that carries the same event id and serial. Keeping observations inside TsunamiAlert preserves one generated top-level dataclass and one {event_id}/{serial} Kafka identity for all tsunami bulletin revisions.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_code` | `union` | `True` | JMA observation station code from the observed tsunami bulletin when the station entry exposes a code; null is emitted for text-only station entries. | - | - | - |
| `station_name_jp` | `string` | `True` | Japanese tsunami observation station name from the observed-wave bulletin. | - | - | - |
| `station_name_en` | `union` | `True` | English observation station name when supplied by JMA or mapped by the bridge; null when the upstream bulletin only contains Japanese station text. | - | - | - |
| `observed_max_wave_height_m` | `union` | `True` | Observed maximum tsunami wave height at the station in meters. Null is emitted for qualitative or not-yet-available observed-wave entries. | unit=`meter` symbol=`m` | minimum=`0` | - |
| `observed_at` | `union` | `True` | Observed wave time converted to RFC3339 UTC when the station entry includes an observation time. | - | - | - |
| `observed_at_local` | `union` | `True` | Original observed wave time preserving the local offset when available in the station entry. | - | - | - |
| `arrival_status` | enum `['ESTIMATED', 'FIRST_WAVE_OBSERVED', 'MAX_WAVE_OBSERVED']` | `True` | Normalized observation lifecycle for station wave entries: ESTIMATED for expected or pending arrivals, FIRST_WAVE_OBSERVED when the first wave has arrived, and MAX_WAVE_OBSERVED when a maximum wave height is reported. | - | - | - |
