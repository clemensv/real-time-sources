# Ireland EPA Radiation Monitoring GeoServer

**Country/Region**: Ireland
**Publisher**: Environmental Protection Agency (EPA) Ireland
**API Endpoint**: `http://gis.epa.ie/geoserver/EPA/ows`
**Documentation**: `https://www.epa.ie/our-services/monitoring--assessment/radiation/mapmon/`
**Protocol**: OGC WFS 1.0.0 / WMS
**Auth**: None
**Data Format**: GeoJSON, GML, image layers
**Update Frequency**: Current network status is visible; raw numeric dose values were not fully verified in this pass
**License**: Public environmental data; exact license text not verified in this pass

## What It Provides

Ireland's EPA GeoServer exposes a radiation-monitoring layer named
`EPA:RAD_MONITORINGSTATION`. The layer returns station features with coordinates,
station name, monitoring context (for example marine), live/not-live status, and
capability flags for measured media such as gamma dose rate, rainwater, seawater,
seaweed, fish, and shellfish.

This is a useful candidate because it is a real, open, machine-readable national
radiation layer. At the same time, it is not yet a perfect bridge target: the WFS layer
confirmed in this pass looks more like station/status and monitoring-capability data
than a fully verified stream of numeric dose-rate observations.

## API Details

### WFS capabilities

```text
GET http://gis.epa.ie/geoserver/EPA/ows?service=WFS&version=1.0.0&request=GetCapabilities
```

Relevant radiation-related feature type found:

- `EPA:RAD_MONITORINGSTATION` - Radiation Monitoring

### GeoJSON feature request

```text
GET http://gis.epa.ie/geoserver/EPA/ows
  ?service=WFS
  &version=1.0.0
  &request=GetFeature
  &typeName=EPA:RAD_MONITORINGSTATION
  &maxFeatures=50
  &outputFormat=application/json
  &srsName=EPSG:4326
```

Sample feature:

```json
{
  "geometry": {
    "type": "MultiPoint",
    "coordinates": [[-6.1831001, 53.61110048]]
  },
  "properties": {
    "StationName": "Balbriggan",
    "StationPosition": "Marine",
    "StationStatus": "Not Live",
    "GammaDoseRate": null,
    "RainWater": null,
    "Seawater": "Y",
    "URL": "https://www.epa.ie/our-services/monitoring--assessment/radiation/mapmon/"
  }
}
```

Observed examples also included stations such as `Cahirciveen` and `Casement` with
`StationStatus = "Live"` and `GammaDoseRate = "Y"`.

## Freshness Assessment

Confirmed live on 2026-04-08 in the sense that the WFS endpoint responded, station
statuses varied between `Live` and `Not Live`, and the layer carried current network
capability metadata. What is still missing is a cleanly verified path from this WFS layer
to numeric time-series dose-rate values. That uncertainty keeps this below the top tier.

## Entity Model

- **Station** - named monitoring location with coordinates
- **Station Status** - `Live` / `Not Live`
- **Monitoring Capability** - gamma dose rate, rainwater, seawater, seaweed, and other media flags
- **Linked Portal Resource** - EPA map page for further drill-down

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Current station status visible, but raw numeric readings not yet confirmed |
| Openness | 3 | No auth; public GeoServer |
| Stability | 2 | Government GIS service, but only one radiation WFS layer surfaced |
| Structure | 2 | Machine-readable GeoJSON, though apparently more metadata-oriented than time-series oriented |
| Identifiers | 2 | Stable station names and feature ids, but no obvious national station-code contract yet |
| Additive Value | 2 | National Irish radiation network detail outside EURDEP |
| **Total** | **13/18** | |

## Notes

- This came out of the `data.europa.eu` SPARQL sweep, which expanded the dataset to a
  concrete WFS access URL.
- It is a legitimate candidate, but it still needs a second pass to determine whether
  the EPA exposes direct numeric dose-rate observations through another layer, download
  surface, or linked service.
- Even if the numeric path proves awkward, the station metadata is still useful as
  reference data for a broader Irish radiation source.
