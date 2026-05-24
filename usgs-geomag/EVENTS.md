# USGS Geomagnetism Program Bridge Events

This document describes the events emitted by the USGS Geomagnetism Program Bridge.

- [gov.usgs.geomag](#message-group-govusgsgeomag)
  - [gov.usgs.geomag.Observatory](#message-govusgsgeomagobservatory)
  - [gov.usgs.geomag.MagneticFieldReading](#message-govusgsgeomagmagneticfieldreading)

---

## Message Group: gov.usgs.geomag

---

### Message: gov.usgs.geomag.Observatory

Reference data for a USGS Geomagnetism Program observatory.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.usgs.geomag.Observatory` |
| `source` | CloudEvent source | `string` | `True` | `https://geomag.usgs.gov` |
| `subject` | Observatory IAGA code | `uritemplate` | `True` | `{iaga_code}` |

#### Schema: Observatory

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `iaga_code` | *string* | — | IAGA observatory code (e.g. BOU, BRW, FRN) |
| `name` | *string* | — | Human-readable observatory name |
| `agency` | *string* | — | Operating agency short identifier |
| `agency_name` | *string* | — | Full operating agency name |
| `latitude` | *number* | degrees | Geodetic latitude |
| `longitude` | *number* | degrees | Geodetic longitude (degrees east) |
| `elevation` | *number* | meters | Elevation above mean sea level |
| `sensor_orientation` | *string* | — | Magnetometer sensor orientation (e.g. HDZ) |
| `sensor_sampling_rate` | *number* | Hz | Native sensor sampling rate |
| `declination_base` | *number* | — | Declination baseline in minutes of arc |

---

### Message: gov.usgs.geomag.MagneticFieldReading

One-minute resolution geomagnetic field variation reading.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.usgs.geomag.MagneticFieldReading` |
| `source` | CloudEvent source | `string` | `True` | `https://geomag.usgs.gov` |
| `subject` | Observatory IAGA code | `uritemplate` | `True` | `{iaga_code}` |

#### Schema: MagneticFieldReading

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `iaga_code` | *string* | — | IAGA observatory code |
| `timestamp` | *string (date-time)* | — | UTC timestamp of the 1-minute sample |
| `h` | *number* | nT | Horizontal intensity component |
| `d` | *number* | minutes of arc | Declination angle |
| `z` | *number* | nT | Vertical intensity component |
| `f` | *number* | nT | Total field intensity |

---

## Message Group: gov.usgs.geomag.mqtt

MQTT/5.0 transport variants for USGS geomagnetic observatory reference data and one-minute readings. Topics are retained QoS-1 leaves under space-weather/us/usgs/usgs-geomag/{iaga_code}/..., where {iaga_code} in the topic is the lowercased IAGA observatory code; the payload field may carry the canonical upstream code. Producers MUST lowercase {iaga_code} for the topic and consumers MUST treat topic filters as case-sensitive. The info leaf is retained reference metadata with no expiry. The reading leaf is a latched current 1-minute observation with Message Expiry Interval 7200 seconds; if the retained value expires, interpret the empty topic as observatory or bridge silence for at least two hours, not a zero magnetic-field reading. The iaga_code is the join key between retained info and readings.

The MQTT transport uses MQTT 5.0 binary-mode CloudEvents: the payload is the JSON body for the referenced message schema, and CloudEvents metadata is carried as MQTT user properties. The MQTT messagegroup references the transport-neutral Kafka/CloudEvents message definitions through `basemessageurl`, so the schemas above remain authoritative.

### MQTT topics

| Topic pattern | Bound message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `space-weather/us/usgs/usgs-geomag/{iaga_code}/info` | `gov.usgs.geomag.Observatory` | `true` | `1` | `` |
| `space-weather/us/usgs/usgs-geomag/{iaga_code}/reading` | `gov.usgs.geomag.MagneticFieldReading` | `true` | `1` | `7200` |
