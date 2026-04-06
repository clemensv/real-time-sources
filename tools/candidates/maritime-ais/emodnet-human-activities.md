# EMODnet Human Activities — Vessel Density & Port Traffic

**Country/Region**: European seas (Atlantic, Baltic, Mediterranean, Black Sea, Arctic)
**Publisher**: European Marine Observation and Data Network (EMODnet)
**API Endpoint**: `https://ows.emodnet-humanactivities.eu/wms` (WMS) / `https://ows.emodnet-humanactivities.eu/wfs` (WFS)
**Documentation**: https://emodnet.ec.europa.eu/en/human-activities
**Protocol**: OGC WMS 1.3.0 / WFS 2.0.0
**Auth**: None (fully open, no registration required)
**Data Format**: GeoJSON (WFS), PNG/GeoTIFF (WMS), XML (GML)
**Update Frequency**: Aggregated data — yearly or seasonal updates (not real-time AIS)
**License**: Open — EU-funded, free access

## What It Provides

EMODnet Human Activities is an EU-funded data portal that provides processed, aggregated
maritime data derived from AIS vessel tracking and port statistics across European waters.
This is not raw AIS data — it's intelligence derived from AIS: vessel traffic density maps,
shipping route density, and port vessel statistics.

Available data layers (verified via WMS/WFS GetCapabilities):

**Route Density** (WMS raster layers, 45 layer variants):
- `routedensity_allavg` — Average route density, all vessel types
- `routedensity_allseasonal` — Seasonal route density, all vessel types
- Broken down by vessel category (01–05): cargo, tanker, passenger, fishing, other
- Yearly and seasonal variants for each category
- Units: routes per square km per month

**Port Vessels** (WFS feature layers):
- `emodnet:portvessels` — Vessel call counts per port per year
- `emodnet:portvesselsbytonnage` — Port traffic by gross tonnage class
- `emodnet:portvesselsbytype` — Port traffic by vessel type (container, tanker, etc.)

## API Details

### WMS (Map tiles and images):

```
GET https://ows.emodnet-humanactivities.eu/wms
  ?SERVICE=WMS&VERSION=1.3.0
  &REQUEST=GetMap
  &LAYERS=routedensity_allavg
  &CRS=EPSG:4326
  &BBOX=50,-5,55,5
  &WIDTH=256&HEIGHT=256
  &FORMAT=image/png
```

Verified: Returns 200 OK with 33KB PNG image of vessel traffic density for North Sea area.

Supports GetCapabilities, GetMap, GetFeatureInfo, GetLegendGraphic.

### WFS (Vector features — port data):

```
GET https://ows.emodnet-humanactivities.eu/wfs
  ?SERVICE=WFS&VERSION=2.0.0
  &REQUEST=GetFeature
  &TYPENAMES=emodnet:portvessels
  &COUNT=10
  &OUTPUTFORMAT=application/json
```

Verified: Returns GeoJSON with port vessel statistics.

Sample WFS response:
```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {
      "port": "Antwerp-Bruges",
      "port_id": "BE003",
      "portcode": "BE_0BE003",
      "country": "BE",
      "year": 2025,
      "vesseltype": "Container ship",
      "nofvessels": 1214,
      "gross_tonnage__gt_thousand": 71996,
      "dateyear": "2025-01-01Z"
    }
  }]
}
```

No authentication required for any request.

### Available WFS feature types:

| Feature Type | Description |
|---|---|
| `emodnet:portvessels` | Vessel calls per port, year |
| `emodnet:portvesselsbytonnage` | Port traffic by tonnage class |
| `emodnet:portvesselsbytype` | Port traffic by vessel type |

### WMS layer categories:

| Category | Layers | Description |
|---|---|---|
| Route Density (all) | routedensity_allavg, _allseasonal | All vessel types combined |
| Route Density (cargo) | routedensity_01avg, _01seasonal | Cargo vessels |
| Route Density (tanker) | routedensity_02avg, _02seasonal | Tanker vessels |
| Route Density (passenger) | routedensity_03avg, _03seasonal | Passenger vessels |
| Route Density (fishing) | routedensity_04avg, _04seasonal | Fishing vessels |
| Route Density (other) | routedensity_05avg, _05seasonal | Other vessel types |

## Freshness Assessment

Moderate. This is aggregated, processed data — not real-time AIS positions. Route density
maps are derived from historical AIS data, typically updated yearly. Port vessel statistics
are updated as Eurostat publishes new port traffic data (annual cycle with ~6 month lag).

The value proposition is derived intelligence, not freshness: where do ships go, how
intensely is a route used, which ports handle what traffic.

## Entity Model

WFS port data:
- `port` (name), `port_id` (EU port code), `portcode` (composite), `country` (ISO 2-letter)
- `year`, `vesseltype`, `tonnage`, `tonnagesize`
- `nofvessels` (vessel calls), `gross_tonnage__gt_thousand`

WMS route density:
- Raster data (pixel values = route count per km² per month)
- CRS: EPSG:4326

Identifiers: EU port codes, country ISO codes, vessel type classifications.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 1 | Aggregated yearly data, not real-time |
| Openness | 3 | No auth, EU public data |
| Stability | 3 | EU-funded infrastructure, operational since 2013 |
| Structure | 2 | OGC WMS/WFS standards, GeoJSON output, but not simple REST |
| Identifiers | 2 | EU port codes, vessel type categories |
| Additive Value | 2 | Unique vessel density intelligence not available elsewhere |

**Total: 13/18**

## Notes

- This is not a real-time AIS source — it's AIS-derived aggregate intelligence. The value
  is in understanding shipping patterns, route intensities, and port traffic volumes.
- The WMS route density maps are visually stunning and useful for understanding maritime
  traffic patterns. They can serve as contextual layers for real-time AIS data.
- WFS port vessel data includes vessel type breakdowns (container, tanker, bulk, Ro-Ro,
  passenger) and tonnage classes — useful for port traffic analysis.
- EMODnet also provides vessel density raster data (distinct from route density), but these
  appear to be available primarily as downloadable files rather than WMS layers.
- The OGC protocols (WMS/WFS) are standard in the GIS community but less familiar to
  developers used to REST/JSON APIs. Libraries like OpenLayers, Leaflet, and QGIS consume
  these natively.
- Coverage is European seas — Atlantic NE, Baltic, Mediterranean, Black Sea, and parts of
  the Arctic. No global coverage.
