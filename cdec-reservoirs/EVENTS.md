# CDEC California Reservoirs Bridge Events

This document describes the events that are emitted by the CDEC California Reservoirs Bridge.

- [gov.ca.water.cdec](#message-group-govcawatercdec)
  - [gov.ca.water.cdec.ReservoirReading](#message-govcawatercdecreservoirreading)

---

## Message Group: gov.ca.water.cdec

---

### Message: gov.ca.water.cdec.ReservoirReading

A single sensor reading from a CDEC reservoir station, representing an hourly (or sub-hourly) observation of storage, elevation, inflow, outflow, or river stage.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `gov.ca.water.cdec.ReservoirReading` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Station and sensor | `uritemplate` | `False` | `{station_id}/{sensor_num}` |

#### Schema:

##### Record: ReservoirReading

*A single sensor reading from a CDEC reservoir station.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Three-letter CDEC station identifier (e.g. SHA, ORO, FOL). |
| `sensor_num` | *int32* | CDEC numeric sensor identifier (15=STORAGE, 6=ELEVATION, 76=INFLOW, 23=OUTFLOW, 1=STAGE). |
| `sensor_type` | *string* | Human-readable sensor type label (e.g. 'STORAGE', 'RES ELE', 'INFLOW'). |
| `value` | *double (nullable)* | Observed measurement value. Null when no observation is available or sentinel -9999. |
| `units` | *string* | Engineering units (e.g. 'AF', 'FEET', 'CFS'). |
| `date` | *string* | Observation timestamp in ISO 8601 with PST offset (-08:00). |
| `dur_code` | *string* | Duration code ('H'=hourly, 'D'=daily, 'E'=event). |
| `data_flag` | *string* | Quality flag character (' '=normal). |
