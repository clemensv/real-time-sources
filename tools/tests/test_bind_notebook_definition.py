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


def native_fixture():
    definition, notebook = fixture()
    metadata = {"kernel_info": {"name": "synapse_pyspark"},
                "dependencies": notebook["metadata"]["dependencies"]}
    source = "# Fabric notebook source\n\n# METADATA ********************\n\n"
    source += "".join("# META " + line + "\n" for line in json.dumps(metadata, indent=2).splitlines())
    source += ("\n# PARAMETERS CELL ********************\n\n"
               "SCHEMA_BINDINGS = {'reading': {'source_uri': 'xreg://./reading'}}\n"
               "STATE_FILE = '/lakehouse/default/Files/feeder-state/example/state.json'\n"
               "\n# CELL ********************\n\n"
               "dataschema_overrides = None\n"
               "deployment_payload_encoding = None\n"
               "\n# CELL ********************\n\n"
               "assert dataschema_overrides\n"
               "# META {\"language\": \"python\", \"language_group\": \"synapse_pyspark\"}\n")
    definition["parts"][1]["path"] = "notebook-content.py"
    definition["parts"][1]["payload"] = base64.b64encode(source.encode()).decode()
    return definition, source


def test_native_definition_preserves_actual_format_metadata_and_state(binder):
    definition, source = native_fixture()
    before = copy.deepcopy(definition)
    overrides = {"xreg://./reading": "https://catalog.example/schemas/reading/versions/2"}
    bound = binder.bind_definition(definition, overrides, "avro", environment_id="synthetic-environment")
    content = base64.b64decode(bound["parts"][1]["payload"]).decode()
    assert definition == before
    assert bound["parts"][0] == before["parts"][0] and bound["parts"][2] == before["parts"][2]
    assert content.split("dataschema_overrides =")[0] == source.split("dataschema_overrides =")[0]
    assert content.split("assert dataschema_overrides")[1] == source.split("assert dataschema_overrides")[1]
    namespace = {}
    exec(content, namespace)
    assert namespace["dataschema_overrides"] == overrides
    assert namespace["deployment_payload_encoding"] == "avro"
    assert namespace["STATE_FILE"] == "/lakehouse/default/Files/feeder-state/example/state.json"
    assert binder.bind_definition(
        bound, overrides, "avro", environment_id="synthetic-environment") == bound


@pytest.mark.parametrize("literal", ["None", repr({"uri": "caf" + chr(233)})])
def test_native_binding_rejects_shared_line_without_losing_other_code(binder, literal):
    definition, source = native_fixture()
    source = source.replace(
        "dataschema_overrides = None\n", f"dataschema_overrides = {literal}; other = 1\n"
    )
    definition["parts"][1]["payload"] = base64.b64encode(source.encode()).decode()
    with pytest.raises(ValueError, match="separate statements"):
        binder.bind_definition(
            definition, {"xreg://./reading": "https://catalog.example/schemas/reading/versions/2"},
            "json", environment_id="synthetic-environment",
        )


@pytest.mark.parametrize("failure", [
    "kernel", "environment", "lakehouse", "duplicate", "mixed", "syntax", "metadata",
])
def test_native_binding_rejects_invalid_definition(binder, failure):
    definition, source = native_fixture()
    if failure == "kernel":
        source = source.replace('"synapse_pyspark"', '"python"')
    elif failure == "environment":
        source = source.replace("synthetic-environment", "different-environment")
    elif failure == "lakehouse":
        source = source.replace('"lakehouse":', '"removed_lakehouse":')
    elif failure == "duplicate":
        source += "\ndataschema_overrides = None\n"
    elif failure == "mixed":
        other = copy.deepcopy(definition["parts"][1])
        other["path"] = "notebook-content.ipynb"
        definition["parts"].append(other)
    elif failure == "syntax":
        source += "\ninvalid (\n"
    else:
        source = source.replace("# META ", "# REMOVED ")
    definition["parts"][1]["payload"] = base64.b64encode(source.encode()).decode()
    with pytest.raises((ValueError, SyntaxError)):
        binder.bind_definition(
            definition, {"xreg://./reading": "https://catalog.example/schemas/reading/versions/2"},
            "json", environment_id="synthetic-environment",
        )
