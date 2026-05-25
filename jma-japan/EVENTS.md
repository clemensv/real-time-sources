# JMA Japan Weather Bulletins Poller Events

**JMA Japan Weather Bulletins Poller** polls the Japan Meteorological Agency (JMA) Atom XML feeds for weather bulletins—forecasts, warnings, advisories, and risk notifications—and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen bulletin IDs to avoid sending duplicates.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `jp.go.jma.WeatherBulletins.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`jp.go.jma.WeatherBulletins`](#messagegroup-jpgojmaweatherbulletins) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `jma-japan` |
| Kafka key | `{bulletin_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `jp.go.jma.WeatherBulletins`
<a id="messagegroup-jpgojmaweatherbulletins"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `jp.go.jma.WeatherBulletins.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `jp.go.jma.WeatherBulletin`
<a id="message-jpgojmaweatherbulletin"></a>

| Field | Value |
| --- | --- |
| Name | WeatherBulletin |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/jp.go.jma.jstruct/schemas/jp.go.jma.WeatherBulletin`](#schema-jpgojmaweatherbulletin) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `jp.go.jma.WeatherBulletin` |
| `source` |  | `string` | `False` | `https://www.data.jma.go.jp` |
| `subject` |  | `uritemplate` | `False` | `{bulletin_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `jp.go.jma.WeatherBulletins.Kafka` | `KAFKA` | topic `jma-japan`; key `{bulletin_id}` |

## Schemagroups

### Schemagroup `jp.go.jma.jstruct`
<a id="schemagroup-jpgojmajstruct"></a>

#### Schema `jp.go.jma.WeatherBulletin`
<a id="schema-jpgojmaweatherbulletin"></a>

| Field | Value |
| --- | --- |
| Name | WeatherBulletin |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.data.jma.go.jp/schemas/jp/go/jma/WeatherBulletin` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherBulletin`
<a id="schema-node-weatherbulletin"></a>

Weather bulletin entry from the JMA XML Atom feed. Covers forecasts, warnings, advisories, and risk notifications published by the Japan Meteorological Agency and its regional observatories.

| Field | Value |
| --- | --- |
| $id | `https://www.data.jma.go.jp/schemas/jp/go/jma/WeatherBulletin` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `bulletin_id` | `string` | `True` | Unique identifier for the bulletin, derived from the Atom entry ID (typically a URL to the full XML document). | - | - | - |
| `title` | `string` | `True` | Title of the weather bulletin in Japanese, e.g. '気象特別警報・警報・注意報' (Special weather warnings/advisories). | - | - | - |
| `author` | `union` | `False` | Issuing authority name in Japanese, e.g. '気象庁' (JMA) or a regional observatory name like '松江地方気象台'. | - | - | - |
| `updated` | `datetime` | `True` | UTC timestamp when the bulletin was last updated. | - | - | - |
| `link` | `union` | `False` | URL to the full XML document for this bulletin on the JMA data server. | - | - | - |
| `content` | `union` | `False` | Brief text summary of the bulletin content in Japanese. | - | - | - |
| `feed_type` | enum `['regular', 'extra']` | `False` | Which JMA Atom feed this bulletin originated from. | - | - | - |
