# GraceDB Gravitational Wave Candidate Alert Events

This document describes the events emitted by the GraceDB bridge.

- [org.ligo.gracedb](#message-group-orgligogracedb)
  - [org.ligo.gracedb.Superevent](#message-orgligogracedbsuperevent)

---

## Message Group: org.ligo.gracedb

---

### Message: org.ligo.gracedb.Superevent

*A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `org.ligo.gracedb.Superevent` |
| `source` | Source URI | `uritemplate` | `True` | `{source_uri}` |
| `subject` | Superevent identifier | `uritemplate` | `True` | `{superevent_id}` |
| `time` | Creation time | `uritemplate` | `True` | `{created}` |

#### Schema: org.ligo.gracedb.Superevent (Avro)

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `superevent_id` | `string` | Unique identifier for the superevent assigned by GraceDB. |
| `category` | `string` | Category: 'Production', 'MDC', or 'Test'. |
| `created` | `string` | ISO-8601 UTC timestamp when the superevent was created. |
| `t_start` | `double` | GPS time marking the start of the superevent time window. |
| `t_0` | `double` | GPS time of the central trigger time. |
| `t_end` | `double` | GPS time marking the end of the superevent time window. |
| `far` | `double` | False alarm rate in Hz. Lower = more significant. |
| `time_coinc_far` | `double?` | Time-coincidence false alarm rate in Hz from RAVEN. |
| `space_coinc_far` | `double?` | Space-and-time-coincidence false alarm rate in Hz from RAVEN. |
| `labels_json` | `string` | JSON-encoded array of label strings (e.g. EM_READY, GCN_PRELIM_SENT). |
| `preferred_event_id` | `string?` | GraceDB event ID of the preferred pipeline event. |
| `pipeline` | `string?` | Detection pipeline name (gstlal, MBTAOnline, SPIIR, PyCBC). |
| `group` | `string?` | Physics group: CBC, Burst, or Test. |
| `instruments` | `string?` | Comma-separated detector list (H1,L1,V1,K1). |
| `gw_id` | `string?` | Official gravitational wave event name after confirmation. |
| `submitter` | `string` | Username or service that submitted the superevent. |
| `em_type` | `string?` | Electromagnetic event ID from external trigger. |
| `search` | `string?` | Search type: AllSky, MDC, BBH, EarlyWarning. |
| `far_is_upper_limit` | `boolean?` | Whether FAR is an upper limit. |
| `nevents` | `int?` | Number of pipeline events aggregated. |
| `self_uri` | `string` | HATEOAS self link for the superevent in the GraceDB API. |
