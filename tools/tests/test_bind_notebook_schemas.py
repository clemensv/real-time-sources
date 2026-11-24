import ast
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "bind_notebook_schemas", ROOT / "tools" / "deploy-fabric" / "bind_notebook_schemas.py")
assert SPEC and SPEC.loader
binder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(binder)


def notebook():
    return json.loads((ROOT / "feeders" / "pegelonline" / "notebook" / "pegelonline-feed.ipynb")
                      .read_text(encoding="utf-8"))


def mapping(nb):
    namespace = {}
    exec("".join(nb["cells"][1]["source"]), namespace)
    return {item["source_uri"]: f"https://catalog.example/schemas/{index}/versions/1"
            for index, item in enumerate(namespace["SCHEMA_BINDINGS"].values())}


@pytest.mark.parametrize("encoding", ["json", "avro"])
def test_injection_is_literal_idempotent_and_preserves_input(encoding):
    original = notebook()
    before = copy.deepcopy(original)
    overrides = mapping(original)
    overrides[next(iter(overrides))] += "'quoted"
    actual = binder.bind_notebook(original, overrides, encoding)
    assert original == before
    assert binder.bind_notebook(actual, overrides, encoding) == actual
    namespace = {}
    exec("".join(actual["cells"][3]["source"]), namespace)
    assert namespace["dataschema_overrides"] == overrides
    assert namespace["deployment_payload_encoding"] == encoding
    for index in (0, 1, 2, 4):
        assert actual["cells"][index] == before["cells"][index]
    for cell in actual["cells"]:
        if cell["cell_type"] == "code":
            ast.parse("".join(cell["source"]))


@pytest.mark.parametrize("failure", ["missing", "extra", "url", "duplicate"])
def test_invalid_deployment_mapping_rejected(failure):
    nb = notebook()
    overrides = mapping(nb)
    if failure == "missing":
        overrides.pop(next(iter(overrides)))
    elif failure == "extra":
        overrides["xreg://./other"] = "https://catalog.example/schemas/other/versions/1"
    elif failure == "url":
        overrides[next(iter(overrides))] = "https://user:password@catalog.example/schemas/s/versions/1"
    else:
        nb["cells"].insert(3, copy.deepcopy(nb["cells"][3]))
    with pytest.raises(ValueError):
        binder.bind_notebook(nb, overrides, "json")


def test_invalid_payload_encoding_rejected():
    nb = notebook()
    with pytest.raises(ValueError, match="payload encoding"):
        binder.bind_notebook(nb, mapping(nb), "invalid")
