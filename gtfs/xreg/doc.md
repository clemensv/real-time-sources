# Table of Contents

- [GeneralTransitFeedRealTime](#message-group-generaltransitfeedrealtime)
  - [GeneralTransitFeedRealTime.Vehicle.VehiclePosition](#message-generaltransitfeedrealtimevehiclevehicleposition)
  - [GeneralTransitFeedRealTime.Trip.TripUpdate](#message-generaltransitfeedrealtimetriptripupdate)
  - [GeneralTransitFeedRealTime.Alert.Alert](#message-generaltransitfeedrealtimealertalert)
- [GeneralTransitFeedStatic](#message-group-generaltransitfeedstatic)
  - [GeneralTransitFeedStatic.Agency](#message-generaltransitfeedstaticagency)
  - [GeneralTransitFeedStatic.Areas](#message-generaltransitfeedstaticareas)
  - [GeneralTransitFeedStatic.Attributions](#message-generaltransitfeedstaticattributions)
  - [GeneralTransitFeed.BookingRules](#message-generaltransitfeedbookingrules)
  - [GeneralTransitFeedStatic.FareAttributes](#message-generaltransitfeedstaticfareattributes)
  - [GeneralTransitFeedStatic.FareLegRules](#message-generaltransitfeedstaticfarelegrules)
  - [GeneralTransitFeedStatic.FareMedia](#message-generaltransitfeedstaticfaremedia)
  - [GeneralTransitFeedStatic.FareProducts](#message-generaltransitfeedstaticfareproducts)
  - [GeneralTransitFeedStatic.FareRules](#message-generaltransitfeedstaticfarerules)
  - [GeneralTransitFeedStatic.FareTransferRules](#message-generaltransitfeedstaticfaretransferrules)
  - [GeneralTransitFeedStatic.FeedInfo](#message-generaltransitfeedstaticfeedinfo)
  - [GeneralTransitFeedStatic.Frequencies](#message-generaltransitfeedstaticfrequencies)
  - [GeneralTransitFeedStatic.Levels](#message-generaltransitfeedstaticlevels)
  - [GeneralTransitFeedStatic.LocationGeoJson](#message-generaltransitfeedstaticlocationgeojson)
  - [GeneralTransitFeedStatic.LocationGroups](#message-generaltransitfeedstaticlocationgroups)
  - [GeneralTransitFeedStatic.LocationGroupStores](#message-generaltransitfeedstaticlocationgroupstores)
  - [GeneralTransitFeedStatic.Networks](#message-generaltransitfeedstaticnetworks)
  - [GeneralTransitFeedStatic.Pathways](#message-generaltransitfeedstaticpathways)
  - [GeneralTransitFeedStatic.RouteNetworks](#message-generaltransitfeedstaticroutenetworks)
  - [GeneralTransitFeedStatic.Routes](#message-generaltransitfeedstaticroutes)
  - [GeneralTransitFeedStatic.Shapes](#message-generaltransitfeedstaticshapes)
  - [GeneralTransitFeedStatic.StopAreas](#message-generaltransitfeedstaticstopareas)
  - [GeneralTransitFeedStatic.Stops](#message-generaltransitfeedstaticstops)
  - [GeneralTransitFeedStatic.StopTimes](#message-generaltransitfeedstaticstoptimes)
  - [GeneralTransitFeedStatic.Timeframes](#message-generaltransitfeedstatictimeframes)
  - [GeneralTransitFeedStatic.Transfers](#message-generaltransitfeedstatictransfers)
  - [GeneralTransitFeedStatic.Translations](#message-generaltransitfeedstatictranslations)
  - [GeneralTransitFeedStatic.Trips](#message-generaltransitfeedstatictrips)

---

## Message Group: GeneralTransitFeedRealTime

### Message: GeneralTransitFeedRealTime.Vehicle.VehiclePosition

**ID**: GeneralTransitFeedRealTime.Vehicle.VehiclePosition
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:33:53.276277
**Modified At**: 2024-09-14T19:33:53.276277

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedRealTime.Vehicle.VehiclePosition

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: VehiclePosition
Realtime positioning information for a given vehicle.

Fields:
- **trip** (union): The Trip that this vehicle is serving. Can be empty or partial if the vehicle can not be identified with a given trip instance.
  **Record**: TripDescriptor
  A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary,   start_time) is set. If route_id is also set, then it should be same as one   that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be   set. Note that if the trip_id is not known, then stop sequence ids in   TripUpdate are not sufficient, and stop_ids must be provided as well. In   addition, absolute arrival/departure times must be provided.

  Fields:
  - **trip_id** (string (optional)): The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary.
  - **route_id** (string (optional)): The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the
  - **direction_id** (int (optional)): direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future.
  - **start_time** (string (optional)): The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance.
  - **start_date** (string (optional)): Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format.
  - **schedule_relationship** (union): 
    **Enum**: ScheduleRelationship
    The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.
    Possible values:
    - SCHEDULED
    - ADDED
    - UNSCHEDULED
    - CANCELED
- **vehicle** (union): Additional information on the vehicle that is serving this trip.
  **Record**: VehicleDescriptor
  Identification information for the vehicle performing the trip.

  Fields:
  - **id** (string (optional)): Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to
  - **label** (string (optional)): help identify the correct vehicle.
  - **license_plate** (string (optional)): The license plate of the vehicle.
- **position** (union): Current position of this vehicle. The stop sequence index of the current stop. The meaning of
  **Record**: Position
  A position.

  Fields:
  - **latitude** (float): Degrees North, in the WGS-84 coordinate system.
  - **longitude** (float): Degrees East, in the WGS-84 coordinate system.
  - **bearing** (float (optional)): Bearing, in degrees, clockwise from North, i.e., 0 is North and 90 is East. This can be the compass bearing, or the direction towards the next stop or intermediate location. This should not be direction deduced from the sequence of previous positions, which can be computed from previous data.
  - **odometer** (double (optional)): Odometer value, in meters.
  - **speed** (float (optional)): Momentary speed measured by the vehicle, in meters per second.
- **current_stop_sequence** (int (optional)): current_stop_sequence (i.e., the stop that it refers to) is determined by current_status. If current_status is missing IN_TRANSIT_TO is assumed. Identifies the current stop. The value must be the same as in stops.txt in
- **stop_id** (string (optional)): the corresponding GTFS feed.
- **current_status** (union): The exact status of the vehicle with respect to the current stop. Ignored if current_stop_sequence is missing. Moment at which the vehicle's position was measured. In POSIX time
  **Enum**: VehicleStopStatus
  Possible values:
  - INCOMING_AT
  - STOPPED_AT
  - IN_TRANSIT_TO
- **timestamp** (long (optional)): (i.e., number of seconds since January 1st 1970 00:00:00 UTC).
- **congestion_level** (union): 
  **Enum**: CongestionLevel
  Congestion level that is affecting this vehicle.
  Possible values:
  - UNKNOWN_CONGESTION_LEVEL
  - RUNNING_SMOOTHLY
  - STOP_AND_GO
  - CONGESTION
  - SEVERE_CONGESTION
- **occupancy_status** (union): 
  **Enum**: OccupancyStatus
  The degree of passenger occupancy of the vehicle. This field is still experimental, and subject to change. It may be formally adopted in the future.
  Possible values:
  - EMPTY
  - MANY_SEATS_AVAILABLE
  - FEW_SEATS_AVAILABLE
  - STANDING_ROOM_ONLY
  - CRUSHED_STANDING_ROOM_ONLY
  - FULL
  - NOT_ACCEPTING_PASSENGERS
### Message: GeneralTransitFeedRealTime.Trip.TripUpdate

**ID**: GeneralTransitFeedRealTime.Trip.TripUpdate
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:33:56.509005
**Modified At**: 2024-09-14T19:33:56.509005

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedRealTime.Trip.TripUpdate

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: TripUpdate
Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule. - A trip that proceeds along a route but has no fixed schedule. - A trip that have been added or removed with regard to schedule. The updates can be for future, predicted arrival/departure events, or for past events that already occurred. Normally, updates should get more precise and more certain (see uncertainty below) as the events gets closer to current time. Even if that is not possible, the information for past events should be precise and certain. In particular, if an update points to time in the past but its update's uncertainty is not 0, the client should conclude that the update is a (wrong) prediction and that the trip has not completed yet. Note that the update can describe a trip that is already completed. To this end, it is enough to provide an update for the last stop of the trip. If the time of that is in the past, the client will conclude from that that the whole trip is in the past (it is possible, although inconsequential, to also provide updates for preceding stops). This option is most relevant for a trip that has completed ahead of schedule, but according to the schedule, the trip is still proceeding at the current time. Removing the updates for this trip could make the client assume that the trip is still proceeding. Note that the feed provider is allowed, but not required, to purge past updates - this is one case where this would be practically useful.

Fields:
- **trip** (record): The Trip that this message applies to. There can be at most one TripUpdate entity for each actual trip instance. If there is none, that means there is no prediction information available. It does *not* mean that the trip is progressing according to schedule.
  **Record**: TripDescriptor
  A descriptor that identifies an instance of a GTFS trip, or all instances of a trip along a route. - To specify a single trip instance, the trip_id (and if necessary,   start_time) is set. If route_id is also set, then it should be same as one   that the given trip corresponds to. - To specify all the trips along a given route, only the route_id should be   set. Note that if the trip_id is not known, then stop sequence ids in   TripUpdate are not sufficient, and stop_ids must be provided as well. In   addition, absolute arrival/departure times must be provided.

  Fields:
  - **trip_id** (string (optional)): The trip_id from the GTFS feed that this selector refers to. For non frequency-based trips, this field is enough to uniquely identify the trip. For frequency-based trip, start_time and start_date might also be necessary.
  - **route_id** (string (optional)): The route_id from the GTFS that this selector refers to. The direction_id from the GTFS feed trips.txt file, indicating the
  - **direction_id** (int (optional)): direction of travel for trips this selector refers to. This field is still experimental, and subject to change. It may be formally adopted in the future.
  - **start_time** (string (optional)): The initially scheduled start time of this trip instance. When the trip_id corresponds to a non-frequency-based trip, this field should either be omitted or be equal to the value in the GTFS feed. When the trip_id corresponds to a frequency-based trip, the start_time must be specified for trip updates and vehicle positions. If the trip corresponds to exact_times=1 GTFS record, then start_time must be some multiple (including zero) of headway_secs later than frequencies.txt start_time for the corresponding time period. If the trip corresponds to exact_times=0, then its start_time may be arbitrary, and is initially expected to be the first departure of the trip. Once established, the start_time of this frequency-based trip should be considered immutable, even if the first departure time changes -- that time change may instead be reflected in a StopTimeUpdate. Format and semantics of the field is same as that of GTFS/frequencies.txt/start_time, e.g., 11:15:35 or 25:15:35. The scheduled start date of this trip instance.
  - **start_date** (string (optional)): Must be provided to disambiguate trips that are so late as to collide with a scheduled trip on a next day. For example, for a train that departs 8:00 and 20:00 every day, and is 12 hours late, there would be two distinct trips on the same time. This field can be provided but is not mandatory for schedules in which such collisions are impossible - for example, a service running on hourly schedule where a vehicle that is one hour late is not considered to be related to schedule anymore. In YYYYMMDD format.
  - **schedule_relationship** (union): 
    **Enum**: ScheduleRelationship
    The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.
    Possible values:
    - SCHEDULED
    - ADDED
    - UNSCHEDULED
    - CANCELED
- **vehicle** (union): Additional information on the vehicle that is serving this trip.
  **Record**: VehicleDescriptor
  Identification information for the vehicle performing the trip.

  Fields:
  - **id** (string (optional)): Internal system identification of the vehicle. Should be unique per vehicle, and can be used for tracking the vehicle as it proceeds through the system. User visible label, i.e., something that must be shown to the passenger to
  - **label** (string (optional)): help identify the correct vehicle.
  - **license_plate** (string (optional)): The license plate of the vehicle.
- **stop_time_update** (array): Updates to StopTimes for the trip (both future, i.e., predictions, and in some cases, past ones, i.e., those that already happened). The updates must be sorted by stop_sequence, and apply for all the following stops of the trip up to the next specified one. Example 1: For a trip with 20 stops, a StopTimeUpdate with arrival delay and departure delay of 0 for stop_sequence of the current stop means that the trip is exactly on time. Example 2: For the same trip instance, 3 StopTimeUpdates are provided: - delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 - delay of unspecified duration for stop_sequence 10 This will be interpreted as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9 have delay of 1 min. - stop_sequences 10,... have unknown delay. Moment at which the vehicle's real-time progress was measured. In POSIX
- **timestamp** (long (optional)): time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC). The current schedule deviation for the trip.  Delay should only be
- **delay** (int (optional)): specified when the prediction is given relative to some existing schedule in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time. Delay information in StopTimeUpdates take precedent of trip-level delay information, such that trip-level delay is only propagated until the next stop along the trip with a StopTimeUpdate delay value specified. Feed providers are strongly encouraged to provide a TripUpdate.timestamp value indicating when the delay value was last updated, in order to evaluate the freshness of the data. NOTE: This field is still experimental, and subject to change. It may be formally adopted in the future.
### Message: GeneralTransitFeedRealTime.Alert.Alert

**ID**: GeneralTransitFeedRealTime.Alert.Alert
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:33:59.755279
**Modified At**: 2024-09-14T19:33:59.755279

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedRealTime.Alert.Alert

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Alert
An alert, indicating some sort of incident in the public transit network.

Fields:
- **active_period** (array): Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them.
- **informed_entity** (array): Entities whose users we should notify of this alert.
- **cause** (union): 
  **Enum**: Cause
  Cause of this alert.
  Possible values:
  - UNKNOWN_CAUSE
  - OTHER_CAUSE
  - TECHNICAL_PROBLEM
  - STRIKE
  - DEMONSTRATION
  - ACCIDENT
  - HOLIDAY
  - WEATHER
  - MAINTENANCE
  - CONSTRUCTION
  - POLICE_ACTIVITY
  - MEDICAL_EMERGENCY
- **effect** (union): 
  **Enum**: Effect
  What is the effect of this problem on the affected entity.
  Possible values:
  - NO_SERVICE
  - REDUCED_SERVICE
  - SIGNIFICANT_DELAYS
  - DETOUR
  - ADDITIONAL_SERVICE
  - MODIFIED_SERVICE
  - OTHER_EFFECT
  - UNKNOWN_EFFECT
  - STOP_MOVED
- **url** (union): The URL which provides additional information about the alert.
  **Record**: TranslatedString
  An internationalized message containing per-language versions of a snippet of text or a URL. One of the strings from a message will be picked up. The resolution proceeds as follows: 1. If the UI language matches the language code of a translation,    the first matching translation is picked. 2. If a default UI language (e.g., English) matches the language code of a    translation, the first matching translation is picked. 3. If some translation has an unspecified language code, that translation is    picked.

  Fields:
  - **translation** (array): At least one translation must be provided.
- **header_text** (GeneralTransitFeedRealTime.Alert.TranslatedString (optional)): Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the
- **description_text** (GeneralTransitFeedRealTime.Alert.TranslatedString (optional)): description should add to the information of the header.
## Message Group: GeneralTransitFeedStatic

### Message: GeneralTransitFeedStatic.Agency

**ID**: GeneralTransitFeedStatic.Agency
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:02.945459
**Modified At**: 2024-09-14T19:34:02.945459

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Agency

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Agency
Information about the transit agencies.

Fields:
- **agencyId** (string): Identifies a transit brand which is often synonymous with a transit agency.
- **agencyName** (string): Full name of the transit agency.
- **agencyUrl** (string): URL of the transit agency.
- **agencyTimezone** (string): Timezone where the transit agency is located.
- **agencyLang** (string (optional)): Primary language used by this transit agency.
- **agencyPhone** (string (optional)): A voice telephone number for the specified agency.
- **agencyFareUrl** (string (optional)): URL of a web page that allows a rider to purchase tickets or other fare instruments for that agency online.
- **agencyEmail** (string (optional)): Email address actively monitored by the agency’s customer service department.
### Message: GeneralTransitFeedStatic.Areas

**ID**: GeneralTransitFeedStatic.Areas
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:06.109457
**Modified At**: 2024-09-14T19:34:06.109457

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Areas

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Areas
Defines areas.

Fields:
- **areaId** (string): Identifies an area.
- **areaName** (string): Name of the area.
- **areaDesc** (string (optional)): Description of the area.
- **areaUrl** (string (optional)): URL of a web page about the area.
### Message: GeneralTransitFeedStatic.Attributions

**ID**: GeneralTransitFeedStatic.Attributions
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:09.322877
**Modified At**: 2024-09-14T19:34:09.322877

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Attributions

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Attributions
Provides information about the attributions.

Fields:
- **attributionId** (string (optional)): Identifies an attribution for the dataset.
- **agencyId** (string (optional)): Identifies the agency associated with the attribution.
- **routeId** (string (optional)): Identifies the route associated with the attribution.
- **tripId** (string (optional)): Identifies the trip associated with the attribution.
- **organizationName** (string): Name of the organization associated with the attribution.
- **isProducer** (int (optional)): Indicates if the organization is a producer.
- **isOperator** (int (optional)): Indicates if the organization is an operator.
- **isAuthority** (int (optional)): Indicates if the organization is an authority.
- **attributionUrl** (string (optional)): URL of a web page about the attribution.
- **attributionEmail** (string (optional)): Email address associated with the attribution.
- **attributionPhone** (string (optional)): Phone number associated with the attribution.
### Message: GeneralTransitFeed.BookingRules

**ID**: GeneralTransitFeed.BookingRules
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:12.495400
**Modified At**: 2024-09-14T19:34:12.495400

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeed.BookingRules

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: BookingRules
Defines booking rules.

Fields:
- **bookingRuleId** (string): Identifies a booking rule.
- **bookingRuleName** (string): Name of the booking rule.
- **bookingRuleDesc** (string (optional)): Description of the booking rule.
- **bookingRuleUrl** (string (optional)): URL of a web page about the booking rule.
### Message: GeneralTransitFeedStatic.FareAttributes

**ID**: GeneralTransitFeedStatic.FareAttributes
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:15.660243
**Modified At**: 2024-09-14T19:34:15.660243

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.FareAttributes

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: FareAttributes
Defines fare attributes.

Fields:
- **fareId** (string): Identifies a fare class.
- **price** (double): Fare price, in the unit specified by currency_type.
- **currencyType** (string): Currency type used to pay the fare.
- **paymentMethod** (int): When 0, fare must be paid on board. When 1, fare must be paid before boarding.
- **transfers** (int (optional)): Specifies the number of transfers permitted on this fare.
- **agencyId** (string (optional)): Identifies the agency for the specified fare.
- **transferDuration** (long (optional)): Length of time in seconds before a transfer expires.
### Message: GeneralTransitFeedStatic.FareLegRules

**ID**: GeneralTransitFeedStatic.FareLegRules
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:18.859990
**Modified At**: 2024-09-14T19:34:18.859990

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.FareLegRules

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: FareLegRules
Defines fare leg rules.

Fields:
- **fareLegRuleId** (string): Identifies a fare leg rule.
- **fareProductId** (string): Identifies a fare product.
- **legGroupId** (string (optional)): Identifies a group of legs.
- **networkId** (string (optional)): Identifies a network.
- **fromAreaId** (string (optional)): Identifies the origin area.
- **toAreaId** (string (optional)): Identifies the destination area.
### Message: GeneralTransitFeedStatic.FareMedia

**ID**: GeneralTransitFeedStatic.FareMedia
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:22.043899
**Modified At**: 2024-09-14T19:34:22.043899

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.FareMedia

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: FareMedia
Defines fare media.

Fields:
- **fareMediaId** (string): Identifies a fare media.
- **fareMediaName** (string): Name of the fare media.
- **fareMediaDesc** (string (optional)): Description of the fare media.
- **fareMediaUrl** (string (optional)): URL of a web page about the fare media.
### Message: GeneralTransitFeedStatic.FareProducts

**ID**: GeneralTransitFeedStatic.FareProducts
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:25.251924
**Modified At**: 2024-09-14T19:34:25.251924

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.FareProducts

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: FareProducts
Defines fare products.

Fields:
- **fareProductId** (string): Identifies a fare product.
- **fareProductName** (string): Name of the fare product.
- **fareProductDesc** (string (optional)): Description of the fare product.
- **fareProductUrl** (string (optional)): URL of a web page about the fare product.
### Message: GeneralTransitFeedStatic.FareRules

**ID**: GeneralTransitFeedStatic.FareRules
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:28.382751
**Modified At**: 2024-09-14T19:34:28.382751

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.FareRules

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: FareRules
Defines fare rules.

Fields:
- **fareId** (string): Identifies a fare class.
- **routeId** (string (optional)): Identifies a route associated with the fare.
- **originId** (string (optional)): Identifies the fare zone of the origin.
- **destinationId** (string (optional)): Identifies the fare zone of the destination.
- **containsId** (string (optional)): Identifies the fare zone that a rider will enter or leave.
### Message: GeneralTransitFeedStatic.FareTransferRules

**ID**: GeneralTransitFeedStatic.FareTransferRules
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:31.594438
**Modified At**: 2024-09-14T19:34:31.594438

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.FareTransferRules

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: FareTransferRules
Defines fare transfer rules.

Fields:
- **fareTransferRuleId** (string): Identifies a fare transfer rule.
- **fareProductId** (string): Identifies a fare product.
- **transferCount** (int (optional)): Number of transfers permitted.
- **fromLegGroupId** (string (optional)): Identifies the leg group from which the transfer starts.
- **toLegGroupId** (string (optional)): Identifies the leg group to which the transfer applies.
- **duration** (long (optional)): Length of time in seconds before a transfer expires.
- **durationType** (string (optional)): Type of duration for the transfer.
### Message: GeneralTransitFeedStatic.FeedInfo

**ID**: GeneralTransitFeedStatic.FeedInfo
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:34.800372
**Modified At**: 2024-09-14T19:34:34.800372

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.FeedInfo

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: FeedInfo
Provides information about the GTFS feed itself.

Fields:
- **feedPublisherName** (string): Full name of the organization that publishes the feed.
- **feedPublisherUrl** (string): URL of the feed publishing organization's website.
- **feedLang** (string): Default language for the text in this feed.
- **defaultLang** (string (optional)): Specifies the language used when the data consumer doesn’t know the language of the user.
- **feedStartDate** (string (optional)): The start date for the dataset.
- **feedEndDate** (string (optional)): The end date for the dataset.
- **feedVersion** (string (optional)): Version string that indicates the current version of their GTFS dataset.
- **feedContactEmail** (string (optional)): Email address for communication with the data publisher.
- **feedContactUrl** (string (optional)): URL for a web page that allows a feed consumer to contact the data publisher.
### Message: GeneralTransitFeedStatic.Frequencies

**ID**: GeneralTransitFeedStatic.Frequencies
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:37.975904
**Modified At**: 2024-09-14T19:34:37.975904

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Frequencies

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Frequencies
Defines frequencies.

Fields:
- **tripId** (string): Identifies a trip.
- **startTime** (string): Time at which service begins with the specified frequency.
- **endTime** (string): Time at which service ends with the specified frequency.
- **headwaySecs** (int): Time between departures from the same stop (headway) for this trip, in seconds.
- **exactTimes** (int (optional)): When 1, frequency-based trips should be exactly scheduled. When 0 (or empty), frequency-based trips are not exactly scheduled.
### Message: GeneralTransitFeedStatic.Levels

**ID**: GeneralTransitFeedStatic.Levels
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:41.164118
**Modified At**: 2024-09-14T19:34:41.164118

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Levels

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Levels
Defines levels.

Fields:
- **levelId** (string): Identifies a level.
- **levelIndex** (double): Numeric index of the level that indicates relative position of the level in relation to other levels.
- **levelName** (string (optional)): Name of the level.
### Message: GeneralTransitFeedStatic.LocationGeoJson

**ID**: GeneralTransitFeedStatic.LocationGeoJson
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:44.385665
**Modified At**: 2024-09-14T19:34:44.385665

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.LocationGeoJson

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: LocationGeoJson
Defines location GeoJSON data.

Fields:
- **locationGeoJsonId** (string): Identifies a location GeoJSON.
- **locationGeoJsonType** (string): Type of the GeoJSON.
- **locationGeoJsonData** (string): GeoJSON data.
### Message: GeneralTransitFeedStatic.LocationGroups

**ID**: GeneralTransitFeedStatic.LocationGroups
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:47.584486
**Modified At**: 2024-09-14T19:34:47.584486

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.LocationGroups

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: LocationGroups
Defines location groups.

Fields:
- **locationGroupId** (string): Identifies a location group.
- **locationGroupName** (string): Name of the location group.
- **locationGroupDesc** (string (optional)): Description of the location group.
- **locationGroupUrl** (string (optional)): URL of a web page about the location group.
### Message: GeneralTransitFeedStatic.LocationGroupStores

**ID**: GeneralTransitFeedStatic.LocationGroupStores
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:50.772270
**Modified At**: 2024-09-14T19:34:50.772270

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.LocationGroupStores

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: LocationGroupStores
Defines location group stores.

Fields:
- **locationGroupStoreId** (string): Identifies a location group store.
- **locationGroupId** (string): Identifies a location group.
- **storeId** (string): Identifies a store.
### Message: GeneralTransitFeedStatic.Networks

**ID**: GeneralTransitFeedStatic.Networks
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:53.975672
**Modified At**: 2024-09-14T19:34:53.975672

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Networks

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Networks
Defines networks.

Fields:
- **networkId** (string): Identifies a network.
- **networkName** (string): Name of the network.
- **networkDesc** (string (optional)): Description of the network.
- **networkUrl** (string (optional)): URL of a web page about the network.
### Message: GeneralTransitFeedStatic.Pathways

**ID**: GeneralTransitFeedStatic.Pathways
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:34:57.277576
**Modified At**: 2024-09-14T19:34:57.277576

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Pathways

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Pathways
Defines pathways.

Fields:
- **pathwayId** (string): Identifies a pathway.
- **fromStopId** (string): Identifies a stop or station where the pathway begins.
- **toStopId** (string): Identifies a stop or station where the pathway ends.
- **pathwayMode** (int): Type of pathway between the specified (from_stop_id, to_stop_id) pair.
- **isBidirectional** (int): When 1, the pathway can be used in both directions. When 0, the pathway can only be used from (from_stop_id) to (to_stop_id).
- **length** (double (optional)): Length of the pathway, in meters.
- **traversalTime** (int (optional)): Average time, in seconds, needed to walk through the pathway.
- **stairCount** (int (optional)): Number of stairs of the pathway.
- **maxSlope** (double (optional)): Maximum slope of the pathway, in percent.
- **minWidth** (double (optional)): Minimum width of the pathway, in meters.
- **signpostedAs** (string (optional)): Signposting information for the pathway.
- **reversedSignpostedAs** (string (optional)): Reversed signposting information for the pathway.
### Message: GeneralTransitFeedStatic.RouteNetworks

**ID**: GeneralTransitFeedStatic.RouteNetworks
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:00.516165
**Modified At**: 2024-09-14T19:35:00.516165

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.RouteNetworks

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: RouteNetworks
Defines route networks.

Fields:
- **routeNetworkId** (string): Identifies a route network.
- **routeId** (string): Identifies a route.
- **networkId** (string): Identifies a network.
### Message: GeneralTransitFeedStatic.Routes

**ID**: GeneralTransitFeedStatic.Routes
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:03.739840
**Modified At**: 2024-09-14T19:35:03.739840

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Routes

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Routes
Identifies a route.

Fields:
- **routeId** (string): Identifies a route.
- **agencyId** (string (optional)): Agency for the specified route.
- **routeShortName** (string (optional)): Short name of a route.
- **routeLongName** (string (optional)): Full name of a route.
- **routeDesc** (string (optional)): Description of a route that provides useful, quality information.
- **routeType** (enum): Indicates the type of transportation used on a route.
  **Enum**: RouteType
  Indicates the type of transportation used on a route. Symbols: TRAM - Tram, streetcar, light rail; SUBWAY - Subway, metro; RAIL - Intercity or long-distance travel; BUS - Short- and long-distance bus routes; FERRY - Boat service; CABLE_TRAM - Street-level rail cars with a cable running beneath the vehicle; AERIAL_LIFT - Cable transport with suspended cabins or chairs; FUNICULAR - Rail system designed for steep inclines; TROLLEYBUS - Electric buses with overhead wires; MONORAIL - Railway with a single rail or beam.
  Possible values:
  - TRAM
  - SUBWAY
  - RAIL
  - BUS
  - FERRY
  - CABLE_TRAM
  - AERIAL_LIFT
  - FUNICULAR
  - RESERVED_1
  - RESERVED_2
  - RESERVED_3
  - TROLLEYBUS
  - MONORAIL
  - OTHER
- **routeUrl** (string (optional)): URL of a web page about the particular route.
- **routeColor** (string (optional)): Route color designation that matches public facing material.
- **routeTextColor** (string (optional)): Legible color to use for text drawn against a background of route_color.
- **routeSortOrder** (int (optional)): Orders the routes in a way which is ideal for presentation to customers.
- **continuousPickup** (enum): Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path.
  **Enum**: ContinuousPickup
  Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping pickup; NO_CONTINUOUS_STOPPING - No continuous stopping pickup; PHONE_AGENCY - Must phone agency to arrange continuous stopping pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping pickup.
  Possible values:
  - CONTINUOUS_STOPPING
  - NO_CONTINUOUS_STOPPING
  - PHONE_AGENCY
  - COORDINATE_WITH_DRIVER
- **continuousDropOff** (enum): Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path.
  **Enum**: ContinuousDropOff
  Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping drop off; NO_CONTINUOUS_STOPPING - No continuous stopping drop off; PHONE_AGENCY - Must phone agency to arrange continuous stopping drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping drop off.
  Possible values:
  - CONTINUOUS_STOPPING
  - NO_CONTINUOUS_STOPPING
  - PHONE_AGENCY
  - COORDINATE_WITH_DRIVER
- **networkId** (string (optional)): Identifies a group of routes.
### Message: GeneralTransitFeedStatic.Shapes

**ID**: GeneralTransitFeedStatic.Shapes
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:06.980418
**Modified At**: 2024-09-14T19:35:06.980418

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Shapes

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Shapes
Defines shapes.

Fields:
- **shapeId** (string): Identifies a shape.
- **shapePtLat** (double): Latitude of a shape point.
- **shapePtLon** (double): Longitude of a shape point.
- **shapePtSequence** (int): Sequence in which the shape points connect to form the shape.
- **shapeDistTraveled** (double (optional)): Actual distance traveled along the shape from the first shape point to the specified shape point.
### Message: GeneralTransitFeedStatic.StopAreas

**ID**: GeneralTransitFeedStatic.StopAreas
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:10.194179
**Modified At**: 2024-09-14T19:35:10.194179

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.StopAreas

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: StopAreas
Defines stop areas.

Fields:
- **stopAreaId** (string): Identifies a stop area.
- **stopId** (string): Identifies a stop.
- **areaId** (string): Identifies an area.
### Message: GeneralTransitFeedStatic.Stops

**ID**: GeneralTransitFeedStatic.Stops
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:13.431326
**Modified At**: 2024-09-14T19:35:13.431326

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Stops

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Stops
Identifies locations such as stop/platform, station, entrance/exit, generic node or boarding area.

Fields:
- **stopId** (string): Identifies a location: stop/platform, station, entrance/exit, generic node or boarding area.
- **stopCode** (string (optional)): Short text or a number that identifies the location for riders.
- **stopName** (string (optional)): Name of the location.
- **ttsStopName** (string (optional)): Readable version of the stop_name.
- **stopDesc** (string (optional)): Description of the location that provides useful, quality information.
- **stopLat** (double (optional)): Latitude of the location.
- **stopLon** (double (optional)): Longitude of the location.
- **zoneId** (string (optional)): Identifies the fare zone for a stop.
- **stopUrl** (string (optional)): URL of a web page about the location.
- **locationType** (enum): Location type.
  **Enum**: LocationType
  Location type. Symbols: STOP - Stop or platform; STATION - Physical structure or area that contains one or more platforms; ENTRANCE_EXIT - Location where passengers can enter or exit a station; GENERIC_NODE - Location within a station used to link pathways; BOARDING_AREA - Specific location on a platform where passengers can board and/or alight vehicles.
  Possible values:
  - STOP
  - STATION
  - ENTRANCE_EXIT
  - GENERIC_NODE
  - BOARDING_AREA
- **parentStation** (string (optional)): Defines hierarchy between the different locations.
- **stopTimezone** (string (optional)): Timezone of the location.
- **wheelchairBoarding** (enum): Indicates whether wheelchair boardings are possible from the location.
  **Enum**: WheelchairBoarding
  Indicates whether wheelchair boardings are possible from the location. Symbols: NO_INFO - No accessibility information; SOME_VEHICLES - Some vehicles at this stop can be boarded by a rider in a wheelchair; NOT_POSSIBLE - Wheelchair boarding is not possible at this stop.
  Possible values:
  - NO_INFO
  - SOME_VEHICLES
  - NOT_POSSIBLE
- **levelId** (string (optional)): Level of the location.
- **platformCode** (string (optional)): Platform identifier for a platform stop.
### Message: GeneralTransitFeedStatic.StopTimes

**ID**: GeneralTransitFeedStatic.StopTimes
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:16.641750
**Modified At**: 2024-09-14T19:35:16.641750

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.StopTimes

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: StopTimes
Represents times that a vehicle arrives at and departs from individual stops for each trip.

Fields:
- **tripId** (string): Identifies a trip.
- **arrivalTime** (string (optional)): Arrival time at the stop for a specific trip.
- **departureTime** (string (optional)): Departure time from the stop for a specific trip.
- **stopId** (string (optional)): Identifies the serviced stop.
- **stopSequence** (int): Order of stops for a particular trip.
- **stopHeadsign** (string (optional)): Text that appears on signage identifying the trip's destination to riders.
- **pickupType** (enum): Indicates pickup method.
  **Enum**: PickupType
  Indicates pickup method. Symbols: REGULAR - Regularly scheduled pickup; NO_PICKUP - No pickup available; PHONE_AGENCY - Must phone agency to arrange pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange pickup.
  Possible values:
  - REGULAR
  - NO_PICKUP
  - PHONE_AGENCY
  - COORDINATE_WITH_DRIVER
- **dropOffType** (enum): Indicates drop off method.
  **Enum**: DropOffType
  Indicates drop off method. Symbols: REGULAR - Regularly scheduled drop off; NO_DROP_OFF - No drop off available; PHONE_AGENCY - Must phone agency to arrange drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange drop off.
  Possible values:
  - REGULAR
  - NO_DROP_OFF
  - PHONE_AGENCY
  - COORDINATE_WITH_DRIVER
- **continuousPickup** (union): Indicates continuous stopping pickup.
  **Enum**: ContinuousPickup
  Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping pickup; NO_CONTINUOUS_STOPPING - No continuous stopping pickup; PHONE_AGENCY - Must phone agency to arrange continuous stopping pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping pickup.
  Possible values:
  - CONTINUOUS_STOPPING
  - NO_CONTINUOUS_STOPPING
  - PHONE_AGENCY
  - COORDINATE_WITH_DRIVER
- **continuousDropOff** (union): Indicates continuous stopping drop off.
  **Enum**: ContinuousDropOff
  Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping drop off; NO_CONTINUOUS_STOPPING - No continuous stopping drop off; PHONE_AGENCY - Must phone agency to arrange continuous stopping drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping drop off.
  Possible values:
  - CONTINUOUS_STOPPING
  - NO_CONTINUOUS_STOPPING
  - PHONE_AGENCY
  - COORDINATE_WITH_DRIVER
- **shapeDistTraveled** (double (optional)): Actual distance traveled along the shape from the first stop to the stop specified in this record.
- **timepoint** (enum): Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times.
  **Enum**: Timepoint
  Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times. Symbols: APPROXIMATE - Times are considered approximate; EXACT - Times are considered exact.
  Possible values:
  - APPROXIMATE
  - EXACT
### Message: GeneralTransitFeedStatic.Timeframes

**ID**: GeneralTransitFeedStatic.Timeframes
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:19.852768
**Modified At**: 2024-09-14T19:35:19.852768

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Timeframes

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Timeframes
Used to describe fares that can vary based on the time of day, the day of the week, or a particular day in the year.

Fields:
- **timeframeGroupId** (string): Identifies a timeframe or set of timeframes.
- **startTime** (string (optional)): Defines the beginning of a timeframe.
- **endTime** (string (optional)): Defines the end of a timeframe.
- **serviceDates** (union): Identifies a set of dates when service is available for one or more routes.
  Union of types:
    **Record**: Calendar
    Fields:
    - **serviceId** (string): Identifies a set of dates when service is available for one or more routes.
    - **monday** (enum): Indicates whether the service operates on all Mondays in the date range specified.
      **Enum**: ServiceAvailability
      Indicates whether the service operates on all Mondays in the date range specified. Symbols: NO_SERVICE - Service is not available; SERVICE_AVAILABLE - Service is available.
      Possible values:
      - NO_SERVICE
      - SERVICE_AVAILABLE
    - **tuesday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Tuesdays in the date range specified.
    - **wednesday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Wednesdays in the date range specified.
    - **thursday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Thursdays in the date range specified.
    - **friday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Fridays in the date range specified.
    - **saturday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Saturdays in the date range specified.
    - **sunday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Sundays in the date range specified.
    - **startDate** (string): Start service day for the service interval.
    - **endDate** (string): End service day for the service interval.
    **Record**: CalendarDates
    Fields:
    - **serviceId** (string): Identifies a set of dates when a service exception occurs for one or more routes.
    - **date** (string): Date when service exception occurs.
    - **exceptionType** (enum): Indicates whether service is available on the date specified.
      **Enum**: ExceptionType
      Indicates whether service is available on the date specified. Symbols: SERVICE_ADDED - Service has been added for the specified date; SERVICE_REMOVED - Service has been removed for the specified date.
      Possible values:
      - SERVICE_ADDED
      - SERVICE_REMOVED
### Message: GeneralTransitFeedStatic.Transfers

**ID**: GeneralTransitFeedStatic.Transfers
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:23.095140
**Modified At**: 2024-09-14T19:35:23.095140

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Transfers

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Transfers
Defines transfers.

Fields:
- **fromStopId** (string): Identifies a stop or station where a connection between routes begins.
- **toStopId** (string): Identifies a stop or station where a connection between routes ends.
- **transferType** (int): Type of connection for the specified (from_stop_id, to_stop_id) pair.
- **minTransferTime** (int (optional)): Amount of time, in seconds, needed to transfer from the specified (from_stop_id) to the specified (to_stop_id).
### Message: GeneralTransitFeedStatic.Translations

**ID**: GeneralTransitFeedStatic.Translations
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:26.333256
**Modified At**: 2024-09-14T19:35:26.333256

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Translations

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Translations
Defines translations.

Fields:
- **tableName** (string): Name of the table containing the field to be translated.
- **fieldName** (string): Name of the field to be translated.
- **language** (string): Language of the translation.
- **translation** (string): Translated value.
### Message: GeneralTransitFeedStatic.Trips

**ID**: GeneralTransitFeedStatic.Trips
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro
**Created At**: 2024-09-14T19:35:29.580497
**Modified At**: 2024-09-14T19:35:29.580497

#### Metadata:

- **specversion**: CloudEvents version
  - Type: string
  - Required: True
  - Value: 1.0

- **type**: Event type
  - Type: string
  - Required: True
  - Value: GeneralTransitFeedStatic.Trips

- **source**: Source Feed URL
  - Type: uritemplate
  - Required: True
  - Value: {feedurl}

- **subject**: Provider name
  - Type: uritemplate
  - Required: False
  - Value: {agencyid}

#### Schema:

**Record**: Trips
Identifies a trip.

Fields:
- **routeId** (string): Identifies a route.
- **serviceDates** (record): 
  **Record**: Calendar
  Fields:
  - **serviceId** (string): Identifies a set of dates when service is available for one or more routes.
  - **monday** (enum): Indicates whether the service operates on all Mondays in the date range specified.
    **Enum**: ServiceAvailability
    Indicates whether the service operates on all Mondays in the date range specified. Symbols: NO_SERVICE - Service is not available; SERVICE_AVAILABLE - Service is available.
    Possible values:
    - NO_SERVICE
    - SERVICE_AVAILABLE
  - **tuesday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Tuesdays in the date range specified.
  - **wednesday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Wednesdays in the date range specified.
  - **thursday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Thursdays in the date range specified.
  - **friday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Fridays in the date range specified.
  - **saturday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Saturdays in the date range specified.
  - **sunday** (GeneralTransitFeedStatic.ServiceAvailability): Indicates whether the service operates on all Sundays in the date range specified.
  - **startDate** (string): Start service day for the service interval.
  - **endDate** (string): End service day for the service interval.
- **serviceExceptions** (array): 
- **tripId** (string): Identifies a trip.
- **tripHeadsign** (string (optional)): Text that appears on signage identifying the trip's destination to riders.
- **tripShortName** (string (optional)): Public facing text used to identify the trip to riders.
- **directionId** (enum): Indicates the direction of travel for a trip.
  **Enum**: DirectionId
  Indicates the direction of travel for a trip. Symbols: OUTBOUND - Travel in one direction; INBOUND - Travel in the opposite direction.
  Possible values:
  - OUTBOUND
  - INBOUND
- **blockId** (string (optional)): Identifies the block to which the trip belongs.
- **shapeId** (string (optional)): Identifies a geospatial shape describing the vehicle travel path for a trip.
- **wheelchairAccessible** (enum): Indicates wheelchair accessibility.
  **Enum**: WheelchairAccessible
  Indicates wheelchair accessibility. Symbols: NO_INFO - No accessibility information for the trip; WHEELCHAIR_ACCESSIBLE - Vehicle can accommodate at least one rider in a wheelchair; NOT_WHEELCHAIR_ACCESSIBLE - No riders in wheelchairs can be accommodated on this trip.
  Possible values:
  - NO_INFO
  - WHEELCHAIR_ACCESSIBLE
  - NOT_WHEELCHAIR_ACCESSIBLE
- **bikesAllowed** (enum): Indicates whether bikes are allowed.
  **Enum**: BikesAllowed
  Indicates whether bikes are allowed. Symbols: NO_INFO - No bike information for the trip; BICYCLE_ALLOWED - Vehicle can accommodate at least one bicycle; BICYCLE_NOT_ALLOWED - No bicycles are allowed on this trip.
  Possible values:
  - NO_INFO
  - BICYCLE_ALLOWED
  - BICYCLE_NOT_ALLOWED
