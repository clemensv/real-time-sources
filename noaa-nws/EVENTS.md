# NOAA NWS Weather Alerts Bridge Events

This document describes the events emitted by the NOAA NWS Weather Alerts Bridge.

- [Microsoft.OpenData.US.NOAA.NWS](#message-group-microsoftopendatausnoaanws)
  - [Microsoft.OpenData.US.NOAA.NWS.WeatherAlert](#message-microsoftopendatausnoaanwsweatheralert)
  - [Microsoft.OpenData.US.NOAA.NWS.Zone](#message-microsoftopendatausnoaanwszone)

---

## Message Group: Microsoft.OpenData.US.NOAA.NWS

---

### Message: Microsoft.OpenData.US.NOAA.NWS.WeatherAlert

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Microsoft.OpenData.US.NOAA.NWS.WeatherAlert` |
| `source` | CloudEvent source | `string` | `True` | `https://api.weather.gov` |

#### Schema: WeatherAlert

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `alert_id` | *string* | NWS alert ID |
| `area_desc` | *string* | Description of affected area |
| `sent` | *string (date-time)* | When the alert was sent |
| `effective` | *string (date-time)* | When the alert becomes effective |
| `expires` | *string (date-time)* | When the alert expires |
| `status` | *string (enum)* | Alert status: Actual, Exercise, System, Test, Draft |
| `message_type` | *string (enum)* | Message type: Alert, Update, Cancel |
| `category` | *string (enum)* | Category: Met, Geo, Safety, Security, Rescue, Fire, Health, Env, Transport, Infra, CBRNE, Other |
| `severity` | *string (enum)* | Severity: Extreme, Severe, Moderate, Minor, Unknown |
| `certainty` | *string (enum)* | Certainty: Observed, Likely, Possible, Unlikely, Unknown |
| `urgency` | *string (enum)* | Urgency: Immediate, Expected, Future, Past, Unknown |
| `event` | *string* | Event type name (e.g., "Tornado Warning", "Flood Watch") |
| `sender_name` | *string* | Name of the sending NWS office |
| `headline` | *string* | Alert headline |
| `description` | *string* | Full alert description |

---

### Message: Microsoft.OpenData.US.NOAA.NWS.Zone

This is reference data sent at startup. It contains NWS forecast zone definitions
fetched from the NWS API zones endpoint.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Microsoft.OpenData.US.NOAA.NWS.Zone` |
| `source` | CloudEvent source | `string` | `True` | `https://api.weather.gov` |

#### Schema: Zone

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `zone_id` | *string* | Zone identifier (e.g., AKZ317) |
| `name` | *string* | Zone name |
| `type` | *string* | Zone type (e.g., public, fire, coastal) |
| `state` | *string* | US state abbreviation |
| `forecast_office` | *string* | Forecast office URL |
| `timezone` | *string* | Timezone identifier |
| `radar_station` | *string* | Associated radar station identifier |
