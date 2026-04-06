# Cologne Parking (Stadt Köln)

**Country/Region**: Germany — Cologne (Köln)
**Publisher**: Stadt Köln (City of Cologne)
**API Endpoint**: `https://www.stadt-koeln.de/externe-dienste/open-data/parking.php`
**Documentation**: https://offenedaten-koeln.de/dataset/parkhausbelegung
**Protocol**: REST (ArcGIS-compatible JSON)
**Auth**: None
**Data Format**: JSON (Esri Feature format)
**Update Frequency**: Real-time (parking guidance system updates)
**License**: Open Data Köln

## What It Provides

Real-time parking garage occupancy for Cologne's city center and event venues. Returns current capacity and occupancy trend for ~30 parking facilities including city center garages, LANXESS arena parking, and stadium event parking. Includes geographic coordinates for each facility.

## API Details

```
GET https://www.stadt-koeln.de/externe-dienste/open-data/parking.php
```

Returns Esri Feature JSON:
```json
{
  "displayFieldName": "IDENTIFIER",
  "geometryType": "esriGeometryPoint",
  "spatialReference": {"wkid": 4258},
  "features": [
    {
      "attributes": {
        "identifier": "PH04",
        "parkhaus": "Brückenstraße",
        "kapazitaet": 466,
        "tendenz": 1
      },
      "geometry": {"x": 6.955, "y": 50.937}
    }
  ]
}
```

Fields:
- `identifier` — garage code (e.g., PH04, D_P001, W_P008W)
- `parkhaus` — garage name
- `kapazitaet` — current available spaces (-1 = no data / closed)
- `tendenz` — trend indicator (0 = stable, 1 = filling, 2 = emptying, -1 = no data)
- `geometry` — WGS84 point coordinates

There's also a timestamped variant:
```
GET https://www.stadt-koeln.de/externe-dienste/open-data/parking-ts.php
```

## Freshness Assessment

Data reflects the city's live parking guidance system. Updates are continuous — the parking guidance displays in the city update in real-time, and this API mirrors that data. Trend indicators (filling/emptying/stable) confirm real-time tracking. `-1` values indicate facilities that are closed or not reporting.

## Entity Model

- **Parking Facility**: Identified by code (PH01–PH34, D_P001–D_P006, W_P001–W_P008)
- **Capacity**: Available spaces (real-time)
- **Trend**: Directional indicator
- **Location**: WGS84 coordinates
- **Types**: City garages (PH*), LANXESS arena (D_P*), Stadium (W_P*)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time parking guidance data |
| Openness | 3 | No auth, open data license |
| Stability | 2 | City-operated; format may change without notice |
| Structure | 2 | Esri Feature format — parseable but non-standard for this domain |
| Identifiers | 2 | Local codes (PH04, etc.) — no standard identifiers |
| Additive Value | 1 | Already covered by ParkAPI aggregator |
| **Total** | **13/18** | |

## Notes

- Cologne is already available through ParkAPI (`Koeln` city). Using ParkAPI is likely more efficient than building a standalone bridge.
- The Esri Feature format is unusual for parking data — it's clearly exposed from the city's GIS system rather than being a purpose-built parking API.
- Event parking facilities (Stadium, LANXESS arena) show `-1` when not active, which is useful for event detection.
- Worth keeping as a test case for the ParkAPI aggregator, but not a high-priority standalone candidate.
