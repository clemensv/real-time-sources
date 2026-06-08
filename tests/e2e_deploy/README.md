# End-to-End Deployment Validation

This suite validates every source in the repository by deploying it to both
Azure (ACI + Event Hubs) and Microsoft Fabric (Notebook + KQL), verifying
that data flows end-to-end, and tearing down resources immediately after
each source.

## Prerequisites

- Azure CLI (`az`) logged in with a subscription that can create resource
  groups, Event Hubs namespaces, and Container Instances.
- GitHub CLI (`gh`) authenticated (for filing issues).
- PowerShell 7+.
- `az` extensions: `eventhubs`, `containerapp` (optional).
- Fabric REST API access (bearer token with Fabric.ReadWrite.All).
- The deploy script dependencies: `pip`, `python 3.10+`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `E2E_SUBSCRIPTION` | Yes (Azure) | Azure subscription name or ID |
| `E2E_REGION` | No | Azure region (default: `westeurope`) |
| `E2E_FABRIC_WORKSPACE` | Yes (Fabric) | Fabric workspace name |
| `E2E_FABRIC_TOKEN` | Yes (Fabric) | Fabric bearer token |
| `E2E_TIMEOUT_AZURE` | No | Azure wait timeout in seconds (default: 600) |
| `E2E_TIMEOUT_FABRIC` | No | Fabric wait timeout in seconds (default: 900) |
| `E2E_SKIP_AZURE` | No | Set to `true` to skip Azure tests |
| `E2E_SKIP_FABRIC` | No | Set to `true` to skip Fabric tests |

Source-specific API keys (e.g. `AISSTREAM_API_KEY`) are read from the
environment. If a required key is missing, the source is **skipped** with a
warning — not marked as failed.

## Usage

```powershell
# Full run — all sources, both targets
./tests/e2e_deploy/run_e2e.ps1

# Single source, Azure only
./tests/e2e_deploy/test_azure_aci.ps1 -Source noaa-ndbc -SessionDir ./tests/e2e_deploy/sessions/2025-01-01-120000

# Single source, Fabric only
./tests/e2e_deploy/test_fabric_notebook.ps1 -Source noaa-ndbc -SessionDir ./tests/e2e_deploy/sessions/2025-01-01-120000
```

## Session Output

Each run creates a timestamped session directory:

```
tests/e2e_deploy/sessions/<YYYY-MM-DD-HHMMSS>/
  CHECKLIST.md      — filled-in copy of the template
  summary.json      — machine-readable results
  log.txt           — full run log
```

Prior sessions are never overwritten. The `sessions/` directory is
git-ignored except for `.gitkeep`.

## Issue Filing

Failures are reported as GitHub issues tagged `e2e-validation`. If an issue
with the same title pattern already exists (open), a comment is appended
rather than creating a duplicate.
