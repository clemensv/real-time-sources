# JMA Bosai Volcanic Warnings and Eruptions Events

This source bridges the Japan Meteorological Agency (JMA) Bosai volcano feeds to Kafka-compatible endpoints as structured CloudEvents. It polls public, unauthenticated JMA endpoints for active volcanic warnings, eruption observations, and the volcano reference catalog.

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `JP.JMA.Volcano.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.JMA.Volcano`](#messagegroup-jpjmavolcano) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `jma-bosai-volcano` |
| Kafka key | `jp.jma.volcano/{volcano_code}` |
| Deployed | False |

## Messagegroups

### Messagegroup `JP.JMA.Volcano`
<a id="messagegroup-jpjmavolcano"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.JMA.Volcano.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `JP.JMA.Volcano.Volcano`
<a id="message-jpjmavolcanovolcano"></a>

JMA Bosai volcano catalog reference data emitted at startup and on monthly refresh.

| Field | Value |
| --- | --- |
| Name | Volcano |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.jma.volcano.jstruct/schemas/jp.jma.volcano.Volcano`](#schema-jpjmavolcanovolcano) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Volcano.Volcano` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.volcano/{volcano_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Volcano.Kafka` | `KAFKA` | topic `jma-bosai-volcano`; key `jp.jma.volcano/{volcano_code}` |

#### Message `JP.JMA.Volcano.VolcanicWarning`
<a id="message-jpjmavolcanovolcanicwarning"></a>

JMA Bosai active volcanic warning or forecast for a target volcano.

| Field | Value |
| --- | --- |
| Name | VolcanicWarning |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.jma.volcano.jstruct/schemas/jp.jma.volcano.VolcanicWarning`](#schema-jpjmavolcanovolcanicwarning) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Volcano.VolcanicWarning` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.volcano/{volcano_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Volcano.Kafka` | `KAFKA` | topic `jma-bosai-volcano`; key `jp.jma.volcano/{volcano_code}` |

#### Message `JP.JMA.Volcano.VolcanicEruption`
<a id="message-jpjmavolcanovolcaniceruption"></a>

JMA Bosai volcanic eruption observation report for a target volcano.

| Field | Value |
| --- | --- |
| Name | VolcanicEruption |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.jma.volcano.jstruct/schemas/jp.jma.volcano.VolcanicEruption`](#schema-jpjmavolcanovolcaniceruption) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Volcano.VolcanicEruption` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.volcano/{volcano_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Volcano.Kafka` | `KAFKA` | topic `jma-bosai-volcano`; key `jp.jma.volcano/{volcano_code}` |

## Schemagroups

### Schemagroup `jp.jma.volcano.jstruct`
<a id="schemagroup-jpjmavolcanojstruct"></a>

#### Schema `jp.jma.volcano.Volcano`
<a id="schema-jpjmavolcanovolcano"></a>

| Field | Value |
| --- | --- |
| Name | Volcano |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/volcano/Volcano` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Volcano`
<a id="schema-node-volcano"></a>

Reference record for one volcano in the JMA Bosai volcano catalog. JMA publishes the catalog to provide volcano names, coordinates, and whether the five-level eruption alert system operates for that volcano.

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/volcano/Volcano` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `volcano_code` | `string` | `True` | Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. | - | pattern=`^[0-9]{3}$` | - |
| `name_jp` | `string` | `True` | Japanese volcano name from the JMA Bosai volcano catalog. This is a display label and is not used as the stable identity because JMA warning records key volcanoes by code. | altnames=`{"json": "nameJp"}` | - | - |
| `name_en` | `string` | `True` | English volcano name from the JMA Bosai volcano catalog, used as a display label for international consumers. | altnames=`{"json": "nameEn"}` | - | - |
| `latitude` | `double` | `True` | Latitude of the volcano in WGS84 decimal degrees. The bridge converts JMA degree-and-minute coordinates when present, and otherwise forwards the Bosai catalog decimal latitude. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Longitude of the volcano in WGS84 decimal degrees. The bridge converts JMA degree-and-minute coordinates when present, and otherwise forwards the Bosai catalog decimal longitude. | unit=`degree` symbol=`°` | - | - |
| `elevation_m` | `union` | `False` | Volcano summit elevation in metres when supplied by the JMA catalog. Some Bosai catalog entries omit elevation, so the field is null in emitted events when JMA does not provide the value. | unit=`meter` symbol=`m` | - | - |
| `level_operation` | `boolean` | `True` | True when JMA marks the volcano as operating under the five-level eruption alert system. False means the volcano is represented by binary issued/not-issued volcanic warnings rather than a local five-level evacuation framework. | - | - | - |

#### Schema `jp.jma.volcano.VolcanicWarning`
<a id="schema-jpjmavolcanovolcanicwarning"></a>

| Field | Value |
| --- | --- |
| Name | VolcanicWarning |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/volcano/VolcanicWarning` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `VolcanicWarning`
<a id="schema-node-volcanicwarning"></a>

Active JMA Bosai volcanic warning or forecast for the target volcano. JMA eruption alert levels express the volcanic activity state, area needing caution, and expected disaster-prevention actions.

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/volcano/VolcanicWarning` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `volcano_code` | `string` | `True` | Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. | - | pattern=`^[0-9]{3}$` | - |
| `event_id` | `string` | `True` | JMA eventId from the Bosai warning record. The warning feed uses this identifier with reportDatetime to identify the active report for a target volcano. | altnames=`{"json": "eventId"}` | - | - |
| `report_datetime` | `datetime` | `True` | Report issue time converted from JMA local Japan Standard Time to UTC and serialized as an RFC3339 timestamp. This is the normalized time used for cross-region analytics. | altnames=`{"json": "reportDatetime"}` | - | - |
| `report_datetime_local` | `datetime` | `True` | Original JMA reportDatetime value in Japan Standard Time as published by the Bosai warning feed. Keeping the local timestamp preserves the official bulletin time shown by JMA. | - | - | - |
| `alert_level_code` | enum `['CODE_02', 'CODE_03', 'CODE_04', 'CODE_11', 'CODE_12', 'CODE_13', 'CODE_22', 'CODE_23', 'CODE_36', 'CODE_43', 'CODE_44', 'CODE_45', 'CODE_49']` | `True` | JMA volcanic warning code from warning.json. Enum symbols CODE_02, CODE_03, CODE_04, CODE_11, CODE_12, CODE_13, CODE_22, CODE_23, CODE_36, CODE_43, CODE_44, CODE_45, and CODE_49 correspond via altenums.json to observed live JMA wire codes 02, 03, 04, 11, 12, 13, 22, 23, 36, 43, 44, 45, and 49. JMA explains eruption alert levels as indicators combining volcanic activity state, area requiring caution, and expected disaster-prevention actions. Labels for CODE_11/CODE_12/CODE_13 are from JMA eruption alert level guidance; CODE_22/CODE_23/CODE_36 are target-volcano warning labels observed in live warning.json; CODE_02/CODE_03/CODE_04/CODE_43/CODE_44/CODE_45/CODE_49 labels are taken from live warning.json item name fields because the Bosai JSON feed publishes those public JMA labels directly. | altnames=`{"json": "code"}`<br>altenums=`{"json": {"CODE_02": "02", "CODE_03": "03", "CODE_04": "04", "CODE_11": "11", "CODE_12": "12", "CODE_13": "13", "CODE_22": "22", "CODE_23": "23", "CODE_36": "36", "CODE_43": "43", "CODE_44": "44", "CODE_45": "45", "CODE_49": "49"}, "lang:en": {"CODE_02": "Crater-area warning", "CODE_03": "Eruption warning for surrounding sea area", "CODE_04": "Eruption forecast: warning lifted", "CODE_11": "Active volcano; pay attention", "CODE_12": "Crater area restriction", "CODE_13": "Mountain access restriction", "CODE_22": "Crater vicinity danger", "CODE_23": "Mountain access danger", "CODE_36": "Surrounding waters warning for submarine or island volcanoes", "CODE_43": "Crater-area warning: entry restrictions and similar measures", "CODE_44": "Eruption warning for surrounding sea area: surrounding sea area warning", "CODE_45": "Active volcano; pay attention", "CODE_49": "Crater-area warning: caution around the crater"}, "lang:ja": {"CODE_02": "火口周辺警報", "CODE_03": "噴火警報（周辺海域）", "CODE_04": "噴火予報：警報解除", "CODE_11": "活動火山であることに留意", "CODE_12": "火口周辺規制", "CODE_13": "入山規制", "CODE_22": "火口周辺危険", "CODE_23": "入山危険", "CODE_36": "周辺海域警戒", "CODE_43": "火口周辺警報：入山規制等", "CODE_44": "噴火警報（周辺海域）：周辺海域警戒", "CODE_45": "活火山であることに留意", "CODE_49": "火口周辺警報：火口周辺警戒"}}` | - | - |
| `alert_level_name` | `string` | `True` | Japanese alert level or warning label from the target-volcano item, such as レベル３（入山規制）. JMA uses this text to communicate the public-facing warning level or restriction phrase. | altnames=`{"json": "name"}` | - | - |
| `previous_level_code` | `union` | `False` | Previous JMA alert level or warning code from lastCode when the warning feed provides one. It allows consumers to determine whether the current report raised, lowered, continued, or newly issued a level. | altnames=`{"json": "lastCode"}` | - | - |
| `condition` | enum `['ISSUED', 'RAISED', 'LOWERED', 'CONTINUED', 'SWITCHED', 'CANCELLED']` | `True` | Normalized lifecycle condition derived from the Japanese JMA condition text. 発表 is mapped to ISSUED, 引上げ to RAISED, 引下げ to LOWERED, 継続 to CONTINUED, 切替 to SWITCHED, and 解除 to CANCELLED so downstream consumers can compare reports without parsing Japanese status labels. | altnames=`{"json": "condition"}`<br>altenums=`{"lang:ja": {"CANCELLED": "解除", "CONTINUED": "継続", "ISSUED": "発表", "LOWERED": "引下げ", "RAISED": "引上げ", "SWITCHED": "切替"}}` | - | - |
| `info_type_jp` | `string` | `True` | Japanese volcanoInfos type label from the JMA feed. For emitted warning events the bridge uses the target-volcano section, normally 噴火警報・予報（対象火山）, because that section carries the stable volcano code identity. | altnames=`{"json": "type"}` | - | - |
| `area_codes` | array of `string` | `True` | List of JMA municipal or regional area codes from the outer areas field of the Bosai volcano report. JMA uses these area identifiers to indicate municipalities or regions affected by the volcanic warning or eruption information. | - | - | - |

#### Schema `jp.jma.volcano.VolcanicEruption`
<a id="schema-jpjmavolcanovolcaniceruption"></a>

| Field | Value |
| --- | --- |
| Name | VolcanicEruption |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/volcano/VolcanicEruption` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `VolcanicEruption`
<a id="schema-node-volcaniceruption"></a>

Discrete JMA Bosai volcanic eruption observation report for a target volcano. The live eruption.json endpoint was empty when reviewed, so structured eruption observation fields are based on JMA documentation for 噴火に関する火山観測報, which states that reports include eruption occurrence time, plume height, plume direction, and volcanic phenomena observed with the eruption; field names also align with observed JMA HTML bulletin examples.

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/volcano/VolcanicEruption` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `volcano_code` | `string` | `True` | Three-digit JMA volcano identifier used in the Bosai volcanic warning feeds and the volcano catalog. This is the stable domain key for the volcano and is used in the CloudEvents subject and Kafka key. | - | pattern=`^[0-9]{3}$` | - |
| `event_id` | `string` | `True` | JMA eventId from the Bosai eruption record. The bridge combines this identifier with reportDatetime for deduplication of eruption observations. | altnames=`{"json": "eventId"}` | - | - |
| `report_datetime` | `datetime` | `True` | Eruption report issue time converted from JMA local Japan Standard Time to UTC and serialized as an RFC3339 timestamp. | altnames=`{"json": "reportDatetime"}` | - | - |
| `report_datetime_local` | `datetime` | `True` | Original JMA reportDatetime value in Japan Standard Time as published in eruption.json. | - | - | - |
| `eruption_datetime` | `union` | `False` | Observed eruption time converted to UTC when the eruption feed contains a structured eruption or observation datetime. The field is null when JMA publishes only report issue time or free text. | - | - | - |
| `eruption_datetime_local` | `union` | `False` | Observed eruption time in the original Japan Standard Time representation when present in a JMA eruption item. The field is null when the live payload does not expose a separate occurrence time. | - | - | - |
| `eruption_type` | enum `['ERUPTION', 'EXPLOSION', 'CONTINUOUS_ERUPTION_CONTINUING', 'CONTINUOUS_ERUPTION_STOPPED', 'UNKNOWN']` | `False` | Normalized phenomenon name from JMA eruption observation bulletins. JMA documentation says the report carries the phenomenon name, with examples including eruption and continuous-eruption state changes; null means the live JSON item did not expose a recognizable phenomenon name. | altenums=`{"lang:ja": {"CONTINUOUS_ERUPTION_CONTINUING": "連続噴火継続", "CONTINUOUS_ERUPTION_STOPPED": "連続噴火停止", "ERUPTION": "噴火", "EXPLOSION": "爆発", "UNKNOWN": "不明"}}` | - | - |
| `crater_name` | `union` | `False` | Japanese crater name from the eruption observation report when JMA identifies the crater, such as 南岳山頂火口 in JMA bulletin examples. Null means the eruption JSON item or text did not include a crater label. | - | - | - |
| `colored_plume_height_m` | `union` | `False` | Height in metres of the colored volcanic plume above the crater, corresponding to the 有色噴煙 field in JMA eruption observation bulletins. Null means no colored-plume height was published or parsed. | unit=`meter` symbol=`m` | - | - |
| `white_plume_height_m` | `union` | `False` | Height in metres of the white volcanic plume above the crater, corresponding to the 白色噴煙 field when JMA publishes it. Null means no white-plume height was published or parsed. | unit=`meter` symbol=`m` | - | - |
| `maximum_plume_height_since_start_m` | `union` | `False` | Maximum plume height in metres above the crater since the eruption began, corresponding to the JMA bulletin field 噴火開始以降の最高噴煙高度. Null means JMA did not publish this field for the observation. | unit=`meter` symbol=`m` | - | - |
| `plume_direction` | `union` | `False` | Japanese plume flow direction from the JMA 流向 field, for example 直上 or 東. Null means the eruption item did not provide a plume direction. | - | - | - |
| `ash_dispersal_direction` | `union` | `False` | Direction or area text for ash dispersal when the eruption observation describes ash movement separately from the plume-flow direction. Null means JMA did not publish a separate ash dispersal direction in the parsed item. | - | - | - |
| `pyroclastic_flow_observed` | `union` | `False` | True when the eruption observation text states that a pyroclastic flow (火砕流) was observed, false when the text explicitly states no pyroclastic flow, and null when the report does not mention pyroclastic-flow status. | - | - | - |
| `plume_amount_jp` | `union` | `False` | Japanese qualitative plume-amount label from JMA bulletin text, such as やや多量. Null means the observation did not include a plume-amount label. | - | - | - |
| `description` | `string` | `True` | Japanese free-text description assembled from the JMA eruption item fields such as description, text, name, title, or content. This preserves the official observational wording when the eruption feed carries discrete eruption observations. | - | - | - |
| `info_type_jp` | `union` | `False` | Japanese volcanoInfos section type from eruption.json when supplied by JMA. It identifies the official section in which the eruption observation was published. | altnames=`{"json": "type"}` | - | - |
| `area_codes` | array of `string` | `True` | List of JMA municipal or regional area codes from the outer areas field of the Bosai volcano report. JMA uses these area identifiers to indicate municipalities or regions affected by the volcanic warning or eruption information. | - | - | - |
