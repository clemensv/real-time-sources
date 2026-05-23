# BfS ODL Events

CloudEvents for the German BfS ODL gamma dose rate monitoring network.

- [de.bfs.odl.mqtt](#message-group-debfsodlmqtt)
  - [de.bfs.odl.mqtt.Station](#message-debfsodlmqttstation)
  - [de.bfs.odl.mqtt.DoseRateMeasurement](#message-debfsodlmqttdoseratemeasurement)
- [de.bfs.odl](#message-group-debfsodl)
  - [de.bfs.odl.Station](#message-debfsodlstation)
  - [de.bfs.odl.DoseRateMeasurement](#message-debfsodldoseratemeasurement)

---

## Message Group: de.bfs.odl.mqtt
---
### Message: de.bfs.odl.mqtt.Station
*Metadata for an ODL (Ortsdosisleistung) measuring station in the BfS gamma dose rate monitoring network. The BfS operates approximately 1,700 stationary probes across Germany that continuously measure ambient gamma dose rate. Station metadata includes the geographic position, elevation above sea level, postal code, and operational status of each probe.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `de.bfs.odl.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Metadata for a BfS ODL gamma dose rate monitoring station. Each station is a stationary probe in the IMIS (Integrated Measuring and Information System) network operated by the German Federal Office for Radiation Protection (Bundesamt für Strahlenschutz). Stations continuously measure ambient gamma dose rate and report hourly averaged values.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Nine-digit station identifier (Kennziffer) assigned by BfS in the IMIS network. Composed of the official municipality key (AGS) prefix and a station sequence number. Example: '033510091'. This is the stable key used for timeseries retrieval. |
| `state` | *string* | - | `True` | German federal state (Bundesland) derived from the first two digits of the station Kennziffer (AGS prefix). Normalized to lowercase kebab-case for use as the {state} segment in the MQTT/UNS topic. Example: 'niedersachsen', 'bayern', 'nordrhein-westfalen'. |
| `station_code` | *string* | - | `True` | Short alphanumeric station code assigned by BfS, consisting of a 'DEZ' prefix followed by a four-digit number. Example: 'DEZ0305'. Used in the BfS web interface and download area. |
| `name` | *string* | - | `True` | Human-readable name of the station location, typically a German municipality or locality name. Example: 'Flensburg'. |
| `postal_code` | *string* | - | `True` | German postal code (Postleitzahl / PLZ) of the station location. Five digits as a string. |
| `site_status` | *int32* | - | `True` | Numeric operational status code. 1 = in operation (in Betrieb), 0 or other values indicate the station is decommissioned or under maintenance. |
| `site_status_text` | *string* | - | `True` | Human-readable German text describing the operational status. Example: 'in Betrieb' (in operation). |
| `kid` | *int32* | - | `True` | Numeric region identifier (Kreis-ID) used internally by BfS to group stations into geographic regions. |
| `height_above_sea` | *double* (optional) | m | `True` | Elevation of the station above mean sea level in meters (Normalhöhennull / NHN). Determines the cosmic radiation component. Null if unknown. |
| `longitude` | *double* | deg (°) | `True` | Longitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates. |
| `latitude` | *double* | deg (°) | `True` | Latitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates. |
---
### Message: de.bfs.odl.mqtt.DoseRateMeasurement
*A one-hour averaged ambient gamma dose rate measurement from the BfS ODL monitoring network. Each measurement reports the gross gamma dose rate in microsieverts per hour (µSv/h), optionally split into cosmic and terrestrial components. The cosmic component originates from secondary cosmic radiation and depends primarily on altitude; the terrestrial component originates from naturally occurring radionuclides in the ground and varies with local geology.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `de.bfs.odl.DoseRateMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: DoseRateMeasurement
*A one-hour averaged ambient gamma dose rate measurement from a BfS ODL station. The gross dose rate value is the total ambient dose equivalent rate H*(10) at 1 meter above ground, expressed in microsieverts per hour (µSv/h). It may be decomposed into a cosmic component (secondary cosmic radiation, altitude-dependent) and a terrestrial component (naturally occurring radionuclides in soil, geology-dependent). Normal background levels in Germany range from approximately 0.05 to 0.18 µSv/h depending on local geology and altitude.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Nine-digit station identifier (Kennziffer) of the measuring probe. Matches the station_id in the Station schema. |
| `state` | *string* | - | `True` | German federal state (Bundesland) derived from the station Kennziffer. Propagated from station catalog so subscribers can route by state without a catalog join. Used as the {state} segment of the MQTT/UNS topic. |
| `start_measure` | *string* | - | `True` | Start of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T12:00:00Z'. |
| `end_measure` | *string* | - | `True` | End of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T13:00:00Z'. |
| `value` | *double* (optional) | uSv/h (µSv/h) | `True` | Gross ambient gamma dose rate averaged over the measurement period in microsieverts per hour (µSv/h). This is the total dose rate including both cosmic and terrestrial components. Null if the station did not report a valid measurement for this interval. |
| `value_cosmic` | *double* (optional) | uSv/h (µSv/h) | `True` | Cosmic radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Estimated from the station's altitude using a standard model. Null when the BfS system has not yet computed the decomposition for this measurement. |
| `value_terrestrial` | *double* (optional) | uSv/h (µSv/h) | `True` | Terrestrial radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Computed as gross value minus cosmic component. Varies with local geology (granite, basalt, sediment). Null when the cosmic component is not available. |
| `validated` | *int32* | - | `True` | Data validation flag. 1 = the measurement has been validated by BfS quality control. 0 = the measurement is preliminary or unvalidated. |
| `nuclide` | *string* | - | `True` | Nuclide identifier describing the type of radiation measured. For standard ODL probes this is always 'Gamma-ODL-Brutto' (gross gamma ambient dose rate). |
## Message Group: de.bfs.odl
---
### Message: de.bfs.odl.Station
*Metadata for an ODL (Ortsdosisleistung) measuring station in the BfS gamma dose rate monitoring network. The BfS operates approximately 1,700 stationary probes across Germany that continuously measure ambient gamma dose rate. Station metadata includes the geographic position, elevation above sea level, postal code, and operational status of each probe.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `de.bfs.odl.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Metadata for a BfS ODL gamma dose rate monitoring station. Each station is a stationary probe in the IMIS (Integrated Measuring and Information System) network operated by the German Federal Office for Radiation Protection (Bundesamt für Strahlenschutz). Stations continuously measure ambient gamma dose rate and report hourly averaged values.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Nine-digit station identifier (Kennziffer) assigned by BfS in the IMIS network. Composed of the official municipality key (AGS) prefix and a station sequence number. Example: '033510091'. This is the stable key used for timeseries retrieval. |
| `state` | *string* | - | `True` | German federal state (Bundesland) derived from the first two digits of the station Kennziffer (AGS prefix). Normalized to lowercase kebab-case for use as the {state} segment in the MQTT/UNS topic. Example: 'niedersachsen', 'bayern', 'nordrhein-westfalen'. |
| `station_code` | *string* | - | `True` | Short alphanumeric station code assigned by BfS, consisting of a 'DEZ' prefix followed by a four-digit number. Example: 'DEZ0305'. Used in the BfS web interface and download area. |
| `name` | *string* | - | `True` | Human-readable name of the station location, typically a German municipality or locality name. Example: 'Flensburg'. |
| `postal_code` | *string* | - | `True` | German postal code (Postleitzahl / PLZ) of the station location. Five digits as a string. |
| `site_status` | *int32* | - | `True` | Numeric operational status code. 1 = in operation (in Betrieb), 0 or other values indicate the station is decommissioned or under maintenance. |
| `site_status_text` | *string* | - | `True` | Human-readable German text describing the operational status. Example: 'in Betrieb' (in operation). |
| `kid` | *int32* | - | `True` | Numeric region identifier (Kreis-ID) used internally by BfS to group stations into geographic regions. |
| `height_above_sea` | *double* (optional) | m | `True` | Elevation of the station above mean sea level in meters (Normalhöhennull / NHN). Determines the cosmic radiation component. Null if unknown. |
| `longitude` | *double* | deg (°) | `True` | Longitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates. |
| `latitude` | *double* | deg (°) | `True` | Latitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates. |
---
### Message: de.bfs.odl.DoseRateMeasurement
*A one-hour averaged ambient gamma dose rate measurement from the BfS ODL monitoring network. Each measurement reports the gross gamma dose rate in microsieverts per hour (µSv/h), optionally split into cosmic and terrestrial components. The cosmic component originates from secondary cosmic radiation and depends primarily on altitude; the terrestrial component originates from naturally occurring radionuclides in the ground and varies with local geology.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `de.bfs.odl.DoseRateMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: DoseRateMeasurement
*A one-hour averaged ambient gamma dose rate measurement from a BfS ODL station. The gross dose rate value is the total ambient dose equivalent rate H*(10) at 1 meter above ground, expressed in microsieverts per hour (µSv/h). It may be decomposed into a cosmic component (secondary cosmic radiation, altitude-dependent) and a terrestrial component (naturally occurring radionuclides in soil, geology-dependent). Normal background levels in Germany range from approximately 0.05 to 0.18 µSv/h depending on local geology and altitude.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | Nine-digit station identifier (Kennziffer) of the measuring probe. Matches the station_id in the Station schema. |
| `state` | *string* | - | `True` | German federal state (Bundesland) derived from the station Kennziffer. Propagated from station catalog so subscribers can route by state without a catalog join. Used as the {state} segment of the MQTT/UNS topic. |
| `start_measure` | *string* | - | `True` | Start of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T12:00:00Z'. |
| `end_measure` | *string* | - | `True` | End of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T13:00:00Z'. |
| `value` | *double* (optional) | uSv/h (µSv/h) | `True` | Gross ambient gamma dose rate averaged over the measurement period in microsieverts per hour (µSv/h). This is the total dose rate including both cosmic and terrestrial components. Null if the station did not report a valid measurement for this interval. |
| `value_cosmic` | *double* (optional) | uSv/h (µSv/h) | `True` | Cosmic radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Estimated from the station's altitude using a standard model. Null when the BfS system has not yet computed the decomposition for this measurement. |
| `value_terrestrial` | *double* (optional) | uSv/h (µSv/h) | `True` | Terrestrial radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Computed as gross value minus cosmic component. Varies with local geology (granite, basalt, sediment). Null when the cosmic component is not available. |
| `validated` | *int32* | - | `True` | Data validation flag. 1 = the measurement has been validated by BfS quality control. 0 = the measurement is preliminary or unvalidated. |
| `nuclide` | *string* | - | `True` | Nuclide identifier describing the type of radiation measured. For standard ODL probes this is always 'Gamma-ODL-Brutto' (gross gamma ambient dose rate). |
