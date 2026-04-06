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