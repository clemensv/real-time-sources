# DWD Pollenflug (German Pollen Forecast) Bridge Events

**DWD Pollenflug Bridge** polls the Deutscher Wetterdienst (DWD) pollen forecast API for the latest daily pollen forecasts across Germany and sends them to a Kafka topic as CloudEvents. The tool tracks the `last_update` timestamp from the API to avoid sending duplicate forecasts.

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

### Endpoint `DE.DWD.Pollenflug.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`DE.DWD.Pollenflug`](#messagegroup-dedwdpollenflug) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `dwd-pollenflug` |
| Kafka key | `{region_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `DE.DWD.Pollenflug`
<a id="messagegroup-dedwdpollenflug"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `DE.DWD.Pollenflug.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `DE.DWD.Pollenflug.Region`
<a id="message-dedwdpollenflugregion"></a>

| Field | Value |
| --- | --- |
| Name | Region |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.Pollenflug.jstruct/schemas/DE.DWD.Pollenflug.Region`](#schema-dedwdpollenflugregion) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.Pollenflug.Region` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de/climate_environment/health/alerts/` |
| `subject` |  | `uritemplate` | `False` | `{region_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.Pollenflug.Kafka` | `KAFKA` | topic `dwd-pollenflug`; key `{region_id}` |

#### Message `DE.DWD.Pollenflug.PollenForecast`
<a id="message-dedwdpollenflugpollenforecast"></a>

| Field | Value |
| --- | --- |
| Name | PollenForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.Pollenflug.jstruct/schemas/DE.DWD.Pollenflug.PollenForecast`](#schema-dedwdpollenflugpollenforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.Pollenflug.PollenForecast` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de/climate_environment/health/alerts/` |
| `subject` |  | `uritemplate` | `False` | `{region_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.Pollenflug.Kafka` | `KAFKA` | topic `dwd-pollenflug`; key `{region_id}` |

## Schemagroups

### Schemagroup `DE.DWD.Pollenflug.jstruct`
<a id="schemagroup-dedwdpollenflugjstruct"></a>

#### Schema `DE.DWD.Pollenflug.Region`
<a id="schema-dedwdpollenflugregion"></a>

| Field | Value |
| --- | --- |
| Name | Region |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Pollenflug/Region` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Region`
<a id="schema-node-region"></a>

Reference data for a DWD pollen forecast region or sub-region. Germany is divided into 11 main regions, some of which are subdivided into 2–4 sub-regions for a total of 27 forecast areas. Emitted at bridge startup so downstream consumers can correlate forecast events with region metadata.

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Pollenflug/Region` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region_id` | `int32` | `True` | Unique numeric identifier for the forecast area. For regions without sub-regions this is the main region_id (e.g. 20 for Mecklenburg-Vorpommern). For sub-regions it is the partregion_id (e.g. 11 for 'Inseln und Marschen' within Schleswig-Holstein). Derived from the DWD JSON fields region_id and partregion_id. | - | - | - |
| `region_name` | `string` | `True` | Name of the main geographic region as published by DWD (e.g. 'Schleswig-Holstein und Hamburg', 'Bayern'). Sourced from the 'region_name' field in the DWD API response. | - | - | - |
| `partregion_id` | `union` | `False` | Numeric identifier of the sub-region within the parent region. Set to -1 by DWD when the region has no sub-divisions; the bridge emits null in that case. Sourced from the 'partregion_id' field in the DWD API response. | - | - | - |
| `partregion_name` | `union` | `False` | Name of the sub-region (e.g. 'Inseln und Marschen', 'Geest,Schleswig-Holstein und Hamburg'). Empty string in the DWD response when the region has no sub-divisions; the bridge emits null in that case. Sourced from the 'partregion_name' field in the DWD API response. | - | - | - |

#### Schema `DE.DWD.Pollenflug.PollenForecast`
<a id="schema-dedwdpollenflugpollenforecast"></a>

| Field | Value |
| --- | --- |
| Name | PollenForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Pollenflug/PollenForecast` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PollenForecast`
<a id="schema-node-pollenforecast"></a>

Daily pollen forecast for a single German region or sub-region, published by the Deutscher Wetterdienst (DWD). Contains intensity values for eight pollen types across three forecast days (today, tomorrow, day after tomorrow). Intensity is on a scale from 0 (no load) to 3 (high load) with intermediate half-step ranges such as '0-1', '1-2', '2-3'. The bridge maps the German pollen names from the upstream API to English equivalents.

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Pollenflug/PollenForecast` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region_id` | `int32` | `True` | Unique numeric identifier for the forecast area. Same identity model as Region: uses partregion_id when the area is a sub-region, otherwise uses the main region_id. | - | - | - |
| `region_name` | `string` | `True` | Display name of the forecast area. Uses partregion_name when available, otherwise region_name. | - | - | - |
| `last_update` | `string` | `True` | Timestamp of the last forecast update as published by DWD, e.g. '2025-04-08 11:00 Uhr'. Retained as a string because the upstream format includes the German suffix 'Uhr'. | - | - | - |
| `next_update` | `string` | `True` | Timestamp of the next expected forecast update as published by DWD, e.g. '2025-04-09 11:00 Uhr'. | - | - | - |
| `sender` | `union` | `False` | Issuing organization as stated in the DWD API response, typically 'Deutscher Wetterdienst - Medizin-Meteorologie'. | - | - | - |
| `hazel_today` | `union` | `False` | Pollen intensity for Hasel (hazel) today. Values: '0' (none), '0-1' (none to low), '1' (low), '1-2' (low to medium), '2' (medium), '2-3' (medium to high), '3' (high). | altnames=`{"lang:de": "Hasel heute"}` | - | - |
| `hazel_tomorrow` | `union` | `False` | Pollen intensity for Hasel (hazel) tomorrow. | altnames=`{"lang:de": "Hasel morgen"}` | - | - |
| `hazel_dayafter_to` | `union` | `False` | Pollen intensity for Hasel (hazel) the day after tomorrow. | altnames=`{"lang:de": "Hasel übermorgen"}` | - | - |
| `alder_today` | `union` | `False` | Pollen intensity for Erle (alder) today. | altnames=`{"lang:de": "Erle heute"}` | - | - |
| `alder_tomorrow` | `union` | `False` | Pollen intensity for Erle (alder) tomorrow. | altnames=`{"lang:de": "Erle morgen"}` | - | - |
| `alder_dayafter_to` | `union` | `False` | Pollen intensity for Erle (alder) the day after tomorrow. | altnames=`{"lang:de": "Erle übermorgen"}` | - | - |
| `birch_today` | `union` | `False` | Pollen intensity for Birke (birch) today. | altnames=`{"lang:de": "Birke heute"}` | - | - |
| `birch_tomorrow` | `union` | `False` | Pollen intensity for Birke (birch) tomorrow. | altnames=`{"lang:de": "Birke morgen"}` | - | - |
| `birch_dayafter_to` | `union` | `False` | Pollen intensity for Birke (birch) the day after tomorrow. | altnames=`{"lang:de": "Birke übermorgen"}` | - | - |
| `ash_today` | `union` | `False` | Pollen intensity for Esche (ash) today. | altnames=`{"lang:de": "Esche heute"}` | - | - |
| `ash_tomorrow` | `union` | `False` | Pollen intensity for Esche (ash) tomorrow. | altnames=`{"lang:de": "Esche morgen"}` | - | - |
| `ash_dayafter_to` | `union` | `False` | Pollen intensity for Esche (ash) the day after tomorrow. | altnames=`{"lang:de": "Esche übermorgen"}` | - | - |
| `grasses_today` | `union` | `False` | Pollen intensity for Gräser (grasses) today. In the upstream API this field is named 'Graeser'. | altnames=`{"lang:de": "Gräser heute"}` | - | - |
| `grasses_tomorrow` | `union` | `False` | Pollen intensity for Gräser (grasses) tomorrow. | altnames=`{"lang:de": "Gräser morgen"}` | - | - |
| `grasses_dayafter_to` | `union` | `False` | Pollen intensity for Gräser (grasses) the day after tomorrow. | altnames=`{"lang:de": "Gräser übermorgen"}` | - | - |
| `rye_today` | `union` | `False` | Pollen intensity for Roggen (rye) today. | altnames=`{"lang:de": "Roggen heute"}` | - | - |
| `rye_tomorrow` | `union` | `False` | Pollen intensity for Roggen (rye) tomorrow. | altnames=`{"lang:de": "Roggen morgen"}` | - | - |
| `rye_dayafter_to` | `union` | `False` | Pollen intensity for Roggen (rye) the day after tomorrow. | altnames=`{"lang:de": "Roggen übermorgen"}` | - | - |
| `mugwort_today` | `union` | `False` | Pollen intensity for Beifuß (mugwort) today. In the upstream API this field is named 'Beifuss'. | altnames=`{"lang:de": "Beifuß heute"}` | - | - |
| `mugwort_tomorrow` | `union` | `False` | Pollen intensity for Beifuß (mugwort) tomorrow. | altnames=`{"lang:de": "Beifuß morgen"}` | - | - |
| `mugwort_dayafter_to` | `union` | `False` | Pollen intensity for Beifuß (mugwort) the day after tomorrow. | altnames=`{"lang:de": "Beifuß übermorgen"}` | - | - |
| `ragweed_today` | `union` | `False` | Pollen intensity for Ambrosia (ragweed) today. | altnames=`{"lang:de": "Ambrosia heute"}` | - | - |
| `ragweed_tomorrow` | `union` | `False` | Pollen intensity for Ambrosia (ragweed) tomorrow. | altnames=`{"lang:de": "Ambrosia morgen"}` | - | - |
| `ragweed_dayafter_to` | `union` | `False` | Pollen intensity for Ambrosia (ragweed) the day after tomorrow. | altnames=`{"lang:de": "Ambrosia übermorgen"}` | - | - |
