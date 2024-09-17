# GTFS API Bridge Events

This document describes the events that are emitted by the GTFS API Bridge.

- [GTFS API Bridge Events](#gtfs-api-bridge-events)
  - [Message Group: GeneralTransitFeedRealTime](#message-group-generaltransitfeedrealtime)
    - [Message: GeneralTransitFeedRealTime.Vehicle.VehiclePosition](#message-generaltransitfeedrealtimevehiclevehicleposition)
      - [CloudEvents Attributes:](#cloudevents-attributes)
      - [Schema:](#schema)
        - [Record: VehiclePosition](#record-vehicleposition)
        - [Record: TripDescriptor](#record-tripdescriptor)
        - [Record: VehicleDescriptor](#record-vehicledescriptor)
        - [Record: Position](#record-position)
        - [Enum: VehicleStopStatus](#enum-vehiclestopstatus)
        - [Enum: CongestionLevel](#enum-congestionlevel)
        - [Enum: OccupancyStatus](#enum-occupancystatus)
        - [Enum: ScheduleRelationship](#enum-schedulerelationship)
    - [Message: GeneralTransitFeedRealTime.Trip.TripUpdate](#message-generaltransitfeedrealtimetriptripupdate)
      - [CloudEvents Attributes:](#cloudevents-attributes-1)
      - [Schema:](#schema-1)
        - [Record: TripUpdate](#record-tripupdate)
        - [Record: TripDescriptor](#record-tripdescriptor-1)
        - [Record: VehicleDescriptor](#record-vehicledescriptor-1)
        - [Enum: ScheduleRelationship](#enum-schedulerelationship-1)
    - [Message: GeneralTransitFeedRealTime.Alert.Alert](#message-generaltransitfeedrealtimealertalert)
      - [CloudEvents Attributes:](#cloudevents-attributes-2)
      - [Schema:](#schema-2)
        - [Record: Alert](#record-alert)
        - [Record: TranslatedString](#record-translatedstring)
        - [Enum: Cause](#enum-cause)
        - [Enum: Effect](#enum-effect)
  - [Message Group: GeneralTransitFeedStatic](#message-group-generaltransitfeedstatic)
    - [Message: GeneralTransitFeedStatic.Agency](#message-generaltransitfeedstaticagency)
      - [CloudEvents Attributes:](#cloudevents-attributes-3)
      - [Schema:](#schema-3)
        - [Record: Agency](#record-agency)
    - [Message: GeneralTransitFeedStatic.Areas](#message-generaltransitfeedstaticareas)
      - [CloudEvents Attributes:](#cloudevents-attributes-4)
      - [Schema:](#schema-4)
        - [Record: Areas](#record-areas)
    - [Message: GeneralTransitFeedStatic.Attributions](#message-generaltransitfeedstaticattributions)
      - [CloudEvents Attributes:](#cloudevents-attributes-5)
      - [Schema:](#schema-5)
        - [Record: Attributions](#record-attributions)
    - [Message: GeneralTransitFeed.BookingRules](#message-generaltransitfeedbookingrules)
      - [CloudEvents Attributes:](#cloudevents-attributes-6)
      - [Schema:](#schema-6)
        - [Record: BookingRules](#record-bookingrules)
    - [Message: GeneralTransitFeedStatic.FareAttributes](#message-generaltransitfeedstaticfareattributes)
      - [CloudEvents Attributes:](#cloudevents-attributes-7)
      - [Schema:](#schema-7)
        - [Record: FareAttributes](#record-fareattributes)
    - [Message: GeneralTransitFeedStatic.FareLegRules](#message-generaltransitfeedstaticfarelegrules)
      - [CloudEvents Attributes:](#cloudevents-attributes-8)
      - [Schema:](#schema-8)
        - [Record: FareLegRules](#record-farelegrules)
    - [Message: GeneralTransitFeedStatic.FareMedia](#message-generaltransitfeedstaticfaremedia)
      - [CloudEvents Attributes:](#cloudevents-attributes-9)
      - [Schema:](#schema-9)
        - [Record: FareMedia](#record-faremedia)
    - [Message: GeneralTransitFeedStatic.FareProducts](#message-generaltransitfeedstaticfareproducts)
      - [CloudEvents Attributes:](#cloudevents-attributes-10)
      - [Schema:](#schema-10)
        - [Record: FareProducts](#record-fareproducts)
    - [Message: GeneralTransitFeedStatic.FareRules](#message-generaltransitfeedstaticfarerules)
      - [CloudEvents Attributes:](#cloudevents-attributes-11)
      - [Schema:](#schema-11)
        - [Record: FareRules](#record-farerules)
    - [Message: GeneralTransitFeedStatic.FareTransferRules](#message-generaltransitfeedstaticfaretransferrules)
      - [CloudEvents Attributes:](#cloudevents-attributes-12)
      - [Schema:](#schema-12)
        - [Record: FareTransferRules](#record-faretransferrules)
    - [Message: GeneralTransitFeedStatic.FeedInfo](#message-generaltransitfeedstaticfeedinfo)
      - [CloudEvents Attributes:](#cloudevents-attributes-13)
      - [Schema:](#schema-13)
        - [Record: FeedInfo](#record-feedinfo)
    - [Message: GeneralTransitFeedStatic.Frequencies](#message-generaltransitfeedstaticfrequencies)
      - [CloudEvents Attributes:](#cloudevents-attributes-14)
      - [Schema:](#schema-14)
        - [Record: Frequencies](#record-frequencies)
    - [Message: GeneralTransitFeedStatic.Levels](#message-generaltransitfeedstaticlevels)
      - [CloudEvents Attributes:](#cloudevents-attributes-15)
      - [Schema:](#schema-15)
        - [Record: Levels](#record-levels)
    - [Message: GeneralTransitFeedStatic.LocationGeoJson](#message-generaltransitfeedstaticlocationgeojson)
      - [CloudEvents Attributes:](#cloudevents-attributes-16)
      - [Schema:](#schema-16)
        - [Record: LocationGeoJson](#record-locationgeojson)
    - [Message: GeneralTransitFeedStatic.LocationGroups](#message-generaltransitfeedstaticlocationgroups)
      - [CloudEvents Attributes:](#cloudevents-attributes-17)
      - [Schema:](#schema-17)
        - [Record: LocationGroups](#record-locationgroups)
    - [Message: GeneralTransitFeedStatic.LocationGroupStores](#message-generaltransitfeedstaticlocationgroupstores)
      - [CloudEvents Attributes:](#cloudevents-attributes-18)
      - [Schema:](#schema-18)
        - [Record: LocationGroupStores](#record-locationgroupstores)
    - [Message: GeneralTransitFeedStatic.Networks](#message-generaltransitfeedstaticnetworks)
      - [CloudEvents Attributes:](#cloudevents-attributes-19)
      - [Schema:](#schema-19)
        - [Record: Networks](#record-networks)
    - [Message: GeneralTransitFeedStatic.Pathways](#message-generaltransitfeedstaticpathways)
      - [CloudEvents Attributes:](#cloudevents-attributes-20)
      - [Schema:](#schema-20)
        - [Record: Pathways](#record-pathways)
    - [Message: GeneralTransitFeedStatic.RouteNetworks](#message-generaltransitfeedstaticroutenetworks)
      - [CloudEvents Attributes:](#cloudevents-attributes-21)
      - [Schema:](#schema-21)
        - [Record: RouteNetworks](#record-routenetworks)
    - [Message: GeneralTransitFeedStatic.Routes](#message-generaltransitfeedstaticroutes)
      - [CloudEvents Attributes:](#cloudevents-attributes-22)
      - [Schema:](#schema-22)
        - [Record: Routes](#record-routes)
        - [Enum: RouteType](#enum-routetype)
        - [Enum: ContinuousPickup](#enum-continuouspickup)
        - [Enum: ContinuousDropOff](#enum-continuousdropoff)
    - [Message: GeneralTransitFeedStatic.Shapes](#message-generaltransitfeedstaticshapes)
      - [CloudEvents Attributes:](#cloudevents-attributes-23)
      - [Schema:](#schema-23)
        - [Record: Shapes](#record-shapes)
    - [Message: GeneralTransitFeedStatic.StopAreas](#message-generaltransitfeedstaticstopareas)
      - [CloudEvents Attributes:](#cloudevents-attributes-24)
      - [Schema:](#schema-24)
        - [Record: StopAreas](#record-stopareas)
    - [Message: GeneralTransitFeedStatic.Stops](#message-generaltransitfeedstaticstops)
      - [CloudEvents Attributes:](#cloudevents-attributes-25)
      - [Schema:](#schema-25)
        - [Record: Stops](#record-stops)
        - [Enum: LocationType](#enum-locationtype)
        - [Enum: WheelchairBoarding](#enum-wheelchairboarding)
    - [Message: GeneralTransitFeedStatic.StopTimes](#message-generaltransitfeedstaticstoptimes)
      - [CloudEvents Attributes:](#cloudevents-attributes-26)
      - [Schema:](#schema-26)
        - [Record: StopTimes](#record-stoptimes)
        - [Enum: PickupType](#enum-pickuptype)
        - [Enum: DropOffType](#enum-dropofftype)
        - [Enum: ContinuousPickup](#enum-continuouspickup-1)
        - [Enum: ContinuousDropOff](#enum-continuousdropoff-1)
        - [Enum: Timepoint](#enum-timepoint)
    - [Message: GeneralTransitFeedStatic.Timeframes](#message-generaltransitfeedstatictimeframes)
      - [CloudEvents Attributes:](#cloudevents-attributes-27)
      - [Schema:](#schema-27)
        - [Record: Timeframes](#record-timeframes)
        - [Record: Calendar](#record-calendar)
        - [Record: CalendarDates](#record-calendardates)
        - [Enum: ServiceAvailability](#enum-serviceavailability)
        - [Enum: ExceptionType](#enum-exceptiontype)
    - [Message: GeneralTransitFeedStatic.Transfers](#message-generaltransitfeedstatictransfers)
      - [CloudEvents Attributes:](#cloudevents-attributes-28)
      - [Schema:](#schema-28)
        - [Record: Transfers](#record-transfers)
    - [Message: GeneralTransitFeedStatic.Translations](#message-generaltransitfeedstatictranslations)
      - [CloudEvents Attributes:](#cloudevents-attributes-29)
      - [Schema:](#schema-29)
        - [Record: Translations](#record-translations)
    - [Message: GeneralTransitFeedStatic.Trips](#message-generaltransitfeedstatictrips)
      - [CloudEvents Attributes:](#cloudevents-attributes-30)
      - [Schema:](#schema-30)
        - [Record: Trips](#record-trips)
        - [Record: Calendar](#record-calendar-1)
        - [Enum: DirectionId](#enum-directionid)
        - [Enum: WheelchairAccessible](#enum-wheelchairaccessible)
        - [Enum: BikesAllowed](#enum-bikesallowed)
        - [Enum: ServiceAvailability](#enum-serviceavailability-1)

---

## Message Group: GeneralTransitFeedRealTime

### Message: GeneralTransitFeedRealTime.Vehicle.VehiclePosition

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedRealTime.Vehicle.VehiclePosition` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: VehiclePosition

*Realtime positioning information for a given vehicle.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `trip` | [Record TripDescriptor](#record-tripdescriptor) (optional) | The Trip that this vehicle is serving. Can be empty or partial if the vehicle can not be identified with a given trip instance. |
| `vehicle` | [Record VehicleDescriptor](#record-vehicledescriptor) (optional) | Additional information on the vehicle that is serving this trip. |
| `position` | [Record Position](#record-position) (optional) | Current position of this vehicle. The stop sequence index of the current stop. The meaning of |
| `current_stop_sequence` | *int* (optional) | current_stop_sequence (i.e., the stop that it refers to) is determined by current_status. If current_status is missing IN_TRANSIT_TO is assumed. Identifies the current stop. The value must be the same as in stops.txt in |
| `stop_id` | *string* (optional) | the corresponding GTFS feed. |
| `current_status` | [Enum VehicleStopStatus](#enum-vehiclestopstatus) (optional) | The exact status of the vehicle with respect to the current stop. Ignored if current_stop_sequence is missing. Moment at which the vehicle's position was measured. In POSIX time |
| `timestamp` | *long* (optional) | (i.e., number of seconds since January 1st 1970 00:00:00 UTC). |
| `congestion_level` | [Enum CongestionLevel](#enum-congestionlevel) (optional) |  |
| `occupancy_status` | [Enum OccupancyStatus](#enum-occupancystatus) (optional) |  |

---

##### Record: TripDescriptor

*A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary,   start_time) is set. If route_id is also set, then it should be same as one   that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be   set. Note that if the trip_id is not known, then stop sequence ids in   TripUpdate are not sufficient, and stop_ids must be provided as well. In   addition, absolute arrival/departure times must be provided.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `trip_id` | *string* (optional) | The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary. |
| `route_id` | *string* (optional) | The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the |
| `direction_id` | *int* (optional) | direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future. |
| `start_time` | *string* (optional) | The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance. |
| `start_date` | *string* (optional) | Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format. |
| `schedule_relationship` | [Enum ScheduleRelationship](#enum-schedulerelationship) (optional) |  |

---

##### Record: VehicleDescriptor

*Identification information for the vehicle performing the trip.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `id` | *string* (optional) | Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to |
| `label` | *string* (optional) | help identify the correct vehicle. |
| `license_plate` | *string* (optional) | The license plate of the vehicle. |

---

##### Record: Position

*A position.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `latitude` | *float* | Degrees North, in the WGS-84 coordinate system. |
| `longitude` | *float* | Degrees East, in the WGS-84 coordinate system. |
| `bearing` | *float* (optional) | Bearing, in degrees, clockwise from North, i.e., 0 is North and 90 is East. This can be the compass bearing, or the direction towards the next stop or intermediate location. This should not be direction deduced from the sequence of previous positions, which can be computed from previous data. |
| `odometer` | *double* (optional) | Odometer value, in meters. |
| `speed` | *float* (optional) | Momentary speed measured by the vehicle, in meters per second. |

---

##### Enum: VehicleStopStatus

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `INCOMING_AT` | 0 |  |
| `STOPPED_AT` | 1 |  |
| `IN_TRANSIT_TO` | 2 |  |

---

##### Enum: CongestionLevel

*Congestion level that is affecting this vehicle.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `UNKNOWN_CONGESTION_LEVEL` | 0 |  |
| `RUNNING_SMOOTHLY` | 1 |  |
| `STOP_AND_GO` | 2 |  |
| `CONGESTION` | 3 |  |
| `SEVERE_CONGESTION` | 4 |  |

---

##### Enum: OccupancyStatus

*The degree of passenger occupancy of the vehicle. This field is still experimental, and subject to change. It may be formally adopted in the future.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `EMPTY` | 0 |  |
| `MANY_SEATS_AVAILABLE` | 1 |  |
| `FEW_SEATS_AVAILABLE` | 2 |  |
| `STANDING_ROOM_ONLY` | 3 |  |
| `CRUSHED_STANDING_ROOM_ONLY` | 4 |  |
| `FULL` | 5 |  |
| `NOT_ACCEPTING_PASSENGERS` | 6 |  |

---

##### Enum: ScheduleRelationship

*The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `SCHEDULED` | 0 |  |
| `ADDED` | 1 |  |
| `UNSCHEDULED` | 2 |  |
| `CANCELED` | 3 |  |
### Message: GeneralTransitFeedRealTime.Trip.TripUpdate

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedRealTime.Trip.TripUpdate` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: TripUpdate

*Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule. - A trip that proceeds along a route but has no fixed schedule. - A trip that have been added or removed with regard to schedule. The updates can be for future, predicted arrival/departure events, or for past events that already occurred. Normally, updates should get more precise and more certain (see uncertainty below) as the events gets closer to current time. Even if that is not possible, the information for past events should be precise and certain. In particular, if an update points to time in the past but its update's uncertainty is not 0, the client should conclude that the update is a (wrong) prediction and that the trip has not completed yet. Note that the update can describe a trip that is already completed. To this end, it is enough to provide an update for the last stop of the trip. If the time of that is in the past, the client will conclude from that that the whole trip is in the past (it is possible, although inconsequential, to also provide updates for preceding stops). This option is most relevant for a trip that has completed ahead of schedule, but according to the schedule, the trip is still proceeding at the current time. Removing the updates for this trip could make the client assume that the trip is still proceeding. Note that the feed provider is allowed, but not required, to purge past updates - this is one case where this would be practically useful.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `trip` | [Record TripDescriptor](#record-tripdescriptor) | The Trip that this message applies to. There can be at most one TripUpdate entity for each actual trip instance. If there is none, that means there is no prediction information available. It does *not* mean that the trip is progressing according to schedule. |
| `vehicle` | [Record VehicleDescriptor](#record-vehicledescriptor) (optional) | Additional information on the vehicle that is serving this trip. |
| `stop_time_update` | *array* | Updates to StopTimes for the trip (both future, i.e., predictions, and in some cases, past ones, i.e., those that already happened). The updates must be sorted by stop_sequence, and apply for all the following stops of the trip up to the next specified one. Example 1: For a trip with 20 stops, a StopTimeUpdate with arrival delay and departure delay of 0 for stop_sequence of the current stop means that the trip is exactly on time. Example 2: For the same trip instance, 3 StopTimeUpdates are provided: - delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 - delay of unspecified duration for stop_sequence 10 This will be interpreted as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9 have delay of 1 min. - stop_sequences 10,... have unknown delay. Moment at which the vehicle's real-time progress was measured. In POSIX |
| `timestamp` | *long* (optional) | time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC). The current schedule deviation for the trip.  Delay should only be |
| `delay` | *int* (optional) | specified when the prediction is given relative to some existing schedule in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time. Delay information in StopTimeUpdates take precedent of trip-level delay information, such that trip-level delay is only propagated until the next stop along the trip with a StopTimeUpdate delay value specified. Feed providers are strongly encouraged to provide a TripUpdate.timestamp value indicating when the delay value was last updated, in order to evaluate the freshness of the data. NOTE: This field is still experimental, and subject to change. It may be formally adopted in the future. |

---

##### Record: TripDescriptor

*A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary,   start_time) is set. If route_id is also set, then it should be same as one   that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be   set. Note that if the trip_id is not known, then stop sequence ids in   TripUpdate are not sufficient, and stop_ids must be provided as well. In   addition, absolute arrival/departure times must be provided.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `trip_id` | *string* (optional) | The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary. |
| `route_id` | *string* (optional) | The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the |
| `direction_id` | *int* (optional) | direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future. |
| `start_time` | *string* (optional) | The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance. |
| `start_date` | *string* (optional) | Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format. |
| `schedule_relationship` | [Enum ScheduleRelationship](#enum-schedulerelationship) (optional) |  |

---

##### Record: VehicleDescriptor

*Identification information for the vehicle performing the trip.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `id` | *string* (optional) | Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to |
| `label` | *string* (optional) | help identify the correct vehicle. |
| `license_plate` | *string* (optional) | The license plate of the vehicle. |

---

##### Enum: ScheduleRelationship

*The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `SCHEDULED` | 0 |  |
| `ADDED` | 1 |  |
| `UNSCHEDULED` | 2 |  |
| `CANCELED` | 3 |  |
### Message: GeneralTransitFeedRealTime.Alert.Alert

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedRealTime.Alert.Alert` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Alert

*An alert, indicating some sort of incident in the public transit network.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `active_period` | *array* | Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them. |
| `informed_entity` | *array* | Entities whose users we should notify of this alert. |
| `cause` | [Enum Cause](#enum-cause) (optional) |  |
| `effect` | [Enum Effect](#enum-effect) (optional) |  |
| `url` | [Record TranslatedString](#record-translatedstring) (optional) | The URL which provides additional information about the alert. |
| `header_text` | *GeneralTransitFeedRealTime.Alert.TranslatedString* (optional) | Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the |
| `description_text` | *GeneralTransitFeedRealTime.Alert.TranslatedString* (optional) | description should add to the information of the header. |

---

##### Record: TranslatedString

*An internationalized message containing per-language versions of a snippet of text or a URL. One of the strings from a message will be picked up. The resolution proceeds as follows: 1. If the UI language matches the language code of a translation,    the first matching translation is picked. 2. If a default UI language (e.g., English) matches the language code of a    translation, the first matching translation is picked. 3. If some translation has an unspecified language code, that translation is    picked.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `translation` | *array* | At least one translation must be provided. |

---

##### Enum: Cause

*Cause of this alert.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `UNKNOWN_CAUSE` | 1 |  |
| `OTHER_CAUSE` | 2 |  |
| `TECHNICAL_PROBLEM` | 3 |  |
| `STRIKE` | 4 |  |
| `DEMONSTRATION` | 5 |  |
| `ACCIDENT` | 6 |  |
| `HOLIDAY` | 7 |  |
| `WEATHER` | 8 |  |
| `MAINTENANCE` | 9 |  |
| `CONSTRUCTION` | 10 |  |
| `POLICE_ACTIVITY` | 11 |  |
| `MEDICAL_EMERGENCY` | 12 |  |

---

##### Enum: Effect

*What is the effect of this problem on the affected entity.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `NO_SERVICE` | 1 |  |
| `REDUCED_SERVICE` | 2 |  |
| `SIGNIFICANT_DELAYS` | 3 |  |
| `DETOUR` | 4 |  |
| `ADDITIONAL_SERVICE` | 5 |  |
| `MODIFIED_SERVICE` | 6 |  |
| `OTHER_EFFECT` | 7 |  |
| `UNKNOWN_EFFECT` | 8 |  |
| `STOP_MOVED` | 9 |  |
## Message Group: GeneralTransitFeedStatic

### Message: GeneralTransitFeedStatic.Agency

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Agency` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Agency

*Information about the transit agencies.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `agencyId` | *string* | Identifies a transit brand which is often synonymous with a transit agency. |
| `agencyName` | *string* | Full name of the transit agency. |
| `agencyUrl` | *string* | URL of the transit agency. |
| `agencyTimezone` | *string* | Timezone where the transit agency is located. |
| `agencyLang` | *string* (optional) | Primary language used by this transit agency. |
| `agencyPhone` | *string* (optional) | A voice telephone number for the specified agency. |
| `agencyFareUrl` | *string* (optional) | URL of a web page that allows a rider to purchase tickets or other fare instruments for that agency online. |
| `agencyEmail` | *string* (optional) | Email address actively monitored by the agency�s customer service department. |
### Message: GeneralTransitFeedStatic.Areas

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Areas` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Areas

*Defines areas.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `areaId` | *string* | Identifies an area. |
| `areaName` | *string* | Name of the area. |
| `areaDesc` | *string* (optional) | Description of the area. |
| `areaUrl` | *string* (optional) | URL of a web page about the area. |
### Message: GeneralTransitFeedStatic.Attributions

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Attributions` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Attributions

*Provides information about the attributions.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `attributionId` | *string* (optional) | Identifies an attribution for the dataset. |
| `agencyId` | *string* (optional) | Identifies the agency associated with the attribution. |
| `routeId` | *string* (optional) | Identifies the route associated with the attribution. |
| `tripId` | *string* (optional) | Identifies the trip associated with the attribution. |
| `organizationName` | *string* | Name of the organization associated with the attribution. |
| `isProducer` | *int* (optional) | Indicates if the organization is a producer. |
| `isOperator` | *int* (optional) | Indicates if the organization is an operator. |
| `isAuthority` | *int* (optional) | Indicates if the organization is an authority. |
| `attributionUrl` | *string* (optional) | URL of a web page about the attribution. |
| `attributionEmail` | *string* (optional) | Email address associated with the attribution. |
| `attributionPhone` | *string* (optional) | Phone number associated with the attribution. |
### Message: GeneralTransitFeed.BookingRules

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeed.BookingRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: BookingRules

*Defines booking rules.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `bookingRuleId` | *string* | Identifies a booking rule. |
| `bookingRuleName` | *string* | Name of the booking rule. |
| `bookingRuleDesc` | *string* (optional) | Description of the booking rule. |
| `bookingRuleUrl` | *string* (optional) | URL of a web page about the booking rule. |
### Message: GeneralTransitFeedStatic.FareAttributes

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareAttributes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: FareAttributes

*Defines fare attributes.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `fareId` | *string* | Identifies a fare class. |
| `price` | *double* | Fare price, in the unit specified by currency_type. |
| `currencyType` | *string* | Currency type used to pay the fare. |
| `paymentMethod` | *int* | When 0, fare must be paid on board. When 1, fare must be paid before boarding. |
| `transfers` | *int* (optional) | Specifies the number of transfers permitted on this fare. |
| `agencyId` | *string* (optional) | Identifies the agency for the specified fare. |
| `transferDuration` | *long* (optional) | Length of time in seconds before a transfer expires. |
### Message: GeneralTransitFeedStatic.FareLegRules

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareLegRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: FareLegRules

*Defines fare leg rules.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `fareLegRuleId` | *string* | Identifies a fare leg rule. |
| `fareProductId` | *string* | Identifies a fare product. |
| `legGroupId` | *string* (optional) | Identifies a group of legs. |
| `networkId` | *string* (optional) | Identifies a network. |
| `fromAreaId` | *string* (optional) | Identifies the origin area. |
| `toAreaId` | *string* (optional) | Identifies the destination area. |
### Message: GeneralTransitFeedStatic.FareMedia

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareMedia` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: FareMedia

*Defines fare media.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `fareMediaId` | *string* | Identifies a fare media. |
| `fareMediaName` | *string* | Name of the fare media. |
| `fareMediaDesc` | *string* (optional) | Description of the fare media. |
| `fareMediaUrl` | *string* (optional) | URL of a web page about the fare media. |
### Message: GeneralTransitFeedStatic.FareProducts

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareProducts` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: FareProducts

*Defines fare products.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `fareProductId` | *string* | Identifies a fare product. |
| `fareProductName` | *string* | Name of the fare product. |
| `fareProductDesc` | *string* (optional) | Description of the fare product. |
| `fareProductUrl` | *string* (optional) | URL of a web page about the fare product. |
### Message: GeneralTransitFeedStatic.FareRules

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: FareRules

*Defines fare rules.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `fareId` | *string* | Identifies a fare class. |
| `routeId` | *string* (optional) | Identifies a route associated with the fare. |
| `originId` | *string* (optional) | Identifies the fare zone of the origin. |
| `destinationId` | *string* (optional) | Identifies the fare zone of the destination. |
| `containsId` | *string* (optional) | Identifies the fare zone that a rider will enter or leave. |
### Message: GeneralTransitFeedStatic.FareTransferRules

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareTransferRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: FareTransferRules

*Defines fare transfer rules.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `fareTransferRuleId` | *string* | Identifies a fare transfer rule. |
| `fareProductId` | *string* | Identifies a fare product. |
| `transferCount` | *int* (optional) | Number of transfers permitted. |
| `fromLegGroupId` | *string* (optional) | Identifies the leg group from which the transfer starts. |
| `toLegGroupId` | *string* (optional) | Identifies the leg group to which the transfer applies. |
| `duration` | *long* (optional) | Length of time in seconds before a transfer expires. |
| `durationType` | *string* (optional) | Type of duration for the transfer. |
### Message: GeneralTransitFeedStatic.FeedInfo

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FeedInfo` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: FeedInfo

*Provides information about the GTFS feed itself.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `feedPublisherName` | *string* | Full name of the organization that publishes the feed. |
| `feedPublisherUrl` | *string* | URL of the feed publishing organization's website. |
| `feedLang` | *string* | Default language for the text in this feed. |
| `defaultLang` | *string* (optional) | Specifies the language used when the data consumer doesn�t know the language of the user. |
| `feedStartDate` | *string* (optional) | The start date for the dataset. |
| `feedEndDate` | *string* (optional) | The end date for the dataset. |
| `feedVersion` | *string* (optional) | Version string that indicates the current version of their GTFS dataset. |
| `feedContactEmail` | *string* (optional) | Email address for communication with the data publisher. |
| `feedContactUrl` | *string* (optional) | URL for a web page that allows a feed consumer to contact the data publisher. |
### Message: GeneralTransitFeedStatic.Frequencies

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Frequencies` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Frequencies

*Defines frequencies.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `tripId` | *string* | Identifies a trip. |
| `startTime` | *string* | Time at which service begins with the specified frequency. |
| `endTime` | *string* | Time at which service ends with the specified frequency. |
| `headwaySecs` | *int* | Time between departures from the same stop (headway) for this trip, in seconds. |
| `exactTimes` | *int* (optional) | When 1, frequency-based trips should be exactly scheduled. When 0 (or empty), frequency-based trips are not exactly scheduled. |
### Message: GeneralTransitFeedStatic.Levels

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Levels` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Levels

*Defines levels.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `levelId` | *string* | Identifies a level. |
| `levelIndex` | *double* | Numeric index of the level that indicates relative position of the level in relation to other levels. |
| `levelName` | *string* (optional) | Name of the level. |
### Message: GeneralTransitFeedStatic.LocationGeoJson

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.LocationGeoJson` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: LocationGeoJson

*Defines location GeoJSON data.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `locationGeoJsonId` | *string* | Identifies a location GeoJSON. |
| `locationGeoJsonType` | *string* | Type of the GeoJSON. |
| `locationGeoJsonData` | *string* | GeoJSON data. |
### Message: GeneralTransitFeedStatic.LocationGroups

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.LocationGroups` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: LocationGroups

*Defines location groups.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `locationGroupId` | *string* | Identifies a location group. |
| `locationGroupName` | *string* | Name of the location group. |
| `locationGroupDesc` | *string* (optional) | Description of the location group. |
| `locationGroupUrl` | *string* (optional) | URL of a web page about the location group. |
### Message: GeneralTransitFeedStatic.LocationGroupStores

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.LocationGroupStores` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: LocationGroupStores

*Defines location group stores.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `locationGroupStoreId` | *string* | Identifies a location group store. |
| `locationGroupId` | *string* | Identifies a location group. |
| `storeId` | *string* | Identifies a store. |
### Message: GeneralTransitFeedStatic.Networks

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Networks` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Networks

*Defines networks.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `networkId` | *string* | Identifies a network. |
| `networkName` | *string* | Name of the network. |
| `networkDesc` | *string* (optional) | Description of the network. |
| `networkUrl` | *string* (optional) | URL of a web page about the network. |
### Message: GeneralTransitFeedStatic.Pathways

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Pathways` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Pathways

*Defines pathways.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `pathwayId` | *string* | Identifies a pathway. |
| `fromStopId` | *string* | Identifies a stop or station where the pathway begins. |
| `toStopId` | *string* | Identifies a stop or station where the pathway ends. |
| `pathwayMode` | *int* | Type of pathway between the specified (from_stop_id, to_stop_id) pair. |
| `isBidirectional` | *int* | When 1, the pathway can be used in both directions. When 0, the pathway can only be used from (from_stop_id) to (to_stop_id). |
| `length` | *double* (optional) | Length of the pathway, in meters. |
| `traversalTime` | *int* (optional) | Average time, in seconds, needed to walk through the pathway. |
| `stairCount` | *int* (optional) | Number of stairs of the pathway. |
| `maxSlope` | *double* (optional) | Maximum slope of the pathway, in percent. |
| `minWidth` | *double* (optional) | Minimum width of the pathway, in meters. |
| `signpostedAs` | *string* (optional) | Signposting information for the pathway. |
| `reversedSignpostedAs` | *string* (optional) | Reversed signposting information for the pathway. |
### Message: GeneralTransitFeedStatic.RouteNetworks

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.RouteNetworks` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: RouteNetworks

*Defines route networks.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `routeNetworkId` | *string* | Identifies a route network. |
| `routeId` | *string* | Identifies a route. |
| `networkId` | *string* | Identifies a network. |
### Message: GeneralTransitFeedStatic.Routes

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Routes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Routes

*Identifies a route.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `routeId` | *string* | Identifies a route. |
| `agencyId` | *string* (optional) | Agency for the specified route. |
| `routeShortName` | *string* (optional) | Short name of a route. |
| `routeLongName` | *string* (optional) | Full name of a route. |
| `routeDesc` | *string* (optional) | Description of a route that provides useful, quality information. |
| `routeType` | [Enum RouteType](#enum-routetype) | Indicates the type of transportation used on a route. |
| `routeUrl` | *string* (optional) | URL of a web page about the particular route. |
| `routeColor` | *string* (optional) | Route color designation that matches public facing material. |
| `routeTextColor` | *string* (optional) | Legible color to use for text drawn against a background of route_color. |
| `routeSortOrder` | *int* (optional) | Orders the routes in a way which is ideal for presentation to customers. |
| `continuousPickup` | [Enum ContinuousPickup](#enum-continuouspickup) | Indicates that the rider can board the transit vehicle at any point along the vehicle�s travel path. |
| `continuousDropOff` | [Enum ContinuousDropOff](#enum-continuousdropoff) | Indicates that the rider can alight from the transit vehicle at any point along the vehicle�s travel path. |
| `networkId` | *string* (optional) | Identifies a group of routes. |

---

##### Enum: RouteType

*Indicates the type of transportation used on a route. Symbols: TRAM - Tram, streetcar, light rail; SUBWAY - Subway, metro; RAIL - Intercity or long-distance travel; BUS - Short- and long-distance bus routes; FERRY - Boat service; CABLE_TRAM - Street-level rail cars with a cable running beneath the vehicle; AERIAL_LIFT - Cable transport with suspended cabins or chairs; FUNICULAR - Rail system designed for steep inclines; TROLLEYBUS - Electric buses with overhead wires; MONORAIL - Railway with a single rail or beam.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `TRAM` | 0 |  |
| `SUBWAY` | 1 |  |
| `RAIL` | 2 |  |
| `BUS` | 3 |  |
| `FERRY` | 4 |  |
| `CABLE_TRAM` | 5 |  |
| `AERIAL_LIFT` | 6 |  |
| `FUNICULAR` | 7 |  |
| `RESERVED_1` | 8 |  |
| `RESERVED_2` | 9 |  |
| `RESERVED_3` | 10 |  |
| `TROLLEYBUS` | 11 |  |
| `MONORAIL` | 12 |  |
| `OTHER` | 13 |  |

---

##### Enum: ContinuousPickup

*Indicates that the rider can board the transit vehicle at any point along the vehicle�s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping pickup; NO_CONTINUOUS_STOPPING - No continuous stopping pickup; PHONE_AGENCY - Must phone agency to arrange continuous stopping pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping pickup.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `CONTINUOUS_STOPPING` | 0 |  |
| `NO_CONTINUOUS_STOPPING` | 1 |  |
| `PHONE_AGENCY` | 2 |  |
| `COORDINATE_WITH_DRIVER` | 3 |  |

---

##### Enum: ContinuousDropOff

*Indicates that the rider can alight from the transit vehicle at any point along the vehicle�s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping drop off; NO_CONTINUOUS_STOPPING - No continuous stopping drop off; PHONE_AGENCY - Must phone agency to arrange continuous stopping drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping drop off.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `CONTINUOUS_STOPPING` | 0 |  |
| `NO_CONTINUOUS_STOPPING` | 1 |  |
| `PHONE_AGENCY` | 2 |  |
| `COORDINATE_WITH_DRIVER` | 3 |  |
### Message: GeneralTransitFeedStatic.Shapes

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Shapes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Shapes

*Defines shapes.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `shapeId` | *string* | Identifies a shape. |
| `shapePtLat` | *double* | Latitude of a shape point. |
| `shapePtLon` | *double* | Longitude of a shape point. |
| `shapePtSequence` | *int* | Sequence in which the shape points connect to form the shape. |
| `shapeDistTraveled` | *double* (optional) | Actual distance traveled along the shape from the first shape point to the specified shape point. |
### Message: GeneralTransitFeedStatic.StopAreas

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.StopAreas` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: StopAreas

*Defines stop areas.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `stopAreaId` | *string* | Identifies a stop area. |
| `stopId` | *string* | Identifies a stop. |
| `areaId` | *string* | Identifies an area. |
### Message: GeneralTransitFeedStatic.Stops

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Stops` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Stops

*Identifies locations such as stop/platform, station, entrance/exit, generic node or boarding area.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `stopId` | *string* | Identifies a location: stop/platform, station, entrance/exit, generic node or boarding area. |
| `stopCode` | *string* (optional) | Short text or a number that identifies the location for riders. |
| `stopName` | *string* (optional) | Name of the location. |
| `ttsStopName` | *string* (optional) | Readable version of the stop_name. |
| `stopDesc` | *string* (optional) | Description of the location that provides useful, quality information. |
| `stopLat` | *double* (optional) | Latitude of the location. |
| `stopLon` | *double* (optional) | Longitude of the location. |
| `zoneId` | *string* (optional) | Identifies the fare zone for a stop. |
| `stopUrl` | *string* (optional) | URL of a web page about the location. |
| `locationType` | [Enum LocationType](#enum-locationtype) | Location type. |
| `parentStation` | *string* (optional) | Defines hierarchy between the different locations. |
| `stopTimezone` | *string* (optional) | Timezone of the location. |
| `wheelchairBoarding` | [Enum WheelchairBoarding](#enum-wheelchairboarding) | Indicates whether wheelchair boardings are possible from the location. |
| `levelId` | *string* (optional) | Level of the location. |
| `platformCode` | *string* (optional) | Platform identifier for a platform stop. |

---

##### Enum: LocationType

*Location type. Symbols: STOP - Stop or platform; STATION - Physical structure or area that contains one or more platforms; ENTRANCE_EXIT - Location where passengers can enter or exit a station; GENERIC_NODE - Location within a station used to link pathways; BOARDING_AREA - Specific location on a platform where passengers can board and/or alight vehicles.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `STOP` | 0 |  |
| `STATION` | 1 |  |
| `ENTRANCE_EXIT` | 2 |  |
| `GENERIC_NODE` | 3 |  |
| `BOARDING_AREA` | 4 |  |

---

##### Enum: WheelchairBoarding

*Indicates whether wheelchair boardings are possible from the location. Symbols: NO_INFO - No accessibility information; SOME_VEHICLES - Some vehicles at this stop can be boarded by a rider in a wheelchair; NOT_POSSIBLE - Wheelchair boarding is not possible at this stop.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `NO_INFO` | 0 |  |
| `SOME_VEHICLES` | 1 |  |
| `NOT_POSSIBLE` | 2 |  |
### Message: GeneralTransitFeedStatic.StopTimes

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.StopTimes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: StopTimes

*Represents times that a vehicle arrives at and departs from individual stops for each trip.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `tripId` | *string* | Identifies a trip. |
| `arrivalTime` | *string* (optional) | Arrival time at the stop for a specific trip. |
| `departureTime` | *string* (optional) | Departure time from the stop for a specific trip. |
| `stopId` | *string* (optional) | Identifies the serviced stop. |
| `stopSequence` | *int* | Order of stops for a particular trip. |
| `stopHeadsign` | *string* (optional) | Text that appears on signage identifying the trip's destination to riders. |
| `pickupType` | [Enum PickupType](#enum-pickuptype) | Indicates pickup method. |
| `dropOffType` | [Enum DropOffType](#enum-dropofftype) | Indicates drop off method. |
| `continuousPickup` | [Enum ContinuousPickup](#enum-continuouspickup) (optional) | Indicates continuous stopping pickup. |
| `continuousDropOff` | [Enum ContinuousDropOff](#enum-continuousdropoff) (optional) | Indicates continuous stopping drop off. |
| `shapeDistTraveled` | *double* (optional) | Actual distance traveled along the shape from the first stop to the stop specified in this record. |
| `timepoint` | [Enum Timepoint](#enum-timepoint) | Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times. |

---

##### Enum: PickupType

*Indicates pickup method. Symbols: REGULAR - Regularly scheduled pickup; NO_PICKUP - No pickup available; PHONE_AGENCY - Must phone agency to arrange pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange pickup.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `REGULAR` | 0 |  |
| `NO_PICKUP` | 1 |  |
| `PHONE_AGENCY` | 2 |  |
| `COORDINATE_WITH_DRIVER` | 3 |  |

---

##### Enum: DropOffType

*Indicates drop off method. Symbols: REGULAR - Regularly scheduled drop off; NO_DROP_OFF - No drop off available; PHONE_AGENCY - Must phone agency to arrange drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange drop off.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `REGULAR` | 0 |  |
| `NO_DROP_OFF` | 1 |  |
| `PHONE_AGENCY` | 2 |  |
| `COORDINATE_WITH_DRIVER` | 3 |  |

---

##### Enum: ContinuousPickup

*Indicates that the rider can board the transit vehicle at any point along the vehicle�s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping pickup; NO_CONTINUOUS_STOPPING - No continuous stopping pickup; PHONE_AGENCY - Must phone agency to arrange continuous stopping pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping pickup.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `CONTINUOUS_STOPPING` | 0 |  |
| `NO_CONTINUOUS_STOPPING` | 1 |  |
| `PHONE_AGENCY` | 2 |  |
| `COORDINATE_WITH_DRIVER` | 3 |  |

---

##### Enum: ContinuousDropOff

*Indicates that the rider can alight from the transit vehicle at any point along the vehicle�s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping drop off; NO_CONTINUOUS_STOPPING - No continuous stopping drop off; PHONE_AGENCY - Must phone agency to arrange continuous stopping drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping drop off.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `CONTINUOUS_STOPPING` | 0 |  |
| `NO_CONTINUOUS_STOPPING` | 1 |  |
| `PHONE_AGENCY` | 2 |  |
| `COORDINATE_WITH_DRIVER` | 3 |  |

---

##### Enum: Timepoint

*Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times. Symbols: APPROXIMATE - Times are considered approximate; EXACT - Times are considered exact.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `APPROXIMATE` | 0 |  |
| `EXACT` | 1 |  |
### Message: GeneralTransitFeedStatic.Timeframes

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Timeframes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Timeframes

*Used to describe fares that can vary based on the time of day, the day of the week, or a particular day in the year.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `timeframeGroupId` | *string* | Identifies a timeframe or set of timeframes. |
| `startTime` | *string* (optional) | Defines the beginning of a timeframe. |
| `endTime` | *string* (optional) | Defines the end of a timeframe. |
| `serviceDates` | [Record Calendar](#record-calendar), [Record CalendarDates](#record-calendardates) | Identifies a set of dates when service is available for one or more routes. |

---

##### Record: Calendar

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `serviceId` | *string* | Identifies a set of dates when service is available for one or more routes. |
| `monday` | [Enum ServiceAvailability](#enum-serviceavailability) | Indicates whether the service operates on all Mondays in the date range specified. |
| `tuesday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Tuesdays in the date range specified. |
| `wednesday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Wednesdays in the date range specified. |
| `thursday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Thursdays in the date range specified. |
| `friday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Fridays in the date range specified. |
| `saturday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Saturdays in the date range specified. |
| `sunday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Sundays in the date range specified. |
| `startDate` | *string* | Start service day for the service interval. |
| `endDate` | *string* | End service day for the service interval. |

---

##### Record: CalendarDates

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `serviceId` | *string* | Identifies a set of dates when a service exception occurs for one or more routes. |
| `date` | *string* | Date when service exception occurs. |
| `exceptionType` | [Enum ExceptionType](#enum-exceptiontype) | Indicates whether service is available on the date specified. |

---

##### Enum: ServiceAvailability

*Indicates whether the service operates on all Mondays in the date range specified. Symbols: NO_SERVICE - Service is not available; SERVICE_AVAILABLE - Service is available.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `NO_SERVICE` | 0 |  |
| `SERVICE_AVAILABLE` | 1 |  |

---

##### Enum: ExceptionType

*Indicates whether service is available on the date specified. Symbols: SERVICE_ADDED - Service has been added for the specified date; SERVICE_REMOVED - Service has been removed for the specified date.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `SERVICE_ADDED` | 0 |  |
| `SERVICE_REMOVED` | 1 |  |
### Message: GeneralTransitFeedStatic.Transfers

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Transfers` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Transfers

*Defines transfers.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `fromStopId` | *string* | Identifies a stop or station where a connection between routes begins. |
| `toStopId` | *string* | Identifies a stop or station where a connection between routes ends. |
| `transferType` | *int* | Type of connection for the specified (from_stop_id, to_stop_id) pair. |
| `minTransferTime` | *int* (optional) | Amount of time, in seconds, needed to transfer from the specified (from_stop_id) to the specified (to_stop_id). |
### Message: GeneralTransitFeedStatic.Translations

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Translations` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Translations

*Defines translations.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `tableName` | *string* | Name of the table containing the field to be translated. |
| `fieldName` | *string* | Name of the field to be translated. |
| `language` | *string* | Language of the translation. |
| `translation` | *string* | Translated value. |
### Message: GeneralTransitFeedStatic.Trips

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Trips` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `False` | `{agencyid}` |

#### Schema:

##### Record: Trips

*Identifies a trip.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `routeId` | *string* | Identifies a route. |
| `serviceDates` | [Record Calendar](#record-calendar) |  |
| `serviceExceptions` | *array* |  |
| `tripId` | *string* | Identifies a trip. |
| `tripHeadsign` | *string* (optional) | Text that appears on signage identifying the trip's destination to riders. |
| `tripShortName` | *string* (optional) | Public facing text used to identify the trip to riders. |
| `directionId` | [Enum DirectionId](#enum-directionid) | Indicates the direction of travel for a trip. |
| `blockId` | *string* (optional) | Identifies the block to which the trip belongs. |
| `shapeId` | *string* (optional) | Identifies a geospatial shape describing the vehicle travel path for a trip. |
| `wheelchairAccessible` | [Enum WheelchairAccessible](#enum-wheelchairaccessible) | Indicates wheelchair accessibility. |
| `bikesAllowed` | [Enum BikesAllowed](#enum-bikesallowed) | Indicates whether bikes are allowed. |

---

##### Record: Calendar

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `serviceId` | *string* | Identifies a set of dates when service is available for one or more routes. |
| `monday` | [Enum ServiceAvailability](#enum-serviceavailability) | Indicates whether the service operates on all Mondays in the date range specified. |
| `tuesday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Tuesdays in the date range specified. |
| `wednesday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Wednesdays in the date range specified. |
| `thursday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Thursdays in the date range specified. |
| `friday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Fridays in the date range specified. |
| `saturday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Saturdays in the date range specified. |
| `sunday` | *GeneralTransitFeedStatic.ServiceAvailability* | Indicates whether the service operates on all Sundays in the date range specified. |
| `startDate` | *string* | Start service day for the service interval. |
| `endDate` | *string* | End service day for the service interval. |

---

##### Enum: DirectionId

*Indicates the direction of travel for a trip. Symbols: OUTBOUND - Travel in one direction; INBOUND - Travel in the opposite direction.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `OUTBOUND` | 0 |  |
| `INBOUND` | 1 |  |

---

##### Enum: WheelchairAccessible

*Indicates wheelchair accessibility. Symbols: NO_INFO - No accessibility information for the trip; WHEELCHAIR_ACCESSIBLE - Vehicle can accommodate at least one rider in a wheelchair; NOT_WHEELCHAIR_ACCESSIBLE - No riders in wheelchairs can be accommodated on this trip.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `NO_INFO` | 0 |  |
| `WHEELCHAIR_ACCESSIBLE` | 1 |  |
| `NOT_WHEELCHAIR_ACCESSIBLE` | 2 |  |

---

##### Enum: BikesAllowed

*Indicates whether bikes are allowed. Symbols: NO_INFO - No bike information for the trip; BICYCLE_ALLOWED - Vehicle can accommodate at least one bicycle; BICYCLE_NOT_ALLOWED - No bicycles are allowed on this trip.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `NO_INFO` | 0 |  |
| `BICYCLE_ALLOWED` | 1 |  |
| `BICYCLE_NOT_ALLOWED` | 2 |  |

---

##### Enum: ServiceAvailability

*Indicates whether the service operates on all Mondays in the date range specified. Symbols: NO_SERVICE - Service is not available; SERVICE_AVAILABLE - Service is available.*

| **Symbol** | **Ordinal** | **Description** |
|------------|-------------|-----------------|
| `NO_SERVICE` | 0 |  |
| `SERVICE_AVAILABLE` | 1 |  |
