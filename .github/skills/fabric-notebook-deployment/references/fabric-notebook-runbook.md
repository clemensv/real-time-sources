# Fabric Notebook Runbook

Implementation reference for the [notebook skill](../SKILL.md).
The isolated Pegelonline pilot established the requirements below; its
implementation and acceptance receipts are separate work.
Do not treat legacy deployer flags as a schematized deployment recipe.

## Environment and definition

1. Build the actual source-local core, transport and generated producer wheels.
   Strip local path dependencies with `tools/deploy-fabric/strip-wheel-pathdeps.py`.
2. Verify native wheels in a clean Linux container matching the Fabric Python
   ABI and platform. For Proton, assert `SSL.present()`; import alone passes
   even when the library was compiled with TLS stubs.
3. If building Proton from source, install compatible OpenSSL development
   headers and pkg-config before building, then repair with auditwheel.
   The pilot used CPython 3.11 in manylinux_2_28 with `openssl-devel`.
   Record exact tool versions, build image digest and final wheel SHA-256.
4. Upload an explicit allowlist of custom wheels and `environment.yml` through
   multipart library upload. Do not glob a scratch directory containing failed
   wheels or build dependencies. Wait for publication `Success`.
5. Upload/read back the Spark notebook definition, Environment, Lakehouse and
   child KQL database bindings. The verified native definition uses
   `notebook-content.py`, `format: fabricGitSource`, an InlineBase64 part and
   kernel `synapse_pyspark`. This definition format is distinct from the
   multipart Environment library API.

The current shared deployer forces Python and removes Environment bindings.
Do not use it against migrated items until corrected and verified.
Use documented public operation-state/result APIs for accepted asynchronous
requests. Honor `Retry-After`, bound waits, and reconcile accepted jobs/items
before retrying a mutation after an ambiguous response.

## Identity and source connection lookup

Prefer the workspace managed identity for both control-plane and publishing
operations wherever supported. Verify the runtime principal, token audience,
transport support and least-privilege role assignments for each operation.
Do not assume `notebookutils.credentials.getToken("pbi")` runs as the workspace
identity; establish the effective identity through supported runtime/service
metadata. Do not log tokens to inspect them.

Resolve the exact source's binding through the public Topology API with an
approved Fabric API token. Use token-based publishing with workspace identity
where supported. If it is unsupported, record that limitation and obtain
approval for a fallback; prefer another supported Entra flow before SAS.
Do not enable local authentication or fetch access keys as a default.

The helper below is for an approved source-connection lookup, not an
instruction to select SAS. It selects one Eventstream and named CustomEndpoint,
and its connection response can contain secrets. It
raises on HTTP failure, handles continuation pages and rejects ambiguity.
Keep the returned connection in memory; never print it.

```python
from urllib.parse import urlparse

import requests

FABRIC_API = "https://api.fabric.microsoft.com/v1"

def source_connection(workspace_id, eventstream_name, source_name, token):
    headers = {"Authorization": f"Bearer {token}"}

    def get_json(url):
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    url = f"{FABRIC_API}/workspaces/{workspace_id}/eventstreams"
    matches = []
    seen = set()
    while url:
        parsed = urlparse(url)
        if (parsed.scheme != "https" or parsed.netloc != "api.fabric.microsoft.com"
                or not parsed.path.startswith(f"/v1/workspaces/{workspace_id}/")):
            raise RuntimeError("Unexpected Fabric continuation URI")
        if url in seen:
            raise RuntimeError("Repeated Fabric continuation URI")
        seen.add(url)
        page = get_json(url)
        matches.extend(item for item in page["value"]
                       if item["displayName"] == eventstream_name)
        url = page.get("continuationUri")
        if page.get("continuationToken") and not url:
            raise RuntimeError("Fabric continuation token has no continuation URI")
    if len(matches) != 1:
        raise RuntimeError(f"Expected one Eventstream; found {len(matches)}")
    base = f"{FABRIC_API}/workspaces/{workspace_id}/eventstreams/{matches[0]['id']}"
    sources = [item for item in get_json(base + "/topology")["sources"]
               if item["type"] == "CustomEndpoint" and item["name"] == source_name]
    if len(sources) != 1:
        raise RuntimeError(f"Expected one named CustomEndpoint; found {len(sources)}")
    return get_json(base + f"/sources/{sources[0]['id']}/connection")
```

Map the returned binding to the selected transport's supported authentication.
Do not assume Kafka and AMQP consume identical connection-string forms.
For an explicitly approved SAS fallback only, preserve key padding when parsing
key/value pairs (`split("=", 1)`). The pilot used this fallback; its receipt
does not establish that workspace identity is unavailable.

## Bounded one-shot run wrapper

The following function accepts a source adapter that runs one cycle with its
already-resolved connection and state configuration. Call it from a cell with
`notebookutils.notebook.exit(run_once(...))`; keep that exit outside exception
handlers. For bridges whose entry point uses `asyncio.run()`, the worker owns
the loop. Do not modify global producer classes to inject configuration.

```python
import logging
import threading
from pathlib import Path

def run_once(run_feeder, duration, log_path):
    if duration <= 0:
        raise ValueError("Run duration must be positive")
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    failures = []

    class RunLog(logging.FileHandler):
        def emit(self, record):
            super().emit(record)
            if record.levelno >= logging.ERROR:
                failures.append(record.getMessage())

    handler = RunLog(log_path, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger()
    previous_level = logger.level
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    try:
        def worker():
            try:
                run_feeder()
            except BaseException as exc:
                failures.append(f"{type(exc).__name__}: {exc}")
                logger.exception("Feeder worker failed")

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        thread.join(timeout=duration)
        if thread.is_alive():
            raise TimeoutError("Feeder still running; stop the job/session before reuse")
        if failures:
            raise RuntimeError("Feeder failed; inspect the OneLake run log")
        logger.info("Cycle complete")
        result = "OK"
    except Exception as exc:
        logger.exception("Notebook feeder failed")
        result = f"FAIL: {exc}"
    finally:
        handler.flush()
        logger.removeHandler(handler)
        handler.close()
        logger.setLevel(previous_level)
    return result
```

Use `/lakehouse/default/Files/feeder-state/<source>/last-run.log`. The source
adapter must flush/close its producer in `finally` and retain dedupe state.
Do not log credentials. A timeout does not kill a Python thread: the failed
invocation must be stopped before reusing its session or state. Continuous
mode requires a source-specific cooperative shutdown and verified worker exit;
abandoning a daemon thread is not clean completion.

## TLS preflight

Before any AMQP publish, check the installed native library and CA bundle:

```python
import os
from pathlib import Path
from proton import SSL
import requests

if not SSL.present():
    raise RuntimeError("Installed Proton wheel has no TLS support")
ca_bundle = requests.certs.where()
if not Path(ca_bundle).is_file():
    raise RuntimeError("CA bundle is missing")
os.environ["SSL_CERT_FILE"] = ca_bundle
```

Run this within the notebook's logged failure boundary. Never disable
certificate verification to get a connection.

## Diagnostics and acceptance

Read OneLake logs with the storage token audience:

```powershell
$tok = az_m account get-access-token --resource https://storage.azure.com --query accessToken -o tsv
$ws = '<workspaceId>'
$lh = '<lakehouseItemId>'
irm "https://onelake.dfs.fabric.microsoft.com/$ws/$lh/Files/feeder-state/<source>/last-run.log" `
  -Headers @{Authorization="Bearer $tok"}
```

Job `Completed` can coexist with runtime failure or total ingestion rejection.
Broker success with no fresh typed rows requires inspection of Eventstream
validation logs and actual wire metadata, not a connection-string reset.
Verify all selected families and correlate fresh output/history; see the
[acceptance criteria](../SKILL.md#e2e-verification-mandatory-before-declaring-done).

Do not hardcode reference event counts: upstream inventory and dedupe change
them. Keep per-run evidence. The pilot's first accepted manual cycle matched
1,525 events and first scheduled cycle matched 1,399; these are receipts,
not expected constants for later runs.

After manual acceptance, approve and read back schedule cadence/expiry,
observe a real scheduled invocation and record its full duration. Retain
history, items and state when a temporary schedule expires.
