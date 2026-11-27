import base64
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def binder(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "tools" / "deploy-fabric"))
    spec = importlib.util.spec_from_file_location(
        "bind_notebook_definition", ROOT / "tools" / "deploy-fabric" / "bind_notebook_definition.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture():
    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"name": "synapse_pyspark"},
                     "dependencies": {
                         "environment": {"environmentId": "synthetic-environment", "workspaceId": "synthetic"},
                         "lakehouse": {"default_lakehouse": "synthetic-lakehouse"},
                         "kqlDatabases": [{"databaseId": "synthetic-database"}],
                     }, "unknown": {"preserve": True}},
        "cells": [
            {"cell_type": "code", "metadata": {"tags": ["parameters"]},
             "source": ["SCHEMA_BINDINGS = {'reading': {'source_uri': 'xreg://./reading'}}\n"],
             "outputs": [], "execution_count": None},
            {"cell_type": "code", "metadata": {"tags": ["deployment-dataschema-overrides"]},
             "source": ["dataschema_overrides = None\n"], "outputs": [], "execution_count": None},
        ],
    }
    return {
        "parts": [
            {"path": ".platform", "payload": "unchanged-platform", "payloadType": "InlineBase64"},
            {"path": "notebook-content.ipynb",
             "payload": base64.b64encode(json.dumps(notebook).encode()).decode(),
             "payloadType": "InlineBase64", "unknown": "retained"},
            {"path": "unknown.json", "payload": "unchanged-extra", "payloadType": "InlineBase64"},
        ], "unknown": {"outer": True},
    }, notebook


def test_binding_preserves_definition_parts_kernel_and_dependencies(binder):
    definition, notebook = fixture()
    before = copy.deepcopy(definition)
    overrides = {"xreg://./reading": "https://catalog.example/schemas/reading/versions/2"}
    result = binder.bind_definition(definition, overrides, "json", environment_id="synthetic-environment")
    assert definition == before
    assert result["parts"][0] == before["parts"][0]
    assert result["parts"][2] == before["parts"][2]
    assert result["unknown"] == before["unknown"]
    assert result["parts"][1]["unknown"] == "retained"
    bound = json.loads(base64.b64decode(result["parts"][1]["payload"]))
    assert bound["metadata"] == notebook["metadata"]
    namespace = {}
    exec("".join(bound["cells"][1]["source"]), namespace)
    assert namespace["dataschema_overrides"] == overrides
    assert binder.bind_definition(result, overrides, "json", environment_id="synthetic-environment") == result


@pytest.mark.parametrize("failure", ["kernel", "environment", "lakehouse", "database", "duplicate"])
def test_binding_rejects_lost_or_wrong_dependencies(binder, failure):
    definition, notebook = fixture()
    if failure == "kernel":
        notebook["metadata"]["kernelspec"]["name"] = "jupyter_python"
    elif failure == "environment":
        notebook["metadata"]["dependencies"]["environment"]["environmentId"] = "wrong"
    elif failure == "lakehouse":
        notebook["metadata"]["dependencies"]["lakehouse"] = {}
    elif failure == "database":
        notebook["metadata"]["dependencies"]["kqlDatabases"] = []
    else:
        definition["parts"].append(copy.deepcopy(definition["parts"][1]))
    definition["parts"][1]["payload"] = base64.b64encode(json.dumps(notebook).encode()).decode()
    with pytest.raises(ValueError):
        binder.bind_definition(
            definition, {"xreg://./reading": "https://catalog.example/schemas/reading/versions/2"},
            "json", environment_id="synthetic-environment",
        )
