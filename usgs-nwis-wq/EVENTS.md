# USGS NWIS Water Quality Bridge Events

This document describes the events emitted by the USGS NWIS Water Quality bridge.

- [USGS.WaterQuality.Sites](#message-group-usgswaterqualitysites)
  - [USGS.WaterQuality.Sites.MonitoringSite](#message-usgswaterqualitysitesmonitoringsite)
- [USGS.WaterQuality.Readings](#message-group-usgswaterqualityreadings)
  - [USGS.WaterQuality.Readings.WaterQualityReading](#message-usgswaterqualityreadingswaterqualityreading)

---

## Message Group: USGS.WaterQuality.Sites

---

### Message: USGS.WaterQuality.Sites.MonitoringSite

*USGS water quality monitoring site reference data. Describes a physical monitoring location equipped with continuous water quality sensors.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `True` | `USGS.WaterQuality.Sites.MonitoringSite` |
| `source` |  | `uritemplate` | `True` | `{source_uri}` |
| `subject` |  | `uritemplate` | `True` | `{site_number}` |

#### Schema: MonitoringSite

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_number` | *string* | USGS site identification number (8-to-15-digit). |
| `site_name` | *string* | Official USGS station name. |
| `agency_code` | *string* | Agency code (typically 'USGS'). |
| `latitude` | *double* (nullable) | Decimal latitude (WGS84). |
| `longitude` | *double* (nullable) | Decimal longitude (WGS84). |
| `site_type` | *string* (nullable) | Site type code (ST=stream, LK=lake, GW=groundwater, ES=estuary). |
| `state_code` | *string* (nullable) | Two-digit FIPS state code. |
| `county_code` | *string* (nullable) | Five-digit FIPS county code. |
| `huc_code` | *string* (nullable) | Hydrologic Unit Code (watershed identifier). |

---

## Message Group: USGS.WaterQuality.Readings

---

### Message: USGS.WaterQuality.Readings.WaterQualityReading

*A single water quality observation from a USGS continuous monitoring sensor.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `True` | `USGS.WaterQuality.Readings.WaterQualityReading` |
| `source` |  | `uritemplate` | `True` | `{source_uri}` |
| `subject` |  | `uritemplate` | `True` | `{site_number}/{parameter_code}` |

#### Schema: WaterQualityReading

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `site_number` | *string* | USGS site identification number. |
| `site_name` | *string* | Official USGS station name. |
| `parameter_code` | *string* | Five-digit USGS parameter code (00010=water temp, 00300=DO, 00400=pH, 00095=conductance, 63680=turbidity, 99133=nitrate). |
| `parameter_name` | *string* | Human-readable parameter description. |
| `value` | *double* (nullable) | Numeric sensor reading. Null when no valid value. |
| `unit` | *string* | Unit of measurement (e.g. 'deg C', 'mg/l', 'uS/cm @25C', 'FNU'). |
| `qualifier` | *string* (nullable) | Data qualifier code ('P'=provisional, 'A'=approved, 'e'=estimated). |
| `date_time` | *string* | ISO 8601 UTC date-time of the observation. |
