# ENTSO-E Transparency Platform Bridge Events

CloudEvents emitted by the ENTSO-E Transparency Platform feeder across Kafka, MQTT/UNS, and AMQP 1.0 transports.

- [eu.entsoe.transparency.ByDomain](#message-group-euentsoetransparencybydomain)
  - [eu.entsoe.transparency.DayAheadPrices](#message-euentsoetransparencydayaheadprices)
  - [eu.entsoe.transparency.ActualTotalLoad](#message-euentsoetransparencyactualtotalload)
  - [eu.entsoe.transparency.LoadForecastMargin](#message-euentsoetransparencyloadforecastmargin)
  - [eu.entsoe.transparency.GenerationForecast](#message-euentsoetransparencygenerationforecast)
  - [eu.entsoe.transparency.ReservoirFillingInformation](#message-euentsoetransparencyreservoirfillinginformation)
  - [eu.entsoe.transparency.ActualGeneration](#message-euentsoetransparencyactualgeneration)
- [eu.entsoe.transparency.ByDomainPsrType](#message-group-euentsoetransparencybydomainpsrtype)
  - [eu.entsoe.transparency.ActualGenerationPerType](#message-euentsoetransparencyactualgenerationpertype)
  - [eu.entsoe.transparency.WindSolarForecast](#message-euentsoetransparencywindsolarforecast)
  - [eu.entsoe.transparency.WindSolarGeneration](#message-euentsoetransparencywindsolargeneration)
  - [eu.entsoe.transparency.InstalledGenerationCapacityPerType](#message-euentsoetransparencyinstalledgenerationcapacitypertype)
- [eu.entsoe.transparency.CrossBorder](#message-group-euentsoetransparencycrossborder)
  - [eu.entsoe.transparency.CrossBorderPhysicalFlows](#message-euentsoetransparencycrossborderphysicalflows)
- [eu.entsoe.transparency.ByDomain.mqtt](#message-group-euentsoetransparencybydomainmqtt)
  - [eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices](#message-euentsoetransparencybydomainmqttdayaheadprices)
  - [eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad](#message-euentsoetransparencybydomainmqttactualtotalload)
  - [eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin](#message-euentsoetransparencybydomainmqttloadforecastmargin)
  - [eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast](#message-euentsoetransparencybydomainmqttgenerationforecast)
  - [eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation](#message-euentsoetransparencybydomainmqttreservoirfillinginformation)
  - [eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration](#message-euentsoetransparencybydomainmqttactualgeneration)
- [eu.entsoe.transparency.ByDomainPsrType.mqtt](#message-group-euentsoetransparencybydomainpsrtypemqtt)
  - [eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType](#message-euentsoetransparencybydomainpsrtypemqttactualgenerationpertype)
  - [eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast](#message-euentsoetransparencybydomainpsrtypemqttwindsolarforecast)
  - [eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration](#message-euentsoetransparencybydomainpsrtypemqttwindsolargeneration)
  - [eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType](#message-euentsoetransparencybydomainpsrtypemqttinstalledgenerationcapacitypertype)
- [eu.entsoe.transparency.CrossBorder.mqtt](#message-group-euentsoetransparencycrossbordermqtt)
  - [eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows](#message-euentsoetransparencycrossbordermqttcrossborderphysicalflows)
- [eu.entsoe.transparency.ByDomain.amqp](#message-group-euentsoetransparencybydomainamqp)
  - [eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices](#message-euentsoetransparencybydomainamqpdayaheadprices)
  - [eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad](#message-euentsoetransparencybydomainamqpactualtotalload)
  - [eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin](#message-euentsoetransparencybydomainamqploadforecastmargin)
  - [eu.entsoe.transparency.ByDomain.amqp.GenerationForecast](#message-euentsoetransparencybydomainamqpgenerationforecast)
  - [eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation](#message-euentsoetransparencybydomainamqpreservoirfillinginformation)
  - [eu.entsoe.transparency.ByDomain.amqp.ActualGeneration](#message-euentsoetransparencybydomainamqpactualgeneration)
- [eu.entsoe.transparency.ByDomainPsrType.amqp](#message-group-euentsoetransparencybydomainpsrtypeamqp)
  - [eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType](#message-euentsoetransparencybydomainpsrtypeamqpactualgenerationpertype)
  - [eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast](#message-euentsoetransparencybydomainpsrtypeamqpwindsolarforecast)
  - [eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration](#message-euentsoetransparencybydomainpsrtypeamqpwindsolargeneration)
  - [eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType](#message-euentsoetransparencybydomainpsrtypeamqpinstalledgenerationcapacitypertype)
- [eu.entsoe.transparency.CrossBorder.amqp](#message-group-euentsoetransparencycrossborderamqp)
  - [eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows](#message-euentsoetransparencycrossborderamqpcrossborderphysicalflows)

---

## Message Group: eu.entsoe.transparency.ByDomain
---
### Message: eu.entsoe.transparency.DayAheadPrices
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.DayAheadPrices` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: DayAheadPrices
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `price` | *double* | - | `True` | Day-ahead price |
| `currency` | *string* | - | `True` | Currency code (EUR) |
| `unitName` | *string* | - | `True` | Price unit (MWH) |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A44) |
---
### Message: eu.entsoe.transparency.ActualTotalLoad
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ActualTotalLoad` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: ActualTotalLoad
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `quantity` | *double* | - | `True` | Total load in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `outDomain` | *string* | - | `False` | EIC code of the out domain, if applicable |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A65) |
---
### Message: eu.entsoe.transparency.LoadForecastMargin
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.LoadForecastMargin` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: LoadForecastMargin
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `quantity` | *double* | - | `True` | Forecast margin in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A70) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
---
### Message: eu.entsoe.transparency.GenerationForecast
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.GenerationForecast` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: GenerationForecast
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `quantity` | *double* | - | `True` | Forecast total generation in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A71) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
---
### Message: eu.entsoe.transparency.ReservoirFillingInformation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ReservoirFillingInformation` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: ReservoirFillingInformation
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `quantity` | *double* | - | `True` | Stored energy in MWh |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A72) |
| `unitName` | *string* | - | `True` | Unit of measurement |
---
### Message: eu.entsoe.transparency.ActualGeneration
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ActualGeneration` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: ActualGeneration
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `quantity` | *double* | - | `True` | Total actual generation in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A73) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
## Message Group: eu.entsoe.transparency.ByDomainPsrType
---
### Message: eu.entsoe.transparency.ActualGenerationPerType
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.ActualGenerationPerType` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: ActualGenerationPerType
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `psrType` | *string* | - | `True` | Production type code (B01=Biomass, B02=Lignite, ...) |
| `quantity` | *double* | - | `True` | Generated power in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration (PT15M, PT60M) |
| `businessType` | *string* | - | `True` | Business type code |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A75) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
---
### Message: eu.entsoe.transparency.WindSolarForecast
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.WindSolarForecast` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: WindSolarForecast
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `psrType` | *string* | - | `True` | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) |
| `quantity` | *double* | - | `True` | Forecast power in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration (PT15M, PT60M) |
| `businessType` | *string* | - | `True` | Business type code |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A69) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
---
### Message: eu.entsoe.transparency.WindSolarGeneration
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.WindSolarGeneration` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: WindSolarGeneration
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `psrType` | *string* | - | `True` | Production type code (B16=Solar, B18=Wind Offshore, B19=Wind Onshore) |
| `quantity` | *double* | - | `True` | Actual wind/solar generation in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `businessType` | *string* | - | `True` | Business type code |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A74) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
---
### Message: eu.entsoe.transparency.InstalledGenerationCapacityPerType
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.InstalledGenerationCapacityPerType` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{psrType}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: InstalledGenerationCapacityPerType
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the bidding zone |
| `psrType` | *string* | - | `True` | Production type code (B01=Biomass, B02=Lignite, ...) |
| `quantity` | *double* | - | `True` | Installed capacity in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `businessType` | *string* | - | `True` | Business type code |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A68) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
## Message Group: eu.entsoe.transparency.CrossBorder
---
### Message: eu.entsoe.transparency.CrossBorderPhysicalFlows
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `eu.entsoe.transparency.CrossBorderPhysicalFlows` |
| `source` |  | `` | `False` | `https://transparency.entsoe.eu/api` |
| `subject` |  | `uritemplate` | `False` | `{inDomain}/{outDomain}` |
| `datacontenttype` |  | `` | `False` | `application/json` |

#### Schema:
##### Object: CrossBorderPhysicalFlows
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `inDomain` | *string* | - | `True` | EIC code of the importing bidding zone |
| `outDomain` | *string* | - | `True` | EIC code of the exporting bidding zone |
| `quantity` | *double* | - | `True` | Physical flow in MW |
| `resolution` | *string* | - | `True` | ISO 8601 duration |
| `documentType` | *string* | - | `True` | ENTSO-E document type code (A11) |
| `unitName` | *string* | - | `True` | Unit of measurement (MAW) |
## Message Group: eu.entsoe.transparency.ByDomain.mqtt
---
### Message: eu.entsoe.transparency.ByDomain.mqtt.DayAheadPrices
*MQTT/UNS binary CloudEvents variant for DayAheadPrices. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.mqtt.ActualTotalLoad
*MQTT/UNS binary CloudEvents variant for ActualTotalLoad. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.mqtt.LoadForecastMargin
*MQTT/UNS binary CloudEvents variant for LoadForecastMargin. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.mqtt.GenerationForecast
*MQTT/UNS binary CloudEvents variant for GenerationForecast. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.mqtt.ReservoirFillingInformation
*MQTT/UNS binary CloudEvents variant for ReservoirFillingInformation. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.mqtt.ActualGeneration
*MQTT/UNS binary CloudEvents variant for ActualGeneration. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
## Message Group: eu.entsoe.transparency.ByDomainPsrType.mqtt
---
### Message: eu.entsoe.transparency.ByDomainPsrType.mqtt.ActualGenerationPerType
*MQTT/UNS binary CloudEvents variant for ActualGenerationPerType. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarForecast
*MQTT/UNS binary CloudEvents variant for WindSolarForecast. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomainPsrType.mqtt.WindSolarGeneration
*MQTT/UNS binary CloudEvents variant for WindSolarGeneration. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomainPsrType.mqtt.InstalledGenerationCapacityPerType
*MQTT/UNS binary CloudEvents variant for InstalledGenerationCapacityPerType. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
## Message Group: eu.entsoe.transparency.CrossBorder.mqtt
---
### Message: eu.entsoe.transparency.CrossBorder.mqtt.CrossBorderPhysicalFlows
*MQTT/UNS binary CloudEvents variant for CrossBorderPhysicalFlows. ENTSO-E poll cycles emit individual market time-series points; retain is false so a retained slot never misrepresents an old forecast or historical MTU point as current state.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
## Message Group: eu.entsoe.transparency.ByDomain.amqp
---
### Message: eu.entsoe.transparency.ByDomain.amqp.DayAheadPrices
*AMQP 1.0 binary CloudEvents variant for DayAheadPrices, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.amqp.ActualTotalLoad
*AMQP 1.0 binary CloudEvents variant for ActualTotalLoad, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.amqp.LoadForecastMargin
*AMQP 1.0 binary CloudEvents variant for LoadForecastMargin, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.amqp.GenerationForecast
*AMQP 1.0 binary CloudEvents variant for GenerationForecast, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.amqp.ReservoirFillingInformation
*AMQP 1.0 binary CloudEvents variant for ReservoirFillingInformation, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomain.amqp.ActualGeneration
*AMQP 1.0 binary CloudEvents variant for ActualGeneration, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
## Message Group: eu.entsoe.transparency.ByDomainPsrType.amqp
---
### Message: eu.entsoe.transparency.ByDomainPsrType.amqp.ActualGenerationPerType
*AMQP 1.0 binary CloudEvents variant for ActualGenerationPerType, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}/{psrType}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarForecast
*AMQP 1.0 binary CloudEvents variant for WindSolarForecast, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}/{psrType}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomainPsrType.amqp.WindSolarGeneration
*AMQP 1.0 binary CloudEvents variant for WindSolarGeneration, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}/{psrType}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
---
### Message: eu.entsoe.transparency.ByDomainPsrType.amqp.InstalledGenerationCapacityPerType
*AMQP 1.0 binary CloudEvents variant for InstalledGenerationCapacityPerType, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}/{psrType}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
## Message Group: eu.entsoe.transparency.CrossBorder.amqp
---
### Message: eu.entsoe.transparency.CrossBorder.amqp.CrossBorderPhysicalFlows
*AMQP 1.0 binary CloudEvents variant for CrossBorderPhysicalFlows, sent to the `entsoe` AMQP address. The CloudEvent subject and Azure x-opt-partition-key mirror the Kafka key template {inDomain}/{outDomain}.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|

Schema not found.
