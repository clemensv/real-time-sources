# Kystverket AIS Bridge Events

This document describes the events emitted by the Kystverket AIS bridge.

- [NO.Kystverket.AIS](#message-group-nokystverketais)
  - [NO.Kystverket.AIS.PositionReportClassA](#message-nokystverketaispositionreportclassa)
  - [NO.Kystverket.AIS.StaticVoyageData](#message-nokystverketaisstaticvoyagedata)
  - [NO.Kystverket.AIS.PositionReportClassB](#message-nokystverketaispositionreportclassb)
  - [NO.Kystverket.AIS.StaticDataClassB](#message-nokystverketaisstaticdataclassb)
  - [NO.Kystverket.AIS.AidToNavigation](#message-nokystverketaisaidtonavigation)

---

## Message Group: NO.Kystverket.AIS

---

### Message: NO.Kystverket.AIS.PositionReportClassA

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.PositionReportClassA` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: NO.Kystverket.AIS.StaticVoyageData

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.StaticVoyageData` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: NO.Kystverket.AIS.PositionReportClassB

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.PositionReportClassB` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: NO.Kystverket.AIS.StaticDataClassB

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.StaticDataClassB` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: NO.Kystverket.AIS.AidToNavigation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.Kystverket.AIS.AidToNavigation` |
| `source` |  | `` | `False` | `urn:ais:kystverket:tcp` |

#### Schema:

##### Record: None

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
