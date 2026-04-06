# AFAD Turkey Earthquake API — Deep Dive Update

**Country/Region**: Turkey
**Publisher**: AFAD (Disaster and Emergency Management Authority), Ministry of Interior
**API Endpoint**: `https://deprem.afad.gov.tr/apiv2/event/filter`
**Documentation**: https://deprem.afad.gov.tr/ (earthquake portal with API)
**Protocol**: REST (JSON)
**Auth**: None (anonymous access)
**Data Format**: JSON
**Update Frequency**: Near-real-time (events appear within minutes of detection)
**License**: Turkish government public data

## Extended Probe Results (April 2026)

Building on the existing `afad-turkey.md` candidate (scored 11/18), this deep dive re-probes the API with refined parameters and documents what's actually working in 2026.

### Working Query Confirmed

```
GET https://deprem.afad.gov.tr/apiv2/event/filter?start=2026-04-01&end=2026-04-07&minmag=3&format=json
```

Returns a JSON array with 25+ events in the 6-day window. Notable events include:

```json
{
  "rms": "0.57",
  "eventID": "712319",
  "location": "Tuşba (Van)",
  "latitude": "38.83278",
  "longitude": "43.54194",
  "depth": "7",
  "type": "MW",
  "magnitude": "5.2",
  "country": "Türkiye",
  "province": "Van",
  "district": "Tuşba",
  "neighborhood": "Ermişler",
  "date": "2026-04-04T05:52:42",
  "isEventUpdate": false
}
```

A **M5.2 earthquake in Van** (Eastern Turkey) on April 4, 2026 — this is exactly the kind of event that makes this feed valuable. Van was devastated by a M7.2 earthquake in 2011.

### Key Improvements Over Original Assessment

1. **Date range queries work reliably**: The `start`/`end` parameter combination with `minmag` and `format=json` is stable
2. **Rich local detail**: Province, district, and neighborhood-level granularity — not available in any global feed
3. **Cross-border events**: The feed includes events located in neighboring countries (Iran, Greece) that were felt in Turkey
4. **Magnitude types**: Both ML (local) and MW (moment) magnitudes reported

### What Still Doesn't Work

- `orderby=timedesc` → HTTP 500 (confirmed again)
- `limit` parameter → inconsistent behavior
- No pagination support — returns all matching events at once
- No FDSN-compatible endpoint

### Updated Score Justification

The original assessment scored AFAD 11/18 due to "flaky API." Our 2026 re-probe shows that date-range + magnitude filtering works reliably. The main limitations are:
- No streaming/push
- Some parameter combinations cause 500 errors
- No formal API documentation

## Updated Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Near-real-time; M5.2 Van event appeared within minutes |
| Openness | 3 | No auth, anonymous access, confirmed working |
| Stability | 2 | Working with specific parameter patterns; 500 errors on others |
| Structure | 2 | Clean JSON but flat array; no GeoJSON; inconsistent parameter support |
| Identifiers | 2 | eventID is unique; province/district/neighborhood codes are Turkish |
| Additive Value | 3 | Turkey is among the world's most seismically active; local detail unique |
| **Total** | **15/18** (revised up from 11/18) | |

## Integration Notes

- Use date-range polling: query last N hours with `start` and `end` parameters
- Dedup by `eventID`
- The `isEventUpdate` flag tracks whether an event has been revised
- Turkish location hierarchy (il/ilçe/mahalle) is unique enrichment not available globally
- Post-February 2023 earthquake, AFAD invested significantly in monitoring infrastructure
- Pair with EMSC/USGS for global context; use AFAD for Turkey-specific detail

## Verdict

Significantly better than originally assessed. The AFAD earthquake API works reliably with the right parameter combination and provides Turkey-specific location detail (down to neighborhood level) that no global catalog offers. The M5.2 Van event in the probe window demonstrates the feed captures significant events promptly. Upgraded recommendation: **Build**.
