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
| `external_sales_url` | string \| null | HTTPS URL to an external ticket vendor, when tickets are sold outside the Xceed platform. Null when tickets are sold via Xceed admissions. |
| `venue_id` | string \| null | UUID identifying the venue where the event takes place. Null if venue information is not attached. |
| `venue_name` | string \| null | Display name of the venue (e.g. `Berghain`, `Fabric`, `Pacha Barcelona`). Null if not available. |
| `venue_city` | string \| null | City where the venue is located. Null if not available. |
| `venue_country_code` | string \| null | ISO 3166-1 alpha-2 country code of the venue country (e.g. `DE`, `GB`, `ES`). Null if not available. |

---

## Message Group: `xceed.admissions`

### `xceed.EventAdmission`

Ticket-availability snapshot for a single admission tier of an Xceed event, retrieved from the `/events/:eventId/admissions` endpoint. An event may have multiple admission tiers (e.g. Early Bird, General Admission, VIP). Each tier carries real-time sales-state signals including `is_sold_out` and `is_sales_closed`. Emitted on every polling cycle.

**CloudEvents Attributes:**
- `type`: `xceed.EventAdmission`
- `source`: `{feedurl}` (Xceed Open Event API base URL)
- `subject`: `{event_id}/{admission_id}` (parent event UUID / admission tier UUID)

**Kafka Key:** `{event_id}/{admission_id}`

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `event_id` | string | UUID of the parent Xceed event. Matches the `event_id` field in the corresponding `xceed.Event` record. |
| `admission_id` | string | Stable UUID identifying this admission tier within its parent event. Returned as `id` in the /events/:eventId/admissions response. |
| `name` | string \| null | Human-readable label for this admission tier (e.g. `Early Bird`, `General Admission`, `VIP Access`). Null if no label is set. |
| `is_sold_out` | boolean \| null | True if all available tickets for this tier have been sold. False means tickets are still available. Null if not present in the API response. |
| `is_sales_closed` | boolean \| null | True if ticket sales for this tier have been closed (due to event start, expired sales window, or manual close). Null if not present. |
| `price` | double \| null | Ticket price in the currency specified by `currency`. Null for free events, guest-list admissions, or when pricing is not exposed publicly. |
| `currency` | string \| null | ISO 4217 three-letter currency code for `price` (e.g. `EUR`, `GBP`). Null when price is null or not provided. |
| `remaining` | int32 \| null | Number of tickets remaining at poll time. Null when not tracked or not exposed by the API. Value of 0 typically accompanies `is_sold_out=true`. |
