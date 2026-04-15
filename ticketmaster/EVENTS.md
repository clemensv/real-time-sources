# Ticketmaster Discovery API Bridge Events

This document describes the CloudEvents produced by the Ticketmaster Discovery API bridge.

- [Ticketmaster.Events](#message-group-ticketmasterevents)
  - [Ticketmaster.Events.Event](#message-ticketmastereventsevent)
- [Ticketmaster.Reference](#message-group-ticketmasterreference)
  - [Ticketmaster.Reference.Venue](#message-ticketmasterreferencevenue)
  - [Ticketmaster.Reference.Attraction](#message-ticketmasterreferenceattraction)
  - [Ticketmaster.Reference.Classification](#message-ticketmasterreferenceclassification)

---

## Message Group: Ticketmaster.Events
---
### Message: Ticketmaster.Events.Event
*A Ticketmaster event representing a concert, sports match, theater performance, or other live public event. Emitted when a new event is discovered or when an existing event's status or schedule changes.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Ticketmaster.Events.Event` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/events` |
| `subject` |  | `uritemplate` | `False` | `{event_id}` |
| `time` |  | `uritemplate` | `False` | `{start_datetime_utc}` |

#### Schema:
##### Object: Event
*A Ticketmaster event representing a concert, sports match, theater performance, or other live public event. Sourced from the Discovery API v2 /events endpoint.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `event_id` | *string* | - | `True` | Stable Ticketmaster event identifier. Globally unique across all event types (e.g. 'G5v0Z9iQkPl_2'). Used as the Kafka message key. |
| `name` | *string* | - | `True` | Human-readable event name as provided by Ticketmaster (e.g. 'Taylor Swift \| The Eras Tour'). |
| `type` | *string* (optional) | - | `False` | Ticketmaster resource type discriminator. Usually 'event'. |
| `url` | *string* (optional) | - | `False` | URL to the event page on Ticketmaster.com where tickets can be purchased. |
| `locale` | *string* (optional) | - | `False` | BCP-47 locale string for the event page (e.g. 'en-us', 'en-gb', 'de-de'). |
| `start_date` | *string* (optional) | - | `False` | Local calendar date on which the event starts, in ISO 8601 YYYY-MM-DD format. May be absent for events without a confirmed date (time-to-be-announced). |
| `start_time` | *string* (optional) | - | `False` | Local clock time at which the event starts, in HH:MM:SS format. May be absent when the time is to be announced. |
| `start_datetime_local` | *string* (optional) | - | `False` | Combined local start date and time as an ISO 8601 datetime string (e.g. '2024-07-20T19:30:00'). Not adjusted to UTC. |
| `start_datetime_utc` | *string* (optional) | - | `False` | Start date and time expressed in UTC as an ISO 8601 datetime string (e.g. '2024-07-20T23:30:00Z'). Used as the CloudEvents time attribute. |
| `status` | *string* (optional) | - | `False` | Current on-sale status of the event. Known values: 'onsale' (tickets available), 'offsale' (tickets not available), 'cancelled' (event cancelled), 'postponed' (date changed, new date not yet set), 'rescheduled' (new date confirmed). |
| `segment_id` | *string* (optional) | - | `False` | Stable Ticketmaster classification segment identifier for this event (e.g. 'KZFzniwnSyZfZ7v7nJ' for Music). Corresponds to the top-level category. |
| `segment_name` | *string* (optional) | - | `False` | Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre', 'Film', 'Miscellaneous'). |
| `genre_id` | *string* (optional) | - | `False` | Stable Ticketmaster genre identifier within the segment. Second level of the classification hierarchy. |
| `genre_name` | *string* (optional) | - | `False` | Human-readable genre name (e.g. 'Rock', 'Pop', 'Hip-Hop/Rap', 'Basketball', 'Theatre'). |
| `subgenre_id` | *string* (optional) | - | `False` | Stable Ticketmaster subgenre identifier. Third level of the classification hierarchy, below genre. |
| `subgenre_name` | *string* (optional) | - | `False` | Human-readable subgenre name (e.g. 'Alternative Rock', 'Dance Pop', 'NBA'). |
| `venue_id` | *string* (optional) | - | `False` | Stable Ticketmaster venue identifier for the primary venue where this event takes place. Matches entity_id in a Ticketmaster.Reference.Venue event. |
| `venue_name` | *string* (optional) | - | `False` | Human-readable name of the primary venue (e.g. 'Madison Square Garden'). |
| `venue_city` | *string* (optional) | - | `False` | City where the venue is located. |
| `venue_state_code` | *string* (optional) | - | `False` | ISO 3166-2 state or province code for the venue location (e.g. 'NY', 'CA'). May be absent for non-US/CA venues. |
| `venue_country_code` | *string* (optional) | - | `False` | ISO 3166-1 alpha-2 country code for the venue location (e.g. 'US', 'GB', 'DE'). |
| `venue_latitude` | *double* (optional) | - | `False` | WGS-84 latitude of the venue in decimal degrees. North is positive. |
| `venue_longitude` | *double* (optional) | - | `False` | WGS-84 longitude of the venue in decimal degrees. East is positive. |
| `price_min` | *double* (optional) | - | `False` | Minimum face-value ticket price in the currency indicated by the currency field. Provided by the price_ranges element in the Discovery API response when available. |
| `price_max` | *double* (optional) | - | `False` | Maximum face-value ticket price in the currency indicated by the currency field. Provided by the price_ranges element in the Discovery API response when available. |
| `currency` | *string* (optional) | - | `False` | ISO 4217 currency code for price_min and price_max (e.g. 'USD', 'GBP', 'EUR'). |
| `attraction_ids` | *string* (optional) | - | `False` | JSON-encoded array of Ticketmaster attraction identifiers associated with this event (e.g. '["K8vZ91718H7","K8vZ9179Ki7"]'). Each ID corresponds to an entity_id in a Ticketmaster.Reference.Attraction reference event. |
| `attraction_names` | *string* (optional) | - | `False` | JSON-encoded array of attraction names corresponding to the attraction_ids array (e.g. '["Taylor Swift","Sabrina Carpenter"]'). |
| `onsale_start_datetime` | *string* (optional) | - | `False` | ISO 8601 UTC datetime when public ticket sales open for this event. |
| `onsale_end_datetime` | *string* (optional) | - | `False` | ISO 8601 UTC datetime when public ticket sales close for this event. |
| `info` | *string* (optional) | - | `False` | General informational text about the event as provided by the promoter or Ticketmaster. May include age restrictions, bag policies, or other event notes. |
| `please_note` | *string* (optional) | - | `False` | Important notes for ticket purchasers, such as bag-check policies, camera restrictions, or health and safety requirements. Displayed prominently on the event page. |
## Message Group: Ticketmaster.Reference
---
### Message: Ticketmaster.Reference.Venue
*Reference data for a Ticketmaster venue. Emitted at bridge startup and refreshed periodically. Carries the stable venue identifier, location, address, timezone, and capacity information.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Ticketmaster.Reference.Venue` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/venues` |
| `subject` |  | `uritemplate` | `False` | `{entity_id}` |

#### Schema:
##### Object: Venue
*Reference data for a Ticketmaster venue. Carries the venue's stable identifier, location details, timezone, and geographic coordinates as returned by the Discovery API v2 /venues endpoint.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `entity_id` | *string* | - | `True` | Stable Ticketmaster venue identifier (e.g. 'KovZpaFVAeA'). Used as both the Kafka message key and the CloudEvents subject. Matches the venue_id field in Event records. |
| `name` | *string* | - | `True` | Human-readable name of the venue as listed on Ticketmaster (e.g. 'Madison Square Garden', 'The O2 Arena'). |
| `url` | *string* (optional) | - | `False` | URL to the venue page on Ticketmaster.com. |
| `locale` | *string* (optional) | - | `False` | BCP-47 locale string for the venue page (e.g. 'en-us'). |
| `timezone` | *string* (optional) | - | `False` | IANA timezone database name for the venue's local time (e.g. 'America/New_York', 'Europe/London'). Used to interpret local start times in Event records. |
| `city` | *string* (optional) | - | `False` | City name where the venue is located. |
| `state_code` | *string* (optional) | - | `False` | ISO 3166-2 state or province code (e.g. 'NY', 'CA'). Populated for US and Canadian venues; absent for most international venues. |
| `country_code` | *string* (optional) | - | `False` | ISO 3166-1 alpha-2 country code (e.g. 'US', 'GB', 'DE', 'AU'). |
| `address` | *string* (optional) | - | `False` | Street address line 1 for the venue (e.g. '4 Pennsylvania Plaza'). |
| `postal_code` | *string* (optional) | - | `False` | Postal or ZIP code for the venue address. |
| `latitude` | *double* (optional) | - | `False` | WGS-84 latitude of the venue in decimal degrees. North is positive. |
| `longitude` | *double* (optional) | - | `False` | WGS-84 longitude of the venue in decimal degrees. East is positive. |
---
### Message: Ticketmaster.Reference.Attraction
*Reference data for a Ticketmaster attraction (performer, artist, sports team, or production). Emitted at bridge startup and refreshed periodically. Carries stable attraction identifier, name, and classification.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Ticketmaster.Reference.Attraction` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/attractions` |
| `subject` |  | `uritemplate` | `False` | `{entity_id}` |

#### Schema:
##### Object: Attraction
*Reference data for a Ticketmaster attraction, which represents a performer, musical artist, sports team, theatrical production, or other headline act. Sourced from the Discovery API v2 /attractions endpoint.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `entity_id` | *string* | - | `True` | Stable Ticketmaster attraction identifier (e.g. 'K8vZ91718H7'). Used as both the Kafka message key and the CloudEvents subject. Matches values in the attraction_ids array of Event records. |
| `name` | *string* | - | `True` | Human-readable name of the attraction as listed on Ticketmaster (e.g. 'Taylor Swift', 'Los Angeles Lakers'). |
| `url` | *string* (optional) | - | `False` | URL to the attraction page on Ticketmaster.com. |
| `locale` | *string* (optional) | - | `False` | BCP-47 locale string for the attraction page (e.g. 'en-us'). |
| `segment_id` | *string* (optional) | - | `False` | Stable Ticketmaster classification segment identifier for this attraction (e.g. 'KZFzniwnSyZfZ7v7nJ' for Music). Matches entity_id in Classification reference events. |
| `segment_name` | *string* (optional) | - | `False` | Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre'). |
| `genre_id` | *string* (optional) | - | `False` | Stable Ticketmaster genre identifier for this attraction within its segment. |
| `genre_name` | *string* (optional) | - | `False` | Human-readable genre name (e.g. 'Rock', 'Pop', 'Basketball'). |
| `subgenre_id` | *string* (optional) | - | `False` | Stable Ticketmaster subgenre identifier for this attraction. |
| `subgenre_name` | *string* (optional) | - | `False` | Human-readable subgenre name (e.g. 'Alternative Rock', 'Dance Pop'). |
---
### Message: Ticketmaster.Reference.Classification
*Reference data for a Ticketmaster classification segment (e.g. Music, Sports, Arts & Theatre). Emitted at bridge startup and refreshed daily. Carries the stable segment identifier, name, and the primary genre and subgenre under that segment.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Ticketmaster.Reference.Classification` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/classifications` |
| `subject` |  | `uritemplate` | `False` | `{entity_id}` |

#### Schema:
##### Object: Classification
*Reference data for a Ticketmaster classification segment, which represents the top level of the event classification hierarchy (Music, Sports, Arts & Theatre, Film, Miscellaneous, etc.). Emitted at bridge startup from the Discovery API v2 /classifications endpoint.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `entity_id` | *string* | - | `True` | Stable Ticketmaster segment identifier (e.g. 'KZFzniwnSyZfZ7v7nJ'). Used as both the Kafka message key and the CloudEvents subject. Matches segment_id in Event and Attraction records. |
| `name` | *string* | - | `True` | Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre', 'Film', 'Miscellaneous'). |
| `type` | *string* (optional) | - | `False` | Ticketmaster resource type discriminator for this classification entry. Usually 'segment'. |
| `primary_genre_id` | *string* (optional) | - | `False` | Stable identifier for the primary or most prominent genre within this segment. Provided when the API returns a primary_genre sub-object. |
| `primary_genre_name` | *string* (optional) | - | `False` | Human-readable name of the primary genre (e.g. 'Rock', 'Pop', 'Basketball'). |
| `primary_subgenre_id` | *string* (optional) | - | `False` | Stable identifier for the primary subgenre under the primary genre. |
| `primary_subgenre_name` | *string* (optional) | - | `False` | Human-readable name of the primary subgenre. |
