# Xceed Events

## Message Group: `xceed`

### `xceed.Event`

Scheduled nightlife or live-entertainment event from the Xceed Open Event API. Contains event metadata including schedule times, venue details, cover image, and optional external ticket sales link. Emitted as reference data at bridge startup and refreshed periodically.

**CloudEvents Attributes:**
- `type`: `xceed.Event`
- `source`: `{feedurl}` (Xceed Open Event API base URL)
- `subject`: `{event_id}` (Xceed event UUID)

**Kafka Key:** `{event_id}`

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `event_id` | string | Stable UUID assigned by Xceed to uniquely identify this event. Returned as `id` in the /events response. |
| `legacy_id` | int32 \| null | Legacy numeric integer identifier from an earlier Xceed system version (`legacyId`). Null for events created in the current UUID-based system. |
| `name` | string | Human-readable display name of the event as entered by the organiser. |
| `slug` | string \| null | URL-friendly string identifier derived from the event name, suitable for Xceed web URLs. Null for draft or unlisted events. |
| `starting_time` | datetime | Scheduled start time of the event in UTC. Derived from the `startingTime` UNIX epoch seconds value. |
| `ending_time` | datetime \| null | Scheduled end time of the event in UTC. Null if not specified by the organiser. |
| `cover_url` | string \| null | HTTPS URL to the event's main banner or cover image on the Xceed CDN. Null if no image has been uploaded. |
| `external_sales_url` | string \| null | HTTPS URL to an external ticket vendor, when Xceed exposes such a link in the public event payload. Null when no external sales link is published for the event. |
| `venue_id` | string \| null | UUID identifying the venue where the event takes place. Null if venue information is not attached. |
| `venue_name` | string \| null | Display name of the venue (e.g. `Berghain`, `Fabric`, `Pacha Barcelona`). Null if not available. |
| `venue_city` | string \| null | City where the venue is located. Null if not available. |
| `venue_country_code` | string \| null | ISO 3166-1 alpha-2 country code of the venue country (e.g. `DE`, `GB`, `ES`). Null if not available. |

---

