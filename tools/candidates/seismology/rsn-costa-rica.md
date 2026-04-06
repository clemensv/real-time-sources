# RSN Costa Rica — Red Sismológica Nacional

**Country/Region**: Costa Rica (national)
**Publisher**: Red Sismológica Nacional (RSN), Universidad de Costa Rica + ICE
**API Endpoint**: `https://rsn.ucr.ac.cr/actividad-sismica/ultimos-sismos` (HTML only)
**Documentation**: https://rsn.ucr.ac.cr/
**Protocol**: HTTP (Joomla CMS)
**Auth**: None
**Data Format**: HTML
**Update Frequency**: Near-real-time (event-by-event CMS posts)
**License**: UCR (University of Costa Rica)

## What It Provides

Costa Rica's RSN is a joint operation between the University of Costa Rica (UCR) and the national electric utility (ICE). The country sits at the intersection of the Cocos, Caribbean, and Nazca plates — a geologically extreme location with:

- **Subduction earthquakes** along the Pacific coast
- **Active volcanoes**: Arenal, Poás, Irazú, Rincón de la Vieja, Turrialba
- **Volcanic seismicity**: Tremor and swarm activity near active volcanoes
- Proximity to the **Middle America Trench**

## API Details

The RSN website runs on Joomla CMS and publishes earthquake reports as individual articles:

```
https://rsn.ucr.ac.cr/actividad-sismica/ultimos-sismos
```

Response is HTML with structured article listings:
```
SISMO, 06 de abril del 2026, 8:01 am., Mag: 3,7 Mw, SENTIDO
SISMO, 06 de abril del 2026, 7:44 am., Mag: 3,8 Mw, SENTIDO
SISMO, 03 de abril del 2026, 5:00 am., Mag: 2,7 Mw, SENTIDO
...
```

Each article title contains: date, time, magnitude (Mw), and whether it was felt ("SENTIDO"). Individual article pages contain detailed information.

No JSON API, RSS feed, or structured data endpoint was found.

### Related: OVSICORI

OVSICORI (Observatorio Vulcanológico y Sismológico de Costa Rica) at Universidad Nacional is a separate monitoring network. Endpoints tested:
```
GET https://www.ovsicori.una.ac.cr/ → Various 404s
GET https://api.ovsicori.una.ac.cr/ → Connection failed
```

## Freshness Assessment

The website is actively updated — the most recent earthquake on 2026-04-06 was posted the same day. RSN appears to post felt events within hours. However, only HTML scraping would enable data extraction.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Same-day reporting for felt events |
| Openness | 1 | HTML only, no API; scraping Joomla articles |
| Stability | 2 | UCR institution, active website |
| Structure | 1 | Article titles contain structured data but need parsing |
| Identifiers | 1 | No standard event IDs |
| Additive Value | 2 | Ring of Fire + active volcanoes, but covered by USGS for M4+ |
| **Total** | **9/18** | |

## Verdict

⚠️ **Maybe** — If HTML scraping is acceptable, the article title format is parseable (date, magnitude, felt status). Costa Rica's seismicity and volcanic activity are scientifically significant. However, the Joomla CMS format is fragile and could change without notice. Larger events are available via USGS/EMSC.
