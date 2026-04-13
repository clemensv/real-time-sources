# Events — Canada ECCC Water Office Hydrometric Bridge

## CA.Gov.ECCC.Hydro.Station

CloudEvents type: `CA.Gov.ECCC.Hydro.Station`  
Source: `https://api.weather.gc.ca/collections/hydrometric-stations`  
Subject template: `stations/{station_number}`  
Kafka key: `stations/{station_number}`  

Reference data for a Water Survey of Canada hydrometric monitoring station.
Emitted at bridge startup and refreshed every 24 hours.

| Field | Type | Description |
|---|---|---|
| `station_number` | string | Unique WSC station identifier (e.g. `05BJ004`) |
| `station_name` | string | Official station name |
| `prov_terr_state_loc` | string | Province/territory/state code (e.g. `AB`) |
| `status_en` | string? | Operational status in English |
| `contributor_en` | string? | Contributing agency name |
| `drainage_area_gross` | double? | Gross drainage area (km²) |
| `drainage_area_effect` | double? | Effective drainage area (km²) |
| `rhbn` | boolean? | Part of Reference Hydrometric Basin Network |
| `real_time` | boolean? | Real-time data availability flag |
| `latitude` | double? | Station latitude (decimal degrees, WGS84) |
| `longitude` | double? | Station longitude (decimal degrees, WGS84) |

---

## CA.Gov.ECCC.Hydro.Observation

CloudEvents type: `CA.Gov.ECCC.Hydro.Observation`  
Source: `https://api.weather.gc.ca/collections/hydrometric-realtime`  
Subject template: `stations/{station_number}`  
Kafka key: `stations/{station_number}`  

Real-time hydrometric observation (water level and/or discharge).
Provisional data, updated approximately every 5 minutes.

| Field | Type | Description |
|---|---|---|
| `station_number` | string | WSC station identifier |
| `identifier` | string | Unique observation identifier (`STATION_NUMBER.DATETIME`) |
| `station_name` | string | Station name |
| `prov_terr_state_loc` | string | Province/territory/state code |
| `observation_datetime` | datetime | Observation timestamp (UTC) |
| `level` | double? | Water level in metres |
| `discharge` | double? | Discharge in m³/s |
| `latitude` | double? | Station latitude |
| `longitude` | double? | Station longitude |
