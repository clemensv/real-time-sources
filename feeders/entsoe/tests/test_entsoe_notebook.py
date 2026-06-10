import json
from pathlib import Path


def test_entsoe_fabric_notebook_structure():
    notebook_path = Path(__file__).resolve().parents[1] / "notebook" / "entsoe-feed.ipynb"
    assert notebook_path.exists()

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert notebook["nbformat"] == 4
    assert notebook["metadata"]["dependencies"] == {
        "environment": {},
        "kqlDatabases": [],
        "lakehouse": {},
    }

    parameters_cell = notebook["cells"][1]
    assert parameters_cell["metadata"]["tags"] == ["parameters"]
    parameters_source = "".join(parameters_cell["source"])
    assert 'EVENTSTREAM_NAME = "entsoe-ingest"' in parameters_source
    assert 'STATE_FILE       = "/lakehouse/default/Files/feeder-state/entsoe/state.json"' in parameters_source

    lookup_source = "".join(notebook["cells"][4]["source"])
    assert "notebookutils.credentials.getToken('pbi')" in lookup_source
    assert "'Bearer ' + _get_pbi_token()" in lookup_source
    assert "/workspaces/{workspace_id}/eventstreams" in lookup_source
    assert "/sources/{src[\"id\"]}/connection" in lookup_source

    run_source = "".join(notebook["cells"][6]["source"])
    assert "from entsoe import entsoe as feeder" in run_source
    assert "sys.argv = ['entsoe', 'feed', '--once'] if ONCE_MODE else ['entsoe', 'feed']" in run_source
    assert "ENTSOE_SECURITY_TOKEN present" in run_source
    assert "threading.Thread" in run_source
    assert "notebookutils.notebook.exit('OK')" in run_source
