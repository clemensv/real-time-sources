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
