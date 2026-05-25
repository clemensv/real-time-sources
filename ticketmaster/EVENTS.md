# Ticketmaster Discovery API Bridge Events

This bridge polls the [Ticketmaster Discovery API v2](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/) for upcoming public events and emits them as CloudEvents to an Apache Kafka topic.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `Ticketmaster.Events.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Ticketmaster.Events`](#messagegroup-ticketmasterevents) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ticketmaster` |
| Kafka key | `{event_id}` |
| Deployed | False |

### Endpoint `Ticketmaster.Reference.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Ticketmaster.Reference`](#messagegroup-ticketmasterreference) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ticketmaster` |
| Kafka key | `{entity_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Ticketmaster.Events`
<a id="messagegroup-ticketmasterevents"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Ticketmaster.Events.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Ticketmaster.Events.Event`
<a id="message-ticketmastereventsevent"></a>

A Ticketmaster event representing a concert, sports match, theater performance, or other live public event. Emitted when a new event is discovered or when an existing event's status or schedule changes.

| Field | Value |
| --- | --- |
| Name | Event |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Ticketmaster.jstruct/schemas/Ticketmaster.Events.Event`](#schema-ticketmastereventsevent) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Ticketmaster.Events.Event` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/events` |
| `subject` |  | `uritemplate` | `False` | `{event_id}` |
| `time` |  | `uritemplate` | `False` | `{start_datetime_utc}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Ticketmaster.Events.Kafka` | `KAFKA` | topic `ticketmaster`; key `{event_id}` |

### Messagegroup `Ticketmaster.Reference`
<a id="messagegroup-ticketmasterreference"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Ticketmaster.Reference.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `Ticketmaster.Reference.Venue`
<a id="message-ticketmasterreferencevenue"></a>

Reference data for a Ticketmaster venue. Emitted at bridge startup and refreshed periodically. Carries the stable venue identifier, location, address, timezone, and capacity information.

| Field | Value |
| --- | --- |
| Name | Venue |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Ticketmaster.jstruct/schemas/Ticketmaster.Reference.Venue`](#schema-ticketmasterreferencevenue) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Ticketmaster.Reference.Venue` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/venues` |
| `subject` |  | `uritemplate` | `False` | `{entity_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Ticketmaster.Reference.Kafka` | `KAFKA` | topic `ticketmaster`; key `{entity_id}` |

#### Message `Ticketmaster.Reference.Attraction`
<a id="message-ticketmasterreferenceattraction"></a>

Reference data for a Ticketmaster attraction (performer, artist, sports team, or production). Emitted at bridge startup and refreshed periodically. Carries stable attraction identifier, name, and classification.

| Field | Value |
| --- | --- |
| Name | Attraction |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Ticketmaster.jstruct/schemas/Ticketmaster.Reference.Attraction`](#schema-ticketmasterreferenceattraction) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Ticketmaster.Reference.Attraction` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/attractions` |
| `subject` |  | `uritemplate` | `False` | `{entity_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Ticketmaster.Reference.Kafka` | `KAFKA` | topic `ticketmaster`; key `{entity_id}` |

#### Message `Ticketmaster.Reference.Classification`
<a id="message-ticketmasterreferenceclassification"></a>

Reference data for a Ticketmaster classification segment (e.g. Music, Sports, Arts & Theatre). Emitted at bridge startup and refreshed daily. Carries the stable segment identifier, name, and the primary genre and subgenre under that segment.

| Field | Value |
| --- | --- |
| Name | Classification |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Ticketmaster.jstruct/schemas/Ticketmaster.Reference.Classification`](#schema-ticketmasterreferenceclassification) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Ticketmaster.Reference.Classification` |
| `source` |  | `uritemplate` | `False` | `https://app.ticketmaster.com/discovery/v2/classifications` |
| `subject` |  | `uritemplate` | `False` | `{entity_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Ticketmaster.Reference.Kafka` | `KAFKA` | topic `ticketmaster`; key `{entity_id}` |

## Schemagroups

### Schemagroup `Ticketmaster.avro`
<a id="schemagroup-ticketmasteravro"></a>

#### Schema `Ticketmaster.Events.Event`
<a id="schema-ticketmastereventsevent"></a>

| Field | Value |
| --- | --- |
| Name | Event |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Event |
| Namespace | Ticketmaster.Events |
| Type | `record` |
| Doc | A Ticketmaster event representing a concert, sports match, theater performance, or other live public event. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `event_id` | `string` | Stable Ticketmaster event identifier. | `-` |
| `name` | `string` | Human-readable event name. | `-` |
| `type` | `null` \| `string` | Ticketmaster resource type discriminator. | `-` |
| `url` | `null` \| `string` | URL to the event page on Ticketmaster.com. | `-` |
| `locale` | `null` \| `string` | BCP-47 locale string for the event page. | `-` |
| `start_date` | `null` \| `string` | Local calendar date the event starts, YYYY-MM-DD. | `-` |
| `start_time` | `null` \| `string` | Local clock time the event starts, HH:MM:SS. | `-` |
| `start_datetime_local` | `null` \| `string` | Combined local start date and time as ISO 8601. | `-` |
| `start_datetime_utc` | `null` \| `string` | Start date and time in UTC as ISO 8601. | `-` |
| `status` | `null` \| `string` | On-sale status: onsale, offsale, cancelled, postponed, rescheduled. | `-` |
| `segment_id` | `null` \| `string` | Stable classification segment identifier. | `-` |
| `segment_name` | `null` \| `string` | Classification segment name. | `-` |
| `genre_id` | `null` \| `string` | Stable genre identifier within the segment. | `-` |
| `genre_name` | `null` \| `string` | Genre name. | `-` |
| `subgenre_id` | `null` \| `string` | Stable subgenre identifier. | `-` |
| `subgenre_name` | `null` \| `string` | Subgenre name. | `-` |
| `venue_id` | `null` \| `string` | Stable venue identifier. | `-` |
| `venue_name` | `null` \| `string` | Venue name. | `-` |
| `venue_city` | `null` \| `string` | City where the venue is located. | `-` |
| `venue_state_code` | `null` \| `string` | ISO 3166-2 state or province code. | `-` |
| `venue_country_code` | `null` \| `string` | ISO 3166-1 alpha-2 country code. | `-` |
| `venue_latitude` | `null` \| `double` | WGS-84 latitude of the venue. | `-` |
| `venue_longitude` | `null` \| `double` | WGS-84 longitude of the venue. | `-` |
| `price_min` | `null` \| `double` | Minimum face-value ticket price. | `-` |
| `price_max` | `null` \| `double` | Maximum face-value ticket price. | `-` |
| `currency` | `null` \| `string` | ISO 4217 currency code for price fields. | `-` |
| `attraction_ids` | `null` \| `string` | JSON-encoded array of attraction identifiers. | `-` |
| `attraction_names` | `null` \| `string` | JSON-encoded array of attraction names. | `-` |
| `onsale_start_datetime` | `null` \| `string` | UTC datetime when public ticket sales open. | `-` |
| `onsale_end_datetime` | `null` \| `string` | UTC datetime when public ticket sales close. | `-` |
| `info` | `null` \| `string` | General informational text about the event. | `-` |
| `please_note` | `null` \| `string` | Important notes for ticket purchasers. | `-` |

#### Schema `Ticketmaster.Reference.Venue`
<a id="schema-ticketmasterreferencevenue"></a>

| Field | Value |
| --- | --- |
| Name | Venue |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Venue |
| Namespace | Ticketmaster.Reference |
| Type | `record` |
| Doc | Reference data for a Ticketmaster venue. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `entity_id` | `string` | Stable Ticketmaster venue identifier. | `-` |
| `name` | `string` | Human-readable name of the venue. | `-` |
| `url` | `null` \| `string` | URL to the venue page on Ticketmaster.com. | `-` |
| `locale` | `null` \| `string` | BCP-47 locale string. | `-` |
| `timezone` | `null` \| `string` | IANA timezone database name. | `-` |
| `city` | `null` \| `string` | City name. | `-` |
| `state_code` | `null` \| `string` | ISO 3166-2 state or province code. | `-` |
| `country_code` | `null` \| `string` | ISO 3166-1 alpha-2 country code. | `-` |
| `address` | `null` \| `string` | Street address line 1. | `-` |
| `postal_code` | `null` \| `string` | Postal or ZIP code. | `-` |
| `latitude` | `null` \| `double` | WGS-84 latitude in decimal degrees. | `-` |
| `longitude` | `null` \| `double` | WGS-84 longitude in decimal degrees. | `-` |

#### Schema `Ticketmaster.Reference.Attraction`
<a id="schema-ticketmasterreferenceattraction"></a>

| Field | Value |
| --- | --- |
| Name | Attraction |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Attraction |
| Namespace | Ticketmaster.Reference |
| Type | `record` |
| Doc | Reference data for a Ticketmaster attraction (performer, artist, sports team, or production). |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `entity_id` | `string` | Stable Ticketmaster attraction identifier. | `-` |
| `name` | `string` | Human-readable name of the attraction. | `-` |
| `url` | `null` \| `string` | URL to the attraction page on Ticketmaster.com. | `-` |
| `locale` | `null` \| `string` | BCP-47 locale string. | `-` |
| `segment_id` | `null` \| `string` | Stable classification segment identifier. | `-` |
| `segment_name` | `null` \| `string` | Classification segment name. | `-` |
| `genre_id` | `null` \| `string` | Stable genre identifier. | `-` |
| `genre_name` | `null` \| `string` | Genre name. | `-` |
| `subgenre_id` | `null` \| `string` | Stable subgenre identifier. | `-` |
| `subgenre_name` | `null` \| `string` | Subgenre name. | `-` |

#### Schema `Ticketmaster.Reference.Classification`
<a id="schema-ticketmasterreferenceclassification"></a>

| Field | Value |
| --- | --- |
| Name | Classification |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Classification |
| Namespace | Ticketmaster.Reference |
| Type | `record` |
| Doc | Reference data for a Ticketmaster classification segment. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `entity_id` | `string` | Stable Ticketmaster segment identifier. | `-` |
| `name` | `string` | Human-readable segment name. | `-` |
| `type` | `null` \| `string` | Resource type discriminator. | `-` |
| `primary_genre_id` | `null` \| `string` | Stable identifier for the primary genre within this segment. | `-` |
| `primary_genre_name` | `null` \| `string` | Human-readable primary genre name. | `-` |
| `primary_subgenre_id` | `null` \| `string` | Stable identifier for the primary subgenre. | `-` |
| `primary_subgenre_name` | `null` \| `string` | Human-readable primary subgenre name. | `-` |

### Schemagroup `Ticketmaster.jstruct`
<a id="schemagroup-ticketmasterjstruct"></a>

#### Schema `Ticketmaster.Events.Event`
<a id="schema-ticketmastereventsevent"></a>

| Field | Value |
| --- | --- |
| Name | Event |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://raw.githubusercontent.com/clemensv/real-time-sources/main/ticketmaster/xreg/schemas/Ticketmaster.Events.Event` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Ticketmaster/Events/Event` |
| Type | `object` |

###### Object `Event`
<a id="schema-node-event"></a>

A Ticketmaster event representing a concert, sports match, theater performance, or other live public event. Sourced from the Discovery API v2 /events endpoint.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `True` | Stable Ticketmaster event identifier. Globally unique across all event types (e.g. 'G5v0Z9iQkPl_2'). Used as the Kafka message key. | - | - | - |
| `name` | `string` | `True` | Human-readable event name as provided by Ticketmaster (e.g. 'Taylor Swift \\| The Eras Tour'). | - | - | - |
| `type` | `union` | `False` | Ticketmaster resource type discriminator. Usually 'event'. | - | - | - |
| `url` | `union` | `False` | URL to the event page on Ticketmaster.com where tickets can be purchased. | - | - | - |
| `locale` | `union` | `False` | BCP-47 locale string for the event page (e.g. 'en-us', 'en-gb', 'de-de'). | - | - | - |
| `start_date` | `union` | `False` | Local calendar date on which the event starts, in ISO 8601 YYYY-MM-DD format. May be absent for events without a confirmed date (time-to-be-announced). | - | - | - |
| `start_time` | `union` | `False` | Local clock time at which the event starts, in HH:MM:SS format. May be absent when the time is to be announced. | - | - | - |
| `start_datetime_local` | `union` | `False` | Combined local start date and time as an ISO 8601 datetime string (e.g. '2024-07-20T19:30:00'). Not adjusted to UTC. | - | - | - |
| `start_datetime_utc` | `union` | `False` | Start date and time expressed in UTC as an ISO 8601 datetime string (e.g. '2024-07-20T23:30:00Z'). Used as the CloudEvents time attribute. | - | - | - |
| `status` | `union` | `False` | Current on-sale status of the event. Known values: 'onsale' (tickets available), 'offsale' (tickets not available), 'cancelled' (event cancelled), 'postponed' (date changed, new date not yet set), 'rescheduled' (new date confirmed). | - | - | - |
| `segment_id` | `union` | `False` | Stable Ticketmaster classification segment identifier for this event (e.g. 'KZFzniwnSyZfZ7v7nJ' for Music). Corresponds to the top-level category. | - | - | - |
| `segment_name` | `union` | `False` | Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre', 'Film', 'Miscellaneous'). | - | - | - |
| `genre_id` | `union` | `False` | Stable Ticketmaster genre identifier within the segment. Second level of the classification hierarchy. | - | - | - |
| `genre_name` | `union` | `False` | Human-readable genre name (e.g. 'Rock', 'Pop', 'Hip-Hop/Rap', 'Basketball', 'Theatre'). | - | - | - |
| `subgenre_id` | `union` | `False` | Stable Ticketmaster subgenre identifier. Third level of the classification hierarchy, below genre. | - | - | - |
| `subgenre_name` | `union` | `False` | Human-readable subgenre name (e.g. 'Alternative Rock', 'Dance Pop', 'NBA'). | - | - | - |
| `venue_id` | `union` | `False` | Stable Ticketmaster venue identifier for the primary venue where this event takes place. Matches entity_id in a Ticketmaster.Reference.Venue event. | - | - | - |
| `venue_name` | `union` | `False` | Human-readable name of the primary venue (e.g. 'Madison Square Garden'). | - | - | - |
| `venue_city` | `union` | `False` | City where the venue is located. | - | - | - |
| `venue_state_code` | `union` | `False` | ISO 3166-2 state or province code for the venue location (e.g. 'NY', 'CA'). May be absent for non-US/CA venues. | - | - | - |
| `venue_country_code` | `union` | `False` | ISO 3166-1 alpha-2 country code for the venue location (e.g. 'US', 'GB', 'DE'). | - | - | - |
| `venue_latitude` | `union` | `False` | WGS-84 latitude of the venue in decimal degrees. North is positive. | - | - | - |
| `venue_longitude` | `union` | `False` | WGS-84 longitude of the venue in decimal degrees. East is positive. | - | - | - |
| `price_min` | `union` | `False` | Minimum face-value ticket price in the currency indicated by the currency field. Provided by the price_ranges element in the Discovery API response when available. | - | - | - |
| `price_max` | `union` | `False` | Maximum face-value ticket price in the currency indicated by the currency field. Provided by the price_ranges element in the Discovery API response when available. | - | - | - |
| `currency` | `union` | `False` | ISO 4217 currency code for price_min and price_max (e.g. 'USD', 'GBP', 'EUR'). | - | - | - |
| `attraction_ids` | `union` | `False` | JSON-encoded array of Ticketmaster attraction identifiers associated with this event (e.g. '["K8vZ91718H7","K8vZ9179Ki7"]'). Each ID corresponds to an entity_id in a Ticketmaster.Reference.Attraction reference event. | - | - | - |
| `attraction_names` | `union` | `False` | JSON-encoded array of attraction names corresponding to the attraction_ids array (e.g. '["Taylor Swift","Sabrina Carpenter"]'). | - | - | - |
| `onsale_start_datetime` | `union` | `False` | ISO 8601 UTC datetime when public ticket sales open for this event. | - | - | - |
| `onsale_end_datetime` | `union` | `False` | ISO 8601 UTC datetime when public ticket sales close for this event. | - | - | - |
| `info` | `union` | `False` | General informational text about the event as provided by the promoter or Ticketmaster. May include age restrictions, bag policies, or other event notes. | - | - | - |
| `please_note` | `union` | `False` | Important notes for ticket purchasers, such as bag-check policies, camera restrictions, or health and safety requirements. Displayed prominently on the event page. | - | - | - |

#### Schema `Ticketmaster.Reference.Venue`
<a id="schema-ticketmasterreferencevenue"></a>

| Field | Value |
| --- | --- |
| Name | Venue |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://raw.githubusercontent.com/clemensv/real-time-sources/main/ticketmaster/xreg/schemas/Ticketmaster.Reference.Venue` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Ticketmaster/Reference/Venue` |
| Type | `object` |

###### Object `Venue`
<a id="schema-node-venue"></a>

Reference data for a Ticketmaster venue. Carries the venue's stable identifier, location details, timezone, and geographic coordinates as returned by the Discovery API v2 /venues endpoint.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `entity_id` | `string` | `True` | Stable Ticketmaster venue identifier (e.g. 'KovZpaFVAeA'). Used as both the Kafka message key and the CloudEvents subject. Matches the venue_id field in Event records. | - | - | - |
| `name` | `string` | `True` | Human-readable name of the venue as listed on Ticketmaster (e.g. 'Madison Square Garden', 'The O2 Arena'). | - | - | - |
| `url` | `union` | `False` | URL to the venue page on Ticketmaster.com. | - | - | - |
| `locale` | `union` | `False` | BCP-47 locale string for the venue page (e.g. 'en-us'). | - | - | - |
| `timezone` | `union` | `False` | IANA timezone database name for the venue's local time (e.g. 'America/New_York', 'Europe/London'). Used to interpret local start times in Event records. | - | - | - |
| `city` | `union` | `False` | City name where the venue is located. | - | - | - |
| `state_code` | `union` | `False` | ISO 3166-2 state or province code (e.g. 'NY', 'CA'). Populated for US and Canadian venues; absent for most international venues. | - | - | - |
| `country_code` | `union` | `False` | ISO 3166-1 alpha-2 country code (e.g. 'US', 'GB', 'DE', 'AU'). | - | - | - |
| `address` | `union` | `False` | Street address line 1 for the venue (e.g. '4 Pennsylvania Plaza'). | - | - | - |
| `postal_code` | `union` | `False` | Postal or ZIP code for the venue address. | - | - | - |
| `latitude` | `union` | `False` | WGS-84 latitude of the venue in decimal degrees. North is positive. | - | - | - |
| `longitude` | `union` | `False` | WGS-84 longitude of the venue in decimal degrees. East is positive. | - | - | - |

#### Schema `Ticketmaster.Reference.Attraction`
<a id="schema-ticketmasterreferenceattraction"></a>

| Field | Value |
| --- | --- |
| Name | Attraction |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://raw.githubusercontent.com/clemensv/real-time-sources/main/ticketmaster/xreg/schemas/Ticketmaster.Reference.Attraction` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Ticketmaster/Reference/Attraction` |
| Type | `object` |

###### Object `Attraction`
<a id="schema-node-attraction"></a>

Reference data for a Ticketmaster attraction, which represents a performer, musical artist, sports team, theatrical production, or other headline act. Sourced from the Discovery API v2 /attractions endpoint.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `entity_id` | `string` | `True` | Stable Ticketmaster attraction identifier (e.g. 'K8vZ91718H7'). Used as both the Kafka message key and the CloudEvents subject. Matches values in the attraction_ids array of Event records. | - | - | - |
| `name` | `string` | `True` | Human-readable name of the attraction as listed on Ticketmaster (e.g. 'Taylor Swift', 'Los Angeles Lakers'). | - | - | - |
| `url` | `union` | `False` | URL to the attraction page on Ticketmaster.com. | - | - | - |
| `locale` | `union` | `False` | BCP-47 locale string for the attraction page (e.g. 'en-us'). | - | - | - |
| `segment_id` | `union` | `False` | Stable Ticketmaster classification segment identifier for this attraction (e.g. 'KZFzniwnSyZfZ7v7nJ' for Music). Matches entity_id in Classification reference events. | - | - | - |
| `segment_name` | `union` | `False` | Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre'). | - | - | - |
| `genre_id` | `union` | `False` | Stable Ticketmaster genre identifier for this attraction within its segment. | - | - | - |
| `genre_name` | `union` | `False` | Human-readable genre name (e.g. 'Rock', 'Pop', 'Basketball'). | - | - | - |
| `subgenre_id` | `union` | `False` | Stable Ticketmaster subgenre identifier for this attraction. | - | - | - |
| `subgenre_name` | `union` | `False` | Human-readable subgenre name (e.g. 'Alternative Rock', 'Dance Pop'). | - | - | - |

#### Schema `Ticketmaster.Reference.Classification`
<a id="schema-ticketmasterreferenceclassification"></a>

| Field | Value |
| --- | --- |
| Name | Classification |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://raw.githubusercontent.com/clemensv/real-time-sources/main/ticketmaster/xreg/schemas/Ticketmaster.Reference.Classification` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Ticketmaster/Reference/Classification` |
| Type | `object` |

###### Object `Classification`
<a id="schema-node-classification"></a>

Reference data for a Ticketmaster classification segment, which represents the top level of the event classification hierarchy (Music, Sports, Arts & Theatre, Film, Miscellaneous, etc.). Emitted at bridge startup from the Discovery API v2 /classifications endpoint.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `entity_id` | `string` | `True` | Stable Ticketmaster segment identifier (e.g. 'KZFzniwnSyZfZ7v7nJ'). Used as both the Kafka message key and the CloudEvents subject. Matches segment_id in Event and Attraction records. | - | - | - |
| `name` | `string` | `True` | Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre', 'Film', 'Miscellaneous'). | - | - | - |
| `type` | `union` | `False` | Ticketmaster resource type discriminator for this classification entry. Usually 'segment'. | - | - | - |
| `primary_genre_id` | `union` | `False` | Stable identifier for the primary or most prominent genre within this segment. Provided when the API returns a primary_genre sub-object. | - | - | - |
| `primary_genre_name` | `union` | `False` | Human-readable name of the primary genre (e.g. 'Rock', 'Pop', 'Basketball'). | - | - | - |
| `primary_subgenre_id` | `union` | `False` | Stable identifier for the primary subgenre under the primary genre. | - | - | - |
| `primary_subgenre_name` | `union` | `False` | Human-readable name of the primary subgenre. | - | - | - |
