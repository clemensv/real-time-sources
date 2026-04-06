# VAAC Volcanic Ash Advisories (Washington VAAC / NOAA)

**Country/Region**: Global (9 VAACs worldwide; Washington VAAC covers Americas)
**Publisher**: NOAA/NESDIS Satellite Analysis Branch (Washington VAAC) and 8 other VAACs
**API Endpoint**: `https://www.ssd.noaa.gov/VAAC/messages.html` (Washington VAAC)
**Documentation**: https://www.ssd.noaa.gov/VAAC/
**Protocol**: HTTP (HTML pages + individual XML/KML files)
**Auth**: None
**Data Format**: XML (SIGMET-like), KML, JPEG, HTML
**Update Frequency**: As needed — every 6 hours during active ash events, more frequently for significant eruptions
**License**: US Government public domain (Washington VAAC); varies by VAAC

## What It Provides

The nine Volcanic Ash Advisory Centers (VAACs) worldwide are responsible for issuing advisories about volcanic ash clouds to the aviation community. The Washington VAAC (operated by NOAA) covers the Americas and issues:

- **Volcanic Ash Advisories (VAA)** — Text/XML advisories with ash cloud location, height, and movement
- **Volcanic Ash Graphics (VAG)** — JPEG images showing ash cloud extent and forecast
- **KML files** — Google Earth-compatible ash cloud polygons
- **Current ash advisory list** — Active volcanoes with recent advisories

The 9 VAACs globally are: Washington, Montreal, Buenos Aires, London, Toulouse, Darwin, Tokyo, Wellington, Anchorage.

## API Details

**Washington VAAC current advisories:**
```
https://www.ssd.noaa.gov/VAAC/messages.html
```
Returns HTML page listing all advisories from the past 24 hours and 15 days.

**Individual advisory XML:**
```
https://www.ssd.noaa.gov/products/atmosphere/vaac/volcanoes/xml_files/FVXX24_20260406_0954.xml
```

**Individual advisory KML:**
```
https://www.ssd.noaa.gov/products/atmosphere/vaac/volcanoes/kml_files/POPOCATEPETL_ASH_202604060954.kml
```

**Advisory graphics (JPEG):**
```
https://www.ssd.noaa.gov/VAAC/ARCH26/GFX/POPO0152.jpg
```

File naming convention: `FVXX{nn}_{date}_{time}.xml` for XML, `{VOLCANO}_ASH_{datetime}.kml` for KML.

## Freshness Assessment

Good for active volcanic events. During eruptions with ash emissions, advisories are updated every 6 hours or more frequently. Between events, the feed is quiet. The Washington VAAC showed recent advisories (within minutes) for multiple volcanoes during testing: Popocatépetl, Fuego, Reventador, Sangay, Santa Maria.

## Entity Model

**Volcanic Ash Advisory:**
- Volcano name and location
- Advisory datetime (UTC)
- Ash cloud observation: location polygon, flight level/altitude, movement direction/speed
- Ash cloud forecast: 6h, 12h, 18h positions
- Advisory text narrative
- Source VAAC identifier
- WMO message header (FVXX series)

**KML data:**
- Ash cloud polygon geometries at observed and forecast times
- Altitude information
- Advisory metadata

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Updated during events (every 6h), quiet between |
| Openness | 3 | Public domain, no auth |
| Stability | 3 | ICAO-mandated operational service |
| Structure | 2 | XML/KML individual files, HTML index page |
| Identifiers | 2 | WMO headers, volcano names (no standard IDs) |
| Additive Value | 3 | Unique aviation-critical ash cloud data |
| **Total** | **15/18** | |

## Notes

- VAAC advisories are operationally critical for aviation — this is the authoritative source for volcanic ash hazards.
- The Washington VAAC provides the most accessible data (US government, public domain). Other VAACs may have different access policies.
- No formal REST API exists — the data must be scraped from HTML index pages and individual XML/KML files.
- The KML files are particularly valuable as they contain georeferenced ash cloud polygons.
- Consider monitoring the HTML index page for new advisories and then fetching individual XML/KML files.
- The data is inherently event-driven and bursty — may need special handling for quiet periods vs eruption sequences.
- Tokyo VAAC (`https://ds.data.jma.go.jp/svd/vaac/data/`) covers the western Pacific, another active region.
