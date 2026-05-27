[![Build Containers](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml)

# Real Time Sources for Apache Kafka, Azure Event Hubs, and Fabric Event Streams

> 🚀 **Explore the catalog interactively at [clemensv.github.io/real-time-sources](http://clemensv.github.io/real-time-sources)** — browse every source, read its docs, and one-click deploy to Azure or Fabric.

Learning how to build event streaming solutions with Microsoft Azure Event Hubs,
Microsoft Fabric Event Streams, and any Apache Kafka compatible server and
service is more interesting when you have real time data sources to work with.

This repo contains command line tools, written in Python, that can be used to
retrieve real-time streaming data and related reference data from various APIs,
and then route the data to Apache Kafka compatible endpoints.

For each tool, there is a corresponding, pre-built (Docker-) container image
that you can pull and use instantly from this repo's container registry. The
container images will work with any Apache Kafka compatible server or service
that supports TLS with `SASL/PLAIN` authentication, as long as you provide the
required connection information.

## Deployment models

> ⚡ **MQTT 5.0 / Unified-Namespace pilot.** Seventeen sources — including
> **[NWS Alerts](nws-alerts/CONTAINER.md)**,
> ⚡ **MQTT 5.0 / Unified-Namespace pilot.** Selected sources — including
> **[TfL Road Traffic](tfl-road-traffic/CONTAINER.md#mqtt-50--unified-namespace-feeder)**,
> **[Autobahn](autobahn/CONTAINER.md#mqtt-50--unified-namespace-feeder)**,
> **[Bluesky](bluesky/CONTAINER.md#mqtt-50--unified-namespace-feeder-pilot)**,
> **[AISStream](aisstream/CONTAINER.md#mqtt-50--unified-namespace-feeder-pilot)**,
> **[Kystverket AIS](kystverket-ais/CONTAINER.md#mqtt-50--unified-namespace-feeder)**,
> and **[Blitzortung](blitzortung/CONTAINER.md#mqtt-50--unified-namespace-feeder)** —
> now ship a second container image (`Dockerfile.mqtt`) that publishes into MQTT
> 5.0 brokers on UNS topic trees using the CloudEvents binary binding. The Kafka
> images and contracts are unchanged.
> ship a second container image (`Dockerfile.mqtt`) that publishes into MQTT
> 5.0 brokers on UNS topic trees using the CloudEvents binary binding. The
> Kafka images remain separate.

Every source can be deployed in three ways. The [interactive catalog](https://clemensv.github.io/real-time-sources)
exposes a one-click deploy button for each supported model:

1. **Azure Container Instance → Azure Event Hubs.** An [ARM template](https://learn.microsoft.com/azure/azure-resource-manager/templates/overview)
   provisions an [Azure Container Instance](https://learn.microsoft.com/azure/container-instances/)
   running the feeder, with the choice of either provisioning a fresh
   [Azure Event Hubs](https://learn.microsoft.com/azure/event-hubs/event-hubs-about)
   namespace alongside it (*Azure + Event Hub*) or feeding into an existing
   Event Hubs connection string you already have (*Azure BYO Event Hub*).

2. **Azure Container Instance → Microsoft Fabric Event Stream.** The same ACI
   feeder, deployed from the gh-pages portal, writes into a
   [Fabric Event Stream](https://learn.microsoft.com/fabric/real-time-intelligence/event-streams/overview)
   custom endpoint inside a [Fabric Eventhouse](https://learn.microsoft.com/fabric/real-time-intelligence/eventhouse).
   This is the right choice when you want the data in Fabric but prefer to host
   the feeder in Azure.

3. **Fabric-only via notebooks.** For supported sources, the feeder runs as a
   [Fabric notebook](https://learn.microsoft.com/fabric/data-engineering/how-to-use-notebook)
   on a [scheduled trigger](https://learn.microsoft.com/fabric/data-engineering/schedule-notebook-runs),
   with no Azure subscription required at all. The deploy script provisions an
   Eventhouse, Event Stream, [KQL database](https://learn.microsoft.com/fabric/real-time-intelligence/create-database),
   and update policies, then imports the notebook and schedules it. Everything
   — ingestion, storage, query — stays inside your Fabric workspace. Look for
   the **Fabric Notebook Feeder** button in the catalog below.

<!-- root-catalog:begin -->
_The catalog below is rendered from `catalog.json`. Click a category to expand. Inside each category, click a source to see deploy targets, contract key, and event types. The [interactive portal](https://clemensv.github.io/real-time-sources) has the same content with live filters._

<details open><summary><b>💧 Hydrology and Water Monitoring</b> &nbsp;<sub>22 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇨🇭 <b>BAFU Hydro</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~300 stations, FOEN</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇨🇭 Switzerland</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~300 stations, FOEN

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbafu-hydro%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#bafu-hydro/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#bafu-hydro/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bafu-hydro)

<sub>📘 [README](bafu-hydro/README.md) &nbsp;·&nbsp; 📑 [EVENTS](bafu-hydro/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](bafu-hydro/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.hydrodaten.admin.ch](https://www.hydrodaten.admin.ch/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇨🇦 <b>Canada ECCC Water Office</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~2,100 hydrometric stations, ECCC/WSC</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇨🇦 Canada</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>stations/{station_number}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~2,100 hydrometric stations, ECCC/WSC

<sub><b>📍 keyed by</b> <code>stations/{station_number}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Observation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-eccc-wateroffice%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#canada-eccc-wateroffice/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-canada-eccc-wateroffice)

<sub>📘 [README](canada-eccc-wateroffice/README.md) &nbsp;·&nbsp; 📑 [EVENTS](canada-eccc-wateroffice/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](canada-eccc-wateroffice/CONTAINER.md) &nbsp;·&nbsp; ↗ [wateroffice.ec.gc.ca](https://wateroffice.ec.gc.ca/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>CDEC Reservoirs</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~2,600 stations, DWR</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 California</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}/{sensor_num}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~2,600 stations, DWR

<sub><b>📍 keyed by</b> <code>{station_id}/{sensor_num}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>ReservoirReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#cdec-reservoirs/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#cdec-reservoirs/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-cdec-reservoirs)

<sub>📘 [README](cdec-reservoirs/README.md) &nbsp;·&nbsp; 📑 [EVENTS](cdec-reservoirs/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](cdec-reservoirs/CONTAINER.md) &nbsp;·&nbsp; ↗ [cdec.water.ca.gov](https://cdec.water.ca.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇨🇿 <b>CHMI Hydro</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>CHMU</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇨🇿 Czech Republic</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

CHMU

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fchmi-hydro%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#chmi-hydro/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#chmi-hydro/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-chmi-hydro)

<sub>📘 [README](chmi-hydro/README.md) &nbsp;·&nbsp; 📑 [EVENTS](chmi-hydro/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](chmi-hydro/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.chmi.cz](https://www.chmi.cz/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>German Waters</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>12 state portals, ~2,724 stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

12 state portals, ~2,724 stations

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgerman-waters%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#german-waters/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-german-waters)

<sub>📘 [README](german-waters/README.md) &nbsp;·&nbsp; 📑 [EVENTS](german-waters/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](german-waters/CONTAINER.md) &nbsp;·&nbsp; ↗ [hvz.lubw.baden-wuerttemberg.de](https://hvz.lubw.baden-wuerttemberg.de/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇫🇷 <b>Hub'Eau Hydrometrie</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~6,300 stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇫🇷 France</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{code_station}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~6,300 stations

<sub><b>📍 keyed by</b> <code>{code_station}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Observation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhubeau-hydrometrie%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhubeau-hydrometrie%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhubeau-hydrometrie%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhubeau-hydrometrie%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhubeau-hydrometrie%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhubeau-hydrometrie%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#hubeau-hydrometrie/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#hubeau-hydrometrie/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-hubeau-hydrometrie)

<sub>📘 [README](hubeau-hydrometrie/README.md) &nbsp;·&nbsp; 📑 [EVENTS](hubeau-hydrometrie/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](hubeau-hydrometrie/CONTAINER.md) &nbsp;·&nbsp; ↗ [hubeau.eaufrance.fr](https://hubeau.eaufrance.fr/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇵🇱 <b>IMGW Hydro</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>IMGW-PIB</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇵🇱 Poland</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

IMGW-PIB

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#imgw-hydro/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#imgw-hydro/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-imgw-hydro)

<sub>📘 [README](imgw-hydro/README.md) &nbsp;·&nbsp; 📑 [EVENTS](imgw-hydro/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](imgw-hydro/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.imgw.pl](https://www.imgw.pl/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇮🇪 <b>Ireland OPW Water Level</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~500 OPW hydrometric stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇮🇪 Ireland</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_ref}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~500 OPW hydrometric stations

<sub><b>📍 keyed by</b> <code>{station_ref}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fireland-opw-waterlevel%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fireland-opw-waterlevel%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fireland-opw-waterlevel%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fireland-opw-waterlevel%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fireland-opw-waterlevel%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fireland-opw-waterlevel%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ireland-opw-waterlevel/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ireland-opw-waterlevel/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ireland-opw-waterlevel)

<sub>📘 [README](ireland-opw-waterlevel/README.md) &nbsp;·&nbsp; 📑 [EVENTS](ireland-opw-waterlevel/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](ireland-opw-waterlevel/CONTAINER.md) &nbsp;·&nbsp; ↗ [waterlevel.ie](https://waterlevel.ie/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>King County Marine</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>buoy and mooring telemetry</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 Washington State / Puget Sound</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

buoy and mooring telemetry

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterQualityReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fking-county-marine%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#king-county-marine/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#king-county-marine/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-king-county-marine)

<sub>📘 [README](king-county-marine/README.md) &nbsp;·&nbsp; 📑 [EVENTS](king-county-marine/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](king-county-marine/CONTAINER.md) &nbsp;·&nbsp; ↗ [green2.kingcounty.gov](https://green2.kingcounty.gov/marine/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇳🇵 <b>Nepal BIPAD Hydrology</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>Himalayan river basins, BIPAD</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇵 Nepal</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

Himalayan river basins, BIPAD

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>RiverStation</code>, <code>WaterLevelReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nepal-bipad-hydrology/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nepal-bipad-hydrology/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nepal-bipad-hydrology)

<sub>📘 [README](nepal-bipad-hydrology/README.md) &nbsp;·&nbsp; 📑 [EVENTS](nepal-bipad-hydrology/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](nepal-bipad-hydrology/CONTAINER.md) &nbsp;·&nbsp; ↗ [bipadportal.gov.np](https://bipadportal.gov.np/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>NOAA NDBC</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>buoy observations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">9 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

buoy observations

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>BuoyObservation</code>, <code>BuoyStation</code>, <code>BuoySolarRadiationObservation</code>, <code>BuoyOceanographicObservation</code>, <code>BuoyDartMeasurement</code>, <code>BuoyContinuousWindObservation</code>, <code>BuoySupplementalMeasurement</code>, <code>BuoyDetailedWaveSummary</code>, <code>BuoyHourlyRainMeasurement</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-ndbc%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-ndbc/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-ndbc/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa-ndbc)

<sub>📘 [README](noaa-ndbc/README.md) &nbsp;·&nbsp; 📑 [EVENTS](noaa-ndbc/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](noaa-ndbc/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.ndbc.noaa.gov](https://www.ndbc.noaa.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>NOAA Tides & Currents</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~3,000 stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">13 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~3,000 stations

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>WaterLevel</code>, <code>Predictions</code>, <code>AirPressure</code>, <code>AirTemperature</code>, <code>WaterTemperature</code>, <code>Wind</code>, <code>Humidity</code>, <code>Conductivity</code>, <code>Salinity</code>, <code>Station</code>, <code>Visibility</code>, <code>Currents</code>, <code>CurrentPredictions</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa)

<sub>📘 [README](noaa/README.md) &nbsp;·&nbsp; 📑 [EVENTS](noaa/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](noaa/CONTAINER.md) &nbsp;·&nbsp; ↗ [tidesandcurrents.noaa.gov](https://tidesandcurrents.noaa.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇳🇴 <b>NVE Hydro</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>NVE (requires free API key)</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇴 Norway</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

NVE (requires free API key)

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnve-hydro%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nve-hydro/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nve-hydro/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nve-hydro)

<sub>📘 [README](nve-hydro/README.md) &nbsp;·&nbsp; 📑 [EVENTS](nve-hydro/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](nve-hydro/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.nve.no](https://www.nve.no/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>Pegelonline</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>federal waterways, ~3,000 stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

federal waterways, ~3,000 stations

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>CurrentMeasurement</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#pegelonline/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#pegelonline/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-pegelonline)

<sub>📘 [README](pegelonline/README.md) &nbsp;·&nbsp; 📑 [EVENTS](pegelonline/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](pegelonline/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.pegelonline.wsv.de](https://www.pegelonline.wsv.de/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇳🇱 <b>RWS Waterwebservices</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~785 stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇱 Netherlands</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~785 stations

<sub><b>📍 keyed by</b> <code>{station_code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frws-waterwebservices%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#rws-waterwebservices/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#rws-waterwebservices/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-rws-waterwebservices)

<sub>📘 [README](rws-waterwebservices/README.md) &nbsp;·&nbsp; 📑 [EVENTS](rws-waterwebservices/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](rws-waterwebservices/CONTAINER.md) &nbsp;·&nbsp; ↗ [waterinfo.rws.nl](https://waterinfo.rws.nl/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇸🇪 <b>SMHI Hydro</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>SMHI</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇸🇪 Sweden</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

SMHI

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>DischargeObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#smhi-hydro/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#smhi-hydro/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-smhi-hydro)

<sub>📘 [README](smhi-hydro/README.md) &nbsp;·&nbsp; 📑 [EVENTS](smhi-hydro/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](smhi-hydro/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.smhi.se](https://www.smhi.se/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>SNOTEL Snow</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~900 snowpack stations, NRCS</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 Western US & Alaska</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_triplet}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~900 snowpack stations, NRCS

<sub><b>📍 keyed by</b> <code>{station_triplet}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>SnowObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsnotel%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#snotel/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#snotel/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-snotel)

<sub>📘 [README](snotel/README.md) &nbsp;·&nbsp; 📑 [EVENTS](snotel/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](snotel/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.nrcs.usda.gov](https://www.nrcs.usda.gov/wps/portal/wcc/home/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇫🇮 <b>SYKE Hydro</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>SYKE</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇫🇮 Finland</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

SYKE

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsyke-hydro%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#syke-hydro/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#syke-hydro/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-syke-hydro)

<sub>📘 [README](syke-hydro/README.md) &nbsp;·&nbsp; 📑 [EVENTS](syke-hydro/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](syke-hydro/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.syke.fi](https://www.syke.fi/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇬🇧 <b>UK EA Flood Monitoring</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~4,000 stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇬🇧 England</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_reference}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~4,000 stations

<sub><b>📍 keyed by</b> <code>{station_reference}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Reading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#uk-ea-flood-monitoring/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#uk-ea-flood-monitoring/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-uk-ea-flood-monitoring)

<sub>📘 [README](uk-ea-flood-monitoring/README.md) &nbsp;·&nbsp; 📑 [EVENTS](uk-ea-flood-monitoring/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](uk-ea-flood-monitoring/CONTAINER.md) &nbsp;·&nbsp; ↗ [environment.data.gov.uk](https://environment.data.gov.uk/flood-monitoring/doc/reference)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>USGS Instantaneous Values</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~1.5M stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{agency_cd}/{site_no}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~1.5M stations

<sub><b>📍 keyed by</b> <code>{agency_cd}/{site_no}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Site</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-iv%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-iv/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-iv/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-iv)

<sub>📘 [README](usgs-iv/README.md) &nbsp;·&nbsp; 📑 [EVENTS](usgs-iv/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](usgs-iv/CONTAINER.md) &nbsp;·&nbsp; ↗ [waterdata.usgs.gov](https://waterdata.usgs.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>USGS NWIS Water Quality</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~3,000 continuous WQ sites</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{site_number}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~3,000 continuous WQ sites

<sub><b>📍 keyed by</b> <code>{site_number}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>MonitoringSite</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-nwis-wq%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-nwis-wq/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-nwis-wq/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-nwis-wq)

<sub>📘 [README](usgs-nwis-wq/README.md) &nbsp;·&nbsp; 📑 [EVENTS](usgs-nwis-wq/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](usgs-nwis-wq/CONTAINER.md) &nbsp;·&nbsp; ↗ [waterdata.usgs.gov](https://waterdata.usgs.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇧🇪 <b>Waterinfo VMM</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~1,785 stations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇧🇪 Belgium / Flanders</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_no}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~1,785 stations

<sub><b>📍 keyed by</b> <code>{station_no}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WaterLevelReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwaterinfo-vmm%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwaterinfo-vmm%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwaterinfo-vmm%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwaterinfo-vmm%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwaterinfo-vmm%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwaterinfo-vmm%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#waterinfo-vmm/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#waterinfo-vmm/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-waterinfo-vmm)

<sub>📘 [README](waterinfo-vmm/README.md) &nbsp;·&nbsp; 📑 [EVENTS](waterinfo-vmm/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](waterinfo-vmm/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.waterinfo.be](https://www.waterinfo.be/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>⛅ Weather and Meteorology</b> &nbsp;<sub>21 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🌐 <b>AviationWeather.gov</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>METAR, SIGMET advisories</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{icao_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

METAR, SIGMET advisories

<sub><b>📍 keyed by</b> <code>{icao_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Metar</code>, <code>Sigmet</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#aviationweather/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#aviationweather/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-aviationweather)

<sub>📘 [README](aviationweather/README.md) &nbsp;·&nbsp; 📑 [EVENTS](aviationweather/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](aviationweather/CONTAINER.md) &nbsp;·&nbsp; ↗ [aviationweather.gov](https://aviationweather.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>Blitzortung</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>community lightning strokes, seconds latency</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{source_id}/{stroke_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

community lightning strokes, seconds latency

<sub><b>📍 keyed by</b> <code>{source_id}/{stroke_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>LightningStroke</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#blitzortung/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-blitzortung)

<sub>📘 [README](blitzortung/README.md) &nbsp;·&nbsp; 📑 [EVENTS](blitzortung/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](blitzortung/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.blitzortung.org](https://www.blitzortung.org/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇦🇺 <b>BOM Australia</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~8 capital city airports, half-hourly obs</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇦🇺 Australia</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_wmo}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~8 capital city airports, half-hourly obs

<sub><b>📍 keyed by</b> <code>{station_wmo}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WeatherObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#bom-australia/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#bom-australia/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bom-australia)

<sub>📘 [README](bom-australia/README.md) &nbsp;·&nbsp; 📑 [EVENTS](bom-australia/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](bom-australia/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.bom.gov.au](https://www.bom.gov.au/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇰 <b>DMI</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-_-eaeef2?style=flat-square"> &nbsp;<sub>DMI observation triad (metObs + oceanObs + lightning)</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-4-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-2-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇰 Denmark</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><i>n/a</i></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

DMI observation triad (metObs + oceanObs + lightning)

<sub><b>📍 keyed by</b> <i>n/a</i> &nbsp; · &nbsp; <b>📦 events</b> <code>MetObsStation</code>, <code>MetObsObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#dmi/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#dmi/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-dmi)

<sub>📘 [README](dmi/README.md) &nbsp;·&nbsp; 📑 [EVENTS](dmi/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](dmi/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.dmi.dk](https://www.dmi.dk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇰 <b>DMI</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-_-eaeef2?style=flat-square"> &nbsp;<sub>meteorological observations, sea level, lightning strikes</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-4-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-2-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇰 Denmark</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><i>n/a</i></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

meteorological observations, sea level, lightning strikes

<sub><b>📍 keyed by</b> <i>n/a</i> &nbsp; · &nbsp; <b>📦 events</b> <code>MetObsStation</code>, <code>MetObsObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#dmi/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#dmi/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-dmi)

<sub>📘 [README](dmi/README.md) &nbsp;·&nbsp; 📑 [EVENTS](dmi/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](dmi/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.dmi.dk](https://www.dmi.dk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>DWD</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~1,450 stations, observations and CAP alerts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">8 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~1,450 stations, observations and CAP alerts

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>StationMetadata</code>, <code>AirTemperature10Min</code>, <code>Precipitation10Min</code>, <code>Wind10Min</code>, <code>Solar10Min</code>, <code>HourlyObservation</code>, <code>ExtremeWind10Min</code>, <code>ExtremeTemperature10Min</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#dwd/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-dwd)

<sub>📘 [README](dwd/README.md) &nbsp;·&nbsp; 📑 [EVENTS](dwd/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](dwd/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.dwd.de](https://www.dwd.de/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>DWD Pollenflug</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>daily pollen forecasts, 27 regions</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{region_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

daily pollen forecasts, 27 regions

<sub><b>📍 keyed by</b> <code>{region_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Region</code>, <code>PollenForecast</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#dwd-pollenflug/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#dwd-pollenflug/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-dwd-pollenflug)

<sub>📘 [README](dwd-pollenflug/README.md) &nbsp;·&nbsp; 📑 [EVENTS](dwd-pollenflug/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](dwd-pollenflug/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.dwd.de](https://www.dwd.de/EN/specialusers/medical/pollenflug/pollenflug_node.html)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇨🇦 <b>Environment Canada</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~963 SWOB stations, hourly obs</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇨🇦 Canada</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{msc_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~963 SWOB stations, hourly obs

<sub><b>📍 keyed by</b> <code>{msc_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WeatherObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenvironment-canada%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenvironment-canada%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenvironment-canada%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenvironment-canada%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenvironment-canada%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenvironment-canada%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#environment-canada/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#environment-canada/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-environment-canada)

<sub>📘 [README](environment-canada/README.md) &nbsp;·&nbsp; 📑 [EVENTS](environment-canada/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](environment-canada/CONTAINER.md) &nbsp;·&nbsp; ↗ [weather.gc.ca](https://weather.gc.ca/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇦🇹 <b>GeoSphere Austria</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~280 TAWES stations, 10-min obs</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇦🇹 Austria</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~280 TAWES stations, 10-min obs

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>WeatherStation</code>, <code>WeatherObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#geosphere-austria/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#geosphere-austria/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-geosphere-austria)

<sub>📘 [README](geosphere-austria/README.md) &nbsp;·&nbsp; 📑 [EVENTS](geosphere-austria/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](geosphere-austria/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.geosphere.at](https://www.geosphere.at/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇭🇰 <b>HKO Hong Kong</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>27 temp stations, 18 rainfall districts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇭🇰 Hong Kong</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{place_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

27 temp stations, 18 rainfall districts

<sub><b>📍 keyed by</b> <code>{place_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WeatherObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#hko-hong-kong/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#hko-hong-kong/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-hko-hong-kong)

<sub>📘 [README](hko-hong-kong/README.md) &nbsp;·&nbsp; 📑 [EVENTS](hko-hong-kong/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](hko-hong-kong/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.hko.gov.hk](https://www.hko.gov.hk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇯🇵 <b>JMA Bosai AMeDAS</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~1,300 AMeDAS stations, 10-min observations via Bosai JSON API</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇯🇵 Japan</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>jp.jma.amedas/{station_code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~1,300 AMeDAS stations, 10-min observations via Bosai JSON API

<sub><b>📍 keyed by</b> <code>jp.jma.amedas/{station_code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Observation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-amedas%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-amedas%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-amedas%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-amedas%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-amedas%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-amedas%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-amedas/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-amedas/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-jma-bosai-amedas)

<sub>📘 [README](jma-bosai-amedas/README.md) &nbsp;·&nbsp; 📑 [EVENTS](jma-bosai-amedas/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](jma-bosai-amedas/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.jma.go.jp](https://www.jma.go.jp/bosai/amedas/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇯🇵 <b>JMA Japan</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>weather bulletins, warnings, forecasts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇯🇵 Japan</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{bulletin_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

weather bulletins, warnings, forecasts

<sub><b>📍 keyed by</b> <code>{bulletin_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>WeatherBulletin</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-japan/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-japan/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-jma-japan)

<sub>📘 [README](jma-japan/README.md) &nbsp;·&nbsp; 📑 [EVENTS](jma-japan/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](jma-japan/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.jma.go.jp](https://www.jma.go.jp/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇧🇪 <b>KMI Belgium</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~14 AWS stations, 10-min observations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇧🇪 Belgium</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~14 AWS stations, 10-min observations

<sub><b>📍 keyed by</b> <code>{station_code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WeatherObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkmi-belgium%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkmi-belgium%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkmi-belgium%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkmi-belgium%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkmi-belgium%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkmi-belgium%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#kmi-belgium/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#kmi-belgium/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-kmi-belgium)

<sub>📘 [README](kmi-belgium/README.md) &nbsp;·&nbsp; 📑 [EVENTS](kmi-belgium/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](kmi-belgium/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.meteo.be](https://www.meteo.be/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇪🇺 <b>Meteoalarm</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>37 countries, severe weather warnings</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇺 Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{identifier}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

37 countries, severe weather warnings

<sub><b>📍 keyed by</b> <code>{identifier}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>WeatherWarning</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#meteoalarm/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-meteoalarm)

<sub>📘 [README](meteoalarm/README.md) &nbsp;·&nbsp; 📑 [EVENTS](meteoalarm/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](meteoalarm/CONTAINER.md) &nbsp;·&nbsp; ↗ [meteoalarm.org](https://meteoalarm.org/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>NOAA GOES / SWPC</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>space weather, solar wind, K-index</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{product_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

space weather, solar wind, K-index

<sub><b>📍 keyed by</b> <code>{product_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>SpaceWeatherAlert</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-goes/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-goes/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa-goes)

<sub>📘 [README](noaa-goes/README.md) &nbsp;·&nbsp; 📑 [EVENTS](noaa-goes/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](noaa-goes/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.swpc.noaa.gov](https://www.swpc.noaa.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>NOAA NWS</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>weather alerts, CAP</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{alert_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

weather alerts, CAP

<sub><b>📍 keyed by</b> <code>{alert_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>WeatherAlert</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-nws/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-nws/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa-nws)

<sub>📘 [README](noaa-nws/README.md) &nbsp;·&nbsp; 📑 [EVENTS](noaa-nws/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](noaa-nws/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.weather.gov](https://www.weather.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>NOAA SWPC L1</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{spacecraft}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time

<sub><b>📍 keyed by</b> <code>{spacecraft}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>PropagatedSolarWind</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-swpc-l1/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#noaa-swpc-l1/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa-swpc-l1)

<sub>📘 [README](noaa-swpc-l1/README.md) &nbsp;·&nbsp; 📑 [EVENTS](noaa-swpc-l1/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](noaa-swpc-l1/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.swpc.noaa.gov](https://www.swpc.noaa.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>NWS CAP Alerts</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>active alerts via api.weather.gov</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{alert_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

active alerts via api.weather.gov

<sub><b>📍 keyed by</b> <code>{alert_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>WeatherAlert</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nws-alerts/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nws-alerts)

<sub>📘 [README](nws-alerts/README.md) &nbsp;·&nbsp; 📑 [EVENTS](nws-alerts/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](nws-alerts/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.weather.gov](https://www.weather.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>NWS Forecast Zones</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>configurable land and marine forecast zones</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{zone_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

configurable land and marine forecast zones

<sub><b>📍 keyed by</b> <code>{zone_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>ForecastZone</code>, <code>LandZoneForecast</code>, <code>MarineZoneForecast</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-forecasts%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-forecasts%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-forecasts%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-forecasts%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-forecasts%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-forecasts%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nws-forecasts/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nws-forecasts/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nws-forecasts)

<sub>📘 [README](nws-forecasts/README.md) &nbsp;·&nbsp; 📑 [EVENTS](nws-forecasts/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](nws-forecasts/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.weather.gov](https://www.weather.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇸🇬 <b>Singapore NEA</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>62 weather stations + 5 air-quality regions</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇸🇬 Singapore</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

62 weather stations + 5 air-quality regions

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WeatherObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsingapore-nea%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsingapore-nea%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsingapore-nea%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsingapore-nea%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsingapore-nea%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsingapore-nea%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#singapore-nea/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#singapore-nea/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-singapore-nea)

<sub>📘 [README](singapore-nea/README.md) &nbsp;·&nbsp; 📑 [EVENTS](singapore-nea/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](singapore-nea/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.nea.gov.sg](https://www.nea.gov.sg/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇸🇪 <b>SMHI Weather</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~232 stations, hourly obs</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇸🇪 Sweden</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~232 stations, hourly obs

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>WeatherObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#smhi-weather/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#smhi-weather/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-smhi-weather)

<sub>📘 [README](smhi-weather/README.md) &nbsp;·&nbsp; 📑 [EVENTS](smhi-weather/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](smhi-weather/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.smhi.se](https://www.smhi.se/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>🌫️ Air Quality and Environmental Health</b> &nbsp;<sub>12 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇨🇦 <b>Canada AQHI</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>community AQHI observations and forecasts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇨🇦 Canada</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{province}/{community_name}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

community AQHI observations and forecasts

<sub><b>📍 keyed by</b> <code>{province}/{community_name}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Community</code>, <code>Observation</code>, <code>Forecast</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcanada-aqhi%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#canada-aqhi/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#canada-aqhi/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-canada-aqhi)

<sub>📘 [README](canada-aqhi/README.md) &nbsp;·&nbsp; 📑 [EVENTS](canada-aqhi/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](canada-aqhi/CONTAINER.md) &nbsp;·&nbsp; ↗ [weather.gc.ca](https://weather.gc.ca/airquality/pages/index_e.html)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇬🇧 <b>Defra AURN</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>300+ monitoring locations, hourly pollutants</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇬🇧 United Kingdom</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

300+ monitoring locations, hourly pollutants

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdefra-aurn%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#defra-aurn/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#defra-aurn/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-defra-aurn)

<sub>📘 [README](defra-aurn/README.md) &nbsp;·&nbsp; 📑 [EVENTS](defra-aurn/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](defra-aurn/CONTAINER.md) &nbsp;·&nbsp; ↗ [uk-air.defra.gov.uk](https://uk-air.defra.gov.uk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>EPA UV Index</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>city-scoped hourly and daily UV forecasts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{location_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

city-scoped hourly and daily UV forecasts

<sub><b>📍 keyed by</b> <code>{location_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>HourlyForecast</code>, <code>DailyForecast</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fepa-uv%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#epa-uv/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#epa-uv/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-epa-uv)

<sub>📘 [README](epa-uv/README.md) &nbsp;·&nbsp; 📑 [EVENTS](epa-uv/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](epa-uv/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.epa.gov](https://www.epa.gov/sunsafety/uv-index-1)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇫🇮 <b>FMI Finland</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>hourly air quality observations via FMI WFS</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇫🇮 Finland</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{fmisid}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

hourly air quality observations via FMI WFS

<sub><b>📍 keyed by</b> <code>{fmisid}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Observation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffmi-finland%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#fmi-finland/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#fmi-finland/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-fmi-finland)

<sub>📘 [README](fmi-finland/README.md) &nbsp;·&nbsp; 📑 [EVENTS](fmi-finland/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](fmi-finland/CONTAINER.md) &nbsp;·&nbsp; ↗ [en.ilmatieteenlaitos.fi](https://en.ilmatieteenlaitos.fi/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇵🇱 <b>GIOŚ Poland</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~250 stations, hourly pollutants + AQI</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇵🇱 Poland</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">4 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~250 stations, hourly pollutants + AQI

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Sensor</code>, <code>Measurement</code>, <code>AirQualityIndex</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgios-poland%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgios-poland%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgios-poland%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgios-poland%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgios-poland%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgios-poland%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#gios-poland/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#gios-poland/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gios-poland)

<sub>📘 [README](gios-poland/README.md) &nbsp;·&nbsp; 📑 [EVENTS](gios-poland/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](gios-poland/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.gios.gov.pl](https://www.gios.gov.pl/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇭🇰 <b>Hong Kong EPD AQHI</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>18 AQHI stations, hourly health index</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇭🇰 Hong Kong</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

18 AQHI stations, hourly health index

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>AQHIReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhongkong-epd%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#hongkong-epd/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#hongkong-epd/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-hongkong-epd)

<sub>📘 [README](hongkong-epd/README.md) &nbsp;·&nbsp; 📑 [EVENTS](hongkong-epd/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](hongkong-epd/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.aqhi.gov.hk](https://www.aqhi.gov.hk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇧🇪 <b>IRCELINE Belgium</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>station, timeseries, and hourly observations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇧🇪 Belgium</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

station, timeseries, and hourly observations

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firceline-belgium%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#irceline-belgium/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#irceline-belgium/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-irceline-belgium)

<sub>📘 [README](irceline-belgium/README.md) &nbsp;·&nbsp; 📑 [EVENTS](irceline-belgium/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](irceline-belgium/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.irceline.be](https://www.irceline.be/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇬🇧 <b>LAQN London</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>site metadata, species, hourly measurements</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇬🇧 London</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{site_code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

site metadata, species, hourly measurements

<sub><b>📍 keyed by</b> <code>{site_code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Site</code>, <code>Measurement</code>, <code>DailyIndex</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#laqn-london/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#laqn-london/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-laqn-london)

<sub>📘 [README](laqn-london/README.md) &nbsp;·&nbsp; 📑 [EVENTS](laqn-london/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](laqn-london/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.londonair.org.uk](https://www.londonair.org.uk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇳🇱 <b>Luchtmeetnet Netherlands</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>station measurements, components, LKI index</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇱 Netherlands</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_number}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

station measurements, components, LKI index

<sub><b>📍 keyed by</b> <code>{station_number}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Measurement</code>, <code>LKI</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fluchtmeetnet-nl%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#luchtmeetnet-nl/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#luchtmeetnet-nl/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-luchtmeetnet-nl)

<sub>📘 [README](luchtmeetnet-nl/README.md) &nbsp;·&nbsp; 📑 [EVENTS](luchtmeetnet-nl/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](luchtmeetnet-nl/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.luchtmeetnet.nl](https://www.luchtmeetnet.nl/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>Sensor.Community</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>citizen air sensors, PM and climate readings</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{sensor_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

citizen air sensors, PM and climate readings

<sub><b>📍 keyed by</b> <code>{sensor_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>SensorInfo</code>, <code>SensorReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#sensor-community/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#sensor-community/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-sensor-community)

<sub>📘 [README](sensor-community/README.md) &nbsp;·&nbsp; 📑 [EVENTS](sensor-community/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](sensor-community/CONTAINER.md) &nbsp;·&nbsp; ↗ [sensor.community](https://sensor.community/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>UBA AirData</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>stations, pollutant components, hourly measures</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

stations, pollutant components, hourly measures

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>Measure</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#uba-airdata/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#uba-airdata/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-uba-airdata)

<sub>📘 [README](uba-airdata/README.md) &nbsp;·&nbsp; 📑 [EVENTS](uba-airdata/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](uba-airdata/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.umweltbundesamt.de](https://www.umweltbundesamt.de/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇧🇪 <b>Wallonia ISSeP</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>low-cost air quality sensors</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇧🇪 Belgium / Wallonia</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{configuration_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

low-cost air quality sensors

<sub><b>📍 keyed by</b> <code>{configuration_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>SensorConfiguration</code>, <code>Observation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#wallonia-issep/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wallonia-issep)

<sub>📘 [README](wallonia-issep/README.md) &nbsp;·&nbsp; 📑 [EVENTS](wallonia-issep/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](wallonia-issep/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.issep.be](https://www.issep.be/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>🚨 Disaster Alerts and Civil Protection</b> &nbsp;<sub>12 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇦🇺 <b>Australian Wildfires</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>NSW, QLD, VIC bushfire incidents</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇦🇺 Australia</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{state}/{incident_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

NSW, QLD, VIC bushfire incidents

<sub><b>📍 keyed by</b> <code>{state}/{incident_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>FireIncident</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#australia-wildfires/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#australia-wildfires/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-australia-wildfires)

<sub>📘 [README](australia-wildfires/README.md) &nbsp;·&nbsp; 📑 [EVENTS](australia-wildfires/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](australia-wildfires/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.rfs.nsw.gov.au](https://www.rfs.nsw.gov.au/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇦🇹 <b>EAWS ALBINA Avalanche</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>daily avalanche bulletins, CAAMLv6</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇦🇹 European Alps</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{region_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

daily avalanche bulletins, CAAMLv6

<sub><b>📍 keyed by</b> <code>{region_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>AvalancheRegion</code>, <code>AvalancheBulletin</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#eaws-albina/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#eaws-albina/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-eaws-albina)

<sub>📘 [README](eaws-albina/README.md) &nbsp;·&nbsp; 📑 [EVENTS](eaws-albina/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](eaws-albina/CONTAINER.md) &nbsp;·&nbsp; ↗ [avalanche.report](https://avalanche.report/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>GDACS</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>earthquakes, floods, cyclones, volcanoes, droughts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_type}/{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

earthquakes, floods, cyclones, volcanoes, droughts

<sub><b>📍 keyed by</b> <code>{event_type}/{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>DisasterAlert</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#gdacs/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gdacs)

<sub>📘 [README](gdacs/README.md) &nbsp;·&nbsp; 📑 [EVENTS](gdacs/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](gdacs/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.gdacs.org](https://www.gdacs.org/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇧🇷 <b>INPE DETER Brazil</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>Amazon & Cerrado deforestation alerts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇧🇷 Brazil</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{biome}/{alert_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

Amazon & Cerrado deforestation alerts

<sub><b>📍 keyed by</b> <code>{biome}/{alert_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>DeforestationAlert</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#inpe-deter-brazil/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-inpe-deter-brazil)

<sub>📘 [README](inpe-deter-brazil/README.md) &nbsp;·&nbsp; 📑 [EVENTS](inpe-deter-brazil/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](inpe-deter-brazil/CONTAINER.md) &nbsp;·&nbsp; ↗ [terrabrasilis.dpi.inpe.br](http://terrabrasilis.dpi.inpe.br/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇯🇵 <b>JMA Bosai Quake</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>JMA earthquake bulletins (hypocenter, magnitude, JMA intensity)</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇯🇵 Japan</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>jp.jma.quake/{event_id}/{serial}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

JMA earthquake bulletins (hypocenter, magnitude, JMA intensity)

<sub><b>📍 keyed by</b> <code>jp.jma.quake/{event_id}/{serial}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>EarthquakeReport</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-quake%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-quake%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-quake%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-quake%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-quake%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-quake%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-quake/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-quake/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-jma-bosai-quake)

<sub>📘 [README](jma-bosai-quake/README.md) &nbsp;·&nbsp; 📑 [EVENTS](jma-bosai-quake/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](jma-bosai-quake/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.jma.go.jp](https://www.jma.go.jp/bosai/map.html?contents=earthquake_map)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇯🇵 <b>JMA Bosai Volcano</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>111 volcanoes, alert levels, eruption observations</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇯🇵 Japan</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>jp.jma.volcano/{volcano_code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

111 volcanoes, alert levels, eruption observations

<sub><b>📍 keyed by</b> <code>jp.jma.volcano/{volcano_code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Volcano</code>, <code>VolcanicWarning</code>, <code>VolcanicEruption</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-volcano%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-volcano%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-volcano%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-volcano%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-volcano%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-volcano%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-volcano/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-volcano/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-jma-bosai-volcano)

<sub>📘 [README](jma-bosai-volcano/README.md) &nbsp;·&nbsp; 📑 [EVENTS](jma-bosai-volcano/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](jma-bosai-volcano/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.jma.go.jp](https://www.jma.go.jp/bosai/map.html?contents=volcano)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇯🇵 <b>JMA Bosai Warning & Tsunami</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>per-prefecture weather warnings + tsunami alerts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇯🇵 Japan</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>jp.jma.warning/{office_code}/{area_code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

per-prefecture weather warnings + tsunami alerts

<sub><b>📍 keyed by</b> <code>jp.jma.warning/{office_code}/{area_code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Office</code>, <code>WeatherWarning</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-warning%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-warning%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-warning%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-warning%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-warning%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-warning%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-warning/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#jma-bosai-warning/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-jma-bosai-warning)

<sub>📘 [README](jma-bosai-warning/README.md) &nbsp;·&nbsp; 📑 [EVENTS](jma-bosai-warning/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](jma-bosai-warning/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.jma.go.jp](https://www.jma.go.jp/bosai/map.html?contents=warning)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>NIFC USA Wildfires</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>active wildfire incidents, NIFC</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{irwin_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

active wildfire incidents, NIFC

<sub><b>📍 keyed by</b> <code>{irwin_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>WildfireIncident</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnifc-usa-wildfires%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nifc-usa-wildfires/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nifc-usa-wildfires)

<sub>📘 [README](nifc-usa-wildfires/README.md) &nbsp;·&nbsp; 📑 [EVENTS](nifc-usa-wildfires/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](nifc-usa-wildfires/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.nifc.gov](https://www.nifc.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>NINA/BBK</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>MOWAS, KATWARN, BIWAPP, DWD, LHP, Police</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{warning_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

MOWAS, KATWARN, BIWAPP, DWD, LHP, Police

<sub><b>📍 keyed by</b> <code>{warning_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>CivilWarning</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnina-bbk%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nina-bbk/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nina-bbk)

<sub>📘 [README](nina-bbk/README.md) &nbsp;·&nbsp; 📑 [EVENTS](nina-bbk/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](nina-bbk/CONTAINER.md) &nbsp;·&nbsp; ↗ [warnung.bund.de](https://warnung.bund.de/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>PTWC Tsunami</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>NOAA tsunami bulletins</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Pacific and Atlantic</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{bulletin_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

NOAA tsunami bulletins

<sub><b>📍 keyed by</b> <code>{bulletin_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>TsunamiBulletin</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ptwc-tsunami/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ptwc-tsunami)

<sub>📘 [README](ptwc-tsunami/README.md) &nbsp;·&nbsp; 📑 [EVENTS](ptwc-tsunami/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](ptwc-tsunami/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.tsunami.gov](https://www.tsunami.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>Seattle Fire 911</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>real-time fire dispatch incidents</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 Seattle</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{incident_number}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

real-time fire dispatch incidents

<sub><b>📍 keyed by</b> <code>{incident_number}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Incident</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#seattle-911/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#seattle-911/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-seattle-911)

<sub>📘 [README](seattle-911/README.md) &nbsp;·&nbsp; 📑 [EVENTS](seattle-911/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](seattle-911/CONTAINER.md) &nbsp;·&nbsp; ↗ [data.seattle.gov](https://data.seattle.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>USGS Earthquakes</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>seismic events</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{net}/{code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

seismic events

<sub><b>📍 keyed by</b> <code>{net}/{code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Event</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-earthquakes%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-earthquakes/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-earthquakes/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-earthquakes)

<sub>📘 [README](usgs-earthquakes/README.md) &nbsp;·&nbsp; 📑 [EVENTS](usgs-earthquakes/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](usgs-earthquakes/CONTAINER.md) &nbsp;·&nbsp; ↗ [earthquake.usgs.gov](https://earthquake.usgs.gov/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>☢️ Radiation Monitoring</b> &nbsp;<sub>3 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>BfS ODL</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~1,700 stations, hourly gamma dose rate</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~1,700 stations, hourly gamma dose rate

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>DoseRateMeasurement</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#bfs-odl/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#bfs-odl/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bfs-odl)

<sub>📘 [README](bfs-odl/README.md) &nbsp;·&nbsp; 📑 [EVENTS](bfs-odl/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](bfs-odl/CONTAINER.md) &nbsp;·&nbsp; ↗ [odlinfo.bfs.de](https://odlinfo.bfs.de/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇪🇺 <b>EURDEP Radiation</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~5,500 stations, 39 countries, gamma dose</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇺 Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~5,500 stations, 39 countries, gamma dose

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>DoseRateReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#eurdep-radiation/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#eurdep-radiation/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-eurdep-radiation)

<sub>📘 [README](eurdep-radiation/README.md) &nbsp;·&nbsp; 📑 [EVENTS](eurdep-radiation/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](eurdep-radiation/CONTAINER.md) &nbsp;·&nbsp; ↗ [remon.jrc.ec.europa.eu](https://remon.jrc.ec.europa.eu/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>USGS Geomagnetism</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>14 observatories, 1-min geomagnetic field</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 United States</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{iaga_code}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

14 observatories, 1-min geomagnetic field

<sub><b>📍 keyed by</b> <code>{iaga_code}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Observatory</code>, <code>MagneticFieldReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-geomag/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#usgs-geomag/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-geomag)

<sub>📘 [README](usgs-geomag/README.md) &nbsp;·&nbsp; 📑 [EVENTS](usgs-geomag/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](usgs-geomag/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.usgs.gov](https://www.usgs.gov/programs/geomagnetism)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>⚓ Maritime and Vessel Tracking</b> &nbsp;<sub>3 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🌐 <b>AISStream</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>Global â€” AIS via WebSocket, ~200 km from shore</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global â€” AIS via WebSocket</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{mmsi}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">23 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

Global â€” AIS via WebSocket, ~200 km from shore

<sub><b>📍 keyed by</b> <code>{mmsi}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>PositionReport</code>, <code>ShipStaticData</code>, <code>StandardClassBPositionReport</code>, <code>ExtendedClassBPositionReport</code>, <code>AidsToNavigationReport</code>, <code>StaticDataReport</code>, <code>BaseStationReport</code>, <code>SafetyBroadcastMessage</code>, <code>StandardSearchAndRescueAircraftReport</code>, <code>LongRangeAisBroadcastMessage</code>, <code>AddressedSafetyMessage</code>, <code>AddressedBinaryMessage</code>, <code>AssignedModeCommand</code>, <code>BinaryAcknowledge</code>, <code>BinaryBroadcastMessage</code>, <code>ChannelManagement</code>, <code>CoordinatedUTCInquiry</code>, <code>DataLinkManagementMessage</code>, <code>GnssBroadcastBinaryMessage</code>, <code>GroupAssignmentCommand</code>, <code>Interrogation</code>, <code>MultiSlotBinaryMessage</code>, <code>SingleSlotBinaryMessage</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#aisstream/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-aisstream)

<sub>📘 [README](aisstream/README.md) &nbsp;·&nbsp; 📑 [EVENTS](aisstream/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](aisstream/CONTAINER.md) &nbsp;·&nbsp; ↗ [aisstream.io](https://aisstream.io/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇫🇮 <b>Digitraffic Maritime</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>AIS via MQTT</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇫🇮 Finland / Baltic Sea</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{mmsi}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

AIS via MQTT

<sub><b>📍 keyed by</b> <code>{mmsi}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>VesselLocation</code>, <code>VesselMetadata</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#digitraffic-maritime/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-digitraffic-maritime)

<sub>📘 [README](digitraffic-maritime/README.md) &nbsp;·&nbsp; 📑 [EVENTS](digitraffic-maritime/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](digitraffic-maritime/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.digitraffic.fi](https://www.digitraffic.fi/en/marine-traffic/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇳🇴 <b>Kystverket AIS</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>Norway / Svalbard â€” raw TCP AIS, ~34 msg/s</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇴 Norway / Svalbard â€” raw TCP AIS</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{mmsi}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">7 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

Norway / Svalbard â€” raw TCP AIS, ~34 msg/s

<sub><b>📍 keyed by</b> <code>{mmsi}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>PositionReportClassA</code>, <code>StaticVoyageData</code>, <code>PositionReportClassB</code>, <code>StaticDataClassB</code>, <code>AidToNavigation</code>, <code>PositionReport</code>, <code>ShipStatic</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#kystverket-ais/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-kystverket-ais)

<sub>📘 [README](kystverket-ais/README.md) &nbsp;·&nbsp; 📑 [EVENTS](kystverket-ais/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](kystverket-ais/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.kystverket.no](https://www.kystverket.no/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>✈️ Aviation</b> &nbsp;<sub>2 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🌐 <b>Mode-S</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>Local â€” ADS-B via dump1090 receivers</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Local â€” ADS-B via dump1090 receivers</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{stationid}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">6 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

Local â€” ADS-B via dump1090 receivers

<sub><b>📍 keyed by</b> <code>{stationid}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>ADSB</code>, <code>AltitudeReply</code>, <code>IdentityReply</code>, <code>AcquisitionReply</code>, <code>CommBAltitude</code>, <code>CommBIdentity</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#mode-s/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-mode-s)

<sub>📘 [README](mode-s/README.md) &nbsp;·&nbsp; 📑 [EVENTS](mode-s/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](mode-s/CONTAINER.md) &nbsp;·&nbsp; ↗ [opensky-network.org](https://opensky-network.org/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>VATSIM</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>virtual aviation network, pilots & controllers</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{callsign}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

virtual aviation network, pilots & controllers

<sub><b>📍 keyed by</b> <code>{callsign}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>PilotPosition</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#vatsim/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#vatsim/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-vatsim)

<sub>📘 [README](vatsim/README.md) &nbsp;·&nbsp; 📑 [EVENTS](vatsim/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](vatsim/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.vatsim.net](https://www.vatsim.net/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>🚦 Road and Public Transport</b> &nbsp;<sub>14 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇩🇪 <b>Autobahn</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>roadworks, warnings, closures, webcams</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇪 Germany</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{identifier}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">30 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

roadworks, warnings, closures, webcams

<sub><b>📍 keyed by</b> <code>{identifier}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>RoadworkAppeared</code>, <code>RoadworkUpdated</code>, <code>RoadworkResolved</code>, <code>ShortTermRoadworkAppeared</code>, <code>ShortTermRoadworkUpdated</code>, <code>ShortTermRoadworkResolved</code>, <code>WarningAppeared</code>, <code>WarningUpdated</code>, <code>WarningResolved</code>, <code>ClosureAppeared</code>, <code>ClosureUpdated</code>, <code>ClosureResolved</code>, <code>EntryExitClosureAppeared</code>, <code>EntryExitClosureUpdated</code>, <code>EntryExitClosureResolved</code>, <code>WeightLimit35RestrictionAppeared</code>, <code>WeightLimit35RestrictionUpdated</code>, <code>WeightLimit35RestrictionResolved</code>, <code>ParkingLorryAppeared</code>, <code>ParkingLorryUpdated</code>, <code>ParkingLorryResolved</code>, <code>ElectricChargingStationAppeared</code>, <code>ElectricChargingStationUpdated</code>, <code>ElectricChargingStationResolved</code>, <code>StrongElectricChargingStationAppeared</code>, <code>StrongElectricChargingStationUpdated</code>, <code>StrongElectricChargingStationResolved</code>, <code>WebcamAppeared</code>, <code>WebcamUpdated</code>, <code>WebcamResolved</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#autobahn/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#autobahn/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-autobahn)

<sub>📘 [README](autobahn/README.md) &nbsp;·&nbsp; 📑 [EVENTS](autobahn/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](autobahn/CONTAINER.md) &nbsp;·&nbsp; ↗ [autobahn.de](https://autobahn.de/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇫🇮 <b>Digitraffic Road</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>TMS sensors, road weather, traffic messages</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇫🇮 Finland</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}/{sensor_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

TMS sensors, road weather, traffic messages

<sub><b>📍 keyed by</b> <code>{station_id}/{sensor_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>TmsSensorData</code>, <code>WeatherSensorData</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#digitraffic-road/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-digitraffic-road)

<sub>📘 [README](digitraffic-road/README.md) &nbsp;·&nbsp; 📑 [EVENTS](digitraffic-road/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](digitraffic-road/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.digitraffic.fi](https://www.digitraffic.fi/en/road-traffic/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇫🇷 <b>French Road Traffic</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>national road network, DATEX II</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇫🇷 France</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{site_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

national road network, DATEX II

<sub><b>📍 keyed by</b> <code>{site_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>TrafficFlowMeasurement</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#french-road-traffic/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#french-road-traffic/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-french-road-traffic)

<sub>📘 [README](french-road-traffic/README.md) &nbsp;·&nbsp; 📑 [EVENTS](french-road-traffic/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](french-road-traffic/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.bison-fute.gouv.fr](https://www.bison-fute.gouv.fr/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>GTFS Realtime</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>1,000+ transit agencies, vehicles, trips, alerts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{agencyid}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

1,000+ transit agencies, vehicles, trips, alerts

<sub><b>📍 keyed by</b> <code>{agencyid}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>VehiclePosition</code>, <code>TripUpdate</code>, <code>Alert</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#gtfs/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gtfs)

<sub>📘 [README](gtfs/README.md) &nbsp;·&nbsp; 📑 [EVENTS](gtfs/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](gtfs/CONTAINER.md) &nbsp;·&nbsp; ↗ [gtfs.org](https://gtfs.org/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇪🇸 <b>Madrid Traffic</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~4,000 sensors, Informo</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇸 Madrid</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{sensor_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~4,000 sensors, Informo

<sub><b>📍 keyed by</b> <code>{sensor_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>MeasurementPoint</code>, <code>TrafficReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#madrid-traffic/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#madrid-traffic/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-madrid-traffic)

<sub>📘 [README](madrid-traffic/README.md) &nbsp;·&nbsp; 📑 [EVENTS](madrid-traffic/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](madrid-traffic/CONTAINER.md) &nbsp;·&nbsp; ↗ [datos.madrid.es](https://datos.madrid.es/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇳🇱 <b>NDW Netherlands Traffic</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>national road traffic, DATEX II</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇱 Netherlands</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{site_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

national road traffic, DATEX II

<sub><b>📍 keyed by</b> <code>{site_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>TrafficSpeed</code>, <code>TravelTime</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ndl-netherlands/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ndl-netherlands/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ndl-netherlands)

<sub>📘 [README](ndl-netherlands/README.md) &nbsp;·&nbsp; 📑 [EVENTS](ndl-netherlands/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](ndl-netherlands/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.ndw.nu](https://www.ndw.nu/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇳🇱 <b>NDW Road Traffic</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>national road traffic, DATEX II XML</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇱 Netherlands</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>measurement-sites/{measurement_site_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">4 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

national road traffic, DATEX II XML

<sub><b>📍 keyed by</b> <code>measurement-sites/{measurement_site_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>PointMeasurementSite</code>, <code>RouteMeasurementSite</code>, <code>TrafficObservation</code>, <code>TravelTimeObservation</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndw-road-traffic%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ndw-road-traffic/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ndw-road-traffic)

<sub>📘 [README](ndw-road-traffic/README.md) &nbsp;·&nbsp; 📑 [EVENTS](ndw-road-traffic/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](ndw-road-traffic/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.ndw.nu](https://www.ndw.nu/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>Nextbus</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>public transit arrivals</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 North America</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{agency_id}/{route_tag}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">4 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

public transit arrivals

<sub><b>📍 keyed by</b> <code>{agency_id}/{route_tag}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>VehiclePosition</code>, <code>RouteConfig</code>, <code>Schedule</code>, <code>Message</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nextbus/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nextbus)

<sub>📘 [README](nextbus/README.md) &nbsp;·&nbsp; 📑 [EVENTS](nextbus/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](nextbus/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.umoiq.com](https://www.umoiq.com/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇫🇷 <b>Paris Bicycle Counters</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~141 counting stations, hourly counts</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇫🇷 Paris</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{counter_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~141 counting stations, hourly counts

<sub><b>📍 keyed by</b> <code>{counter_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Counter</code>, <code>BicycleCount</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fparis-bicycle-counters%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#paris-bicycle-counters/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#paris-bicycle-counters/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-paris-bicycle-counters)

<sub>📘 [README](paris-bicycle-counters/README.md) &nbsp;·&nbsp; 📑 [EVENTS](paris-bicycle-counters/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](paris-bicycle-counters/CONTAINER.md) &nbsp;·&nbsp; ↗ [opendata.paris.fr](https://opendata.paris.fr/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>Seattle Street Closures</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>permit-driven street closure windows</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 Seattle</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{closure_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

permit-driven street closure windows

<sub><b>📍 keyed by</b> <code>{closure_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>StreetClosure</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-street-closures%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#seattle-street-closures/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#seattle-street-closures/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-seattle-street-closures)

<sub>📘 [README](seattle-street-closures/README.md) &nbsp;·&nbsp; 📑 [EVENTS](seattle-street-closures/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](seattle-street-closures/CONTAINER.md) &nbsp;·&nbsp; ↗ [data.seattle.gov](https://data.seattle.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇬🇧 <b>TfL Road Traffic</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>road corridor status and disruptions</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇬🇧 London</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>roads/{road_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

road corridor status and disruptions

<sub><b>📍 keyed by</b> <code>roads/{road_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>RoadCorridor</code>, <code>RoadStatus</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#tfl-road-traffic/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-tfl-road-traffic)

<sub>📘 [README](tfl-road-traffic/README.md) &nbsp;·&nbsp; 📑 [EVENTS](tfl-road-traffic/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](tfl-road-traffic/CONTAINER.md) &nbsp;·&nbsp; ↗ [tfl.gov.uk](https://tfl.gov.uk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇯🇵 <b>Tokyo Docomo Bikeshare</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>1,794 stations, GBFS 2.3 via ODPT</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇯🇵 Tokyo</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{system_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

1,794 stations, GBFS 2.3 via ODPT

<sub><b>📍 keyed by</b> <code>{system_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>BikeshareSystem</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#tokyo-docomo-bikeshare/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-tokyo-docomo-bikeshare)

<sub>📘 [README](tokyo-docomo-bikeshare/README.md) &nbsp;·&nbsp; 📑 [EVENTS](tokyo-docomo-bikeshare/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](tokyo-docomo-bikeshare/CONTAINER.md) &nbsp;·&nbsp; ↗ [docomo-cycle.jp](https://docomo-cycle.jp/tokyo/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>US CBP Border Wait</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~81 ports of entry</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 US borders</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{port_number}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~81 ports of entry

<sub><b>📍 keyed by</b> <code>{port_number}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Port</code>, <code>WaitTime</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcbp-border-wait%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#cbp-border-wait/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#cbp-border-wait/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-cbp-border-wait)

<sub>📘 [README](cbp-border-wait/README.md) &nbsp;·&nbsp; 📑 [EVENTS](cbp-border-wait/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](cbp-border-wait/CONTAINER.md) &nbsp;·&nbsp; ↗ [bwt.cbp.gov](https://bwt.cbp.gov/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇺🇸 <b>WSDOT</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~1,000 traffic flow sensors (requires free key)</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇺🇸 Washington State</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{flow_data_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~1,000 traffic flow sensors (requires free key)

<sub><b>📍 keyed by</b> <code>{flow_data_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>TrafficFlowStation</code>, <code>TrafficFlowReading</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwsdot%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#wsdot/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#wsdot/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wsdot)

<sub>📘 [README](wsdot/README.md) &nbsp;·&nbsp; 📑 [EVENTS](wsdot/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](wsdot/CONTAINER.md) &nbsp;·&nbsp; ↗ [wsdot.wa.gov](https://wsdot.wa.gov/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>🚆 Railway</b> &nbsp;<sub>2 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇳🇴 <b>Entur Norway</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>national real-time transit, SIRI ET/VM/SX</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇳🇴 Norway</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>journeys/{operating_day}/{service_journey_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

national real-time transit, SIRI ET/VM/SX

<sub><b>📍 keyed by</b> <code>journeys/{operating_day}/{service_journey_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>DatedServiceJourney</code>, <code>EstimatedVehicleJourney</code>, <code>MonitoredVehicleJourney</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#entur-norway/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-entur-norway)

<sub>📘 [README](entur-norway/README.md) &nbsp;·&nbsp; 📑 [EVENTS](entur-norway/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](entur-norway/CONTAINER.md) &nbsp;·&nbsp; ↗ [entur.no](https://entur.no/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇧🇪 <b>iRail</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>~600 NMBS/SNCB stations, departures, delays</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇧🇪 Belgium</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{station_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

~600 NMBS/SNCB stations, departures, delays

<sub><b>📍 keyed by</b> <code>{station_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Station</code>, <code>StationBoard</code>, <code>ArrivalBoard</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#irail/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#irail/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-irail)

<sub>📘 [README](irail/README.md) &nbsp;·&nbsp; 📑 [EVENTS](irail/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](irail/CONTAINER.md) &nbsp;·&nbsp; ↗ [irail.be](https://irail.be/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>🎵 Nightlife and Live Entertainment</b> &nbsp;<sub>1 source</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇪🇺 <b>Xceed</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>clubs, bars, parties, festivals — event schedules</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇺 Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

clubs, bars, parties, festivals — event schedules

<sub><b>📍 keyed by</b> <code>{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Event</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fxceed%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fxceed%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fxceed%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fxceed%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fxceed%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fxceed%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#xceed/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-xceed)

<sub>📘 [README](xceed/README.md) &nbsp;·&nbsp; 📑 [EVENTS](xceed/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](xceed/CONTAINER.md) &nbsp;·&nbsp; ↗ [xceed.me](https://xceed.me/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>⚡ Energy and Infrastructure</b> &nbsp;<sub>6 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇬🇧 <b>Carbon Intensity UK</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>national grid carbon intensity</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇬🇧 United Kingdom</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{period_from}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

national grid carbon intensity

<sub><b>📍 keyed by</b> <code>{period_from}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Intensity</code>, <code>GenerationMix</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#carbon-intensity/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#carbon-intensity/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-carbon-intensity)

<sub>📘 [README](carbon-intensity/README.md) &nbsp;·&nbsp; 📑 [EVENTS](carbon-intensity/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](carbon-intensity/CONTAINER.md) &nbsp;·&nbsp; ↗ [carbonintensity.org.uk](https://carbonintensity.org.uk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇬🇧 <b>Elexon BMRS</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>electricity market, generation, demand</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇬🇧 Great Britain</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{settlement_period}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

electricity market, generation, demand

<sub><b>📍 keyed by</b> <code>{settlement_period}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>GenerationMix</code>, <code>DemandOutturn</code>, <code>Info</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Felexon-bmrs%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Felexon-bmrs%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Felexon-bmrs%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Felexon-bmrs%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Felexon-bmrs%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Felexon-bmrs%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#elexon-bmrs/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#elexon-bmrs/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-elexon-bmrs)

<sub>📘 [README](elexon-bmrs/README.md) &nbsp;·&nbsp; 📑 [EVENTS](elexon-bmrs/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](elexon-bmrs/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.elexon.co.uk](https://www.elexon.co.uk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇩🇰 <b>Energi Data Service</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>power system, spot prices, CO₂</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇩🇰 Denmark</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{price_area}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">3 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

power system, spot prices, CO₂

<sub><b>📍 keyed by</b> <code>{price_area}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>PowerSystemSnapshot</code>, <code>SpotPrice</code>, <code>Info</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#energidataservice-dk/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#energidataservice-dk/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-energidataservice-dk)

<sub>📘 [README](energidataservice-dk/README.md) &nbsp;·&nbsp; 📑 [EVENTS](energidataservice-dk/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](energidataservice-dk/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.energidataservice.dk](https://www.energidataservice.dk/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇪🇺 <b>Energy-Charts</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>40+ countries, electricity generation & prices</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇺 Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{country}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">4 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

40+ countries, electricity generation & prices

<sub><b>📍 keyed by</b> <code>{country}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>PublicPower</code>, <code>SpotPrice</code>, <code>GridSignal</code>, <code>Info</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#energy-charts/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#energy-charts/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-energy-charts)

<sub>📘 [README](energy-charts/README.md) &nbsp;·&nbsp; 📑 [EVENTS](energy-charts/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](energy-charts/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.energy-charts.info](https://www.energy-charts.info/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇪🇺 <b>ENTSO-E</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>electricity generation, prices, load, flows (requires token)</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇺 Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{inDomain}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">6 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

electricity generation, prices, load, flows (requires token)

<sub><b>📍 keyed by</b> <code>{inDomain}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>DayAheadPrices</code>, <code>ActualTotalLoad</code>, <code>LoadForecastMargin</code>, <code>GenerationForecast</code>, <code>ReservoirFillingInformation</code>, <code>ActualGeneration</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#entsoe/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-entsoe)

<sub>📘 [README](entsoe/README.md) &nbsp;·&nbsp; 📑 [EVENTS](entsoe/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](entsoe/CONTAINER.md) &nbsp;·&nbsp; ↗ [transparency.entsoe.eu](https://transparency.entsoe.eu/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇯🇵 <b>TEPCO Denkiyoho</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>TEPCO electricity supply, hourly forecast, 5-min actuals + solar</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇯🇵 Japan / Kanto</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>jp.tepco.denkiyoho/{date}/{time}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">5 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

TEPCO electricity supply, hourly forecast, 5-min actuals + solar

<sub><b>📍 keyed by</b> <code>jp.tepco.denkiyoho/{date}/{time}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>SupplyCapacity</code>, <code>PeakDemandForecast</code>, <code>DemandActual</code>, <code>DemandForecast</code>, <code>Info</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftepco-denkiyoho%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftepco-denkiyoho%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftepco-denkiyoho%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftepco-denkiyoho%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftepco-denkiyoho%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftepco-denkiyoho%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#tepco-denkiyoho/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#tepco-denkiyoho/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-tepco-denkiyoho)

<sub>📘 [README](tepco-denkiyoho/README.md) &nbsp;·&nbsp; 📑 [EVENTS](tepco-denkiyoho/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](tepco-denkiyoho/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.tepco.co.jp](https://www.tepco.co.jp/forecast/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>💬 Social Media and News</b> &nbsp;<sub>4 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🌐 <b>Bluesky Firehose</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>posts, likes, reposts, follows</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{did}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">6 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

posts, likes, reposts, follows

<sub><b>📍 keyed by</b> <code>{did}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Post</code>, <code>Like</code>, <code>Repost</code>, <code>Follow</code>, <code>Block</code>, <code>Profile</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#bluesky/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bluesky)

<sub>📘 [README](bluesky/README.md) &nbsp;·&nbsp; 📑 [EVENTS](bluesky/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](bluesky/CONTAINER.md) &nbsp;·&nbsp; ↗ [bsky.app](https://bsky.app/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>OpenStreetMap Diffs</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>OSM minutely replication diffs</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{element_type}/{element_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

OSM minutely replication diffs

<sub><b>📍 keyed by</b> <code>{element_type}/{element_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>MapChange</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#wikimedia-osm-diffs/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#wikimedia-osm-diffs/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wikimedia-osm-diffs)

<sub>📘 [README](wikimedia-osm-diffs/README.md) &nbsp;·&nbsp; 📑 [EVENTS](wikimedia-osm-diffs/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](wikimedia-osm-diffs/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.openstreetmap.org](https://www.openstreetmap.org/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>RSS Feeds</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>configurable RSS/Atom feed URLs or OPML files</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Any</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{item_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

configurable RSS/Atom feed URLs or OPML files

<sub><b>📍 keyed by</b> <code>{item_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>FeedItem</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#rss/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-rss)

<sub>📘 [README](rss/README.md) &nbsp;·&nbsp; 📑 [EVENTS](rss/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](rss/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.rssboard.org](https://www.rssboard.org/rss-specification)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>Wikimedia EventStreams</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>Wikipedia, Wikidata, Commons recent changes</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

Wikipedia, Wikidata, Commons recent changes

<sub><b>📍 keyed by</b> <code>{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>RecentChange</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#wikimedia-eventstreams/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wikimedia-eventstreams)

<sub>📘 [README](wikimedia-eventstreams/README.md) &nbsp;·&nbsp; 📑 [EVENTS](wikimedia-eventstreams/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](wikimedia-eventstreams/CONTAINER.md) &nbsp;·&nbsp; ↗ [wikitech.wikimedia.org](https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>📅 Public Events</b> &nbsp;<sub>3 sources</sub></summary>

<table width="100%"><tr><td>

<details><summary>🇪🇺 <b>Billetto</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>pan-European ticketed public events</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇺 Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

pan-European ticketed public events

<sub><b>📍 keyed by</b> <code>{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Event</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#billetto/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-billetto)

<sub>📘 [README](billetto/README.md) &nbsp;·&nbsp; 📑 [EVENTS](billetto/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](billetto/CONTAINER.md) &nbsp;·&nbsp; ↗ [billetto.com](https://billetto.com/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🇪🇺 <b>Fienta</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>ticketed public events with sale-status signals</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🇪🇺 Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

ticketed public events with sale-status signals

<sub><b>📍 keyed by</b> <code>{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Event</code>, <code>EventSaleStatus</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#fienta/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-fienta)

<sub>📘 [README](fienta/README.md) &nbsp;·&nbsp; 📑 [EVENTS](fienta/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](fienta/CONTAINER.md) &nbsp;·&nbsp; ↗ [fienta.com](https://fienta.com/)</sub>

</details>

</td></tr></table>

<table width="100%"><tr><td>

<details><summary>🌐 <b>Ticketmaster</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>concerts, sports, theater, arts via Discovery API</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

concerts, sports, theater, arts via Discovery API

<sub><b>📍 keyed by</b> <code>{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Event</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ticketmaster/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ticketmaster)

<sub>📘 [README](ticketmaster/README.md) &nbsp;·&nbsp; 📑 [EVENTS](ticketmaster/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](ticketmaster/CONTAINER.md) &nbsp;·&nbsp; ↗ [www.ticketmaster.com](https://www.ticketmaster.com/)</sub>

</details>

</td></tr></table>

</details>

<details open><summary><b>🔬 Scientific Research</b> &nbsp;<sub>1 source</sub></summary>

<table width="100%"><tr><td>

<details><summary>🌐 <b>GraceDB</b> &nbsp;&nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp;<sub>LIGO/Virgo/KAGRA gravitational wave candidates</sub>&nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"> &nbsp; <a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle">🌐 Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{superevent_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
<tr><td valign="middle">🗄️</td><td valign="middle"><b>KQL schema</b></td><td valign="middle">yes</td></tr>
</table>

LIGO/Virgo/KAGRA gravitational wave candidates

<sub><b>📍 keyed by</b> <code>{superevent_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Superevent</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#gracedb/fabric-aci) [![](https://img.shields.io/badge/Fabric-Notebook-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#gracedb/fabric-notebook) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gracedb)

<sub>📘 [README](gracedb/README.md) &nbsp;·&nbsp; 📑 [EVENTS](gracedb/EVENTS.md) &nbsp;·&nbsp; 🐳 [CONTAINER](gracedb/CONTAINER.md) &nbsp;·&nbsp; ↗ [gracedb.ligo.org](https://gracedb.ligo.org/)</sub>

</details>

</td></tr></table>

</details>

<!-- root-catalog:end -->


## Code Generation

Projects with checked-in `xreg` manifests regenerate their producer clients with
`xrcg generate`. Use `xrcg` `0.10.1`; the checked-in producer output and the
key-aware Kafka producer behavior now relied on by the repo are generated with
that version. Each project’s `generate_producer.ps1` script uses the checked-in
manifest as the source of truth, validates the `xrcg` version up front, and
refreshes the generated client package from that definition.

## Command Line Tools

Detailed descriptions of each data source, its API, update frequency, and
configuration options are in the per-project README files linked in the tables
above.

### Hydrology and Water Monitoring

**[BAFU Hydro](bafu-hydro/README.md)** -- Swiss Federal Office for the
Environment (BAFU/FOEN) hydrological monitoring network. Forwards water level,
discharge, and temperature observations from approximately 300 stations.
Available as both a Kafka image and an MQTT/UNS image (topic root
`hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/…`).

**[Canada ECCC Water Office](canada-eccc-wateroffice/README.md)** -- Environment
and Climate Change Canada (ECCC) Water Survey of Canada. Real-time water level
and discharge from approximately 2,100 hydrometric stations across all Canadian
provinces and territories, updated every 5 minutes via OGC API Features.

**[CDEC Reservoirs](cdec-reservoirs/README.md)** -- California Data Exchange
Center (CDEC). Real-time reservoir storage, elevation, inflow, and outflow from
over 2,600 stations operated by the Department of Water Resources.

**[CHMI Hydro](chmi-hydro/README.md)** -- Czech Hydrometeorological Institute.
Real-time water level, discharge, and temperature. Polled every 10 minutes.
Available as both a Kafka image and an MQTT/UNS image (topic root
`hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/…`).

**[German Waters](german-waters/README.md)** -- Aggregates water level and
discharge data from 12 German state open data portals (~2,724 stations). Polled
every 15 minutes.

**[Hub’Eau Hydrometrie](hubeau-hydrometrie/README.md)** -- French Hub’Eau
Hydrométrie API, covering ~6,300 stations across France.

**[IMGW Hydro](imgw-hydro/README.md)** -- Polish Institute of Meteorology and
Water Management (IMGW-PIB). Polled every 10 minutes.

**[Ireland OPW Water Level](ireland-opw-waterlevel/README.md)** -- Ireland
Office of Public Works (OPW) hydrometric stations via waterlevel.ie. Real-time
water level, temperature, and voltage data. Polled every 15 minutes.

**[Nepal BIPAD Hydrology](nepal-bipad-hydrology/README.md)** -- Nepal BIPAD
Portal river monitoring network. Real-time water level data from Himalayan river
basins. Polled every 10 minutes.

**[NOAA Tides and Currents](noaa/README.md)** -- NOAA NOS water level and
current data for over 3,000 US stations. Updated every 6 minutes.

**[NOAA NDBC](noaa-ndbc/README.md)** -- National Data Buoy Center buoy
observations across the United States. Polled every 5 minutes.

**[King County Marine](king-county-marine/README.md)** -- Current raw buoy and
mooring telemetry from King County marine monitoring datasets. Emits station
reference events plus normalized water-quality readings for the active marine
datasets.

**[NVE Hydro](nve-hydro/README.md)** -- Norwegian Water Resources and Energy
Directorate (NVE). Water level and discharge observations. Requires a free API
key. Available as both a Kafka image and an MQTT/UNS image (topic root
`hydro/no/nve/nve-hydro/{river_name}/{station_id}/…`).

**[Pegelonline](pegelonline/README.md)** -- German Federal Waterways and
Shipping Administration (WSV). Over 3,000 stations, updated every 15 minutes.

**[RWS Waterwebservices](rws-waterwebservices/README.md)** -- Dutch
Rijkswaterstaat water level data from ~785 stations. Polled every 10 minutes.

**[SMHI Hydro](smhi-hydro/README.md)** -- Swedish Meteorological and
Hydrological Institute (SMHI). Discharge data for hundreds of stations. Polled
every 15 minutes.

**[SNOTEL Snow](snotel/README.md)** -- USDA NRCS SNOTEL (SNOwpack TELemetry)
network. Hourly snow water equivalent, snow depth, temperature, and
precipitation from over 900 sites in the western US and Alaska.

**[SYKE Hydro](syke-hydro/README.md)** -- Finnish Environment Institute (SYKE).
Water level and discharge observations.

**[UK EA Flood Monitoring](uk-ea-flood-monitoring/README.md)** -- UK Environment
Agency. ~4,000 stations across England. Polled every 15 minutes.

**[USGS Instantaneous Values](usgs-iv/README.md)** -- USGS water quality and
quantity data for over 1.5 million US stations. Updated every 15 minutes.

**[USGS NWIS Water Quality](usgs-nwis-wq/README.md)** -- USGS National Water
Information System continuous water quality sensors. Dissolved oxygen, pH,
temperature, conductance, turbidity, and nitrate from over 3,000 monitoring
sites.

**[Waterinfo VMM](waterinfo-vmm/README.md)** -- Belgian Waterinfo.be KIWIS API,
~1,785 stations across Flanders. Polled every 15 minutes.

### Weather and Meteorology

**[AviationWeather.gov](aviationweather/README.md)** -- NOAA Aviation Weather
Center. METAR observations, SIGMET advisories, and station reference data from
aviationweather.gov. Polled every 5 minutes.

**[Blitzortung](blitzortung/README.md)** -- Public LightningMaps / Blitzortung
live websocket feed with global lightning strokes, typically delivered within
seconds of occurrence.

**[BOM Australia](bom-australia/README.md)** -- Australian Bureau of Meteorology.
Half-hourly weather observations from capital city airports: temperature, wind,
pressure, humidity, rainfall, cloud cover, visibility.

**[DWD](dwd/README.md)** -- German Weather Service. ~1,450 stations with
10-minute observations (temperature, precipitation, wind) plus CAP weather
alerts.

**[DWD Pollenflug](dwd-pollenflug/README.md)** -- Deutscher Wetterdienst pollen
forecasts for 27 German regions. Daily forecasts with today/tomorrow/day-after-tomorrow
danger levels for 8 pollen types.

**[Environment Canada](environment-canada/README.md)** -- Environment and
Climate Change Canada (ECCC). ~963 SWOB stations via OGC API with hourly
temperature, humidity, dew point, pressure, wind, and precipitation.

**[GeoSphere Austria](geosphere-austria/README.md)** -- GeoSphere Austria
(formerly ZAMG) TAWES automatic weather stations. 10-minute observations
including temperature, humidity, wind, pressure, precipitation, and sunshine
duration from approximately 280 stations.

**[HKO Hong Kong](hko-hong-kong/README.md)** -- Hong Kong Observatory. 27
temperature stations, 18 rainfall districts, humidity, and UV index. Updated
hourly.

**[JMA Japan](jma-japan/README.md)** -- Japan Meteorological Agency weather
bulletins. Forecasts, warnings, advisories, and risk notifications from the JMA
Atom XML feeds.

**[JMA Bosai AMeDAS](jma-bosai-amedas/README.md)** -- Japan Meteorological Agency
AMeDAS automated weather station network. ~1,300 stations across Japan reporting
temperature, humidity, precipitation, wind, and snow at 10-minute resolution from
the JMA Bosai JSON API.

**[Meteoalarm](meteoalarm/README.md)** -- EUMETNET Meteoalarm. Severe weather
warnings aggregated from 37 European national meteorological services.

**[NOAA NWS](noaa-nws/README.md)** -- National Weather Service active weather
alerts across the United States. Polled every 60 seconds.

**[NWS CAP Alerts](nws-alerts/README.md)** -- US National Weather Service
active alerts via the api.weather.gov GeoJSON endpoint with SAME/UGC geocodes
and VTEC codes.

**[NOAA GOES / SWPC](noaa-goes/README.md)** -- NOAA Space Weather Prediction
Center. Space weather alerts, planetary K-index, and solar wind data. Polled
every 60 seconds.

**[Singapore NEA](singapore-nea/README.md)** -- National Environment Agency of
Singapore. 62 weather stations with temperature, rainfall, wind speed, wind
direction, 2-hour area forecasts, and regional PSI/PM2.5 air-quality readings.

**[SMHI Weather](smhi-weather/README.md)** -- Swedish Meteorological and
Hydrological Institute (SMHI). ~232 stations with hourly temperature, wind gust,
dew point, pressure, humidity, and precipitation.

### Air Quality and Environmental Health

**[Canada AQHI](canada-aqhi/README.md)** -- Environment and Climate Change
Canada. Community-keyed AQHI reference data, current observations, and public
forecast periods across all provinces and territories.

**[Defra AURN](defra-aurn/README.md)** -- UK Defra Automatic Urban and Rural
Network. Station reference data, pollutant timeseries metadata, and hourly
observations from the public SOS API.

**[FMI Finland](fmi-finland/README.md)** -- Finnish Meteorological Institute
air-quality WFS feed. Station reference records plus hourly aggregated pollutant
and AQI observations.

**[GIOŚ Poland](gios-poland/README.md)** -- Polish Chief Inspectorate of
Environmental Protection (GIOŚ). Station and sensor reference data, hourly
pollutant measurements, and air quality index values from approximately 250
monitoring stations.

**[Hong Kong EPD AQHI](hongkong-epd/README.md)** -- Hong Kong Environmental
Protection Department AQHI feed. Station reference events and the latest AQHI
reading per station from the public 24-hour XML feed.

**[IRCELINE Belgium](irceline-belgium/README.md)** -- Belgian IRCELINE SOS API.
Station metadata, pollutant timeseries metadata, and hourly observations with
BelAQI context on the timeseries records.

**[LAQN London](laqn-london/README.md)** -- King’s College London LAQN API.
Monitoring sites, pollutant species metadata, hourly measurements, and Daily
Air Quality Index bulletin records for London.

**[Luchtmeetnet Netherlands](luchtmeetnet-nl/README.md)** -- Dutch
Luchtmeetnet open API. Station and component reference data, hourly station
measurements, and Dutch LKI air-quality-index readings.

**[EPA UV Index](epa-uv/README.md)** -- United States EPA Envirofacts UV
forecast service. Location-keyed hourly and daily UV forecast events for
configured city/state pairs.

**[Sensor.Community](sensor-community/README.md)** -- Sensor.Community public
JSON sensor feeds. Sensor reference metadata plus particulate and climate sensor
readings from the community network worldwide.

**[Singapore NEA Air Quality](singapore-nea/README.md)** -- The Singapore NEA
bridge also publishes regional air-quality reference data, PSI readings, and
PM2.5 readings alongside the existing weather feed.

**[UBA AirData](uba-airdata/README.md)** -- German Umweltbundesamt air-data
API. Station reference records, pollutant component catalog events, and hourly
measurements from the federal monitoring network.

**[Wallonia ISSeP](wallonia-issep/README.md)** -- Wallonia ISSeP (Institut
Scientifique de Service Public) low-cost air quality sensor network across
Wallonia, Belgium. Sensor reference data and near-real-time observations.

### Disaster Alerts and Civil Protection

**[Australian Wildfires](australia-wildfires/README.md)** -- Aggregated bushfire
incident data from NSW Rural Fire Service, Queensland Fire and Emergency
Services, and Victoria’s Country Fire Authority. Normalized fire incident events.

**[EAWS ALBINA Avalanche](eaws-albina/README.md)** -- European Avalanche
Warning Services (EAWS) ALBINA system. Daily avalanche danger bulletins in
CAAMLv6 standard for the European Alps (Tirol, South Tyrol, Trentino). Five
danger levels with aspect/elevation detail.

**[GDACS](gdacs/README.md)** -- Global Disaster Alert and Coordination System.
Earthquake, tropical cyclone, flood, volcano, flash flood, and drought alerts
from the GDACS RSS feed.

**[INPE DETER Brazil](inpe-deter-brazil/README.md)** -- INPE TerraBrasilis
DETER real-time deforestation detection system. Deforestation alerts for the
Amazon and Cerrado biomes with area, coordinates, and satellite data.

**[JMA Bosai Quake](jma-bosai-quake/README.md)** -- Japan Meteorological Agency
earthquake bulletins from the Bosai JSON API. Hypocenter, magnitude, JMA
intensity (shindo 1–7), affected prefectures/cities, and tsunami flag.
Append-style event stream keyed by `{event_id}/{serial}` covering 発表/訂正/取消
bulletin lifecycle.

**[JMA Bosai Volcano](jma-bosai-volcano/README.md)** -- Japan Meteorological
Agency volcanic warnings and eruption observations for all 111 Japanese
volcanoes. Alert-level changes (噴火警戒レベル 1–5), eruption-event reports,
and stable volcano reference catalog.

**[JMA Bosai Warning & Tsunami](jma-bosai-warning/README.md)** -- Japan
Meteorological Agency per-prefecture weather warnings (advisory, warning,
emergency warning) covering 28 hazard categories plus the tsunami warning feed
(forecasts + VTSE51/52 observed wave heights).

**[NIFC USA Wildfires](nifc-usa-wildfires/README.md)** -- National Interagency
Fire Center (NIFC) active wildfire incident data from the ArcGIS Feature
Service. Incident name, location, acres burned, containment percentage, and
discovery date.

**[NINA/BBK](nina-bbk/README.md)** -- German Federal Office of Civil Protection
(BBK) NINA warning system. Aggregates warnings from six providers: MOWAS
(federal), KATWARN, BIWAPP, DWD, LHP (flood centers), and Police.

**[PTWC Tsunami](ptwc-tsunami/README.md)** -- NOAA National Tsunami Warning
Center (NTWC) and Pacific Tsunami Warning Center (PTWC). Tsunami bulletins from
two Atom XML feeds covering the Pacific, Atlantic, and Caribbean.

**[Seattle Fire 911](seattle-911/README.md)** -- Seattle Open Data real-time
Fire 911 calls feed. Incident-keyed dispatch events with address and published
coordinates.

**[USGS Earthquakes](usgs-earthquakes/README.md)** -- Real-time earthquake
events from the USGS GeoJSON feeds with deduplication. Polled every 60 seconds.

### Radiation Monitoring

**[BfS ODL](bfs-odl/README.md)** -- German Federal Office for Radiation
Protection (BfS) ODL ambient gamma dose rate monitoring network. Approximately
1,700 stationary probes measuring hourly averaged gamma dose rates in µSv/h,
with cosmic and terrestrial decomposition. Open WFS data interface, no auth.
Polled hourly.

**[EURDEP Radiation](eurdep-radiation/README.md)** -- European Radiological
Data Exchange Platform (EURDEP). Ambient gamma dose rate monitoring from
approximately 5,500 stations across 39 European countries. Hourly averages in
µSv/h.

**[USGS Geomagnetism](usgs-geomag/README.md)** -- USGS Geomagnetism Program.
1-minute geomagnetic field variation data (H, D, Z, F components) from 14 US
observatories.

### Maritime and Vessel Tracking

**[AISStream](aisstream/README.md)** -- AISStream.io WebSocket API. Real-time
AIS vessel tracking from ships worldwide (~200 km from shore). Publishes 23 AIS
message types. Requires API key. The free service can be unreliable.

**[Digitraffic Maritime](digitraffic-maritime/README.md)** -- Finland’s
Digitraffic Marine MQTT stream. AIS vessel positions and metadata from the
Finnish coastal zone and Baltic Sea. ~35 messages/second. Open data (CC 4.0 BY).

**[Kystverket AIS](kystverket-ais/README.md)** -- Norwegian Coastal
Administration raw TCP AIS stream. NMEA sentences from 50+ stations covering the
Norwegian economic zone, Svalbard, and Jan Mayen. ~34 messages/second (~2.9M/day).

### Aviation

**[Mode-S](mode-s/README.md)** -- ADS-B aircraft position and telemetry data
from dump1090 receivers. Polled every 60 seconds.

**[VATSIM](vatsim/README.md)** -- VATSIM virtual aviation network live data feed.
Pilot positions, controller positions, ATIS, pre-files, and network status from
the VATSIM v3 JSON feed.

### Road Transport

**[Autobahn](autobahn/README.md)** -- German Autobahn API. Roadworks, warnings,
closures, parking areas, charging stations, and webcams. Uses ETags and local
state to detect changes. Available as both a Kafka image and an MQTT/UNS image
(topic root `traffic/de/autobahn/autobahn/{road}/{kind}/{identifier}/{state}`).

**[Digitraffic Road](digitraffic-road/README.md)** -- Finland’s Digitraffic Road
MQTT stream. TMS sensor readings (vehicle counts and speeds from 500+ stations),
road weather measurements (350+ stations), traffic messages, and maintenance
vehicle tracking. Open data (CC 4.0 BY).

**[French Road Traffic](french-road-traffic/README.md)** -- French national road
traffic data via DATEX II from Bison Futé (tipi.bison-fute.gouv.fr). Traffic flow
measurements (~1,000 sites with vehicle counts and speeds) and road events (~300
situations including accidents, roadworks, and restrictions). Polled every 6
minutes.

**[GTFS Realtime](gtfs/README.md)** -- GTFS and GTFS-RT data from 1,000+ public
transport agencies worldwide. Vehicle positions, trip updates, and alerts. MTA
feeds alone produce over 50 GB/day.

**[Madrid Traffic](madrid-traffic/README.md)** -- Madrid Informo traffic sensor
API. Real-time readings from approximately 4,000 sensors across Madrid’s road
network including the M-30 ring motorway. Updated every 5 minutes.

**[NDW Netherlands Traffic](ndl-netherlands/README.md)** -- Dutch NDW (Nationaal
Dataportaal Wegverkeer) DATEX II traffic data. Speed, travel time, and traffic
situations from the national road network.

**[TfL Road Traffic](tfl-road-traffic/README.md)** -- Transport for London (TfL)
Unified API road corridor status and disruption data. Road corridor reference
data, real-time aggregate traffic status per corridor, and active road
disruptions including incidents, planned works, and road closures across
London's TfL-managed road network (A-roads and motorways such as A2, A12, M25).
Disruption events are deduped by ID and last-modified time.

**[Nextbus](nextbus/README.md)** -- Public transit arrivals from the Nextbus
service.

**[Paris Bicycle Counters](paris-bicycle-counters/README.md)** -- Paris Open
Data bicycle counting stations. Hourly bicycle counts from 141 permanent
counting stations across Paris with counter location reference data.

**[Seattle Street Closures](seattle-street-closures/README.md)** -- Seattle
Open Data street closure schedule feed. Permit-keyed closure windows with
street segments, dates, and serialized geometry snapshots.

**[Tokyo Docomo Bikeshare](tokyo-docomo-bikeshare/README.md)** -- Tokyo Docomo
Bikeshare real-time availability. GBFS 2.3 feed from the Open Data Platform for
Transportation (ODPT) covering 1,794 dock-based stations across central Tokyo
wards. System metadata, station locations (bilingual names), and real-time bike
and dock availability updated on a 60-second TTL.

**[US CBP Border Wait](cbp-border-wait/README.md)** -- US Customs and Border
Protection border wait times. Real-time delay data for approximately 81 land
border ports of entry along the US-Canada and US-Mexico borders.

**[WSDOT](wsdot/README.md)** -- Washington State DOT traffic flow data from
approximately 1,000 inductive loop sensors across five regions. Level of Service
readings updated every 90 seconds. Requires a free API access code.

### Railway

**[iRail](irail/README.md)** -- Belgian railway real-time data from the iRail
API. Station metadata and departure boards for approximately 600 NMBS/SNCB
stations, including delays, platform assignments, cancellations, and occupancy.
No authentication. Rate-limited to 3 requests/second; full cycle ~3–4 minutes.

### Nightlife and Live Entertainment

**[Xceed](xceed/README.md)** -- Xceed Open Event API. European nightlife and
live-entertainment events including clubs, bars, parties, and festivals. Emits
event reference data (schedule, venue, cover image) and admission telemetry
(per-tier ticket-availability signals including `isSoldOut` and `isSalesClosed`).
No authentication required. Polled every 5 minutes by default.

### Energy and Infrastructure

**[Carbon Intensity UK](carbon-intensity/README.md)** -- National Grid ESO Carbon
Intensity API. National carbon intensity (gCO₂/kWh forecast and actual) and
fuel-mix generation percentages for 10 fuel types. Polled every 30 minutes.

**[Elexon BMRS](elexon-bmrs/README.md)** -- Elexon Balancing Mechanism
Reporting Service. GB electricity generation mix, demand outturn, system
frequency, and interconnector flows. Settlement-period-keyed data from the BMRS
API.

**[Energi Data Service](energidataservice-dk/README.md)** -- Energinet Energi
Data Service. Danish power system snapshots (CO₂, solar, wind, exchange flows)
and day-ahead spot prices per bidding zone.

**[Energy-Charts](energy-charts/README.md)** -- Fraunhofer ISE Energy-Charts
API. Electricity generation, prices, and grid carbon signals for 40+ European
countries. CC BY 4.0 open data.

**[ENTSO-E](entsoe/README.md)** -- European electricity market data from the
ENTSO-E Transparency Platform. Generation output, day-ahead prices, load,
forecasts, installed capacity, reservoir filling, and cross-border flows.

**[TEPCO Denkiyoho](tepco-denkiyoho/README.md)** -- Tokyo Electric Power Company
でんき予報 supply/demand feed for the Kanto region (Tokyo + 8 prefectures). Peak
supply capacity, hourly demand forecast, 5-min actuals, solar PV generation, and
reserve margin from the Shift-JIS CSV publication, refreshed every 5 minutes.

### Social Media and News

**[Bluesky Firehose](bluesky/README.md)** -- Bluesky AT Protocol firehose.
Posts, likes, reposts, follows, blocks, and profile updates. Supports selective
filtering and cursor management for resumable streaming.

**[OpenStreetMap Diffs](wikimedia-osm-diffs/README.md)** -- OpenStreetMap
minutely replication diffs. Every node, way, and relation create/modify/delete
from the OSM replication feed as individual CloudEvents.

**[RSS Feeds](rss/README.md)** -- Configurable RSS/Atom feed poller. Supports
feed URLs or OPML files. Only forwards new items.

**[Wikimedia EventStreams](wikimedia-eventstreams/README.md)** -- Wikimedia’s
public recentchange stream for edits, page creations, and log actions across
Wikipedia, Wikidata, Commons, and sister projects.

### Public Events

**[Billetto](billetto/README.md)** -- Billetto pan-European event-discovery
platform. Polls the public events API for new and updated ticketed events
across Denmark, the United Kingdom, Germany, Sweden, Norway, Finland, Belgium,
Austria, and Ireland. Emits event schedule, venue, organizer, pricing, and
ticket availability as CloudEvents keyed by stable Billetto event ID.

### Scientific Research

**[GraceDB](gracedb/README.md)** -- LIGO/Virgo/KAGRA GraceDB gravitational wave
candidate event database. Superevent alerts including chirp mass, false alarm
rate, classification probabilities, and sky localization data.

### Public Events

**[Fienta](fienta/README.md)** -- European public event ticketing platform
(Estonia, Latvia, Lithuania, and other European markets). Emits full event
reference data including name, location, organizer, and schedule, plus
sale-status change telemetry (`onSale`, `soldOut`, `notOnSale`, `saleEnded`)
whenever a public event's ticket status changes. Polling the Fienta public REST
API requires no authentication.

### External

**[Forza Motorsport PC](https://github.com/clemensv/forza-telemetry-bridge)** --
Racing game telemetry bridge (separate repository). Captures UDP telemetry from
Forza Motorsport games and forwards to Event Hubs or Fabric Event Streams.
Binary release available.


## AMQP companion feeders for maritime and tracking sources

AMQP 1.0 companion images and Service Bus deployment templates are available for `kystverket-ais`, `king-county-marine`, `vatsim`, `mode-s`, and `aisstream` via each source's `Dockerfile.amqp`, `azure-template-with-servicebus.json`, and container documentation.




<!-- B2-weather MQTT+AMQP companions -->
- `aviationweather`: MQTT + AMQP companion feeders (`aviationweather-mqtt`, `aviationweather-amqp`).
- `blitzortung`: MQTT + AMQP companion feeders (`blitzortung-mqtt`, `blitzortung-amqp`).
- `bom-australia`: MQTT + AMQP companion feeders (`bom-australia-mqtt`, `bom-australia-amqp`).
- `dwd`: MQTT + AMQP companion feeders (`dwd-mqtt`, `dwd-amqp`).
- `dwd-pollenflug`: MQTT + AMQP companion feeders (`dwd-pollenflug-mqtt`, `dwd-pollenflug-amqp`).
- `environment-canada`: MQTT + AMQP companion feeders (`environment-canada-mqtt`, `environment-canada-amqp`).
- `geosphere-austria`: MQTT + AMQP companion feeders (`geosphere-austria-mqtt`, `geosphere-austria-amqp`).
- `hko-hong-kong`: MQTT + AMQP companion feeders (`hko-hong-kong-mqtt`, `hko-hong-kong-amqp`).
- `jma-japan`: MQTT + AMQP companion feeders (`jma-japan-mqtt`, `jma-japan-amqp`).
- `kmi-belgium`: MQTT + AMQP companion feeders (`kmi-belgium-mqtt`, `kmi-belgium-amqp`).
- `noaa-nws`: MQTT + AMQP companion feeders (`noaa-nws-mqtt`, `noaa-nws-amqp`).
- `smhi-weather`: MQTT + AMQP companion feeders (`smhi-weather-mqtt`, `smhi-weather-amqp`).

