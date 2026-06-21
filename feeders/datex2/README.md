# DATEX II real-time traffic feeder

[Events](EVENTS.md) · [Container contract](CONTAINER.md) · [Source contract](xreg/datex2.xreg.json)

DATEX II is the European road-traffic exchange standard used by traffic-management centres to share incidents, roadworks, speed/flow observations, and measurement-site catalogues. This generalized feeder polls a configurable registry of DATEX II XML endpoints and emits normalized CloudEvents so transport operators, journey-planning teams, digital twins, and road-safety analysts can consume multiple road authorities through one contract.

## Scope and upstream hit list

Kept for this build: `SituationPublication`, `MeasuredDataPublication`, `MeasurementSiteTablePublication`, and a future slot for `PredefinedLocationsPublication` reference data. NDW free endpoints studied include incidents/planning feeds, `trafficspeed`, `traveltime`, and `measurement_current` site tables. Bison Futé/French feeders were studied for measured flow and road-event situation profiles. Dropped for now: parking, EV charging, VMS/MSI/DRIP sign-display profiles, and provider-specific non-traffic metadata; those remain later DATEX II profile groups and the existing bespoke feeders are not folded in this PR.

## Transports

| App | Image | Transport | Default shape |
| --- | --- | --- | --- |
| `datex2_kafka` | `ghcr.io/clemensv/real-time-sources-datex2:latest` | Kafka/Event Hubs | Structured CloudEvents on one configured topic. |
| `datex2_mqtt` | `ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest` | MQTT 5 | Binary CloudEvents under `traffic/{country}/{operator}/datex2/...`. |
| `datex2_amqp` | `ghcr.io/clemensv/real-time-sources-datex2-amqp:latest` | AMQP 1.0 | Binary CloudEvents to one queue/topic address. |

Set `DATEX2_ENDPOINTS` to a JSON list of endpoint objects with `id`, `url`, `publication` or `profile`, optional `country`, `operator`, and optional `auth_header`. If omitted, the bridge uses representative no-auth NDW public endpoints. Set `DATEX2_MOCK=true` for deterministic local and Docker E2E validation.

Fabric notebook hosting is included via `notebook/datex2-feed.ipynb` and can be deployed with `tools/deploy-fabric/deploy-feeder-notebook.ps1`.

## Quick start

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2:latest
docker pull ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
```

Kafka/Event Hubs:

```powershell
docker run --rm -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=datex2" -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2:latest
```

MQTT 5:

```powershell
docker run --rm -e MQTT_BROKER_URL="broker:1883" -e MQTT_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
```

AMQP 1.0:

```powershell
docker run --rm -e AMQP_HOST="broker" -e AMQP_ADDRESS="datex2" -e AMQP_USERNAME="user" -e AMQP_PASSWORD="secret" ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
```

## Deploy

[![Deploy Kafka BYO connection](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template.json)
[![Deploy Event Hubs](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventhub.json)
[![Deploy MQTT BYO broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-mqtt.json)
[![Deploy Event Grid MQTT](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventgrid-mqtt.json)
[![Deploy Service Bus AMQP](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-servicebus.json)

See [CONTAINER.md](CONTAINER.md) for the full environment-variable contract and authentication options.
