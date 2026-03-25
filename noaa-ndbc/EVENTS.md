# NOAA NDBC Buoy Observations Bridge Events

This document describes the events emitted by the NOAA NDBC Buoy Observations Bridge.

- [Microsoft.OpenData.US.NOAA.NDBC](#message-group-microsoftopendatausnoaandbc)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation](#message-microsoftopendatausnoaandbcbuoyobservation)

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
