import json
from pathlib import Path


def test_xceed_fabric_notebook_exists_and_has_required_contract():
    repo_root = Path(__file__).resolve().parents[1]
    notebook_path = repo_root / "feeders" / "xceed" / "notebook" / "xceed-feed.ipynb"
    assert notebook_path.exists(), "Expected xceed Fabric notebook at feeders/xceed/notebook/xceed-feed.ipynb"

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    assert len(cells) >= 4

    parameters_cell = cells[1]
    assert parameters_cell.get("cell_type") == "code"
    param_source = "".join(parameters_cell.get("source", []))
    for name in ["EVENTSTREAM_NAME", "STATE_FILE", "POLLING_INTERVAL", "ONCE_MODE", "WORKSPACE_ID"]:
        assert name in param_source
    assert "CONNECTION_STRING" not in param_source

    run_source = "".join(cells[-1].get("source", []))
    assert "from xceed import xceed as feeder" in run_source
    assert "sys.argv = ['xceed', 'feed']" in run_source
    assert "/lakehouse/default/Files/feeder-state/xceed/last-run.log" in run_source
