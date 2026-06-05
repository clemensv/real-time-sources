# Fabric Notebook Runbook

Reference material for the `fabric-notebook-deployment` skill. Pure
implementation detail — no policy. The policy lives in `SKILL.md`.

## Canonical "Run Cell" (thread-isolated asyncio, continuous mode)

Every bridge `main()` in this repo calls `asyncio.run(...)`. The Fabric
notebook kernel already owns the asyncio loop, so the call raises:

```
RuntimeError: asyncio.run() cannot be called from a running event loop
```

Solution: run the bridge in a worker thread that owns its own loop. The
worker also captures the exception so it can be re-raised on the main thread
and surfaced via `notebookutils.notebook.exit("FAIL: …")`.

**Continuous mode** (preferred for real-time sources): the feeder polls
at its native cadence for `RUN_DURATION` seconds (default 3300 = 55 min),
then exits. The Fabric scheduler (60 min) restarts it as a safety net.
This amortizes the ~65-70 s cold-start overhead across the full run.

```python
import os, pathlib, sys, traceback, datetime

LOG_PATH = '/lakehouse/default/Files/feeder-state/<source>/last-run.log'
pathlib.Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)

def _log(msg):
    line = f'[{datetime.datetime.utcnow().isoformat()}Z] {msg}'
    print(line)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

# truncate at start of run
with open(LOG_PATH, 'w', encoding='utf-8') as f:
    f.write('')

try:
    _log('Starting feeder (continuous mode)')
    pathlib.Path(STATE_FILE).parent.mkdir(parents=True, exist_ok=True)
    os.environ['STATE_FILE']       = STATE_FILE
    os.environ['POLLING_INTERVAL'] = str(POLLING_INTERVAL)
    os.environ['ONCE_MODE']        = 'true' if ONCE_MODE else 'false'
    _log(f'CONNECTION_STRING present: {bool(os.environ.get("CONNECTION_STRING"))}')

    _log('Importing <source> package from Fabric Environment...')
    from <source> import <source> as feeder
    _log(f'Imported feeder from: {feeder.__file__}')

    argv_backup = sys.argv
    try:
        sys.argv = ['<source>', 'feed', '--once'] if ONCE_MODE else ['<source>', 'feed']
        _log(f'Running feeder.main() with argv={sys.argv}, duration={RUN_DURATION}s')
        import threading
        _err = []
        def _worker():
            try:
                feeder.main()
            except BaseException as e:
                _err.append(e)
        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        t.join(timeout=RUN_DURATION)
        if t.is_alive():
            _log(f'Run duration {RUN_DURATION}s reached; exiting cleanly.')
        elif _err:
            raise _err[0]
    finally:
        sys.argv = argv_backup
    _log('Cycle complete.')
    try:
        import notebookutils
        notebookutils.notebook.exit('OK')
    except Exception:
        pass
except Exception as exc:
    tb = traceback.format_exc()
    _log(f'FAILED: {exc}\n{tb}')
    try:
        import notebookutils
        notebookutils.notebook.exit(f'FAIL: {exc}')
    except Exception:
        pass
    raise
```

**Key difference from single-shot mode:** `t.join(timeout=RUN_DURATION)`
instead of `t.join()`. The daemon thread is abandoned on timeout — its
asyncio loop dies with the thread. No explicit cancellation is needed.

For single-shot mode (`ONCE_MODE = True`), the feeder passes `--once`
and exits after one poll cycle; use `t.join()` with no timeout.

## Canonical "CS Lookup Cell" (public Topology API)

```python
import os, requests
try:
    import notebookutils
    token = notebookutils.credentials.getToken('pbi')
except Exception:
    from notebookutils import mssparkutils
    token = mssparkutils.credentials.getToken('pbi')

FABRIC_API = 'https://api.fabric.microsoft.com/v1'
headers = {'Authorization': f'Bearer {token}'}
workspace_id = WORKSPACE_ID

es_list = requests.get(f'{FABRIC_API}/workspaces/{workspace_id}/eventstreams', headers=headers, timeout=30).json()
es = next((e for e in es_list.get('value', []) if e.get('displayName') == EVENTSTREAM_NAME), None)
if not es:
    raise RuntimeError(f"Event Stream '{EVENTSTREAM_NAME}' not found in workspace {workspace_id}.")

topo = requests.get(f'{FABRIC_API}/workspaces/{workspace_id}/eventstreams/{es["id"]}/topology', headers=headers, timeout=30).json()
src = next((s for s in topo.get('sources', []) if s.get('type') == 'CustomEndpoint'), None)
if not src:
    raise RuntimeError("Event Stream has no CustomEndpoint source.")

conn = requests.get(
    f'{FABRIC_API}/workspaces/{workspace_id}/eventstreams/{es["id"]}/sources/{src["id"]}/connection',
    headers=headers, timeout=30,
).json()
os.environ['CONNECTION_STRING'] = conn['accessKeys']['primaryConnectionString']
```

## Deploy Flag Matrix

| Scenario | Flags |
|----------|-------|
| First-ever deploy (continuous mode) | _(none)_ — defaults to 60-min schedule |
| First-ever deploy (single-shot mode) | `-ScheduleIntervalMinutes 15` (or per source cadence) |
| Notebook-only change, env unchanged | `-SkipEnvironment` |
| Inspect deploy without scheduling | `-NoSchedule -NoTriggerNow` |
| Two Lakehouses in workspace | `-DefaultLakehouse <name>` |
| Override schedule interval | `-ScheduleIntervalMinutes <5-60>` |

## OneLake Log Read (PowerShell)

```powershell
$tok = az account get-access-token --resource https://storage.azure.com --query accessToken -o tsv
$ws  = '<workspaceId>'
$lh  = '<lakehouseItemId>'
irm "https://onelake.dfs.fabric.microsoft.com/$ws/$lh/Files/feeder-state/<source>/last-run.log" `
  -Headers @{Authorization="Bearer $tok"}
```

## Known Transient Errors

| Symptom | Cause | Action |
|---------|-------|--------|
| `InternalServerError` from `/kqlDatabases` GET | Fabric warmup | Wait 20s, retry |
| `notebookSnapshot` returns 404 | Not exposed via REST | Use OneLake log file |
| Publish stuck at `Running` >5 min | Cold pool | Poll up to 10 min |
| Job `Failed` with no failure detail beyond `System cancelled` | Cell exception | Read OneLake log |
| 401 with `kusto.fabric.microsoft.com` audience | Wrong resource | Use `kusto.kusto.windows.net` |
| `asyncio.run() cannot be called from a running event loop` | Direct asyncio in cell | Wrap in `threading.Thread` |
| `Requires-Dist: foo @ file:///…` install failure | Poetry path-dep in wheel | Run `strip-wheel-pathdeps.py` |
| Env publish accepted but libraries missing | Used JSON upload | Re-upload via `Invoke-WebRequest -Form` |

## Reference Deployment Numbers (pegelonline)

- Env publish: 3–4 min
- Notebook cold run: 3–4 min total (60–120 s startup + 2 min work)
- Notebook warm run (env cached): 30–60 s
- Single cycle output: 785 stations + 736 measurements = 1521 events
