# King County Marine Bridge Events

This document describes the events emitted by the King County Marine bridge.

- [US.WA.KingCounty.Marine](#message-group-uswakingcountymarine)
  - [US.WA.KingCounty.Marine.Station](#message-uswakingcountymarinestation)
  - [US.WA.KingCounty.Marine.WaterQualityReading](#message-uswakingcountymarinewaterqualityreading)

---

## Message Group: US.WA.KingCounty.Marine
---
### Message: US.WA.KingCounty.Marine.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `US.WA.KingCounty.Marine.Station` |
| `source` |  | `` | `False` | `https://data.kingcounty.gov/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Reference metadata for one active King County buoy or mooring raw-data dataset.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Stable bridge identifier for the buoy or mooring dataset. |
| `station_name` | *string* | - | `True` | Human-readable station name derived from the dataset title. |
| `dataset_id` | *string* | - | `True` | Socrata dataset identifier for the source dataset. |
| `dataset_name` | *string* | - | `True` | Original King County dataset title. |
| `dataset_url` | *string* | - | `True` | Dataset page URL on data.kingcounty.gov. |
| `sensor_level` | *string* | - | `True` | Sensor position classification inferred from the dataset title, such as surface, bottom, or water-column. |
| `latitude` | *double* (optional) | - | `False` | Station latitude in decimal degrees north, parsed from the dataset description. |
| `longitude` | *double* (optional) | - | `False` | Station longitude in decimal degrees east of Greenwich; King County locations are negative because they lie west of Greenwich. |
---
### Message: US.WA.KingCounty.Marine.WaterQualityReading
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `US.WA.KingCounty.Marine.WaterQualityReading` |
| `source` |  | `` | `False` | `https://data.kingcounty.gov/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterQualityReading
*Normalized King County buoy or mooring reading carrying the documented water-quality and weather measurements published by the current raw-data datasets.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Stable bridge identifier for the buoy or mooring dataset. |
| `station_name` | *string* | - | `True` | Human-readable station name derived from the dataset title. |
| `observation_time` | *string* | - | `True` | Observation timestamp normalized to UTC ISO 8601 form. |
| `water_temperature_c` | *double* (optional) | Cel (°C) | `False` | Water temperature in degrees Celsius. |
| `conductivity_s_m` | *double* (optional) | S/m | `False` | Electrical conductivity in siemens per meter. |
| `pressure_dbar` | *double* (optional) | dbar | `False` | Water pressure in decibar as published by the raw datasets. |
| `dissolved_oxygen_mg_l` | *double* (optional) | mg/L | `False` | Dissolved oxygen concentration in milligrams per liter. |
| `ph` | *double* (optional) | - | `False` | Measured pH value. |
| `chlorophyll_ug_l` | *double* (optional) | ug/L (µg/L) | `False` | Chlorophyll fluorescence or chlorophyll concentration in micrograms per liter. |
| `turbidity_ntu` | *double* (optional) | NTU | `False` | Turbidity in nephelometric turbidity units. |
| `chlorophyll_stddev_ug_l` | *double* (optional) | ug/L (µg/L) | `False` | Standard deviation of chlorophyll fluorescence in micrograms per liter. |
| `turbidity_stddev_ntu` | *double* (optional) | NTU | `False` | Standard deviation of turbidity in nephelometric turbidity units. |
| `salinity_psu` | *double* (optional) | PSU | `False` | Salinity in practical salinity units. |
| `specific_conductivity_s_m` | *double* (optional) | S/m | `False` | Specific conductivity in siemens per meter. |
| `dissolved_oxygen_saturation_pct` | *double* (optional) | P1 (%) | `False` | Dissolved oxygen saturation as a percentage. |
| `nitrate_umol` | *double* (optional) | umol (µmol) | `False` | Nitrate or nitrate-plus-nitrite concentration in micromoles. |
| `nitrate_mg_l` | *double* (optional) | mg/L | `False` | Nitrate or nitrate-plus-nitrite concentration in milligrams per liter. |
| `wind_direction_deg` | *double* (optional) | deg (°) | `False` | Wind direction in degrees at the buoy surface. |
| `wind_speed_m_s` | *double* (optional) | m/s | `False` | Wind speed in meters per second at the buoy surface. |
| `photosynthetically_active_radiation_umol_s_m2` | *double* (optional) | umol/s/m2 (µmol/s/m²) | `False` | Photosynthetically active radiation in micromoles per second per square meter. |
| `air_temperature_f` | *double* (optional) | [degF] (°F) | `False` | Air temperature in degrees Fahrenheit. |
| `air_humidity_pct` | *double* (optional) | P1 (%) | `False` | Relative humidity percentage. |
| `air_pressure_in_hg` | *double* (optional) | [in_i'Hg] (inHg) | `False` | Air pressure in inches of mercury. |
| `system_battery_v` | *double* (optional) | V | `False` | System battery voltage in volts. |
| `sensor_battery_v` | *double* (optional) | V | `False` | Sensor or sonde battery voltage in volts. |
