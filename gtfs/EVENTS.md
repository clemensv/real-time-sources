# GTFS and GTFS-RT API Bridge Usage Guide Events

**GTFS and GTFS-RT API Bridge** is a tool that fetches GTFS (General Transit Feed Specification) Realtime and Static data from various transit agency sources, processes the data, and publishes it to Kafka topics using SASL PLAIN authentication. This tool can be integrated with systems like Microsoft Event Hubs or Microsoft Fabric Event Streams.

## At a glance

- **Event types:** 31 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 31 telemetry event types.
- **Identity:** `{agencyid}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `gtfs`. The record key is `{agencyid}`. In plain language, `{agencyid}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['gtfs'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Vehicle Position

CloudEvents type: `GeneralTransitFeedRealTime.Vehicle.VehiclePosition`

#### What it tells you

Realtime positioning information for a given vehicle.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Vehicle Position` payloads are JSON object. No required field list is declared.

- **`trip`** (object, optional): The Trip that this vehicle is serving. Can be empty or partial if the vehicle can not be identified with a given trip instance. See [TripDescriptor](#payload-generaltransitfeedrealtime-vehicle-vehicleposition-tripdescriptor).
- **`vehicle`** (object, optional): Additional information on the vehicle that is serving this trip. See [VehicleDescriptor](#payload-generaltransitfeedrealtime-vehicle-vehicleposition-vehicledescriptor).
- **`position`** (object, optional): Current position of this vehicle. The stop sequence index of the current stop. The meaning of See [Position](#payload-generaltransitfeedrealtime-vehicle-vehicleposition-position).
- **`current_stop_sequence`** (int32, optional): current_stop_sequence (i.e., the stop that it refers to) is determined by current_status. If current_status is missing IN_TRANSIT_TO is assumed. Identifies the current stop. The value must be the same as in stops.txt in
- **`stop_id`** (string, optional): the corresponding GTFS feed.
- **`current_status`** (enum, optional): The exact status of the vehicle with respect to the current stop. Ignored if current_stop_sequence is missing. Moment at which the vehicle's position was measured. In POSIX time
- **`timestamp`** (int64, optional): (i.e., number of seconds since January 1st 1970 00:00:00 UTC).
- **`congestion_level`** (enum, optional): Congestion level that is affecting this vehicle.
- **`occupancy_status`** (enum, optional): The degree of passenger occupancy of the vehicle. This field is still experimental, and subject to change. It may be formally adopted in the future.
##### `current_status` values

- `INCOMING_AT`
- `STOPPED_AT`
- `IN_TRANSIT_TO`
##### `congestion_level` values

- `UNKNOWN_CONGESTION_LEVEL`
- `RUNNING_SMOOTHLY`
- `STOP_AND_GO`
- `CONGESTION`
- `SEVERE_CONGESTION`
##### `occupancy_status` values

- `EMPTY`
- `MANY_SEATS_AVAILABLE`
- `FEW_SEATS_AVAILABLE`
- `STANDING_ROOM_ONLY`
- `CRUSHED_STANDING_ROOM_ONLY`
- `FULL`
- `NOT_ACCEPTING_PASSENGERS`
##### `schedule_relationship` values

- `SCHEDULED`
- `ADDED`
- `UNSCHEDULED`
- `CANCELED`
##### TripDescriptor
<a id="payload-generaltransitfeedrealtime-vehicle-vehicleposition-tripdescriptor"></a>

A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary, start_time) is set. If route_id is also set, then it should be same as one that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be set. Note that if the trip_id is not known, then stop sequence ids in TripUpdate are not sufficient, and stop_ids must be provided as well. In addition, absolute arrival/departure times must be provided.

- **`trip_id`** (string, optional): The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary.
- **`route_id`** (string, optional): The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the
- **`direction_id`** (int32, optional): direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future.
- **`start_time`** (string, optional): The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance.
- **`start_date`** (string, optional): Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format.
- **`schedule_relationship`** (enum, optional): The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.
##### VehicleDescriptor
<a id="payload-generaltransitfeedrealtime-vehicle-vehicleposition-vehicledescriptor"></a>

Identification information for the vehicle performing the trip.

- **`id`** (string, optional): Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to
- **`label`** (string, optional): help identify the correct vehicle.
- **`license_plate`** (string, optional): The license plate of the vehicle.
##### Position
<a id="payload-generaltransitfeedrealtime-vehicle-vehicleposition-position"></a>

A position.

- **`latitude`** (float, required): Degrees North, in the WGS-84 coordinate system.
- **`longitude`** (float, required): Degrees East, in the WGS-84 coordinate system.
- **`bearing`** (float, optional): Bearing, in degrees, clockwise from North, i.e., 0 is North and 90 is East. This can be the compass bearing, or the direction towards the next stop or intermediate location. This should not be direction deduced from the sequence of previous positions, which can be computed from previous data.
- **`odometer`** (double, optional): Odometer value, in meters.
- **`speed`** (float, optional): Momentary speed measured by the vehicle, in meters per second.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "trip": {
    "trip_id": "string",
    "route_id": "string",
    "direction_id": 0,
    "start_time": "string",
    "start_date": "string",
    "schedule_relationship": "SCHEDULED"
  },
  "vehicle": {
    "id": "string",
    "label": "string",
    "license_plate": "string"
  },
  "position": {
    "latitude": 0,
    "longitude": 0,
    "bearing": 0,
    "odometer": 0,
    "speed": 0
  },
  "current_stop_sequence": 0,
  "stop_id": "string",
  "current_status": "INCOMING_AT",
  "timestamp": 0,
  "congestion_level": "UNKNOWN_CONGESTION_LEVEL",
  "occupancy_status": "EMPTY"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Trip Update

CloudEvents type: `GeneralTransitFeedRealTime.Trip.TripUpdate`

#### What it tells you

Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Trip Update` payloads are JSON object. Required fields: `trip`, `stop_time_update`.

- **`trip`** (object, required): The Trip that this message applies to. There can be at most one TripUpdate entity for each actual trip instance. If there is none, that means there is no prediction information available. It does *not* mean that the trip is progressing according to schedule. See [TripDescriptor](#payload-generaltransitfeedrealtime-trip-tripupdate-tripdescriptor).
- **`vehicle`** (object, optional): Additional information on the vehicle that is serving this trip. See [VehicleDescriptor](#payload-generaltransitfeedrealtime-trip-tripupdate-vehicledescriptor).
- **`stop_time_update`** (array of object, required): Updates to StopTimes for the trip (both future, i.e., predictions, and in some cases, past ones, i.e., those that already happened). The updates must be sorted by stop_sequence, and apply for all the following stops of the trip up to the next specified one. Example 1: For a trip with 20 stops, a StopTimeUpdate with arrival delay and departure delay of 0 for stop_sequence of the current stop means that the trip is exactly on time. Example 2: For the same trip instance, 3 StopTimeUpdates are provided: - delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 - delay of unspecified duration for stop_sequence 10 This will be interpreted as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9 have delay of 1 min. - stop_sequences 10,... have unknown delay. Moment at which the vehicle's real-time progress was measured. In POSIX
- **`timestamp`** (int64, optional): time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC). The current schedule deviation for the trip. Delay should only be
- **`delay`** (int32, optional): specified when the prediction is given relative to some existing schedule in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time. Delay information in StopTimeUpdates take precedent of trip-level delay information, such that trip-level delay is only propagated until the next stop along the trip with a StopTimeUpdate delay value specified. Feed providers are strongly encouraged to provide a TripUpdate.timestamp value indicating when the delay value was last updated, in order to evaluate the freshness of the data. NOTE: This field is still experimental, and subject to change. It may be formally adopted in the future.
##### `schedule_relationship` values

- `SCHEDULED`
- `ADDED`
- `UNSCHEDULED`
- `CANCELED`
##### TripDescriptor
<a id="payload-generaltransitfeedrealtime-trip-tripupdate-tripdescriptor"></a>

A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary, start_time) is set. If route_id is also set, then it should be same as one that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be set. Note that if the trip_id is not known, then stop sequence ids in TripUpdate are not sufficient, and stop_ids must be provided as well. In addition, absolute arrival/departure times must be provided.

- **`trip_id`** (string, optional): The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary.
- **`route_id`** (string, optional): The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the
- **`direction_id`** (int32, optional): direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future.
- **`start_time`** (string, optional): The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance.
- **`start_date`** (string, optional): Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format.
- **`schedule_relationship`** (enum, optional): The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.
##### VehicleDescriptor
<a id="payload-generaltransitfeedrealtime-trip-tripupdate-vehicledescriptor"></a>

Identification information for the vehicle performing the trip.

- **`id`** (string, optional): Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to
- **`label`** (string, optional): help identify the correct vehicle.
- **`license_plate`** (string, optional): The license plate of the vehicle.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "trip": {
    "trip_id": "string",
    "route_id": "string",
    "direction_id": 0,
    "start_time": "string",
    "start_date": "string",
    "schedule_relationship": "SCHEDULED"
  },
  "vehicle": {
    "id": "string",
    "label": "string",
    "license_plate": "string"
  },
  "stop_time_update": [
    {
      "stop_sequence": 0,
      "stop_id": "string",
      "arrival": {
        "delay": 0,
        "time": 0,
        "uncertainty": 0
      },
      "departure": {},
      "schedule_relationship": "SCHEDULED"
    }
  ],
  "timestamp": 0,
  "delay": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Alert

CloudEvents type: `GeneralTransitFeedRealTime.Alert.Alert`

#### What it tells you

An alert, indicating some sort of incident in the public transit network.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Alert` payloads are JSON object. Required fields: `active_period`, `informed_entity`.

- **`active_period`** (array of object, required): Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them.
- **`informed_entity`** (array of object, required): Entities whose users we should notify of this alert.
- **`cause`** (enum, optional): Cause of this alert.
- **`effect`** (enum, optional): What is the effect of this problem on the affected entity.
- **`url`** (object, optional): The URL which provides additional information about the alert. See [TranslatedString](#payload-generaltransitfeedrealtime-alert-alert-translatedstring).
- **`header_text`** (object, optional): Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the See [TranslatedString](#payload-generaltransitfeedrealtime-alert-alert-translatedstring).
- **`description_text`** (object, optional): description should add to the information of the header. See [TranslatedString](#payload-generaltransitfeedrealtime-alert-alert-translatedstring).
##### `cause` values

- `UNKNOWN_CAUSE`
- `OTHER_CAUSE`
- `TECHNICAL_PROBLEM`
- `STRIKE`
- `DEMONSTRATION`
- `ACCIDENT`
- `HOLIDAY`
- `WEATHER`
- `MAINTENANCE`
- `CONSTRUCTION`
- `POLICE_ACTIVITY`
- `MEDICAL_EMERGENCY`
##### `effect` values

- `NO_SERVICE`
- `REDUCED_SERVICE`
- `SIGNIFICANT_DELAYS`
- `DETOUR`
- `ADDITIONAL_SERVICE`
- `MODIFIED_SERVICE`
- `OTHER_EFFECT`
- `UNKNOWN_EFFECT`
- `STOP_MOVED`
##### TranslatedString
<a id="payload-generaltransitfeedrealtime-alert-alert-translatedstring"></a>

An internationalized message containing per-language versions of a snippet of text or a URL. One of the strings from a message will be picked up. The resolution proceeds as follows: 1. If the UI language matches the language code of a translation, the first matching translation is picked. 2. If a default UI language (e.g., English) matches the language code of a translation, the first matching translation is picked. 3. If some translation has an unspecified language code, that translation is picked.

- **`translation`** (array of object, required): At least one translation must be provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "active_period": [
    {
      "start": 0,
      "end": 0
    }
  ],
  "informed_entity": [
    {
      "agency_id": "string",
      "route_id": "string",
      "route_type": 0,
      "trip": {
        "trip_id": "string",
        "route_id": "string",
        "direction_id": 0,
        "start_time": "string",
        "start_date": "string",
        "schedule_relationship": "SCHEDULED"
      },
      "stop_id": "string"
    }
  ],
  "cause": "UNKNOWN_CAUSE",
  "effect": "NO_SERVICE",
  "url": {
    "translation": [
      {
        "text": "string",
        "language": "string"
      }
    ]
  },
  "header_text": {},
  "description_text": {}
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Agency

CloudEvents type: `GeneralTransitFeedStatic.Agency`

#### What it tells you

Information about the transit agencies.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Agency` payloads are JSON object. Required fields: `agencyId`, `agencyName`, `agencyUrl`, `agencyTimezone`.

- **`agencyId`** (string, required): Identifies a transit brand which is often synonymous with a transit agency.
- **`agencyName`** (string, required): Full name of the transit agency.
- **`agencyUrl`** (string, required): URL of the transit agency.
- **`agencyTimezone`** (string, required): Timezone where the transit agency is located.
- **`agencyLang`** (string, optional): Primary language used by this transit agency.
- **`agencyPhone`** (string, optional): A voice telephone number for the specified agency.
- **`agencyFareUrl`** (string, optional): URL of a web page that allows a rider to purchase tickets or other fare instruments for that agency online.
- **`agencyEmail`** (string, optional): Email address actively monitored by the agency’s customer service department.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "agencyId": "string",
  "agencyName": "string",
  "agencyUrl": "string",
  "agencyTimezone": "string",
  "agencyLang": "string",
  "agencyPhone": "string",
  "agencyFareUrl": "string",
  "agencyEmail": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Areas

CloudEvents type: `GeneralTransitFeedStatic.Areas`

#### What it tells you

Defines areas.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Areas` payloads are JSON object. Required fields: `areaId`, `areaName`.

- **`areaId`** (string, required): Identifies an area.
- **`areaName`** (string, required): Name of the area.
- **`areaDesc`** (string, optional): Description of the area.
- **`areaUrl`** (string, optional): URL of a web page about the area.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "areaId": "string",
  "areaName": "string",
  "areaDesc": "string",
  "areaUrl": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Attributions

CloudEvents type: `GeneralTransitFeedStatic.Attributions`

#### What it tells you

Provides information about the attributions.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Attributions` payloads are JSON object. Required fields: `organizationName`.

- **`attributionId`** (string, optional): Identifies an attribution for the dataset.
- **`agencyId`** (string, optional): Identifies the agency associated with the attribution.
- **`routeId`** (string, optional): Identifies the route associated with the attribution.
- **`tripId`** (string, optional): Identifies the trip associated with the attribution.
- **`organizationName`** (string, required): Name of the organization associated with the attribution.
- **`isProducer`** (int32, optional): Indicates if the organization is a producer.
- **`isOperator`** (int32, optional): Indicates if the organization is an operator.
- **`isAuthority`** (int32, optional): Indicates if the organization is an authority.
- **`attributionUrl`** (string, optional): URL of a web page about the attribution.
- **`attributionEmail`** (string, optional): Email address associated with the attribution.
- **`attributionPhone`** (string, optional): Phone number associated with the attribution.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "attributionId": "string",
  "agencyId": "string",
  "routeId": "string",
  "tripId": "string",
  "organizationName": "string",
  "isProducer": 0,
  "isOperator": 0,
  "isAuthority": 0,
  "attributionUrl": "string",
  "attributionEmail": "string",
  "attributionPhone": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Booking Rules

CloudEvents type: `GeneralTransitFeed.BookingRules`

#### What it tells you

Defines booking rules.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Booking Rules` payloads are JSON object. Required fields: `bookingRuleId`, `bookingRuleName`.

- **`bookingRuleId`** (string, required): Identifies a booking rule.
- **`bookingRuleName`** (string, required): Name of the booking rule.
- **`bookingRuleDesc`** (string, optional): Description of the booking rule.
- **`bookingRuleUrl`** (string, optional): URL of a web page about the booking rule.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "bookingRuleId": "string",
  "bookingRuleName": "string",
  "bookingRuleDesc": "string",
  "bookingRuleUrl": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Fare Attributes

CloudEvents type: `GeneralTransitFeedStatic.FareAttributes`

#### What it tells you

Defines fare attributes.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Fare Attributes` payloads are JSON object. Required fields: `fareId`, `price`, `currencyType`, `paymentMethod`.

- **`fareId`** (string, required): Identifies a fare class.
- **`price`** (double, required): Fare price, in the unit specified by currency_type.
- **`currencyType`** (string, required): Currency type used to pay the fare.
- **`paymentMethod`** (int32, required): When 0, fare must be paid on board. When 1, fare must be paid before boarding.
- **`transfers`** (int32, optional): Specifies the number of transfers permitted on this fare.
- **`agencyId`** (string, optional): Identifies the agency for the specified fare.
- **`transferDuration`** (int64, optional): Length of time in seconds before a transfer expires.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fareId": "string",
  "price": 0,
  "currencyType": "string",
  "paymentMethod": 0,
  "transfers": 0,
  "agencyId": "string",
  "transferDuration": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Fare Leg Rules

CloudEvents type: `GeneralTransitFeedStatic.FareLegRules`

#### What it tells you

Defines fare leg rules.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Fare Leg Rules` payloads are JSON object. Required fields: `fareLegRuleId`, `fareProductId`.

- **`fareLegRuleId`** (string, required): Identifies a fare leg rule.
- **`fareProductId`** (string, required): Identifies a fare product.
- **`legGroupId`** (string, optional): Identifies a group of legs.
- **`networkId`** (string, optional): Identifies a network.
- **`fromAreaId`** (string, optional): Identifies the origin area.
- **`toAreaId`** (string, optional): Identifies the destination area.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fareLegRuleId": "string",
  "fareProductId": "string",
  "legGroupId": "string",
  "networkId": "string",
  "fromAreaId": "string",
  "toAreaId": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Fare Media

CloudEvents type: `GeneralTransitFeedStatic.FareMedia`

#### What it tells you

Defines fare media.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Fare Media` payloads are JSON object. Required fields: `fareMediaId`, `fareMediaName`.

- **`fareMediaId`** (string, required): Identifies a fare media.
- **`fareMediaName`** (string, required): Name of the fare media.
- **`fareMediaDesc`** (string, optional): Description of the fare media.
- **`fareMediaUrl`** (string, optional): URL of a web page about the fare media.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fareMediaId": "string",
  "fareMediaName": "string",
  "fareMediaDesc": "string",
  "fareMediaUrl": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Fare Products

CloudEvents type: `GeneralTransitFeedStatic.FareProducts`

#### What it tells you

Defines fare products.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Fare Products` payloads are JSON object. Required fields: `fareProductId`, `fareProductName`.

- **`fareProductId`** (string, required): Identifies a fare product.
- **`fareProductName`** (string, required): Name of the fare product.
- **`fareProductDesc`** (string, optional): Description of the fare product.
- **`fareProductUrl`** (string, optional): URL of a web page about the fare product.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fareProductId": "string",
  "fareProductName": "string",
  "fareProductDesc": "string",
  "fareProductUrl": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Fare Rules

CloudEvents type: `GeneralTransitFeedStatic.FareRules`

#### What it tells you

Defines fare rules.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Fare Rules` payloads are JSON object. Required fields: `fareId`.

- **`fareId`** (string, required): Identifies a fare class.
- **`routeId`** (string, optional): Identifies a route associated with the fare.
- **`originId`** (string, optional): Identifies the fare zone of the origin.
- **`destinationId`** (string, optional): Identifies the fare zone of the destination.
- **`containsId`** (string, optional): Identifies the fare zone that a rider will enter or leave.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fareId": "string",
  "routeId": "string",
  "originId": "string",
  "destinationId": "string",
  "containsId": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Fare Transfer Rules

CloudEvents type: `GeneralTransitFeedStatic.FareTransferRules`

#### What it tells you

Defines fare transfer rules.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Fare Transfer Rules` payloads are JSON object. Required fields: `fareTransferRuleId`, `fareProductId`.

- **`fareTransferRuleId`** (string, required): Identifies a fare transfer rule.
- **`fareProductId`** (string, required): Identifies a fare product.
- **`transferCount`** (int32, optional): Number of transfers permitted.
- **`fromLegGroupId`** (string, optional): Identifies the leg group from which the transfer starts.
- **`toLegGroupId`** (string, optional): Identifies the leg group to which the transfer applies.
- **`duration`** (int64, optional): Length of time in seconds before a transfer expires.
- **`durationType`** (string, optional): Type of duration for the transfer.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fareTransferRuleId": "string",
  "fareProductId": "string",
  "transferCount": 0,
  "fromLegGroupId": "string",
  "toLegGroupId": "string",
  "duration": 0,
  "durationType": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Feed Info

CloudEvents type: `GeneralTransitFeedStatic.FeedInfo`

#### What it tells you

Provides information about the GTFS feed itself.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Feed Info` payloads are JSON object. Required fields: `feedPublisherName`, `feedPublisherUrl`, `feedLang`.

- **`feedPublisherName`** (string, required): Full name of the organization that publishes the feed.
- **`feedPublisherUrl`** (string, required): URL of the feed publishing organization's website.
- **`feedLang`** (string, required): Default language for the text in this feed.
- **`defaultLang`** (string, optional): Specifies the language used when the data consumer doesn’t know the language of the user.
- **`feedStartDate`** (string, optional): The start date for the dataset.
- **`feedEndDate`** (string, optional): The end date for the dataset.
- **`feedVersion`** (string, optional): Version string that indicates the current version of their GTFS dataset.
- **`feedContactEmail`** (string, optional): Email address for communication with the data publisher.
- **`feedContactUrl`** (string, optional): URL for a web page that allows a feed consumer to contact the data publisher.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "feedPublisherName": "string",
  "feedPublisherUrl": "string",
  "feedLang": "string",
  "defaultLang": "string",
  "feedStartDate": "string",
  "feedEndDate": "string",
  "feedVersion": "string",
  "feedContactEmail": "string",
  "feedContactUrl": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Frequencies

CloudEvents type: `GeneralTransitFeedStatic.Frequencies`

#### What it tells you

Defines frequencies.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Frequencies` payloads are JSON object. Required fields: `tripId`, `startTime`, `endTime`, `headwaySecs`.

- **`tripId`** (string, required): Identifies a trip.
- **`startTime`** (string, required): Time at which service begins with the specified frequency.
- **`endTime`** (string, required): Time at which service ends with the specified frequency.
- **`headwaySecs`** (int32, required): Time between departures from the same stop (headway) for this trip, in seconds.
- **`exactTimes`** (int32, optional): When 1, frequency-based trips should be exactly scheduled. When 0 (or empty), frequency-based trips are not exactly scheduled.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "tripId": "string",
  "startTime": "string",
  "endTime": "string",
  "headwaySecs": 0,
  "exactTimes": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Levels

CloudEvents type: `GeneralTransitFeedStatic.Levels`

#### What it tells you

Defines levels.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Levels` payloads are JSON object. Required fields: `levelId`, `levelIndex`.

- **`levelId`** (string, required): Identifies a level.
- **`levelIndex`** (double, required): Numeric index of the level that indicates relative position of the level in relation to other levels.
- **`levelName`** (string, optional): Name of the level.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "levelId": "string",
  "levelIndex": 0,
  "levelName": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Location Geo Json

CloudEvents type: `GeneralTransitFeedStatic.LocationGeoJson`

#### What it tells you

Defines location GeoJSON data.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Location Geo Json` payloads are JSON object. Required fields: `locationGeoJsonId`, `locationGeoJsonType`, `locationGeoJsonData`.

- **`locationGeoJsonId`** (string, required): Identifies a location GeoJSON.
- **`locationGeoJsonType`** (string, required): Type of the GeoJSON.
- **`locationGeoJsonData`** (string, required): GeoJSON data.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "locationGeoJsonId": "string",
  "locationGeoJsonType": "string",
  "locationGeoJsonData": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Location Groups

CloudEvents type: `GeneralTransitFeedStatic.LocationGroups`

#### What it tells you

Defines location groups.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Location Groups` payloads are JSON object. Required fields: `locationGroupId`, `locationGroupName`.

- **`locationGroupId`** (string, required): Identifies a location group.
- **`locationGroupName`** (string, required): Name of the location group.
- **`locationGroupDesc`** (string, optional): Description of the location group.
- **`locationGroupUrl`** (string, optional): URL of a web page about the location group.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "locationGroupId": "string",
  "locationGroupName": "string",
  "locationGroupDesc": "string",
  "locationGroupUrl": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Location Group Stores

CloudEvents type: `GeneralTransitFeedStatic.LocationGroupStores`

#### What it tells you

Defines location group stores.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Location Group Stores` payloads are JSON object. Required fields: `locationGroupStoreId`, `locationGroupId`, `storeId`.

- **`locationGroupStoreId`** (string, required): Identifies a location group store.
- **`locationGroupId`** (string, required): Identifies a location group.
- **`storeId`** (string, required): Identifies a store.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "locationGroupStoreId": "string",
  "locationGroupId": "string",
  "storeId": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Networks

CloudEvents type: `GeneralTransitFeedStatic.Networks`

#### What it tells you

Defines networks.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Networks` payloads are JSON object. Required fields: `networkId`, `networkName`.

- **`networkId`** (string, required): Identifies a network.
- **`networkName`** (string, required): Name of the network.
- **`networkDesc`** (string, optional): Description of the network.
- **`networkUrl`** (string, optional): URL of a web page about the network.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "networkId": "string",
  "networkName": "string",
  "networkDesc": "string",
  "networkUrl": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Pathways

CloudEvents type: `GeneralTransitFeedStatic.Pathways`

#### What it tells you

Defines pathways.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Pathways` payloads are JSON object. Required fields: `pathwayId`, `fromStopId`, `toStopId`, `pathwayMode`, `isBidirectional`.

- **`pathwayId`** (string, required): Identifies a pathway.
- **`fromStopId`** (string, required): Identifies a stop or station where the pathway begins.
- **`toStopId`** (string, required): Identifies a stop or station where the pathway ends.
- **`pathwayMode`** (int32, required): Type of pathway between the specified (from_stop_id, to_stop_id) pair.
- **`isBidirectional`** (int32, required): When 1, the pathway can be used in both directions. When 0, the pathway can only be used from (from_stop_id) to (to_stop_id).
- **`length`** (double, optional): Length of the pathway, in meters.
- **`traversalTime`** (int32, optional): Average time, in seconds, needed to walk through the pathway.
- **`stairCount`** (int32, optional): Number of stairs of the pathway.
- **`maxSlope`** (double, optional): Maximum slope of the pathway, in percent.
- **`minWidth`** (double, optional): Minimum width of the pathway, in meters.
- **`signpostedAs`** (string, optional): Signposting information for the pathway.
- **`reversedSignpostedAs`** (string, optional): Reversed signposting information for the pathway.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "pathwayId": "string",
  "fromStopId": "string",
  "toStopId": "string",
  "pathwayMode": 0,
  "isBidirectional": 0,
  "length": 0,
  "traversalTime": 0,
  "stairCount": 0,
  "maxSlope": 0,
  "minWidth": 0,
  "signpostedAs": "string",
  "reversedSignpostedAs": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Route Networks

CloudEvents type: `GeneralTransitFeedStatic.RouteNetworks`

#### What it tells you

Defines route networks.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Route Networks` payloads are JSON object. Required fields: `routeNetworkId`, `routeId`, `networkId`.

- **`routeNetworkId`** (string, required): Identifies a route network.
- **`routeId`** (string, required): Identifies a route.
- **`networkId`** (string, required): Identifies a network.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "routeNetworkId": "string",
  "routeId": "string",
  "networkId": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Routes

CloudEvents type: `GeneralTransitFeedStatic.Routes`

#### What it tells you

Identifies a route.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Routes` payloads are JSON object. Required fields: `routeId`, `routeType`, `continuousPickup`, `continuousDropOff`.

- **`routeId`** (string, required): Identifies a route.
- **`agencyId`** (string, optional): Agency for the specified route.
- **`routeShortName`** (string, optional): Short name of a route.
- **`routeLongName`** (string, optional): Full name of a route.
- **`routeDesc`** (string, optional): Description of a route that provides useful, quality information.
- **`routeType`** (enum, required): Indicates the type of transportation used on a route.
- **`routeUrl`** (string, optional): URL of a web page about the particular route.
- **`routeColor`** (string, optional): Route color designation that matches public facing material.
- **`routeTextColor`** (string, optional): Legible color to use for text drawn against a background of route_color.
- **`routeSortOrder`** (int32, optional): Orders the routes in a way which is ideal for presentation to customers.
- **`continuousPickup`** (enum, required): Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path.
- **`continuousDropOff`** (enum, required): Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path.
- **`networkId`** (string, optional): Identifies a group of routes.
##### `routeType` values

- `TRAM`
- `SUBWAY`
- `RAIL`
- `BUS`
- `FERRY`
- `CABLE_TRAM`
- `AERIAL_LIFT`
- `FUNICULAR`
- `RESERVED_1`
- `RESERVED_2`
- `RESERVED_3`
- `TROLLEYBUS`
- `MONORAIL`
- `OTHER`
##### `continuousPickup` values

- `CONTINUOUS_STOPPING`
- `NO_CONTINUOUS_STOPPING`
- `PHONE_AGENCY`
- `COORDINATE_WITH_DRIVER`
##### `continuousDropOff` values

- `CONTINUOUS_STOPPING`
- `NO_CONTINUOUS_STOPPING`
- `PHONE_AGENCY`
- `COORDINATE_WITH_DRIVER`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "routeId": "string",
  "agencyId": "string",
  "routeShortName": "string",
  "routeLongName": "string",
  "routeDesc": "string",
  "routeType": "TRAM",
  "routeUrl": "string",
  "routeColor": "string",
  "routeTextColor": "string",
  "routeSortOrder": 0,
  "continuousPickup": "CONTINUOUS_STOPPING",
  "continuousDropOff": "CONTINUOUS_STOPPING",
  "networkId": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Shapes

CloudEvents type: `GeneralTransitFeedStatic.Shapes`

#### What it tells you

Defines shapes.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Shapes` payloads are JSON object. Required fields: `shapeId`, `shapePtLat`, `shapePtLon`, `shapePtSequence`.

- **`shapeId`** (string, required): Identifies a shape.
- **`shapePtLat`** (double, required): Latitude of a shape point.
- **`shapePtLon`** (double, required): Longitude of a shape point.
- **`shapePtSequence`** (int32, required): Sequence in which the shape points connect to form the shape.
- **`shapeDistTraveled`** (double, optional): Actual distance traveled along the shape from the first shape point to the specified shape point.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "shapeId": "string",
  "shapePtLat": 0,
  "shapePtLon": 0,
  "shapePtSequence": 0,
  "shapeDistTraveled": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Stop Areas

CloudEvents type: `GeneralTransitFeedStatic.StopAreas`

#### What it tells you

Defines stop areas.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Stop Areas` payloads are JSON object. Required fields: `stopAreaId`, `stopId`, `areaId`.

- **`stopAreaId`** (string, required): Identifies a stop area.
- **`stopId`** (string, required): Identifies a stop.
- **`areaId`** (string, required): Identifies an area.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "stopAreaId": "string",
  "stopId": "string",
  "areaId": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Stops

CloudEvents type: `GeneralTransitFeedStatic.Stops`

#### What it tells you

Identifies locations such as stop/platform, station, entrance/exit, generic node or boarding area.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Stops` payloads are JSON object. Required fields: `stopId`, `locationType`, `wheelchairBoarding`.

- **`stopId`** (string, required): Identifies a location: stop/platform, station, entrance/exit, generic node or boarding area.
- **`stopCode`** (string, optional): Short text or a number that identifies the location for riders.
- **`stopName`** (string, optional): Name of the location.
- **`ttsStopName`** (string, optional): Readable version of the stop_name.
- **`stopDesc`** (string, optional): Description of the location that provides useful, quality information.
- **`stopLat`** (double, optional): Latitude of the location.
- **`stopLon`** (double, optional): Longitude of the location.
- **`zoneId`** (string, optional): Identifies the fare zone for a stop.
- **`stopUrl`** (string, optional): URL of a web page about the location.
- **`locationType`** (enum, required): Location type.
- **`parentStation`** (string, optional): Defines hierarchy between the different locations.
- **`stopTimezone`** (string, optional): Timezone of the location.
- **`wheelchairBoarding`** (enum, required): Indicates whether wheelchair boardings are possible from the location.
- **`levelId`** (string, optional): Level of the location.
- **`platformCode`** (string, optional): Platform identifier for a platform stop.
##### `locationType` values

- `STOP`
- `STATION`
- `ENTRANCE_EXIT`
- `GENERIC_NODE`
- `BOARDING_AREA`
##### `wheelchairBoarding` values

- `NO_INFO`
- `SOME_VEHICLES`
- `NOT_POSSIBLE`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "stopId": "string",
  "stopCode": "string",
  "stopName": "string",
  "ttsStopName": "string",
  "stopDesc": "string",
  "stopLat": 0,
  "stopLon": 0,
  "zoneId": "string",
  "stopUrl": "string",
  "locationType": "STOP",
  "parentStation": "string",
  "stopTimezone": "string",
  "wheelchairBoarding": "NO_INFO",
  "levelId": "string",
  "platformCode": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Stop Times

CloudEvents type: `GeneralTransitFeedStatic.StopTimes`

#### What it tells you

Represents times that a vehicle arrives at and departs from individual stops for each trip.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Stop Times` payloads are JSON object. Required fields: `tripId`, `stopSequence`, `pickupType`, `dropOffType`, `timepoint`.

- **`tripId`** (string, required): Identifies a trip.
- **`arrivalTime`** (string, optional): Arrival time at the stop for a specific trip.
- **`departureTime`** (string, optional): Departure time from the stop for a specific trip.
- **`stopId`** (string, optional): Identifies the serviced stop.
- **`stopSequence`** (int32, required): Order of stops for a particular trip.
- **`stopHeadsign`** (string, optional): Text that appears on signage identifying the trip's destination to riders.
- **`pickupType`** (enum, required): Indicates pickup method.
- **`dropOffType`** (enum, required): Indicates drop off method.
- **`continuousPickup`** (enum, optional): Indicates continuous stopping pickup.
- **`continuousDropOff`** (enum, optional): Indicates continuous stopping drop off.
- **`shapeDistTraveled`** (double, optional): Actual distance traveled along the shape from the first stop to the stop specified in this record.
- **`timepoint`** (enum, required): Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times.
##### `pickupType` values

- `REGULAR`
- `NO_PICKUP`
- `PHONE_AGENCY`
- `COORDINATE_WITH_DRIVER`
##### `dropOffType` values

- `REGULAR`
- `NO_DROP_OFF`
- `PHONE_AGENCY`
- `COORDINATE_WITH_DRIVER`
##### `continuousPickup` values

- `CONTINUOUS_STOPPING`
- `NO_CONTINUOUS_STOPPING`
- `PHONE_AGENCY`
- `COORDINATE_WITH_DRIVER`
##### `continuousDropOff` values

- `CONTINUOUS_STOPPING`
- `NO_CONTINUOUS_STOPPING`
- `PHONE_AGENCY`
- `COORDINATE_WITH_DRIVER`
##### `timepoint` values

- `APPROXIMATE`
- `EXACT`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "tripId": "string",
  "arrivalTime": "string",
  "departureTime": "string",
  "stopId": "string",
  "stopSequence": 0,
  "stopHeadsign": "string",
  "pickupType": "REGULAR",
  "dropOffType": "REGULAR",
  "continuousPickup": "CONTINUOUS_STOPPING",
  "continuousDropOff": "CONTINUOUS_STOPPING",
  "shapeDistTraveled": 0,
  "timepoint": "APPROXIMATE"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Timeframes

CloudEvents type: `GeneralTransitFeedStatic.Timeframes`

#### What it tells you

Used to describe fares that can vary based on the time of day, the day of the week, or a particular day in the year.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Timeframes` payloads are JSON object. Required fields: `timeframeGroupId`, `serviceDates`.

- **`timeframeGroupId`** (string, required): Identifies a timeframe or set of timeframes.
- **`startTime`** (string, optional): Defines the beginning of a timeframe.
- **`endTime`** (string, optional): Defines the end of a timeframe.
- **`serviceDates`** (choice, required): Identifies a set of dates when service is available for one or more routes.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "timeframeGroupId": "string",
  "startTime": "string",
  "endTime": "string",
  "serviceDates": null
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Transfers

CloudEvents type: `GeneralTransitFeedStatic.Transfers`

#### What it tells you

Defines transfers.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Transfers` payloads are JSON object. Required fields: `fromStopId`, `toStopId`, `transferType`.

- **`fromStopId`** (string, required): Identifies a stop or station where a connection between routes begins.
- **`toStopId`** (string, required): Identifies a stop or station where a connection between routes ends.
- **`transferType`** (int32, required): Type of connection for the specified (from_stop_id, to_stop_id) pair.
- **`minTransferTime`** (int32, optional): Amount of time, in seconds, needed to transfer from the specified (from_stop_id) to the specified (to_stop_id).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fromStopId": "string",
  "toStopId": "string",
  "transferType": 0,
  "minTransferTime": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Translations

CloudEvents type: `GeneralTransitFeedStatic.Translations`

#### What it tells you

Defines translations.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Translations` payloads are JSON object. Required fields: `tableName`, `fieldName`, `language`, `translation`.

- **`tableName`** (string, required): Name of the table containing the field to be translated.
- **`fieldName`** (string, required): Name of the field to be translated.
- **`language`** (string, required): Language of the translation.
- **`translation`** (string, required): Translated value.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "tableName": "string",
  "fieldName": "string",
  "language": "string",
  "translation": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Trips

CloudEvents type: `GeneralTransitFeedStatic.Trips`

#### What it tells you

Identifies a trip.

#### Identity

Each event identifies the real-world resource with `{agencyid}`. `{agencyid}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gtfs`, key `{agencyid}` |

#### Payload

`Trips` payloads are JSON object. Required fields: `routeId`, `serviceDates`, `serviceExceptions`, `tripId`, `directionId`, `wheelchairAccessible`, `bikesAllowed`.

- **`routeId`** (string, required): Identifies a route.
- **`serviceDates`** (object, required): No description provided. See [Calendar](#payload-generaltransitfeedstatic-trips-calendar).
- **`serviceExceptions`** (array of object, required): No description provided.
- **`tripId`** (string, required): Identifies a trip.
- **`tripHeadsign`** (string, optional): Text that appears on signage identifying the trip's destination to riders.
- **`tripShortName`** (string, optional): Public facing text used to identify the trip to riders.
- **`directionId`** (enum, required): Indicates the direction of travel for a trip.
- **`blockId`** (string, optional): Identifies the block to which the trip belongs.
- **`shapeId`** (string, optional): Identifies a geospatial shape describing the vehicle travel path for a trip.
- **`wheelchairAccessible`** (enum, required): Indicates wheelchair accessibility.
- **`bikesAllowed`** (enum, required): Indicates whether bikes are allowed.
##### `directionId` values

- `OUTBOUND`
- `INBOUND`
##### `wheelchairAccessible` values

- `NO_INFO`
- `WHEELCHAIR_ACCESSIBLE`
- `NOT_WHEELCHAIR_ACCESSIBLE`
##### `bikesAllowed` values

- `NO_INFO`
- `BICYCLE_ALLOWED`
- `BICYCLE_NOT_ALLOWED`
##### `monday` values

- `NO_SERVICE`
- `SERVICE_AVAILABLE`
##### `tuesday` values

- `NO_SERVICE`
- `SERVICE_AVAILABLE`
##### `wednesday` values

- `NO_SERVICE`
- `SERVICE_AVAILABLE`
##### `thursday` values

- `NO_SERVICE`
- `SERVICE_AVAILABLE`
##### `friday` values

- `NO_SERVICE`
- `SERVICE_AVAILABLE`
##### `saturday` values

- `NO_SERVICE`
- `SERVICE_AVAILABLE`
##### `sunday` values

- `NO_SERVICE`
- `SERVICE_AVAILABLE`
##### Calendar
<a id="payload-generaltransitfeedstatic-trips-calendar"></a>

Nested record.

- **`serviceId`** (string, required): Identifies a set of dates when service is available for one or more routes.
- **`monday`** (enum, required): Indicates whether the service operates on all Mondays in the date range specified.
- **`tuesday`** (enum, required): Indicates whether the service operates on all Tuesdays in the date range specified.
- **`wednesday`** (enum, required): Indicates whether the service operates on all Wednesdays in the date range specified.
- **`thursday`** (enum, required): Indicates whether the service operates on all Thursdays in the date range specified.
- **`friday`** (enum, required): Indicates whether the service operates on all Fridays in the date range specified.
- **`saturday`** (enum, required): Indicates whether the service operates on all Saturdays in the date range specified.
- **`sunday`** (enum, required): Indicates whether the service operates on all Sundays in the date range specified.
- **`startDate`** (string, required): Start service day for the service interval.
- **`endDate`** (string, required): End service day for the service interval.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "routeId": "string",
  "serviceDates": {
    "serviceId": "string",
    "monday": "NO_SERVICE",
    "tuesday": "NO_SERVICE",
    "wednesday": "NO_SERVICE",
    "thursday": "NO_SERVICE",
    "friday": "NO_SERVICE",
    "saturday": "NO_SERVICE",
    "sunday": "NO_SERVICE",
    "startDate": "string",
    "endDate": "string"
  },
  "serviceExceptions": [
    {
      "serviceId": "string",
      "date": "string",
      "exceptionType": "SERVICE_ADDED"
    }
  ],
  "tripId": "string",
  "tripHeadsign": "string",
  "tripShortName": "string",
  "directionId": "OUTBOUND",
  "blockId": "string",
  "shapeId": "string",
  "wheelchairAccessible": "NO_INFO",
  "bikesAllowed": "NO_INFO"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

All payloads documented here are JSON. MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/gtfs.xreg.json`](xreg/gtfs.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
