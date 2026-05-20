# JMA Bosai Volcano Events

This source emits structured JSON CloudEvents to one Kafka endpoint, `JP.JMA.Volcano.Kafka`, using key and subject `jp.jma.volcano/{volcano_code}`.

> Note: the volcano topic is intentionally keyed by `{volcano_code}` as a latest-state/compaction-style stream per volcano, unlike append-style quake feeds that key by event identifiers.

## Message group: JP.JMA.Volcano

### JP.JMA.Volcano.Volcano

Reference data from the JMA Bosai volcano catalog.

| Field | Type | Description |
| --- | --- | --- |
| `volcano_code` | string | Stable three-digit JMA volcano code. |
| `name_jp` | string | Japanese volcano name (`nameJp`). |
| `name_en` | string | English volcano name (`nameEn`). |
| `latitude` | double | WGS84 decimal latitude. |
| `longitude` | double | WGS84 decimal longitude. |
| `elevation_m` | double/null | Summit elevation in metres (`unit: meter`, `symbol: m`) when JMA supplies it. |
| `level_operation` | boolean | True when JMA operates the five-level alert system for the volcano. |

### JP.JMA.Volcano.VolcanicWarning

Active volcanic warning or forecast from `warning.json`.

| Field | Type | Description |
| --- | --- | --- |
| `volcano_code` | string | Stable three-digit JMA volcano code. |
| `event_id` | string | JMA `eventId`. |
| `report_datetime` | datetime | Report issue time converted to UTC from `reportDatetime`. |
| `report_datetime_local` | datetime | Original JST `reportDatetime`. |
| `alert_level_code` | enum/string | Observed JMA codes `02`, `03`, `04`, `11`, `12`, `13`, `22`, `23`, `36`, `43`, `44`, `45`, `49`; xreg enum symbols use `CODE_XX` with `altenums.json` for the wire code. |
| `alert_level_name` | string | Japanese public alert label from `name`. |
| `previous_level_code` | string/null | Previous `lastCode` value when present. |
| `condition` | enum | Normalized lifecycle: `ISSUED`, `RAISED`, `LOWERED`, `CONTINUED`, `SWITCHED`, or `CANCELLED` (`発表`, `引上げ`, `引下げ`, `継続`, `切替`, `解除`). |
| `info_type_jp` | string | JMA section type from `type`, normally `噴火警報・予報（対象火山）`. |
| `area_codes` | string[] | Affected JMA area codes from the outer record. |

### JP.JMA.Volcano.VolcanicEruption

Discrete eruption observation from `eruption.json`. The live endpoint was empty during review, so structured plume and phenomenon fields are based on JMA `噴火に関する火山観測報` documentation and published HTML bulletin examples.

| Field | Type | Description |
| --- | --- | --- |
| `volcano_code` | string | Stable three-digit JMA volcano code. |
| `event_id` | string | JMA `eventId`. |
| `report_datetime` | datetime | Report issue time converted to UTC from `reportDatetime`. |
| `report_datetime_local` | datetime | Original JST `reportDatetime`. |
| `eruption_datetime` | datetime/null | Structured eruption occurrence time in UTC when present. |
| `eruption_datetime_local` | datetime/null | Structured eruption occurrence time in JST when present. |
| `eruption_type` | enum/null | Normalized phenomenon: `ERUPTION`, `EXPLOSION`, `CONTINUOUS_ERUPTION_CONTINUING`, `CONTINUOUS_ERUPTION_STOPPED`, or `UNKNOWN`. |
| `crater_name` | string/null | Crater label such as `南岳山頂火口` when published. |
| `colored_plume_height_m` | double/null | Colored plume height above crater in metres (`unit: meter`, `symbol: m`). |
| `white_plume_height_m` | double/null | White plume height above crater in metres (`unit: meter`, `symbol: m`). |
| `maximum_plume_height_since_start_m` | double/null | Maximum plume height since eruption start in metres (`unit: meter`, `symbol: m`). |
| `plume_direction` | string/null | JMA plume flow direction (`流向`), for example `直上` or `東`. |
| `ash_dispersal_direction` | string/null | Separate ash dispersal direction text when published. |
| `pyroclastic_flow_observed` | boolean/null | Pyroclastic-flow status when explicitly mentioned. |
| `plume_amount_jp` | string/null | Japanese qualitative plume amount such as `やや多量`. |
| `description` | string | Japanese observation text from the eruption item. |
| `info_type_jp` | string/null | JMA eruption section type from `type` when present. |
| `area_codes` | string[] | Affected JMA area codes from the outer record. |
