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

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Switzerland" title="Switzerland" src="https://flagcdn.com/20x15/ch.png" width="20" height="15"> &nbsp;<b>BAFU Hydro</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~300 stations, FOEN</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Switzerland" title="Switzerland" src="https://flagcdn.com/20x15/ch.png" width="20" height="15"> &nbsp;Switzerland</td></tr>
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

<sub>📘 <a href="bafu-hydro/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="bafu-hydro/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="bafu-hydro/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.hydrodaten.admin.ch/">hydrodaten.admin.ch</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Canada" title="Canada" src="https://flagcdn.com/20x15/ca.png" width="20" height="15"> &nbsp;<b>Canada ECCC Water Office</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~2,100 hydrometric stations, ECCC/WSC</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Canada" title="Canada" src="https://flagcdn.com/20x15/ca.png" width="20" height="15"> &nbsp;Canada</td></tr>
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

<sub>📘 <a href="canada-eccc-wateroffice/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="canada-eccc-wateroffice/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="canada-eccc-wateroffice/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://wateroffice.ec.gc.ca/">wateroffice.ec.gc.ca</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="California" title="California" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>CDEC Reservoirs</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~2,600 stations, DWR</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="California" title="California" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;California</td></tr>
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

<sub>📘 <a href="cdec-reservoirs/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="cdec-reservoirs/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="cdec-reservoirs/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://cdec.water.ca.gov/">cdec.water.ca.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Czech Republic" title="Czech Republic" src="https://flagcdn.com/20x15/cz.png" width="20" height="15"> &nbsp;<b>CHMI Hydro</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;CHMU</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Czech Republic" title="Czech Republic" src="https://flagcdn.com/20x15/cz.png" width="20" height="15"> &nbsp;Czech Republic</td></tr>
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

<sub>📘 <a href="chmi-hydro/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="chmi-hydro/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="chmi-hydro/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.chmi.cz/">chmi.cz</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>German Waters</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;12 state portals, ~2,724 stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="german-waters/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="german-waters/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="german-waters/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://hvz.lubw.baden-wuerttemberg.de/">hvz.lubw.baden-wuerttemberg.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="France" title="France" src="https://flagcdn.com/20x15/fr.png" width="20" height="15"> &nbsp;<b>Hub'Eau Hydrometrie</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~6,300 stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="France" title="France" src="https://flagcdn.com/20x15/fr.png" width="20" height="15"> &nbsp;France</td></tr>
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

<sub>📘 <a href="hubeau-hydrometrie/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="hubeau-hydrometrie/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="hubeau-hydrometrie/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://hubeau.eaufrance.fr/">hubeau.eaufrance.fr</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Poland" title="Poland" src="https://flagcdn.com/20x15/pl.png" width="20" height="15"> &nbsp;<b>IMGW Hydro</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;IMGW-PIB</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Poland" title="Poland" src="https://flagcdn.com/20x15/pl.png" width="20" height="15"> &nbsp;Poland</td></tr>
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

<sub>📘 <a href="imgw-hydro/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="imgw-hydro/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="imgw-hydro/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.imgw.pl/">imgw.pl</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Ireland" title="Ireland" src="https://flagcdn.com/20x15/ie.png" width="20" height="15"> &nbsp;<b>Ireland OPW Water Level</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~500 OPW hydrometric stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Ireland" title="Ireland" src="https://flagcdn.com/20x15/ie.png" width="20" height="15"> &nbsp;Ireland</td></tr>
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

<sub>📘 <a href="ireland-opw-waterlevel/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="ireland-opw-waterlevel/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="ireland-opw-waterlevel/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://waterlevel.ie/">waterlevel.ie</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Washington State / Puget Sound" title="Washington State / Puget Sound" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>King County Marine</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;buoy and mooring telemetry</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Washington State / Puget Sound" title="Washington State / Puget Sound" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;Washington State / Puget Sound</td></tr>
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

<sub>📘 <a href="king-county-marine/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="king-county-marine/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="king-county-marine/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://green2.kingcounty.gov/marine/">green2.kingcounty.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Nepal" title="Nepal" src="https://flagcdn.com/20x15/np.png" width="20" height="15"> &nbsp;<b>Nepal BIPAD Hydrology</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;Himalayan river basins, BIPAD</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Nepal" title="Nepal" src="https://flagcdn.com/20x15/np.png" width="20" height="15"> &nbsp;Nepal</td></tr>
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

<sub>📘 <a href="nepal-bipad-hydrology/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="nepal-bipad-hydrology/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="nepal-bipad-hydrology/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://bipadportal.gov.np/">bipadportal.gov.np</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>NOAA NDBC</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;buoy observations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="noaa-ndbc/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="noaa-ndbc/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="noaa-ndbc/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.ndbc.noaa.gov/">ndbc.noaa.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>NOAA Tides & Currents</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~3,000 stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="noaa/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="noaa/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="noaa/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://tidesandcurrents.noaa.gov/">tidesandcurrents.noaa.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Norway" title="Norway" src="https://flagcdn.com/20x15/no.png" width="20" height="15"> &nbsp;<b>NVE Hydro</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;NVE (requires free API key)</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Norway" title="Norway" src="https://flagcdn.com/20x15/no.png" width="20" height="15"> &nbsp;Norway</td></tr>
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

<sub>📘 <a href="nve-hydro/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="nve-hydro/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="nve-hydro/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.nve.no/">nve.no</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>Pegelonline</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;federal waterways, ~3,000 stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="pegelonline/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="pegelonline/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="pegelonline/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.pegelonline.wsv.de/">pegelonline.wsv.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;<b>RWS Waterwebservices</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~785 stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;Netherlands</td></tr>
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

<sub>📘 <a href="rws-waterwebservices/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="rws-waterwebservices/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="rws-waterwebservices/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://waterinfo.rws.nl/">waterinfo.rws.nl</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Sweden" title="Sweden" src="https://flagcdn.com/20x15/se.png" width="20" height="15"> &nbsp;<b>SMHI Hydro</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;SMHI</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Sweden" title="Sweden" src="https://flagcdn.com/20x15/se.png" width="20" height="15"> &nbsp;Sweden</td></tr>
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

<sub>📘 <a href="smhi-hydro/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="smhi-hydro/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="smhi-hydro/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.smhi.se/">smhi.se</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Western US & Alaska" title="Western US & Alaska" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>SNOTEL Snow</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~900 snowpack stations, NRCS</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Western US & Alaska" title="Western US & Alaska" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;Western US & Alaska</td></tr>
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

<sub>📘 <a href="snotel/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="snotel/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="snotel/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.nrcs.usda.gov/wps/portal/wcc/home/">nrcs.usda.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Finland" title="Finland" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;<b>SYKE Hydro</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;SYKE</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Finland" title="Finland" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;Finland</td></tr>
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

<sub>📘 <a href="syke-hydro/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="syke-hydro/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="syke-hydro/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.syke.fi/">syke.fi</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="England" title="England" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;<b>UK EA Flood Monitoring</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~4,000 stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="England" title="England" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;England</td></tr>
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

<sub>📘 <a href="uk-ea-flood-monitoring/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="uk-ea-flood-monitoring/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="uk-ea-flood-monitoring/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://environment.data.gov.uk/flood-monitoring/doc/reference">environment.data.gov.uk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>USGS Instantaneous Values</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~1.5M stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="usgs-iv/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="usgs-iv/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="usgs-iv/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://waterdata.usgs.gov/">waterdata.usgs.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>USGS NWIS Water Quality</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~3,000 continuous WQ sites</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="usgs-nwis-wq/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="usgs-nwis-wq/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="usgs-nwis-wq/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://waterdata.usgs.gov/">waterdata.usgs.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Belgium / Flanders" title="Belgium / Flanders" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;<b>Waterinfo VMM</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~1,785 stations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Belgium / Flanders" title="Belgium / Flanders" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;Belgium / Flanders</td></tr>
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

<sub>📘 <a href="waterinfo-vmm/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="waterinfo-vmm/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="waterinfo-vmm/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.waterinfo.be/">waterinfo.be</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>⛅ Weather and Meteorology</b> &nbsp;<sub>21 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>AviationWeather.gov</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;METAR, SIGMET advisories</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="aviationweather/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="aviationweather/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="aviationweather/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://aviationweather.gov/">aviationweather.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>Blitzortung</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;community lightning strokes, seconds latency</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="blitzortung/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="blitzortung/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="blitzortung/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.blitzortung.org/">blitzortung.org</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Australia" title="Australia" src="https://flagcdn.com/20x15/au.png" width="20" height="15"> &nbsp;<b>BOM Australia</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~8 capital city airports, half-hourly obs</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Australia" title="Australia" src="https://flagcdn.com/20x15/au.png" width="20" height="15"> &nbsp;Australia</td></tr>
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

<sub>📘 <a href="bom-australia/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="bom-australia/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="bom-australia/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.bom.gov.au/">bom.gov.au</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Denmark" title="Denmark" src="https://flagcdn.com/20x15/dk.png" width="20" height="15"> &nbsp;<b>DMI</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-_-eaeef2?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-4-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-2-2496ed?style=flat-square"><sub>&nbsp;&nbsp;DMI observation triad (metObs + oceanObs + lightning)</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Denmark" title="Denmark" src="https://flagcdn.com/20x15/dk.png" width="20" height="15"> &nbsp;Denmark</td></tr>
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

<sub>📘 <a href="dmi/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="dmi/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="dmi/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.dmi.dk/">dmi.dk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Denmark" title="Denmark" src="https://flagcdn.com/20x15/dk.png" width="20" height="15"> &nbsp;<b>DMI</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-_-eaeef2?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-4-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-2-2496ed?style=flat-square"><sub>&nbsp;&nbsp;meteorological observations, sea level, lightning strikes</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Denmark" title="Denmark" src="https://flagcdn.com/20x15/dk.png" width="20" height="15"> &nbsp;Denmark</td></tr>
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

<sub>📘 <a href="dmi/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="dmi/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="dmi/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.dmi.dk/">dmi.dk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>DWD</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~1,450 stations, observations and CAP alerts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="dwd/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="dwd/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="dwd/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.dwd.de/">dwd.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>DWD Pollenflug</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;daily pollen forecasts, 27 regions</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="dwd-pollenflug/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="dwd-pollenflug/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="dwd-pollenflug/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.dwd.de/EN/specialusers/medical/pollenflug/pollenflug_node.html">dwd.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Canada" title="Canada" src="https://flagcdn.com/20x15/ca.png" width="20" height="15"> &nbsp;<b>Environment Canada</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~963 SWOB stations, hourly obs</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Canada" title="Canada" src="https://flagcdn.com/20x15/ca.png" width="20" height="15"> &nbsp;Canada</td></tr>
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

<sub>📘 <a href="environment-canada/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="environment-canada/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="environment-canada/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://weather.gc.ca/">weather.gc.ca</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Austria" title="Austria" src="https://flagcdn.com/20x15/at.png" width="20" height="15"> &nbsp;<b>GeoSphere Austria</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~280 TAWES stations, 10-min obs</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Austria" title="Austria" src="https://flagcdn.com/20x15/at.png" width="20" height="15"> &nbsp;Austria</td></tr>
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

<sub>📘 <a href="geosphere-austria/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="geosphere-austria/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="geosphere-austria/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.geosphere.at/">geosphere.at</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Hong Kong" title="Hong Kong" src="https://flagcdn.com/20x15/hk.png" width="20" height="15"> &nbsp;<b>HKO Hong Kong</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;27 temp stations, 18 rainfall districts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Hong Kong" title="Hong Kong" src="https://flagcdn.com/20x15/hk.png" width="20" height="15"> &nbsp;Hong Kong</td></tr>
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

<sub>📘 <a href="hko-hong-kong/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="hko-hong-kong/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="hko-hong-kong/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.hko.gov.hk/">hko.gov.hk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;<b>JMA Bosai AMeDAS</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~1,300 AMeDAS stations, 10-min observations via Bosai JSON API</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;Japan</td></tr>
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

<sub>📘 <a href="jma-bosai-amedas/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="jma-bosai-amedas/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="jma-bosai-amedas/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.jma.go.jp/bosai/amedas/">jma.go.jp</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;<b>JMA Japan</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;weather bulletins, warnings, forecasts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;Japan</td></tr>
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

<sub>📘 <a href="jma-japan/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="jma-japan/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="jma-japan/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.jma.go.jp/">jma.go.jp</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Belgium" title="Belgium" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;<b>KMI Belgium</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~14 AWS stations, 10-min observations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Belgium" title="Belgium" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;Belgium</td></tr>
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

<sub>📘 <a href="kmi-belgium/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="kmi-belgium/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="kmi-belgium/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.meteo.be/">meteo.be</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;<b>Meteoalarm</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;37 countries, severe weather warnings</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;Europe</td></tr>
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

<sub>📘 <a href="meteoalarm/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="meteoalarm/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="meteoalarm/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://meteoalarm.org/">meteoalarm.org</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>NOAA GOES / SWPC</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;space weather, solar wind, K-index</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="noaa-goes/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="noaa-goes/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="noaa-goes/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.swpc.noaa.gov/">swpc.noaa.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>NOAA NWS</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;weather alerts, CAP</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="noaa-nws/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="noaa-nws/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="noaa-nws/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.weather.gov/">weather.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>NOAA SWPC L1</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="noaa-swpc-l1/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="noaa-swpc-l1/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="noaa-swpc-l1/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.swpc.noaa.gov/">swpc.noaa.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>NWS CAP Alerts</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;active alerts via api.weather.gov</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="nws-alerts/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="nws-alerts/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="nws-alerts/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.weather.gov/">weather.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>NWS Forecast Zones</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;configurable land and marine forecast zones</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="nws-forecasts/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="nws-forecasts/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="nws-forecasts/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.weather.gov/">weather.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Singapore" title="Singapore" src="https://flagcdn.com/20x15/sg.png" width="20" height="15"> &nbsp;<b>Singapore NEA</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;62 weather stations + 5 air-quality regions</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Singapore" title="Singapore" src="https://flagcdn.com/20x15/sg.png" width="20" height="15"> &nbsp;Singapore</td></tr>
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

<sub>📘 <a href="singapore-nea/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="singapore-nea/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="singapore-nea/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.nea.gov.sg/">nea.gov.sg</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Sweden" title="Sweden" src="https://flagcdn.com/20x15/se.png" width="20" height="15"> &nbsp;<b>SMHI Weather</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~232 stations, hourly obs</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Sweden" title="Sweden" src="https://flagcdn.com/20x15/se.png" width="20" height="15"> &nbsp;Sweden</td></tr>
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

<sub>📘 <a href="smhi-weather/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="smhi-weather/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="smhi-weather/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.smhi.se/">smhi.se</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>🌫️ Air Quality and Environmental Health</b> &nbsp;<sub>12 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Canada" title="Canada" src="https://flagcdn.com/20x15/ca.png" width="20" height="15"> &nbsp;<b>Canada AQHI</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;community AQHI observations and forecasts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Canada" title="Canada" src="https://flagcdn.com/20x15/ca.png" width="20" height="15"> &nbsp;Canada</td></tr>
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

<sub>📘 <a href="canada-aqhi/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="canada-aqhi/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="canada-aqhi/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://weather.gc.ca/airquality/pages/index_e.html">weather.gc.ca</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United Kingdom" title="United Kingdom" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;<b>Defra AURN</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;300+ monitoring locations, hourly pollutants</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United Kingdom" title="United Kingdom" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;United Kingdom</td></tr>
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

<sub>📘 <a href="defra-aurn/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="defra-aurn/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="defra-aurn/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://uk-air.defra.gov.uk/">uk-air.defra.gov.uk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>EPA UV Index</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;city-scoped hourly and daily UV forecasts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="epa-uv/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="epa-uv/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="epa-uv/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.epa.gov/sunsafety/uv-index-1">epa.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Finland" title="Finland" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;<b>FMI Finland</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;hourly air quality observations via FMI WFS</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Finland" title="Finland" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;Finland</td></tr>
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

<sub>📘 <a href="fmi-finland/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="fmi-finland/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="fmi-finland/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://en.ilmatieteenlaitos.fi/">en.ilmatieteenlaitos.fi</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Poland" title="Poland" src="https://flagcdn.com/20x15/pl.png" width="20" height="15"> &nbsp;<b>GIOŚ Poland</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~250 stations, hourly pollutants + AQI</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Poland" title="Poland" src="https://flagcdn.com/20x15/pl.png" width="20" height="15"> &nbsp;Poland</td></tr>
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

<sub>📘 <a href="gios-poland/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="gios-poland/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="gios-poland/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.gios.gov.pl/">gios.gov.pl</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Hong Kong" title="Hong Kong" src="https://flagcdn.com/20x15/hk.png" width="20" height="15"> &nbsp;<b>Hong Kong EPD AQHI</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;18 AQHI stations, hourly health index</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Hong Kong" title="Hong Kong" src="https://flagcdn.com/20x15/hk.png" width="20" height="15"> &nbsp;Hong Kong</td></tr>
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

<sub>📘 <a href="hongkong-epd/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="hongkong-epd/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="hongkong-epd/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.aqhi.gov.hk/">aqhi.gov.hk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Belgium" title="Belgium" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;<b>IRCELINE Belgium</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;station, timeseries, and hourly observations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Belgium" title="Belgium" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;Belgium</td></tr>
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

<sub>📘 <a href="irceline-belgium/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="irceline-belgium/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="irceline-belgium/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.irceline.be/">irceline.be</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="London" title="London" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;<b>LAQN London</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;site metadata, species, hourly measurements</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="London" title="London" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;London</td></tr>
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

<sub>📘 <a href="laqn-london/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="laqn-london/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="laqn-london/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.londonair.org.uk/">londonair.org.uk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;<b>Luchtmeetnet Netherlands</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;station measurements, components, LKI index</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;Netherlands</td></tr>
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

<sub>📘 <a href="luchtmeetnet-nl/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="luchtmeetnet-nl/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="luchtmeetnet-nl/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.luchtmeetnet.nl/">luchtmeetnet.nl</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>Sensor.Community</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;citizen air sensors, PM and climate readings</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="sensor-community/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="sensor-community/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="sensor-community/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://sensor.community/">sensor.community</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>UBA AirData</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;stations, pollutant components, hourly measures</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="uba-airdata/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="uba-airdata/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="uba-airdata/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.umweltbundesamt.de/">umweltbundesamt.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Belgium / Wallonia" title="Belgium / Wallonia" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;<b>Wallonia ISSeP</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;low-cost air quality sensors</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Belgium / Wallonia" title="Belgium / Wallonia" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;Belgium / Wallonia</td></tr>
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

<sub>📘 <a href="wallonia-issep/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="wallonia-issep/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="wallonia-issep/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.issep.be/">issep.be</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>🚨 Disaster Alerts and Civil Protection</b> &nbsp;<sub>12 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Australia" title="Australia" src="https://flagcdn.com/20x15/au.png" width="20" height="15"> &nbsp;<b>Australian Wildfires</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;NSW, QLD, VIC bushfire incidents</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Australia" title="Australia" src="https://flagcdn.com/20x15/au.png" width="20" height="15"> &nbsp;Australia</td></tr>
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

<sub>📘 <a href="australia-wildfires/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="australia-wildfires/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="australia-wildfires/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.rfs.nsw.gov.au/">rfs.nsw.gov.au</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="European Alps" title="European Alps" src="https://flagcdn.com/20x15/at.png" width="20" height="15"> &nbsp;<b>EAWS ALBINA Avalanche</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;daily avalanche bulletins, CAAMLv6</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="European Alps" title="European Alps" src="https://flagcdn.com/20x15/at.png" width="20" height="15"> &nbsp;European Alps</td></tr>
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

<sub>📘 <a href="eaws-albina/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="eaws-albina/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="eaws-albina/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://avalanche.report/">avalanche.report</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>GDACS</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;earthquakes, floods, cyclones, volcanoes, droughts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="gdacs/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="gdacs/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="gdacs/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.gdacs.org/">gdacs.org</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Brazil" title="Brazil" src="https://flagcdn.com/20x15/br.png" width="20" height="15"> &nbsp;<b>INPE DETER Brazil</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;Amazon & Cerrado deforestation alerts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Brazil" title="Brazil" src="https://flagcdn.com/20x15/br.png" width="20" height="15"> &nbsp;Brazil</td></tr>
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

<sub>📘 <a href="inpe-deter-brazil/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="inpe-deter-brazil/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="inpe-deter-brazil/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="http://terrabrasilis.dpi.inpe.br/">terrabrasilis.dpi.inpe.br</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;<b>JMA Bosai Quake</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;JMA earthquake bulletins (hypocenter, magnitude, JMA intensity)</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;Japan</td></tr>
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

<sub>📘 <a href="jma-bosai-quake/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="jma-bosai-quake/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="jma-bosai-quake/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.jma.go.jp/bosai/map.html?contents=earthquake_map">jma.go.jp</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;<b>JMA Bosai Volcano</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;111 volcanoes, alert levels, eruption observations</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;Japan</td></tr>
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

<sub>📘 <a href="jma-bosai-volcano/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="jma-bosai-volcano/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="jma-bosai-volcano/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.jma.go.jp/bosai/map.html?contents=volcano">jma.go.jp</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;<b>JMA Bosai Warning & Tsunami</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;per-prefecture weather warnings + tsunami alerts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Japan" title="Japan" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;Japan</td></tr>
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

<sub>📘 <a href="jma-bosai-warning/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="jma-bosai-warning/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="jma-bosai-warning/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.jma.go.jp/bosai/map.html?contents=warning">jma.go.jp</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>NIFC USA Wildfires</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;active wildfire incidents, NIFC</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="nifc-usa-wildfires/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="nifc-usa-wildfires/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="nifc-usa-wildfires/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.nifc.gov/">nifc.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>NINA/BBK</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;MOWAS, KATWARN, BIWAPP, DWD, LHP, Police</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="nina-bbk/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="nina-bbk/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="nina-bbk/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://warnung.bund.de/">warnung.bund.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Pacific and Atlantic" title="Pacific and Atlantic" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>PTWC Tsunami</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;NOAA tsunami bulletins</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Pacific and Atlantic" title="Pacific and Atlantic" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Pacific and Atlantic</td></tr>
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

<sub>📘 <a href="ptwc-tsunami/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="ptwc-tsunami/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="ptwc-tsunami/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.tsunami.gov/">tsunami.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Seattle" title="Seattle" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>Seattle Fire 911</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;real-time fire dispatch incidents</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Seattle" title="Seattle" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;Seattle</td></tr>
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

<sub>📘 <a href="seattle-911/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="seattle-911/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="seattle-911/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://data.seattle.gov/">data.seattle.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>USGS Earthquakes</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;seismic events</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="usgs-earthquakes/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="usgs-earthquakes/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="usgs-earthquakes/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://earthquake.usgs.gov/">earthquake.usgs.gov</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>☢️ Radiation Monitoring</b> &nbsp;<sub>3 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>BfS ODL</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~1,700 stations, hourly gamma dose rate</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="bfs-odl/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="bfs-odl/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="bfs-odl/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://odlinfo.bfs.de/">odlinfo.bfs.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;<b>EURDEP Radiation</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~5,500 stations, 39 countries, gamma dose</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;Europe</td></tr>
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

<sub>📘 <a href="eurdep-radiation/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="eurdep-radiation/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="eurdep-radiation/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://remon.jrc.ec.europa.eu/">remon.jrc.ec.europa.eu</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>USGS Geomagnetism</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;14 observatories, 1-min geomagnetic field</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United States" title="United States" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;United States</td></tr>
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

<sub>📘 <a href="usgs-geomag/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="usgs-geomag/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="usgs-geomag/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.usgs.gov/programs/geomagnetism">usgs.gov</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>⚓ Maritime and Vessel Tracking</b> &nbsp;<sub>3 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Global â€” AIS via WebSocket" title="Global â€” AIS via WebSocket" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>AISStream</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;Global â€” AIS via WebSocket, ~200 km from shore</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global â€” AIS via WebSocket" title="Global â€” AIS via WebSocket" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global â€” AIS via WebSocket</td></tr>
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

<sub>📘 <a href="aisstream/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="aisstream/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="aisstream/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://aisstream.io/">aisstream.io</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Finland / Baltic Sea" title="Finland / Baltic Sea" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;<b>Digitraffic Maritime</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;AIS via MQTT</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Finland / Baltic Sea" title="Finland / Baltic Sea" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;Finland / Baltic Sea</td></tr>
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

<sub>📘 <a href="digitraffic-maritime/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="digitraffic-maritime/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="digitraffic-maritime/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.digitraffic.fi/en/marine-traffic/">digitraffic.fi</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Norway / Svalbard â€” raw TCP AIS" title="Norway / Svalbard â€” raw TCP AIS" src="https://flagcdn.com/20x15/no.png" width="20" height="15"> &nbsp;<b>Kystverket AIS</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;Norway / Svalbard â€” raw TCP AIS, ~34 msg/s</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Norway / Svalbard â€” raw TCP AIS" title="Norway / Svalbard â€” raw TCP AIS" src="https://flagcdn.com/20x15/no.png" width="20" height="15"> &nbsp;Norway / Svalbard â€” raw TCP AIS</td></tr>
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

<sub>📘 <a href="kystverket-ais/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="kystverket-ais/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="kystverket-ais/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.kystverket.no/">kystverket.no</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>✈️ Aviation</b> &nbsp;<sub>2 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Local â€” ADS-B via dump1090 receivers" title="Local â€” ADS-B via dump1090 receivers" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>Mode-S</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;Local â€” ADS-B via dump1090 receivers</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Local â€” ADS-B via dump1090 receivers" title="Local â€” ADS-B via dump1090 receivers" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Local â€” ADS-B via dump1090 receivers</td></tr>
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

<sub>📘 <a href="mode-s/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="mode-s/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="mode-s/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://opensky-network.org/">opensky-network.org</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>VATSIM</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;virtual aviation network, pilots & controllers</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="vatsim/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="vatsim/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="vatsim/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.vatsim.net/">vatsim.net</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>🚦 Road and Public Transport</b> &nbsp;<sub>14 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;<b>Autobahn</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;roadworks, warnings, closures, webcams</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Germany" title="Germany" src="https://flagcdn.com/20x15/de.png" width="20" height="15"> &nbsp;Germany</td></tr>
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

<sub>📘 <a href="autobahn/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="autobahn/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="autobahn/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://autobahn.de/">autobahn.de</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Finland" title="Finland" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;<b>Digitraffic Road</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;TMS sensors, road weather, traffic messages</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Finland" title="Finland" src="https://flagcdn.com/20x15/fi.png" width="20" height="15"> &nbsp;Finland</td></tr>
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

<sub>📘 <a href="digitraffic-road/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="digitraffic-road/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="digitraffic-road/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.digitraffic.fi/en/road-traffic/">digitraffic.fi</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="France" title="France" src="https://flagcdn.com/20x15/fr.png" width="20" height="15"> &nbsp;<b>French Road Traffic</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;national road network, DATEX II</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="France" title="France" src="https://flagcdn.com/20x15/fr.png" width="20" height="15"> &nbsp;France</td></tr>
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

<sub>📘 <a href="french-road-traffic/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="french-road-traffic/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="french-road-traffic/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.bison-fute.gouv.fr/">bison-fute.gouv.fr</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>GTFS Realtime</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;1,000+ transit agencies, vehicles, trips, alerts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="gtfs/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="gtfs/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="gtfs/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://gtfs.org/">gtfs.org</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Madrid" title="Madrid" src="https://flagcdn.com/20x15/es.png" width="20" height="15"> &nbsp;<b>Madrid Traffic</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~4,000 sensors, Informo</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Madrid" title="Madrid" src="https://flagcdn.com/20x15/es.png" width="20" height="15"> &nbsp;Madrid</td></tr>
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

<sub>📘 <a href="madrid-traffic/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="madrid-traffic/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="madrid-traffic/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://datos.madrid.es/">datos.madrid.es</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;<b>NDW Netherlands Traffic</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;national road traffic, DATEX II</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;Netherlands</td></tr>
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

<sub>📘 <a href="ndl-netherlands/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="ndl-netherlands/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="ndl-netherlands/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.ndw.nu/">ndw.nu</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;<b>NDW Road Traffic</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;national road traffic, DATEX II XML</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Netherlands" title="Netherlands" src="https://flagcdn.com/20x15/nl.png" width="20" height="15"> &nbsp;Netherlands</td></tr>
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

<sub>📘 <a href="ndw-road-traffic/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="ndw-road-traffic/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="ndw-road-traffic/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.ndw.nu/">ndw.nu</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="North America" title="North America" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>Nextbus</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;public transit arrivals</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="North America" title="North America" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;North America</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{agency_id}/{route_tag}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">4 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

public transit arrivals

<sub><b>📍 keyed by</b> <code>{agency_id}/{route_tag}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>VehiclePosition</code>, <code>RouteConfig</code>, <code>Schedule</code>, <code>Message</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#nextbus/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nextbus)

<sub>📘 <a href="nextbus/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="nextbus/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="nextbus/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.umoiq.com/">umoiq.com</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Paris" title="Paris" src="https://flagcdn.com/20x15/fr.png" width="20" height="15"> &nbsp;<b>Paris Bicycle Counters</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~141 counting stations, hourly counts</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Paris" title="Paris" src="https://flagcdn.com/20x15/fr.png" width="20" height="15"> &nbsp;Paris</td></tr>
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

<sub>📘 <a href="paris-bicycle-counters/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="paris-bicycle-counters/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="paris-bicycle-counters/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://opendata.paris.fr/">opendata.paris.fr</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Seattle" title="Seattle" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>Seattle Street Closures</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;permit-driven street closure windows</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Seattle" title="Seattle" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;Seattle</td></tr>
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

<sub>📘 <a href="seattle-street-closures/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="seattle-street-closures/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="seattle-street-closures/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://data.seattle.gov/">data.seattle.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="London" title="London" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;<b>TfL Road Traffic</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;road corridor status and disruptions</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="London" title="London" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;London</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>roads/{road_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">2 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

road corridor status and disruptions

<sub><b>📍 keyed by</b> <code>roads/{road_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>RoadCorridor</code>, <code>RoadStatus</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftfl-road-traffic%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#tfl-road-traffic/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-tfl-road-traffic)

<sub>📘 <a href="tfl-road-traffic/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="tfl-road-traffic/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="tfl-road-traffic/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://tfl.gov.uk/">tfl.gov.uk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Tokyo" title="Tokyo" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;<b>Tokyo Docomo Bikeshare</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;1,794 stations, GBFS 2.3 via ODPT</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Tokyo" title="Tokyo" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;Tokyo</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{system_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

1,794 stations, GBFS 2.3 via ODPT

<sub><b>📍 keyed by</b> <code>{system_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>BikeshareSystem</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#tokyo-docomo-bikeshare/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-tokyo-docomo-bikeshare)

<sub>📘 <a href="tokyo-docomo-bikeshare/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="tokyo-docomo-bikeshare/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="tokyo-docomo-bikeshare/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://docomo-cycle.jp/tokyo/">docomo-cycle.jp</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="US borders" title="US borders" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>US CBP Border Wait</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~81 ports of entry</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="US borders" title="US borders" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;US borders</td></tr>
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

<sub>📘 <a href="cbp-border-wait/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="cbp-border-wait/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="cbp-border-wait/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://bwt.cbp.gov/">bwt.cbp.gov</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Washington State" title="Washington State" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;<b>WSDOT</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~1,000 traffic flow sensors (requires free key)</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Washington State" title="Washington State" src="https://flagcdn.com/20x15/us.png" width="20" height="15"> &nbsp;Washington State</td></tr>
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

<sub>📘 <a href="wsdot/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="wsdot/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="wsdot/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://wsdot.wa.gov/">wsdot.wa.gov</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>🚆 Railway</b> &nbsp;<sub>2 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Norway" title="Norway" src="https://flagcdn.com/20x15/no.png" width="20" height="15"> &nbsp;<b>Entur Norway</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;national real-time transit, SIRI ET/VM/SX</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Norway" title="Norway" src="https://flagcdn.com/20x15/no.png" width="20" height="15"> &nbsp;Norway</td></tr>
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

<sub>📘 <a href="entur-norway/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="entur-norway/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="entur-norway/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://entur.no/">entur.no</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Belgium" title="Belgium" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;<b>iRail</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;~600 NMBS/SNCB stations, departures, delays</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Belgium" title="Belgium" src="https://flagcdn.com/20x15/be.png" width="20" height="15"> &nbsp;Belgium</td></tr>
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

<sub>📘 <a href="irail/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="irail/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="irail/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://irail.be/">irail.be</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>🎵 Nightlife and Live Entertainment</b> &nbsp;<sub>1 source</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;<b>Xceed</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;clubs, bars, parties, festivals — event schedules</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;Europe</td></tr>
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

<sub>📘 <a href="xceed/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="xceed/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="xceed/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://xceed.me/">xceed.me</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>⚡ Energy and Infrastructure</b> &nbsp;<sub>6 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="United Kingdom" title="United Kingdom" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;<b>Carbon Intensity UK</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;national grid carbon intensity</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="United Kingdom" title="United Kingdom" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;United Kingdom</td></tr>
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

<sub>📘 <a href="carbon-intensity/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="carbon-intensity/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="carbon-intensity/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://carbonintensity.org.uk/">carbonintensity.org.uk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Great Britain" title="Great Britain" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;<b>Elexon BMRS</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;electricity market, generation, demand</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Great Britain" title="Great Britain" src="https://flagcdn.com/20x15/gb.png" width="20" height="15"> &nbsp;Great Britain</td></tr>
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

<sub>📘 <a href="elexon-bmrs/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="elexon-bmrs/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="elexon-bmrs/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.elexon.co.uk/">elexon.co.uk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Denmark" title="Denmark" src="https://flagcdn.com/20x15/dk.png" width="20" height="15"> &nbsp;<b>Energi Data Service</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;power system, spot prices, CO₂</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Denmark" title="Denmark" src="https://flagcdn.com/20x15/dk.png" width="20" height="15"> &nbsp;Denmark</td></tr>
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

<sub>📘 <a href="energidataservice-dk/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="energidataservice-dk/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="energidataservice-dk/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.energidataservice.dk/">energidataservice.dk</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;<b>Energy-Charts</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;40+ countries, electricity generation & prices</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;Europe</td></tr>
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

<sub>📘 <a href="energy-charts/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="energy-charts/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="energy-charts/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.energy-charts.info/">energy-charts.info</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;<b>ENTSO-E</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;electricity generation, prices, load, flows (requires token)</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;Europe</td></tr>
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

<sub>📘 <a href="entsoe/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="entsoe/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="entsoe/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://transparency.entsoe.eu/">transparency.entsoe.eu</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Japan / Kanto" title="Japan / Kanto" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;<b>TEPCO Denkiyoho</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;TEPCO electricity supply, hourly forecast, 5-min actuals + solar</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Japan / Kanto" title="Japan / Kanto" src="https://flagcdn.com/20x15/jp.png" width="20" height="15"> &nbsp;Japan / Kanto</td></tr>
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

<sub>📘 <a href="tepco-denkiyoho/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="tepco-denkiyoho/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="tepco-denkiyoho/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.tepco.co.jp/forecast/">tepco.co.jp</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>💬 Social Media and News</b> &nbsp;<sub>4 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>Bluesky Firehose</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;posts, likes, reposts, follows</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="bluesky/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="bluesky/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="bluesky/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://bsky.app/">bsky.app</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>OpenStreetMap Diffs</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;OSM minutely replication diffs</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="wikimedia-osm-diffs/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="wikimedia-osm-diffs/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="wikimedia-osm-diffs/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.openstreetmap.org/">openstreetmap.org</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Any" title="Any" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>RSS Feeds</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;configurable RSS/Atom feed URLs or OPML files</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Any" title="Any" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Any</td></tr>
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

<sub>📘 <a href="rss/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="rss/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="rss/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.rssboard.org/rss-specification">rssboard.org</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>Wikimedia EventStreams</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;Wikipedia, Wikidata, Commons recent changes</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="wikimedia-eventstreams/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="wikimedia-eventstreams/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="wikimedia-eventstreams/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams">wikitech.wikimedia.org</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>📅 Public Events</b> &nbsp;<sub>3 sources</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;<b>Billetto</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;pan-European ticketed public events</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;Europe</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

pan-European ticketed public events

<sub><b>📍 keyed by</b> <code>{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Event</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbilletto%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#billetto/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-billetto)

<sub>📘 <a href="billetto/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="billetto/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="billetto/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://billetto.com/">billetto.com</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;<b>Fienta</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;ticketed public events with sale-status signals</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Europe" title="Europe" src="https://flagcdn.com/20x15/eu.png" width="20" height="15"> &nbsp;Europe</td></tr>
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

<sub>📘 <a href="fienta/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="fienta/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="fienta/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://fienta.com/">fienta.com</a></sub>

</details>

</td></tr>
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>Ticketmaster</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-1-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;concerts, sports, theater, arts via Discovery API</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
<tr><td valign="middle">🔌</td><td valign="middle"><b>Transports</b></td><td valign="middle">Kafka · MQTT · AMQP</td></tr>
<tr><td valign="middle">📍</td><td valign="middle"><b>Kafka key</b></td><td valign="middle"><code>{event_id}</code></td></tr>
<tr><td valign="middle">📦</td><td valign="middle"><b>Events</b></td><td valign="middle">1 type(s)</td></tr>
<tr><td valign="middle">✅</td><td valign="middle"><b>Build</b></td><td valign="middle"><a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml">passing</a></td></tr>
</table>

concerts, sports, theater, arts via Discovery API

<sub><b>📍 keyed by</b> <code>{event_id}</code> &nbsp; · &nbsp; <b>📦 events</b> <code>Event</code></sub>

<sub><b>DEPLOY</b></sub><br>
[![](https://img.shields.io/badge/Azure-Container%20%2B%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventhub.json) [![](https://img.shields.io/badge/Azure-BYO%20EH-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template.json) [![](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-servicebus.json) [![](https://img.shields.io/badge/Azure-BYO%20Service%20Bus-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-amqp.json) [![](https://img.shields.io/badge/Azure-Event%20Grid%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventgrid-mqtt.json) [![](https://img.shields.io/badge/Azure-BYO%20MQTT-0078d4?style=flat-square)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-mqtt.json) [![](https://img.shields.io/badge/Fabric-Container%20%2B%20Event%20Stream-117865?style=flat-square)](https://clemensv.github.io/real-time-sources/#ticketmaster/fabric-aci) [![](https://img.shields.io/badge/Docker-pull-2496ed?style=flat-square&logo=docker&logoColor=white)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ticketmaster)

<sub>📘 <a href="ticketmaster/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="ticketmaster/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="ticketmaster/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://www.ticketmaster.com/">ticketmaster.com</a></sub>

</details>

</td></tr>
</table>

</details>

<details open><summary><b>🔬 Scientific Research</b> &nbsp;<sub>1 source</sub></summary>

<table width="100%">
<tr><td>

<details><summary><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;<b>GraceDB</b> &nbsp; <img align="middle" alt="K" src="https://img.shields.io/badge/-K-231f20?style=flat-square"><img align="middle" alt="M" src="https://img.shields.io/badge/-M-660066?style=flat-square"><img align="middle" alt="A" src="https://img.shields.io/badge/-A-1a4a78?style=flat-square"> &nbsp; <img align="middle" src="https://img.shields.io/badge/Az-6-0078d4?style=flat-square"><img align="middle" src="https://img.shields.io/badge/Fab-2-117865?style=flat-square"><img align="middle" src="https://img.shields.io/badge/D-3-2496ed?style=flat-square"><sub>&nbsp;&nbsp;LIGO/Virgo/KAGRA gravitational wave candidates</sub></summary>

<table align="right">
<tr><td valign="middle">🌍</td><td valign="middle"><b>Region</b></td><td valign="middle"><img align="middle" alt="Global" title="Global" src="https://flagcdn.com/20x15/un.png" width="20" height="15"> &nbsp;Global</td></tr>
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

<sub>📘 <a href="gracedb/README.md">README</a> &nbsp;·&nbsp; 📑 <a href="gracedb/EVENTS.md">EVENTS</a> &nbsp;·&nbsp; 🐳 <a href="gracedb/CONTAINER.md">CONTAINER</a> &nbsp;·&nbsp; ↗ <a href="https://gracedb.ligo.org/">gracedb.ligo.org</a></sub>

</details>

</td></tr>
</table>

</details>

<!-- root-catalog:end -->


## Code Generation

Projects with checked-in `xreg` manifests regenerate their producer clients with
`xrcg generate`. Use `xrcg` `0.10.1`; the checked-in producer output and the
key-aware Kafka producer behavior now relied on by the repo are generated with
that version. Each project’s `generate_producer.ps1` script uses the checked-in
manifest as the source of truth, validates the `xrcg` version up front, and
refreshes the generated client package from that definition.
