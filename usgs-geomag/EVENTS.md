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
