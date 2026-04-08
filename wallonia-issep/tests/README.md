# Tests

Unit and integration tests for the Wallonia ISSeP air quality bridge.

## Running tests

```powershell
cd wallonia-issep
pip install -e wallonia_issep_producer\wallonia_issep_producer_data
pip install -e wallonia_issep_producer\wallonia_issep_producer_kafka_producer
pip install -e .
python -m pytest tests -m "unit or integration" --no-header -q
```
