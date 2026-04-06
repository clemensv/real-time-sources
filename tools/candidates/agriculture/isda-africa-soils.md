# Africa Soil Information Service (AfSIS) / iSDA

- **Country/Region**: Pan-African (continental soil maps at 30m resolution)
- **Endpoint**: `https://api.isda-africa.com/v1/soilproperty?key={KEY}&lat={lat}&lon={lon}&property=ph`
- **Protocol**: REST
- **Auth**: API key (free registration)
- **Format**: JSON
- **Freshness**: Static (soil properties) but updated periodically with new surveys
- **Docs**: https://www.isda-africa.com/isdasoil/developer/
- **Score**: 10/18

## Overview

iSDA (Innovative Solutions for Decision Agriculture) provides the most detailed
digital soil map of Africa — continental coverage at 30m resolution. The dataset
includes 20+ soil properties at two depths (0-20cm and 20-50cm).

For 600+ million African smallholder farmers, soil data is critical for:
- **Fertilizer recommendations**: What nutrients are deficient?
- **Crop suitability**: Which crops grow best where?
- **Carbon monitoring**: Soil organic carbon for climate change mitigation
- **Land degradation**: Tracking soil health over time

## Endpoint Analysis

The iSDA API provides point queries for soil properties:

```
GET https://api.isda-africa.com/v1/soilproperty
  ?key={API_KEY}
  &lat=-1.29
  &lon=36.82
  &property=ph,organic_carbon,nitrogen,sand,clay
  &depth=0-20
```

Available properties:
| Property | Description | Unit |
|----------|-------------|------|
| ph | Soil pH | - |
| organic_carbon | Soil organic carbon | g/kg |
| nitrogen | Total nitrogen | g/kg |
| phosphorus | Extractable phosphorus | ppm |
| potassium | Extractable potassium | ppm |
| sand | Sand content | % |
| clay | Clay content | % |
| silt | Silt content | % |
| cec | Cation exchange capacity | cmol/kg |
| bulk_density | Bulk density | kg/dm³ |
| water_holding_capacity | Available water capacity | mm |
| texture_class | USDA texture classification | class |

## Integration Notes

- **Reference data bridge**: Like the Global Solar Atlas, this provides static
  reference data rather than real-time streams. But as context enrichment for
  agricultural event streams, it's invaluable.
- **API key registration**: Free at https://www.isda-africa.com/isdasoil/developer/
- **Combine with rainfall**: Pair iSDA soil data with CHIRPS rainfall to model
  crop water availability — the foundation of food security monitoring.
- **Carbon monitoring**: Soil organic carbon data supports Africa's carbon credit
  markets and climate commitments.
- **Resolution**: 30m resolution is extraordinary for a continental dataset.
  Individual farm plots can be assessed.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Static soil properties |
| Openness | 2 | Free API key required |
| Stability | 2 | Academic/commercial hybrid |
| Structure | 3 | Clean JSON API |
| Identifiers | 1 | Coordinate-based |
| Richness | 2 | 20+ soil properties at 30m resolution |
