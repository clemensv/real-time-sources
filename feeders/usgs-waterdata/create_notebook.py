"""Build the four-cell native feeder notebook for the shared Python host."""

import argparse
import json
from pathlib import Path


PARAMETERS = '''# Parameters patched by the Fabric deployer.
EVENTSTREAM_NAME = "usgs-waterdata-ingest"
EVENTSTREAM_SOURCE_NAME = "usgs-waterdata-input"
USGS_WATERDATA_SITES = "USGS-01646500"
USGS_WATERDATA_PARAMETERS = "00010,00060"
STATE_FILE = "/lakehouse/default/Files/feeder-state/usgs-waterdata/state.json"
POLLING_INTERVAL = 300
RUN_DURATION = 900
ONCE_MODE = True
WORKSPACE_ID = ""
'''

LOOKUP = '''import importlib, importlib.metadata, os, pathlib, subprocess, sys
import notebookutils

FABRIC_API = "https://api.fabric.microsoft.com/v1"

def _bootstrap():
    directory = pathlib.Path("/lakehouse/default/Files/wheels/usgs-waterdata")
    wheels = sorted(directory.glob("*.whl"))
    required = ("usgs_waterdata-", "usgs_waterdata_core-",
                "usgs_waterdata_producer_data-", "usgs_waterdata_producer_kafka_producer-")
    for prefix in required:
        if len([wheel for wheel in wheels if wheel.name.startswith(prefix)]) != 1:
            raise RuntimeError(f"Expected one deployed {prefix} wheel in {directory}")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps"]
        + [str(wheel) for wheel in wheels], timeout=300)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade",
         "requests>=2.32.3", "urllib3>=2.2.3", "cloudevents>=1.12.1,<2.0.0", "isodate>=0.6.1",
         "confluent-kafka>=2.5.3", "avro>=1.11.3", "dataclasses-json>=0.6.7,<0.7.0",
         "azure-identity>=1.19.0", "azure-storage-file-share>=12.20.0,<13.0.0"],
        timeout=300)
    importlib.invalidate_caches()
    for distribution in ("usgs-waterdata", "usgs-waterdata-core",
                         "usgs-waterdata-producer-data", "usgs-waterdata-producer-kafka-producer"):
        logging.info("Active package %s version %s", distribution, importlib.metadata.version(distribution))

def _read(url, headers):
    import requests
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()

def _pages(url, headers):
    while url:
        page = _read(url, headers)
        yield from page.get("value", [])
        next_url = page.get("continuationUri")
        if next_url and not next_url.startswith(FABRIC_API + "/"):
            raise RuntimeError("Fabric pagination escaped the public API origin")
        url = next_url

def _connection():
    workspace_id = WORKSPACE_ID or notebookutils.runtime.context["currentWorkspaceId"]
    token = notebookutils.credentials.getToken("pbi")
    headers = {"Authorization": f"Bearer {token}"}
    matches = [item for item in _pages(f"{FABRIC_API}/workspaces/{workspace_id}/eventstreams", headers)
               if item.get("displayName") == EVENTSTREAM_NAME]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one named Eventstream")
    endpoint = f"{FABRIC_API}/workspaces/{workspace_id}/eventstreams/{matches[0]['id']}"
    topology = _read(endpoint + "/topology", headers)
    sources = [item for item in topology.get("sources", [])
               if item.get("type") == "CustomEndpoint" and item.get("name") == EVENTSTREAM_SOURCE_NAME]
    if len(sources) != 1:
        raise RuntimeError("Expected exactly one named CustomEndpoint source")
    connection = _read(f"{endpoint}/sources/{sources[0]['id']}/connection", headers)
    # This metadata endpoint also returns keys. Discard them without selecting or logging one.
    connection.pop("accessKeys", None)
    namespace, entity = connection.get("fullyQualifiedNamespace"), connection.get("eventHubName")
    if (connection.get("type") != "CustomEndpoint"
            or not isinstance(namespace, str) or not namespace
            or any(character in namespace for character in "/:; \\t\\r\\n")
            or not isinstance(entity, str) or not entity or ";" in entity):
        raise RuntimeError("Named source connection response has no valid namespace/entity binding")
    return f"BootstrapServer={namespace}:9093;EntityPath={entity}"

'''

RUN = '''import datetime, logging, os, pathlib, sys, threading, traceback
import notebookutils

LOG_PATH = "/lakehouse/default/Files/feeder-state/usgs-waterdata/last-run.log"
pathlib.Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
handler = logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)
status = "FAIL: feeder did not complete"
try:
    if not ONCE_MODE:
        raise RuntimeError("This scheduled notebook requires bounded one-shot polling")
    if RUN_DURATION <= 0:
        raise ValueError("RUN_DURATION must be positive")
    _bootstrap()
    os.environ["CONNECTION_STRING"] = _connection()
    os.environ["KAFKA_AUTH_MODE"] = "fabric-entra"
    os.environ["KAFKA_ENABLE_TLS"] = "true"
    pathlib.Path(STATE_FILE).parent.mkdir(parents=True, exist_ok=True)
    os.environ["STATE_FILE"] = STATE_FILE
    os.environ["STATE_BACKEND"] = "local"
    os.environ["POLLING_INTERVAL"] = str(POLLING_INTERVAL)
    os.environ["USGS_WATERDATA_SITES"] = str(USGS_WATERDATA_SITES)
    os.environ["USGS_WATERDATA_PARAMETERS"] = str(USGS_WATERDATA_PARAMETERS)
    os.environ["ONCE_MODE"] = "true"
    from usgs_waterdata import app as feeder
    logging.info("Starting native USGS cycle; existing dedupe state is preserved")
    previous_argv = sys.argv
    errors = []
    try:
        sys.argv = ["usgs-waterdata", "feed", "--once"]
        def _worker():
            try:
                feeder.main()
            except BaseException as exc:
                errors.append(exc)
        worker = threading.Thread(target=_worker, daemon=True)
        worker.start()
        worker.join(timeout=RUN_DURATION)
        if worker.is_alive():
            raise TimeoutError("Feeder worker did not exit; stop this Fabric job/session before reusing its state")
        if errors:
            raise errors[0]
    finally:
        sys.argv = previous_argv
    logging.info("Native USGS cycle completed with confirmed transport delivery")
    status = "OK"
except BaseException as exc:
    logging.error("Native USGS notebook failed: %s\\n%s", exc, traceback.format_exc())
    status = f"FAIL: {type(exc).__name__}: {exc}"
finally:
    handler.flush()
    root_logger.removeHandler(handler)
    handler.close()
notebookutils.notebook.exit(status)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("usgs-waterdata", "usgs-iv", "usgs-nwis-wq"),
                        default="usgs-waterdata")
    source = parser.parse_args().source
    package = source.replace("-", "_")
    title = {"usgs-waterdata": "USGS Water Data", "usgs-iv": "USGS Instantaneous Values",
             "usgs-nwis-wq": "USGS Water Quality"}[source]
    intro = (
        "# USGS Water Data Feeder (Fabric Notebook)\n\n"
        "Runs the native continuous-observation Kafka bridge and its monitoring-location, "
        "time-series and parameter reference events in the plain Python kernel. "
        "See [source documentation](https://github.com/clemensv/real-time-sources/tree/main/feeders/usgs-waterdata). "
        "The shared deployer uploads source wheels to OneLake; the run cell installs them "
        "and their public dependencies before acquisition, without an Environment binding. "
        "Missing or ambiguous wheels and installation failures are reported in the OneLake log. "
        "Kafka uses refreshed NotebookUtils Event Hubs tokens with OAUTHBEARER, without source-key authentication. "
        "The token represents the notebook execution principal; workspace managed identity must not be assumed. "
        "The public connection metadata API also returns keys, which are discarded without use or logging. "
        "This notebook is one-shot only. "
        "Never delete delivery state for validation. A worker timeout is failure, not successful completion.\n"
    )
    parameters, lookup, run = PARAMETERS, LOOKUP, RUN
    if source != "usgs-waterdata":
        parameters = parameters.replace("usgs-waterdata", source)
        parameters = parameters.replace("USGS_WATERDATA_SITES", "USGS_SITES").replace(
            "USGS_WATERDATA_PARAMETERS", "USGS_PARAMETERS").replace('"USGS-01646500"', '"01646500"')
        parameters += 'USGS_API_MODE = "legacy"\nUSGS_ENROLLMENT_FILE = ""\n'
        lookup = lookup.replace("/wheels/usgs-waterdata", f"/wheels/{source}")
        lookup = lookup.replace('"usgs_waterdata-"', f'"{package}-"')
        lookup = lookup.replace("usgs_waterdata_producer", f"{package}_producer")
        lookup = lookup.replace('"usgs-waterdata"', f'"{source}"').replace(
            "usgs-waterdata-producer", f"{source}-producer")
        lookup = lookup.replace('"requests>=2.32.3", "urllib3>=2.2.3"',
                                '"requests>=2.34.2", "urllib3>=2.7.0", "aiohttp>=3.14.1"')
        if source == "usgs-iv":
            lookup = lookup.replace('"isodate>=0.6.1"', '"isodate>=0.6.1", "gtfs-realtime-bindings>=1.0.0", "idna>=3.15"')
        run = run.replace("usgs-waterdata", source).replace(
            "from usgs_waterdata import app as feeder", f"from {package} import {package} as feeder")
        run = run.replace("USGS_WATERDATA_SITES", "USGS_SITES").replace(
            "USGS_WATERDATA_PARAMETERS", "USGS_PARAMETERS")
        run = run.replace('os.environ["ONCE_MODE"] = "true"',
                          'os.environ["ONCE_MODE"] = "true"\n'
                          '    os.environ["USGS_API_MODE"] = USGS_API_MODE\n'
                          '    os.environ["USGS_ENROLLMENT_FILE"] = USGS_ENROLLMENT_FILE\n')
        if source == "usgs-iv":
            run = run.replace('os.environ["STATE_FILE"] = STATE_FILE',
                              'os.environ["STATE_FILE"] = STATE_FILE\n'
                              '    os.environ["USGS_LAST_POLLED_FILE"] = STATE_FILE\n')
        intro = (
            f"# {title} Feeder (Fabric Notebook)\n\n"
            "Runs the schema-frozen Kafka bridge in the plain Python kernel with OneLake wheels, state and logs. "
            "Uses namespace-scoped NotebookUtils Entra tokens for Kafka OAUTHBEARER, without source-key authentication. "
            "The token represents the execution principal, not necessarily the workspace identity. "
            "The public connection metadata API also returns keys, which are discarded without use or logging. "
            "Select `USGS_API_MODE=waterdata` and an explicitly reviewed `USGS_ENROLLMENT_FILE` for migration. "
            "Use separate state files for legacy and transitional modes; never delete state to force fresh events. "
            "The notebook is bounded and one-shot. A worker timeout is failure, not successful completion.\n"
        )
    cells = [{"cell_type": "markdown", "metadata": {}, "source": intro.splitlines(True)}]
    for index, code in enumerate((parameters, lookup, run)):
        cells.append({"cell_type": "code", "execution_count": None,
                      "metadata": {"tags": ["parameters"]} if index == 0 else {},
                      "outputs": [], "source": code.splitlines(True)})
    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"name": "jupyter_python", "display_name": "Python (Jupyter)", "language": "python"},
            "language_info": {"name": "python"},
            "microsoft": {"language": "python", "language_group": "jupyter_python"},
            "dependencies": {"environment": {}, "kqlDatabases": [], "lakehouse": {}},
        },
        "cells": cells,
    }
    directory = Path(__file__).parent.parent / source / "notebook"
    directory.mkdir(exist_ok=True)
    (directory / f"{source}-feed.ipynb").write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
