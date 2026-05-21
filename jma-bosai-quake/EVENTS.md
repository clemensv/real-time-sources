# JMA Bosai Earthquake Bridge Events

This document describes the CloudEvents emitted by the JMA Bosai earthquake bridge.

- [JP.JMA.Quake](#message-group-jpjmaquake)
  - [JP.JMA.Quake.EarthquakeReport](#message-jpjmaquakeearthquakereport)

---

## Message Group: JP.JMA.Quake

Kafka endpoint: `JP.JMA.Quake.Kafka`

- Topic: `jma-bosai-quake`
- Key template: `jp.jma.quake/{event_id}/{serial}`
- Envelope: CloudEvents 1.0 structured JSON

---

### Message: JP.JMA.Quake.EarthquakeReport

JMA Bosai earthquake and seismic intensity report header enriched with parsed hypocenter coordinates, prefecture and city intensity summaries, and tsunami-related comment interpretation from the detail bulletin when available.

#### CloudEvents Attributes

| Name | Type | Required | Value |
| --- | --- | --- | --- |
| `specversion` | `string` | yes | `1.0` |
| `type` | `string` | yes | `JP.JMA.Quake.EarthquakeReport` |
| `source` | `uritemplate` | yes | `{feedurl}` |
| `subject` | `uritemplate` | yes | `jp.jma.quake/{event_id}/{serial}` |
| `datacontenttype` | `string` | yes | `application/json` |

#### Schema: EarthquakeReport

Schema `$id`: `https://www.jma.go.jp/schemas/bosai/quake/EarthquakeReport`

| Field | Type | Description |
| --- | --- | --- |
| `event_id` | `string` | Stable JMA earthquake event id copied from `eid`; pattern `^[0-9]{14}$` (`YYYYMMDDHHMMSS`). |
| `report_id` | `string` | Composite `event_id + '_' + serial` report id. |
| `serial` | `integer` | JMA report serial parsed from `ser`. |
| `info_type` | enum string | `ISSUED`, `CORRECTED`, or `CANCELLED`, derived from `発表`, `訂正`, or `取消`. |
| `report_datetime` | RFC3339 UTC string | Report event time converted from `rdt` to UTC. |
| `report_datetime_local` | RFC3339 string | Original `rdt` timestamp with JMA's supplied local offset. |
| `control_datetime` | RFC3339 UTC string | JMA control timestamp from `ctt`, converted from JST to UTC; this is when the bulletin was published to the JMA distribution system and is distinct from `report_datetime`. |
| `control_datetime_local` | RFC3339 JST string | JMA control timestamp from `ctt`, preserving the Japan Standard Time offset. |
| `origin_datetime` | RFC3339 UTC string | Earthquake origin time converted from `at` to UTC. |
| `origin_datetime_local` | RFC3339 string | Original `at` timestamp with JMA's supplied local offset. |
| `title_jp` | `string` | Japanese bulletin title from `ttl`. |
| `title_en` | `string` or `null` | English bulletin title from `en_ttl`; null when the feed omits `en_ttl`, including some `震度速報`, `南海トラフ関連解説情報`, and `顕著な地震の震源要素更新のお知らせ` bulletins. |
| `epicenter_area_code` | `string` or `null` | JMA hypocenter/epicenter area code from `acd`; null for bulletin types that omit hypocenter metadata, including `震度速報`, `南海トラフ関連解説情報`, and `顕著な地震の震源要素更新のお知らせ`. |
| `epicenter_area_jp` | `string` or `null` | Japanese epicenter area name from `anm`; null for bulletin types that omit hypocenter metadata. |
| `epicenter_area_en` | `string` or `null` | English epicenter area name from `en_anm`; null for bulletin types that omit hypocenter metadata. |
| `latitude` | `double` or `null` | Hypocenter latitude parsed from the ISO 6709 `cod` coordinate; null when `cod` is absent. |
| `longitude` | `double` or `null` | Hypocenter longitude parsed from `cod`; null when `cod` is absent. |
| `depth_km` | `double` or `null` | Hypocenter depth in kilometres, parsed from `cod` metres and divided by 1000; range 0-700 km, null when `cod` is absent. |
| `magnitude` | `double` or `null` | Dimensionless JMA magnitude from `mag` on the JMA magnitude scale; null when the bulletin omits magnitude. |
| `max_intensity` | enum string or `null` | Maximum JMA seismic intensity (`1`, `2`, `3`, `4`, `5-`, `5+`, `6-`, `6+`, `7`) from `maxi`; null when no observed intensity summary is present. |
| `bulletin_type` | enum string | Detail product code parsed from `json`: `VXSE51`, `VXSE52`, `VXSE53`, `VXSE5k`, `VXSE61`, or `VYSE52`. |
| `detail_url` | URI string | Full URL of the detail JSON file. |
| `affected_prefectures` | array of `AffectedPrefecture` | Prefecture intensity summaries from `int[]`. |
| `affected_cities` | array of `AffectedCity` | City intensity summaries flattened from `int[].city[]`. |
| `tsunami_possible` | `boolean` or `null` | `true` when detail comments indicate tsunami possibility, `false` when they explicitly say there is no tsunami concern, otherwise `null`. |

#### Bulletin Type Enum

| Code | JMA meaning |
| --- | --- |
| `VXSE51` | `震度速報` — prompt seismic intensity bulletin. |
| `VXSE52` | `震源に関する情報` — hypocenter information. |
| `VXSE53` | `震源・震度に関する情報` — hypocenter and seismic intensity information. |
| `VXSE5k` | `震源・震度情報` — JMA Bosai detail bulletin variant. |
| `VXSE61` | `長周期地震動に関する観測情報` — observed long-period ground motion information. |
| `VYSE52` | `南海トラフ地震関連解説情報` — Nankai Trough earthquake-related explanatory information. |

#### Record: AffectedPrefecture

| Field | Type | Description |
| --- | --- | --- |
| `code` | `string` | JMA prefecture code from `int[].code`. |
| `max_intensity` | enum string | Maximum JMA seismic intensity for the prefecture from `int[].maxi`; one of `1`, `2`, `3`, `4`, `5-`, `5+`, `6-`, `6+`, or `7`. |

#### Record: AffectedCity

| Field | Type | Description |
| --- | --- | --- |
| `prefecture_code` | `string` | Parent JMA prefecture code. |
| `city_code` | `string` | JMA city/municipality code from `int[].city[].code`. |
| `max_intensity` | enum string | Maximum JMA seismic intensity for the city from `int[].city[].maxi`; one of `1`, `2`, `3`, `4`, `5-`, `5+`, `6-`, `6+`, or `7`. |
