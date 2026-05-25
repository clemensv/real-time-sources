# Seattle Street Closures Bridge Events

**Seattle Street Closures Bridge** polls the City of Seattle Open Data street closures dataset and emits one event per permitted closed street segment occurrence window.

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

### Endpoint `US.WA.Seattle.StreetClosures.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`US.WA.Seattle.StreetClosures`](#messagegroup-uswaseattlestreetclosures) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `seattle-street-closures` |
| Kafka key | `{closure_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `US.WA.Seattle.StreetClosures`
<a id="messagegroup-uswaseattlestreetclosures"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `US.WA.Seattle.StreetClosures.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `US.WA.Seattle.StreetClosures.StreetClosure`
<a id="message-uswaseattlestreetclosuresstreetclosure"></a>

| Field | Value |
| --- | --- |
| Name | StreetClosure |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.WA.Seattle.StreetClosures.jstruct/schemas/US.WA.Seattle.StreetClosures.StreetClosure`](#schema-uswaseattlestreetclosuresstreetclosure) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.WA.Seattle.StreetClosures.StreetClosure` |
| `source` |  | `string` | `False` | `https://data.seattle.gov/Built-Environment/Street-Closures/ium9-iqtc` |
| `subject` |  | `uritemplate` | `False` | `{closure_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.WA.Seattle.StreetClosures.Kafka` | `KAFKA` | topic `seattle-street-closures`; key `{closure_id}` |

## Schemagroups

### Schemagroup `US.WA.Seattle.StreetClosures.jstruct`
<a id="schemagroup-uswaseattlestreetclosuresjstruct"></a>

#### Schema `US.WA.Seattle.StreetClosures.StreetClosure`
<a id="schema-uswaseattlestreetclosuresstreetclosure"></a>

| Field | Value |
| --- | --- |
| Name | StreetClosure |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/seattle-street-closures/schemas/US.WA.Seattle.StreetClosures.StreetClosure.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `StreetClosure`
<a id="schema-node-streetclosure"></a>

Street closure row from the Seattle Department of Transportation street closures dataset, describing one closed street segment and its active occurrence window.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/seattle-street-closures/schemas/US.WA.Seattle.StreetClosures.StreetClosure.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `closure_id` | `string` | `True` | Derived stable identity for the closure row, composed from permit number, street segment key, start date, and end date. | - | - | - |
| `permit_number` | `string` | `True` | Identifier for the permit record granting authorization to close the street. | alternates=`[{"description": "Original field name in the Seattle street closures dataset.", "name": "permit_number"}]` | - | - |
| `permit_type` | `string` | `True` | Type of permit, such as Block Party, Play Street, Farmers Market, or Temporary Activation. | alternates=`[{"description": "Original field name in the Seattle street closures dataset.", "name": "permit_type"}]` | - | - |
| `project_name` | `union` | `False` | Short title used by Seattle to quickly identify the closure permit. | alternates=`[{"description": "Original field name in the Seattle street closures dataset.", "name": "project_name"}]` | - | - |
| `project_description` | `union` | `False` | Longer description of the permit, including issuance notes and closure details. | alternates=`[{"description": "Original field name in the Seattle street closures dataset.", "name": "project_description"}]` | - | - |
| `start_date` | `string` | `True` | Date on which the closure event begins, normalized to YYYY-MM-DD. | alternates=`[{"description": "Original field name in the Seattle street closures dataset.", "name": "start_date"}]` | - | - |
| `end_date` | `string` | `True` | Date on which the closure event ends, normalized to YYYY-MM-DD. | alternates=`[{"description": "Original field name in the Seattle street closures dataset.", "name": "end_date"}]` | - | - |
| `sunday` | `union` | `False` | Time period, if any, during which the closure occurs on Sundays between the start and end dates. | - | - | - |
| `monday` | `union` | `False` | Time period, if any, during which the closure occurs on Mondays between the start and end dates. | - | - | - |
| `tuesday` | `union` | `False` | Time period, if any, during which the closure occurs on Tuesdays between the start and end dates. | - | - | - |
| `wednesday` | `union` | `False` | Time period, if any, during which the closure occurs on Wednesdays between the start and end dates. | - | - | - |
| `thursday` | `union` | `False` | Time period, if any, during which the closure occurs on Thursdays between the start and end dates. | - | - | - |
| `friday` | `union` | `False` | Time period, if any, during which the closure occurs on Fridays between the start and end dates. | - | - | - |
| `saturday` | `union` | `False` | Time period, if any, during which the closure occurs on Saturdays between the start and end dates. | - | - | - |
| `street_on` | `union` | `False` | Street name of the closed street segment. | - | - | - |
| `street_from` | `union` | `False` | Name of the intersecting street at the low end of the closed segment. | - | - | - |
| `street_to` | `union` | `False` | Name of the intersecting street at the high end of the closed segment. | - | - | - |
| `segkey` | `union` | `False` | Identifier for the street segment that is closed. | - | - | - |
| `geometry_json` | `union` | `False` | Serialized GeoJSON LineString geometry for the closed street block. | alternates=`[{"description": "Original GeoJSON geometry object in the Seattle street closures dataset.", "name": "line_string"}]` | - | - |
