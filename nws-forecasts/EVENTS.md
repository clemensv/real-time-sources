# NWS Forecast Zones Events

## ForecastZone

Reference event for one configured NWS forecast zone.

**Key / subject:** `zone_id`

## LandZoneForecast

Narrative land forecast snapshot for one public forecast zone from `api.weather.gov/zones/forecast/{zoneId}/forecast`.

**Key / subject:** `zone_id`

## MarineZoneForecast

Narrative marine bulletin snapshot for one marine forecast zone from `tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/{zone}.txt`.

**Key / subject:** `zone_id`
