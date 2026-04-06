# Nepal BIPAD Portal — Earthquake Catalog & Seismic Monitoring

**Country/Region**: Nepal
**Publisher**: Government of Nepal, National Disaster Risk Reduction and Management Authority (NDRRMA)
**API Endpoint**: `https://bipadportal.gov.np/api/v1/earthquake/`
**Documentation**: https://bipadportal.gov.np/ (disaster information portal)
**Protocol**: REST (JSON with GeoJSON geometry)
**Auth**: None (anonymous access)
**Data Format**: JSON
**Update Frequency**: Historical catalog; new events added as reported by NSC (National Seismological Centre)
**License**: Nepal government open data

## What It Provides

Nepal sits on the Himalayan collision zone — one of the most seismically active regions on Earth. The 2015 Gorkha earthquake (M7.8) killed nearly 9,000 people and demonstrated the catastrophic potential of this region. The BIPAD portal provides an earthquake catalog sourced from the National Seismological Centre (NSC).

Each earthquake record includes:
- **Magnitude**: Event magnitude (e.g., M4.3)
- **Location**: GeoJSON Point geometry (longitude, latitude)
- **Address**: District/location description
- **Event time**: ISO 8601 timestamp with Nepal Time (UTC+05:45)
- **Administrative codes**: Ward, municipality, district, province

### Probe Results (live, April 2026)

```json
{
  "count": 9223372036854775807,
  "next": "...?limit=3&offset=3",
  "results": [
    {
      "id": 698,
      "description": "NSC",
      "point": {"type": "Point", "coordinates": [86.04, 27.68]},
      "magnitude": 4.3,
      "address": "Dolakha",
      "eventOn": "2015-05-12T19:31:00+05:45",
      "ward": 530,
      "municipality": 22002,
      "district": 22,
      "province": 3
    }
  ]
}
```

The catalog appears to contain primarily historical events with magnitudes ≥4.0, sourced from the NSC. New significant events are added to the catalog over time.

## API Details

Standard Django REST Framework pagination:

```
GET https://bipadportal.gov.np/api/v1/earthquake/?format=json&limit=100&offset=0
```

The API supports pagination via `limit` and `offset`. The `count` field returns max long (API quirk — same as the river station endpoint).

## Freshness Assessment

This endpoint appears to be a historical earthquake catalog rather than a real-time feed. The events probed were from 2010-2015. For true real-time seismic monitoring, the USGS and EMSC global feeds cover Nepal's seismic events. However, the BIPAD catalog provides local detail (ward, municipality, district) not available in global catalogs.

## Entity Model

- **Earthquake**: ID, magnitude, location (GeoJSON), event time, source (NSC)
- **Administrative**: Province → district → municipality → ward hierarchy
- **Source**: NSC (National Seismological Centre)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Historical catalog; new events added with delay |
| Openness | 3 | No auth; anonymous access; clean REST API |
| Stability | 2 | Government portal; Django REST Framework |
| Structure | 3 | Clean JSON with GeoJSON geometry |
| Identifiers | 2 | Numeric IDs; administrative codes; GeoJSON coordinates |
| Additive Value | 2 | Local administrative detail unique; Himalayan seismic zone; but global feeds cover Nepal |
| **Total** | **13/18** | |

## Integration Notes

- More useful as a supplementary catalog than a real-time source
- The administrative detail (ward/municipality/district) is unique and valuable for impact assessment
- Combine with USGS/EMSC real-time feeds for live detection + local detail enrichment
- The river station endpoint at `/api/v1/river-stations/` is the stronger real-time offering from this portal
- CloudEvents: batch event for new catalog entries; or enrichment events linking global earthquake IDs to local admin areas

## Verdict

Useful supplementary source rather than a primary real-time feed. The earthquake catalog provides Nepal-specific administrative detail that global sources lack. The real value of the BIPAD portal for this project is the river station monitoring endpoint (see nepal-bipad-hydrology.md). The earthquake catalog is documented here for completeness and potential enrichment use cases.
