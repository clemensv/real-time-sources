"""Build the four-cell, Environment-backed native feeder notebook."""

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
# This Kafka binding requires a source access key; approve explicitly after identity review.
ACCESS_KEY_FALLBACK_APPROVED = False
'''

LOOKUP = '''import os, requests
import notebookutils

FABRIC_API = "https://api.fabric.microsoft.com/v1"

def _read(url, headers):
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
    if not ACCESS_KEY_FALLBACK_APPROVED:
        raise RuntimeError("Kafka source binding uses access-key authentication; explicit fallback approval is required.")
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
    value = connection.get("accessKeys", {}).get("primaryConnectionString")
    if not value:
        raise RuntimeError("Named source connection response has no Kafka connection string")
    return value

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
    os.environ["CONNECTION_STRING"] = _connection()
    pathlib.Path(STATE_FILE).parent.mkdir(parents=True, exist_ok=True)
    os.environ["STATE_FILE"] = STATE_FILE
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
    intro = (
        "# USGS Water Data Feeder (Fabric Notebook)\n\n"
        "Runs the native continuous-observation Kafka bridge and its monitoring-location, "
        "time-series and parameter reference events from a Fabric Environment. "
        "See [source documentation](https://github.com/clemensv/real-time-sources/tree/main/feeders/usgs-waterdata). "
        "Pure-Python metadata matches the static validator, but the shared deployer does not preserve the Spark Environment "
        "required by current hosting guidance. Hosting and identity approval remain release gates. Access-key fallback requires explicit approval; "
        "the generated Kafka binding has no verified workspace-identity flow. This notebook is one-shot only. "
        "Never delete delivery state for validation. A worker timeout is failure, not successful completion.\n"
    )
    cells = [{"cell_type": "markdown", "metadata": {}, "source": intro.splitlines(True)}]
    for index, code in enumerate((PARAMETERS, LOOKUP, RUN)):
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
    directory = Path(__file__).parent / "notebook"
    directory.mkdir(exist_ok=True)
    (directory / "usgs-waterdata-feed.ipynb").write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
