---
name: notebook-feeder-retrofit
description: "Use to retrofit an existing poll-based feeder in this repo with a Fabric notebook hosting option. Adds `<source>/notebook/<source>-feed.ipynb`, flips `catalog.json` `notebook: true`, validates the bridge supports single-cycle execution, runs the existing test suite, and opens a PR. Designed to be dispatched in parallel across many sources by a fleet of upgrade agents."
argument-hint: "Pass exactly one source id (e.g. `bafu-hydro`) per agent invocation. Optionally pass a Branch name; otherwise the agent uses `notebook-retrofit-<source>`."
---

# Notebook Feeder Retrofit (Upgrade Agent)

You are an **upgrade agent**. Your job is to retrofit **one** existing
poll-based source in this repo with a Fabric notebook hosting option, by
replicating the canonical `pegelonline` pattern. Do not invent new
patterns — copy, substitute, validate, open PR. If the source is
ineligible, abort with a clear reason; do not "make it work" by changing
the bridge architecture.

## Inputs

- `SOURCE` — the source directory name (e.g. `bafu-hydro`,
  `usgs-iv`, `entsoe`).
- `BRANCH` — optional; default `notebook-retrofit-<SOURCE>`.

## Single-Source Scope

**One agent processes one source.** Do not loop over sources in a single
agent. The orchestrator dispatches a fleet of agents in parallel, one per
source.

## Eligibility Gate (run first, abort if any fail)

A source qualifies if **all** of the following are true:

1. `<SOURCE>/` exists and contains `<SOURCE>/pyproject.toml`,
   `xreg/<SOURCE>.xreg.json`, and a bridge module exposing `def main()`.
2. The bridge supports **single-cycle execution** — either via a
   `--once` CLI flag (preferred) or via an `ONCE_MODE` environment
   variable that exits after one polling cycle. Verify by grepping the
   bridge module for `--once|once_mode|ONCE_MODE`.
3. The bridge is **poll-based**, not a long-lived stream. WebSocket,
   MQTT, raw-TCP, and SSE-firehose bridges are **out of scope** for this
   agent. Heuristic: the bridge calls `time.sleep`, `asyncio.sleep`, or
   has a `POLLING_INTERVAL` env var, and does **not** open a persistent
   socket.
4. The source has a Docker E2E test that already passes on `main`
   (`tests/docker_e2e/test_docker_kafka_flow.py` contains a class for
   the source). If it does not, the bridge's contract is unverified;
   abort.
5. `<SOURCE>/notebook/<SOURCE>-feed.ipynb` does **not** already exist.

If any check fails, write a one-line skip reason to
`tmp/notebook-retrofit-skipped.log` (append) and call `task_complete`
with the reason. Do **not** open a PR.

### Add `--once` if missing

If gate (2) fails but the bridge is clearly a poller (gate 3 passes),
you may add a `--once` flag to the bridge's argparse setup and a
single-cycle exit branch in the polling loop, modeled after
`pegelonline/pegelonline/pegelonline.py`. This is a small, mechanical
change. Add a unit test that asserts `--once` causes `main()` to return
after exactly one cycle (mock the upstream HTTP). If the bridge is not
written with a clean polling loop you can interrupt, abort instead.

## Retrofit Steps (in order)

### 1. Branch + folder

```powershell
git checkout main
git pull --ff-only
git checkout -b $BRANCH
New-Item -ItemType Directory -Force -Path "$SOURCE/notebook" | Out-Null
```

### 2. Copy and substitute the canonical notebook

The template is `pegelonline/notebook/pegelonline-feed.ipynb`. **Copy
verbatim**, then perform the substitutions in
[`references/notebook-substitution-table.md`](references/notebook-substitution-table.md).
The substitutions are exact and mechanical; do not paraphrase.

Critical substitutions:

| From (pegelonline) | To |
|---|---|
| `from pegelonline import pegelonline as feeder` | `from <PKG> import <MODULE> as feeder` |
| `sys.argv = ['pegelonline', 'feed', '--once']` | `sys.argv = [<bridge argv-0>, <subcommand>, '--once']` |
| `sys.argv = ['pegelonline', 'feed']` (else branch) | same as above without `--once` |
| `/lakehouse/default/Files/feeder-state/pegelonline/` | `/lakehouse/default/Files/feeder-state/<SOURCE>/` |
| `Pegelonline Feeder (Fabric Notebook)` (title) | `<Display Name> Feeder (Fabric Notebook)` |
| `pegelonline-ingest` (default `EVENTSTREAM_NAME`) | `<SOURCE>-ingest` (the deploy script overwrites this) |
| Markdown copy describing the source | one-paragraph adaptation from `<SOURCE>/README.md` |

Resolve `<PKG>`, `<MODULE>`, `<bridge argv-0>`, and `<subcommand>` by
inspecting `<SOURCE>/pyproject.toml` (`[tool.poetry.scripts]` or the
package layout) and the bridge module's `argparse` setup. **Do not
guess.** If the bridge has no CLI subcommand (calls `main()` with no
args), drop the subcommand element and use `sys.argv = ['<SOURCE>',
'--once']` instead.

Do **not** change the four-cell structure, the CS-lookup cell, the
worker-thread run cell, or the OneLake log path layout. Those are
load-bearing — see `.github/skills/fabric-notebook-deployment/SKILL.md`.

### 3. Catalog flag

Edit `catalog.json` to add `"notebook": true` to the `<SOURCE>` entry.
Keep the existing key order; insert `notebook` after `kql`. If the entry
does not exist, abort — the source isn't published in the portal and
shouldn't have a notebook button.

### 4. Validate locally

Run these checks in order; **fix and re-run on any failure** before
opening a PR:

```powershell
# Notebook JSON well-formed
python -c "import json; json.load(open('$SOURCE/notebook/$SOURCE-feed.ipynb'))"

# Bridge unit tests still pass
cd $SOURCE; python -m pytest tests/ -x --no-header -q; cd ..

# If you added --once, run the new unit test specifically:
cd $SOURCE; python -m pytest tests/test_once_mode.py -v; cd ..

# Notebook params cell actually contains the placeholders the deploy script patches
$nb = Get-Content "$SOURCE/notebook/$SOURCE-feed.ipynb" -Raw
foreach ($k in 'EVENTSTREAM_NAME','STATE_FILE','POLLING_INTERVAL','ONCE_MODE','WORKSPACE_ID') {
    if ($nb -notmatch "(?m)^\s*$k\s*=") { throw "Missing placeholder: $k" }
}

# Notebook does NOT contain forbidden patterns
foreach ($bad in 'asyncio\.run\(','%pip install','CONNECTION_STRING\s*=\s*"','primaryConnectionString.*=') {
    if ($nb -match $bad) { throw "Forbidden pattern present: $bad" }
}
```

### 5. Documentation touch (minimal)

- Add a one-sentence "Fabric notebook hosting" bullet to
  `<SOURCE>/README.md` linking to
  `tools/deploy-fabric/deploy-feeder-notebook.ps1`. Do **not** create a
  separate doc.
- Do **not** edit `EVENTS.md` or `CONTAINER.md`.

### 6. Commit + PR

```powershell
git add "$SOURCE/notebook/" "$SOURCE/README.md" catalog.json
# include bridge + test changes only if you added --once
git commit -m "feat($SOURCE): Fabric notebook hosting option

Adds notebook/$SOURCE-feed.ipynb following the pegelonline pattern.
Flips catalog.json notebook flag so the gh-pages portal exposes the
Fabric Notebook deploy button.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push -u origin $BRANCH
gh pr create --base main --title "feat($SOURCE): Fabric notebook hosting option" `
  --body "Retrofit by notebook-feeder-retrofit agent. Validated locally: notebook JSON ok, bridge tests pass, parameters cell complete, no forbidden patterns. The wheel-bundle workflow (.github/workflows/publish-notebook-wheels.yml) will pick up this source on next push to main and publish wheels to the notebook-wheels release."
```

### 7. Do NOT run a live Fabric deployment

The agent does **not** deploy to ContosoRealTimeTest. The wheel-publish
workflow runs on PR merge and the portal exposes the button once
`update-ghpages-catalog.yml` syncs the flag. End-to-end Fabric
validation is performed manually by the maintainer (or by a separate
verification agent) once the PR is merged.

Reason: each Fabric deployment consumes capacity time, creates
workspaces/environments/notebooks, and competes with other agents in
the fleet for the same shared workspace. Serial verification is cheaper
than parallel deployment.

## Done Criteria

The agent is done when:

- A PR is open with the notebook, the catalog flag flip, and (if
  needed) the `--once` addition.
- Local validation passed (notebook JSON, bridge tests, placeholder
  check, forbidden-pattern check).
- The PR body cites this skill and lists the validations performed.

If any retrofit step cannot complete (e.g. bridge has no extractable
CLI shape, tests fail and the cause is the new code), abort, push
nothing, and call `task_complete` with a clear blocker description.

## Things That Are Not Allowed

- Deploying to Fabric from the agent. Hand-off to manual verification.
- Editing wheels, the deploy script, the publish workflow, or anything
  under `tools/deploy-fabric/`. Those are infrastructure; this agent
  only consumes them.
- Editing `.github/skills/fabric-notebook-deployment/` or
  `.github/copilot-instructions.md` — the agent is a consumer of those.
- Bundling multiple sources into one PR. One source, one PR.
- Skipping the eligibility gate.
- Inventing new notebook cell structure, alternative CS-lookup
  techniques, or new log-file locations. Copy verbatim from
  `pegelonline`.
- Forcing a streaming bridge (websocket/MQTT/SSE) into the polling
  notebook model. Abort instead.

## References

- `.github/skills/fabric-notebook-deployment/SKILL.md` — the deployment
  pipeline this notebook plugs into.
- `pegelonline/notebook/pegelonline-feed.ipynb` — template.
- `tools/deploy-fabric/deploy-feeder-notebook.ps1` — line ~540: shows
  the exact parameter names the deploy script will overwrite. The
  notebook MUST declare all of them.
- `references/notebook-substitution-table.md` — exact substitution
  mapping.
- `references/eligibility-discovery.ps1` — one-shot discovery script
  that prints the eligible-source set for the orchestrator.
