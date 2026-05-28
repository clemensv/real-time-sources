import json
from pathlib import Path


def test_nws_alerts_fabric_notebook_exists_and_has_required_parameters():
    repo_root = Path(__file__).resolve().parents[1]
    notebook_path = repo_root / "feeders" / "nws-alerts" / "notebook" / "nws-alerts-feed.ipynb"

    assert notebook_path.exists(), "Missing Fabric notebook artifact"

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    assert notebook.get("nbformat") == 4

    cells = notebook.get("cells", [])
    assert len(cells) >= 4

    parameter_cells = [
        cell
        for cell in cells
        if "parameters" in (cell.get("metadata", {}).get("tags") or [])
    ]
    assert parameter_cells, "Notebook must include a tagged parameters cell"

    params_source = "".join(parameter_cells[0].get("source", []))
    for key in ["EVENTSTREAM_NAME", "STATE_FILE", "POLLING_INTERVAL", "ONCE_MODE", "WORKSPACE_ID"]:
        assert key in params_source
    assert "CONNECTION_STRING" not in params_source
