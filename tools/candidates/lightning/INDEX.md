# Lightning Detection — Candidate Data Sources

## Summary

| Source | Region | Protocol | Auth | Freshness | Total | Status |
|--------|--------|----------|------|-----------|-------|--------|
| [Blitzortung.org](blitzortung.md) | Global | WebSocket | None | Real-time (<1s) | **14/18** | ✅ Recommended |
| [DWD Lightning](dwd-lightning.md) | Germany/Europe | File download | None | ~10 min files | **13/18** | ✅ Viable |
| [Vaisala GLD360/NLDN](vaisala-gld360-nldn.md) | Global/USA | Commercial | Commercial license | Real-time | **15/18** | ❌ Dismissed (commercial) |
| [WWLLN](wwlln.md) | Global | Academic | Agreement required | Delayed | **8/18** | ❌ Dismissed (restricted) |

## Recommendations

**Tier 1 — Implement first:**
- **Blitzortung.org** — True real-time WebSocket streaming of global lightning strikes. Community project but remarkably capable. ToS restrict redistribution, so use for internal/non-commercial purposes.

**Tier 2 — High value addition:**
- **DWD Lightning** — Professional-grade European lightning data from the EUCLID network, published as open data. File-based but frequent updates (~10 min). Excellent legal clarity under German open data law.

**Dismissed:**
- **Vaisala GLD360/NLDN** — Gold standard commercial product. No open access.
- **WWLLN** — Academic network requiring data sharing agreements. Low detection efficiency.

## Notes

Lightning detection is a challenging domain for open data. The best data (Vaisala) is commercial. Blitzortung is the standout open alternative with global real-time coverage, though it operates as a community project without SLAs. DWD provides the unique combination of professional-grade data + fully open access, but limited to the European region.
