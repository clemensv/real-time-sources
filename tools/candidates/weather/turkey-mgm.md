# Turkey MGM (Turkish State Meteorological Service) — Weather Observations

**Country/Region**: Turkey
**Publisher**: Turkish State Meteorological Service (Meteoroloji Genel Müdürlüğü — MGM)
**API Endpoint**: `https://servis.mgm.gov.tr/web/sondurumlar` (current conditions service)
**Documentation**: https://www.mgm.gov.tr/eng/ (English portal), https://servis.mgm.gov.tr/ (API documentation — Turkish)
**Protocol**: REST (JSON)
**Auth**: API Key (free registration at servis.mgm.gov.tr)
**Data Format**: JSON
**Update Frequency**: Hourly to 3-hourly observations; sub-hourly for select stations
**License**: Turkish government open data

## What It Provides

MGM operates Turkey's national meteorological observation network — approximately 400+ stations across one of the most geographically diverse countries in Europe/Asia. Turkey's position makes it meteorologically fascinating: Mediterranean coast, Black Sea coast, continental Anatolian plateau, and semi-arid southeast.

The API provides:
- **Current conditions** (sondurumlar): Latest observations from all stations
- **Forecasts** (tahmin): 5-day city forecasts
- **Warnings** (uyarılar): Severe weather warnings
- **Historical data**: Past observations

Station parameters include temperature, humidity, wind speed/direction, pressure, precipitation, visibility, and weather codes.

## API Details

The service API at `servis.mgm.gov.tr` provides JSON REST endpoints:

```
# Current conditions for a station
GET https://servis.mgm.gov.tr/web/sondurumlar?merkezid={station_id}

# All current conditions
GET https://servis.mgm.gov.tr/web/sondurumlar

# 5-day forecast
GET https://servis.mgm.gov.tr/web/tahminler/gunluk?merkezid={station_id}
```

### Probe Results

The endpoint `https://servis.mgm.gov.tr/web/sondurumlar?merkezid=90601` returned **HTTP 500** during testing. This is consistent with reports that the service API requires authentication via an API key obtained through registration at the MGM developer portal. Without the key, the server errors rather than returning a 401/403.

### MGM Website Confirmed Working

The public-facing website at `mgm.gov.tr` loads current conditions and forecasts via client-side rendering. The forecast page for Ankara shows:
- Current temperature observations
- 5-day forecasts
- Historical climate normals
- Extremes (max/min temperatures)
- Precipitation and wind records

## Freshness Assessment

MGM is Turkey's national meteorological authority with a well-established observation network. Hourly synoptic observations from ~400 stations are standard. However, the API's current HTTP 500 response for unauthenticated requests means freshness could not be independently verified through the API.

## Entity Model

- **Station**: MGM center ID (merkezid), station name, location
- **Observation**: Timestamped meteorological readings
- **Forecast**: Multi-day predictions per city
- **Warning**: Severe weather alerts with geographic scope

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly observations expected; not independently verified |
| Openness | 1 | API requires registration and key; returned 500 without auth |
| Stability | 2 | National meteorological service; API endpoint exists but documentation is in Turkish |
| Structure | 2 | JSON expected based on service documentation; not verified |
| Identifiers | 2 | MGM station IDs (merkezid); standard WMO IDs likely available internally |
| Additive Value | 3 | Only source for Turkish weather; 85M population; diverse geography |
| **Total** | **12/18** | |

## Integration Notes

- Registration at `servis.mgm.gov.tr` is required to obtain an API key
- Documentation is primarily in Turkish — translation needed
- API appears to use cookie-based session auth in addition to or instead of API keys
- The website shows that data exists and is updated — the challenge is API access
- Consider as a future candidate pending successful API registration
- Turkey is well-covered by ECMWF and Open-Meteo global models, but local observations from MGM would provide ground truth
- Particularly valuable for: Black Sea flash floods, Anatolian continental extremes, Mediterranean weather, and agricultural weather

## Verdict

Turkey's national weather service has an API infrastructure, but access requires registration and the endpoint was not responsive during testing. Worth pursuing through the registration process — Turkey is meteorologically important (85M people, extreme weather events) and currently has zero weather coverage in the repository. Rated as promising but requiring follow-up.
