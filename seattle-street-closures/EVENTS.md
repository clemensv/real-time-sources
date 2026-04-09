# Seattle Street Closures Bridge Events

This document describes the events emitted by the Seattle street closures bridge.

- [US.WA.Seattle.StreetClosures](#message-group-uswaseattlestreetclosures)
  - [US.WA.Seattle.StreetClosures.StreetClosure](#message-uswaseattlestreetclosuresstreetclosure)

---

## Message Group: US.WA.Seattle.StreetClosures
---
### Message: US.WA.Seattle.StreetClosures.StreetClosure
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `US.WA.Seattle.StreetClosures.StreetClosure` |
| `source` |  | `` | `False` | `https://data.seattle.gov/Built-Environment/Street-Closures/ium9-iqtc` |
| `subject` |  | `uritemplate` | `False` | `{closure_id}` |

#### Schema:
##### Object: StreetClosure
*Street closure row from the Seattle Department of Transportation street closures dataset, describing one closed street segment and its active occurrence window.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `closure_id` | *string* | - | `True` | Derived stable identity for the closure row, composed from permit number, street segment key, start date, and end date. |
| `permit_number` | *string* | - | `True` | Identifier for the permit record granting authorization to close the street. |
| `permit_type` | *string* | - | `True` | Type of permit, such as Block Party, Play Street, Farmers Market, or Temporary Activation. |
| `project_name` | *string* (optional) | - | `False` | Short title used by Seattle to quickly identify the closure permit. |
| `project_description` | *string* (optional) | - | `False` | Longer description of the permit, including issuance notes and closure details. |
| `start_date` | *string* | - | `True` | Date on which the closure event begins, normalized to YYYY-MM-DD. |
| `end_date` | *string* | - | `True` | Date on which the closure event ends, normalized to YYYY-MM-DD. |
| `sunday` | *string* (optional) | - | `False` | Time period, if any, during which the closure occurs on Sundays between the start and end dates. |
| `monday` | *string* (optional) | - | `False` | Time period, if any, during which the closure occurs on Mondays between the start and end dates. |
| `tuesday` | *string* (optional) | - | `False` | Time period, if any, during which the closure occurs on Tuesdays between the start and end dates. |
| `wednesday` | *string* (optional) | - | `False` | Time period, if any, during which the closure occurs on Wednesdays between the start and end dates. |
| `thursday` | *string* (optional) | - | `False` | Time period, if any, during which the closure occurs on Thursdays between the start and end dates. |
| `friday` | *string* (optional) | - | `False` | Time period, if any, during which the closure occurs on Fridays between the start and end dates. |
| `saturday` | *string* (optional) | - | `False` | Time period, if any, during which the closure occurs on Saturdays between the start and end dates. |
| `street_on` | *string* (optional) | - | `False` | Street name of the closed street segment. |
| `street_from` | *string* (optional) | - | `False` | Name of the intersecting street at the low end of the closed segment. |
| `street_to` | *string* (optional) | - | `False` | Name of the intersecting street at the high end of the closed segment. |
| `segkey` | *string* (optional) | - | `False` | Identifier for the street segment that is closed. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized GeoJSON LineString geometry for the closed street block. |
