# AirQo Uganda Air Quality Bridge Events

This document describes the events emitted by the AirQo Uganda Air Quality Bridge.

- [net.airqo.uganda](#message-group-netairqouganda)
  - [net.airqo.uganda.Site](#message-netairqougandasite)
  - [net.airqo.uganda.Measurement](#message-netairqougandameasurement)

---

## Message Group: net.airqo.uganda

---

### Message: net.airqo.uganda.Site

*Reference data — sent once at startup before telemetry polling begins.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `net.airqo.uganda.Site` |
| `source` | CloudEvent source | `string` | `True` | `https://api.airqo.net` |

#### Schema: Site

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_id` | *string* | AirQo site identifier (24-char hex ObjectId) |
| `name` | *string* | Human-readable site name |
| `formatted_name` | *string* | Full geocoded address string |
| `latitude` | *number* | Approximate latitude in decimal degrees |
| `longitude` | *number* | Approximate longitude in decimal degrees |
| `country` | *string* | Country where the site is located |
| `region` | *string* | Administrative region or province |
| `city` | *string* | Nearest city or town |
| `is_online` | *boolean* | Whether the site is currently reporting data |

---

### Message: net.airqo.uganda.Measurement

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `net.airqo.uganda.Measurement` |
| `source` | CloudEvent source | `string` | `True` | `https://api.airqo.net` |

#### Schema: Measurement

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `site_id` | *string* | — | AirQo site identifier |
| `device` | *string* | — | Short device name (e.g. 'aq_01') |
| `device_id` | *string* | — | AirQo device identifier (24-char hex ObjectId) |
| `timestamp` | *string (date-time)* | — | ISO timestamp of measurement |
| `pm2_5_raw` | *number* | µg/m³ | Raw PM2.5 concentration |
| `pm2_5_calibrated` | *number* | µg/m³ | Calibrated PM2.5 concentration |
| `pm10_raw` | *number* | µg/m³ | Raw PM10 concentration |
| `pm10_calibrated` | *number* | µg/m³ | Calibrated PM10 concentration |
| `temperature` | *number* | °C | Ambient air temperature |
| `humidity` | *number* | % | Relative humidity |
| `latitude` | *number* | degrees | Measurement location latitude |
| `longitude` | *number* | degrees | Measurement location longitude |
| `frequency` | *string* | — | Measurement frequency (e.g. 'hourly') |
