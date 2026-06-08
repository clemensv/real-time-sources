# E2E Validation Checklist — Session {SESSION_ID}

> Generated from `CHECKLIST_TEMPLATE.md` at {TIMESTAMP}
> Subscription: {SUBSCRIPTION} | Fabric Workspace: {WORKSPACE}

---

## Source: `{SOURCE_NAME}`

### Azure ACI Validation

- [ ] Resource group `e2e-{SOURCE_NAME}-{TS}` created
- [ ] Event Hubs namespace deployed (Standard, 1 TU)
- [ ] Event Hub entity `{SOURCE_NAME}` created
- [ ] Connection string obtained
- [ ] ACI container deployed from `azure-template.json`
- [ ] Container reached Running state
- [ ] Messages received on Event Hub (count: ___)
- [ ] CloudEvents envelope validated (type, source, subject present)
- [ ] Kafka key matches xreg subject template
- [ ] Schema validated against xreg manifest
- [ ] Resource group deleted and confirmed gone

**Azure result**: {PASS | FAIL | SKIP}
**Notes**: ___

### Fabric Notebook Validation

- [ ] Notebook deployed via `deploy-feeder-notebook.ps1`
- [ ] Notebook run triggered (job instance ID: ___)
- [ ] Notebook run completed successfully (status: ___)
- [ ] KQL `_cloudevents_dispatch` table has rows (count: ___)
- [ ] At least one typed table has rows (table: ___, count: ___)
- [ ] Map item verified (if applicable): {YES | N/A}
- [ ] Dashboard item verified (if applicable): {YES | N/A}
- [ ] Fabric items cleaned up (notebook, KQL DB entries, Lakehouse state)

**Fabric result**: {PASS | FAIL | SKIP}
**Notes**: ___

### Issues Filed

| Issue # | Title | Action |
|---------|-------|--------|
| ___ | ___ | Created / Amended |

---

<!-- Repeat the "Source" section above for each source in the run -->

## Summary

| Metric | Count |
|--------|-------|
| Sources tested (Azure) | ___ |
| Sources tested (Fabric) | ___ |
| Sources skipped | ___ |
| Passes (Azure) | ___ |
| Passes (Fabric) | ___ |
| Failures (Azure) | ___ |
| Failures (Fabric) | ___ |
| Issues filed | ___ |
| Issues amended | ___ |
| Total runtime | ___ |
