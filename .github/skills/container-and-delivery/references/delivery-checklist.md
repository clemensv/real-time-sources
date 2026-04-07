# Delivery Checklist

## Minimum Delivery Set

- `Dockerfile`
- `CONTAINER.md`
- `EVENTS.md`
- source-local tests
- root `README.md` entry if the source is new

## Common Additional Assets

- `azure-template.json`
- `generate-template.ps1`
- `kql/<source>.kql`
- `fabric/README.md`

## Dockerfile Checklist

- Follow an existing source folder pattern instead of inventing a new image layout.
- Use a slim Python base unless the source needs something else.
- Set OCI labels for source, title, description, documentation, and license.
- Point the documentation label at the source `CONTAINER.md` file.
- Ensure the container starts the bridge directly and relies on environment variables for configuration.

## CONTAINER.md Checklist

- Explain the upstream source and what the bridge emits.
- State that events are CloudEvents and point to `EVENTS.md`.
- Document required and optional environment variables.
- Include `docker pull` and `docker run` examples.
- Cover Kafka broker usage plus Event Hubs and Fabric connection-string usage.
- Cover Azure Container Instance deployment when applicable.
- Add database or analytics follow-on guidance when relevant.

## Validation Before Commit

- Run the source-local test suite.
- Build the Docker image.
- If the source should participate in the shared Docker tests, make sure it works with the plain Kafka connection-string flow used by `tests/docker_e2e/test_docker_kafka_flow.py`.
- **Ensure `avro` is listed in `pyproject.toml` dependencies.** The generated data classes depend on the `avro` package. Missing it causes `ModuleNotFoundError` at container startup.
- **Verify generated method names match bridge calls.** After regeneration, generated method names derive from xreg message names (e.g. `send_water_level_observation`). Run a quick grep to confirm the bridge calls the exact generated method names. Stale calls cause `AttributeError` at runtime.
- **Install generated sub-packages sequentially if pip resolution conflicts.** Install data first, then kafka_producer, then the main package: `pip install <source>_producer/<source>_producer_data && pip install <source>_producer/<source>_producer_kafka_producer && pip install -e .`
- Ensure no secrets are committed.
- Make sure generated producer code, runtime wrapper code, and docs all describe the same subject and key behavior.

## Useful Repo References

- Azure template plus container docs: `chmi-hydro`, `hubeau-hydrometrie`, `pegelonline`, `uk-ea-flood-monitoring`
- Fabric-focused example: `kystverket-ais/fabric/README.md`
- Events doc generation script: `tools/generate-events-md.ps1`
- Repo-wide container build behavior: `.github/workflows/build_containers.yml`

## Common Mistakes

- Shipping a new source without container docs.
- Leaving `EVENTS.md` stale after changing xreg.
- Adding a Dockerfile that does not match the env var contract described in the docs.
- Forgetting to expose the source through the root `README.md` catalog when it is a new addition.
- **Not adding `avro` to `pyproject.toml`.** The generated `_data` sub-package imports `avro` at runtime. Without it, the container crashes immediately with `ModuleNotFoundError: No module named 'avro'`.
- **Not adding the source to the Docker E2E CI workflow matrix.** Test class exists in `test_docker_kafka_flow.py` but the CI matrix in `.github/workflows/docker_e2e.yml` (or equivalent) must also include the source name. Without it, the E2E test never runs in CI.
- **E2E CI workflow path triggers missing xreg files.** If the workflow only triggers on `Dockerfile` and `pyproject.toml` changes, xreg contract changes won't trigger E2E validation. Add `**/xreg/*.xreg.json` and bridge source `**/<source>/<source>.py` to the workflow path filters.
- **Not regenerating producers after schema field renames.** The generated data classes and producer methods reflect the old field names until `generate_producer.ps1` is rerun. The bridge will crash with `AttributeError` or `TypeError` at runtime.