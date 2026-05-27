# data.europa.eu SPARQL Sweep — Round 2

Research conducted: 2026-04-08

This pass used the new `data.europa.eu` discovery workflow from the search playbook:

1. REST search queries to find high-signal datasets per candidate category.
2. SPARQL queries against `https://data.europa.eu/sparql` to expand shortlisted datasets into concrete distribution URLs.
3. Direct endpoint probes to separate live APIs from static catalog entries.

The useful result is not that the portal contains many datasets. It does. The useful result is which of those datasets actually expose something bridgeable.

## Strong new leads

| Category | Candidate | Country | Portal finding | Verified endpoint | Assessment |
|---|---|---|---|---|---|
| Hydrology | Danish Miljoeportalen VANDaH (`Hydrometri og grundvand`) | Denmark | `data.europa.eu` exposes the dataset and points at a public OpenAPI description | `https://vandah.miljoeportal.dk/api/swagger/v1/swagger.json` and live `GET /api/stations`, `GET /api/water-levels?stationId=70000590&from=2026-04-06&to=2026-04-08` | **Strong new candidate.** This closes the Denmark hydrology gap more convincingly than the earlier DMI weather-observation workaround. The API is real, current, and station-keyed. |
| Radiation | Ireland EPA `Radiation Monitoring locations` | Ireland | SPARQL expands the dataset to a concrete WFS download URL | `http://gis.epa.ie/geoserver/EPA/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=EPA:RAD_MONITORINGSTATION&maxFeatures=50&outputFormat=application/json&srsName=EPSG:4326` | **Strong new candidate.** Public GeoServer WFS, no auth seen, live station features returned. This is the cleanest non-EURDEP European radiation lead found in this pass. |
| Road traffic | Luxembourg CITA DATEX II traffic feeds | Luxembourg | SPARQL expands `Cita : Donnees trafic en DATEX II` into concrete roadway feed URLs | `https://www.cita.lu/info_trafic/datex/trafficstatus_a6` (plus `a1`, `a3`, `a4`, `a7`, `a13`, `b40`) | **Strong new candidate.** The sampled feed returned DATEX II XML with 36 `siteMeasurements` on the A6. This is exactly the kind of reusable European DATEX source worth building against. |
| Air quality | Wallonia ISSeP `last-data-capteurs-qualite-de-l-air-issep` | Belgium | SPARQL confirms JSON/CSV/RDF distributions for the dataset | `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records?limit=2` | **Good additive candidate.** Live Opendatasoft JSON returned records timestamped on 2026-04-08. This complements the existing Belgian IRCELINE note with a regional feed that is simpler to consume. |

## Detail-only improvements for existing candidate families

| Category | Existing family | New detail from the portal | Why it matters |
|---|---|---|---|
| EV charging | AFIR / Mobilithek landscape | `AFIR-recharging-dyn-Tesla`, `AFIR-recharging-dyn-Wirelane`, and `AFIR-recharging-stat-Wirelane` are explicitly indexed with JSON distributions and recent modification timestamps | This does not create a brand-new source family, but it does confirm that operator-level AFIR dynamic/static feeds are landing in the portal and are worth folding into the AFIR landscape work. |
| Radiation | Poland GIOS INSPIRE radiation services | The portal exposes both SOS and ATOM distributions for ionizing-radiation monitoring datasets | This is more useful as supporting detail than as a top-priority runtime source. Still, it shows the portal can surface machine-readable INSPIRE downloads outside the EURDEP path. |
| Weather | DWD SYNOP | `data.europa.eu` points straight at `https://opendata.dwd.de/weather/weather_reports/synoptic/germany/` | Not a new candidate, but it confirms the portal is useful for discovering WMO/DWD distribution endpoints when the source name is already known. |

## Low-signal or non-bridgeable hits in this round

| Category | Portal hit | Result | Conclusion |
|---|---|---|---|
| Parking | Galway `CarParkingOpenData` | Live ArcGIS layer exists, but the exposed fields are `NAME`, `TYPE`, `NO_SPACES`, and coordinates — effectively static inventory, not occupancy | Useful reference data, not a parking-availability bridge candidate by itself |
| Wildfire | Valencia `PATFOR` datasets | Portal exposes WMS and GIS download links, but the content is vulnerability / fire-risk mapping, not live fire incidents | Good context layer, weak runtime source |
| Tidal / sea level | Irish `Tide Gauge Deployment` datasets | The portal indexed station catalog entries, but the exposed distribution links collapsed to `marine.ie` landing pages rather than concrete data endpoints | Worth deeper direct probing later, but not actionable from the portal alone |
| Water quality | `Bathing Water Quality` hits | Results were mostly compliance/static layers or misclassified marine-planning content, not real-time telemetry | Low-value for this repo's streaming focus |
| Parking / traffic overlap | Luxembourg `Infos parking en DATEX II` | The portal exposes parking feeds alongside traffic feeds, but the traffic feed was the clearly stronger immediate runtime target | Build traffic first; revisit parking after inspecting the DATEX parking payloads |

## Category-by-category take

- **Hydrology**: The best surprise. Denmark now has a concrete, public, station-keyed hydrometry API with current water-level results.
- **Radiation**: Ireland EPA is a legitimate new candidate. The portal also surfaced Polish INSPIRE downloads, but Ireland is the cleaner bridge target.
- **Road traffic**: Luxembourg CITA is the standout DATEX find from this round.
- **Air quality**: Belgium ISSeP adds regional detail and a very simple Opendatasoft access path.
- **EV charging**: The portal is strongest here as a metadata amplifier. It makes AFIR operator feeds easier to enumerate, but it mostly enriches work already underway.
- **Weather**: Good for confirming known distributions, weak for finding genuinely new high-priority runtime sources.
- **Parking / wildfire / water quality / tidal**: The portal mostly surfaced reference layers, catalogs, or planning artifacts rather than stream-grade feeds.

## Practical query pattern that worked

The portal was most useful when used in two stages:

```sparql
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct:  <http://purl.org/dc/terms/>

SELECT ?access ?format
WHERE {
  VALUES ?dataset { <http://data.europa.eu/88u/dataset/...> }
  ?dataset dcat:distribution ?dist .
  ?dist dcat:accessURL ?access .
  OPTIONAL { ?dist dct:format ?format . }
}
LIMIT 20
```

That is the right shape of query. Use REST search to find candidate dataset resources first; then use SPARQL to fan out the distributions. Doing discovery with SPARQL alone is possible, but noisier and more failure-prone.

## Recommended follow-up

1. Promote **Denmark VANDaH**, **Ireland EPA radiation**, and **Luxembourg CITA DATEX** into full candidate notes.
2. Fold the **AFIR operator-level findings** into `tools/candidates/ev-charging/eu-afir-nap-landscape.md`.
3. Treat **Galway parking**, **PATFOR**, and the Irish tide-gauge catalog entries as reference-data leads until a real telemetry endpoint is confirmed.
