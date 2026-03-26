# NOAA NDBC Buoy Observations Bridge Events

This document describes the events emitted by the NOAA NDBC Buoy Observations Bridge.

- [Microsoft.OpenData.US.NOAA.NDBC](#message-group-microsoftopendatausnoaandbc)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation](#message-microsoftopendatausnoaandbcbuoyobservation)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyStation](#message-microsoftopendatausnoaandbcbuoystation)

---

## Message Group: Microsoft.OpenData.US.NOAA.NDBC

---

### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation` |
| `source` | CloudEvent source | `string` | `True` | `https://www.ndbc.noaa.gov` |

#### Schema: BuoyObservation

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `station_id` | *string* | — | NDBC station identifier |
| `latitude` | *number* | degrees | Station latitude |
| `longitude` | *number* | degrees | Station longitude |
| `timestamp` | *string (date-time)* | — | ISO timestamp of observation |
| `wind_direction` | *number* | degrees | Wind direction |
| `wind_speed` | *number* | m/s | Wind speed |
| `gust` | *number* | m/s | Wind gust speed |
| `wave_height` | *number* | meters | Significant wave height |
| `dominant_wave_period` | *number* | seconds | Dominant wave period |
| `average_wave_period` | *number* | seconds | Average wave period |
| `mean_wave_direction` | *number* | degrees | Mean wave direction |
| `pressure` | *number* | hPa | Sea level pressure |
| `air_temperature` | *number* | celsius | Air temperature |
| `water_temperature` | *number* | celsius | Sea surface temperature |
| `dewpoint` | *number* | celsius | Dewpoint temperature |

---

### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyStation

*Reference data — sent once at startup before telemetry polling begins.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation` |
| `source` | CloudEvent source | `string` | `True` | `https://www.ndbc.noaa.gov` |

#### Schema: BuoyStation

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | NDBC station identifier |
| `owner` | *string* | Station owner organization |
| `station_type` | *string* | Station type (e.g., Weather Buoy, C-MAN Station) |
| `hull` | *string* | Hull type |
| `name` | *string* | Station name and location description |
| `latitude` | *number* | Station latitude in decimal degrees |
| `longitude` | *number* | Station longitude in decimal degrees |
| `timezone` | *string* | Station timezone |
