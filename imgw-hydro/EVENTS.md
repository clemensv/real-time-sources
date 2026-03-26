# IMGW-PIB Hydrological Data Bridge Events

This document describes the events that are emitted by the IMGW-PIB Hydrological Data Bridge.

- [PL.Gov.IMGW.Hydro](#message-group-plgovimgwhydro)
  - [PL.Gov.IMGW.Hydro.Station](#message-plgovimgwhydrostation)
  - [PL.Gov.IMGW.Hydro.WaterLevelObservation](#message-plgovimgwhydrowaterlevelobservation)

---

## Message Group: PL.Gov.IMGW.Hydro

---

### Message: PL.Gov.IMGW.Hydro.Station

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `PL.Gov.IMGW.Hydro.Station` |
| `source` | Source Feed URL | `uritemplate` | `True` | `https://danepubliczne.imgw.pl` |

#### Schema:

##### Record: Station

*A hydrological station from IMGW-PIB.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `id_stacji` | *string* | Station identifier |
| `stacja` | *string* | Station name |
| `rzeka` | *string* | River name |
| `wojewodztwo` | *string* | Voivodeship (province) |
| `longitude` | *number* | Longitude in WGS84 |
| `latitude` | *number* | Latitude in WGS84 |

---

### Message: PL.Gov.IMGW.Hydro.WaterLevelObservation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `PL.Gov.IMGW.Hydro.WaterLevelObservation` |
| `source` | Source Feed URL | `uritemplate` | `True` | `https://danepubliczne.imgw.pl` |

#### Schema:

##### Record: WaterLevelObservation

*A water level observation from IMGW-PIB.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Station identifier |
| `station_name` | *string* | Station name |
| `river` | *string* | River name |
| `voivodeship` | *string* | Voivodeship (province) |
| `water_level` | *number* | Water level in cm |
| `water_level_timestamp` | *string* | Water level measurement timestamp |
| `water_temperature` | *number* (nullable) | Water temperature in °C |
| `water_temperature_timestamp` | *string* (nullable) | Water temperature measurement timestamp |
| `discharge` | *number* (nullable) | Discharge in m³/s |
| `discharge_timestamp` | *string* (nullable) | Discharge measurement timestamp |
| `ice_phenomenon_code` | *string* (nullable) | Ice phenomenon code |
| `overgrowth_code` | *string* (nullable) | Vegetation overgrowth code |
