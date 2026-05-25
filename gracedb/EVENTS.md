# GraceDB Gravitational Wave Candidate Alerts Events

MQTT/5.0 transport variant for GraceDB superevents. Non-retained QoS-1 event stream routed by category, physics group, and superevent id under seismic/intl/ligo/gracedb/...

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `org.ligo.gracedb.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`org.ligo.gracedb`](#messagegroup-orgligogracedb) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `gracedb` |
| Kafka key | `{superevent_id}` |
| Deployed | False |

### Endpoint `org.ligo.gracedb.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`org.ligo.gracedb.mqtt`](#messagegroup-orgligogracedbmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `org.ligo.gracedb`
<a id="messagegroup-orgligogracedb"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `org.ligo.gracedb.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `org.ligo.gracedb.Superevent`
<a id="message-orgligogracedbsuperevent"></a>

A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata.

| Field | Value |
| --- | --- |
| Name | Superevent |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/org.ligo.gracedb.jstruct/schemas/org.ligo.gracedb.Superevent`](#schema-orgligogracedbsuperevent) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `org.ligo.gracedb.Superevent` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{superevent_id}` |
| `time` |  | `uritemplate` | `False` | `{created}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `org.ligo.gracedb.Kafka` | `KAFKA` | topic `gracedb`; key `{superevent_id}` |

### Messagegroup `org.ligo.gracedb.mqtt`
<a id="messagegroup-orgligogracedbmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for GraceDB superevents. Non-retained QoS-1 event stream routed by category, physics group, and superevent id under seismic/intl/ligo/gracedb/... |
| Transport bindings | `org.ligo.gracedb.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `org.ligo.gracedb.mqtt.Superevent`
<a id="message-orgligogracedbmqttsuperevent"></a>

A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata.

| Field | Value |
| --- | --- |
| Name | Superevent |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/org.ligo.gracedb.jstruct/schemas/org.ligo.gracedb.Superevent`](#schema-orgligogracedbsuperevent) |
| Base message chain | `/messagegroups/org.ligo.gracedb/messages/org.ligo.gracedb.Superevent` |
| Transport override | `MQTT/5.0` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `org.ligo.gracedb.Superevent` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{superevent_id}` |
| `time` |  | `uritemplate` | `False` | `{created}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `org.ligo.gracedb.Mqtt` | `MQTT/5.0` | topic `seismic/intl/ligo/gracedb/{category}/{group}/{superevent_id}/superevent` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `seismic/intl/ligo/gracedb/{category}/{group}/{superevent_id}/superevent` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `org.ligo.gracedb.jstruct`
<a id="schemagroup-orgligogracedbjstruct"></a>

#### Schema `org.ligo.gracedb.Superevent`
<a id="schema-orgligogracedbsuperevent"></a>

| Field | Value |
| --- | --- |
| Name | Superevent |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://gracedb.ligo.org/schemas/org/ligo/gracedb/Superevent` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/org/ligo/gracedb/Superevent` |
| Type | `object` |

###### Object `Superevent`
<a id="schema-node-superevent"></a>

A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `superevent_id` | `string` | `True` | Unique identifier for the superevent assigned by GraceDB, e.g. 'S240414a' for production events or 'MS260408x' for MDC (mock data challenge) events. | - | - | - |
| `category` | `string` | `True` | Category of the superevent. 'Production' for real observing-run candidates, 'MDC' for mock data challenge injections, 'Test' for engineering/test events. | - | - | - |
| `created` | `string` | `True` | ISO-8601 UTC timestamp when the superevent was first created in GraceDB, e.g. '2026-04-08 23:59:34 UTC'. | - | - | - |
| `t_start` | `double` | `True` | GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the start of the superevent time window. | - | - | - |
| `t_0` | `double` | `True` | GPS time (seconds since 1980-01-06T00:00:00 UTC) of the central trigger time for this superevent. | - | - | - |
| `t_end` | `double` | `True` | GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the end of the superevent time window. | - | - | - |
| `far` | `double` | `True` | False alarm rate in Hz. Lower values indicate a more significant event. For example, 1e-14 Hz corresponds to roughly one false alarm per 3 million years. | - | - | - |
| `time_coinc_far` | `union` | `False` | Time-coincidence false alarm rate in Hz from the RAVEN pipeline, representing the probability of a temporal coincidence with an external trigger. Null if no external coincidence was evaluated. | - | - | - |
| `space_coinc_far` | `union` | `False` | Space-and-time-coincidence false alarm rate in Hz from the RAVEN pipeline, incorporating both temporal and spatial overlap with an external trigger. Null if no external coincidence was evaluated. | - | - | - |
| `labels_json` | `string` | `True` | JSON-encoded array of label strings attached to this superevent, e.g. '["EM_READY","GCN_PRELIM_SENT","SKYMAP_READY"]'. Labels track alert lifecycle: EM_READY (electromagnetic follow-up viable), GCN_PRELIM_SENT (GCN preliminary notice sent), SKYMAP_READY (sky localization map available), EMBRIGHT_READY (source classification available), PASTRO_READY (probability of astrophysical origin available), ADVOK/ADVNO (advocate approval/rejection), SIGNIF_LOCKED (significance frozen), DQR_REQUEST (data quality review requested), HIGH_PROFILE (high-profile candidate), RAVEN_ALERT (external trigger coincidence found). | - | - | - |
| `preferred_event_id` | `union` | `False` | GraceDB event ID of the preferred pipeline event (the best detection) associated with this superevent, e.g. 'M632680'. Null if no preferred event has been selected. | - | - | - |
| `pipeline` | `union` | `False` | Name of the detection pipeline that produced the preferred event, e.g. 'gstlal', 'MBTAOnline', 'SPIIR', 'PyCBC'. Null if no preferred event has been set. | - | - | - |
| `group` | `string` | `True` | Physics group of the preferred event: 'CBC' (compact binary coalescence), 'Burst' (unmodeled transient), 'Test', or 'unknown' when GraceDB has not supplied preferred-event group data. | - | - | - |
| `instruments` | `union` | `False` | Comma-separated list of detector instruments that contributed to the preferred event, e.g. 'H1,L1,V1' for LIGO Hanford, LIGO Livingston, and Virgo. Null if no preferred event has been set. | - | - | - |
| `gw_id` | `union` | `False` | Official gravitational wave event name assigned after confirmation, e.g. 'GW200115'. Null if the event has not been confirmed or named. | - | - | - |
| `submitter` | `string` | `True` | Username or service account that submitted the superevent to GraceDB, e.g. 'read-cvmfs-emfollow'. | - | - | - |
| `em_type` | `union` | `False` | Identifier of the associated electromagnetic event from an external trigger (e.g. a Fermi GBM or Swift trigger ID). Null if no external EM association exists. | - | - | - |
| `search` | `union` | `False` | Search type of the preferred event: 'AllSky' (standard all-sky search), 'MDC' (mock data challenge), 'BBH' (binary black hole targeted), 'EarlyWarning' (pre-merger alert). Null if no preferred event has been set. | - | - | - |
| `far_is_upper_limit` | `union` | `False` | Whether the reported FAR value is an upper limit rather than an exact estimate. True indicates the actual false alarm rate may be lower. Null if no preferred event has been set. | - | - | - |
| `nevents` | `union` | `False` | Number of pipeline events aggregated into this superevent. Null if the preferred event data is not available. | - | - | - |
| `self_uri` | `string` | `True` | HATEOAS self link for the superevent resource in the GraceDB REST API, e.g. 'https://gracedb.ligo.org/api/superevents/MS260408x/'. | - | - | - |

### Schemagroup `org.ligo.gracedb.avro`
<a id="schemagroup-orgligogracedbavro"></a>

#### Schema `org.ligo.gracedb.Superevent`
<a id="schema-orgligogracedbsuperevent"></a>

| Field | Value |
| --- | --- |
| Name | Superevent |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Superevent |
| Namespace | org.ligo.gracedb |
| Type | `record` |
| Doc | A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `superevent_id` | `string` | Unique identifier for the superevent assigned by GraceDB, e.g. 'S240414a' for production events or 'MS260408x' for MDC (mock data challenge) events. | `-` |
| `category` | `string` | Category of the superevent. 'Production' for real observing-run candidates, 'MDC' for mock data challenge injections, 'Test' for engineering/test events. | `-` |
| `created` | `string` | ISO-8601 UTC timestamp when the superevent was first created in GraceDB, e.g. '2026-04-08 23:59:34 UTC'. | `-` |
| `t_start` | `double` | GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the start of the superevent time window. | `-` |
| `t_0` | `double` | GPS time (seconds since 1980-01-06T00:00:00 UTC) of the central trigger time for this superevent. | `-` |
| `t_end` | `double` | GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the end of the superevent time window. | `-` |
| `far` | `double` | False alarm rate in Hz. Lower values indicate a more significant event. | `-` |
| `time_coinc_far` | `double` \| `null` | Time-coincidence false alarm rate in Hz from the RAVEN pipeline. Null if no external coincidence was evaluated. | `-` |
| `space_coinc_far` | `double` \| `null` | Space-and-time-coincidence false alarm rate in Hz from the RAVEN pipeline. Null if no external coincidence was evaluated. | `-` |
| `labels_json` | `string` | JSON-encoded array of label strings attached to this superevent. | `-` |
| `preferred_event_id` | `string` \| `null` | GraceDB event ID of the preferred pipeline event associated with this superevent. Null if no preferred event has been selected. | `-` |
| `pipeline` | `string` \| `null` | Name of the detection pipeline that produced the preferred event, e.g. 'gstlal', 'MBTAOnline', 'SPIIR', 'PyCBC'. Null if not set. | `-` |
| `group` | `string` | Physics group of the preferred event: 'CBC', 'Burst', 'Test', or 'unknown' when not supplied. | `-` |
| `instruments` | `string` \| `null` | Comma-separated list of detector instruments that contributed to the preferred event, e.g. 'H1,L1,V1'. Null if not set. | `-` |
| `gw_id` | `string` \| `null` | Official gravitational wave event name assigned after confirmation. Null if the event has not been confirmed or named. | `-` |
| `submitter` | `string` | Username or service account that submitted the superevent to GraceDB. | `-` |
| `em_type` | `string` \| `null` | Identifier of the associated electromagnetic event from an external trigger. Null if no external EM association exists. | `-` |
| `search` | `string` \| `null` | Search type of the preferred event: 'AllSky', 'MDC', 'BBH', 'EarlyWarning'. Null if not set. | `-` |
| `far_is_upper_limit` | `boolean` \| `null` | Whether the reported FAR value is an upper limit rather than an exact estimate. Null if not set. | `-` |
| `nevents` | `int` \| `null` | Number of pipeline events aggregated into this superevent. Null if not available. | `-` |
| `self_uri` | `string` | HATEOAS self link for the superevent resource in the GraceDB REST API. | `-` |
