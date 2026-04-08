# Blitzortung Lightning Events

This document describes the live lightning events emitted by the Blitzortung bridge.

- [Blitzortung.Lightning](#message-group-blitzortunglightning)
  - [Blitzortung.Lightning.LightningStroke](#message-blitzortunglightninglightningstroke)

---

## Message Group: Blitzortung.Lightning

---

### Message: Blitzortung.Lightning.LightningStroke

*Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed. Each event represents one source-scoped stroke identifier with its observation time, coordinates, upstream delay and accuracy values, and optionally the detector participation flags carried in the public sta object.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Blitzortung.Lightning.LightningStroke` |
| `source` |  | `` | `False` | `wss://live.lightningmaps.org/` |
| `subject` |  | `uritemplate` | `False` | `{source_id}/{stroke_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:

##### Record: LightningStroke

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
