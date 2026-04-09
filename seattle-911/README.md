# Seattle Fire 911 Bridge

## Overview

**Seattle Fire 911 Bridge** polls the City of Seattle Open Data feed for Seattle Fire Department 911 dispatches and forwards them to Kafka as CloudEvents.

The upstream is the official **Seattle Real Time Fire 911 Calls** dataset on `data.seattle.gov`. The dataset is updated every 5 minutes and exposes machine-readable JSON, CSV, and XML through the Socrata SODA API.

## Upstream Audit

The relevant upstream surface for this source is:

| Family | Transport | Identity | Keep/Drop | Why |
|---|---|---|---|---|
| Fire 911 calls dataset | Socrata SODA JSON `/resource/kzjm-xkqj.json` | `incident_number` | Keep | This is the live dispatch feed. |
| Dataset metadata | Socrata view metadata `/api/views/kzjm-xkqj` | n/a | Keep for docs only | Useful for field descriptions, not a business entity stream. |
| CSV/XML/RDF exports | Alternate renderings of same dataset | `incident_number` | Drop | Duplicate presentation of the same records. |
| Seattle police/public safety datasets nearby | Separate datasets | separate | Drop | Different upstream semantics and lifecycle. |

This source models the live dispatch feed only. The dataset does not expose a separate reference catalog for incident types or stations, so there is no reference-data event family to emit.

## Event Model

- **Incident** — one Seattle Fire Department 911 dispatch record keyed by `incident_number`

Dropped upstream fields:

- `report_location` — duplicate geometry presentation of `latitude` and `longitude`
- Socrata `:@computed_region_*` fields — platform-derived geographies, not authoritative incident fields

## Running

```bash
python -m seattle_911 --connection-string "BootstrapServer=localhost:9092;EntityPath=seattle-911"
```

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Kafka/Event Hubs/Fabric connection string |
| `SEATTLE_911_LAST_POLLED_FILE` | State file path for dedupe and resume state |

## Upstream Links

- Dataset page: https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj
- SODA endpoint: https://data.seattle.gov/resource/kzjm-xkqj.json
- Socrata API docs: https://dev.socrata.com/
