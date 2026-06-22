# KiWIS

[Events](EVENTS.md) · [Container deployment](CONTAINER.md) · [xRegistry contract](xreg/kiwis.xreg.json)

KiWIS turns public KISTERS Web Interoperability Solution hydrological databases into streaming CloudEvents. Water agencies, flood-warning teams, researchers, and operations dashboards can subscribe to consistent station catalogs, timeseries metadata, and live values from many KiWIS instances without writing one bespoke integration per authority.

The feeder is generalized by configuration. `KIWIS_ENDPOINTS` accepts CSV lines (`kiwis_id,base_url,datasource,station_filter,timeseries_filter,ts_ids,period,api_key`) or a JSON array, and may also point at `@file`. The shipped default uses the public, key-less SEPA Scotland KiWIS endpoint.

## Upstream API audit

| Request | Family | Decision |
| --- | --- | --- |
| `getRequestInfo` | capability discovery | Used during audit and diagnostics; not emitted because it describes the service surface, not a hydrological entity. |
| `getStationList` | station reference | Kept as `org.kiwis.Station`, keyed `{kiwis_id}/{station_id}`. |
| `getParameterList`, `getParameterTypeList` | parameter reference | Reviewed; parameter labels used from `getTimeseriesList`. Dedicated parameter events are not emitted because timeseries metadata already carries the parameter context needed by values. |
| `getTimeseriesChanges` / `changedSince` filters | delta discovery | Reviewed; not emitted as its own event family because it is a polling optimization/change index for timeseries already modeled by `Timeseries` and `TimeseriesValue`. The bridge uses state-based dedupe and can add `changedSince` later without changing the event contract. |
| Graph, layer, comments, release-state, ensemble requests | presentation or specialized extensions | Dropped for this generalized public default because they are either visualization helpers, optional quality workflow metadata, or specialized products not consistently available on public keyless instances. |
| `getTimeseriesList` | timeseries catalog | Kept as `org.kiwis.Timeseries`, keyed `{kiwis_id}/{ts_id}`. |
| `getTimeseriesValues` | telemetry | Kept as `org.kiwis.TimeseriesValue`, keyed `{kiwis_id}/{ts_id}`. |

Validated public instance: `https://timeseries.sepa.org.uk/KiWIS/KiWIS`. SEPA returned station fields `station_id`, `station_no`, `station_name`, `station_latitude`, `station_longitude`, `river_name`, `catchment_name`; timeseries fields including `ts_id`, station linkage, parameter labels, `ts_unitname`, `ts_unitsymbol`, and coverage; values as `Timestamp,Value,Quality Code` rows.

## Transports

| Variant | Image | Delivery shape |
| --- | --- | --- |
| Kafka | `ghcr.io/clemensv/real-time-sources-kiwis:latest` | Structured CloudEvents to Kafka/Event Hubs/Fabric Eventstream topic `kiwis`. |
| MQTT | `ghcr.io/clemensv/real-time-sources-kiwis-mqtt:latest` | Binary-mode MQTT 5 CloudEvents under `hydro/kiwis/{kiwis_id}/...`, retained QoS 1. |
| AMQP 1.0 | `ghcr.io/clemensv/real-time-sources-kiwis-amqp:latest` | Binary-mode CloudEvents to one AMQP address for Service Bus or generic brokers. |

Fabric notebook hosting is available via `tools/deploy-fabric/deploy-feeder-notebook.ps1`; the notebook runs the Kafka feeder in `--once` mode and looks up the Event Stream connection string at runtime.

## Quick start

Kafka/Event Hubs using the packaged default catalog:

```powershell
docker run --rm `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=kiwis" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-kiwis:latest
```

Select the shipped SEPA entry explicitly:

```powershell
docker run --rm `
  -e KIWIS_SOURCES="sepa-scotland" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=kiwis" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-kiwis:latest
```

## Configuring sources

The feeder ships a checked-in source catalog at `kiwis_core/kiwis_core/sources/kiwis-sources.json`. Use the catalog for repeatable deployments and keep `KIWIS_ENDPOINTS` as a one-off override.

| Variable | Purpose | Default |
| --- | --- | --- |
| `KIWIS_SOURCES_FILE` | Path to a JSON catalog with KiWIS/KISTERS source entries. Mount your own copy when you need private agency endpoints or different station/timeseries filters. | Packaged catalog |
| `KIWIS_SOURCES` | Comma-separated catalog entry `name`s to run, or `*` for every entry including disabled templates. When unset, entries with `enabled: true` run. | enabled entries |
| `KIWIS_ENDPOINTS` | Legacy inline CSV/JSON endpoint list or `@file`. Takes precedence over the catalog whenever it is set. | unset |

### Catalog format

```json
{
  "description": "KiWIS/KISTERS source catalog...",
  "sources": [
    {
      "name": "sepa-scotland",
      "enabled": true,
      "description": "Scottish Environment Protection Agency public KiWIS endpoint.",
      "kiwis_id": "sepa",
      "base_url": "https://timeseries.sepa.org.uk/KiWIS/KiWIS",
      "datasource": "0",
      "station_filter": "station_id=36870",
      "timeseries_filter": "station_id=36870",
      "ts_ids": "65452010",
      "period": "PT6H",
      "api_key": ""
    }
  ]
}
```

| Field | Required | Description |
| --- | ---: | --- |
| `name` | ✅ | Stable catalog selector used by `KIWIS_SOURCES`. |
| `enabled` | ❌ | Defaults to `true`; disabled templates are skipped unless `KIWIS_SOURCES=*` or selected by name. |
| `description` | ✅ | Human-readable publisher, geography, and access notes. |
| `kiwis_id` | ✅ | Stable source identifier emitted in event keys and subjects. |
| `base_url` | ✅ | KiWIS QueryServices endpoint URL, for example `https://timeseries.sepa.org.uk/KiWIS/KiWIS`. |
| `datasource` | ❌ | KiWIS datasource number passed to QueryServices; defaults to `0`. |
| `station_filter` | ❌ | Filter string for `getStationList`, such as `station_id=36870`. |
| `timeseries_filter` | ❌ | Filter string for `getTimeseriesList`, such as `station_id=36870`. |
| `ts_ids` | ❌ | Optional comma-separated allow-list of timeseries IDs to fetch values for. |
| `period` | ❌ | Query period passed to `getTimeseriesValues`; defaults to `PT6H`. |
| `api_key` | ❌ | Optional KiWIS API key. Use `${ENV_VAR}` or `$ENV_VAR` so secrets come from the runtime environment. |

### Selecting sources

- Unset `KIWIS_SOURCES` — poll every catalog entry with `enabled: true`.
- `KIWIS_SOURCES=sepa-scotland` — poll only that entry.
- `KIWIS_SOURCES=agency-b,agency-a` — poll named entries in the requested order.
- `KIWIS_SOURCES=*` — load every entry, including disabled templates. This is mostly useful for validation after editing a private catalog.
- Unknown names fail fast with a `ValueError` that lists known names.

### Keeping secrets out of the catalog

Put placeholders in the catalog and provide the secret at runtime:

```powershell
docker run --rm `
  -v ${PWD}\my-kiwis.sources.json:/app/kiwis-sources.json:ro `
  -e KIWIS_SOURCES_FILE="/app/kiwis-sources.json" `
  -e KIWIS_SOURCES="private-agency" `
  -e SOME_KIWIS_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=kiwis" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-kiwis:latest
```

### Known KiWIS/KISTERS sources

KiWIS/KISTERS is a hydrology data platform used by many water agencies. This feeder ships the already verified SEPA Scotland public default (enabled), two disabled Australian Bureau of Meteorology entries (Water Data Online + Water Storage, same KiWIS protocol), and one disabled template for private or key-protected KiWIS hosts; add other publishers by copying the catalog and choosing filters that match the contract.

| Catalog name | Status | Publisher | Public URL / notes |
| --- | --- | --- | --- |
| `sepa-scotland` | Shipped enabled | Scottish Environment Protection Agency time-series service | `https://timeseries.sepa.org.uk/KiWIS/KiWIS` |
| `bom-australia-water` | Shipped disabled | Australian Bureau of Meteorology — Water Data Online (~3500+ level/discharge/rainfall stations, CC BY 3.0 AU) | `https://www.bom.gov.au/waterdata/services` |
| `bom-australia-storage` | Shipped disabled | Australian Bureau of Meteorology — Water Storage (~613 reservoirs/dams, Storage Volume, CC BY 3.0 AU) | `https://www.bom.gov.au/waterdata/services` |
| `key-protected-template` | Shipped disabled template | Any KiWIS/KISTERS publisher that requires a key | Replace the catalog's placeholder with the publisher's real KiWIS service URL. |
| not shipped | Known KiWIS/KISTERS publisher to configure separately | Bayerisches Landesamt für Umwelt / Gewässerkundlicher Dienst Bayern | `https://www.gkd.bayern.de/` |

Default polling is 300 seconds, well below the practical rate pressure for a small configured timeseries set; SEPA's public KiWIS endpoint did not publish an explicit rate-limit statement in the audited response.
