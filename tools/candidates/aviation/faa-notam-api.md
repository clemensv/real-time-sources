# FAA NOTAM API

**Country/Region**: United States (global NOTAMs available via ICAO feed)
**Publisher**: Federal Aviation Administration (FAA)
**API Endpoint**: `https://external-api.faa.gov/notamapi/v1/notams`
**Documentation**: https://notams.aim.faa.gov/notamSearch/ (user-facing), API docs via developer portal
**Protocol**: REST
**Auth**: API Key (free registration required)
**Data Format**: JSON
**Update Frequency**: Real-time (NOTAMs published as issued)
**License**: US Government public domain

## What It Provides

Digital NOTAMs (Notices to Air Missions) provide critical real-time information about
temporary or permanent changes to the National Airspace System. This includes:

- **Airspace restrictions**: TFRs (Temporary Flight Restrictions), special use airspace activation
- **Airport operational changes**: Runway closures, taxiway closures, lighting outages
- **Navigation aid status**: VOR/DME/ILS outages, GPS interference areas
- **Obstructions**: New obstacles, crane operations near airports
- **Airshow/event notices**: Parachute operations, aerobatic activities
- **Security**: Presidential TFRs, disaster area restrictions
- **International NOTAMs**: Available for non-US locations via ICAO data feed

## API Details

The NOTAM API endpoint was confirmed reachable (returns 401 without API key, confirming
the endpoint exists and requires authentication).

Endpoint: `GET https://external-api.faa.gov/notamapi/v1/notams`

Query parameters (based on published documentation):
- `domesticLocation` — US airport or facility identifier
- `icaoLocation` — ICAO location identifier
- `notamType` — Filter by NOTAM type (N, R, C, etc.)
- `sortBy` — Sort field (icaoLocation, etc.)
- `sortOrder` — Asc/Desc
- `pageSize` — Results per page
- `pageNum` — Page number

Authentication: API key via registration at the FAA developer portal. Registration is free
and typically approved quickly.

Response format: JSON with NOTAM records containing:
- NOTAM ID and series
- Location (ICAO/domestic code)
- Effective date/time and expiration
- NOTAM text (traditional format and parsed fields)
- Classification and category
- Affected facilities/runways
- Geographic coordinates (for applicable NOTAMs)

## Freshness Assessment

Real-time. NOTAMs are published to the API as they are issued. TFRs and urgent NOTAMs
appear within minutes of issuance. The data is authoritative — this is the same NOTAM
system used by airline dispatchers and general aviation pilots.

Endpoint confirmed reachable (401 response without API key). Could not verify response
payload without registered API key.

## Entity Model

- **NOTAM**: notamId, series, type, location (domestic + ICAO), effectiveStart, effectiveEnd,
  text, classification, category, schedule, affectedFacilities, coordinates
- **Location**: domesticLocation, icaoLocation
- **TFR**: type R (restriction), geographic area, altitude limits, effective period

Identifiers: NOTAM ID, ICAO location codes, domestic facility IDs.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time NOTAM publication |
| Openness | 2 | Free API key registration required |
| Stability | 3 | FAA official infrastructure |
| Structure | 2 | JSON, but NOTAM text is still semi-structured legacy format |
| Identifiers | 3 | ICAO codes, NOTAM IDs, facility codes |
| Additive Value | 3 | Unique data type — airspace restrictions and operational changes |

**Total: 16/18**

## Notes

- NOTAMs are a uniquely valuable data type that no other source provides. They represent
  real-time changes to the operational aviation environment: runway closures, TFRs, airspace
  restrictions, nav aid outages.
- The traditional NOTAM text format is notoriously cryptic (abbreviated English with many
  contractions). The JSON API provides some parsed fields but the raw text is often still
  needed for full context.
- Combining NOTAM data with flight tracking (OpenSky/ADS-B Exchange) and weather
  (AviationWeather.gov) creates a comprehensive aviation situation awareness picture.
- EUROCONTROL's European AIS Database (EAD) provides similar NOTAM data for European
  airspace, but access requires organizational registration through a National AIS authority.
- ICAO also operates a NOTAM API (`applications.icao.int/dataservices/`), but it returned
  403 Forbidden during probing — likely requires ICAO membership or paid access.
- For international NOTAMs, the FAA API may include ICAO-distributed NOTAMs, but coverage
  of non-US NOTAMs should be verified after obtaining an API key.
