# Safecast

**Country/Region**: Global (strongest in Japan, North America)
**Publisher**: Safecast (501(c)(3) nonprofit)
**API Endpoint**: `https://api.safecast.org/measurements.json`
**Documentation**: https://api.safecast.org, https://blog.safecast.org/
**Protocol**: REST
**Auth**: None (read access); API key for write
**Data Format**: JSON
**Update Frequency**: Varies (crowd-sourced; data arrives as volunteers submit)
**License**: CC0 1.0 (Public Domain)

## What It Provides

Safecast is a citizen-science radiation monitoring network born from the 2011 Fukushima disaster. Volunteers carry portable Geiger counters (bGeigie Nano) and upload geolocated radiation measurements. The dataset contains over 180 million measurements worldwide, with the densest coverage in Japan. Values are in CPM (counts per minute) and µSv/h (microsieverts per hour).

Live probe confirmed working API: measurements returned with `value` in CPM, `unit: "cpm"`, geographic coordinates, and timestamps. Data showed readings from the San Francisco area from user-contributed drives.

## API Details

- **List measurements**: `GET /measurements.json?latitude={lat}&longitude={lon}&distance={meters}&limit={n}`
- **Parameters**: `latitude`, `longitude`, `distance` (radius in meters), `since` (ISO timestamp), `until`, `captured_after`, `captured_before`, `limit` (default 25, max 100), `order` (asc/desc)
- **Per-device**: Filter by `device_id` or `user_id`
- **Response fields**: `id`, `user_id`, `value` (CPM), `unit`, `latitude`, `longitude`, `captured_at`, `height`, `device_id`, `devicetype_id`, `sensor_id`, `station_id`, `measurement_import_id`
- **Static map tiles**: Pre-rendered radiation map tiles available
- **No authentication for read access**

## Freshness Assessment

Freshness depends entirely on volunteer activity. Bulk uploads from bGeigie drives may arrive days or weeks after capture. Fixed stations (Pointcast) report more frequently. This is not a real-time stream but a crowd-sourced archive with ongoing contributions. The most recent data in any given area may be hours to months old.

## Entity Model

- **Measurement**: `id` (integer), value in CPM, geographic point, timestamp
- **User**: `user_id` — the volunteer who submitted the data
- **Device**: `device_id` — specific Geiger counter unit
- **Import**: `measurement_import_id` — batch upload identifier (bGeigie drive logs)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Crowd-sourced; data arrives sporadically |
| Openness | 3 | CC0 license, no auth for reads |
| Stability | 2 | Nonprofit-run, has been operating since 2011 |
| Structure | 2 | Simple JSON but flat structure, no nested relationships |
| Identifiers | 2 | Integer IDs, no formal URN scheme |
| Additive Value | 3 | Unique citizen radiation dataset; no other source like it |
| **Total** | **13/18** | |

## Notes

- Safecast's value is unique — there is no comparable open citizen radiation monitoring network.
- The data skews heavily toward Japan (Fukushima legacy) but has growing global coverage.
- Fixed Pointcast sensors provide more regular data than mobile bGeigie units.
- The API is simple but lacks streaming or webhook capabilities.
- CC0 licensing makes this maximally reusable.
- Data quality relies on calibrated hardware (bGeigie Nano) but field conditions vary.
