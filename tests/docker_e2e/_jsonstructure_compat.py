"""JSON Structure SDK compatibility shim for the Docker E2E schema validation.

WORKAROUND(clemensv/real-time-sources#1391): the ``json_structure`` SDK
(reproduced on the editable 0.6.3.dev2 build *and* the published 0.7.0 wheel
that CI installs via ``json-structure>=0.6.1``) rejects the ``unit`` and
``ucumUnit`` keywords on a nullable-numeric type union such as
``{"type": ["double", "null"], "unit": "meter"}``. That pattern is the repo's
standard shape for an optional/explicit-null measured value (548 fields across
54 feeders, e.g. gbfs-bikeshare ``current_range_meters``), and it is
spec-defensible:

* JSON Structure Units draft, "The ``unit`` Keyword": *"The ``unit`` keyword
  MAY be used as an annotation on any schema element whose underlying type is
  numeric."* A ``["double","null"]`` union's underlying (value-bearing) type is
  ``double``; the ``"null"`` member only encodes explicit-null on the wire.
* The normative Units meta-schema (``meta/extended/v0`` ``UnitsPropertyAddIn``)
  ``$extends`` *every* ``Property`` and adds ``unit: string`` with **no** numeric
  gate at all.
* The SDK's own ``minimum``/``maximum`` gate silently tolerates unions, and its
  ``unit`` numeric set wrongly omits ``int8/uint8/int16/uint16/float8``. The
  JSON Structure Expert ruled the validator rule a bug, not a correct constraint
  (see issue #1391).

The permanent fix is a ~6-line change in the SDK's ``_check_units_keywords`` and
``_check_ucum_unit`` to use the full numeric set and accept a union whose
non-``null`` members are all numeric. Filed upstream with a verified reproducer
and the proposed fix as json-structure/sdk#175. Until a fixed ``json-structure`` is
released and the pin in ``tests/docker_e2e/requirements.txt`` is bumped, this
shim post-filters **only** those provably-spec-false-positive errors and leaves
every other validation error untouched (``unit`` on a non-numeric type such as
``["string","null"]`` still fails — see the negative control in
``test_helpers.py``).

Remove this shim and import ``SchemaValidator`` directly from ``json_structure``
once the upstream fix (json-structure/sdk#175) ships.
"""
from __future__ import annotations

from json_structure import InstanceValidator  # re-exported unchanged
from json_structure import SchemaValidator as _BaseSchemaValidator
from json_structure import error_codes as _ErrorCodes

__all__ = ["InstanceValidator", "SchemaValidator"]

# Complete numeric primitive set per JSON Structure Core "Extended Primitive
# Types". The SDK's unit gate uses an under-inclusive subset; the SDK's own
# minimum/maximum gate uses this complete set.
_NUMERIC_TYPES = frozenset({
    "number", "integer", "float", "double", "decimal",
    "int8", "uint8", "int16", "uint16", "int32", "uint32",
    "int64", "uint64", "int128", "uint128", "float8",
})

# Keywords the SDK numeric-gates (and only these) that this shim relaxes.
_GATED_KEYWORDS = ("unit", "ucumUnit")

_TYPE_MISMATCH = _ErrorCodes.SCHEMA_CONSTRAINT_TYPE_MISMATCH


def _unit_eligible(type_value) -> bool:
    """True when ``type_value`` is a numeric primitive or a union whose
    non-``null`` members are all numeric primitives."""
    if isinstance(type_value, str):
        return type_value in _NUMERIC_TYPES
    if isinstance(type_value, list):
        non_null = [m for m in type_value if m != "null"]
        return bool(non_null) and all(
            isinstance(m, str) and m in _NUMERIC_TYPES for m in non_null
        )
    return False


def _resolve_pointer(doc, pointer: str):
    """Resolve a ``#/a/b/c`` JSON pointer (dict keys only, as JSON Structure
    schemas use) against ``doc``. Returns ``None`` if it cannot be resolved."""
    if not pointer or not pointer.startswith("#"):
        return None
    node = doc
    for raw in pointer[1:].split("/"):
        if raw == "":
            continue
        key = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return None
    return node


def _is_unit_false_positive(error, doc) -> bool:
    """True iff ``error`` is the SDK's spec-false-positive rejection of
    ``unit``/``ucumUnit`` on an eligible-numeric (incl. nullable-union) type."""
    if getattr(error, "code", None) != _TYPE_MISMATCH:
        return False
    path = getattr(error, "path", "") or ""
    for kw in _GATED_KEYWORDS:
        suffix = "/" + kw
        if path.endswith(suffix):
            field_node = _resolve_pointer(doc, path[: -len(suffix)])
            if isinstance(field_node, dict) and _unit_eligible(field_node.get("type")):
                return True
    return False


class SchemaValidator(_BaseSchemaValidator):
    """``json_structure.SchemaValidator`` with the #1391 unit-on-nullable-numeric
    false positives filtered out. Behaviour is otherwise identical."""

    def validate(self, doc, source_text=None):  # type: ignore[override]
        errors = super().validate(doc, source_text)
        if not errors:
            return errors
        return [e for e in errors if not _is_unit_false_positive(e, doc)]
