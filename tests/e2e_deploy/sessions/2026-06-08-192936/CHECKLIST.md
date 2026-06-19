# E2E Validation Checklist — Session 2026-06-08-192936

> Generated from `CHECKLIST_TEMPLATE.md` at 2026-06-08 19:29:36 UTC
> Subscription: Vasters | Fabric Workspace: ContosoRealTimeTest

---

## Source: `australia-wildfires`

### Azure ACI Validation

- [x] SKIPPED — not tested in this session (Fabric only)

**Azure result**: SKIP
**Notes**: Azure ACI not in scope for this session.

### Fabric Notebook Validation

- [x] Notebook deployed via `deploy-feeder-notebook.ps1`
- [x] Notebook run triggered (job instance ID: 7c66b23f-e0ec-4ca4-8151-d95fa40e6207)
- [x] Notebook run completed successfully (status: Completed)
- [x] KQL `_cloudevents_dispatch` table has rows (count: 37)
- [x] At least one typed table has rows (table: AU.Gov.Emergency.Wildfires.FireIncident, count: 37)
- [x] Map item verified (if applicable): N/A
- [x] Dashboard item verified (if applicable): N/A
- [x] Fabric items cleaned up (notebook deleted)

**Fabric result**: PASS
**Notes**: First two runs failed due to `--once` in argv causing `SystemExit(2)` from argparse (top-level flag passed after `feed` subcommand). Fixed across all 96 notebooks. Third run with fix succeeded in 3 seconds, all 37 fire incidents (VIC, NSW) flowed through dispatch → typed table. Update policy confirmed working.

### Issues Filed

| Issue # | Title | Action |
|---------|-------|--------|
| #839 | Feeders: --once defined on top-level parser instead of feed subparser | Created |

---

## Summary

| Metric | Count |
|--------|-------|
| Sources tested (Azure) | 0 |
| Sources tested (Fabric) | 1 |
| Sources skipped | 0 |
| Passes (Azure) | 0 |
| Passes (Fabric) | 1 |
| Failures (Azure) | 0 |
| Failures (Fabric) | 0 |
| Issues filed | 1 |
| Issues amended | 0 |
| Total runtime | ~25 min (including diagnosis & fix) |

