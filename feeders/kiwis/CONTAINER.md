# KiWIS container contract

[Overview](README.md) · [Events](EVENTS.md) · [xRegistry contract](xreg/kiwis.xreg.json)

The KiWIS images publish hydrological station reference data, timeseries metadata, and latest observation values from configurable KISTERS KiWIS REST endpoints as CloudEvents.

## Image contract

| Image tag | Transport | Dockerfile | State |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-kiwis:latest` | Kafka/Event Hubs/Fabric | `Dockerfile.kafka` | `KIWIS_STATE_FILE` optional |
| `ghcr.io/clemensv/real-time-sources-kiwis-mqtt:latest` | MQTT 5 | `Dockerfile.mqtt` | `KIWIS_STATE_FILE` optional |
| `ghcr.io/clemensv/real-time-sources-kiwis-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | `KIWIS_STATE_FILE` optional |

## Common environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `KIWIS_SOURCES_FILE` | Path to a JSON catalog with KiWIS/KISTERS source entries. Mount your own copy when you need private agency endpoints or different station/timeseries filters. | Packaged catalog |
| `KIWIS_SOURCES` | Comma-separated catalog entry `name`s to run, or `*` for every entry including disabled templates. When unset, entries with `enabled: true` run. | enabled entries |
| `KIWIS_ENDPOINTS` | Legacy inline CSV/JSON endpoint list or `@file`: `kiwis_id,base_url,datasource,station_filter,timeseries_filter,ts_ids,period,api_key`. Takes precedence over the catalog whenever it is set. | unset |
| `KIWIS_MOCK` | `true` emits one offline station, timeseries, and value for E2E. | `false` |
| `KIWIS_MAX_TIMESERIES` | Safety cap for discovered timeseries per endpoint. | `10` |
| `POLLING_INTERVAL` | Seconds between polling cycles. | `300` |
| `KIWIS_STATE_FILE` | JSON dedupe state path used by container and Azure templates. | none |
| `STATE_FILE` | Alternate state file environment variable used by Fabric notebook hosting. | none |
| `LOG_LEVEL` | Python logging level. | `INFO` |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |  |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra ID (Azure Event Grid). |  |
| `MQTT_ENABLE_TLS` | Set `true` to use TLS (`mqtts`) for the MQTT connection. |  |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |  |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |  |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS. |  |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |  |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |  |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |  |

### Catalog format

The packaged catalog lives at `kiwis_core/kiwis_core/sources/kiwis-sources.json` inside the source tree and is included in the wheel/container image.

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
| `base_url` | ✅ | KiWIS QueryServices endpoint URL. |
| `datasource` | ❌ | KiWIS datasource number passed to QueryServices; defaults to `0`. |
| `station_filter` | ❌ | Filter string for `getStationList`. |
| `timeseries_filter` | ❌ | Filter string for `getTimeseriesList`. |
| `ts_ids` | ❌ | Optional comma-separated allow-list of timeseries IDs to fetch values for. |
| `period` | ❌ | Query period passed to `getTimeseriesValues`; defaults to `PT6H`. |
| `api_key` | ❌ | Optional KiWIS API key. Use `${ENV_VAR}` or `$ENV_VAR` so secrets come from the runtime environment. |

### Selecting sources

- Unset `KIWIS_SOURCES` — poll every catalog entry with `enabled: true`.
- `KIWIS_SOURCES=sepa-scotland` — poll only that entry.
- `KIWIS_SOURCES=agency-b,agency-a` — poll named entries in the requested order.
- `KIWIS_SOURCES=*` — load every entry, including disabled templates.
- Unknown names fail fast with a `ValueError` that lists known names.

### Keeping secrets out of the catalog

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

KiWIS/KISTERS is a hydrology data platform deployed by water agencies including SEPA Scotland, the Australian Bureau of Meteorology, and German state water portals. This image ships the verified SEPA Scotland entry enabled, two disabled Australian Bureau of Meteorology entries (Water Data Online + Water Storage), and a disabled key-protected template; add other publishers by mounting your own catalog.

| Catalog name | Status | Publisher | Public URL / notes |
| --- | --- | --- | --- |
| `sepa-scotland` | Shipped enabled | Scottish Environment Protection Agency time-series service | `https://timeseries.sepa.org.uk/KiWIS/KiWIS` |
| `bom-australia-water` | Shipped disabled | Australian Bureau of Meteorology — Water Data Online (~3500+ level/discharge/rainfall stations, CC BY 3.0 AU) | `https://www.bom.gov.au/waterdata/services` |
| `bom-australia-storage` | Shipped disabled | Australian Bureau of Meteorology — Water Storage (~613 reservoirs/dams, Storage Volume, CC BY 3.0 AU) | `https://www.bom.gov.au/waterdata/services` |
| `key-protected-template` | Shipped disabled template | Any KiWIS/KISTERS publisher that requires a key | Replace the catalog's placeholder with the publisher's real KiWIS service URL. |
| not shipped | Known KiWIS/KISTERS publisher to configure separately | Bayerisches Landesamt für Umwelt / Gewässerkundlicher Dienst Bayern | `https://www.gkd.bayern.de/` |

## Kafka

```powershell
docker run --rm -e CONNECTION_STRING='BootstrapServer=broker:9092;EntityPath=kiwis' -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-kiwis:latest
```

Kafka also accepts `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, and `SASL_PASSWORD`.

## MQTT

```powershell
docker run --rm -e MQTT_BROKER_URL='broker:1883' -e MQTT_USERNAME=user -e MQTT_PASSWORD=secret ghcr.io/clemensv/real-time-sources-kiwis-mqtt:latest
```

MQTT variables: `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, plus the common KiWIS variables.

## AMQP 1.0

```powershell
docker run --rm -e AMQP_BROKER_URL='amqp://user:password@broker:5672/kiwis' ghcr.io/clemensv/real-time-sources-kiwis-amqp:latest
```

AMQP variables: `AMQP_BROKER_URL`, `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_TLS`, plus common KiWIS variables.

## Azure templates

This source ships generated templates for Kafka/Event Hubs, MQTT/Event Grid namespace, and AMQP/Service Bus. Use the portal buttons after the PR is merged; no live Azure/Fabric deployment was performed in this PR.
