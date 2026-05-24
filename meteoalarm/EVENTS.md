# Meteoalarm European Weather Warnings Events

## Topics and Keys

| Topic | Key template | Message group | Event types |
|---|---|---|---|
| `meteoalarm` | `{identifier}` | `Meteoalarm.Warnings` | `WeatherWarning` |

## Event Metadata

- `source`: `https://feeds.meteoalarm.org`
- `time`: CAP `sent` timestamp from the alert

## Event Types

### Meteoalarm.WeatherWarning

Severe weather warning from a European national meteorological service,
distributed through the EUMETNET Meteoalarm system. Follows the CAP
(Common Alerting Protocol) structure.

- `identifier` — CAP alert identifier (key)
- `sender` — issuing met service
- `sent`, `effective`, `onset`, `expires` — temporal fields
- `status` — Actual, Test, Exercise, etc.
- `msg_type` — Alert, Update, Cancel
- `scope` — Public, Restricted, Private
- `country` — feed country name
- `event` — weather event description
- `category` — Met, Geo, etc.
- `severity` — Extreme, Severe, Moderate, Minor
- `urgency` — Immediate, Expected, Future, Past
- `certainty` — Observed, Likely, Possible, Unlikely
- `headline`, `description`, `instruction` — human-readable text
- `awareness_level` — Meteoalarm color-coded level (e.g., "2; yellow; Moderate")
- `awareness_type` — hazard type code (e.g., "1; Wind", "10; Rain")
- `area_desc` — affected geographic areas
- `geocodes` — EMMA_ID / WARNCELLID codes
- `language` — info block language
- `web`, `contact` — reference links

## Data Source

Warnings from 30+ European national meteorological services aggregated by
EUMETNET: `https://feeds.meteoalarm.org/api/v1/warnings/feeds-{country}`

---

## Message Group: Meteoalarm.Warnings.mqtt

MQTT/5.0 transport variant for Meteoalarm CAP weather warnings. Non-retained QoS-1 warning events route by country feed slug, native CAP severity, normalized Meteoalarm awareness type, and CAP identifier under alerts/intl/meteoalarm/meteoalarm/... The awareness_type axis is derived from the Meteoalarm awareness_type parameter label and normalized for MQTT topic safety.

The MQTT transport uses MQTT 5.0 binary-mode CloudEvents: the payload is the JSON body for the referenced message schema, and CloudEvents metadata is carried as MQTT user properties. The MQTT messagegroup references the transport-neutral Kafka/CloudEvents message definitions through `basemessageurl`, so the schemas above remain authoritative.

### MQTT topics

| Topic pattern | Bound message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning` | `Meteoalarm.WeatherWarning` | `false` | `1` | `` |
