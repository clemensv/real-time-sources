# USGS Instantaneous Values Tests

This directory contains tests for the USGS Instantaneous Values data poller.

## Test Categories

### Unit Tests (`test_usgs_unit.py`)
- Test initialization and configuration
- Test parameter mapping
- Test timezone conversion
- Test data structure creation
- **Run with:** `poetry run pytest tests/test_usgs_unit.py -v`

### Integration Tests (`test_usgs_integration.py`)
- Test with mocked USGS API responses
- Test error handling
- Test timeout scenarios
- Test data parsing
- **Run with:** `poetry run pytest tests/test_usgs_integration.py -v`

### End-to-End Tests (`test_usgs_e2e.py`)
- Test against real USGS Instantaneous Values Service
- Test real site data retrieval
- **Run with:** `poetry run pytest tests/test_usgs_e2e.py -v`
- **Skip with:** `poetry run pytest -m "not e2e"`

## Running Tests

```bash
# Run all tests except E2E
poetry run pytest -v -m "not e2e"

# Run only unit tests
poetry run pytest -v -m unit

# Run only integration tests
poetry run pytest -v -m integration

# Run all tests including E2E
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=usgs_iv --cov-report=html
```
