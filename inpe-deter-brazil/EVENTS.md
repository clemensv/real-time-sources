# INPE DETER Brazil Deforestation Alerts Events

This document describes the events emitted by the INPE DETER Brazil deforestation alerts bridge.

- [BR.INPE.DETER](#message-group-brinpedeter)
  - [BR.INPE.DETER.DeforestationAlert](#message-brinpedeterdeforestationalert)

---

## Message Group: BR.INPE.DETER

---

### Message: BR.INPE.DETER.DeforestationAlert

*INPE DETER deforestation alert for Amazon and Cerrado biomes.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `BR.INPE.DETER.DeforestationAlert` |
| `source` | Source URI | `uritemplate` | `True` | `{source_uri}` |
| `subject` | Biome and alert ID | `uritemplate` | `True` | `{biome}/{alert_id}` |
| `time` | Observation date | `uritemplate` | `True` | `{view_date}` |

#### Schema: BR.INPE.DETER.DeforestationAlert (Avro)

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `alert_id` | `string` | Stable reference ID from INPE (gid). |
| `biome` | `string` | Biome of the alert: amazon or cerrado. |
| `classname` | `string` | Deforestation class: DESMATAMENTO_CR, DEGRADACAO, MINERACAO, CS_DESORDENADO, etc. |
| `view_date` | `string` | Observation date in YYYY-MM-DD format. |
| `satellite` | `string` | Satellite name (CBERS-4, Amazonia-1, etc.). |
| `sensor` | `string` | Sensor name (AWFI, WFI, MSI). |
| `area_km2` | `double` | Area of the deforestation polygon in square kilometers. |
| `municipality` | `string?` | Municipality name. |
| `state_code` | `string?` | Brazilian state code (UF), e.g. PA, MT, when provided by INPE. |
| `state_slug` | `string` | Lowercased topic-safe state axis (`pa`, `mt`, or `unknown`). |
| `class_slug` | `string` | Lowercase-kebab topic-safe DETER class axis, such as `desmatamento-cr` or `mineracao`. |
| `path_row` | `string?` | Satellite path/row identifier. |
| `publish_month` | `string?` | Publication month in YYYY-MM-DD format. |
| `centroid_latitude` | `double` | Latitude of the polygon centroid in decimal degrees. |
| `centroid_longitude` | `double` | Longitude of the polygon centroid in decimal degrees. |

## MQTT/UNS topic tree

The MQTT feeder publishes JSON (`application/json`) binary-mode CloudEvents with QoS 1 and `retain=false` to the `deforestation` root, used here for DETER deforestation-and-related land-disturbance alerts:

```text
deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert
```

A 7-day MQTT Message Expiry Interval bounds queued delivery for offline durable subscribers. Retain is disabled because DETER alerts are immutable historical events; retaining every `{alert_id}` topic would create an unbounded retained-message graveyard. Consumers should subscribe with wildcards rather than per-alert subscriptions and deduplicate QoS-1 redeliveries by `alert_id`.

Example subscriptions:

- All DETER alerts: `deforestation/br/inpe/inpe-deter-brazil/#`
- Amazon biome only: `deforestation/br/inpe/inpe-deter-brazil/amazon/#`
- Para mining alerts: `deforestation/br/inpe/inpe-deter-brazil/+/pa/mineracao/+/alert`
- One alert regardless of geography/class: `deforestation/br/inpe/inpe-deter-brazil/+/+/+/{alert_id}/alert`
