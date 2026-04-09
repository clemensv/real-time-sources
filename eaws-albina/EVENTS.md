# EAWS ALBINA Avalanche Bulletin Bridge Events

This document describes the events emitted by the EAWS ALBINA Avalanche Bulletin Bridge.

- [org.EAWS.ALBINA.Bulletins](#message-group-orgeawsalbinabulletins)
  - [org.EAWS.ALBINA.AvalancheBulletin](#message-orgeawsalbinaavalanchebulletin)

---

## Message Group: org.EAWS.ALBINA.Bulletins

---

### Message: org.EAWS.ALBINA.AvalancheBulletin

Daily avalanche danger bulletin for a specific micro-region in the European Alps, published by the EAWS ALBINA system in CAAMLv6 format.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `org.EAWS.ALBINA.AvalancheBulletin` |
| `source` | CloudEvent source | `string` | `True` | `https://avalanche.report` |
| `subject` | EAWS micro-region identifier | `uritemplate` | `True` | `{region_id}` |

#### Schema: AvalancheBulletin

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `region_id` | *string* | EAWS micro-region identifier (e.g. AT-07-04-02) |
| `region_name` | *string* | Human-readable name of the micro-region |
| `bulletin_id` | *string* | Unique UUID of the bulletin |
| `publication_time` | *datetime* | When the bulletin was published |
| `valid_time_start` | *datetime* | Start of the validity period |
| `valid_time_end` | *datetime* | End of the validity period |
| `lang` | *string* | Language code (en, de, it) |
| `max_danger_rating` | *string (nullable, enum)* | Highest EAWS danger rating: low, moderate, considerable, high, very_high |
| `max_danger_rating_value` | *int32 (nullable)* | Numeric danger rating (1-5) |
| `danger_ratings_json` | *string* | JSON array of CAAMLv6 danger ratings with elevation bands and time periods |
| `avalanche_problems_json` | *string* | JSON array of CAAMLv6 avalanche problems (problem type, aspects, elevation, size) |
| `tendency_type` | *string (nullable)* | Danger tendency: decreasing, steady, or increasing |
| `danger_patterns_json` | *string (nullable)* | JSON array of LWD Tyrol danger pattern codes (e.g. DP10, DP4) |
| `avalanche_activity_highlights` | *string (nullable)* | Summary of avalanche activity conditions |
| `snowpack_structure_comment` | *string (nullable)* | Description of snowpack structure and layering |
