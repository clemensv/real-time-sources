# Morocco ONEE / Masen — Renewable Energy Monitoring

- **Country/Region**: Morocco
- **Endpoint**: Unknown (requires investigation)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Unknown
- **Docs**: https://www.masen.ma/ / https://www.one.org.ma/
- **Score**: 5/18

## Overview

Morocco is Africa's renewable energy leader, with ambitious targets and massive
infrastructure:

- **Noor-Ouarzazate Solar Complex**: One of the world's largest concentrated solar
  power plants (580 MW), visible from space
- **Tarfaya Wind Farm**: 300 MW, Africa's largest wind farm
- **Midelt Solar-Wind Complex**: Planned 800 MW hybrid
- **ONEE**: Office National de l'Électricité et de l'Eau Potable — national utility
- **Masen**: Moroccan Agency for Sustainable Energy — manages renewable projects

Morocco generates 40%+ of electricity from renewables (target: 52% by 2030). This
makes it potentially the best source for African renewable energy generation data.

## Endpoint Analysis

**No public API discovered** during research. Both ONEE and Masen have websites but
they are informational portals, not data platforms.

Potential data pathways:
- **ONEE generation data**: Morocco's national utility likely publishes generation
  mix data, possibly through regulatory filings
- **ENTSO-E Mediterranean**: Morocco is connected to Spain via submarine cables and
  may have some data in the ENTSO-E transparency platform
- **Electricity Maps**: Morocco (MA) is a tracked zone in Electricity Maps, suggesting
  some generation data is available
- **Global Energy Monitor**: Project-level data for Moroccan power plants

## Integration Notes

- **Investigation needed**: This is a high-potential but unverified source. Morocco's
  advanced renewable infrastructure suggests data exists but may require institutional
  contacts to access.
- **ENTSO-E route**: Morocco's interconnection with Spain means some flow data may
  appear in ENTSO-E transparency platform. Check the Morocco-Spain interconnector.
- **Electricity Maps fallback**: Use Electricity Maps' Morocco zone for modeled
  generation data while investigating direct sources.
- **Regional model**: If Morocco provides an API, it could serve as a template for
  other North African countries (Tunisia, Egypt) with growing renewable capacity.
- **French documentation**: Official Moroccan government data may be in French.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data found |
| Openness | 0 | No API discovered |
| Stability | 2 | Government institutions exist |
| Structure | 0 | No API |
| Identifiers | 1 | Power plant names |
| Richness | 2 | Potential for generation mix, interconnector flows |
