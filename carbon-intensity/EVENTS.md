# Carbon Intensity UK Bridge Events

This document describes the events emitted by the Carbon Intensity UK Bridge.

- [uk.org.carbonintensity](#message-group-ukorgcarbonintensity)
  - [uk.org.carbonintensity.Intensity](#message-ukorgcarbonintensityintensity)
  - [uk.org.carbonintensity.GenerationMix](#message-ukorgcarbonintensitygenerationmix)
- [uk.org.carbonintensity.Regional](#message-group-ukorgcarbonintensityregional)
  - [uk.org.carbonintensity.RegionalIntensity](#message-ukorgcarbonintensityregionalintensity)

---

## Message Group: uk.org.carbonintensity

---

### Message: uk.org.carbonintensity.Intensity

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `uk.org.carbonintensity.Intensity` |
| `source` | CloudEvent source | `string` | `True` | `https://api.carbonintensity.org.uk` |
| `subject` | Settlement period start | `uritemplate` | `True` | `{period_from}` |

#### Schema: Intensity

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `period_from` | *datetime* | — | ISO 8601 UTC timestamp marking the start of the half-hour settlement period |
| `period_to` | *datetime* | — | ISO 8601 UTC timestamp marking the end of the half-hour settlement period |
| `forecast` | *int32 (nullable)* | gCO2/kWh | Forecast carbon intensity for this settlement period |
| `actual` | *int32 (nullable)* | gCO2/kWh | Actual (metered) carbon intensity. Null when the period has not yet completed |
| `index` | *string (nullable)* | — | Qualitative index band: very low, low, moderate, high, or very high |

---

### Message: uk.org.carbonintensity.GenerationMix

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `uk.org.carbonintensity.GenerationMix` |
| `source` | CloudEvent source | `string` | `True` | `https://api.carbonintensity.org.uk` |
| `subject` | Settlement period start | `uritemplate` | `True` | `{period_from}` |

#### Schema: GenerationMix

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `period_from` | *datetime* | — | ISO 8601 UTC timestamp marking the start of the half-hour settlement period |
| `period_to` | *datetime* | — | ISO 8601 UTC timestamp marking the end of the half-hour settlement period |
| `biomass_pct` | *double (nullable)* | % | Percentage from biomass |
| `coal_pct` | *double (nullable)* | % | Percentage from coal |
| `gas_pct` | *double (nullable)* | % | Percentage from natural gas |
| `hydro_pct` | *double (nullable)* | % | Percentage from hydroelectric |
| `imports_pct` | *double (nullable)* | % | Percentage from interconnector imports |
| `nuclear_pct` | *double (nullable)* | % | Percentage from nuclear |
| `oil_pct` | *double (nullable)* | % | Percentage from oil |
| `other_pct` | *double (nullable)* | % | Percentage from other sources |
| `solar_pct` | *double (nullable)* | % | Percentage from solar |
| `wind_pct` | *double (nullable)* | % | Percentage from wind |

---

## Message Group: uk.org.carbonintensity.Regional

---

### Message: uk.org.carbonintensity.RegionalIntensity

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `uk.org.carbonintensity.RegionalIntensity` |
| `source` | CloudEvent source | `string` | `True` | `https://api.carbonintensity.org.uk` |
| `subject` | DNO region identifier | `uritemplate` | `True` | `{region_id}` |

#### Schema: RegionalIntensity

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `region_id` | *int32* | — | Numeric DNO region identifier (1–17) |
| `dnoregion` | *string* | — | Full DNO region name |
| `shortname` | *string* | — | Short display name for the region |
| `period_from` | *datetime* | — | ISO 8601 UTC timestamp of the settlement period start |
| `period_to` | *datetime* | — | ISO 8601 UTC timestamp of the settlement period end |
| `forecast` | *int32 (nullable)* | gCO2/kWh | Forecast carbon intensity for this region |
| `index` | *string (nullable)* | — | Qualitative index band |
| `biomass_pct` | *double (nullable)* | % | Percentage from biomass |
| `coal_pct` | *double (nullable)* | % | Percentage from coal |
| `gas_pct` | *double (nullable)* | % | Percentage from natural gas |
| `hydro_pct` | *double (nullable)* | % | Percentage from hydroelectric |
| `imports_pct` | *double (nullable)* | % | Percentage from interconnector imports |
| `nuclear_pct` | *double (nullable)* | % | Percentage from nuclear |
| `oil_pct` | *double (nullable)* | % | Percentage from oil |
| `other_pct` | *double (nullable)* | % | Percentage from other sources |
| `solar_pct` | *double (nullable)* | % | Percentage from solar |
| `wind_pct` | *double (nullable)* | % | Percentage from wind |
