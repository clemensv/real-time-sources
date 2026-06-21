<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# FDSN Seismology

<sub>8 federated FDSN nodes · Kafka · MQTT · AMQP · <a href="https://www.fdsn.org/webservices/">upstream</a> · <a href="https://geofon.gfz-potsdam.de/fdsnws/event/1/application.wadl">event WADL</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global earthquake detections from pre-configured FDSN event-service nodes

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#fdsn-seismology) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#fdsn-seismology/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/fdsn-seismology.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.fdsn.org/webservices/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the federated **FDSN Event** web-service ecosystem into one CloudEvents stream over **Kafka**, **MQTT 5.0**, or **AMQP 1.0**. It bakes in eight confirmed working nodes and polls them as one planet-scale deployment artifact, with optional `--nodes` and `--exclude-nodes` filters for region-specific deployments.

<!-- upstream-links:begin -->
## Upstream

- FDSN Web Services overview: <https://www.fdsn.org/webservices/>
- Representative FDSN Event WADL: <https://geofon.gfz-potsdam.de/fdsnws/event/1/application.wadl>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published images, environment variables, and Azure deployment shapes.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, JsonStructure schemas, and per-transport routing.

## Why this bridge

The International Federation of Digital Seismograph Networks (**FDSN**) defines a standard event query API that many seismic institutions implement. Change the base URL and the same query works against a different node. That interoperability is great for human analysts, but downstream systems still end up writing polling loops, node catalogs, dedupe logic, and three different transport adapters.

This feeder does that once and republishes the result as typed CloudEvents:

- **Global situational awareness** — combine aggregator nodes and authoritative regional nodes from one deployment.
- **Fabric / Eventhouse ingestion** — land reference node metadata and earthquake detections with one contract.
- **Selective regional routing** — include only `ingv,ethz,resif` for Europe, or exclude a noisy node without rebuilding the image.
- **Transport choice without contract drift** — the Kafka, MQTT, and AMQP variants emit the same `Node` and `Earthquake` payloads.

## Overview

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-fdsn-seismology` | Apache Kafka 2.x compatible (Azure Event Hubs, Fabric Event Streams, plain Kafka) | One topic, structured CloudEvents, keys `{contributor}/{event_id}` for earthquakes and `{node_id}` for node reference records |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-fdsn-seismology-mqtt` | MQTT 5.0 brokers (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT) | UNS tree under `seismology/fdsn/...`, QoS 1, retained `Node` records, non-retained `Earthquake` events |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-fdsn-seismology-amqp` | AMQP 1.0 brokers and Azure Service Bus / Event Hubs | Single AMQP address, binary CloudEvents, SASL PLAIN / SAS CBS / Entra ID via AMQP CBS |

All three variants share:

- the built-in node catalog in [`fdsn_seismology_core/nodes.py`](fdsn_seismology_core/nodes.py)
- the shared parser / polling logic in [`fdsn_seismology_core/fdsn_client.py`](fdsn_seismology_core/fdsn_client.py)
- the xRegistry contract in [`xreg/fdsn-seismology.xreg.json`](xreg/fdsn-seismology.xreg.json)

## Built-in node catalog

| Node ID | Institution | Base URL | Coverage |
|---|---|---|---|
| `emsc` | EMSC | `https://www.seismicportal.eu/fdsnws/event/1/application.wadl` | Global aggregator |
| `gfz` | GFZ GEOFON | `https://geofon.gfz-potsdam.de/fdsnws/event/1/` | Global M4+ |
| `ingv` | INGV | `https://webservices.ingv.it/fdsnws/event/1/` | Italy + Mediterranean |
| `ethz` | ETHZ/SED | `https://eida.ethz.ch/fdsnws/event/1/` | Switzerland + Alpine |
| `resif` | RESIF | `https://ws.resif.fr/fdsnws/event/1/` | France + global M5+ |
| `ipgp` | IPGP | `https://ws.ipgp.fr/fdsnws/event/1/` | Mayotte volcanic swarm |
| `niep` | NIEP | `https://eida-sc3.infp.ro/fdsnws/event/1/` | Romania + Vrancea |
| `usgs` | USGS Earthquake Hazards Program | `https://earthquake.usgs.gov/fdsnws/event/1/` | Global earthquake catalog |

The feeder emits all eight as `org.fdsn.event.Node` reference events at startup before the first earthquake poll cycle. Select only USGS with `FDSN_NODES=usgs` (or `NODES=usgs`).

## Upstream channel review

The FDSN Event API surface reviewed for this source is:

| Channel | Example path | Keep? | Reason |
|---|---|---|---|
| Earthquake query | `/query?format=text&orderby=time&starttime=...` | **Keep** | This is the real-time / near-real-time event feed the source exists to stream. |
| Catalog index | `/catalogs` | Drop | Metadata list only; duplicates node-level or event-level provenance already carried in payload fields. |
| Contributor index | `/contributors` | Drop | Metadata list only; contributor codes already appear on earthquake records. |
| Version | `/version` | Drop | Operational service metadata, not reference data for earthquake entities. |
| Service description | `/application.wadl` | Drop | Static API contract, useful for implementation but not a streamable domain entity. |

## Data model

The feeder emits two event families in one source contract:

| CloudEvents type | Description |
|---|---|
| `org.fdsn.event.Node` | Reference data for one configured FDSN node. |
| `org.fdsn.event.Earthquake` | One earthquake detection record in normalized FDSN text-format shape. |

Earthquakes use the stable identity `{contributor}/{event_id}`. Node reference records use `{node_id}`.

## Polling and dedupe behavior

- Default poll interval: **60 seconds**
- Query shape: `query?format=text&orderby=time&starttime=<last-poll>&limit=500`
- Optional filter: `--min-magnitude`
- Cross-node dedupe key: `{contributor}/{event_id}`
- Restart persistence: `STATE_FILE` stores per-node poll cursors plus last-seen event timestamps

## USGS parity analysis and fold-in recommendation

The `usgs` node uses the USGS FDSN Event endpoint verified at `https://earthquake.usgs.gov/fdsnws/event/1/`: `/version` returned `2.4.0`, and `query?format=text&limit=1&orderby=time&starttime=2026-06-19T00:00:00Z` returned pipe-delimited event rows.

Do **not** treat this node as a parity replacement for the bespoke [`usgs-earthquakes`](../usgs-earthquakes/) feeder:

| Capability | Bespoke `usgs-earthquakes` | FDSN `usgs` node | Parity |
|---|---|---|---|
| Upstream endpoint | USGS GeoJSON summary feeds such as `earthquakes/feed/v1.0/summary/all_hour.geojson` | FDSN Event `query?format=text&orderby=time&starttime=...` | Different upstream surface |
| Latency/cadence | Polls once per minute by default | Polls once per minute by default | No sub-minute behavior in current code; cadence can match |
| Updates/corrections | Tracks the GeoJSON `updated` timestamp and republishes changed events | Dedupe is keyed by origin `time`; FDSN text has no `updated` field | **Lost** |
| Deletes/retractions | Schema carries `status` including `deleted`; changed `updated` values can republish that state | FDSN text schema has no `status` field | **Lost** |
| Payload fields | Includes GeoJSON-specific fields: `url`, `detail_url`, `felt`, `cdi`, `mmi`, `alert`, `status`, `tsunami`, `sig`, `net`, `code`, `sources`, `nst`, `dmin`, `rms`, `gap`, `magnitude_bucket` | Normalized FDSN text fields only: origin, hypocenter, magnitude, provenance, location name, node URL | **Lost** |
| Routing identity | `{net}/{code}` | `{contributor}/{event_id}` | Different key/subject shape |

**RECOMMENDATION: DO-NOT-FOLD.** Adding USGS as an FDSN node is useful for federated catalog polling, but folding the bespoke `usgs-earthquakes` feeder into this FDSN poller would lose update/correction semantics, delete/retraction visibility, GeoJSON-specific fields, and the existing `{net}/{code}` routing identity. A future fold-in would need a USGS GeoJSON real-time mode in `fdsn-seismology` that preserves the current GeoJSON schema, `updated`-based dedupe, `status=deleted` propagation, and transport keys before retiring the bespoke feeder.

## Fabric Notebook

Because this source is poll-based, it ships a Fabric notebook at [`notebook/fdsn-seismology-feed.ipynb`](notebook/fdsn-seismology-feed.ipynb). The notebook runs the Kafka feeder in `--once` mode, looks up the Event Stream connection string at runtime via the Fabric API, and writes diagnostics to OneLake under `/lakehouse/default/Files/feeder-state/fdsn-seismology/`.
