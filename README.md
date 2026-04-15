[![Build Containers](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml)

# Real Time Sources for Apache Kafka, Azure Event Hubs, and Fabric Event Streams

Learning how to build event streaming solutions with Microsoft Azure Event Hubs,
Microsoft Fabric Event Streams, and any Apache Kafka compatible server and
service is more interesting when you have real time data sources to work with.

This repo contains command line tools, written in Python, that can be used to
retrieve real-time streaming data and related reference data from various APIs,
and then routing the data to Apache Kafka compatible endpoints.

For each tool, there is a corresponding, pre-built (Docker-) container image
that you can pull and use instantly from this repo's container registry. There
are also pre-built templates for easily deploying the containers as an Azure
Container Instance (ACI), either feeding data into an Azure Event Hub or an
Fabric Event Stream custom endpoint. The container images will work with any
Apache Kafka compatible server or service, as long as you provide required
information. The supported authentication scheme for the Kafka endpoint is
`SASL/PLAIN`.

The sources are organized by domain below. Each entry links to the container
documentation, and the README in each project directory has full details. There
are 87 containers in total.

### Hydrology and Water Monitoring

| Source | Coverage | README | Container | Build |
|---|---|---|---|---|
| BAFU Hydro | Switzerland (~300 stations, FOEN) | [📖](bafu-hydro/README.md) | [🐳](bafu-hydro/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bafu-hydro) |
| CDEC Reservoirs | California (~2,600 stations, DWR) | [📖](cdec-reservoirs/README.md) | [🐳](cdec-reservoirs/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-cdec-reservoirs) |
| CHMI Hydro | Czech Republic (CHMU) | [📖](chmi-hydro/README.md) | [🐳](chmi-hydro/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-chmi-hydro) |
| German Waters | Germany (12 state portals, ~2,724 stations) | [📖](german-waters/README.md) | [🐳](german-waters/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-german-waters) |
| Hub’Eau Hydrometrie | France (~6,300 stations) | [📖](hubeau-hydrometrie/README.md) | [🐳](hubeau-hydrometrie/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-hubeau-hydrometrie) |
| IMGW Hydro | Poland (IMGW-PIB) | [📖](imgw-hydro/README.md) | [🐳](imgw-hydro/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-imgw-hydro) |
| Ireland OPW Water Level | Ireland (~500 OPW hydrometric stations) | [📖](ireland-opw-waterlevel/README.md) | [🐳](ireland-opw-waterlevel/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ireland-opw-waterlevel) |
| Nepal BIPAD Hydrology | Nepal (Himalayan river basins, BIPAD) | [📖](nepal-bipad-hydrology/README.md) | [🐳](nepal-bipad-hydrology/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nepal-bipad-hydrology) |
| NOAA Tides and Currents | United States (~3,000 stations) | [📖](noaa/README.md) | [🐳](noaa/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa) [![Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-noaa.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-noaa.yml) |
| NOAA NDBC | United States (buoy observations) | [📖](noaa-ndbc/README.md) | [🐳](noaa-ndbc/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa-ndbc) |
| King County Marine | Washington State / Puget Sound (current raw buoy and mooring telemetry) | [📖](king-county-marine/README.md) | [🐳](king-county-marine/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-king-county-marine) |
| NVE Hydro | Norway (NVE) | [📖](nve-hydro/README.md) | [🐳](nve-hydro/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nve-hydro) |
| Pegelonline | Germany (federal waterways, ~3,000 stations) | [📖](pegelonline/README.md) | [🐳](pegelonline/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-pegelonline) [![Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-pegelonline.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-pegelonline.yml) |
| RWS Waterwebservices | Netherlands (~785 stations) | [📖](rws-waterwebservices/README.md) | [🐳](rws-waterwebservices/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-rws-waterwebservices) |
| SMHI Hydro | Sweden (SMHI) | [📖](smhi-hydro/README.md) | [🐳](smhi-hydro/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-smhi-hydro) |
| SNOTEL Snow | Western US & Alaska (~900 snowpack stations, NRCS) | [📖](snotel/README.md) | [🐳](snotel/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-snotel) |
| SYKE Hydro | Finland (SYKE) | [📖](syke-hydro/README.md) | [🐳](syke-hydro/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-syke-hydro) |
| UK EA Flood Monitoring | England (~4,000 stations) | [📖](uk-ea-flood-monitoring/README.md) | [🐳](uk-ea-flood-monitoring/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-uk-ea-flood-monitoring) |
| USGS Instantaneous Values | United States (~1.5M stations) | [📖](usgs-iv/README.md) | [🐳](usgs-iv/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-iv) [![Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-usgs-iv.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-usgs-iv.yml) |
| USGS NWIS Water Quality | United States (~3,000 sites, continuous WQ sensors) | [📖](usgs-nwis-wq/README.md) | [🐳](usgs-nwis-wq/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-nwis-wq) |
| Waterinfo VMM | Belgium / Flanders (~1,785 stations) | [📖](waterinfo-vmm/README.md) | [🐳](waterinfo-vmm/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-waterinfo-vmm) |

### Weather and Meteorology

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| AviationWeather.gov | Global (METAR, SIGMET advisories) | [📖](aviationweather/README.md) | [🐳](aviationweather/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-aviationweather) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-eventhub.json) |
| Blitzortung | Global (community lightning strokes, seconds latency) | [📖](blitzortung/README.md) | [🐳](blitzortung/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-blitzortung) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-eventhub.json) |
| BOM Australia | Australia (~8 capital city airports, half-hourly obs) | [📖](bom-australia/README.md) | [🐳](bom-australia/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bom-australia) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbom-australia%2Fazure-template-with-eventhub.json) |
| DWD | Germany (~1,450 stations, observations and CAP alerts) | [📖](dwd/README.md) | [🐳](dwd/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-dwd) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-eventhub.json) |
| DWD Pollenflug | Germany (daily pollen forecasts, 27 regions) | [📖](dwd-pollenflug/README.md) | [🐳](dwd-pollenflug/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-dwd-pollenflug) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd-pollenflug%2Fazure-template-with-eventhub.json) |
| Environment Canada | Canada (~963 SWOB stations, hourly obs) | [📖](environment-canada/README.md) | [🐳](environment-canada/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-environment-canada) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenvironment-canada%2Fazure-template-with-eventhub.json) |
| GeoSphere Austria | Austria (~280 TAWES stations, 10-min obs) | [📖](geosphere-austria/README.md) | [🐳](geosphere-austria/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-geosphere-austria) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgeosphere-austria%2Fazure-template-with-eventhub.json) |
| HKO Hong Kong | Hong Kong (27 temp stations, 18 rainfall districts) | [📖](hko-hong-kong/README.md) | [🐳](hko-hong-kong/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-hko-hong-kong) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fhko-hong-kong%2Fazure-template-with-eventhub.json) |
| JMA Japan | Japan (weather bulletins, warnings, forecasts) | [📖](jma-japan/README.md) | [🐳](jma-japan/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-jma-japan) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-japan%2Fazure-template-with-eventhub.json) |
| Meteoalarm | Europe (37 countries, severe weather warnings) | [📖](meteoalarm/README.md) | [🐳](meteoalarm/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-meteoalarm) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-with-eventhub.json) |
| NOAA NWS | United States (weather alerts, CAP) | [📖](noaa-nws/README.md) | [🐳](noaa-nws/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa-nws) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-eventhub.json) |
| NWS Forecast Zones | United States (configurable land and marine forecast zones; Puget Sound defaults) | [📖](nws-forecasts/README.md) | [🐳](nws-forecasts/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nws-forecasts) |  |
| NWS CAP Alerts | United States (active alerts via api.weather.gov) | [📖](nws-alerts/README.md) | [🐳](nws-alerts/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nws-alerts) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-with-eventhub.json) |
| NOAA GOES / SWPC | Global (space weather, solar wind, K-index) | [📖](noaa-goes/README.md) | [🐳](noaa-goes/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-noaa-goes) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-goes%2Fazure-template-with-eventhub.json) |
| Singapore NEA | Singapore (62 weather stations + 5 air-quality regions) | [📖](singapore-nea/README.md) | [🐳](singapore-nea/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-singapore-nea) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsingapore-nea%2Fazure-template-with-eventhub.json) |
| SMHI Weather | Sweden (~232 stations, hourly obs) | [📖](smhi-weather/README.md) | [🐳](smhi-weather/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-smhi-weather) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-weather%2Fazure-template-with-eventhub.json) |

### Air Quality and Environmental Health

| Source | Coverage | README | Container | Build |
|---|---|---|---|---|
| Canada AQHI | Canada (community AQHI observations and forecasts) | [📖](canada-aqhi/README.md) | [🐳](canada-aqhi/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-canada-aqhi) |
| Defra AURN | United Kingdom (300+ monitoring locations, hourly pollutants) | [📖](defra-aurn/README.md) | [🐳](defra-aurn/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-defra-aurn) |
| FMI Finland | Finland (hourly air quality observations via FMI WFS) | [📖](fmi-finland/README.md) | [🐳](fmi-finland/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-fmi-finland) |
| GIOŚ Poland | Poland (~250 stations, hourly pollutants + AQI) | [📖](gios-poland/README.md) | [🐳](gios-poland/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gios-poland) |
| Hong Kong EPD AQHI | Hong Kong (18 AQHI stations, hourly health index readings) | [📖](hongkong-epd/README.md) | [🐳](hongkong-epd/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-hongkong-epd) |
| IRCELINE Belgium | Belgium (station, timeseries, and hourly observations) | [📖](irceline-belgium/README.md) | [🐳](irceline-belgium/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-irceline-belgium) |
| LAQN London | London, UK (site metadata, species, hourly measurements, Daily AQI) | [📖](laqn-london/README.md) | [🐳](laqn-london/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-laqn-london) |
| Luchtmeetnet Netherlands | Netherlands (station measurements, components, and LKI index) | [📖](luchtmeetnet-nl/README.md) | [🐳](luchtmeetnet-nl/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-luchtmeetnet-nl) |
| EPA UV Index | United States (city-scoped hourly and daily UV forecasts) | [📖](epa-uv/README.md) | [🐳](epa-uv/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-epa-uv) |
| Sensor.Community | Global (citizen air sensors, PM and climate readings) | [📖](sensor-community/README.md) | [🐳](sensor-community/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-sensor-community) |
| Singapore NEA Air Quality | Singapore (regional PSI and PM2.5 readings) | [📖](singapore-nea/README.md) | [🐳](singapore-nea/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-singapore-nea) |
| UBA AirData | Germany (stations, pollutant components, hourly measures) | [📖](uba-airdata/README.md) | [🐳](uba-airdata/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-uba-airdata) |
| Wallonia ISSeP | Belgium / Wallonia (low-cost air quality sensors) | [📖](wallonia-issep/README.md) | [🐳](wallonia-issep/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wallonia-issep) |

### Disaster Alerts and Civil Protection

| Source | Coverage | README | Container | Build |
|---|---|---|---|---|
| Australian Wildfires | Australia (NSW, QLD, VIC bushfire incidents) | [📖](australia-wildfires/README.md) | [🐳](australia-wildfires/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-australia-wildfires) |
| EAWS ALBINA Avalanche | European Alps (daily avalanche bulletins, CAAMLv6) | [📖](eaws-albina/README.md) | [🐳](eaws-albina/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-eaws-albina) |
| GDACS | Global (earthquakes, floods, cyclones, volcanoes, droughts) | [📖](gdacs/README.md) | [🐳](gdacs/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gdacs) |
| INPE DETER Brazil | Brazil (Amazon & Cerrado deforestation alerts) | [📖](inpe-deter-brazil/README.md) | [🐳](inpe-deter-brazil/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-inpe-deter-brazil) |
| NIFC USA Wildfires | United States (active wildfire incidents, NIFC) | [📖](nifc-usa-wildfires/README.md) | [🐳](nifc-usa-wildfires/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nifc-usa-wildfires) |
| NINA/BBK | Germany (MOWAS, KATWARN, BIWAPP, DWD, LHP, Police) | [📖](nina-bbk/README.md) | [🐳](nina-bbk/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nina-bbk) |
| PTWC Tsunami | Pacific and Atlantic (NOAA tsunami bulletins) | [📖](ptwc-tsunami/README.md) | [🐳](ptwc-tsunami/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ptwc-tsunami) |
| Seattle Fire 911 | Seattle, Washington (real-time fire dispatch incidents) | [📖](seattle-911/README.md) | [🐳](seattle-911/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-seattle-911) |
| USGS Earthquakes | Global (seismic events) | [📖](usgs-earthquakes/README.md) | [🐳](usgs-earthquakes/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-earthquakes) |

### Radiation Monitoring

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| BfS ODL | Germany (~1,700 stations, hourly gamma dose rate) | [📖](bfs-odl/README.md) | [🐳](bfs-odl/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bfs-odl) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbfs-odl%2Fazure-template-with-eventhub.json) |
| EURDEP Radiation | Europe (~5,500 stations, 39 countries, gamma dose) | [📖](eurdep-radiation/README.md) | [🐳](eurdep-radiation/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-eurdep-radiation) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-eventhub.json) |
| USGS Geomagnetism | United States (14 observatories, 1-min geomagnetic field) | [📖](usgs-geomag/README.md) | [🐳](usgs-geomag/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-usgs-geomag) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fusgs-geomag%2Fazure-template-with-eventhub.json) |

### Maritime and Vessel Tracking

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| AISStream | Global (AIS via WebSocket, ~200 km from shore) | [📖](aisstream/README.md) | [🐳](aisstream/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-aisstream) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-eventhub.json) |
| Digitraffic Maritime | Finland / Baltic Sea (AIS via MQTT) | [📖](digitraffic-maritime/README.md) | [🐳](digitraffic-maritime/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-digitraffic-maritime) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-eventhub.json) |
| Kystverket AIS | Norway / Svalbard (raw TCP AIS, ~34 msg/s) | [📖](kystverket-ais/README.md) | [🐳](kystverket-ais/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-kystverket-ais) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fkystverket-ais%2Fazure-template-with-eventhub.json) |

### Aviation

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| Mode-S | Local (ADS-B via dump1090 receivers) | [📖](mode-s/README.md) | [🐳](mode-s/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-mode-s) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template-with-eventhub.json) |
| VATSIM | Global (virtual aviation network, pilots & controllers) | [📖](vatsim/README.md) | [🐳](vatsim/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-vatsim) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventhub.json) |

### Road Transport

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| Autobahn | Germany (roadworks, warnings, closures, webcams) | [📖](autobahn/README.md) | [🐳](autobahn/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-autobahn) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template-with-eventhub.json) |
| Digitraffic Road | Finland (TMS sensors, road weather, traffic messages) | [📖](digitraffic-road/README.md) | [🐳](digitraffic-road/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-digitraffic-road) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventhub.json) |
| French Road Traffic | France (national road network, DATEX II) | [📖](french-road-traffic/README.md) | [🐳](french-road-traffic/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-french-road-traffic) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-with-eventhub.json) |
| GTFS Realtime | Global (1,000+ transit agencies, vehicles, trips, alerts) | [📖](gtfs/README.md) | [🐳](gtfs/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gtfs) [![Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-gtfs.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-gtfs.yml) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template-with-eventhub.json) |
| Madrid Traffic | Madrid, Spain (~4,000 sensors, Informo) | [📖](madrid-traffic/README.md) | [🐳](madrid-traffic/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-madrid-traffic) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-with-eventhub.json) |
| NDW Netherlands Traffic | Netherlands (national road traffic, DATEX II) | [📖](ndl-netherlands/README.md) | [🐳](ndl-netherlands/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-ndl-netherlands) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template-with-eventhub.json) |
| TfL Road Traffic | London, UK (road corridor status and disruptions, TfL Unified API) | [📖](tfl-road-traffic/README.md) | [🐳](tfl-road-traffic/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-tfl-road-traffic) | |
| Nextbus | North America (public transit arrivals) | [📖](nextbus/README.md) | — | — |
| Paris Bicycle Counters | Paris (~141 counting stations, hourly counts) | [📖](paris-bicycle-counters/README.md) | [🐳](paris-bicycle-counters/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-paris-bicycle-counters) |
| Seattle Street Closures | Seattle, Washington (permit-driven street closure windows) | [📖](seattle-street-closures/README.md) | [🐳](seattle-street-closures/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-seattle-street-closures) |
| US CBP Border Wait | US-Canada & US-Mexico borders (~81 ports of entry) | [📖](cbp-border-wait/README.md) | [🐳](cbp-border-wait/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-cbp-border-wait) |
| WSDOT | Washington State (~1,000 traffic flow sensors, LOS readings) | [📖](wsdot/README.md) | [🐳](wsdot/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wsdot) |

### Railway

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| iRail | Belgium (~600 NMBS/SNCB stations, departures, delays) | [📖](irail/README.md) | [🐳](irail/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-irail) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Firail%2Fazure-template-with-eventhub.json) |

### Energy and Infrastructure

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| Carbon Intensity UK | United Kingdom (national grid carbon intensity) | [📖](carbon-intensity/README.md) | [🐳](carbon-intensity/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-carbon-intensity) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcarbon-intensity%2Fazure-template-with-eventhub.json) |
| Elexon BMRS | Great Britain (electricity market, generation, demand) | [📖](elexon-bmrs/README.md) | [🐳](elexon-bmrs/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-elexon-bmrs) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Felexon-bmrs%2Fazure-template-with-eventhub.json) |
| Energi Data Service | Denmark (power system, spot prices, CO₂) | [📖](energidataservice-dk/README.md) | [🐳](energidataservice-dk/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-energidataservice-dk) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-eventhub.json) |
| Energy-Charts | Europe (40+ countries, electricity generation & prices) | [📖](energy-charts/README.md) | [🐳](energy-charts/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-energy-charts) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergy-charts%2Fazure-template-with-eventhub.json) |
| ENTSO-E | Europe (electricity generation, prices, load, flows) | [📖](entsoe/README.md) | [🐳](entsoe/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-entsoe) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventhub.json) |

### Social Media and News

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| Bluesky Firehose | Global (posts, likes, reposts, follows) | [📖](bluesky/README.md) | [🐳](bluesky/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-bluesky) [![Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-bluesky.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-bluesky.yml) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fbluesky%2Fazure-template-with-eventhub.json) |
| OpenStreetMap Diffs | Global (OSM minutely replication diffs) | [📖](wikimedia-osm-diffs/README.md) | [🐳](wikimedia-osm-diffs/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wikimedia-osm-diffs) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-with-eventhub.json) |
| RSS Feeds | Any (configurable RSS/Atom feed URLs or OPML files) | [📖](rss/README.md) | [🐳](rss/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-rss) [![Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-rss.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-rss.yml) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template-with-eventhub.json) |
| Wikimedia EventStreams | Global (Wikipedia, Wikidata, Commons recent changes) | [📖](wikimedia-eventstreams/README.md) | [🐳](wikimedia-eventstreams/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-wikimedia-eventstreams) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-with-eventhub.json) |

### Scientific Research

| Source | Coverage | README | Container | Build | Deploy |
|---|---|---|---|---|---|
| GraceDB | Global (LIGO/Virgo/KAGRA gravitational wave candidates) | [📖](gracedb/README.md) | [🐳](gracedb/CONTAINER.md) | [![Build](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-gracedb) | [![Deploy](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-with-eventhub.json) |

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

**[CDEC Reservoirs](cdec-reservoirs/README.md)** -- California Data Exchange
Center (CDEC). Real-time reservoir storage, elevation, inflow, and outflow from
over 2,600 stations operated by the Department of Water Resources.

**[CHMI Hydro](chmi-hydro/README.md)** -- Czech Hydrometeorological Institute.
Real-time water level, discharge, and temperature. Polled every 10 minutes.

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
key.

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
state to detect changes.

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

### Scientific Research

**[GraceDB](gracedb/README.md)** -- LIGO/Virgo/KAGRA GraceDB gravitational wave
candidate event database. Superevent alerts including chirp mass, false alarm
rate, classification probabilities, and sky localization data.

### External

**[Forza Motorsport PC](https://github.com/clemensv/forza-telemetry-bridge)** --
Racing game telemetry bridge (separate repository). Captures UDP telemetry from
Forza Motorsport games and forwards to Event Hubs or Fabric Event Streams.
Binary release available.
