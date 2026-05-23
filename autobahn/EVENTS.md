# German Autobahn Traffic Events

CloudEvents and JsonStructure contract for the German Autobahn traffic feeder, including Kafka-compatible events and MQTT/UNS overlays.

- [DE.Autobahn](#message-group-deautobahn)
  - [DE.Autobahn.RoadworkAppeared](#message-deautobahnroadworkappeared)
  - [DE.Autobahn.RoadworkUpdated](#message-deautobahnroadworkupdated)
  - [DE.Autobahn.RoadworkResolved](#message-deautobahnroadworkresolved)
  - [DE.Autobahn.ShortTermRoadworkAppeared](#message-deautobahnshorttermroadworkappeared)
  - [DE.Autobahn.ShortTermRoadworkUpdated](#message-deautobahnshorttermroadworkupdated)
  - [DE.Autobahn.ShortTermRoadworkResolved](#message-deautobahnshorttermroadworkresolved)
  - [DE.Autobahn.WarningAppeared](#message-deautobahnwarningappeared)
  - [DE.Autobahn.WarningUpdated](#message-deautobahnwarningupdated)
  - [DE.Autobahn.WarningResolved](#message-deautobahnwarningresolved)
  - [DE.Autobahn.ClosureAppeared](#message-deautobahnclosureappeared)
  - [DE.Autobahn.ClosureUpdated](#message-deautobahnclosureupdated)
  - [DE.Autobahn.ClosureResolved](#message-deautobahnclosureresolved)
  - [DE.Autobahn.EntryExitClosureAppeared](#message-deautobahnentryexitclosureappeared)
  - [DE.Autobahn.EntryExitClosureUpdated](#message-deautobahnentryexitclosureupdated)
  - [DE.Autobahn.EntryExitClosureResolved](#message-deautobahnentryexitclosureresolved)
  - [DE.Autobahn.WeightLimit35RestrictionAppeared](#message-deautobahnweightlimit35restrictionappeared)
  - [DE.Autobahn.WeightLimit35RestrictionUpdated](#message-deautobahnweightlimit35restrictionupdated)
  - [DE.Autobahn.WeightLimit35RestrictionResolved](#message-deautobahnweightlimit35restrictionresolved)
  - [DE.Autobahn.ParkingLorryAppeared](#message-deautobahnparkinglorryappeared)
  - [DE.Autobahn.ParkingLorryUpdated](#message-deautobahnparkinglorryupdated)
  - [DE.Autobahn.ParkingLorryResolved](#message-deautobahnparkinglorryresolved)
  - [DE.Autobahn.ElectricChargingStationAppeared](#message-deautobahnelectricchargingstationappeared)
  - [DE.Autobahn.ElectricChargingStationUpdated](#message-deautobahnelectricchargingstationupdated)
  - [DE.Autobahn.ElectricChargingStationResolved](#message-deautobahnelectricchargingstationresolved)
  - [DE.Autobahn.StrongElectricChargingStationAppeared](#message-deautobahnstrongelectricchargingstationappeared)
  - [DE.Autobahn.StrongElectricChargingStationUpdated](#message-deautobahnstrongelectricchargingstationupdated)
  - [DE.Autobahn.StrongElectricChargingStationResolved](#message-deautobahnstrongelectricchargingstationresolved)
  - [DE.Autobahn.WebcamAppeared](#message-deautobahnwebcamappeared)
  - [DE.Autobahn.WebcamUpdated](#message-deautobahnwebcamupdated)
  - [DE.Autobahn.WebcamResolved](#message-deautobahnwebcamresolved)
- [DE.Autobahn.mqtt](#message-group-deautobahnmqtt)
  - [DE.Autobahn.RoadworkAppeared.mqtt](#message-deautobahnroadworkappearedmqtt)
  - [DE.Autobahn.RoadworkUpdated.mqtt](#message-deautobahnroadworkupdatedmqtt)
  - [DE.Autobahn.RoadworkResolved.mqtt](#message-deautobahnroadworkresolvedmqtt)
  - [DE.Autobahn.ShortTermRoadworkAppeared.mqtt](#message-deautobahnshorttermroadworkappearedmqtt)
  - [DE.Autobahn.ShortTermRoadworkUpdated.mqtt](#message-deautobahnshorttermroadworkupdatedmqtt)
  - [DE.Autobahn.ShortTermRoadworkResolved.mqtt](#message-deautobahnshorttermroadworkresolvedmqtt)
  - [DE.Autobahn.ClosureAppeared.mqtt](#message-deautobahnclosureappearedmqtt)
  - [DE.Autobahn.ClosureUpdated.mqtt](#message-deautobahnclosureupdatedmqtt)
  - [DE.Autobahn.ClosureResolved.mqtt](#message-deautobahnclosureresolvedmqtt)
  - [DE.Autobahn.EntryExitClosureAppeared.mqtt](#message-deautobahnentryexitclosureappearedmqtt)
  - [DE.Autobahn.EntryExitClosureUpdated.mqtt](#message-deautobahnentryexitclosureupdatedmqtt)
  - [DE.Autobahn.EntryExitClosureResolved.mqtt](#message-deautobahnentryexitclosureresolvedmqtt)
  - [DE.Autobahn.WarningAppeared.mqtt](#message-deautobahnwarningappearedmqtt)
  - [DE.Autobahn.WarningUpdated.mqtt](#message-deautobahnwarningupdatedmqtt)
  - [DE.Autobahn.WarningResolved.mqtt](#message-deautobahnwarningresolvedmqtt)
  - [DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt](#message-deautobahnweightlimit35restrictionappearedmqtt)
  - [DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt](#message-deautobahnweightlimit35restrictionupdatedmqtt)
  - [DE.Autobahn.WeightLimit35RestrictionResolved.mqtt](#message-deautobahnweightlimit35restrictionresolvedmqtt)
  - [DE.Autobahn.WebcamAppeared.mqtt](#message-deautobahnwebcamappearedmqtt)
  - [DE.Autobahn.WebcamUpdated.mqtt](#message-deautobahnwebcamupdatedmqtt)
  - [DE.Autobahn.WebcamResolved.mqtt](#message-deautobahnwebcamresolvedmqtt)
  - [DE.Autobahn.ParkingLorryAppeared.mqtt](#message-deautobahnparkinglorryappearedmqtt)
  - [DE.Autobahn.ParkingLorryUpdated.mqtt](#message-deautobahnparkinglorryupdatedmqtt)
  - [DE.Autobahn.ParkingLorryResolved.mqtt](#message-deautobahnparkinglorryresolvedmqtt)
  - [DE.Autobahn.ElectricChargingStationAppeared.mqtt](#message-deautobahnelectricchargingstationappearedmqtt)
  - [DE.Autobahn.ElectricChargingStationUpdated.mqtt](#message-deautobahnelectricchargingstationupdatedmqtt)
  - [DE.Autobahn.ElectricChargingStationResolved.mqtt](#message-deautobahnelectricchargingstationresolvedmqtt)
  - [DE.Autobahn.StrongElectricChargingStationAppeared.mqtt](#message-deautobahnstrongelectricchargingstationappearedmqtt)
  - [DE.Autobahn.StrongElectricChargingStationUpdated.mqtt](#message-deautobahnstrongelectricchargingstationupdatedmqtt)
  - [DE.Autobahn.StrongElectricChargingStationResolved.mqtt](#message-deautobahnstrongelectricchargingstationresolvedmqtt)

---

## Message Group: DE.Autobahn
---
### Message: DE.Autobahn.RoadworkAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.RoadworkAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.RoadworkUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.RoadworkUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.RoadworkResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.RoadworkResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ShortTermRoadworkAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ShortTermRoadworkAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ShortTermRoadworkUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ShortTermRoadworkUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ShortTermRoadworkResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ShortTermRoadworkResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WarningAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WarningAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: WarningEvent
*Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this warning item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for warning items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API warning item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API warning item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the warning item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `delay_minutes` | *integer* (optional) | min | `False` | delayTimeValue from the Autobahn warning item, expressed in minutes. |
| `average_speed_kmh` | *integer* (optional) | km/h | `False` | averageSpeed from the Autobahn warning item, expressed in kilometers per hour. |
| `abnormal_traffic_type` | *string* (optional) | - | `False` | abnormalTrafficType code from the Autobahn warning item. |
| `source_name` | *string* (optional) | - | `False` | source value from the Autobahn warning item that identifies the origin of the warning. |
---
### Message: DE.Autobahn.WarningUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WarningUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: WarningEvent
*Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this warning item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for warning items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API warning item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API warning item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the warning item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `delay_minutes` | *integer* (optional) | min | `False` | delayTimeValue from the Autobahn warning item, expressed in minutes. |
| `average_speed_kmh` | *integer* (optional) | km/h | `False` | averageSpeed from the Autobahn warning item, expressed in kilometers per hour. |
| `abnormal_traffic_type` | *string* (optional) | - | `False` | abnormalTrafficType code from the Autobahn warning item. |
| `source_name` | *string* (optional) | - | `False` | source value from the Autobahn warning item that identifies the origin of the warning. |
---
### Message: DE.Autobahn.WarningResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WarningResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: WarningEvent
*Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this warning item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for warning items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API warning item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API warning item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the warning item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `delay_minutes` | *integer* (optional) | min | `False` | delayTimeValue from the Autobahn warning item, expressed in minutes. |
| `average_speed_kmh` | *integer* (optional) | km/h | `False` | averageSpeed from the Autobahn warning item, expressed in kilometers per hour. |
| `abnormal_traffic_type` | *string* (optional) | - | `False` | abnormalTrafficType code from the Autobahn warning item. |
| `source_name` | *string* (optional) | - | `False` | source value from the Autobahn warning item that identifies the origin of the warning. |
---
### Message: DE.Autobahn.ClosureAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ClosureAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ClosureUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ClosureUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ClosureResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ClosureResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.EntryExitClosureAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.EntryExitClosureAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.EntryExitClosureUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.EntryExitClosureUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.EntryExitClosureResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.EntryExitClosureResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WeightLimit35RestrictionAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WeightLimit35RestrictionAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WeightLimit35RestrictionUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WeightLimit35RestrictionUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WeightLimit35RestrictionResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WeightLimit35RestrictionResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ParkingLorryAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ParkingLorryAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ParkingLorry
*Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this parking item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for lorry parking items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API parking item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API parking item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the parking item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the parking site location. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the parking site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the parking site location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `amenity_descriptions` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities. |
| `car_space_count` | *integer* (optional) | - | `False` | Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. |
| `lorry_space_count` | *integer* (optional) | - | `False` | Number of lorry spaces parsed from description lines that contain LKW Stellplätze. |
---
### Message: DE.Autobahn.ParkingLorryUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ParkingLorryUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ParkingLorry
*Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this parking item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for lorry parking items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API parking item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API parking item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the parking item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the parking site location. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the parking site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the parking site location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `amenity_descriptions` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities. |
| `car_space_count` | *integer* (optional) | - | `False` | Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. |
| `lorry_space_count` | *integer* (optional) | - | `False` | Number of lorry spaces parsed from description lines that contain LKW Stellplätze. |
---
### Message: DE.Autobahn.ParkingLorryResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ParkingLorryResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ParkingLorry
*Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this parking item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for lorry parking items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API parking item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API parking item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the parking item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the parking site location. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the parking site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the parking site location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `amenity_descriptions` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities. |
| `car_space_count` | *integer* (optional) | - | `False` | Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. |
| `lorry_space_count` | *integer* (optional) | - | `False` | Number of lorry spaces parsed from description lines that contain LKW Stellplätze. |
---
### Message: DE.Autobahn.ElectricChargingStationAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ElectricChargingStationAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ElectricChargingStationUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ElectricChargingStationUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ElectricChargingStationResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ElectricChargingStationResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.StrongElectricChargingStationAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.StrongElectricChargingStationAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.StrongElectricChargingStationUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.StrongElectricChargingStationUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.StrongElectricChargingStationResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.StrongElectricChargingStationResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WebcamAppeared
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WebcamAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: Webcam
*Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this webcam item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for webcam items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API webcam item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API webcam item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam location as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the webcam item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the webcam location. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the webcam location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `operator_name` | *string* (optional) | - | `False` | operator value from the Autobahn API webcam item. |
| `image_url` | *uri* (optional) | - | `False` | imageurl value from the Autobahn API webcam item for the still image. |
| `stream_url` | *uri* (optional) | - | `False` | linkurl value from the Autobahn API webcam item for the linked stream or detail page. |
---
### Message: DE.Autobahn.WebcamUpdated
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WebcamUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: Webcam
*Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this webcam item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for webcam items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API webcam item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API webcam item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam location as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the webcam item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the webcam location. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the webcam location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `operator_name` | *string* (optional) | - | `False` | operator value from the Autobahn API webcam item. |
| `image_url` | *uri* (optional) | - | `False` | imageurl value from the Autobahn API webcam item for the still image. |
| `stream_url` | *uri* (optional) | - | `False` | linkurl value from the Autobahn API webcam item for the linked stream or detail page. |
---
### Message: DE.Autobahn.WebcamResolved
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WebcamResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: Webcam
*Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this webcam item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for webcam items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API webcam item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API webcam item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam location as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the webcam item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the webcam location. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the webcam location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `operator_name` | *string* (optional) | - | `False` | operator value from the Autobahn API webcam item. |
| `image_url` | *uri* (optional) | - | `False` | imageurl value from the Autobahn API webcam item for the still image. |
| `stream_url` | *uri* (optional) | - | `False` | linkurl value from the Autobahn API webcam item for the linked stream or detail page. |
## Message Group: DE.Autobahn.mqtt
---
### Message: DE.Autobahn.RoadworkAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.RoadworkAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.RoadworkUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.RoadworkUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.RoadworkResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.RoadworkResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ShortTermRoadworkAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ShortTermRoadworkAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ShortTermRoadworkUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ShortTermRoadworkUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ShortTermRoadworkResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ShortTermRoadworkResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ClosureAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ClosureAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ClosureUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ClosureUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ClosureResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ClosureResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.EntryExitClosureAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.EntryExitClosureAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.EntryExitClosureUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.EntryExitClosureUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.EntryExitClosureResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.EntryExitClosureResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WarningAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WarningAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: WarningEvent
*Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this warning item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for warning items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API warning item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API warning item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the warning item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `delay_minutes` | *integer* (optional) | min | `False` | delayTimeValue from the Autobahn warning item, expressed in minutes. |
| `average_speed_kmh` | *integer* (optional) | km/h | `False` | averageSpeed from the Autobahn warning item, expressed in kilometers per hour. |
| `abnormal_traffic_type` | *string* (optional) | - | `False` | abnormalTrafficType code from the Autobahn warning item. |
| `source_name` | *string* (optional) | - | `False` | source value from the Autobahn warning item that identifies the origin of the warning. |
---
### Message: DE.Autobahn.WarningUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WarningUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: WarningEvent
*Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this warning item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for warning items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API warning item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API warning item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the warning item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `delay_minutes` | *integer* (optional) | min | `False` | delayTimeValue from the Autobahn warning item, expressed in minutes. |
| `average_speed_kmh` | *integer* (optional) | km/h | `False` | averageSpeed from the Autobahn warning item, expressed in kilometers per hour. |
| `abnormal_traffic_type` | *string* (optional) | - | `False` | abnormalTrafficType code from the Autobahn warning item. |
| `source_name` | *string* (optional) | - | `False` | source value from the Autobahn warning item that identifies the origin of the warning. |
---
### Message: DE.Autobahn.WarningResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WarningResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: WarningEvent
*Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this warning item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for warning items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API warning item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API warning item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the warning segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the warning item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `delay_minutes` | *integer* (optional) | min | `False` | delayTimeValue from the Autobahn warning item, expressed in minutes. |
| `average_speed_kmh` | *integer* (optional) | km/h | `False` | averageSpeed from the Autobahn warning item, expressed in kilometers per hour. |
| `abnormal_traffic_type` | *string* (optional) | - | `False` | abnormalTrafficType code from the Autobahn warning item. |
| `source_name` | *string* (optional) | - | `False` | source value from the Autobahn warning item that identifies the origin of the warning. |
---
### Message: DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WeightLimit35RestrictionAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WeightLimit35RestrictionUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WeightLimit35RestrictionResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WeightLimit35RestrictionResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RoadEvent
*Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. |
| `display_type` | *string* | - | `True` | Autobahn API display_type value that identifies the road-event subtype. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the item as a future event. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the affected road segment as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. |
| `start_timestamp` | *datetime* (optional) | - | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the affected road segment. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the affected point on the road segment. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `geometry_json` | *string* (optional) | - | `False` | Serialized Autobahn API geometry object for the affected road segment. |
| `impact_lower` | *string* (optional) | - | `False` | Lower bound from the Autobahn API impact object. |
| `impact_upper` | *string* (optional) | - | `False` | Upper bound from the Autobahn API impact object. |
| `impact_symbols` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Impact symbols from the Autobahn API impact.symbols array. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.WebcamAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WebcamAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: Webcam
*Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this webcam item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for webcam items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API webcam item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API webcam item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam location as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the webcam item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the webcam location. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the webcam location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `operator_name` | *string* (optional) | - | `False` | operator value from the Autobahn API webcam item. |
| `image_url` | *uri* (optional) | - | `False` | imageurl value from the Autobahn API webcam item for the still image. |
| `stream_url` | *uri* (optional) | - | `False` | linkurl value from the Autobahn API webcam item for the linked stream or detail page. |
---
### Message: DE.Autobahn.WebcamUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WebcamUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: Webcam
*Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this webcam item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for webcam items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API webcam item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API webcam item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam location as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the webcam item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the webcam location. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the webcam location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `operator_name` | *string* (optional) | - | `False` | operator value from the Autobahn API webcam item. |
| `image_url` | *uri* (optional) | - | `False` | imageurl value from the Autobahn API webcam item for the still image. |
| `stream_url` | *uri* (optional) | - | `False` | linkurl value from the Autobahn API webcam item for the linked stream or detail page. |
---
### Message: DE.Autobahn.WebcamResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.WebcamResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: Webcam
*Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this webcam item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for webcam items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API webcam item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API webcam item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the webcam location as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the webcam item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the webcam location. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the webcam location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `operator_name` | *string* (optional) | - | `False` | operator value from the Autobahn API webcam item. |
| `image_url` | *uri* (optional) | - | `False` | imageurl value from the Autobahn API webcam item for the still image. |
| `stream_url` | *uri* (optional) | - | `False` | linkurl value from the Autobahn API webcam item for the linked stream or detail page. |
---
### Message: DE.Autobahn.ParkingLorryAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ParkingLorryAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ParkingLorry
*Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this parking item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for lorry parking items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API parking item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API parking item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the parking item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the parking site location. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the parking site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the parking site location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `amenity_descriptions` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities. |
| `car_space_count` | *integer* (optional) | - | `False` | Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. |
| `lorry_space_count` | *integer* (optional) | - | `False` | Number of lorry spaces parsed from description lines that contain LKW Stellplätze. |
---
### Message: DE.Autobahn.ParkingLorryUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ParkingLorryUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ParkingLorry
*Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this parking item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for lorry parking items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API parking item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API parking item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the parking item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the parking site location. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the parking site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the parking site location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `amenity_descriptions` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities. |
| `car_space_count` | *integer* (optional) | - | `False` | Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. |
| `lorry_space_count` | *integer* (optional) | - | `False` | Number of lorry spaces parsed from description lines that contain LKW Stellplätze. |
---
### Message: DE.Autobahn.ParkingLorryResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ParkingLorryResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ParkingLorry
*Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this parking item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for lorry parking items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API parking item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API parking item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the parking site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the parking item. |
| `start_lc_position` | *integer* (optional) | - | `False` | Numeric startLcPosition value emitted by the Autobahn API for the parking site location. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the parking site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the parking site location. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
| `amenity_descriptions` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities. |
| `car_space_count` | *integer* (optional) | - | `False` | Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. |
| `lorry_space_count` | *integer* (optional) | - | `False` | Number of lorry spaces parsed from description lines that contain LKW Stellplätze. |
---
### Message: DE.Autobahn.ElectricChargingStationAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ElectricChargingStationAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ElectricChargingStationUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ElectricChargingStationUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.ElectricChargingStationResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.ElectricChargingStationResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.StrongElectricChargingStationAppeared.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.StrongElectricChargingStationAppeared` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.StrongElectricChargingStationUpdated.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.StrongElectricChargingStationUpdated` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |
---
### Message: DE.Autobahn.StrongElectricChargingStationResolved.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Autobahn.StrongElectricChargingStationResolved` |
| `source` |  | `` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: ChargingStation
*Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. |
| `road` | *string* | - | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. |
| `road_ids` | array of *string* | - | `True` | Autobahn road identifiers for the road query that yielded this charging station item. |
| `event_time` | *datetime* | - | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. |
| `display_type` | *string* | - | `True` | Autobahn API display_type for charging-station items. |
| `title` | *string* (optional) | - | `False` | Human-readable title from the Autobahn API charging-station item. |
| `subtitle` | *string* (optional) | - | `False` | Human-readable subtitle from the Autobahn API charging-station item. |
| `description_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Description lines from the Autobahn API description array. |
| `future` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station item as a future entry. |
| `is_blocked` | *boolean* (optional) | - | `False` | Whether the Autobahn API marks the charging station site as blocked. |
| `icon` | *string* (optional) | - | `False` | Autobahn API icon identifier for the charging station item. |
| `extent` | *string* (optional) | - | `False` | Autobahn API extent text for the charging station site. |
| `point` | *string* (optional) | - | `False` | Autobahn API point text that identifies the charging station site. |
| `coordinate_lat` | *double* (optional) | - | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `coordinate_lon` | *double* (optional) | - | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. |
| `address_line` | *string* (optional) | - | `False` | Address line parsed from the first Autobahn API description line for the charging station site. |
| `charging_point_count` | *integer* (optional) | - | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. |
| `charging_points_json` | *string* (optional) | - | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. |
| `route_recommendation_json` | *string* (optional) | - | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. |
| `footer_lines` | *{'$ref': '#/definitions/StringList'}* (optional) | - | `False` | Footer lines from the Autobahn API footer array. |

## Subscription patterns

The MQTT/UNS feeder publishes under `traffic/de/autobahn/autobahn/{road}/{kind}/{identifier}/{state}`. Useful wildcard subscriptions include:

- All Autobahn MQTT events: `traffic/de/autobahn/autobahn/#`
- All roadworks on A1: `traffic/de/autobahn/autobahn/a1/roadwork/+/+`
- All closures and lifecycle states on A3: `traffic/de/autobahn/autobahn/a3/closure/+/+`
- All retained webcam slots: `traffic/de/autobahn/autobahn/+/webcam/+/+`
- All charging station changes: `traffic/de/autobahn/autobahn/+/+/+/+` filtered by kind `electric-charging-station` or `strong-electric-charging-station`.
