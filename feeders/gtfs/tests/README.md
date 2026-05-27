# GTFS Bridge Test Suite

This directory contains comprehensive tests for the GTFS Bridge project.

## Test Structure

The test suite is organized into three categories:

### 1. Unit Tests (`test_gtfs_bridge_unit.py`)
Tests individual functions and classes without external dependencies:
- Connection string parsing (Event Hubs format)
- URL management and caching
- Hash calculation for schedule files
- Helper functions for data processing
- Configuration validation

**Run unit tests only:**
```bash
pytest -m unit
```

### 2. Integration Tests (`test_gtfs_bridge_integration.py`)
Tests interactions with external services using mocked responses:
- GTFS-RT feed polling with mocked HTTP responses
- Schedule file fetching with ETag support
- Error handling for API failures
- Producer client integration

**Run integration tests only:**
```bash
pytest -m integration
```

### 3. End-to-End Tests (future)
Tests against real GTFS-RT feeds from transit agencies.

## Running Tests

**Run all tests except E2E:**
```bash
pytest -m "not e2e"
```

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=gtfs_rt_bridge --cov-report=html
```

**Run specific test file:**
```bash
pytest tests/test_gtfs_bridge_unit.py -v
```

## Test Requirements

The following test dependencies are required:
- `pytest` >= 8.3.3
- `pytest-cov` >= 6.0.0
- `requests-mock` >= 1.12.1

Install with: `poetry install`

## Writing Tests

Follow these guidelines when adding new tests:

1. **Mark tests appropriately:**
   - `@pytest.mark.unit` for unit tests
   - `@pytest.mark.integration` for integration tests
   - `@pytest.mark.e2e` for end-to-end tests

2. **Use descriptive names:**
   - Test class: `TestConnectionStringParsing`
   - Test method: `test_parse_connection_string_with_all_components`

3. **Keep tests focused:**
   - Each test should verify one specific behavior
   - Use fixtures for common setup

4. **Mock external dependencies:**
   - Use `requests_mock` for HTTP calls
   - Use unittest.mock for other external dependencies
