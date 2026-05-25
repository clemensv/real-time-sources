# JMA Bosai Earthquake & Seismic Intensity Information Events

MQTT/5.0 transport variant for JMA Bosai earthquake reports. Non-retained QoS-1 report events route by Romanized prefecture, magnitude bucket, event id, and retained JMA serial under seismic/jp/jma/jma-bosai-quake/... so subscribers can follow revisions distinctly.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `JP.JMA.Quake.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`JP.JMA.Quake`](#messagegroup-jpjmaquake) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `jma-bosai-quake` |
| Kafka key | `jp.jma.quake/{event_id}/{serial}` |
| Deployed | False |

### Endpoint `JP.JMA.Quake.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`JP.JMA.Quake.mqtt`](#messagegroup-jpjmaquakemqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `JP.JMA.Quake`
<a id="messagegroup-jpjmaquake"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `JP.JMA.Quake.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `JP.JMA.Quake.EarthquakeReport`
<a id="message-jpjmaquakeearthquakereport"></a>

JMA Bosai earthquake and seismic intensity report header enriched with parsed hypocenter coordinates, prefecture and city intensity summaries, and tsunami-related comment interpretation from the detail bulletin when available.

| Field | Value |
| --- | --- |
| Name | EarthquakeReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Quake.jstruct/schemas/JP.JMA.Quake.EarthquakeReport`](#schema-jpjmaquakeearthquakereport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Quake.EarthquakeReport` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.quake/{event_id}/{serial}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Quake.Kafka` | `KAFKA` | topic `jma-bosai-quake`; key `jp.jma.quake/{event_id}/{serial}` |

### Messagegroup `JP.JMA.Quake.mqtt`
<a id="messagegroup-jpjmaquakemqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for JMA Bosai earthquake reports. Non-retained QoS-1 report events route by Romanized prefecture, magnitude bucket, event id, and retained JMA serial under seismic/jp/jma/jma-bosai-quake/... so subscribers can follow revisions distinctly. |
| Transport bindings | `JP.JMA.Quake.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `JP.JMA.Quake.mqtt.EarthquakeReport`
<a id="message-jpjmaquakemqttearthquakereport"></a>

JMA Bosai earthquake and seismic intensity report header enriched with parsed hypocenter coordinates, prefecture and city intensity summaries, and tsunami-related comment interpretation from the detail bulletin when available.

| Field | Value |
| --- | --- |
| Name | EarthquakeReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/JP.JMA.Quake.jstruct/schemas/JP.JMA.Quake.EarthquakeReport`](#schema-jpjmaquakeearthquakereport) |
| Base message chain | `/messagegroups/JP.JMA.Quake/messages/JP.JMA.Quake.EarthquakeReport` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `JP.JMA.Quake.EarthquakeReport` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `jp.jma.quake/{event_id}/{serial}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `JP.JMA.Quake.Mqtt` | `MQTT/5.0` | topic `seismic/jp/jma/jma-bosai-quake/{prefecture}/{magnitude_bucket}/{event_id}/{serial}/report` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `seismic/jp/jma/jma-bosai-quake/{prefecture}/{magnitude_bucket}/{event_id}/{serial}/report` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `JP.JMA.Quake.jstruct`
<a id="schemagroup-jpjmaquakejstruct"></a>

#### Schema `JP.JMA.Quake.EarthquakeReport`
<a id="schema-jpjmaquakeearthquakereport"></a>

| Field | Value |
| --- | --- |
| Name | EarthquakeReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/quake/EarthquakeReport` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| Type | `object` |

###### Object `EarthquakeReport`
<a id="schema-node-earthquakereport"></a>

A JMA Bosai earthquake report record built from the recent earthquake list endpoint and, when available, the matching full detail JSON bulletin. The record is keyed by the stable JMA event id plus report serial so updates, corrections, and cancellations for the same earthquake remain distinct stream records.

| Field | Value |
| --- | --- |
| $id | `https://www.jma.go.jp/schemas/bosai/quake/EarthquakeReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `prefecture` | `string` | `True` | ASCII-safe Romanized prefecture slug derived from the JMA epicenter area name when available, otherwise from the first affected prefecture code. Japanese names remain in epicenter_area_jp and affected prefecture/city payload fields; MQTT topics use this ASCII axis. | - | pattern=`^[a-z0-9][a-z0-9-]*$` | - |
| `magnitude_bucket` | `string` | `True` | MQTT routing bucket derived from the JMA magnitude. Values are magnitude-lt1, magnitude-1 through magnitude-8 for floor buckets, magnitude-9plus, or magnitude-unknown when the bulletin omits magnitude. | - | pattern=`^magnitude-(unknown\\|lt1\\|[1-8]\\|9plus)$` | - |
| `event_id` | `string` | `True` | Stable JMA earthquake event identifier copied from list.json eid and detail Head.EventID. JMA uses the earthquake origin time in YYYYMMDDHHMMSS form as the event id, so multiple serial reports for the same earthquake share this value. | altnames=`{"jma-bosai": "eid"}` | pattern=`^[0-9]{14}$` | - |
| `serial` | `integer` | `True` | JMA report serial number parsed from list.json ser and detail Head.Serial. The serial identifies the revision sequence for bulletins sharing the same event id. | altnames=`{"jma-bosai": "ser"}` | minimum=`0` | - |
| `report_id` | `string` | `True` | Composite report identifier formed as event_id, an underscore, and the JMA serial number. It distinguishes initial, corrected, and subsequent bulletins for the same earthquake event. | - | - | - |
| `info_type` | enum `['ISSUED', 'CORRECTED', 'CANCELLED']` | `True` | Normalized information type derived from the Japanese JMA ift field: ISSUED for 発表, CORRECTED for 訂正, and CANCELLED for 取消. | altnames=`{"jma-bosai": "ift"}`<br>altenums=`{"jma_label": {"CANCELLED": "取消", "CORRECTED": "訂正", "ISSUED": "発表"}}` | - | - |
| `report_datetime` | `datetime` | `True` | Report publication time converted from list.json rdt to an RFC3339 UTC timestamp. JMA publishes rdt with a local offset for the report release time. | altnames=`{"jma-bosai": "rdt"}` | - | - |
| `report_datetime_local` | `datetime` | `True` | Original JMA report publication timestamp copied from list.json rdt, preserving the local offset supplied by the JMA Bosai feed. | altnames=`{"jma-bosai": "rdt"}` | - | - |
| `control_datetime` | `datetime` | `True` | JMA control timestamp — when the bulletin was published to the JMA distribution system, distinct from `report_datetime` which is the event report time. This field converts the compact list.json ctt value from JST to an RFC3339 UTC timestamp. | altnames=`{"jma-bosai": "ctt"}` | - | - |
| `control_datetime_local` | `datetime` | `True` | JMA control timestamp — when the bulletin was published to the JMA distribution system, distinct from `report_datetime` which is the event report time. This field preserves the compact list.json ctt value as an RFC3339 timestamp with the Japan Standard Time offset. | altnames=`{"jma-bosai": "ctt"}` | - | - |
| `origin_datetime` | `datetime` | `True` | Earthquake origin time converted from list.json at to an RFC3339 UTC timestamp. JMA uses this time as the basis for the event id. | altnames=`{"jma-bosai": "at"}` | - | - |
| `origin_datetime_local` | `datetime` | `True` | Original JMA earthquake origin timestamp copied from list.json at, preserving the local offset supplied by the JMA Bosai feed. | altnames=`{"jma-bosai": "at"}` | - | - |
| `title_jp` | `string` | `True` | Japanese JMA bulletin title copied from list.json ttl, such as 震源・震度情報 for earthquake and seismic intensity information. | altnames=`{"jma-bosai": "ttl"}` | - | - |
| `title_en` | `union` | `False` | English bulletin title copied from list.json en_ttl when supplied by the multilingual JMA Bosai feed. Null is emitted when en_ttl is absent, including some 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | altnames=`{"jma-bosai": "en_ttl"}` | - | - |
| `epicenter_area_code` | `union` | `False` | JMA hypocenter or epicenter area code copied from list.json acd and detail Body.Earthquake.Hypocenter.Area.Code. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | altnames=`{"jma-bosai": "acd"}` | - | - |
| `epicenter_area_jp` | `union` | `False` | Japanese epicenter area name copied from list.json anm and detail Body.Earthquake.Hypocenter.Area.Name. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | altnames=`{"jma-bosai": "anm"}` | - | - |
| `epicenter_area_en` | `union` | `False` | English epicenter area name copied from list.json en_anm when supplied by the multilingual JMA Bosai feed. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | altnames=`{"jma-bosai": "en_anm"}` | - | - |
| `latitude` | `union` | `False` | Hypocenter latitude in WGS84 decimal degrees parsed from the ISO 6709 coordinate string in list.json cod or detail Body.Earthquake.Hypocenter.Area.Coordinate. Null is emitted when the coordinate is absent or cannot be parsed; null is also emitted when list.json cod is absent, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | unit=`degree` symbol=`°`<br>altnames=`{"jma-bosai": "cod"}` | maximum=`90.0`<br>minimum=`-90.0` | - |
| `longitude` | `union` | `False` | Hypocenter longitude in WGS84 decimal degrees parsed from the ISO 6709 coordinate string in list.json cod or detail Body.Earthquake.Hypocenter.Area.Coordinate. Null is emitted when the coordinate is absent or cannot be parsed; null is also emitted when list.json cod is absent, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | unit=`degree` symbol=`°`<br>altnames=`{"jma-bosai": "cod"}` | maximum=`180.0`<br>minimum=`-180.0` | - |
| `depth_km` | `union` | `False` | Hypocenter depth in kilometres parsed from the third component of the ISO 6709 coordinate string. JMA encodes depth in metres with a sign in cod; this field divides the absolute metre value by 1000 so +35.0+135.5-10000/ becomes 10.0 km. Null is emitted when list.json cod is absent, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | unit=`kilometer` symbol=`km`<br>altnames=`{"jma-bosai": "cod"}` | maximum=`700.0`<br>minimum=`0.0` | - |
| `magnitude` | `union` | `False` | Dimensionless JMA earthquake magnitude parsed from list.json mag or detail Body.Earthquake.Magnitude and expressed on the JMA magnitude scale, which is similar to Richter magnitude for shallow events. Null is emitted when the source bulletin omits magnitude, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | altnames=`{"jma-bosai": "mag"}` | - | - |
| `max_intensity` | enum `['1', '2', '3', '4', '5-', '5+', '6-', '6+', '7']` | `False` | Maximum observed JMA seismic intensity for the report copied from list.json maxi or detail Body.Intensity.Observation.MaxInt. Null is emitted when the bulletin has no observed intensity summary, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins. | altnames=`{"jma-bosai": "maxi"}`<br>altenums=`{"jma_label": {"1": "震度1 (slight)", "2": "震度2", "3": "震度3", "4": "震度4", "5+": "震度5強", "5-": "震度5弱", "6+": "震度6強", "6-": "震度6弱", "7": "震度7 (catastrophic)"}}` | pattern=`^(1\\|2\\|3\\|4\\|5-\\|5\+\\|6-\\|6\+\\|7)$` | - |
| `bulletin_type` | enum `['VXSE51', 'VXSE52', 'VXSE53', 'VXSE5k', 'VXSE61', 'VYSE52']` | `True` | JMA detail bulletin product code parsed from the detail JSON filename. Supported earthquake-related JMA Bosai codes are VXSE51 (震度速報), VXSE52 (震源に関する情報), VXSE53 (震源・震度に関する情報), VXSE5k (震源・震度情報 Bosai variant), VXSE61 (長周期地震動に関する観測情報), and VYSE52 (南海トラフ地震関連解説情報). Tsunami-specific VTSE products are deliberately not modeled by this source. | altnames=`{"jma-bosai": "json"}`<br>altenums=`{"jma_documentation": {"VXSE51": "震度速報 — prompt seismic intensity bulletin reporting observed intensity before hypocenter details are finalized.", "VXSE52": "震源に関する情報 — hypocenter bulletin issued when source parameters are available and observed intensity details may be absent.", "VXSE53": "震源・震度に関する情報 — hypocenter and seismic intensity bulletin with source parameters and observation summaries.", "VXSE5k": "震源・震度情報 — JMA Bosai detail bulletin variant for earthquake source and seismic intensity information.", "VXSE61": "長周期地震動に関する観測情報 — observed long-period ground motion information related to an earthquake.", "VYSE52": "南海トラフ地震関連解説情報 — explanatory information related to the Nankai Trough earthquake assessment process."}}` | - | - |
| `detail_url` | `uri` | `True` | Absolute URL for the full JMA Bosai earthquake detail JSON referenced by list.json json. | altnames=`{"jma-bosai": "json"}` | - | - |
| `affected_prefectures` | array of `schema` | `True` | Prefecture intensity summaries derived from list.json int[]. Each entry includes the JMA prefecture code and maximum JMA seismic intensity reported for that prefecture. | altnames=`{"jma-bosai": "int"}` | - | - |
| `affected_cities` | array of `schema` | `True` | City intensity summaries flattened from list.json int[].city[]. Each entry carries its parent prefecture code, city code, and maximum JMA seismic intensity for the city. | altnames=`{"jma-bosai": "int.city"}` | - | - |
| `tsunami_possible` | `union` | `True` | Interpretation of tsunami-related text in the full detail JSON comments. True means the detail bulletin text indicates tsunami attention or possibility; false means the detail explicitly states there is no tsunami concern; null means no tsunami-related detail text was available or fetched. | - | - | - |
