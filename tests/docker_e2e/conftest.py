"""Shared pytest fixtures for Docker end-to-end tests."""

import os
import sys

import pytest

# Ensure helpers is importable regardless of how pytest was invoked
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

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
