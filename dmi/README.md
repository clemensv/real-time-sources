# DMI Observation Triad → Apache Kafka & MQTT/UNS

## Overview

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.dmi.dk/>
- API / data documentation: <https://opendatadocs.dmi.govcloud.dk/>

<!-- upstream-links:end -->

**DMI** is a bridge that polls the [Danish Meteorological Institute Open Data
API](https://opendatadocs.dmi.govcloud.dk/) and re-emits the **observation
triad** (`metObs` + `oceanObs` + `lightningData`) as CloudEvents. A single
upstream poller feeds two transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-dmi-kafka` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | Single topic `dmi`, JSON CloudEvents (binary mode), keys = stable upstream identifiers |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-dmi-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `weather/dk/dmi/…` and `ocean/dk/dmi/…`, JSON body, CloudEvent attributes as MQTT 5 user properties, retained at QoS 1 |

> **Lightning is Kafka-only.** Per-strike events have no natural last-known-value
> shape, so the MQTT image publishes only `metObs` and `oceanObs` and skips
> `lightningData`.

## CloudEvent types

| Type | Source | Key / subject template | Retained on MQTT |
|---|---|---|---|
| `dk.dmi.metObs.Station` | metObs | `{station_id}` | yes |
| `dk.dmi.metObs.Observation` | metObs | `{station_id}/{parameter_id}` | yes |
| `dk.dmi.oceanObs.OceanStation` | oceanObs | `{station_id}` | yes |
| `dk.dmi.oceanObs.OceanObservation` | oceanObs | `{station_id}/{parameter_id}` | yes |
| `dk.dmi.oceanObs.TidewaterStation` | oceanObs | `{station_id}` | yes |
| `dk.dmi.oceanObs.TidewaterPrediction` | oceanObs | `{station_id}` | yes |
| `dk.dmi.lightning.Sensor` | lightningData | `{sensor_id}` | — (Kafka only) |
| `dk.dmi.lightning.Strike` | lightningData | `{strike_id}` | — (Kafka only) |

All three messagegroups multiplex onto the **single** Kafka topic `dmi`.
Subscribers route by CloudEvent `type`. Full schemas are in
[EVENTS.md](EVENTS.md); KQL ingestion in [kql/dmi.kql](kql/dmi.kql).

## Repository Layout

```
dmi/
  xreg/dmi.xreg.json            # shared xRegistry contract
  dmi_core/                     # transport-agnostic acquisition + config
  dmi_kafka/                    # Kafka feeder (metObs + oceanObs + lightning)
  dmi_mqtt/                     # MQTT/UNS feeder  (metObs + oceanObs)
  dmi_producer/                 # xrcg-generated Kafka producer
  dmi_mqtt_producer/            # xrcg-generated MQTT producer
  Dockerfile.kafka              # Kafka image
  Dockerfile.mqtt               # MQTT image
  kql/dmi.kql                   # KQL schema for Fabric Eventhouse / ADX
  notebook/dmi-feed.ipynb       # Fabric notebook feeder (Kafka path)
  azure-template*.json          # four one-click ACI deploy templates
  tests/                        # unit + integration tests
```

## API keys

Every DMI API requires a per-API key from
[https://dmiapi.govcloud.dk/](https://dmiapi.govcloud.dk/) sent in the
`X-Gravitee-Api-Key` header. Provide one of:

* `DMI_METOBS_API_KEY` / `DMI_OCEANOBS_API_KEY` / `DMI_LIGHTNING_API_KEY` —
  per-API keys.
* `DMI_API_KEY` — fallback used for any API without a dedicated key.

The MQTT image ignores `DMI_LIGHTNING_API_KEY`.

Rate limits: **500 req / 5 s** per key (DMI public quota).

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="$EVENT_HUBS_CONNECTION_STRING" \
  -e DMI_METOBS_API_KEY="$DMI_METOBS_API_KEY" \
  -e DMI_OCEANOBS_API_KEY="$DMI_OCEANOBS_API_KEY" \
  -e DMI_LIGHTNING_API_KEY="$DMI_LIGHTNING_API_KEY" \
  ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
```

### MQTT / UNS

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://broker.example.com:8883 \
  -e MQTT_USERNAME=alice \
  -e MQTT_PASSWORD=secret \
  -e DMI_METOBS_API_KEY="$DMI_METOBS_API_KEY" \
  -e DMI_OCEANOBS_API_KEY="$DMI_OCEANOBS_API_KEY" \
  ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
```

Topics published (retained, QoS 1):

```
weather/dk/dmi/met-obs/{station_id}/info
weather/dk/dmi/met-obs/{station_id}/{parameter_id}
ocean/dk/dmi/ocean-obs/{station_id}/info
ocean/dk/dmi/ocean-obs/{station_id}/{parameter_id}
ocean/dk/dmi/tidewater/{station_id}/info
ocean/dk/dmi/tidewater/{station_id}/prediction
```

## Configuration knobs

Both images share these upstream-side knobs:

* `POLLING_INTERVAL` — seconds between polling cycles (default `300`).
* `STATE_FILE` — path to the dedupe state file.
* `ONCE_MODE=true` — single cycle and exit.
* `DMI_OBSERVATION_PERIOD` — DMI period filter (default `latest-hour`).
* `DMI_REFERENCE_REFRESH_HOURS` — re-emit reference data every N hours
  (default `6`).

Transport-specific knobs are listed in [CONTAINER.md](CONTAINER.md).

## Deploying into Azure Container Instances

Four one-click templates are available — see [CONTAINER.md](CONTAINER.md)
for the badges and full parameter lists:

| Template | Purpose |
|---|---|
| `azure-template.json` | Kafka image, bring your own Event Hub |
| `azure-template-with-eventhub.json` | Kafka image + new Event Hubs namespace |
| `azure-template-mqtt.json` | MQTT image, bring your own broker |
| `azure-template-with-eventgrid-mqtt.json` | MQTT image + new Event Grid namespace MQTT broker |

## Upstream

* DMI Open Data Portal: <https://opendatadocs.dmi.govcloud.dk/>
* MetObs Bulk: <https://opendatadocs.dmi.govcloud.dk/APIs/MetObsAPI>
* OceanObs Bulk: <https://opendatadocs.dmi.govcloud.dk/APIs/OceanObsAPI>
* Lightning: <https://opendatadocs.dmi.govcloud.dk/APIs/LightningDataAPI>
* Data licence: [Creative Commons Attribution (CC BY 4.0)](https://www.dmi.dk/vejrarkiv/about-dmi/about-dmis-data/).
