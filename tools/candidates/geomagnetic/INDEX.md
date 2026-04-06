# Geomagnetic Candidates

Real-time and archival geomagnetic field data and activity indices.

| Source | Protocol | Auth | Freshness | Total Score |
|--------|----------|------|-----------|-------------|
| [INTERMAGNET](intermagnet.md) | HAPI (REST) | None | Minutes-Hours | 16/18 |
| [GFZ Kp Index](gfz-kp-index.md) | REST | None | 3-hourly | 16/18 |
| [NOAA SWPC Geomagnetic](noaa-swpc-geomag.md) | REST | None | 1-minute | 16/18 |
| [WDC for Geomagnetism](wdc-geomagnetism.md) | HTTP/forms | None | Hours-Months | 11/18 |

## Summary

Three strong contenders at 16/18 each. NOAA SWPC provides the most accessible and freshest data (1-minute GOES magnetometers, 3-hourly Kp, real-time alerts) — all as static JSON with zero auth. INTERMAGNET's HAPI endpoint is well-structured and provides access to 150+ ground observatories. GFZ's Kp index is the authoritative geomagnetic activity measure under CC BY 4.0. The WDCs are essential archives but lack modern APIs — NOAA mirrors their key products in more accessible formats.
