/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Real-Time Sources — Catalog App
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

const REPO = "clemensv/real-time-sources";
const BRANCH = "main";
const RAW = `https://raw.githubusercontent.com/${REPO}/${BRANCH}`;
const FEEDERS_PREFIX = "feeders";

/* ── Source catalog ────────────────────────────────────────────────────── */
const SOURCES = [
  // ── Hydrology and Water Monitoring ──
  { id: "bafu-hydro", name: "BAFU Hydro", cat: "Hydrology", key: false, desc: "Switzerland — ~300 stations, FOEN", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "canada-eccc-wateroffice", name: "Canada ECCC Water Office", cat: "Hydrology", key: false, desc: "Canada — ~2,100 hydrometric stations, ECCC/WSC", mqtt: true, amqp: true },
  { id: "cdec-reservoirs", name: "CDEC Reservoirs", cat: "Hydrology", key: false, desc: "California — ~2,600 stations, DWR", notebook: true, mqtt: true, amqp: true },
  { id: "chmi-hydro", name: "CHMI Hydro", cat: "Hydrology", key: false, desc: "Czech Republic — CHMU", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "german-waters", name: "German Waters", cat: "Hydrology", key: false, desc: "Germany — 12 state portals, ~2,724 stations", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "hubeau-hydrometrie", name: "Hub'Eau Hydrometrie", cat: "Hydrology", key: false, desc: "France — ~6,300 stations", notebook: true, mqtt: true, amqp: true },
  { id: "imgw-hydro", name: "IMGW Hydro", cat: "Hydrology", key: false, desc: "Poland — IMGW-PIB", notebook: true, mqtt: true, amqp: true },
  { id: "ireland-opw-waterlevel", name: "Ireland OPW Water Level", cat: "Hydrology", key: false, desc: "Ireland — ~500 OPW hydrometric stations", notebook: true, mqtt: true, amqp: true },
  { id: "king-county-marine", name: "King County Marine", cat: "Hydrology", key: false, desc: "Washington State / Puget Sound — buoy and mooring telemetry", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "nepal-bipad-hydrology", name: "Nepal BIPAD Hydrology", cat: "Hydrology", key: false, desc: "Nepal — Himalayan river basins, BIPAD", notebook: true, mqtt: true, amqp: true },
  { id: "noaa-ndbc", name: "NOAA NDBC", cat: "Hydrology", key: false, desc: "United States — buoy observations", notebook: true, mqtt: true, amqp: true },
  { id: "noaa", name: "NOAA Tides & Currents", cat: "Hydrology", key: false, desc: "United States — ~3,000 stations", notebook: true, mqtt: true, amqp: true },
  { id: "nve-hydro", name: "NVE Hydro", cat: "Hydrology", key: true, desc: "Norway — NVE (requires free API key)", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "pegelonline", name: "Pegelonline", cat: "Hydrology", key: false, desc: "Germany — federal waterways, ~3,000 stations", notebook: true, mqtt: true, amqp: true },
  { id: "rws-waterwebservices", name: "RWS Waterwebservices", cat: "Hydrology", key: false, desc: "Netherlands — ~785 stations", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "smhi-hydro", name: "SMHI Hydro", cat: "Hydrology", key: false, desc: "Sweden — SMHI", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "snotel", name: "SNOTEL Snow", cat: "Hydrology", key: false, desc: "Western US & Alaska — ~900 snowpack stations, NRCS", notebook: true, mqtt: true, amqp: true },
  { id: "syke-hydro", name: "SYKE Hydro", cat: "Hydrology", key: false, desc: "Finland — SYKE", notebook: true, mqtt: true, amqp: true },
  { id: "uk-ea-flood-monitoring", name: "UK EA Flood Monitoring", cat: "Hydrology", key: false, desc: "England — ~4,000 stations", notebook: true, mqtt: true, amqp: true },
  { id: "usgs-iv", name: "USGS Instantaneous Values", cat: "Hydrology", key: false, desc: "United States — ~1.5M stations", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "usgs-nwis-wq", name: "USGS NWIS Water Quality", cat: "Hydrology", key: false, desc: "United States — ~3,000 continuous WQ sites", notebook: true, mqtt: true, amqp: true },
  { id: "waterinfo-vmm", name: "Waterinfo VMM", cat: "Hydrology", key: false, desc: "Belgium / Flanders — ~1,785 stations", notebook: true, mqtt: true, amqp: true },

  // ── Weather and Meteorology ──
  { id: "aviationweather", name: "AviationWeather.gov", cat: "Weather", key: false, desc: "Global — METAR, SIGMET advisories", notebook: true, mqtt: true, amqp: true },
  { id: "blitzortung", name: "Blitzortung", cat: "Weather", key: false, desc: "Global — community lightning strokes, seconds latency", mqtt: true, amqp: true },
  { id: "bom-australia", name: "BOM Australia", cat: "Weather", key: false, desc: "Australia — ~8 capital city airports, half-hourly obs", notebook: true, mqtt: true, amqp: true },
  { id: "dwd", name: "DWD", cat: "Weather", key: false, desc: "Germany — ~1,450 stations, observations and CAP alerts", mqtt: true, amqp: true },
  { id: "dwd-pollenflug", name: "DWD Pollenflug", cat: "Weather", key: false, desc: "Germany — daily pollen forecasts, 27 regions", notebook: true, mqtt: true, amqp: true },
  { id: "dmi", name: "DMI Denmark", cat: "Weather", key: true, desc: "Denmark — Danish Meteorological Institute observations", notebook: true, mqtt: true, amqp: true },
  { id: "environment-canada", name: "Environment Canada", cat: "Weather", key: false, desc: "Canada — ~963 SWOB stations, hourly obs", notebook: true, mqtt: true, amqp: true },
  { id: "geosphere-austria", name: "GeoSphere Austria", cat: "Weather", key: false, desc: "Austria — ~280 TAWES stations, 10-min obs", notebook: true, mqtt: true, amqp: true },
  { id: "hko-hong-kong", name: "HKO Hong Kong", cat: "Weather", key: false, desc: "Hong Kong — 27 temp stations, 18 rainfall districts", notebook: true, mqtt: true, amqp: true },
  { id: "jma-japan", name: "JMA Japan", cat: "Weather", key: false, desc: "Japan — weather bulletins, warnings, forecasts", notebook: true, mqtt: true, amqp: true },
  { id: "jma-bosai-amedas", name: "JMA Bosai AMeDAS", cat: "Weather", key: false, desc: "Japan — ~1,300 AMeDAS automated weather stations, 10-min obs", notebook: true, mqtt: true, amqp: true, kafka: false },
  { id: "kmi-belgium", name: "KMI Belgium", cat: "Weather", key: false, desc: "Belgium — ~14 AWS stations, 10-min observations", notebook: true, mqtt: true, amqp: true },
  { id: "meteoalarm", name: "Meteoalarm", cat: "Weather", key: false, desc: "Europe — 37 countries, severe weather warnings", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "noaa-goes", name: "NOAA GOES / SWPC", cat: "Weather", key: false, desc: "Global — space weather, solar wind, K-index", notebook: true, mqtt: true, amqp: true },
  { id: "noaa-swpc-l1", name: "NOAA SWPC L1", cat: "Weather", key: false, desc: "Global — L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time", notebook: true, mqtt: true, amqp: true },
  { id: "noaa-nws", name: "NOAA NWS", cat: "Weather", key: false, desc: "United States — weather alerts, CAP", notebook: true, mqtt: true, amqp: true },
  { id: "nws-alerts", name: "NWS CAP Alerts", cat: "Weather", key: false, desc: "United States — active alerts via api.weather.gov", notebook: true, mqtt: true, amqp: true },
  { id: "nws-forecasts", name: "NWS Forecast Zones", cat: "Weather", key: false, desc: "United States — configurable land and marine forecast zones", notebook: true, mqtt: true, amqp: true },
  { id: "singapore-nea", name: "Singapore NEA", cat: "Weather", key: false, desc: "Singapore — 62 weather stations + 5 air-quality regions", notebook: true, mqtt: true, amqp: true },
  { id: "smhi-weather", name: "SMHI Weather", cat: "Weather", key: false, desc: "Sweden — ~232 stations, hourly obs", notebook: true, mqtt: true, amqp: true },

  // ── Air Quality and Environmental Health ──
  { id: "canada-aqhi", name: "Canada AQHI", cat: "Air Quality", key: false, desc: "Canada — community AQHI observations and forecasts", notebook: true, mqtt: true, amqp: true },
  { id: "defra-aurn", name: "Defra AURN", cat: "Air Quality", key: false, desc: "United Kingdom — 300+ monitoring locations, hourly pollutants", notebook: true, mqtt: true, amqp: true },
  { id: "epa-uv", name: "EPA UV Index", cat: "Air Quality", key: false, desc: "United States — city-scoped hourly and daily UV forecasts", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "fmi-finland", name: "FMI Finland", cat: "Air Quality", key: false, desc: "Finland — hourly air quality observations via FMI WFS", notebook: true, mqtt: true, amqp: true },
  { id: "gios-poland", name: "GIOŚ Poland", cat: "Air Quality", key: false, desc: "Poland — ~250 stations, hourly pollutants + AQI", notebook: true, mqtt: true, amqp: true },
  { id: "hongkong-epd", name: "Hong Kong EPD AQHI", cat: "Air Quality", key: false, desc: "Hong Kong — 18 AQHI stations, hourly health index", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "irceline-belgium", name: "IRCELINE Belgium", cat: "Air Quality", key: false, desc: "Belgium — station, timeseries, and hourly observations", notebook: true, mqtt: true, amqp: true },
  { id: "laqn-london", name: "LAQN London", cat: "Air Quality", key: false, desc: "London, UK — site metadata, species, hourly measurements", notebook: true, mqtt: true, amqp: true },
  { id: "luchtmeetnet-nl", name: "Luchtmeetnet Netherlands", cat: "Air Quality", key: false, desc: "Netherlands — station measurements, components, LKI index", notebook: true, mqtt: true, amqp: true },
  { id: "sensor-community", name: "Sensor.Community", cat: "Air Quality", key: false, desc: "Global — citizen air sensors, PM and climate readings", notebook: true, mqtt: true, amqp: true },
  { id: "uba-airdata", name: "UBA AirData", cat: "Air Quality", key: false, desc: "Germany — stations, pollutant components, hourly measures", notebook: true, mqtt: true, amqp: true },
  { id: "wallonia-issep", name: "Wallonia ISSeP", cat: "Air Quality", key: false, desc: "Belgium / Wallonia — low-cost air quality sensors", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },

  // ── Disaster Alerts and Civil Protection ──
  { id: "australia-wildfires", name: "Australian Wildfires", cat: "Disasters", key: false, desc: "Australia — NSW, QLD, VIC bushfire incidents", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "eaws-albina", name: "EAWS ALBINA Avalanche", cat: "Disasters", key: false, desc: "European Alps — daily avalanche bulletins, CAAMLv6", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "gdacs", name: "GDACS", cat: "Disasters", key: false, desc: "Global — earthquakes, floods, cyclones, volcanoes, droughts", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "inpe-deter-brazil", name: "INPE DETER Brazil", cat: "Disasters", key: false, desc: "Brazil — Amazon & Cerrado deforestation alerts", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "jma-bosai-quake", name: "JMA Bosai Earthquake", cat: "Disasters", key: false, desc: "Japan — JMA earthquake / tsunami / hypocenter feeds", notebook: true, mqtt: true, amqp: true, kafka: false },
  { id: "jma-bosai-volcano", name: "JMA Bosai Volcano", cat: "Disasters", key: false, desc: "Japan — JMA volcanic activity bulletins and alerts", notebook: true, mqtt: true, amqp: true, kafka: false },
  { id: "jma-bosai-warning", name: "JMA Bosai Warning", cat: "Disasters", key: false, desc: "Japan — JMA weather warnings and advisories", notebook: true, mqtt: true, amqp: true, kafka: false },
  { id: "nasa-firms", name: "NASA FIRMS Active Fire", cat: "Disasters", key: true, desc: "Global — VIIRS/MODIS active-fire detections, OSINT", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "nifc-usa-wildfires", name: "NIFC USA Wildfires", cat: "Disasters", key: false, desc: "United States — active wildfire incidents, NIFC", notebook: true, mqtt: true, amqp: true },
  { id: "nina-bbk", name: "NINA/BBK", cat: "Disasters", key: false, desc: "Germany — MOWAS, KATWARN, BIWAPP, DWD, LHP, Police", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "ptwc-tsunami", name: "PTWC Tsunami", cat: "Disasters", key: false, desc: "Pacific and Atlantic — NOAA tsunami bulletins", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "seattle-911", name: "Seattle Fire 911", cat: "Disasters", key: false, desc: "Seattle, WA — real-time fire dispatch incidents", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "usgs-earthquakes", name: "USGS Earthquakes", cat: "Disasters", key: false, desc: "Global — seismic events", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },

  // ── Radiation Monitoring ──
  { id: "bfs-odl", name: "BfS ODL", cat: "Radiation", key: false, desc: "Germany — ~1,700 stations, hourly gamma dose rate", notebook: true, mqtt: true, amqp: true },
  { id: "eurdep-radiation", name: "EURDEP Radiation", cat: "Radiation", key: false, desc: "Europe — ~5,500 stations, 39 countries, gamma dose", notebook: true, mqtt: true, amqp: true },
  { id: "usgs-geomag", name: "USGS Geomagnetism", cat: "Radiation", key: false, desc: "United States — 14 observatories, 1-min geomagnetic field", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },

  // ── Maritime and Vessel Tracking ──
  { id: "aisstream", name: "AISStream", cat: "Maritime", key: true, desc: "Global — AIS via WebSocket, ~200 km from shore", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "digitraffic-maritime", name: "Digitraffic Maritime", cat: "Maritime", key: false, desc: "Finland / Baltic Sea — AIS via MQTT", mqtt: true, amqp: true },
  { id: "kystverket-ais", name: "Kystverket AIS", cat: "Maritime", key: false, desc: "Norway / Svalbard — raw TCP AIS, ~34 msg/s", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },

  // ── Aviation ──
  { id: "mode-s", name: "Mode-S", cat: "Aviation", key: false, desc: "Local — ADS-B via dump1090 receivers", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "vatsim", name: "VATSIM", cat: "Aviation", key: false, desc: "Global — virtual aviation network, pilots & controllers", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },

  // ── Road and Public Transport ──
  { id: "autobahn", name: "Autobahn", cat: "Transport", key: false, desc: "Germany — roadworks, warnings, closures, webcams", notebook: true, mqtt: true, amqp: true },
  { id: "digitraffic-road", name: "Digitraffic Road", cat: "Transport", key: false, desc: "Finland — TMS sensors, road weather, traffic messages", mqtt: true, amqp: true },
  { id: "french-road-traffic", name: "French Road Traffic", cat: "Transport", key: false, desc: "France — national road network, DATEX II", notebook: true, mqtt: true, amqp: true, amqpSb: false },
  { id: "gtfs", name: "GTFS Realtime", cat: "Transport", key: false, desc: "Global — 1,000+ transit agencies, vehicles, trips, alerts", notebook: true, mqtt: true, amqp: true, amqpSb: false },
  { id: "madrid-traffic", name: "Madrid Traffic", cat: "Transport", key: false, desc: "Madrid, Spain — ~4,000 sensors, Informo", notebook: true, mqtt: true, amqp: true, amqpSb: false },
  { id: "ndw-road-traffic", name: "NDW Road Traffic", cat: "Transport", key: false, desc: "Netherlands — national road traffic, DATEX II XML", notebook: true, mqtt: true, amqp: true, amqpSb: false },
  { id: "nextbus", name: "Nextbus", cat: "Transport", key: true, desc: "North America — public transit arrivals", kql: false, notebook: true, mqtt: true, amqp: true, amqpSb: false },
  { id: "paris-bicycle-counters", name: "Paris Bicycle Counters", cat: "Transport", key: false, desc: "Paris — ~141 counting stations, hourly counts", notebook: true, mqtt: true, amqp: true },
  { id: "seattle-street-closures", name: "Seattle Street Closures", cat: "Transport", key: false, desc: "Seattle, WA — permit-driven street closure windows", notebook: true, mqtt: true, amqp: true, amqpSb: false },
  { id: "tfl-road-traffic", name: "TfL Road Traffic", cat: "Transport", key: false, desc: "London, UK — road corridor status and disruptions", kql: false, mqtt: true, amqp: true, kafka: false },
  { id: "tokyo-docomo-bikeshare", name: "Tokyo Docomo Bikeshare", cat: "Transport", key: false, desc: "Tokyo, Japan — 1,794 stations, GBFS 2.3 via ODPT", kql: false, mqtt: true, amqp: true, kafka: false, amqpSb: false },
  { id: "cbp-border-wait", name: "US CBP Border Wait", cat: "Transport", key: false, desc: "US borders — ~81 ports of entry", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "wsdot", name: "WSDOT", cat: "Transport", key: true, desc: "Washington State — ~1,000 traffic flow sensors (requires free key)", notebook: true, mqtt: true, amqp: true, amqpSb: false },

  // ── Railway ──
  { id: "entur-norway", name: "Entur Norway", cat: "Railway", key: false, desc: "Norway — national real-time transit, SIRI ET/VM/SX", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },
  { id: "irail", name: "iRail", cat: "Railway", key: false, desc: "Belgium — ~600 NMBS/SNCB stations, departures, delays", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false },

  // ── Nightlife and Live Entertainment ──
  { id: "xceed", name: "Xceed", cat: "Nightlife", key: false, desc: "Europe — clubs, bars, parties, festivals — event schedules", mqtt: true, amqp: true },

  // ── Energy and Infrastructure ──
  { id: "carbon-intensity", name: "Carbon Intensity UK", cat: "Energy", key: false, desc: "United Kingdom — national grid carbon intensity", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "elexon-bmrs", name: "Elexon BMRS", cat: "Energy", key: false, desc: "Great Britain — electricity market, generation, demand", notebook: true, mqtt: true, amqp: true },
  { id: "energidataservice-dk", name: "Energi Data Service", cat: "Energy", key: false, desc: "Denmark — power system, spot prices, CO₂", notebook: true, mqtt: true, amqp: true },
  { id: "energy-charts", name: "Energy-Charts", cat: "Energy", key: false, desc: "Europe — 40+ countries, electricity generation & prices", notebook: true, mqtt: true, amqp: true },
  { id: "entsoe", name: "ENTSO-E", cat: "Energy", key: true, desc: "Europe — electricity generation, prices, load, flows (requires token)", mqtt: true, amqp: true },
  { id: "tepco-denkiyoho", name: "TEPCO Denkiyoho", cat: "Energy", key: false, desc: "Japan / Kanto — TEPCO electricity supply, hourly forecast, 5-min actuals + solar", notebook: true, mqtt: true, amqp: true, kafka: false },

  // ── Social Media and News ──
  { id: "bluesky", name: "Bluesky Firehose", cat: "Social", key: false, desc: "Global — posts, likes, reposts, follows", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "wikimedia-osm-diffs", name: "OpenStreetMap Diffs", cat: "Social", key: false, desc: "Global — OSM minutely replication diffs", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "rss", name: "RSS Feeds", cat: "Social", key: false, desc: "Any — configurable RSS/Atom feed URLs or OPML files", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
  { id: "wikimedia-eventstreams", name: "Wikimedia EventStreams", cat: "Social", key: false, desc: "Global — Wikipedia, Wikidata, Commons recent changes", mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },

  // ── Public Events ──
  { id: "billetto", name: "Billetto", cat: "Public Events", key: false, desc: "Europe — pan-European ticketed public events", kql: false, mqtt: true, amqp: true },
  { id: "fienta", name: "Fienta", cat: "Public Events", key: false, desc: "Europe — ticketed public events with sale-status signals", mqtt: true, amqp: true },
  { id: "ticketmaster", name: "Ticketmaster", cat: "Public Events", key: true, desc: "Global — concerts, sports, theater, arts via Discovery API", kql: false, mqtt: true, amqp: true },

  // ── Scientific Research ──
  { id: "gracedb", name: "GraceDB", cat: "Science", key: false, desc: "Global — LIGO/Virgo/KAGRA gravitational wave candidates", notebook: true, mqtt: true, amqp: true, mqttBasic: false, mqttEg: false, amqpSb: false },
];

/* ── Derived data ──────────────────────────────────────────────────────── */
const CATEGORIES = [...new Set(SOURCES.map(s => s.cat))];

/* ── DOM refs ──────────────────────────────────────────────────────────── */
const $pills     = document.getElementById("category-pills");
const $list      = document.getElementById("source-list");
const $search    = document.getElementById("search-box");
const $content   = document.getElementById("content-area");
const $deployBar = document.getElementById("deploy-bar");
const $deployBarFabric = document.getElementById("deploy-bar-fabric");
const $btnContainer = document.getElementById("btn-container");
const $btnContainerEH = document.getElementById("btn-container-eh");
const $btnContainerMqtt = document.getElementById("btn-container-mqtt");
const $btnContainerMqttEG = document.getElementById("btn-container-mqtt-eg");
const $btnContainerAmqpSB = document.getElementById("btn-container-amqp-sb");
const $btnFabric = document.getElementById("btn-container-eh-adx");
const $btnFabricNotebook = document.getElementById("btn-fabric-notebook");
const $deployPane = document.getElementById("deploy-pane");
const $deployTitle = document.getElementById("deploy-pane-title");
const $deployClose = document.getElementById("deploy-pane-close");
const $deployForm = document.getElementById("deploy-form-area");

// Share button + popover (per-source social-card sharing). These elements
// live in the ghpages header; when absent (e.g. older index.html) the
// share-* lookups are null and the share logic is silently skipped.
const $shareBtn      = document.getElementById("share-btn");
const $sharePopover  = document.getElementById("share-popover");
const $shareTitle    = document.getElementById("share-title");
const $shareUrl      = document.getElementById("share-url-input");
const $shareCopy     = document.getElementById("share-copy-btn");
const $shareToast    = document.getElementById("share-toast");
const $shareIntents  = document.getElementById("share-intents");

let activeCat = null;
let activeSource = null;

/* ── Theme toggle ──────────────────────────────────────────────────────── */
(function initTheme() {
  const saved = localStorage.getItem("rts-theme");
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("rts-theme", next);
  });
})();

/* ── Category pills ────────────────────────────────────────────────────── */
function renderPills() {
  const allPill = el("span", { class: "pill active", "data-cat": "" }, "All");
  allPill.addEventListener("click", () => selectCategory(null));
  $pills.appendChild(allPill);

  for (const cat of CATEGORIES) {
    const p = el("span", { class: "pill", "data-cat": cat }, cat);
    p.addEventListener("click", () => selectCategory(cat));
    $pills.appendChild(p);
  }
}

function selectCategory(cat) {
  activeCat = cat;
  $pills.querySelectorAll(".pill").forEach(p => {
    const pCat = p.getAttribute("data-cat");
    p.classList.toggle("active", cat === null ? pCat === "" : pCat === cat);
  });
  renderList();
}

/* ── Source list ────────────────────────────────────────────────────────── */
function filteredSources() {
  const q = $search.value.trim().toLowerCase();
  return SOURCES.filter(s => {
    if (activeCat && s.cat !== activeCat) return false;
    if (q && !s.name.toLowerCase().includes(q) && !s.desc.toLowerCase().includes(q) && !s.id.includes(q)) return false;
    return true;
  }).sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: "base" }));
}

function renderList() {
  $list.innerHTML = "";
  for (const s of filteredSources()) {
    const li = el("li", {
      class: "source-item" + (activeSource === s.id ? " active" : ""),
      "data-id": s.id,
    });
    li.innerHTML = `
      <span class="name">${esc(s.name)}</span>
      <span>${s.key ? '<span class="key-badge" title="API key required">KEY</span>' : ""}</span>
      <span class="desc">${esc(s.desc)}</span>`;
    li.addEventListener("click", () => selectSource(s));
    $list.appendChild(li);
  }
}

$search.addEventListener("input", renderList);

/* ── Source selection ──────────────────────────────────────────────────── */
async function selectSource(s) {
  activeSource = s.id;
  renderList();
  $deployBar.style.display = "flex";
  $deployBarFabric.style.display = "flex";
  updateShareButton();

  // wire deploy buttons
  // Granular template-availability flags (default true). Set to false in the
  // source entry to suppress a button whose ARM template hasn't been authored.
  const hasKafka     = s.kafka     !== false;
  const hasMqttBasic = s.mqtt && s.mqttBasic !== false;
  const hasMqttEg    = s.mqtt && s.mqttEg    !== false;
  const hasAmqpSb    = s.amqp && s.amqpSb    !== false;
  if ($btnContainer) {
    $btnContainer.style.display = hasKafka ? "" : "none";
    $btnContainer.onclick = () => {
      const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template.json`;
      window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
    };
  }
  if ($btnContainerEH) {
    $btnContainerEH.style.display = hasKafka ? "" : "none";
    $btnContainerEH.onclick = () => {
      const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-with-eventhub.json`;
      window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
    };
  }
  if ($btnContainerMqtt) {
    // MQTT BYO-broker deploy is opt-in per source (requires azure-template-mqtt.json).
    $btnContainerMqtt.style.display = hasMqttBasic ? "" : "none";
    $btnContainerMqtt.onclick = () => {
      const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-mqtt.json`;
      window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
    };
  }
  if ($btnContainerMqttEG) {
    // MQTT + Event Grid namespace deploy is opt-in per source (requires azure-template-with-eventgrid-mqtt.json).
    $btnContainerMqttEG.style.display = hasMqttEg ? "" : "none";
    $btnContainerMqttEG.onclick = () => {
      const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-with-eventgrid-mqtt.json`;
      window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
    };
  }
  if ($btnContainerAmqpSB) {
    // AMQP 1.0 + Service Bus namespace deploy is opt-in per source (requires azure-template-with-servicebus.json).
    $btnContainerAmqpSB.style.display = hasAmqpSb ? "" : "none";
    $btnContainerAmqpSB.onclick = () => {
      const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-with-servicebus.json`;
      window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
    };
  }
  // Hide Fabric ACI deploy button if the source lacks a KQL schema; the
  // central deploy-fabric.ps1 aborts at step 0/6 when feeders/<id>/kql/<id>.kql
  // is missing, so the button would only lead to a failed deploy.
  const hasKql = s.kql !== false;
  $btnFabric.style.display = hasKql ? "" : "none";
  $btnFabric.onclick      = () => openDeployForm(s, "fabric-aci");
  if ($btnFabricNotebook) {
    // Notebook deploy is opt-in per source (requires <source>/notebook/<source>-feed.ipynb)
    // and also needs the KQL schema for the database it writes into.
    $btnFabricNotebook.style.display = (s.notebook && hasKql) ? "" : "none";
    $btnFabricNotebook.onclick = () => openDeployForm(s, "fabric-notebook");
  }
  // If both Fabric buttons are hidden, hide the whole Fabric deploy bar.
  if (!hasKql && (!s.notebook || !hasKql)) {
    $deployBarFabric.style.display = "none";
  }

  // fetch and render README.md
  $content.innerHTML = '<div class="loading-indicator">Loading documentation…</div>';
  try {
    const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/README.md`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    let md = await resp.text();
    md = md.replace(/\]\((?!https?:\/\/)([^)]+)\)/g, (m, p) =>
      `](https://github.com/${REPO}/blob/${BRANCH}/${FEEDERS_PREFIX}/${s.id}/${p})`
    );
    $content.innerHTML = `<div class="md-body">${marked.parse(md)}</div>`;
  } catch (e) {
    $content.innerHTML = `<div class="error-msg">Could not load documentation for <strong>${esc(s.name)}</strong>.<br><code>${esc(e.message)}</code></div>`;
  }
}

/* ── Deploy form ───────────────────────────────────────────────────────── */

const AZURE_LOGO_SVG = `<svg viewBox="0 0 256 256" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="az-btn-g1" x1="-960.606" y1="283.397" x2="-1032.511" y2="70.972" gradientTransform="matrix(1 0 0 -1 1075 318)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#114a8b"/><stop offset="1" stop-color="#0669bc"/></linearGradient>
    <linearGradient id="az-btn-g2" x1="-947.292" y1="289.594" x2="-868.363" y2="79.308" gradientTransform="matrix(1 0 0 -1 1075 318)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#3ccbf4"/><stop offset="1" stop-color="#2892df"/></linearGradient>
  </defs>
  <path d="M89.158 18.266h69.238L86.523 231.224a11.041 11.041 0 01-10.461 7.51H22.179a11.023 11.023 0 01-10.445-14.548l66.963-198.41a11.04 11.04 0 0110.461-7.51z" fill="url(#az-btn-g1)"/>
  <path d="M189.77 161.104H79.976a5.083 5.083 0 00-3.468 8.8l70.552 65.847a11.091 11.091 0 007.567 2.983h62.167z" fill="#0078d4"/>
  <path d="M177.592 25.764a11.023 11.023 0 00-10.444-7.498H89.984a11.024 11.024 0 0110.445 7.498l66.967 198.421a11.024 11.024 0 01-10.445 14.549h77.164a11.024 11.024 0 0010.444-14.549z" fill="url(#az-btn-g2)"/>
</svg>`;

async function openDeployForm(source, mode) {
  $deployTitle.textContent = `Deploy ${source.name} to Fabric`;
  $deployPane.style.display = "flex";
  $deployForm.innerHTML = "";

  // Azure section
  //   fabric-aci      → needs RG + Location + (optional) Subscription (creates ACI)
  //   fabric-notebook → only Subscription (Fabric capacity token, no Azure deploy)
  //   fabric          → only Subscription (optional)
  if (mode === "fabric-aci") {
    const azSection = el("div", { class: "form-section" });
    azSection.innerHTML = '<div class="form-section-title">Azure (for the ACI feeder container)</div>';
    azSection.appendChild(makeField("subscriptionId", "Subscription (name or ID)", "text",
      "", "Optional. Uses your current Cloud Shell subscription context unless you override it here.", false));
    azSection.appendChild(makeField("resourceGroup", "Resource Group", "text",
      "", "Azure resource group (created on demand)", true));
    azSection.appendChild(makeField("location", "Location", "text",
      "westeurope", "Azure region (defaults to RG location, else westeurope)", false));
    azSection.appendChild(makeField("containerGroupName", "Container Group Name", "text",
      source.id, "Name for the Azure Container Group", false));
    $deployForm.appendChild(azSection);
  } else if (mode === "fabric-notebook") {
    const azSection = el("div", { class: "form-section" });
    azSection.innerHTML = '<div class="form-section-title">Azure Subscription</div>';
    azSection.appendChild(makeField("subscriptionId", "Subscription (name or ID)", "text",
      "", "Optional. Enter an Azure subscription name or GUID; leave blank to use your current Cloud Shell context.", false));
    $deployForm.appendChild(azSection);
  } else if (mode === "fabric") {
    const azSection = el("div", { class: "form-section" });
    azSection.innerHTML = '<div class="form-section-title">Azure Subscription <span style="font-weight:normal;color:var(--muted);font-size:11px">(optional)</span></div>';
    azSection.appendChild(makeField("subscriptionId", "Subscription (name or ID)", "text",
      "", "Optional. Enter an Azure subscription name or GUID; leave blank to use your current Cloud Shell context.", false));
    $deployForm.appendChild(azSection);
  }

  // Fabric section
  const fabSection = el("div", { class: "form-section" });
  fabSection.innerHTML = '<div class="form-section-title">Microsoft Fabric</div>';
  fabSection.appendChild(makeField("workspaceId", "Workspace (name or GUID)", "text",
    "", "Fabric workspace name or GUID", true));
  fabSection.appendChild(makeField("eventhouseId", "Eventhouse (name or GUID)", "text",
    "", "Fabric Eventhouse name or GUID (created on demand)", false));
  fabSection.appendChild(makeField("databaseName", "KQL Database Name", "text",
    source.id.replace(/-/g, "_"), "Name for the KQL database", false));
  $deployForm.appendChild(fabSection);

  // API key section (only for sources that require one, and only the
  // fabric-aci mode actually deploys the feeder).
  if (source.key && mode === "fabric-aci") {
    const keyMap = {
      "aisstream": { param: "aisstreamApiKey", label: "AISStream API Key" },
      "entsoe":    { param: "entsoeSecurityToken", label: "ENTSO-E Security Token" },
      "nve-hydro": { param: "nveApiKey", label: "NVE API Key" },
      "wsdot":     { param: "wsdotAccessCode", label: "WSDOT Access Code" }
    };
    const meta = keyMap[source.id];
    if (meta) {
      const keySection = el("div", { class: "form-section" });
      keySection.innerHTML = `<div class="form-section-title">${esc(meta.label)} <span style="font-weight:normal;color:var(--accent);font-size:11px">required</span></div>`;
      keySection.appendChild(makeField("apiKey", meta.label, "password",
        "", "Stored as a securestring template parameter", true, true));
      // remember the param name on a hidden field
      const hidden = el("input", { type: "hidden", id: "deploy-apiKeyParamName", value: meta.param });
      keySection.appendChild(hidden);
      $deployForm.appendChild(keySection);
    }
  }

  // Submit button
  const submitBtn = el("button", { class: "deploy-submit", type: "button" });
  submitBtn.innerHTML = `${AZURE_LOGO_SVG} Copy deployment command to the clipboard and open Azure Cloud Shell`;
  submitBtn.addEventListener("click", () => launchCloudShell(source, mode));
  $deployForm.appendChild(submitBtn);

  // Note
  const note = el("div", { class: "deploy-note" });
  note.innerHTML = '<strong style="font-size:13px">Once Azure Cloud Shell has opened, paste the command to run!</strong>';
  $deployForm.appendChild(note);
}

function makeField(name, label, type, defaultVal, hint, required, secure) {
  const group = el("div", { class: "form-group" });
  const lbl = el("label");
  lbl.setAttribute("for", `deploy-${name}`);
  lbl.innerHTML = esc(label) + (required ? '<span class="required">*</span>' : '');
  group.appendChild(lbl);

  const input = el("input", {
    type: type,
    id: `deploy-${name}`,
    name: name,
    value: defaultVal || "",
    placeholder: hint || "",
  });
  if (secure) input.classList.add("secure");
  group.appendChild(input);

  if (hint) {
    const h = el("div", { class: "form-hint" });
    h.textContent = hint;
    group.appendChild(h);
  }
  return group;
}

function launchCloudShell(source, mode) {
  const getValue = (name) => {
    const el = document.getElementById(`deploy-${name}`);
    return el ? el.value.trim() : "";
  };

  const subId = getValue("subscriptionId");

  if (mode === "fabric-aci" || mode === "fabric" || mode === "fabric-notebook") {
    const wsId = getValue("workspaceId");
    if (!wsId) {
      alert("Workspace (name or GUID) is required for Fabric deployment.");
      return;
    }
    const ehId = getValue("eventhouseId");
    const dbName = getValue("databaseName") || source.id.replace(/-/g, "_");

    let scriptName;
    if (mode === "fabric-aci")           scriptName = "deploy-fabric-aci.ps1";
    else if (mode === "fabric-notebook") scriptName = "deploy-feeder-notebook.ps1";
    else                                 scriptName = "deploy-fabric.ps1";

    let cmd = `Invoke-WebRequest -Uri '${RAW}/tools/deploy-fabric/${scriptName}' -OutFile ${scriptName}; `
      + `./${scriptName}`
      + ` -Source '${source.id}'`;

    if (mode === "fabric-aci") {
      const rg = getValue("resourceGroup");
      if (!rg) { alert("Resource Group is required for the ACI + Fabric deployment."); return; }
      const loc = getValue("location");
      const cgName = getValue("containerGroupName") || source.id;
      cmd += ` -ResourceGroup '${rg}'`;
      if (loc) cmd += ` -Location '${loc}'`;
      cmd += ` -ContainerGroupName '${cgName}'`;
      if (source.key) {
        const apiKey = getValue("apiKey");
        const apiKeyParamName = getValue("apiKeyParamName");
        if (!apiKey) { alert(`This source requires an API key (${apiKeyParamName || "secret"}).`); return; }
        if (apiKeyParamName) {
          cmd += ` -ApiKeyParamName '${apiKeyParamName}' -ApiKey '${apiKey}'`;
        }
      }
    }
    if (subId) cmd += ` -SubscriptionId '${subId}'`;
    cmd += ` -Workspace '${wsId}'`;
    if (ehId) cmd += ` -Eventhouse '${ehId}'`;
    cmd += ` -DatabaseName '${dbName}'`;
    if (mode === "fabric-notebook" || mode === "fabric-aci") {
      cmd += ` -Branch '${BRANCH}'`;
    }

    navigator.clipboard.writeText(cmd).then(() => {
      showDeployNotice("PowerShell command copied to clipboard. Paste it into the Cloud Shell tab.");
      window.open("https://shell.azure.com/?shellType=ps", "_blank", "noopener");
    }).catch(() => {
      showDeployCommand(cmd, "PowerShell");
      window.open("https://shell.azure.com/?shellType=ps", "_blank", "noopener");
    });
  } else {
    // ARM template deploy — use the Azure Portal custom deployment blade
    const templateFile = mode === "container" ? "azure-template.json" : "azure-template-with-eventhub.json";
    const templateUrl = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/${FEEDERS_PREFIX}/${source.id}/${templateFile}`;
    const portalUrl = `https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(templateUrl)}`;
    window.open(portalUrl, "_blank", "noopener");
  }
}

function showDeployNotice(msg) {
  const note = $deployForm.querySelector(".deploy-note");
  if (note) note.innerHTML = `<strong>✓</strong> ${esc(msg)}`;
}

function showDeployCommand(cmd, shell) {
  const note = $deployForm.querySelector(".deploy-note");
  if (note) {
    note.innerHTML = `<strong>Copy this command</strong> into the ${esc(shell)} Cloud Shell tab:`
      + `<pre style="margin-top:8px;white-space:pre-wrap;word-break:break-all;font-size:11px;font-family:var(--font-mono)">${esc(cmd)}</pre>`;
  }
}

function closeDeployPane() {
  $deployPane.style.display = "none";
}

$deployClose.addEventListener("click", closeDeployPane);

function camelToTitle(s) {
  return s.replace(/([A-Z])/g, " $1").replace(/^./, c => c.toUpperCase()).trim();
}

/* ── Helpers ───────────────────────────────────────────────────────────── */
function el(tag, attrs, text) {
  const e = document.createElement(tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (text) e.textContent = text;
  return e;
}

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

/* ── Welcome / landing panel ───────────────────────────────────────────── */
function renderWelcome() {
  let wel = document.getElementById("welcome");
  if (!wel) {
    $content.innerHTML = '<div id="welcome" class="welcome welcome-rich"></div>';
    wel = document.getElementById("welcome");
  }

  const total = SOURCES.length;
  const keyFree = SOURCES.filter(s => !s.key).length;
  const withMqtt = SOURCES.filter(s => s.mqtt).length;
  const withAmqp = SOURCES.filter(s => s.amqp).length;
  const withNotebook = SOURCES.filter(s => s.notebook).length;

  // Category counts, sorted by size descending
  const catCounts = {};
  for (const s of SOURCES) catCounts[s.cat] = (catCounts[s.cat] || 0) + 1;
  const cats = Object.entries(catCounts).sort((a, b) => b[1] - a[1]);

  const catChips = cats.map(([c, n]) =>
    `<button class="welcome-cat" data-cat="${esc(c)}">${esc(c)} <span class="welcome-cat-n">${n}</span></button>`
  ).join("");

  const plural = n => n === 1 ? "" : "s";

  // A few curated quick-starts (all key-free unless noted)
  const quickStarts = [
    { id: "pegelonline", note: "Germany — 3,000 river gauges, every 15 min. Reference implementation for Kafka + MQTT + AMQP transport variants.", mqtt: true, amqp: true },
    { id: "aisstream",   note: "Global — live AIS vessel positions via WebSocket. Free API key, registers in seconds.", mqtt: true, amqp: true },
    { id: "bluesky",     note: "Global — the Bluesky firehose, normalized to CloudEvents.", mqtt: true, amqp: true },
    { id: "dwd",         note: "Germany — DWD weather observations plus CAP severe-weather alerts.", mqtt: true, amqp: true },
    { id: "gtfs",        note: "Global — GTFS-Realtime transit feeds (vehicle positions, trip updates, alerts).", mqtt: true, amqp: true },
    { id: "noaa",        note: "United States — NOAA Tides & Currents, ~3,000 coastal/estuarine stations.", mqtt: true, amqp: true },
  ].filter(q => SOURCES.find(s => s.id === q.id));

  const qsCards = quickStarts.map(q => {
    const s = SOURCES.find(x => x.id === q.id);
    const keyBadge = s.key ? ' <span class="welcome-quick-key">key</span>' : "";
    return `<a class="welcome-quick" href="#${esc(s.id)}">
      <div class="welcome-quick-name">${esc(s.name)}${keyBadge}</div>
      <div class="welcome-quick-note">${esc(q.note)}</div>
    </a>`;
  }).join("");

  wel.innerHTML = `
    <div class="welcome-hero">
      <h2>Real-time data for Apache&nbsp;Kafka, MQTT, AMQP&nbsp;1.0 &mdash; on Azure Event&nbsp;Hubs, Service&nbsp;Bus, Event&nbsp;Grid &amp; Microsoft&nbsp;Fabric</h2>
      <p class="welcome-lede">
        A curated, open-source catalog of <strong>${total} containerized bridges</strong> that pull live, public data
        from weather services, water-level networks, transit feeds, lightning detectors, energy markets, AIS vessel
        trackers, social firehoses, and dozens more &mdash; and re-emit it as binary-mode
        <a href="https://cloudevents.io/" target="_blank" rel="noopener">CloudEvents</a> with strongly-typed
        <a href="https://json-structure.org/" target="_blank" rel="noopener">JSON&nbsp;Structure</a> payloads over
        <strong>Apache&nbsp;Kafka</strong>, <strong>MQTT&nbsp;5.0</strong> (Unified Namespace), and
        <strong>AMQP&nbsp;1.0</strong>. Pick a source, click <strong>Deploy</strong>,
        you&rsquo;re streaming in a couple of minutes.
      </p>
      <div class="welcome-stats">
        <div class="welcome-stat"><div class="welcome-stat-n">${total}</div><div class="welcome-stat-l">sources</div></div>
        <div class="welcome-stat"><div class="welcome-stat-n">${keyFree}</div><div class="welcome-stat-l">no API key</div></div>
        <div class="welcome-stat"><div class="welcome-stat-n">${withMqtt}</div><div class="welcome-stat-l">also MQTT&nbsp;/&nbsp;UNS</div></div>
        <div class="welcome-stat"><div class="welcome-stat-n">${withAmqp}</div><div class="welcome-stat-l">also AMQP&nbsp;1.0</div></div>
        <div class="welcome-stat"><div class="welcome-stat-n">${withNotebook}</div><div class="welcome-stat-l">Fabric notebook</div></div>
      </div>
    </div>

    <div class="welcome-section">
      <h3>What you&rsquo;ll find in the catalog</h3>
      <p>Sources are organized by domain. Click a chip to filter the list on the left, or pick any row.</p>
      <div class="welcome-cats">${catChips}</div>
    </div>

    <div class="welcome-section">
      <h3>Five ways to deploy &mdash; one click each</h3>
      <div class="welcome-deploys">
        <div class="welcome-deploy">
          <div class="welcome-deploy-title">Azure Container &rarr; Event Hubs</div>
          <div class="welcome-deploy-body">
            ARM templates that spin up an Azure Container Instance running the Kafka feeder, writing into an
            Event Hubs namespace you already own &mdash; or a brand-new one provisioned alongside.
            <em>Every source supports this.</em>
          </div>
        </div>
        <div class="welcome-deploy">
          <div class="welcome-deploy-title">Azure Container &rarr; Service Bus (AMQP&nbsp;1.0)</div>
          <div class="welcome-deploy-body">
            ${withAmqp} source${plural(withAmqp)} ship${withAmqp === 1 ? "s" : ""} an AMQP&nbsp;1.0 variant that publishes via Microsoft Entra ID
            (no SAS-key rotation) into a brand-new Azure Service Bus namespace provisioned by the template.
            Also works against Event Hubs, RabbitMQ AMQP&nbsp;1.0, Artemis, and Qpid&nbsp;Dispatch.
          </div>
        </div>
        <div class="welcome-deploy">
          <div class="welcome-deploy-title">Azure Container &rarr; MQTT&nbsp;/&nbsp;Event Grid</div>
          <div class="welcome-deploy-body">
            ${withMqtt} source${plural(withMqtt)} additionally publish${withMqtt === 1 ? "es" : ""} MQTT&nbsp;5.0 binary-mode CloudEvents on a hierarchical
            Unified-Namespace topic tree (e.g. <code>weather/dk/dmi/met-obs/&lt;station&gt;/&lt;parameter&gt;</code>).
            Deploy alongside an Azure Event Grid namespace MQTT broker, or point at any MQTT&nbsp;5 broker you run.
          </div>
        </div>
        <div class="welcome-deploy">
          <div class="welcome-deploy-title">Azure Container &rarr; Fabric Event Stream</div>
          <div class="welcome-deploy-body">
            Same ACI feeder, deployed via the portal here, writing into a Fabric Event Stream custom endpoint
            inside a Fabric Eventhouse. The deploy script provisions the Eventhouse, KQL database, and
            update policies for you.
          </div>
        </div>
        <div class="welcome-deploy">
          <div class="welcome-deploy-title">Fabric Notebook &mdash; no Azure subscription</div>
          <div class="welcome-deploy-body">
            For poll-based sources (${withNotebook} of ${total}): the feeder runs as a scheduled Fabric
            notebook inside your workspace. Ingestion, storage, query &mdash; all in Fabric.
            Look for the <em>Fabric Notebook Feeder</em> button.
          </div>
        </div>
      </div>
    </div>

    <div class="welcome-section">
      <h3>Designed for serious use, not just demos</h3>
      <ul class="welcome-bullets">
        <li><strong>Stable keys, topics, and addresses.</strong> Every source keys on a stable upstream identifier
          (station ID, MMSI, gauge number, sensor ID) and aligns the Kafka key, CloudEvents subject, MQTT topic
          template, and AMQP node so partitioning, log compaction, joins, and broker routing work the way you
          expect.</li>
        <li><strong>CloudEvents + JSON&nbsp;Structure contracts.</strong> Every source ships an
          <a href="https://github.com/xregistry/spec" target="_blank" rel="noopener">xRegistry</a>
          manifest with exhaustive schemas, units, validation extensions, and altnames mapping to
          upstream field names. Browse the per-source <code>EVENTS.md</code> for the full event list.</li>
        <li><strong>Reference data as events.</strong> Catalog data (stations, sensors, routes, zones)
          is emitted as named CloudEvents on the same topic, MQTT tree, or AMQP node as telemetry &mdash;
          not hidden in an out-of-band API. Re-emitted on a refresh cadence.</li>
        <li><strong>KQL schemas included.</strong> Every source ships a generated
          <code>kql/&lt;source&gt;.kql</code> with tables, materialized views, update policies,
          and ingestion mappings for Azure Data Explorer / Fabric Eventhouse.</li>
      </ul>
    </div>

    <div class="welcome-section">
      <h3>Try one of these first</h3>
      <div class="welcome-quicks">${qsCards}</div>
    </div>

    <div class="welcome-foot">
      Built and maintained by <a href="https://github.com/clemensv" target="_blank" rel="noopener">Clemens&nbsp;Vasters</a>
      and contributors &middot; <a href="https://github.com/clemensv/real-time-sources" target="_blank" rel="noopener">source on GitHub</a>
      &middot; MIT-licensed.
    </div>
  `;

  // Wire up category chips
  wel.querySelectorAll(".welcome-cat").forEach(chip => {
    chip.addEventListener("click", () => {
      const cat = chip.getAttribute("data-cat");
      selectCategory(cat);
      const sb = document.getElementById("search-box");
      if (sb) sb.value = "";
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
}

/* ── Boot ──────────────────────────────────────────────────────────────── */
renderPills();
renderList();

/* ── Share button + popover ─────────────────────────────────────────────
   The Share button is visible only when a source is selected (location.hash
   resolves to a known source). Clicking it opens a popover containing:
     - the canonical share URL (https://<host>/<base>/share/<sid>/) which is
       backed by a static OG-meta-rich HTML shell + 1200x630 og.png that
       crawlers can render rich link previews for
     - a Copy button
     - intent links for X, LinkedIn, Bluesky, Mastodon, Reddit and email
   The static shells are emitted at build time by
   tools/ghpages/generate_share_pages.py and committed to the ghpages branch
   alongside this app.js.
   ────────────────────────────────────────────────────────────────────── */
const SITE_BASE = `${location.origin}${location.pathname.replace(/\/[^/]*$/, "")}`;

function shareUrlFor(sid) {
  return `${SITE_BASE}/share/${sid}/`;
}

function buildIntents(sourceName, url) {
  const text = `${sourceName} — real-time data on Kafka, MQTT and AMQP`;
  const encU = encodeURIComponent(url);
  const encT = encodeURIComponent(text);
  const encTU = encodeURIComponent(`${text}\n${url}`);
  return [
    { label: "X",        href: `https://twitter.com/intent/tweet?text=${encT}&url=${encU}` },
    { label: "LinkedIn", href: `https://www.linkedin.com/sharing/share-offsite/?url=${encU}` },
    { label: "Bluesky",  href: `https://bsky.app/intent/compose?text=${encTU}` },
    { label: "Mastodon", href: `https://mastodonshare.com/?text=${encTU}` },
    { label: "Reddit",   href: `https://www.reddit.com/submit?url=${encU}&title=${encT}` },
    { label: "Email",    href: `mailto:?subject=${encT}&body=${encTU}` },
  ];
}

function renderShareIntents(source, url) {
  if (!$shareIntents) return;
  $shareIntents.innerHTML = "";
  for (const intent of buildIntents(source.name, url)) {
    const a = document.createElement("a");
    a.className = "share-intent";
    a.href = intent.href;
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = intent.label;
    $shareIntents.appendChild(a);
  }
}

function openSharePopover(source) {
  if (!$sharePopover || !$shareBtn) return;
  const url = shareUrlFor(source.id);
  if ($shareTitle) $shareTitle.textContent = `Share ${source.name}`;
  if ($shareUrl)   $shareUrl.value = url;
  renderShareIntents(source, url);
  $sharePopover.style.display = "block";
  $shareBtn.setAttribute("aria-expanded", "true");
}

function closeSharePopover() {
  if (!$sharePopover || !$shareBtn) return;
  $sharePopover.style.display = "none";
  $shareBtn.setAttribute("aria-expanded", "false");
}

function flashShareToast(msg) {
  if (!$shareToast) return;
  $shareToast.textContent = msg;
  $shareToast.style.opacity = "1";
  clearTimeout(flashShareToast._t);
  flashShareToast._t = setTimeout(() => { $shareToast.style.opacity = "0"; }, 1800);
}

function updateShareButton() {
  if (!$shareBtn) return;
  const s = activeSource ? SOURCES.find(x => x.id === activeSource) : null;
  if (s) {
    $shareBtn.style.display = "";
    $shareBtn.dataset.source = s.id;
    $shareBtn.title = `Share ${s.name}`;
  } else {
    $shareBtn.style.display = "none";
    closeSharePopover();
  }
}

if ($shareBtn) {
  $shareBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    const s = SOURCES.find(x => x.id === activeSource);
    if (!s) return;
    if ($sharePopover && $sharePopover.style.display === "block") {
      closeSharePopover();
    } else {
      openSharePopover(s);
    }
  });
}
if ($shareCopy && $shareUrl) {
  $shareCopy.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText($shareUrl.value);
      flashShareToast("Link copied!");
    } catch {
      // Fallback: select the input so the user can copy manually.
      $shareUrl.select();
      $shareUrl.setSelectionRange(0, 9999);
      flashShareToast("Press Ctrl/Cmd+C to copy");
    }
  });
}
if ($sharePopover) {
  // Click-outside dismiss.
  document.addEventListener("click", (e) => {
    if ($sharePopover.style.display !== "block") return;
    if (e.target === $shareBtn || $shareBtn?.contains?.(e.target)) return;
    if ($sharePopover.contains(e.target)) return;
    closeSharePopover();
  });
  // Esc dismiss.
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && $sharePopover.style.display === "block") {
      closeSharePopover();
      $shareBtn?.focus();
    }
  });
}

/* ── Hash deep-linking ────────────────────────────────────────────────────
   #<id>                     → select source, show docs
   #<id>/fabric              → select source + open Fabric deploy panel
                               (notebook if available, else ACI)
   #<id>/fabric-aci          → select source + open Fabric ACI deploy panel
   #<id>/fabric-notebook     → select source + open Fabric Notebook deploy panel
   #<id>/azure               → select source + launch Azure ARM deploy
                               (azure-template-with-eventhub.json)
   #<id>/azure-byoeh         → select source + launch Azure ARM deploy
                               (azure-template.json, bring-your-own Event Hub)
   #<id>/azure-mqtt          → select source + launch Azure ARM deploy
                               (azure-template-mqtt.json, bring-your-own MQTT broker)
   #<id>/azure-mqtt-eg       → select source + launch Azure ARM deploy
                               (azure-template-with-eventgrid-mqtt.json, Event Grid MQTT broker)
   #<id>/azure-amqp-sb       → select source + launch Azure ARM deploy
                               (azure-template-with-servicebus.json, Service Bus AMQP 1.0 broker) */
async function selectFromHash() {
  const raw = (location.hash || "").replace(/^#/, "").trim();
  if (!raw) {
    // No hash — render the landing/welcome panel.
    activeSource = null;
    $deployBar.style.display = "none";
    $deployBarFabric.style.display = "none";
    if (typeof closeDeployPane === "function") closeDeployPane();
    renderList();
    renderWelcome();
    updateShareButton();
    return;
  }
  const [id, action] = raw.split("/");
  const s = SOURCES.find(x => x.id === id);
  if (!s) { updateShareButton(); return; }
  await selectSource(s);
  updateShareButton();
  if (action === "fabric") {
    openDeployForm(s, s.notebook ? "fabric-notebook" : "fabric-aci");
  } else if (action === "fabric-aci") {
    openDeployForm(s, "fabric-aci");
  } else if (action === "fabric-notebook") {
    openDeployForm(s, "fabric-notebook");
  } else if (action === "azure") {
    const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-with-eventhub.json`;
    window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
  } else if (action === "azure-byoeh") {
    const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template.json`;
    window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
  } else if (action === "azure-mqtt") {
    const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-mqtt.json`;
    window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
  } else if (action === "azure-mqtt-eg") {
    const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-with-eventgrid-mqtt.json`;
    window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
  } else if (action === "azure-amqp-sb") {
    const url = `${RAW}/${FEEDERS_PREFIX}/${s.id}/azure-template-with-servicebus.json`;
    window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
  }
}
window.addEventListener("hashchange", selectFromHash);
selectFromHash();
