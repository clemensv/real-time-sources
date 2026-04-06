# African METAR Stations via AviationWeather.gov

- **Country/Region**: Pan-African (all ICAO-reporting airports across the continent)
- **Endpoint**: `https://aviationweather.gov/api/data/metar?ids=FAOR,HKJK,DNMM,GMMN,HECA,HTDA&format=json`
- **Protocol**: REST
- **Auth**: None
- **Format**: JSON, GeoJSON, CSV, XML, IWXXM
- **Freshness**: Real-time (METAR issued every 30–60 min per station, API cache updates every 1 min)
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 16/18

## Overview

Africa has hundreds of ICAO-reporting weather stations at airports, and every single one
reports METARs through the WMO Global Telecommunication System. AviationWeather.gov
provides free, unauthenticated access to all of them. This is arguably the best real-time
weather data source for the African continent — certainly the most reliable and
standardized.

Key African ICAO stations probed and verified:

| ICAO | Airport | Country | Verified |
|------|---------|---------|----------|
| FAOR | OR Tambo International, Johannesburg | South Africa | ✅ 14°C, 180°/8kt |
| HKJK | Jomo Kenyatta International, Nairobi | Kenya | ✅ 19°C, 070°/9kt |
| DNMM | Murtala Muhammed International, Lagos | Nigeria | ✅ 29°C, 180°/5kt |
| GMMN | Mohammed V International, Casablanca | Morocco | ✅ 18°C, 130°/8kt |
| HECA | Cairo International | Egypt | ❌ Not returned (may be temporarily offline) |
| HTDA | Julius Nyerere International, Dar es Salaam | Tanzania | ❌ Not returned |

Four out of six major African airports returned live data. Coverage extends to hundreds
more stations — virtually every commercial airport on the continent.

## Endpoint Analysis

Request for African stations:
```
GET https://aviationweather.gov/api/data/metar?ids=FAOR,HKJK,DNMM,GMMN&format=json
```

Sample response (Nairobi):
```json
{
  "icaoId": "HKJK",
  "receiptTime": "2026-04-06T21:58:00.824Z",
  "temp": 19,
  "dewp": 16,
  "wdir": 70,
  "wspd": 9,
  "visib": "6+",
  "altim": 1024,
  "fltCat": "MVFR",
  "rawOb": "METAR HKJK 062130Z 07009KT 9999 BKN020 19/16 Q1024 NOSIG",
  "lat": -1.319,
  "lon": 36.928,
  "elev": 1615,
  "name": "Nairobi/Kenyatta Intl, NA, KE"
}
```

Also available as GeoJSON for spatial overlay, and bulk cache files updated every minute.

## Integration Notes

This is the single most impactful "Africa weather" bridge to build:

- **Station discovery**: Use the `/stationinfo` endpoint to enumerate all African stations
  by bounding box: `bbox=-20,-35,55,37`.
- **Bulk approach**: The cache file `/data/cache/metars.cache.csv.gz` contains ALL global
  METARs; filter by latitude/longitude for African stations.
- **Event model**: Emit a CloudEvent per station per METAR observation, keyed on ICAO code.
- **TAF complement**: TAFs provide 24-hour forecasts for the same stations — a companion
  bridge could emit forecast events.
- **Coverage gaps**: Some smaller African airports may have intermittent reporting.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Minute-level cache updates, METAR every 30–60 min |
| Openness | 3 | No auth, US government public domain |
| Stability | 3 | NOAA infrastructure, operational for decades |
| Structure | 3 | JSON/GeoJSON, OpenAPI spec available |
| Identifiers | 3 | ICAO codes are the gold standard |
| Richness | 1 | Weather only (but standardized and comprehensive) |
