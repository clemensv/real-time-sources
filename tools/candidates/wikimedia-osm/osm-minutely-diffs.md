# OpenStreetMap Minutely Diffs

**Country/Region**: Global
**Publisher**: OpenStreetMap Foundation
**API Endpoint**: `https://planet.openstreetmap.org/replication/minute/`
**Documentation**: https://wiki.openstreetmap.org/wiki/Planet.osm/diffs
**Protocol**: HTTP file download (sequential numbered files)
**Auth**: None
**Data Format**: OsmChange XML (gzip-compressed `.osc.gz`)
**Update Frequency**: Every 60 seconds
**License**: ODbL 1.0 (Open Data Commons Open Database License)

## What It Provides

OpenStreetMap publishes a continuous replication feed of all changes to the global map database. Every minute, a new diff file is generated containing all node, way, and relation modifications made in that interval. These diffs capture the full lifecycle of geographic features — creates, modifies, and deletes — with complete geometry (lat/lon for nodes) and tag data.

The state file at `state.txt` contains the current sequence number and timestamp. As of probing, `sequenceNumber=7058774` with timestamp `2026-04-06T10:24:46Z`, confirming active minute-by-minute replication.

## API Details

- **State file**: `https://planet.openstreetmap.org/replication/minute/state.txt` — contains `sequenceNumber`, `timestamp`
- **Diff files**: Numbered by sequence in directory structure: `/replication/minute/NNN/NNN/NNN.osc.gz` (e.g., sequence 7058774 → `/007/058/774.osc.gz`)
- **Replication levels**: minute, hour, day available
- **File format**: OsmChange XML wrapped in gzip — contains `<create>`, `<modify>`, `<delete>` sections with `<node>`, `<way>`, `<relation>` elements
- **Processing tools**: `osmosis`, `osm2pgsql` (with `--slim --append`), `pyosmium`
- **Element attributes**: `id`, `version`, `timestamp`, `uid`, `user`, `changeset`, `lat`/`lon` (nodes), `nd ref` (ways), `member` (relations), `tag k/v` pairs
- **No authentication required**
- **Mirroring**: Several mirrors available (e.g., `download.geofabrik.de`)

## Freshness Assessment

Diffs are generated every 60 seconds, providing near-real-time map updates. The actual latency is typically 60-90 seconds from edit to availability in the diff. This is the canonical way to keep an OSM mirror in sync. The state file can be polled to detect new diffs.

## Entity Model

- **Node**: Point feature with lat/lon, identified by `id` (int64), `version` (incrementing)
- **Way**: Ordered list of node references, forming lines/polygons
- **Relation**: Grouping of nodes/ways/relations with roles
- **Changeset**: `changeset` ID groups related edits by a user in a session
- **Tags**: Key-value pairs on any element (e.g., `highway=residential`, `name=Main Street`)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 60-second replication cycle, continuous |
| Openness | 3 | No auth, publicly mirrored |
| Stability | 3 | Core OSM infrastructure, running since 2009 |
| Structure | 2 | XML format requires parsing; well-defined but verbose |
| Identifiers | 3 | Globally unique element IDs with version numbers |
| Additive Value | 3 | The only real-time global map change feed |
| **Total** | **17/18** | |

## Notes

- Not a REST API — it's a file-based replication system. You poll `state.txt`, fetch the diff file, apply it.
- Processing the full minutely diff stream requires meaningful compute — each file can contain thousands of changes.
- The `pyosmium` library provides efficient Python bindings for processing diffs.
- Augmented diff streams (Augmented Diffs / Overpass) can provide richer context (full geometry for ways, not just node refs).
- OSMCha and other tools build on top of this replication stream.
