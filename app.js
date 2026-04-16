/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Real-Time Sources — Catalog App
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

const REPO = "clemensv/real-time-sources";
const BRANCH = "main";
const RAW = `https://raw.githubusercontent.com/${REPO}/${BRANCH}`;

/* ── Source catalog ────────────────────────────────────────────────────── */
const SOURCES = [
  // ── Hydrology and Water Monitoring ──
  { id: "bafu-hydro",            name: "BAFU Hydro",              cat: "Hydrology",    key: false, desc: "Switzerland — ~300 stations, FOEN" },
  { id: "cdec-reservoirs",       name: "CDEC Reservoirs",         cat: "Hydrology",    key: false, desc: "California — ~2,600 stations, DWR" },
  { id: "chmi-hydro",            name: "CHMI Hydro",              cat: "Hydrology",    key: false, desc: "Czech Republic — CHMU" },
  { id: "german-waters",         name: "German Waters",           cat: "Hydrology",    key: false, desc: "Germany — 12 state portals, ~2,724 stations" },
  { id: "hubeau-hydrometrie",    name: "Hub'Eau Hydrometrie",     cat: "Hydrology",    key: false, desc: "France — ~6,300 stations" },
  { id: "imgw-hydro",            name: "IMGW Hydro",              cat: "Hydrology",    key: false, desc: "Poland — IMGW-PIB" },
  { id: "ireland-opw-waterlevel",name: "Ireland OPW Water Level", cat: "Hydrology",    key: false, desc: "Ireland — ~500 OPW hydrometric stations" },
  { id: "nepal-bipad-hydrology", name: "Nepal BIPAD Hydrology",   cat: "Hydrology",    key: false, desc: "Nepal — Himalayan river basins, BIPAD" },
  { id: "noaa",                  name: "NOAA Tides & Currents",   cat: "Hydrology",    key: false, desc: "United States — ~3,000 stations" },
  { id: "noaa-ndbc",             name: "NOAA NDBC",               cat: "Hydrology",    key: false, desc: "United States — buoy observations" },
  { id: "king-county-marine",    name: "King County Marine",      cat: "Hydrology",    key: false, desc: "Washington State / Puget Sound — buoy and mooring telemetry" },
  { id: "nve-hydro",             name: "NVE Hydro",               cat: "Hydrology",    key: true,  desc: "Norway — NVE (requires free API key)" },
  { id: "pegelonline",           name: "Pegelonline",             cat: "Hydrology",    key: false, desc: "Germany — federal waterways, ~3,000 stations" },
  { id: "rws-waterwebservices",  name: "RWS Waterwebservices",    cat: "Hydrology",    key: false, desc: "Netherlands — ~785 stations" },
  { id: "smhi-hydro",            name: "SMHI Hydro",              cat: "Hydrology",    key: false, desc: "Sweden — SMHI" },
  { id: "snotel",                name: "SNOTEL Snow",             cat: "Hydrology",    key: false, desc: "Western US & Alaska — ~900 snowpack stations, NRCS" },
  { id: "syke-hydro",            name: "SYKE Hydro",              cat: "Hydrology",    key: false, desc: "Finland — SYKE" },
  { id: "uk-ea-flood-monitoring",name: "UK EA Flood Monitoring",  cat: "Hydrology",    key: false, desc: "England — ~4,000 stations" },
  { id: "usgs-iv",               name: "USGS Instantaneous Values", cat: "Hydrology",  key: false, desc: "United States — ~1.5M stations" },
  { id: "usgs-nwis-wq",          name: "USGS NWIS Water Quality", cat: "Hydrology",    key: false, desc: "United States — ~3,000 continuous WQ sites" },
  { id: "waterinfo-vmm",         name: "Waterinfo VMM",           cat: "Hydrology",    key: false, desc: "Belgium / Flanders — ~1,785 stations" },

  // ── Weather and Meteorology ──
  { id: "aviationweather",       name: "AviationWeather.gov",     cat: "Weather",      key: false, desc: "Global — METAR, SIGMET advisories" },
  { id: "blitzortung",           name: "Blitzortung",             cat: "Weather",      key: false, desc: "Global — community lightning strokes, seconds latency" },
  { id: "bom-australia",         name: "BOM Australia",           cat: "Weather",      key: false, desc: "Australia — ~8 capital city airports, half-hourly obs" },
  { id: "dwd",                   name: "DWD",                     cat: "Weather",      key: false, desc: "Germany — ~1,450 stations, observations and CAP alerts" },
  { id: "dwd-pollenflug",        name: "DWD Pollenflug",          cat: "Weather",      key: false, desc: "Germany — daily pollen forecasts, 27 regions" },
  { id: "environment-canada",    name: "Environment Canada",      cat: "Weather",      key: false, desc: "Canada — ~963 SWOB stations, hourly obs" },
  { id: "geosphere-austria",     name: "GeoSphere Austria",       cat: "Weather",      key: false, desc: "Austria — ~280 TAWES stations, 10-min obs" },
  { id: "hko-hong-kong",         name: "HKO Hong Kong",           cat: "Weather",      key: false, desc: "Hong Kong — 27 temp stations, 18 rainfall districts" },
  { id: "jma-japan",             name: "JMA Japan",               cat: "Weather",      key: false, desc: "Japan — weather bulletins, warnings, forecasts" },
  { id: "meteoalarm",            name: "Meteoalarm",              cat: "Weather",      key: false, desc: "Europe — 37 countries, severe weather warnings" },
  { id: "noaa-nws",              name: "NOAA NWS",                cat: "Weather",      key: false, desc: "United States — weather alerts, CAP" },
  { id: "nws-forecasts",         name: "NWS Forecast Zones",      cat: "Weather",      key: false, desc: "United States — configurable land and marine forecast zones" },
  { id: "nws-alerts",            name: "NWS CAP Alerts",          cat: "Weather",      key: false, desc: "United States — active alerts via api.weather.gov" },
  { id: "noaa-goes",             name: "NOAA GOES / SWPC",        cat: "Weather",      key: false, desc: "Global — space weather, solar wind, K-index" },
  { id: "singapore-nea",         name: "Singapore NEA",           cat: "Weather",      key: false, desc: "Singapore — 62 weather stations + 5 air-quality regions" },
  { id: "smhi-weather",          name: "SMHI Weather",            cat: "Weather",      key: false, desc: "Sweden — ~232 stations, hourly obs" },

  // ── Air Quality and Environmental Health ──
  { id: "canada-aqhi",           name: "Canada AQHI",             cat: "Air Quality",  key: false, desc: "Canada — community AQHI observations and forecasts" },
  { id: "defra-aurn",            name: "Defra AURN",              cat: "Air Quality",  key: false, desc: "United Kingdom — 300+ monitoring locations, hourly pollutants" },
  { id: "fmi-finland",           name: "FMI Finland",             cat: "Air Quality",  key: false, desc: "Finland — hourly air quality observations via FMI WFS" },
  { id: "gios-poland",           name: "GIOŚ Poland",             cat: "Air Quality",  key: false, desc: "Poland — ~250 stations, hourly pollutants + AQI" },
  { id: "hongkong-epd",          name: "Hong Kong EPD AQHI",      cat: "Air Quality",  key: false, desc: "Hong Kong — 18 AQHI stations, hourly health index" },
  { id: "irceline-belgium",      name: "IRCELINE Belgium",        cat: "Air Quality",  key: false, desc: "Belgium — station, timeseries, and hourly observations" },
  { id: "laqn-london",           name: "LAQN London",             cat: "Air Quality",  key: false, desc: "London, UK — site metadata, species, hourly measurements" },
  { id: "luchtmeetnet-nl",       name: "Luchtmeetnet Netherlands",cat: "Air Quality",  key: false, desc: "Netherlands — station measurements, components, LKI index" },
  { id: "epa-uv",                name: "EPA UV Index",            cat: "Air Quality",  key: false, desc: "United States — city-scoped hourly and daily UV forecasts" },
  { id: "sensor-community",      name: "Sensor.Community",        cat: "Air Quality",  key: false, desc: "Global — citizen air sensors, PM and climate readings" },
  { id: "uba-airdata",           name: "UBA AirData",             cat: "Air Quality",  key: false, desc: "Germany — stations, pollutant components, hourly measures" },
  { id: "wallonia-issep",        name: "Wallonia ISSeP",          cat: "Air Quality",  key: false, desc: "Belgium / Wallonia — low-cost air quality sensors" },

  // ── Disaster Alerts and Civil Protection ──
  { id: "australia-wildfires",   name: "Australian Wildfires",    cat: "Disasters",    key: false, desc: "Australia — NSW, QLD, VIC bushfire incidents" },
  { id: "eaws-albina",           name: "EAWS ALBINA Avalanche",   cat: "Disasters",    key: false, desc: "European Alps — daily avalanche bulletins, CAAMLv6" },
  { id: "gdacs",                 name: "GDACS",                   cat: "Disasters",    key: false, desc: "Global — earthquakes, floods, cyclones, volcanoes, droughts" },
  { id: "inpe-deter-brazil",     name: "INPE DETER Brazil",       cat: "Disasters",    key: false, desc: "Brazil — Amazon & Cerrado deforestation alerts" },
  { id: "nifc-usa-wildfires",    name: "NIFC USA Wildfires",      cat: "Disasters",    key: false, desc: "United States — active wildfire incidents, NIFC" },
  { id: "nina-bbk",              name: "NINA/BBK",                cat: "Disasters",    key: false, desc: "Germany — MOWAS, KATWARN, BIWAPP, DWD, LHP, Police" },
  { id: "ptwc-tsunami",          name: "PTWC Tsunami",            cat: "Disasters",    key: false, desc: "Pacific and Atlantic — NOAA tsunami bulletins" },
  { id: "seattle-911",           name: "Seattle Fire 911",        cat: "Disasters",    key: false, desc: "Seattle, WA — real-time fire dispatch incidents" },
  { id: "usgs-earthquakes",      name: "USGS Earthquakes",        cat: "Disasters",    key: false, desc: "Global — seismic events" },

  // ── Radiation Monitoring ──
  { id: "bfs-odl",               name: "BfS ODL",                 cat: "Radiation",    key: false, desc: "Germany — ~1,700 stations, hourly gamma dose rate" },
  { id: "eurdep-radiation",      name: "EURDEP Radiation",        cat: "Radiation",    key: false, desc: "Europe — ~5,500 stations, 39 countries, gamma dose" },
  { id: "usgs-geomag",           name: "USGS Geomagnetism",       cat: "Radiation",    key: false, desc: "United States — 14 observatories, 1-min geomagnetic field" },

  // ── Maritime and Vessel Tracking ──
  { id: "aisstream",             name: "AISStream",               cat: "Maritime",     key: true,  desc: "Global — AIS via WebSocket, ~200 km from shore" },
  { id: "digitraffic-maritime",  name: "Digitraffic Maritime",    cat: "Maritime",     key: false, desc: "Finland / Baltic Sea — AIS via MQTT" },
  { id: "kystverket-ais",        name: "Kystverket AIS",          cat: "Maritime",     key: false, desc: "Norway / Svalbard — raw TCP AIS, ~34 msg/s" },

  // ── Aviation ──
  { id: "mode-s",                name: "Mode-S",                  cat: "Aviation",     key: false, desc: "Local — ADS-B via dump1090 receivers" },
  { id: "vatsim",                name: "VATSIM",                  cat: "Aviation",     key: false, desc: "Global — virtual aviation network, pilots & controllers" },

  // ── Road Transport ──
  { id: "autobahn",              name: "Autobahn",                cat: "Transport",    key: false, desc: "Germany — roadworks, warnings, closures, webcams" },
  { id: "digitraffic-road",      name: "Digitraffic Road",        cat: "Transport",    key: false, desc: "Finland — TMS sensors, road weather, traffic messages" },
  { id: "french-road-traffic",   name: "French Road Traffic",     cat: "Transport",    key: false, desc: "France — national road network, DATEX II" },
  { id: "gtfs",                  name: "GTFS Realtime",           cat: "Transport",    key: false, desc: "Global — 1,000+ transit agencies, vehicles, trips, alerts" },
  { id: "madrid-traffic",        name: "Madrid Traffic",          cat: "Transport",    key: false, desc: "Madrid, Spain — ~4,000 sensors, Informo" },
  { id: "ndl-netherlands",       name: "NDW Netherlands Traffic", cat: "Transport",    key: false, desc: "Netherlands — national road traffic, DATEX II" },
  { id: "paris-bicycle-counters",name: "Paris Bicycle Counters",  cat: "Transport",    key: false, desc: "Paris — ~141 counting stations, hourly counts" },
  { id: "seattle-street-closures", name: "Seattle Street Closures", cat: "Transport",  key: false, desc: "Seattle, WA — permit-driven street closure windows" },
  { id: "cbp-border-wait",       name: "US CBP Border Wait",      cat: "Transport",    key: false, desc: "US borders — ~81 ports of entry" },
  { id: "wsdot",                 name: "WSDOT",                   cat: "Transport",    key: true,  desc: "Washington State — ~1,000 traffic flow sensors (requires free key)" },

  // ── Railway ──
  { id: "irail",                 name: "iRail",                   cat: "Railway",      key: false, desc: "Belgium — ~600 NMBS/SNCB stations, departures, delays" },

  // ── Energy and Infrastructure ──
  { id: "carbon-intensity",      name: "Carbon Intensity UK",     cat: "Energy",       key: false, desc: "United Kingdom — national grid carbon intensity" },
  { id: "elexon-bmrs",           name: "Elexon BMRS",             cat: "Energy",       key: false, desc: "Great Britain — electricity market, generation, demand" },
  { id: "energidataservice-dk",  name: "Energi Data Service",     cat: "Energy",       key: false, desc: "Denmark — power system, spot prices, CO₂" },
  { id: "energy-charts",         name: "Energy-Charts",           cat: "Energy",       key: false, desc: "Europe — 40+ countries, electricity generation & prices" },
  { id: "entsoe",                name: "ENTSO-E",                 cat: "Energy",       key: true,  desc: "Europe — electricity generation, prices, load, flows (requires token)" },

  // ── Social Media and News ──
  { id: "bluesky",               name: "Bluesky Firehose",        cat: "Social",       key: false, desc: "Global — posts, likes, reposts, follows" },
  { id: "wikimedia-osm-diffs",   name: "OpenStreetMap Diffs",     cat: "Social",       key: false, desc: "Global — OSM minutely replication diffs" },
  { id: "rss",                   name: "RSS Feeds",               cat: "Social",       key: false, desc: "Any — configurable RSS/Atom feed URLs or OPML files" },
  { id: "wikimedia-eventstreams", name: "Wikimedia EventStreams",  cat: "Social",       key: false, desc: "Global — Wikipedia, Wikidata, Commons recent changes" },

  // ── Scientific Research ──
  { id: "gracedb",               name: "GraceDB",                 cat: "Science",      key: false, desc: "Global — LIGO/Virgo/KAGRA gravitational wave candidates" },
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
const $btnFabric = document.getElementById("btn-container-eh-adx");
const $deployPane = document.getElementById("deploy-pane");
const $deployTitle = document.getElementById("deploy-pane-title");
const $deployClose = document.getElementById("deploy-pane-close");
const $deployForm = document.getElementById("deploy-form-area");

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
  });
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

  // wire deploy buttons
  $btnContainer.onclick   = () => {
    const url = `${RAW}/${s.id}/azure-template.json`;
    window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
  };
  $btnContainerEH.onclick = () => {
    const url = `${RAW}/${s.id}/azure-template-with-eventhub.json`;
    window.open(`https://portal.azure.com/#create/Microsoft.Template/uri/${encodeURIComponent(url)}`, "_blank", "noopener");
  };
  $btnFabric.onclick      = () => openDeployForm(s, "fabric");

  // fetch and render CONTAINER.md
  $content.innerHTML = '<div class="loading-indicator">Loading documentation…</div>';
  try {
    const url = `${RAW}/${s.id}/CONTAINER.md`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    let md = await resp.text();
    md = md.replace(/\]\((?!https?:\/\/)([^)]+)\)/g, (m, p) =>
      `](https://github.com/${REPO}/blob/${BRANCH}/${s.id}/${p})`
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
  const azSection = el("div", { class: "form-section" });
  azSection.innerHTML = '<div class="form-section-title">Azure Resources</div>';
  azSection.appendChild(makeField("subscriptionId", "Subscription ID", "text",
    "", "Azure subscription GUID (leave blank for default)", false));
  azSection.appendChild(makeField("resourceGroup", "Resource Group", "text",
    "", "Azure resource group name", true));
  azSection.appendChild(makeField("location", "Location", "text",
    "westcentralus", "Azure region for deployment", true));
  $deployForm.appendChild(azSection);

  // Fabric section
  const fabSection = el("div", { class: "form-section" });
  fabSection.innerHTML = '<div class="form-section-title">Microsoft Fabric</div>';
  fabSection.appendChild(makeField("workspace", "Workspace", "text",
    "", "Fabric workspace name or GUID", true));
  fabSection.appendChild(makeField("eventhouse", "Eventhouse", "text",
    "", "Fabric Eventhouse name or GUID (leave blank to create new)", false));
  fabSection.appendChild(makeField("databaseName", "KQL Database Name", "text",
    source.id.replace(/-/g, "_"), "Name for the KQL database", false));
  $deployForm.appendChild(fabSection);

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

  const rg = getValue("resourceGroup");
  const loc = getValue("location");
  const subId = getValue("subscriptionId");

  if (!rg) { alert("Resource Group is required."); return; }
  if (!loc) { alert("Location is required."); return; }

  if (mode === "fabric") {
    const ws = getValue("workspace");
    const eh = getValue("eventhouse");
    if (!ws) {
      alert("Workspace is required for Fabric deployment.");
      return;
    }
    const dbName = getValue("databaseName") || source.id.replace(/-/g, "_");

    let cmd = `Invoke-WebRequest -Uri '${RAW}/tools/deploy-fabric/deploy-fabric.ps1' -OutFile deploy-fabric.ps1; `
      + `./deploy-fabric.ps1`
      + ` -Source '${source.id}'`
      + ` -ResourceGroup '${rg}'`
      + ` -Location '${loc}'`;
    if (subId) cmd += ` -SubscriptionId '${subId}'`;
    cmd += ` -Workspace '${ws}'`;
    if (eh) cmd += ` -Eventhouse '${eh}'`;
    cmd += ` -DatabaseName '${dbName}'`;

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
    const templateUrl = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/${source.id}/${templateFile}`;
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

/* ── Boot ──────────────────────────────────────────────────────────────── */
renderPills();
renderList();
