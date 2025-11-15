# NOAA Tests

This directory contains the test suite for the NOAA data poller.

## Test Structure

- `test_noaa_unit.py` - Unit tests for NOAA data poller components
- `test_noaa_integration.py` - Integration tests with mocked external services
- `test_noaa_e2e.py` - End-to-end tests against actual NOAA API endpoints
- `test_cloudevents_config.py` - CloudEvents structure and serialization tests

## Running Tests

Run all tests:
```bash
poetry run pytest tests/
```

Run only unit tests:
```bash
poetry run pytest tests/ -m unit
```

Run only integration tests:
```bash
poetry run pytest tests/ -m integration
```

Run end-to-end tests (hits real NOAA API):
```bash
poetry run pytest tests/test_noaa_e2e.py -v -m e2e
```

Skip end-to-end tests (default for CI/CD):
```bash
poetry run pytest tests/ -v -m "not e2e"
```

Run with coverage:
```bash
poetry run pytest tests/ --cov=noaa --cov-report=html
```

## Test Requirements

The tests use:
- pytest for test framework
- pytest-cov for coverage reporting
- requests-mock for mocking HTTP requests
- testcontainers for integration testing (optional)
