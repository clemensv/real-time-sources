# NINA/BBK German Civil Protection Warnings Events

## Topics and Keys

| Topic | Key template | Message group | Event types |
|---|---|---|---|
| `nina-bbk` | `{warning_id}` | `NINA.Warnings` | `CivilWarning` |

## Event Metadata

- `source`: `https://warnung.bund.de`
- `time`: CAP `sent` timestamp

## Event Types

### NINA.CivilWarning

Civil protection warning from Germany's NINA/BBK system (MOWAS, KATWARN, BIWAPP, DWD, LHP, Police).

- `warning_id` — unique NINA warning identifier (key)
- `provider` — source provider: mowas, katwarn, biwapp, dwd, lhp, police
- `version` — warning version number (increments with updates)
- `sender`, `sender_name` — issuing authority ID and name
- `sent` — issued timestamp
- `status` — Actual, Test, etc.
- `msg_type` — Alert, Update, Cancel
- `scope` — Public, Restricted, Private
- `references` — CAP references to prior related warnings
- `event` — event type description (e.g., "Gefahreninformation")
- `event_code` — BBK event code (e.g., "BBK-EVC-067")
- `category`, `severity`, `urgency`, `certainty` — CAP fields
- `headline`, `description`, `instruction` — human-readable text
- `web`, `contact` — links and contact info
- `area_desc` — affected area names
- `verwaltungsbereiche` — German administrative area codes (AGS)
- `language` — info block language

## Data Source

- Map data: `https://warnung.bund.de/api31/{provider}/mapData.json`
- Detail: `https://warnung.bund.de/api31/warnings/{warning_id}.json`

---

## Message Group: NINA.Warnings.mqtt

MQTT/5.0 transport variant for Germany NINA/BBK CAP warnings. Non-retained QoS-1 warning events route by German federal state, native CAP severity, and warning id under alerts/de/nina/nina-bbk/... The state axis is derived from CAP area administrative codes (warnVerwaltungsbereiche) with sender-code fallback.

The MQTT transport uses MQTT 5.0 binary-mode CloudEvents: the payload is the JSON body for the referenced message schema, and CloudEvents metadata is carried as MQTT user properties. The MQTT messagegroup references the transport-neutral Kafka/CloudEvents message definitions through `basemessageurl`, so the schemas above remain authoritative.

### MQTT topics

| Topic pattern | Bound message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `alerts/de/nina/nina-bbk/{state}/{severity}/{warning_id}/warning` | `NINA.CivilWarning` | `false` | `1` | `` |
