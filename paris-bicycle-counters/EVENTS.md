# Table of Contents

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
| `counter_id` | *string* | - | `True` | Unique identifier for the counting channel (mapped from 'id_compteur'). |
| `counter_name` | *string* | - | `True` | Human-readable name of the counter including street name and direction (mapped from 'nom_compteur'). |
| `count` | *integer* (optional) | - | `False` | Number of bicycles counted during the one-hour window (mapped from 'sum_counts'). |
| `date` | *datetime* | - | `True` | Start of the one-hour counting window in ISO 8601 format with timezone offset. |
| `longitude` | *double* (optional) | - | `False` | Longitude of the counter location in decimal degrees (WGS 84). |
| `latitude` | *double* (optional) | - | `False` | Latitude of the counter location in decimal degrees (WGS 84). |
