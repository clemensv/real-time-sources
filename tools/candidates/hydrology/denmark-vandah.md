# Denmark Miljoeportalen VANDaH Hydrometry API

**Country/Region**: Denmark
**Publisher**: Danmarks Miljoeportal / VANDaH
**API Endpoint**: `https://vandah.miljoeportal.dk/api/`
**Documentation**: `https://vandah.miljoeportal.dk/api/swagger/index.html`
**Protocol**: REST JSON (OpenAPI-described)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Current results plus queryable historical ranges
**License**: Public API; exact license text not verified in this pass

## What It Provides

VANDaH is a proper Danish hydrometry API. It exposes station metadata plus water-level
and water-flow results through a documented REST surface. That matters because the
earlier Denmark candidate work found only DMI meteorological observations, which were
useful but not actually hydrology-specific.

The API is built around stable station identifiers and returns structured measurement
records with timestamps, units, parameter names, and result values. This is much closer
to the repo's normal river and gauge sources than the DMI met-observation fallback.

## API Details

### Base endpoints

- `GET /stations` - list stations
- `GET /water-levels` - current water-level results for a station and date range
- `GET /water-flows` - current water-flow results for a station and date range
- `GET /measurements/results/current` - generic current-result surface

### Station example

`GET https://vandah.miljoeportal.dk/api/stations`

Sample fields:

```json
{
  "stationUid": "bf0a311a-7d17-4dd6-a008-c65866195529",
  "stationId": "70000590",
  "operatorStationId": "WATSONC-11521",
  "locationType": "Vandlob",
  "stationOwnerName": "Aalborg Kommune"
}
```

### Water-level example

`GET https://vandah.miljoeportal.dk/api/water-levels?stationId=70000590&from=2026-04-06&to=2026-04-08`

Sample fields:

```json
{
  "stationId": "70000590",
  "operatorStationId": "WATSONC-11521",
  "results": [
    {
      "measurementPointNumber": 1,
      "parameter": "Vandstand",
      "measurementDateTime": "2026-04-08T00:00:00Z",
      "result": 236,
      "resultElevationCorrected": 236,
      "unit": "cm"
    }
  ]
}
```

### Query parameters

- `stationId`
- `operatorStationId`
- `measurementPointNumber`
- `from`
- `to`
- `createdAfter`
- `format`

## Freshness Assessment

Confirmed live on 2026-04-08. The swagger document was public, `GET /stations`
returned data without authentication, and `GET /water-levels` returned measurements
dated 2026-04-08. That is enough to treat this as a real current-data hydrometry API,
not just a catalog stub.

## Entity Model

- **Station** - stable `stationId`, operator station id, owner, location type
- **Measurement Point** - numbered point at a station
- **Water Level Result** - timestamped level value, corrected value, unit
- **Water Flow Result** - timestamped discharge or flow value, unit

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 3 | Clean REST API with public OpenAPI description |
| Data Richness | 3 | Stations, water levels, water flows, current-result surfaces |
| Freshness | 2 | Current results confirmed; cadence not fully documented in this pass |
| Station Coverage | 2 | National system, but full gauge count not confirmed yet |
| Documentation | 3 | Swagger is public and explicit |
| License/Access | 3 | No auth required |
| **Total** | **16/18** | |

## Notes

- This closes the Denmark hydrology gap more convincingly than the earlier DMI
  meteorological observation candidate.
- The portal was surfaced through `data.europa.eu` under the dataset title
  `Hydrometri og grundvand`, then confirmed directly against the live API.
- The presence of stable station identifiers and explicit units makes this a good fit
  for the repository's normal reference-data-plus-measurement model.
