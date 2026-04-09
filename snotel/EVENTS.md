# SNOTEL Snow and Weather Bridge Events

This document describes the events emitted by the USDA NRCS SNOTEL bridge.

- [gov.usda.nrcs.snotel](#message-group-govusdanrcssnotel)
  - [gov.usda.nrcs.snotel.Station](#message-govusdanrcssnotelstation)
  - [gov.usda.nrcs.snotel.SnowObservation](#message-govusdanrcssnotelsnowobservation)

---

## Message Group: gov.usda.nrcs.snotel

---

### Message: gov.usda.nrcs.snotel.Station

*Reference data — sent at startup before telemetry polling begins.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.usda.nrcs.snotel.Station` |
| `source` | CloudEvent source | `string` | `True` | `https://wcc.sc.egov.usda.gov` |
| `subject` | Station triplet | `uritemplate` | `True` | `{station_triplet}` |

#### Schema: Station

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `station_triplet` | *string* | — | SNOTEL station triplet identifier (e.g. '838:CO:SNTL') |
| `name` | *string* | — | Human-readable station name |
| `state` | *string* | — | Two-letter US state code |
| `elevation` | *number* | ft | Station elevation above sea level in feet |
| `latitude` | *number* | — | Latitude in decimal degrees north |
| `longitude` | *number* | — | Longitude in decimal degrees east |

---

### Message: gov.usda.nrcs.snotel.SnowObservation

*Hourly telemetry — snow and weather observations from SNOTEL stations.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.usda.nrcs.snotel.SnowObservation` |
| `source` | CloudEvent source | `string` | `True` | `https://wcc.sc.egov.usda.gov` |
| `subject` | Station triplet | `uritemplate` | `True` | `{station_triplet}` |

#### Schema: SnowObservation

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `station_triplet` | *string* | — | SNOTEL station triplet identifier |
| `date_time` | *string (datetime)* | — | Observation timestamp |
| `snow_water_equivalent` | *number (nullable)* | in | Snow Water Equivalent — depth of water from melting the entire snowpack |
| `snow_depth` | *number (nullable)* | in | Total snow depth |
| `precipitation` | *number (nullable)* | in | Water-year accumulated precipitation |
| `air_temperature` | *number (nullable)* | °F | Instantaneously observed air temperature |
