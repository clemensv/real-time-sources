# EAWS ALBINA Avalanche Bulletin Bridge Events

MQTT/5.0 transport variant for EAWS ALBINA avalanche bulletins. Non-retained QoS-1 bulletin events route by country, region, and danger level under alerts/at/eaws/eaws-albina/...

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

### Endpoint `org.EAWS.ALBINA.Bulletins.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`org.EAWS.ALBINA.Bulletins`](#messagegroup-orgeawsalbinabulletins) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `eaws-albina` |
| Kafka key | `{region_id}` |
| Deployed | False |

### Endpoint `org.EAWS.ALBINA.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`org.EAWS.ALBINA.mqtt`](#messagegroup-orgeawsalbinamqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `org.EAWS.ALBINA.Bulletins`
<a id="messagegroup-orgeawsalbinabulletins"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `org.EAWS.ALBINA.Bulletins.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `org.EAWS.ALBINA.AvalancheRegion`
<a id="message-orgeawsalbinaavalancheregion"></a>

Reference event describing an EAWS region (or super-region) that the bridge is configured to observe. Emitted at bridge startup and whenever the configured region set changes. Acts as the catalog backbone for downstream consumers, ensuring the regional context is available even outside the avalanche season when no bulletins are being published.

| Field | Value |
| --- | --- |
| Name | AvalancheRegion |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/org.EAWS.ALBINA.jstruct/schemas/org.EAWS.ALBINA.AvalancheRegion`](#schema-orgeawsalbinaavalancheregion) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `org.EAWS.ALBINA.AvalancheRegion` |
| `source` |  | `string` | `False` | `https://avalanche.report` |
| `subject` |  | `uritemplate` | `False` | `{region_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `org.EAWS.ALBINA.Bulletins.Kafka` | `KAFKA` | topic `eaws-albina`; key `{region_id}` |

#### Message `org.EAWS.ALBINA.AvalancheBulletin`
<a id="message-orgeawsalbinaavalanchebulletin"></a>

| Field | Value |
| --- | --- |
| Name | AvalancheBulletin |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/org.EAWS.ALBINA.jstruct/schemas/org.EAWS.ALBINA.AvalancheBulletin`](#schema-orgeawsalbinaavalanchebulletin) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `org.EAWS.ALBINA.AvalancheBulletin` |
| `source` |  | `string` | `False` | `https://avalanche.report` |
| `subject` |  | `uritemplate` | `False` | `{region_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `org.EAWS.ALBINA.Bulletins.Kafka` | `KAFKA` | topic `eaws-albina`; key `{region_id}` |

### Messagegroup `org.EAWS.ALBINA.mqtt`
<a id="messagegroup-orgeawsalbinamqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for EAWS ALBINA avalanche bulletins. Non-retained QoS-1 bulletin events route by country, region, and danger level under alerts/at/eaws/eaws-albina/... |
| Transport bindings | `org.EAWS.ALBINA.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `org.EAWS.ALBINA.mqtt.AvalancheBulletin`
<a id="message-orgeawsalbinamqttavalanchebulletin"></a>

| Field | Value |
| --- | --- |
| Name | AvalancheBulletin |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/org.EAWS.ALBINA.jstruct/schemas/org.EAWS.ALBINA.AvalancheBulletin`](#schema-orgeawsalbinaavalanchebulletin) |
| Base message chain | `/messagegroups/org.EAWS.ALBINA.Bulletins/messages/org.EAWS.ALBINA.AvalancheBulletin` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `org.EAWS.ALBINA.AvalancheBulletin` |
| `source` |  | `string` | `False` | `https://avalanche.report` |
| `subject` |  | `uritemplate` | `False` | `{region_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `org.EAWS.ALBINA.Mqtt` | `MQTT/5.0` | topic `alerts/at/eaws/eaws-albina/{country}/{region_id}/{danger_level}/bulletin` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/at/eaws/eaws-albina/{country}/{region_id}/{danger_level}/bulletin` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `org.EAWS.ALBINA.jstruct`
<a id="schemagroup-orgeawsalbinajstruct"></a>

#### Schema `org.EAWS.ALBINA.AvalancheBulletin`
<a id="schema-orgeawsalbinaavalanchebulletin"></a>

| Field | Value |
| --- | --- |
| Name | AvalancheBulletin |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AvalancheBulletin`
<a id="schema-node-avalanchebulletin"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region_id` | `string` | `True` | EAWS micro-region identifier from the CAAMLv6 regions array, e.g. AT-07-04-02 for Karwendel Mountains East. | - | - | - |
| `region_name` | `string` | `True` | Human-readable name of the EAWS micro-region, e.g. 'Karwendel Mountains East'. | - | - | - |
| `bulletin_id` | `string` | `True` | Unique UUID assigned to this bulletin by the ALBINA system, from the CAAMLv6 bulletinID field. | - | - | - |
| `publication_time` | `datetime` | `True` | ISO 8601 timestamp when this bulletin was published by the avalanche warning service. | - | - | - |
| `valid_time_start` | `datetime` | `True` | ISO 8601 start of the validity period for this bulletin. | - | - | - |
| `valid_time_end` | `datetime` | `True` | ISO 8601 end of the validity period for this bulletin. | - | - | - |
| `lang` | `string` | `True` | ISO 639-1 language code of the bulletin text, e.g. 'en', 'de', 'it'. | - | - | - |
| `max_danger_rating` | enum `['low', 'moderate', 'considerable', 'high', 'very_high']` | `False` | Highest EAWS danger rating across all elevation bands and time periods in this bulletin. One of: low, moderate, considerable, high, very_high, or null if no ratings are present. | - | - | - |
| `max_danger_rating_value` | `union` | `False` | Numeric value (1-5) of the highest EAWS danger rating: 1=low, 2=moderate, 3=considerable, 4=high, 5=very_high. Null if no ratings are present. | - | - | - |
| `danger_ratings_json` | `string` | `True` | JSON-encoded array of CAAMLv6 dangerRatings objects, each with mainValue (string), optional elevation (object with upperBound/lowerBound), and validTimePeriod (string: all_day, earlier, later). | - | - | - |
| `avalanche_problems_json` | `string` | `True` | JSON-encoded array of CAAMLv6 avalancheProblems objects, each with problemType (e.g. wet_snow, persistent_weak_layers, wind_slab, new_snow, gliding_snow), snowpackStability, frequency, avalancheSize (1-5), aspects array, and optional elevation bounds. | - | - | - |
| `tendency_type` | `union` | `False` | Overall tendency of avalanche danger from the first tendency entry: decreasing, steady, or increasing. Null if no tendency data is present. | - | - | - |
| `danger_patterns_json` | `union` | `False` | JSON-encoded array of LWD Tyrol danger pattern codes from customData.LWD_Tyrol.dangerPatterns, e.g. ["DP10","DP4"]. Null if not present (non-Tyrol regions). | - | - | - |
| `avalanche_activity_highlights` | `union` | `False` | Summary of current avalanche activity conditions from avalancheActivity.highlights. May contain HTML markup. Null if not provided. | - | - | - |
| `snowpack_structure_comment` | `union` | `False` | Description of current snowpack structure and layering from snowpackStructure.comment. May contain HTML markup. Null if not provided. | - | - | - |
| `country` | `string` | `True` | Lowercase ISO 3166-1 alpha-2 country code derived from the CAAML region_id prefix, e.g. at or it. | - | - | - |
| `danger_level` | `string` | `True` | Topic-safe EAWS danger level derived from the highest danger rating, or 'unknown' when no rating is present. | - | - | - |

#### Schema `org.EAWS.ALBINA.AvalancheRegion`
<a id="schema-orgeawsalbinaavalancheregion"></a>

| Field | Value |
| --- | --- |
| Name | AvalancheRegion |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AvalancheRegion`
<a id="schema-node-avalancheregion"></a>

Reference record describing an EAWS region (or super-region) the bridge is configured to observe. Emitted at startup so that downstream consumers know the regional context even in summer months when no daily bulletins are published.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region_id` | `string` | `True` | EAWS region identifier (country prefix plus warning service code), e.g. AT-07 for Tirol, IT-32-BZ for South Tyrol. Matches the regionID used in CAAMLv6 bulletins. | - | - | - |
| `lang` | `string` | `True` | ISO 639-1 language code used by the bridge when requesting bulletins for this region (de, en, it, fr, etc.). | - | - | - |
| `configured_at` | `datetime` | `True` | ISO 8601 UTC timestamp when this region was registered in the bridge configuration. Updated whenever the bridge starts and re-emits its catalog. | - | - | - |
| `bulletin_base_url` | `union` | `False` | Base URL used by the bridge to fetch CAAMLv6 bulletins for this region (typically https://avalanche.report/albina_files). Null when not provided. | - | - | - |
