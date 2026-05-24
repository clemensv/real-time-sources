# Seattle Fire 911 Bridge Events

This document describes the events emitted by the Seattle Fire 911 bridge.

- [US.WA.Seattle.Fire911](#message-group-uswaseattlefire911)
  - [US.WA.Seattle.Fire911.Incident](#message-uswaseattlefire911incident)

---

## Message Group: US.WA.Seattle.Fire911
---
### Message: US.WA.Seattle.Fire911.Incident
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `US.WA.Seattle.Fire911.Incident` |
| `source` |  | `` | `False` | `https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj` |
| `subject` |  | `uritemplate` | `False` | `{incident_number}` |

#### Schema:
##### Object: Incident
*Seattle Fire Department 911 dispatch record from the City of Seattle real-time fire calls dataset.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `incident_number` | *string* | - | `True` | Stable Seattle Fire Department incident identifier for the dispatch record. |
| `incident_type` | *string* | - | `True` | Seattle Fire Department response type for the incident, such as Aid Response or Medic Response. |
| `incident_datetime` | *string* | - | `True` | Date and time of the call as published by the Seattle Open Data dataset, in local dataset timestamp form without an explicit UTC offset. |
| `address` | *string* (optional) | - | `False` | Incident location text as published by the dataset. |
| `latitude` | *double* (optional) | - | `False` | Latitude of the incident location in decimal degrees north. |
| `longitude` | *double* (optional) | - | `False` | Longitude of the incident location in decimal degrees east of Greenwich; Seattle values are negative because they lie west of Greenwich. |

---

## Message Group: US.WA.Seattle.Fire911.mqtt

MQTT/5.0 transport variant for Seattle Fire 911 dispatch incidents. Topics are non-retained QoS-1 event messages under civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}. The incident_type_slug field is the deterministic lowercase kebab-case routing key derived from the display incident_type; incident_number preserves the CloudEvents subject/Kafka key for per-incident subscriptions. Message expiry is 86400 seconds for queued/offline delivery only; this event stream does not use retained MQTT state.

The MQTT transport uses MQTT 5.0 binary-mode CloudEvents: the payload is the JSON body for the referenced message schema, and CloudEvents metadata is carried as MQTT user properties. The MQTT messagegroup references the transport-neutral Kafka/CloudEvents message definitions through `basemessageurl`, so the schemas above remain authoritative.

### MQTT topics

| Topic pattern | Bound message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}` | `US.WA.Seattle.Fire911.Incident` | `false` | `1` | `86400` |
