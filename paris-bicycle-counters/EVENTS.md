# Table of Contents

## MQTT/UNS topics

The MQTT feeder publishes binary-mode CloudEvents under `traffic/fr/paris/paris-bicycle-counters/{counter_id}/{event}`:

- `traffic/fr/paris/paris-bicycle-counters/{counter_id}/info` — retained QoS 1 counter reference records.
- `traffic/fr/paris/paris-bicycle-counters/{counter_id}/count` — non-retained QoS 1 hourly bicycle count events.

Recommended bootstrap flow: subscribe to `traffic/fr/paris/paris-bicycle-counters/+/info` first to populate a retained counter cache, then subscribe to `traffic/fr/paris/paris-bicycle-counters/+/count` for live count events. Example subscriptions: all Paris bicycle counter events: `traffic/fr/paris/paris-bicycle-counters/#`; one counter: `traffic/fr/paris/paris-bicycle-counters/{counter_id}/#`; live count events only: `traffic/fr/paris/paris-bicycle-counters/+/count`.

- [FR.Paris.OpenData.Velo](#message-group-frparisopendatavelo)
  - [FR.Paris.OpenData.Velo.Counter](#message-frparisopendatavelocounter)
  - [FR.Paris.OpenData.Velo.BicycleCount](#message-frparisopendatavelobicyclecount)

---

## Message Group: FR.Paris.OpenData.Velo
---
### Message: FR.Paris.OpenData.Velo.Counter
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `FR.Paris.OpenData.Velo.Counter` |
| `source` |  | `` | `False` | `https://opendata.paris.fr/explore/dataset/comptage-velo-compteurs` |
| `subject` |  | `uritemplate` | `False` | `{counter_id}` |

#### Schema:
##### Object: Counter
*Reference record describing a permanent bicycle counting station in Paris, including its identifier, display name, directional channel, installation date, and geographic coordinates.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `ce_id` | *string* | - | `True` | Deterministic CloudEvents id for the retained counter reference record. |
| `counter_id` | *string* | - | `True` | Unique identifier for the counting channel, combining the site ID and channel ID (mapped from 'id_compteur'). |
| `counter_name` | *string* | - | `True` | Human-readable name of the counter including street name and direction (mapped from 'nom_compteur'). |
| `channel_name` | *string* (optional) | - | `False` | Directional channel label for the counter, e.g. 'SE-NO' or 'E-O' (mapped from 'channel_name'). |
| `installation_date` | *string* (optional) | - | `False` | Date when the counter was installed, in ISO 8601 date format (YYYY-MM-DD). |
| `longitude` | *double* (optional) | - | `False` | Longitude of the counter location in decimal degrees (WGS 84). |
| `latitude` | *double* (optional) | - | `False` | Latitude of the counter location in decimal degrees (WGS 84). |
---
### Message: FR.Paris.OpenData.Velo.BicycleCount
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `FR.Paris.OpenData.Velo.BicycleCount` |
| `source` |  | `` | `False` | `https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs` |
| `subject` |  | `uritemplate` | `False` | `{counter_id}` |

#### Schema:
##### Object: BicycleCount
*Hourly bicycle count observation from a permanent counting station in Paris, reporting the number of bicycles detected during a one-hour window.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `ce_id` | *string* | - | `True` | Deterministic CloudEvents id composed from counter_id and hourly count date. |
| `counter_id` | *string* | - | `True` | Unique identifier for the counting channel (mapped from 'id_compteur'). |
| `counter_name` | *string* | - | `True` | Human-readable name of the counter including street name and direction (mapped from 'nom_compteur'). |
| `count` | *integer* (optional) | - | `False` | Number of bicycles counted during the one-hour window (mapped from 'sum_counts'). |
| `date` | *datetime* | - | `True` | Start of the one-hour counting window in ISO 8601 format with timezone offset. |
| `longitude` | *double* (optional) | - | `False` | Longitude of the counter location in decimal degrees (WGS 84). |
| `latitude` | *double* (optional) | - | `False` | Latitude of the counter location in decimal degrees (WGS 84). |
