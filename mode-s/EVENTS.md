# Mode-S API Bridge Events

This document describes the events that are emitted by the Mode-S API Bridge.

- [Mode_S](#message-group-modes)
  - [Mode_S.Messages](#message-modesmessages)

---

## Message Group: Mode_S

---

### Message: Mode_S.Messages

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Mode_S.Messages` |
| `source` | Station Identifier | `uritemplate` | `True` | `{stationid}` |

#### Schema:

##### Record: Messages

*A container for multiple Mode-S and ADS-B decoded messages.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `messages` | *array* | An array of Mode-S and ADS-B decoded message records. |
