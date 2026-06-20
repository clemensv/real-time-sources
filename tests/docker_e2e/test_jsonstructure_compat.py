"""Regression tests for the JSON Structure SDK compatibility shim.

WORKAROUND(clemensv/real-time-sources#1391): these tests guard the shim that
accepts `unit`/`ucumUnit` on nullable-numeric type unions (the repo's standard
optional/explicit-null measured-value shape) while keeping genuine
`unit`-on-non-numeric rejections. They are pure schema-validation tests and do
not require Docker. Delete this module when the upstream json-structure fix
ships and the shim is removed.
"""
import json
import os

import json_structure

from _jsonstructure_compat import SchemaValidator

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _doc(props):
    return {
        "$schema": "https://json-structure.org/meta/extended/v0/#",
        "$id": "https://example.com/test/UnitShim",
        "$uses": ["JSONStructureUnits"],
        "name": "UnitShim",
        "type": "object",
        "properties": props,
    }


def test_conftest_patches_sdk_validator():
    """The conftest monkeypatch must redirect the SDK's SchemaValidator to the
    shim so every Docker E2E call site is covered transparently."""
    assert json_structure.SchemaValidator is SchemaValidator


def test_unit_on_nullable_numeric_union_passes():
    schema = _doc({
        "current_range_meters": {"type": ["double", "null"], "unit": "meter"},
        "lat": {"type": ["double", "null"], "unit": "degree"},
    })
    errors = SchemaValidator(extended=True).validate(schema)
    assert errors == [], [str(e) for e in errors]


def test_unit_on_bare_numeric_still_passes():
    schema = _doc({"value": {"type": "double", "unit": "cm"}})
    assert SchemaValidator(extended=True).validate(schema) == []


def test_ucum_unit_on_nullable_numeric_union_passes():
    schema = _doc({"v": {"type": ["double", "null"], "ucumUnit": "m/s2"}})
    assert SchemaValidator(extended=True).validate(schema) == []


def test_unit_on_nullable_NONnumeric_union_still_fails():
    """Negative control: the shim must NOT mask a genuine mistake."""
    schema = _doc({"bad": {"type": ["string", "null"], "unit": "meter"}})
    errors = SchemaValidator(extended=True).validate(schema)
    assert any(
        getattr(e, "code", None) == "SCHEMA_CONSTRAINT_TYPE_MISMATCH"
        and getattr(e, "path", "").endswith("/unit")
        for e in errors
    ), [str(e) for e in errors]


def test_real_gbfs_free_bike_status_schema_validates():
    """The real gbfs-bikeshare manifest (which uses ["double","null"] + unit on
    free-bike telemetry) must validate cleanly through the shim."""
    xreg = os.path.join(
        REPO_ROOT, "feeders", "gbfs-bikeshare", "xreg", "gbfs-bikeshare.xreg.json"
    )
    doc = json.load(open(xreg, encoding="utf-8"))
    validator = SchemaValidator(extended=True)
    checked = 0
    for sg in doc.get("schemagroups", {}).values():
        for srec in sg.get("schemas", {}).values():
            for vrec in srec.get("versions", {}).values():
                schema = vrec.get("schema")
                if isinstance(schema, dict):
                    errs = validator.validate(schema)
                    assert errs == [], [str(e) for e in errs]
                    checked += 1
    assert checked > 0
