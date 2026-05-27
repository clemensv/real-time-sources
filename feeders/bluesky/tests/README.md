# Bluesky Firehose Producer - Integration Tests

This directory contains integration tests for the Bluesky AT Protocol firehose producer.

## Test Structure

- `test_bluesky_integration.py` - Full integration tests using Kafka test containers

## Running Tests

### Prerequisites

- Docker must be running (required for Kafka test containers)
- Poetry dependencies installed: `poetry install`

### Run All Tests

```powershell
poetry run pytest
```

### Run with Coverage

```powershell
poetry run pytest --cov=bluesky --cov-report=html --cov-report=term
```

### Run Specific Test

```powershell
poetry run pytest tests/test_bluesky_integration.py::test_bluesky_firehose_post_event
```

### Run with Verbose Output

```powershell
poetry run pytest -v -s
```

## Test Coverage

The integration tests cover:

1. **Post Event Processing** - Verifies posts are parsed from the firehose and sent to Kafka with CloudEvents envelope
2. **Like Event Processing** - Verifies likes are processed correctly
3. **Cursor Persistence** - Tests that cursor position is saved and can be resumed
4. **Event Sampling** - Tests that sampling rate filters events appropriately
5. **Connection String Parsing** - Tests Azure Event Hubs connection string parsing

## Test Architecture

### Kafka Test Container

Tests use `testcontainers-python` to spin up a real Kafka broker in Docker. This provides:

- Authentic Kafka behavior (no mocks for broker logic)
- Topic creation and management
- Producer/consumer verification
- CloudEvents serialization testing

### Mocking Strategy

The tests mock:

- **WebSocket connections** - Simulates firehose messages without connecting to Bluesky
- **CAR file parsing** - Returns pre-defined record structures
- **AT Protocol components** - Mocks AtUri and other protocol helpers

This approach tests the full producer logic while isolating from external dependencies.

## Troubleshooting

### Docker Issues

If tests fail with Docker connection errors:

```powershell
# Check Docker is running
docker ps

# On Windows, ensure Docker Desktop is started
```

### Port Conflicts

If Kafka container fails to start due to port conflicts:

```powershell
# Check what's using port 9093
netstat -ano | findstr :9093

# Stop conflicting processes or restart Docker
```

### Slow Tests

First test run may be slow as Docker images are downloaded. Subsequent runs are faster.

## CI/CD Integration

These tests are suitable for CI/CD pipelines that support Docker (GitHub Actions, Azure DevOps, etc.).

Example GitHub Actions:

```yaml
- name: Run integration tests
  run: |
    poetry install
    poetry run pytest --cov=bluesky --cov-report=xml
```
