# India NDMA SACHET — Multi-Hazard Early Warning Alerts

**Country/Region**: India
**Publisher**: National Disaster Management Authority (NDMA), Government of India
**API Endpoint**: `https://sachet.ndma.gov.in/cap_public_website/FetchAllAlertDetails`
**Documentation**: https://sachet.ndma.gov.in/ (web portal)
**Protocol**: REST (JSON)
**Auth**: None (anonymous access)
**Data Format**: JSON (CAP-inspired structure)
**Update Frequency**: Real-time (alerts pushed as issued — typically every few minutes during active weather)
**License**: Government of India public data

## What It Provides

SACHET is India's national multi-hazard early warning dissemination system. Think of it as India's equivalent of the US NWS CAP alerts, but covering a country of 1.4 billion people across one of the most disaster-prone geographies on Earth.

The system aggregates alerts from:
- **IMD** (India Meteorological Department) — thunderstorms, cyclones, heat waves, cold waves, heavy rainfall
- **State Disaster Management Authorities (SDMAs)** — 28+ state agencies forwarding localized warnings
- **CWC** (Central Water Commission) — flood alerts
- **INCOIS** — tsunami and ocean warnings
- **GSI** — landslide alerts

Alert types observed in live data: Thunderstorm with Lightning, Thunderstorms with Hail, Avalanche, Heavy Rainfall, Cyclone, Heat Wave, Cold Wave, Flood, and more.

## API Details

The endpoint is beautifully simple — a single GET request returns all currently active alerts:

```
GET https://sachet.ndma.gov.in/cap_public_website/FetchAllAlertDetails
```

No parameters needed. Returns a JSON array of active alerts.

### Probed Response (live, April 7, 2026)

```json
[
  {
    "severity": "WATCH",
    "identifier": 1775511595204027,
    "effective_start_time": "Tue Apr 07 03:08:00 IST 2026",
    "effective_end_time": "Tue Apr 07 06:08:00 IST 2026",
    "disaster_type": "Thunderstorm with Lightning",
    "area_description": "Deoghar, Dumka, Godda, Jamtara districts of Jharkhand",
    "severity_level": "Very Likely",
    "type": 0,
    "actual_lang": "en",
    "warning_message": "Light Thunderstorm and lightning with surface wind(30-40 kmph) accompanied with rain is likely to occur at isolated places over Deoghar, Dumka, Godda, Jamtara in next 3 hours.",
    "disseminated": "false",
    "severity_color": "yellow",
    "alert_id_sdma_autoinc": 112209,
    "centroid": "87.5449146059983,25.070428298102602",
    "alert_source": "IMD Ranchi",
    "area_covered": "10379.38",
    "sender_org_id": "27"
  },
  {
    "severity": "ALERT",
    "identifier": 1775503156914028,
    "effective_start_time": "Tue Apr 07 00:46:00 IST 2026",
    "effective_end_time": "Tue Apr 07 03:46:00 IST 2026",
    "disaster_type": "Thunderstorm with Lightning",
    "area_description": "9 districts of Rajasthan",
    "severity_level": "Very Likely",
    "severity_color": "orange",
    "alert_source": "Rajasthan SDMA",
    "area_covered": "191809.57",
    "sender_org_id": "28"
  }
]
```

At time of probe, **12+ active alerts** were returned covering thunderstorms, hail, and avalanche warnings across multiple states. During monsoon season (June–September) or cyclone events, this endpoint can return dozens of concurrent alerts.

### Key Fields

| Field | Description |
|-------|-------------|
| `identifier` | Unique alert ID (numeric, timestamp-based) |
| `severity` | Alert level: LOW, WATCH, ALERT, WARNING |
| `severity_color` | yellow, orange, red — maps to alert tiers |
| `disaster_type` | Hazard category string |
| `area_description` | Human-readable affected area (districts, states) |
| `centroid` | Geographic centroid of affected area (lon,lat) |
| `area_covered` | Area in sq km |
| `effective_start_time` / `effective_end_time` | Alert validity window |
| `alert_source` | Issuing authority (e.g., "IMD Ranchi", "Rajasthan SDMA") |
| `warning_message` | Full text of the warning |
| `actual_lang` | Language code (en, hi, kn, etc.) — multilingual alerts! |

## Freshness Assessment

Outstanding. Alerts are issued and appear on the API within minutes. The 3-hour validity windows observed in the probe confirm this is a true real-time alerting feed. During active weather, new alerts appear every 15–30 minutes.

## Entity Model

- **Alert**: Identified by `identifier` (unique numeric); has severity, time window, area, source
- **Source Organization**: Identified by `sender_org_id` — maps to NDMA, IMD regional offices, state SDMAs
- **Disaster Type**: Categorical string — no formal taxonomy code, but consistent naming
- **Area**: Described by district names and centroid coordinates — no formal boundary polygons

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time alert issuance; minutes latency |
| Openness | 3 | No auth, no rate limits observed, anonymous access |
| Stability | 2 | Government system operational since ~2019; no versioned API but stable endpoint |
| Structure | 2 | Clean JSON but non-standard date formats; no formal CAP XML |
| Identifiers | 2 | Numeric IDs are unique; area descriptions are text, not geo-codes |
| Additive Value | 3 | Only machine-readable source for Indian disaster alerts; covers 1.4B people |
| **Total** | **15/18** | |

## Integration Notes

- Poll every 5 minutes to catch new alerts promptly
- Dedup by `identifier` field
- The `effective_end_time` indicates when to expire/remove an alert
- Date parsing: format is `"EEE MMM dd HH:mm:ss z yyyy"` (Java SimpleDateFormat)
- Centroid is `lon,lat` (note: longitude first!) — standard for GeoJSON but reversed from Google Maps convention
- Multilingual support: `actual_lang` field includes `en`, `hi` (Hindi), `kn` (Kannada), etc.
- CloudEvents mapping: one event per alert issuance/update; `severity` maps naturally to CloudEvents extension
- Consider pairing with India CPCB data for air quality alerts and IMD for weather context
- During Cyclone Fani (2019), Amphan (2020), or similar events, this becomes a critical data source

## Verdict

This is a hidden gem. No authentication, clean JSON, real-time multi-hazard alerts covering the world's second-most-populous country. The data is genuinely important — India faces monsoons, cyclones, earthquakes, floods, heat waves, and cold waves regularly. The fact that it aggregates alerts from 28+ state agencies and multiple national agencies into a single endpoint makes it exceptionally valuable. Recommended for integration.
