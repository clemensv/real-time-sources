# Defra AURN tests

This source keeps its fast checks in `test_defra_aurn_unit.py`.

- `unit` tests cover parsing, timestamp conversion, pagination, and de-duplication.
- The tests use fake sessions and fake producer wrappers, so they do not call Kafka or the live Defra API.
