# PegelOnline Tests

This directory contains comprehensive tests for the PegelOnline data poller that fetches water level data from the German WSV PegelOnline API.

## Test Structure

### Unit Tests (`test_pegelonline_unit.py`)
Tests that validate core functionality without external dependencies:
- PegelOnlineAPI initialization
- Connection string parsing for Event Hubs/Kafka
- URL construction and ETag management
- Skip URL list management
- Helper functions and utilities

**Run unit tests only:**
```bash
poetry run pytest -m unit
```

### Integration Tests (`test_pegelonline_integration.py`)
Tests that validate component interactions with mocked external services:
- API request/response handling with requests-mock
- Station listing endpoint
- Water level measurement endpoints
- ETag caching behavior
- Error handling (HTTP errors, timeouts, invalid responses)
- CloudEvents formatting and Kafka producer interaction

**Run integration tests only:**
```bash
poetry run pytest -m integration
```

### End-to-End Tests (`test_pegelonline_e2e.py`)
Tests that validate against the real PegelOnline API:
- Fetching real station data from WSV API
- Retrieving actual water level measurements
- Validating API response structure
- Testing multiple German rivers (Rhine, Elbe, Danube, etc.)
- Verifying data freshness and timestamps

**Run E2E tests only:**
```bash
poetry run pytest -m e2e
```

## Running Tests

**Run all tests:**
```bash
poetry run pytest
```

**Run with coverage:**
```bash
poetry run pytest --cov=pegelonline --cov-report=html
```

**Run specific test file:**
```bash
poetry run pytest tests/test_pegelonline_unit.py -v
```

**Run tests matching a pattern:**
```bash
poetry run pytest -k "station" -v
```

## Test Data

The tests use:
- Mock data for unit and integration tests
- Real PegelOnline API endpoints for E2E tests
- Sample station UUIDs from actual German waterways

## Coverage Goals

- Minimum 70% statement coverage
- All critical paths tested (initialization, API calls, error handling)
- Edge cases covered (missing data, invalid responses, network errors)
