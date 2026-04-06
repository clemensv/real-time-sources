# Ghent Parking (Stad Gent)

**Country/Region**: Belgium — Ghent
**Publisher**: Stad Gent / Mobiliteitsbedrijf Gent
**API Endpoint**: `https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records`
**Documentation**: https://data.stad.gent/explore/dataset/bezetting-parkeergarages-real-time/
**Protocol**: REST (Opendatasoft API)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (every ~1 minute)
**License**: Open Data Ghent (Modellicentie Gratis Hergebruik)

## What It Provides

Real-time parking garage occupancy for the city of Ghent, Belgium. Provides current available capacity, total capacity, and occupancy percentage for 13 parking garages across the city center. Includes opening hours, operator information, temporary closure status, and occupancy trend.

## API Details

```
GET https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records?limit=100
```

Returns Opendatasoft records:
```json
{
  "total_count": 13,
  "results": [
    {
      "name": "Sint-Michiels",
      "lastupdate": "2026-04-06T12:21:57+02:00",
      "totalcapacity": 452,
      "availablecapacity": 222,
      "occupation": 50,
      "type": "carPark",
      "description": "Ondergrondse parkeergarage Sint-Michiels in Gent",
      "openingtimesdescription": "24/7",
      "isopennow": 1,
      "temporaryclosed": 0,
      "operatorinformation": "Mobiliteitsbedrijf Gent",
      "freeparking": 0,
      "occupancytrend": "unknown",
      "location": {"lon": 3.719727, "lat": 51.053110},
      "categorie": "parking in LEZ"
    }
  ]
}
```

The Opendatasoft API supports:
- Pagination (`limit`, `offset`)
- Filtering (`where` parameter with SQL-like syntax)
- Geo-distance queries
- Multiple export formats (JSON, CSV, GeoJSON)

## Freshness Assessment

The `lastupdate` field shows timestamps within the last minute of current time. Data comes from the city's live parking guidance system. Updates are continuous as vehicles enter and exit garages. The `occupancytrend` field (filling/emptying/stable/unknown) confirms real-time tracking. Excellent freshness.

## Entity Model

- **Parking Garage**: 13 garages with name, description, operator, capacity
- **Availability**: Total capacity, available capacity, occupation percentage
- **Status**: Open now, temporarily closed, free parking flags
- **Trend**: Occupancy trend (filling, emptying, stable, unknown)
- **Classification**: Type (carPark), category (parking in LEZ — Low Emission Zone)
- **Location**: WGS84 coordinates

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time with per-minute timestamps |
| Openness | 3 | No auth, open data license, Opendatasoft API |
| Stability | 3 | City-operated on Opendatasoft platform — well-established |
| Structure | 3 | Clean JSON, consistent schema, rich metadata |
| Identifiers | 2 | Name-based identification; URLs as IDs (not ideal) |
| Additive Value | 2 | Good Belgian city example; Opendatasoft pattern reusable across many cities |
| **Total** | **16/18** | |

## Notes

- Ghent uses Opendatasoft, which is used by hundreds of European cities. Building an ingestion pattern for Opendatasoft parking data means potential reuse across many cities (Paris, Bordeaux, Nantes, etc.).
- The LEZ (Low Emission Zone) categorization is a useful enrichment — shows which garages are inside the emission zone.
- Only 13 garages — small dataset but very clean and well-structured. Good for a proof-of-concept.
- Ghent also publishes P+R (Park and Ride) data on the same platform.
