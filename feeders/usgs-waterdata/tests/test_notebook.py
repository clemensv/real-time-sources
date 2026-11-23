import ast
import json
from pathlib import Path
from types import SimpleNamespace


def test_notebook_selection_parameters_override_deployer_environment():
    notebook = json.loads((Path(__file__).parents[1] / "notebook/usgs-waterdata-feed.ipynb").read_text(encoding="utf-8"))
    scope = {}
    exec("".join(notebook["cells"][1]["source"]), scope)
    scope.update(USGS_WATERDATA_SITES="USGS-12345678", USGS_WATERDATA_PARAMETERS="00065")
    environment = {"USGS_WATERDATA_SITES": "USGS-00000000", "USGS_WATERDATA_PARAMETERS": "00010"}
    scope.update(os=SimpleNamespace(environ=environment), _connection=lambda: "test-connection")
    run = ast.parse("".join(notebook["cells"][3]["source"]))
    assignments = [
        node for node in ast.walk(run)
        if isinstance(node, ast.Assign) and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Subscript)
        and ast.unparse(node.targets[0].value) == "os.environ"
    ]
    exec(compile(ast.Module(body=assignments, type_ignores=[]), "notebook-environment", "exec"), scope)
    assert environment["USGS_WATERDATA_SITES"] == "USGS-12345678"
    assert environment["USGS_WATERDATA_PARAMETERS"] == "00065"
