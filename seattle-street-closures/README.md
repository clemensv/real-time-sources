# Seattle Street Closures Bridge

## Overview

**Seattle Street Closures Bridge** polls the City of Seattle Open Data street closures dataset and emits one event per permitted closed street segment occurrence window.

The upstream dataset is the official **Street Closures** feed published by the Seattle Department of Transportation on `data.seattle.gov`. The dataset covers short-term street closures from issued street-use permits for non-construction activities such as block parties, play streets, farmers markets, and temporary activations.

## Upstream Audit

| Family | Transport | Identity | Keep/Drop | Why |
|---|---|---|---|---|
| Street Closures dataset | Socrata SODA JSON `/resource/ium9-iqtc.json` | `permit_number|segkey|start_date|end_date` | Keep | This is the closure event feed. |
| GeoJSON render | `/resource/ium9-iqtc.geojson` | same | Drop as separate family | Same records, alternate representation. |
| Dataset metadata | `/api/views/ium9-iqtc` | n/a | Keep for docs only | Useful for descriptions, not a separate stream. |
| Street use permit datasets | separate Socrata datasets | permit model | Drop | Upstream permit-issuance tables are not the closure event feed. |
| Street Network Database (SND) | separate Socrata dataset | `segkey` | Drop | Useful join table, but not part of the requested closure stream and it does not share the closure event identity. |

The bridge models closure rows only. It intentionally does not model permit issuance tables or the citywide street network as event families because they follow different lifecycles and identities.

## Event Model

- **StreetClosure** — one closed street segment occurrence window keyed by `closure_id`

The bridge derives `closure_id` from `permit_number`, `segkey`, `start_date`, and `end_date` because `permit_number` alone is not unique enough for closure rows.

## Running

```bash
python -m seattle_street_closures --connection-string "BootstrapServer=localhost:9092;EntityPath=seattle-street-closures"
```

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Kafka/Event Hubs/Fabric connection string |
| `SEATTLE_STREET_CLOSURES_STATE_FILE` | Path to persisted snapshot state |

## Upstream Links

- Dataset page: https://data.seattle.gov/Built-Environment/Street-Closures/ium9-iqtc
- SODA endpoint: https://data.seattle.gov/resource/ium9-iqtc.json
- API docs: https://dev.socrata.com/foundry/data.seattle.gov/ium9-iqtc
