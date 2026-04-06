# AFDC Alternative Fuel Stations (DOE/NREL)

**Country/Region**: United States + Canada
**Publisher**: U.S. Department of Energy / National Renewable Energy Laboratory (NREL)
**API Endpoint**: `https://developer.nrel.gov/api/alt-fuel-stations/v1.json`
**Documentation**: https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/
**Protocol**: REST
**Auth**: API Key (free registration at developer.nrel.gov)
**Data Format**: JSON / CSV / GeoJSON
**Real-Time Status**: Partial — station-level status (Available/Planned/Temporarily Unavailable), not connector-level
**Update Frequency**: Daily (last_updated endpoint confirms same-day updates)
**Station Count**: ~70,000+ EV stations in US (~20,800 in California alone); ~16,700 in Canada; ~124,000 total EV ports
**License**: Public domain (U.S. Government work)

## What It Provides

The Alternative Fuels Data Center (AFDC) Station Locator is the authoritative U.S. government database of alternative fuel stations, maintained by NREL for the Department of Energy. For EV charging, it covers every publicly known station in the United States and Canada — from Level 1 home-style outlets to 350 kW DC fast chargers. The dataset tracks 90+ charging networks (ChargePoint, Tesla, Electrify America, EVgo, Blink, FLO, Shell Recharge, bp pulse, etc.) with detailed connector-level port counts and power ratings.

## API Details

**All Stations:**
```
GET https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={key}&fuel_type=ELEC&state=CA&limit=200
```

**Single Station:**
```
GET https://developer.nrel.gov/api/alt-fuel-stations/v1/{id}.json?api_key={key}
```

**Nearest Stations:**
```
GET https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key={key}&fuel_type=ELEC&latitude=37.7749&longitude=-122.4194&radius=5
```

**Last Updated:**
```
GET https://developer.nrel.gov/api/alt-fuel-stations/v1/last-updated.json?api_key={key}
```
Returns: `{"last_updated":"2026-04-06T07:12:43Z"}` — confirms daily updates.

**EV Networks List:**
```
GET https://developer.nrel.gov/api/alt-fuel-stations/v1/electric-networks.json?api_key={key}
```
Returns all 90+ networks with import dates, import types (API/CSV), and transition info.

Key query parameters:
- `fuel_type=ELEC` — filter to EV charging only
- `ev_network` — filter by network (Tesla, ChargePoint, etc.)
- `ev_connector_type` — J1772, J1772COMBO (CCS), CHADEMO, TESLA (NACS)
- `ev_charging_level` — 1, 2, dc_fast
- `status` — E (Available), P (Planned), T (Temporarily Unavailable)
- `country` — US, CA, or all
- `state` — two-letter state/province code
- `limit` — max 200 per request, or "all" for full dump

Response includes per-station:
- `id`, `station_name`, `street_address`, `city`, `state`, `zip`, `country`
- `latitude`, `longitude`
- `ev_connector_types[]` — array of connector types
- `ev_level1_evse_num`, `ev_level2_evse_num`, `ev_dc_fast_num` — port counts by level
- `ev_network` — network name
- `ev_pricing` — free-text pricing info
- `ev_charging_units[]` — detailed per-unit breakdown with connector types and power (kW)
- `status_code` — E/P/T
- `date_last_confirmed` — verification date
- `updated_at` — last data update timestamp
- `facility_type` — venue type (hotel, restaurant, parking lot, etc.)
- `funding_sources` — NEVI, CFI, etc. government funding programs

Rate limits: 1,000 requests per hour with DEMO_KEY; higher limits with registered key.

## Freshness Assessment

AFDC is updated daily via a combination of direct API imports from major networks (ChargePoint, Blink, Tesla, EVgo, Electrify America, bp pulse, Shell Recharge — all imported via API on the same day) and periodic CSV imports from smaller networks. The `status_code` field provides station-level availability (Available/Planned/Temporarily Unavailable) but not real-time connector-level occupancy. You know if a station exists and is operational, but not if a specific plug is currently in use.

For station registry purposes: excellent, authoritative, daily-fresh. For real-time occupancy: not available — you'd need to query individual network APIs for that.

The `date_last_confirmed` field shows when station data was last verified — many stations show confirmation dates within the past few months.

## Entity Model

- **Station**: A physical location with address, coordinates, operator/network
- **EV Charging Unit**: Groups of ports at a station, broken down by network and charging level
- **Connector**: Type (J1772, CCS, CHAdeMO, NACS/Tesla), power (kW), port count
- **Network**: 90+ networks tracked, each with import metadata
- **Status**: Available (E), Planned (P), Temporarily Unavailable (T)
- **Funding**: Government program linkage (NEVI, CFI, etc.)

Station IDs are numeric, unique across the entire database. Network-specific station IDs can be queried via `ev_network_station_ids`.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily station-level updates; no real-time connector occupancy |
| Openness | 3 | Public domain, free API key, generous rate limits |
| Stability | 3 | U.S. government-operated, versioned API, 10+ years of service |
| Structure | 3 | Rich JSON schema with detailed connector/port/power data |
| Identifiers | 3 | Numeric station IDs, network-specific IDs, cross-references |
| Additive Value | 3 | Definitive US+Canada source; 70K+ stations, 90+ networks, bilingual (EN/FR) |
| **Total** | **17/18** | |

## Notes

- This is the single most important EV charging data source for North America. Every EV app, OEM, and navigation service uses AFDC data either directly or indirectly.
- Covers both US and Canada — NRCan's separate locator draws from the same underlying data.
- The `limit=all` parameter enables full database dumps, but the response is large (~100MB+ for all EV stations). Use geographic or network filters for incremental polling.
- No real-time connector occupancy — for that, individual network APIs (ChargePoint, Tesla, EVgo) would be needed. AFDC provides the authoritative station registry layer.
- The electric networks endpoint is gold for understanding the EV charging landscape — it shows which networks are actively imported via API vs. CSV, and tracks network transitions/mergers.
- EU AFIR equivalent: AFDC is what AFIR aspires to create for Europe — a single national access point with all charging infrastructure data.
