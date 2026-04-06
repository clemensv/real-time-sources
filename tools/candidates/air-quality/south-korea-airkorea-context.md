# South Korea AirKorea — National Air Quality (Update Context)

**Country/Region**: South Korea
**Publisher**: Korea Environment Corporation (KECO), Ministry of Environment
**API Endpoint**: `https://www.airkorea.or.kr/` and via data.go.kr Open API
**Documentation**: https://www.data.go.kr/
**Protocol**: REST (XML/JSON)
**Auth**: API Key (free registration at data.go.kr)
**Data Format**: XML or JSON
**Update Frequency**: Hourly (from ~600 CAAQMS stations)
**License**: Korea Open Government License (KOGL)

## Regional Context

The existing `south-korea-airkorea.md` candidate covers South Korea's air quality monitoring network. This document provides additional context for the Asian air quality research theme.

### Cross-Border Air Pollution

South Korea's air quality is significantly affected by transboundary pollution:
- **Chinese industrial emissions**: PM2.5 transported from China's industrial belt
- **Mongolian dust storms**: Yellow dust (황사/hwangsa) from Gobi Desert
- **Domestic sources**: Vehicle emissions, power plants, industrial

This makes South Korea's AQ monitoring network a critical piece of the East Asian air quality picture, alongside:
- China NMC (not accessible — Great Firewall)
- Japan soramame (existing candidate)
- India CPCB (new data.gov.in candidate)
- Taiwan MOENV (existing candidate)

### AirKorea Significance

With ~600 continuous monitoring stations, AirKorea is one of the densest air quality networks in Asia. The data is accessible through Korea's open data portal (data.go.kr) with free API key registration.

## Integration Notes

- AirKorea data enriches the Asian AQ corridor: India → Southeast Asia → East Asia
- Transboundary dust monitoring connects to Mongolia and China
- Combined with new India CPCB data.gov.in candidate, creates Asia's most comprehensive AQ coverage
- data.go.kr portal requires Korean phone number for registration (barrier for international users)

## Verdict

Strong existing candidate (see south-korea-airkorea.md). Documented here to connect it to the broader Asian air quality research theme. South Korea's dense monitoring network and open data infrastructure make it one of the best AQ data sources in Asia.
