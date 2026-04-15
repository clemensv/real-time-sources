# Fabric Event Stream + KQL Database Setup

Sets up a Microsoft Fabric Event Stream and KQL database for raw Puget Sound
CloudEvents landing.

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│ ACI Container Group / Docker Compose                                │
│  seattle-911                                                        │
│  seattle-street-closures                                            │
│  king-county-marine                                                 │
│  epa-uv                                                             │
│  nws-forecasts                                                      │
│  wsdot                                                              │
│  noaa --station 9444090 / 9444900 / 9445958 / 9446484 /             │
│       9447130 / 9449424 / 9449880                                   │
└────────────────────────────────────┬─────────────────────────────────┘
                                     │ CONNECTION_STRING
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ Fabric Event Stream: pugetsound-ingest                              │
│  Source: pugetsound-input (Custom Endpoint)                         │
│  Stream: pugetsound-ingest-stream                                   │
│  Destination: _cloudevents_dispatch                                 │
└────────────────────────────────────┬─────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│ Eventhouse / KQL database: pugetsound                               │
│  _cloudevents_dispatch                                               │
│  WSDOT typed tables + latest views      (from ../../wsdot/kql)      │
│  NOAA typed tables + latest views       (from ../../noaa/kql)       │
│  Seattle + NWS typed tables + latest views (from ./pugetsound.kql)  │
└──────────────────────────────────────────────────────────────────────┘
```

There is no SQL normalization layer here. The Event Stream lands structured
CloudEvents as-is into `_cloudevents_dispatch`, and KQL update policies fan
them back out into typed tables.

## Files

| File | Description |
|---|---|
| `setup.ps1` | Creates or updates the KQL database and Event Stream |
| `pugetsound.kql` | Supplemental KQL for Seattle 911, Seattle street closures, King County marine, EPA UV, and NWS forecasts |
| `..\..\wsdot\kql\wsdot.kql` | Reused WSDOT KQL and update policies |
| `..\..\noaa\kql\noaa.kql` | Reused NOAA KQL and update policies |

## Usage

```powershell
./setup.ps1 `
  -WorkspaceId "c98acd97-4363-4296-8323-b6ab21e53903" `
  -EventhouseId "dbfd2819-2879-4ae7-bff2-95619ad7b8e7"
```

This creates or updates:

- KQL database `pugetsound`
- Event Stream `pugetsound-ingest`
- Custom endpoint source `pugetsound-input`
- Eventhouse destination landing into `_cloudevents_dispatch`

After setup, open the Event Stream in the Fabric portal and retrieve the custom
endpoint connection string for the container group or Docker Compose bundle.

## Example queries

```kusto
_cloudevents_dispatch
| summarize count() by type
| order by count_ desc

SeattleFire911IncidentLatest
| top 20 by ___time desc
| project incident_number, incident_type, incident_datetime, address

SeattleStreetClosureLatest
| where end_date >= format_datetime(now(), "yyyy-MM-dd")
| project closure_id, permit_type, project_name, street_on, street_from, street_to

KingCountyMarineWaterQualityReadingLatest
| project station_name, observation_time, water_temperature_c, dissolved_oxygen_mg_l, ph

EPAUVDailyForecastLatest
| project location_id, forecast_date, uv_index, uv_alert

NWSLandZoneForecastLatest
| mv-expand periods
| project zone_id, updated, periods

NWSMarineZoneForecastLatest
| project zone_id, zone_name, issued_at_text, synopsis

VesselLocationLatest
| top 20 by ___time desc
```
