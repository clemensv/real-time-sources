# Madrid Real-Time Traffic (Informo)

**Country/Region**: Spain — Madrid
**Publisher**: Ayuntamiento de Madrid (Madrid City Council)
**API Endpoint**: `https://informo.madrid.es/informo/tmadrid/pm.xml`
**Documentation**: https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=33cb30c367e78410VgnVCM1000000b205a0aRCRD
**Protocol**: REST
**Auth**: None
**Data Format**: XML
**Update Frequency**: Every 5 minutes
**License**: CC BY 4.0

## What It Provides

Real-time traffic sensor data from measurement points across Madrid's road network. Each sensor reports traffic intensity (vehicles/hour), road occupancy percentage, load, and a service level indicator (free flow through severe congestion). This is raw traffic flow data from induction loops and other sensors — a rare find as a fully open, no-auth XML feed.

## API Details

```
GET https://informo.madrid.es/informo/tmadrid/pm.xml
```

Returns XML with all active traffic measurement points:
```xml
<pm>
  <codigo>3400</codigo>
  <descripcion>Pl. Cibeles - C. Alcalá (E-O)</descripcion>
  <tipo_elem>M30</tipo_elem>
  <intensidad>1860</intensidad>
  <ocupacion>12</ocupacion>
  <carga>35</carga>
  <nivelServicio>1</nivelServicio>
  <intensidadSat>5400</intensidadSat>
  <error>N</error>
  <subarea>301</subarea>
  <st_x>-3.6933</st_x>
  <st_y>40.4195</st_y>
</pm>
```

Key fields:
- `codigo` — Sensor ID
- `descripcion` — Road segment description (street, direction, between intersections)
- `intensidad` — Traffic intensity (vehicles/hour)
- `ocupacion` — Road occupancy percentage (0-100)
- `carga` — Load percentage
- `nivelServicio` — Service level: 0 (free flow), 1 (moderate), 2 (congested), 3 (severe congestion)
- `intensidadSat` — Saturation intensity (theoretical capacity)
- `error` — Sensor error flag (N = normal, Y = error)
- `subarea` — Traffic management zone
- `st_x`, `st_y` — Coordinates (ETRS89 / WGS84)

**Historical data also available:**
```
https://datos.madrid.es/dataset/208627-0-transporte-ptomedida-historico
```

Hourly archives dating back to 2013 in CSV format.

## Freshness Assessment

Updated every 5 minutes. The `error` flag indicates sensor health — sensors reporting `Y` should be excluded. The `nivelServicio` field provides an immediate congestion classification without needing to compute it from raw intensity. The feed includes hundreds of measurement points across Madrid's major roads and the M-30 ring road.

## Entity Model

- **Measurement Point**: Sensor with ID, description, coordinates, traffic zone
- **Traffic Flow**: Intensity (veh/h), occupancy (%), load (%), saturation intensity
- **Service Level**: Congestion classification (0-3)
- **Sensor Health**: Error flag

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute updates, real-time |
| Openness | 3 | No auth, CC BY 4.0 |
| Stability | 3 | City-operated since at least 2013 |
| Structure | 2 | XML (not JSON), but well-structured and consistent |
| Identifiers | 3 | Unique sensor codes, subarea zones, coordinates |
| Additive Value | 3 | Only open real-time traffic flow API found in Spain; rare raw sensor data |
| **Total** | **17/18** | |

## Notes

- Madrid is the only Spanish city with a confirmed open real-time traffic API. The national DGT (Dirección General de Tráfico) provides only a web map (etraffic) with no documented REST API.
- The XML format requires parsing but is simple and consistent. Each `<pm>` element is a self-contained measurement point.
- The `nivelServicio` (service level) is pre-computed by Madrid's traffic management center — a useful enrichment beyond raw speed/flow data.
- Historical data back to 2013 enables pattern analysis and anomaly detection.
- UTM coordinates in the feed are actually WGS84-compatible (ETRS89, which is equivalent for practical purposes).
