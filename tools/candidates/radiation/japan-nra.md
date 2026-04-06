# Japan NRA Radiation Monitoring (RAMDAS)

**Country/Region**: Japan
**Publisher**: Nuclear Regulation Authority (NRA / 原子力規制委員会)
**API Endpoint**: `https://radioactivity.nra.go.jp/en/` (RAMDAS portal)
**Documentation**: https://radioactivity.nra.go.jp/en/
**Protocol**: Web portal with data downloads (no confirmed public REST API)
**Auth**: None (public portal)
**Data Format**: HTML, CSV downloads
**Update Frequency**: Near-real-time (10-minute monitoring post data)
**License**: Government open data (Japanese government)

## What It Provides

Japan operates one of the world's most extensive radiation monitoring networks, established and massively expanded after the 2011 Fukushima Daiichi nuclear disaster. The NRA's RAMDAS (Radiation Monitoring Data Sharing) system provides:

- **Monitoring Post data** — ~4,700 fixed gamma dose rate monitoring posts across Japan, with 10-minute measurement intervals
- **Airborne monitoring** — Aerial radiation surveys
- **Environmental samples** — Soil, water, food, dust monitoring
- **Prefecture-level data** — Each of Japan's 47 prefectures reports radiation levels

The system was designed to provide comprehensive, real-time visibility into radiation levels nationwide, with particular density around the Fukushima exclusion zone and nuclear power plant sites.

## API Details

### RAMDAS Portal

The primary interface is the RAMDAS web application at `https://radioactivity.nra.go.jp/en/`. This is a modern single-page application (React-based) that loads data dynamically. The underlying data API endpoints were not directly accessible during testing — the site appears to load data through internal AJAX calls that may require specific session parameters.

### Known Data Access Patterns

1. **Web portal** — Interactive map and table views of monitoring post data
2. **CSV downloads** — Historical data available as CSV files, organized by date and prefecture
3. **EURDEP contribution** — Japan shares data with EURDEP, so Japanese monitoring post data is accessible via the EURDEP WFS endpoint (see eurdep.md)

### Typical CSV URL Pattern (historical)

```
https://radioactivity.nra.go.jp/en/contents/14000/{content_id}/24/{date_code}_E.csv
```

Note: The exact URL patterns change and specific content IDs need to be discovered through the portal navigation.

## Freshness Assessment

The RAMDAS portal is live as of 2026-04-06. The web application loads (confirmed by HTML response) but actual data endpoints behind the SPA were not directly probeable. Japan's monitoring post data is known to update every 10 minutes — among the fastest refresh rates in the world for radiation monitoring.

Direct API access attempts returned 404s, suggesting the data API is tightly coupled to the web frontend and not designed as a public REST API.

## Entity Model

- **Monitoring Post** — Fixed sensor location with prefecture, municipality, coordinates, and altitude. Over 4,700 posts nationwide.
- **Measurement** — 10-minute gamma dose rate in µSv/h or µGy/h. Includes timestamp, monitoring post ID, and quality flags.
- **Prefecture** — Administrative region containing multiple monitoring posts. Japan has 47 prefectures.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | 10-minute updates — among the fastest in the world |
| Openness | 1 | Public portal but no documented public API. Data locked behind SPA. |
| Stability | 3 | Government infrastructure, critical post-Fukushima system |
| Structure | 1 | No REST API confirmed. CSV downloads exist but URL patterns unstable. |
| Identifiers | 2 | Monitoring post IDs exist within the system |
| Additive Value | 3 | ~4,700 posts, 10-min resolution, critical Fukushima region coverage |
| **Total** | **13/18** | |

## Notes

- Japan's data is among the most valuable radiation monitoring data in the world due to the Fukushima context, but it's frustratingly difficult to access programmatically.
- The best route for accessing Japanese radiation data may be through EURDEP, where Japan contributes monitoring post data.
- The RAMDAS portal underwent a major redesign (modern SPA), which likely broke any previously reverse-engineered API endpoints.
- An alternative data source is **Safecast**, which has extensive citizen-collected radiation data across Japan.
- Some prefectural governments also publish radiation data on their own portals with varying API accessibility.
- The NRA also publishes PDF reports and press releases with radiation data summaries.
- Reverse-engineering the RAMDAS SPA's AJAX endpoints is technically possible but fragile and not recommended for production use.
