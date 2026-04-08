# Nepal BIPAD Portal River Monitoring API Bridge Events

This document describes the events emitted by the Nepal BIPAD Portal river monitoring bridge.

- [np.gov.bipad.hydrology](#message-group-npgovbipadhydrology)
  - [np.gov.bipad.hydrology.RiverStation](#message-npgovbipadhydrologyriverstation)
  - [np.gov.bipad.hydrology.WaterLevelReading](#message-npgovbipadhydrologywaterlevelreading)

---

## Message Group: np.gov.bipad.hydrology

---

### Message: np.gov.bipad.hydrology.RiverStation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `np.gov.bipad.hydrology.RiverStation` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Station | `uritemplate` | `False` | `{station_id}` |

#### Schema:

##### Record: RiverStation

*Reference data for a BIPAD river monitoring station in Nepal, including location, river basin, administrative boundaries, and configured danger/warning thresholds.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Unique integer identifier of the river station assigned by the BIPAD portal, transmitted as a string for key compatibility. |
| `title` | *string* | Human-readable name of the river station, typically in the format 'River at Location'. |
| `basin` | *string* | Name of the river basin the station belongs to. |
| `latitude` | *double* | Latitude coordinate of the station in WGS84 decimal degrees. |
| `longitude` | *double* | Longitude coordinate of the station in WGS84 decimal degrees. |
| `elevation` | *integer (nullable)* | Elevation of the station in meters above sea level. Null when not available. |
| `danger_level` | *double (nullable)* | Configured danger water level threshold in meters. Null when not configured. |
| `warning_level` | *double (nullable)* | Configured warning water level threshold in meters. Null when not configured. |
| `description` | *string (nullable)* | Free-text description of the station. Null when not provided. |
| `data_source` | *string* | Origin system providing the station data, typically 'hydrology.gov.np'. |
| `province` | *integer (nullable)* | Nepal province administrative code. Null when not assigned. |
| `district` | *integer (nullable)* | Nepal district administrative code. Null when not assigned. |
| `municipality` | *integer (nullable)* | Nepal municipality administrative code. Null when not assigned. |
| `ward` | *integer (nullable)* | Nepal ward-level administrative code. Null when not assigned. |

---

### Message: np.gov.bipad.hydrology.WaterLevelReading

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `np.gov.bipad.hydrology.WaterLevelReading` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Station | `uritemplate` | `False` | `{station_id}` |

#### Schema:

##### Record: WaterLevelReading

*Real-time water level telemetry reading from a BIPAD river monitoring station in Nepal, including current water level, alert status, and trend direction.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Unique integer identifier of the river station. |
| `title` | *string* | Human-readable name of the river station at the time of the reading. |
| `basin` | *string* | Name of the river basin the station belongs to. |
| `water_level` | *double (nullable)* | Current water level at the station in meters. Null when no reading available. |
| `danger_level` | *double (nullable)* | Configured danger water level threshold in meters. Null when not configured. |
| `warning_level` | *double (nullable)* | Configured warning water level threshold in meters. Null when not configured. |
| `status` | *string* | Current alert status: 'BELOW WARNING LEVEL', 'WARNING', or 'DANGER'. |
| `trend` | *string* | Direction of water level change: 'STEADY', 'RISING', or 'FALLING'. |
| `water_level_on` | *string* | ISO 8601 timestamp of when the water level was measured, in Nepal Standard Time (+05:45). |
