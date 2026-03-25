# NOAA SWPC Space Weather Bridge Events

This document describes the events emitted by the NOAA SWPC Space Weather Bridge.

- [Microsoft.OpenData.US.NOAA.SWPC](#message-group-microsoftopendatausnoaaswpc)
  - [Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert](#message-microsoftopendatausnoaaswpcspaceweatheralert)
  - [Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex](#message-microsoftopendatausnoaaswpcplanetarykindex)
  - [Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary](#message-microsoftopendatausnoaaswpcsolarwindsummary)

---

## Message Group: Microsoft.OpenData.US.NOAA.SWPC

---

### Message: Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert

Space weather alerts issued by the NOAA Space Weather Prediction Center, including solar flare warnings, geomagnetic storm watches, and radio blackout alerts.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert` |
| `source` | CloudEvent source | `string` | `True` | `https://services.swpc.noaa.gov` |

#### Schema: SpaceWeatherAlert

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `product_id` | *string* | Alert product ID |
| `issue_datetime` | *string* | When the alert was issued |
| `message` | *string* | Full alert message text |

---

### Message: Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex

Planetary K-index measurements from ground-based magnetometer stations, indicating the level of geomagnetic activity on a 0–9 scale.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex` |
| `source` | CloudEvent source | `string` | `True` | `https://services.swpc.noaa.gov` |

#### Schema: PlanetaryKIndex

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `time_tag` | *string* | Timestamp of the measurement |
| `kp` | *number* | Planetary K-index value (0-9) |
| `kp_fraction` | *number* | Fractional K-index |
| `a_running` | *number* | Running A-index |
| `station_count` | *number* | Number of stations used |

---

### Message: Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary

Combined solar wind speed and interplanetary magnetic field summary from upstream spacecraft measurements.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary` |
| `source` | CloudEvent source | `string` | `True` | `https://services.swpc.noaa.gov` |

#### Schema: SolarWindSummary

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `timestamp` | *string* | Timestamp of the measurement |
| `wind_speed` | *number* | Solar wind speed in km/s |
| `bt` | *number* | Total magnetic field strength in nT |
| `bz` | *number* | North-south magnetic field component in nT |
