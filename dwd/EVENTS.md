# DWD Open Data Bridge Events

This document describes the events emitted by the DWD Open Data bridge.

- [DE.DWD.CDC](#message-group-dedwdcdc)
  - [DE.DWD.CDC.StationMetadata](#message-dedwdcdcstationmetadata)
  - [DE.DWD.CDC.AirTemperature10Min](#message-dedwdcdcairtemperature10min)
  - [DE.DWD.CDC.Precipitation10Min](#message-dedwdcdcprecipitation10min)
  - [DE.DWD.CDC.Wind10Min](#message-dedwdcdcwind10min)
  - [DE.DWD.CDC.Solar10Min](#message-dedwdcdcsolar10min)
  - [DE.DWD.CDC.HourlyObservation](#message-dedwdcdchourlyobservation)
  - [DE.DWD.Weather.Alert](#message-dedwdweatheralert)

---

## Message Group: DE.DWD.CDC

---

### Message: DE.DWD.CDC.StationMetadata

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.StationMetadata` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.AirTemperature10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.AirTemperature10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.Precipitation10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Precipitation10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.Wind10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Wind10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.Solar10Min

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Solar10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.CDC.HourlyObservation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.HourlyObservation` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: DE.DWD.Weather.Alert

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Weather.Alert` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
