"""Shared pytest fixtures for Docker end-to-end tests."""

import os
import sys

import pytest

# Ensure helpers is importable regardless of how pytest was invoked
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

# WORKAROUND(clemensv/real-time-sources#1391): the json_structure SDK (editable
# 0.6.3.dev2 and published 0.7.0) wrongly rejects `unit`/`ucumUnit` on a
# nullable-numeric type union (e.g. {"type": ["double","null"], "unit": "meter"}),
# the repo's standard shape for an optional/explicit-null measured value used by
# 500+ fields across 54 feeders. Patch json_structure.SchemaValidator with the
# spec-faithful compat shim BEFORE helpers (or any test module) imports it, so
# every Docker E2E schema-validation call site picks up the fix uniformly. The
# shim only drops those provably-false-positive errors; `unit` on a non-numeric
# type still fails. Remove this once a fixed json-structure is released and the
# pin in tests/docker_e2e/requirements.txt is bumped. See the shim module for
# the full spec citation and the upstream-fix recommendation.
import _jsonstructure_compat as _js_compat  # noqa: E402  (captures the real base)
import json_structure as _json_structure  # noqa: E402
_json_structure.SchemaValidator = _js_compat.SchemaValidator

import helpers as _helpers  # noqa: E402


def pytest_addoption(parser):
    parser.addoption(
        "--kafka-artifacts-dir",
        action="store",
        default=None,
        help=(
            "Write Docker E2E verification artifacts to this directory, including "
            "consumed Kafka messages and container logs."
        ),
    )


def pytest_configure(config):
    _helpers.configure_kafka_artifacts_dir(config.getoption("--kafka-artifacts-dir"))


@pytest.fixture(scope='session')
def kafka(request):
    """Session-scoped Kafka fixture shared across all Docker e2e tests."""
    kf = _helpers.KafkaFixture()
    kf.start()
    request.addfinalizer(kf.stop)
    return kf
