---
name: container-and-delivery
description: Use this skill when packaging or finishing a source for merge in this repo. Covers Dockerfile patterns, CONTAINER.md authoring, Azure Container Instance templates, optional Fabric and KQL assets, EVENTS.md generation, root README updates, and repo-level validation before commit or PR.
argument-hint: Describe the source, its runtime package, required environment variables, deployment target, and whether it needs Azure ACI, Fabric, or KQL artifacts.
user-invocable: true
---

In this repo, a source is not done when the Python bridge runs locally. It is done when it is packaged, documented, and testable like the rest of the catalog.

Minimum delivery set for a mergeable source:

- `Dockerfile`
- `CONTAINER.md`
- `EVENTS.md`
- source-local tests
- root `README.md` entry if the source is new

Common additional delivery assets:

- `azure-template.json`
- `generate-template.ps1`
- `kql/<source>.kql`
- `fabric/README.md`

Dockerfile guidance:

- Follow the existing source folders rather than inventing a new image pattern.
- Use a slim Python base unless the source needs something else.
- Set OCI labels for source, title, description, documentation, and license.
- Point the documentation label at the source `CONTAINER.md` file in the repo.
- Ensure the container starts the bridge directly and relies on environment variables for configuration.

`CONTAINER.md` should cover:

- What the upstream source is and why it matters.
- What the bridge emits.
- That events are CloudEvents and where `EVENTS.md` lives.
- Required and optional environment variables.
- `docker pull` and `docker run` examples.
- Kafka broker usage.
- Azure Event Hubs and Fabric Event Streams usage through connection strings.
- Azure Container Instance deployment, usually with `az deployment group create --template-file azure-template.json`.
- Database and analytics follow-on guidance when relevant, often pointing at `DATABASE.md`, `kql/`, or `fabric/` assets.

Azure and Fabric conventions:

- If the source should be deployable to Azure Container Instances, add or update `azure-template.json`.
- If the source has richer Fabric guidance, mirror the pattern used by `kystverket-ais/fabric/README.md`.
- If the source feeds Eventhouse or ADX, add KQL assets under `kql/`.

Documentation workflow:

1. Keep `README.md` focused on the source, local usage, configuration, and behavior.
2. Keep `CONTAINER.md` focused on packaging and deployment.
3. Generate `EVENTS.md` from xreg instead of hand-writing schema docs.
4. If the source is new, add it to the root catalog in `README.md`.

Validation before commit:

- Run the source-local test suite.
- Build the Docker image.
- If the source should participate in the shared Docker tests, make sure it works with the plain Kafka connection-string flow used by `tests/docker_e2e/test_docker_kafka_flow.py`.
- Ensure no secrets are committed. Credentials belong in env vars or deployment parameters only.
- Make sure generated producer code, runtime wrapper code, and docs all describe the same subject and key behavior.

Good delivery references:

- Azure template plus container docs: `chmi-hydro`, `hubeau-hydrometrie`, `pegelonline`, `uk-ea-flood-monitoring`
- Fabric-focused example: `kystverket-ais/fabric/README.md`
- Events doc generation script: `tools/generate-events-md.ps1`
- Repo-wide container build behavior: `.github/workflows/build_containers.yml`

Avoid these mistakes:

- Shipping a new source without container docs.
- Leaving `EVENTS.md` stale after changing xreg.
- Adding a Dockerfile that does not match the env var contract described in the docs.
- Forgetting to expose the source through the root `README.md` catalog when it is a new addition.