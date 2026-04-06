# Thailand National Hydroinformatics (Thaiwater)

**Country/Region**: Thailand
**Publisher**: Hydro-Agro Informatics Institute (HAII) / National Hydroinformatics Data Center
**API Endpoint**: `https://api-v3.thaiwater.net/api/v1/thaiwater30/public/waterlevel_load`
**Documentation**: https://www.thaiwater.net/ (portal; no formal API docs published)
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly (water levels), Daily (dam data)
**Station Count**: 1000+ telemetric water level stations, 35+ major dams
**License**: Thai government open data (implied public access)

## What It Provides

Comprehensive real-time water monitoring for all of Thailand:
- **Water levels** at telemetric stations across all 25 major river basins
- **River discharge** measurements
- **Dam storage** levels, inflow, outflow, and capacity percentages
- **Flood situation levels** (1-5 severity scale)
- **Bank overflow calculations** (distance above/below bank level)

## API Details

### Real-time water level data
```
GET https://api-v3.thaiwater.net/api/v1/thaiwater30/public/waterlevel_load
```
Returns nested JSON with `waterlevel_data.data[]` array. Each entry contains:
- `waterlevel_datetime` — timestamp
- `waterlevel_msl` — water level above mean sea level
- `discharge` — river discharge (m³/s)
- `storage_percent` — storage percentage
- `situation_level` — flood severity (1-5)
- `station` — nested object with name (Thai/English), lat/lon, old code, warning levels, bank heights
- `agency` — data provider agency (RID, EGAT, etc.)
- `basin` — river basin (Thai/English)
- `geocode` — province/district/subdistrict (Thai/English)
- `diff_wl_bank` — distance from bank level
- `river_name` — river name

### Dam daily data
```
GET https://api-v3.thaiwater.net/api/v1/thaiwater30/public/thailand
```
Returns dam storage, inflow, outflow, capacity, accumulated rainfall, etc.

### Example response (water level, truncated)
```json
{
  "waterlevel_data": {
    "result": "OK",
    "data": [{
      "waterlevel_datetime": "2026-04-06 17:00",
      "waterlevel_msl": "330.49",
      "discharge": "1.80",
      "storage_percent": "99.01",
      "situation_level": 4,
      "station": {
        "tele_station_name": {"th": "...", "en": "Khwae Yai Bridge"},
        "tele_station_lat": 16.05,
        "tele_station_long": 99.51,
        "left_bank": 663.26, "right_bank": 663.58,
        "warning_level_m": null, "critical_level_msl": null
      },
      "basin": {"basin_name": {"en": "Mae Klong Basin"}},
      "geocode": {"province_name": {"en": "Nakhon Ratchasima"}},
      "diff_wl_bank": "3.31",
      "river_name": "ลำโดมน้อย"
    }]
  }
}
```

## Freshness Assessment

- Water level data is updated hourly — confirmed with timestamps from the current day
- Dam data updated daily
- Situation levels (flood warnings) are actively maintained
- Multiple agencies contribute data (RID, EGAT, FOP, etc.)

## Entity Model

- **Station**: id, name (Thai/English/Japanese), lat/lon, old code, station type, bank heights, warning levels, agency, basin, geocode
- **Observation**: datetime, water level (MSL), discharge, storage percent, situation level
- **Dam**: id, name (multilingual), lat/lon, max/normal/uses storage, agency, basin
- **Dam observation**: date, storage, inflow, outflow, rainfall accumulation
- **Basin**: id, code, name (Thai/English)
- **Agency**: id, name, shortname (Thai/English/Japanese)
- **Geocode**: area, province, amphoe (district), tumbon (subdistrict)

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 3 | Clean JSON, no auth, single-request bulk data |
| Data Richness | 3 | Water level, discharge, dam storage, flood severity, bank overflow |
| Freshness | 3 | Hourly water levels, daily dam data, confirmed current |
| Station Coverage | 3 | 1000+ stations, 35+ dams, all 25 Thai river basins |
| Documentation | 1 | No public API documentation; endpoint discovered via SPA source |
| License/Access | 2 | Public access, no auth, but no explicit license statement |
| **Total** | **15/18** | |

## Notes

- Bilingual data (Thai + English) for station names, basins, provinces — reduces localization burden
- Japanese translations also available for some fields (dam names, agency names)
- Flood situation levels (1-5) provide built-in severity classification
- Bank overflow calculation (`diff_wl_bank`) gives immediate flood risk assessment
- Multiple contributing agencies (Royal Irrigation Department, EGAT, etc.) ensure broad coverage
- The `waterlevel_load` endpoint returns all stations with critical/elevated water levels in a single request — ideal for change-driven polling
- API version (v3) suggests maturity
- River names are predominantly in Thai script; English basin names are available
