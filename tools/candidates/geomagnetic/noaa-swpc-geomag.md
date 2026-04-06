# NOAA SWPC Geomagnetic Data

**Country/Region**: Global
**Publisher**: NOAA Space Weather Prediction Center (SWPC)
**API Endpoint**: `https://services.swpc.noaa.gov/products/`
**Documentation**: https://www.swpc.noaa.gov/
**Protocol**: REST (static JSON files)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 1-minute to 3-hourly depending on product
**License**: US Government public domain

## What It Provides

NOAA's Space Weather Prediction Center provides a comprehensive suite of space weather data products as static JSON files. The geomagnetic-relevant products include the planetary Kp index, NOAA Space Weather Scales (G/S/R), geospace propagated solar wind, GOES satellite magnetometer data, Dst index (from Kyoto), and alerts/warnings. These products power operational space weather forecasting and are updated continuously.

Live probing confirmed multiple active endpoints:
- Planetary Kp index: 3-hourly values with station counts, showing storm activity (Kp reached 6.67 on 2026-04-03)
- GOES magnetometers: 1-minute cadence He/Hp/Hn field components with arcjet flags
- Solar wind propagation: 1-minute speed/density/temperature/magnetic field data
- NOAA Scales: Current and forecast R/S/G scale levels

## API Details

- **Kp index**: `/products/noaa-planetary-k-index.json` — 3-hourly Kp, a_running, station_count
- **Kp forecast**: `/products/noaa-planetary-k-index-forecast.json` — predicted Kp values
- **NOAA Scales**: `/products/noaa-scales.json` — current R (radio), S (solar radiation), G (geomagnetic) scale levels with probabilities
- **GOES magnetometers**: `/json/goes/primary/magnetometers-1-day.json` — 1-minute He, Hp, Hn, total field components from GOES satellites
- **Solar wind**: `/products/geospace/propagated-solar-wind-1-hour.json` — propagated solar wind speed, density, temperature, magnetic field
- **Alerts**: `/products/alerts.json` — space weather alerts, watches, warnings (~150 KB)
- **Dst index**: `/products/kyoto-dst.json` — Dst (disturbance storm time) index from Kyoto
- **10.7 cm flux**: `/products/10cm-flux-30-day.json` — solar radio flux
- **All products**: Directory listing at `/products/` with timestamps showing continuous updates
- **No authentication, no rate limiting**

## Freshness Assessment

GOES magnetometer data updates every minute. Solar wind data updates every minute. Kp index updates every 3 hours. Alerts are issued in real-time as conditions warrant. NOAA Scales are updated continuously. This is genuine operational space weather data with excellent freshness across the product suite.

## Entity Model

- **Kp Record**: time_tag, Kp value, running a-index, station count
- **GOES Magnetometer**: time_tag, satellite ID, He/Hp/Hn components (nT), total field, arcjet flag
- **Solar Wind**: time_tag, speed (km/s), density (p/cc), temperature (K), Bx/By/Bz/Bt (nT), propagated time
- **NOAA Scale**: Date/time, R/S/G scale levels (0-5) with descriptive text and probabilities
- **Alert**: Issue time, type, serial number, message body

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 1-minute cadence for key products; continuous updates |
| Openness | 3 | No auth; US Gov public domain; no rate limits |
| Stability | 3 | NOAA operational infrastructure; mission-critical |
| Structure | 2 | Clean JSON but heterogeneous schemas across products |
| Identifiers | 2 | Time-based keys; satellite IDs; no URI scheme |
| Additive Value | 3 | Comprehensive space weather data suite; unique operational data |
| **Total** | **16/18** | |

## Notes

- The SWPC products suite is impressively broad — a single base URL provides dozens of real-time space weather data products.
- Products are static JSON files regenerated on schedule — simple to consume, cache-friendly, highly reliable.
- The GOES magnetometer data complements the INTERMAGNET ground observations with space-based measurements.
- The alerts.json file contains the full text of NOAA space weather alerts — useful for event detection and notification.
- NOAA Scales (G1-G5 for geomagnetic storms, S1-S5 for solar radiation, R1-R5 for radio blackouts) are the standard framework used by government agencies and industry.
- Some of these products (GOES satellite data) may overlap with existing bridges in this project — check for duplication.
