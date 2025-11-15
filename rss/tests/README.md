# RSS Bridge Test Suite

This directory contains comprehensive tests for the RSS Bridge project.

## Test Structure

The test suite is organized into three categories:

### 1. Unit Tests (`test_rssbridge_unit.py`)

Tests individual functions and classes without external dependencies:
- Connection string parsing (Event Hubs format)
- Feed URL extraction from OPML
- State file management
- Feed metadata extraction
- Helper functions

**Run unit tests only:**

```bash
pytest -m unit
```

### 2. Integration Tests (`test_rssbridge_integration.py`)

Tests interactions with external services using mocked responses:
- RSS/Atom feed parsing with mocked HTTP responses
- Feed discovery from web pages
- OPML file processing
- Error handling for malformed feeds
- Producer client integration

**Run integration tests only:**

```bash
pytest -m integration
```

### 3. End-to-End Tests (future)

Tests against real RSS/Atom feeds.

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
pytest --cov=rssbridge --cov-report=html
```

**Run specific test file:**

```bash
pytest tests/test_rssbridge_unit.py -v
```

## Test Requirements

The following test dependencies are required:
- `pytest` >= 8.3.3
- `pytest-cov` >= 5.0.0
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
