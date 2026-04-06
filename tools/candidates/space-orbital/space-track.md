# Space-Track.org

**Country/Region**: Global
**Publisher**: 18th Space Defense Squadron (18 SDS), US Space Force
**API Endpoint**: `https://www.space-track.org/basicspacedata/query/`
**Documentation**: https://www.space-track.org/documentation
**Protocol**: REST (session-based authentication)
**Auth**: Free account required (username/password)
**Data Format**: JSON, XML, CSV, TLE, KVN
**Update Frequency**: Multiple times per day (as observations are processed)
**License**: US Government public domain (with usage agreement)

## What It Provides

Space-Track.org is the official public portal for the US Space Surveillance Network's catalog data. It provides TLEs/GP element sets, satellite catalog (SATCAT) entries, launch data, decay/reentry predictions, conjunction data (CDMs), and historical element sets. This is the authoritative source — CelesTrak and other providers ultimately derive their data from Space-Track.

## API Details

- **Authentication**: POST to `/ajaxauth/login` with identity/password, receive session cookie
- **Query syntax**: `/basicspacedata/query/class/{class}/NORAD_CAT_ID/{id}/format/{format}/orderby/EPOCH desc/limit/1`
- **Classes**: `gp` (GP elements), `gp_history` (historical), `satcat` (catalog), `launch_site`, `decay`, `tip` (tracking/impact prediction), `cdm_public` (conjunction data messages)
- **Formats**: `json`, `xml`, `csv`, `tle`, `3le`, `kvn`
- **Predicates**: `NORAD_CAT_ID`, `OBJECT_NAME`, `EPOCH` (with `/>`, `/<` operators), `INTLDES`, `OBJECT_TYPE`
- **Rate limits**: 300 requests per minute (per documentation); 20 simultaneous connections
- **Historical data**: `gp_history` class provides element sets going back to the start of the catalog

## Freshness Assessment

Data is updated multiple times per day as the Space Surveillance Network processes observations. GP elements for active satellites are typically refreshed every few hours. For newly launched objects, initial elements appear within hours of tracking. Conjunction data is updated as events approach.

## Entity Model

- **GP Element Set**: Orbital elements (same fields as CelesTrak JSON) with additional metadata
- **SATCAT Entry**: Object name, international designator, NORAD catalog number, object type, launch date, decay date, RCS (radar cross-section), country
- **Conjunction Data Message (CDM)**: TCA (time of closest approach), miss distance, probability of collision, object pair
- **TIP (Tracking & Impact Prediction)**: Decay/reentry predictions with uncertainty windows

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Updated multiple times/day; not real-time |
| Openness | 1 | Free account required; usage agreement; session auth |
| Stability | 3 | US Space Force operational system |
| Structure | 3 | Rich query API with multiple output formats |
| Identifiers | 3 | NORAD catalog numbers; international designators |
| Additive Value | 2 | Authoritative source; CelesTrak provides easier access for basic data |
| **Total** | **14/18** | |

## Notes

- Space-Track is the authoritative source but CelesTrak is easier for basic TLE access (no auth).
- The conjunction data messages (CDMs) are unique to Space-Track — critical for collision avoidance.
- Historical GP element sets allow orbit reconstruction over time.
- The session-based authentication is cumbersome for automated workflows.
- Rate limits are generous but require careful management for bulk downloads.
- The SATCAT provides metadata not available elsewhere (RCS, object type classification).
