# PTWC/NTWC Tsunami Bulletins Bridge Events

MQTT/5.0 transport variant for tsunami.gov PTWC/NTWC tsunami bulletins. Non-retained QoS-1 bulletin events route by basin, tsunami bulletin level, and bulletin id under alerts/intl/ptwc/ptwc-tsunami/... Basin is derived from the NOAA feed (PHEB=pacific, PAAQ=alaska); ptwc_level is the native bulletin category normalized to lowercase.

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `PTWC.Bulletins.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`PTWC.Bulletins`](#messagegroup-ptwcbulletins) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `ptwc-tsunami` |
| Kafka key | `{bulletin_id}` |
| Deployed | False |

### Endpoint `PTWC.Bulletins.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`PTWC.Bulletins.mqtt`](#messagegroup-ptwcbulletinsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `PTWC.Bulletins`
<a id="messagegroup-ptwcbulletins"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `PTWC.Bulletins.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `PTWC.TsunamiBulletin`
<a id="message-ptwctsunamibulletin"></a>

A tsunami bulletin from the US National Tsunami Warning Center (NTWC) or the Pacific Tsunami Warning Center (PTWC). Bulletins indicate seismic events and their tsunami threat assessment, parsed from the NOAA Atom feeds at tsunami.gov.

| Field | Value |
| --- | --- |
| Name | TsunamiBulletin |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/PTWC.jstruct/schemas/PTWC.TsunamiBulletin`](#schema-ptwctsunamibulletin) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `PTWC.TsunamiBulletin` |
| `source` |  | `string` | `False` | `https://www.tsunami.gov` |
| `subject` |  | `uritemplate` | `False` | `{bulletin_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `PTWC.Bulletins.Kafka` | `KAFKA` | topic `ptwc-tsunami`; key `{bulletin_id}` |

### Messagegroup `PTWC.Bulletins.mqtt`
<a id="messagegroup-ptwcbulletinsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for tsunami.gov PTWC/NTWC tsunami bulletins. Non-retained QoS-1 bulletin events route by basin, tsunami bulletin level, and bulletin id under alerts/intl/ptwc/ptwc-tsunami/... Basin is derived from the NOAA feed (PHEB=pacific, PAAQ=alaska); ptwc_level is the native bulletin category normalized to lowercase. |
| Transport bindings | `PTWC.Bulletins.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `PTWC.Bulletins.mqtt.TsunamiBulletin`
<a id="message-ptwcbulletinsmqtttsunamibulletin"></a>

A tsunami bulletin from the US National Tsunami Warning Center (NTWC) or the Pacific Tsunami Warning Center (PTWC). Bulletins indicate seismic events and their tsunami threat assessment, parsed from the NOAA Atom feeds at tsunami.gov.

| Field | Value |
| --- | --- |
| Name | TsunamiBulletin |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/PTWC.jstruct/schemas/PTWC.TsunamiBulletin`](#schema-ptwctsunamibulletin) |
| Base message chain | `/messagegroups/PTWC.Bulletins/messages/PTWC.TsunamiBulletin` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `PTWC.TsunamiBulletin` |
| `source` |  | `string` | `False` | `https://www.tsunami.gov` |
| `subject` |  | `uritemplate` | `False` | `{bulletin_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `PTWC.Bulletins.Mqtt` | `MQTT/5.0` | topic `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `PTWC.jstruct`
<a id="schemagroup-ptwcjstruct"></a>

#### Schema `PTWC.TsunamiBulletin`
<a id="schema-ptwctsunamibulletin"></a>

| Field | Value |
| --- | --- |
| Name | TsunamiBulletin |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | A tsunami bulletin from the US National Tsunami Warning Center (NTWC) or the Pacific Tsunami Warning Center (PTWC). Contains seismic event details and tsunami threat assessment parsed from NOAA Atom feeds. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.tsunami.gov/schemas/PTWC/TsunamiBulletin` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TsunamiBulletin`
<a id="schema-node-tsunamibulletin"></a>

A tsunami bulletin from the US National Tsunami Warning Center (NTWC) or the Pacific Tsunami Warning Center (PTWC). Contains seismic event details and tsunami threat assessment parsed from NOAA Atom feeds.

| Field | Value |
| --- | --- |
| $id | `https://www.tsunami.gov/schemas/PTWC/TsunamiBulletin` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `bulletin_id` | `string` | `True` | The unique bulletin identifier as a URN UUID from the Atom entry (e.g., 'urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9'). | - | - | - |
| `feed` | enum `['PAAQ', 'PHEB']` | `True` | The feed this bulletin was obtained from. | - | - | - |
| `center` | `string` | `False` | The issuing tsunami warning center name (e.g., 'NWS National Tsunami Warning Center Palmer AK', 'NWS PACIFIC TSUNAMI WARNING CENTER HONOLULU HI'). | - | - | - |
| `title` | `string` | `True` | The title of the bulletin, typically the location of the seismic event (e.g., '60 miles SW of Buldir I., Alaska'). | - | - | - |
| `updated` | `datetime` | `True` | The date and time when the bulletin was last updated, in ISO-8601 format. | - | - | - |
| `latitude` | `double` | `False` | The latitude of the seismic event epicenter in decimal degrees. | - | - | - |
| `longitude` | `double` | `False` | The longitude of the seismic event epicenter in decimal degrees. | - | - | - |
| `category` | enum `['Warning', 'Advisory', 'Watch', 'Information']` | `False` | Native tsunami bulletin category from the feed summary (Warning, Advisory, Watch, or Information). ptwc_level carries the lowercase topic-routing form. | - | - | - |
| `magnitude` | `string` | `False` | The preliminary earthquake magnitude and type (e.g., '5.2(mb)', '7.1(Mw)'). | - | - | - |
| `affected_region` | `string` | `False` | The affected region description from the bulletin summary. | - | - | - |
| `note` | `string` | `False` | Additional notes from the bulletin (e.g., 'There is NO tsunami danger from this earthquake.'). | - | - | - |
| `bulletin_url` | `string` | `False` | URL to the full text bulletin on tsunami.gov. | - | - | - |
| `cap_url` | `string` | `False` | URL to the CAP XML document for this bulletin. | - | - | - |
| `basin` | enum `['pacific', 'alaska', 'unknown']` | `True` | Basin or warning-area slug derived from the NOAA tsunami.gov feed (pacific for PHEB, alaska for PAAQ, or unknown). Matches the {basin} MQTT topic axis. | - | - | - |
| `ptwc_level` | enum `['warning', 'advisory', 'watch', 'information', 'unknown']` | `True` | Native tsunami bulletin category normalized to lowercase for MQTT routing. Matches the {ptwc_level} MQTT topic axis. | - | - | - |
