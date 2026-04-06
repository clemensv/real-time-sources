# Capital Bikeshare Washington DC

**Country/Region**: United States — Washington DC Metro Area
**Publisher**: Lyft (operator), DDOT (sponsor)
**API Endpoint**: `https://gbfs.capitalbikeshare.com/gbfs/gbfs.json`
**Documentation**: https://capitalbikeshare.com/system-data
**Protocol**: GBFS 1.1
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 60-second TTL
**License**: Capital Bikeshare data license

## What It Provides

Real-time station availability for the DC Metro area's bikeshare system. Capital Bikeshare operates ~700 stations across Washington DC, Arlington, Alexandria, Fairfax, and Montgomery County with approximately 5,000 bikes including e-bikes. One of the oldest and most established bikeshare systems in the US (since 2010).

## API Details

The auto-discovery URL redirects to Lyft's GBFS infrastructure:

- `gbfs.json` → `https://gbfs.lyft.com/gbfs/1.1/dca-cabi/gbfs.json`
- `station_information.json` — station metadata
- `station_status.json` — real-time availability
- `free_bike_status.json` — dockless e-bikes
- `system_information.json` — system_id: `lyft_cabi`, start_date: 2010-09-20

Same Lyft GBFS infrastructure as Citi Bike and Bay Wheels.

## Freshness Assessment

TTL is 60 seconds. Lyft GBFS infrastructure delivers consistent near real-time updates. Identical freshness profile to other Lyft systems.

## Entity Model

- **Station**: ~700 stations with UUID-based IDs
- **Availability**: Standard bikes + e-bikes, docks
- **Regions**: DC, Arlington, Alexandria, Fairfax, Montgomery County

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 60s TTL |
| Openness | 3 | No auth |
| Stability | 3 | Lyft infrastructure |
| Structure | 3 | Standard GBFS 1.1 |
| Identifiers | 3 | UUID station IDs |
| Additive Value | 1 | Covered by generic GBFS bridge |
| **Total** | **16/18** | |

## Notes

- Covered by the MobilityData GBFS catalog. No standalone bridge needed.
- Capital Bikeshare's long history (since 2010) means stable station IDs and well-established infrastructure.
- Multi-jurisdictional coverage (DC + Virginia + Maryland) makes it interesting for cross-boundary analysis.
