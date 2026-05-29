# Delivery Checklist

## Minimum Delivery Set

- `Dockerfile`
- `CONTAINER.md`
- `EVENTS.md`
- `kql/<source>.kql` — generated from the xreg via `tools/generate-kql-from-xreg.ps1 -Qualified`; **mandatory**, reviewed by the KQL Optimizer agent. Without it, deployed Fabric KQL databases skip the schema step and have no typed tables.
- `kql/create-kql-script.ps1` — thin wrapper that re-runs the generator after xreg changes.
- source-local tests
- root `README.md` entry if the source is new
- `catalog.json` entry includes a `kql` reference to the generated script.

## Common Additional Assets

- `azure-template.json` (Kafka, BYO connection string)
- `azure-template-with-eventhub.json` (Kafka, provisions Event Hubs namespace)
- `azure-template-with-servicebus.json` (AMQP, provisions Service Bus namespace)
- `azure-template-amqp.json` (AMQP, BYO broker)
- `azure-template-mqtt.json` (MQTT, BYO broker)
- `azure-template-with-eventgrid-mqtt.json` (MQTT, provisions Event Grid namespace)
- `generate-template.ps1`
- `fabric/README.md`

## ARM Template Correctness — BLOCKING

Every `azure-template-*.json` shipped with the source is a blocking
review item. The most common silent regression in this repo is an
ARM template whose `resources` array is empty — the deploy button
succeeds and creates an empty resource group, then the user has no
recourse. Every PR that adds or modifies a feeder MUST pass these
checks, and the reviewer MUST paste evidence into the PR body:

- [ ] **Every shipped `azure-template-*.json` has a non-empty
      `resources` array.** Quick check:
      `(Get-Content <tpl> -Raw | ConvertFrom-Json).resources.Count -gt 0`.
      Repo-wide static audit:
      `pwsh tools/validate-arm-templates.ps1 -RepoRoot .` enforces
      six checks per template (empty-resources, image suffix per
      transport, storage+share when the bridge reads a `*_STATE_FILE`
      env var, non-stub `metadata.description`, env-var coverage,
      and CONTAINER.md ↔ ARM symmetry). Blockers MUST be zero;
      warnings triaged in the PR body.
- [ ] **Every required feeder env var is exposed as an ARM
      parameter** with appropriate `type` (`string` or
      `securestring`), `defaultValue` where one applies, and a real
      `metadata.description` derived from CONTAINER.md or runtime
      argparse help text (not a placeholder phrase). The parameter
      must be wired into the container's `environmentVariables`
      array. Missing required-secret parameters block merge.
- [ ] **CONTAINER.md ↔ ARM parameter symmetry.** Every
      feeder-prefixed env var the template exposes must also appear
      in `CONTAINER.md`'s env-var table. The static auditor enforces
      this; drift between the two artifacts is the default once two
      authors can edit them independently.
- [ ] **Image suffix matches transport family.** kafka + eventhub
      use the base image (`:latest` no suffix), servicebus + amqp
      use `-amqp:latest`, mqtt + eventgrid-mqtt use `-mqtt:latest`.
      The suffix may live in the resource `image` expression OR in
      the `imageName` parameter `defaultValue` — the static auditor
      resolves both forms. Mismatches deploy the wrong container
      variant.
- [ ] **Generator regeneration produces no diff.** Re-run
      `python tools/generate-arm-templates.py --filter <slug>` and
      confirm `git diff -- feeders/<slug>/azure-template*.json` is
      empty. Non-empty diff means a reviewer hand-edited a
      generated template; move the change into the generator or
      `fleet-catalog.json` and re-emit.
- [ ] **Identity + role assignments correct** where Entra ID is the
      auth path (UAMI + the right
      `Microsoft.Authorization/roleAssignments` per resource scope).
- [ ] **Live deploy verification.** Run
      `pwsh tools/verify-arm-template.ps1 -FeederSlug <slug>
      -Variant <variant>` for every variant the PR touches. The
      script creates a real RG, deploys the template, validates
      data flow on the provisioned broker (or container-group
      shape for BYO-broker variants), and tears the RG down in
      `finally`. Paste the PASS line **with ISO-8601 timestamp**
      into the PR body. A PR that has not been live-verified
      against Azure within the last 30 days is not mergeable.
- [ ] **KQL update-policy apply check** when `kql/<slug>.kql`
      exists and the source ships no Fabric notebook (notebook
      sources exercise this automatically). Apply the script to a
      scratch Eventhouse — a script that compiles locally can still
      fail when applied (table missing, syntax variant the Kusto
      engine rejects, ordering dependency on an update-policy that
      hasn't materialized).

Run the regenerator (`python tools/generate-arm-templates.py`)
rather than hand-editing per-feeder templates when the change is a
parameter / env-var addition that applies fleet-wide.

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

- **Shipping an `azure-template-*.json` whose `resources` array is empty (`"resources": []`).** This is the most common silent regression in this repo. The deploy button succeeds, the user gets an empty resource group, and the failure mode is invisible from the portal. Audit before merge with `pwsh tools/validate-arm-templates.ps1 -RepoRoot .` and live-deploy-test with `pwsh tools/verify-arm-template.ps1 -FeederSlug <slug> -Variant <variant>`. Never accept a "placeholder template" for a transport variant that has a corresponding Dockerfile — regenerate from the aisstream canonical via `python tools/generate-arm-templates.py`.
- **Required feeder env vars not exposed as ARM parameters.** A bridge that requires `<FEEDER>_API_KEY` or per-feeder filter env vars (regions, categories, sort orders) but does not expose them as ARM parameters with `metadata.description` forces every user to fork the template. Mine env vars from CONTAINER.md and runtime argparse; expose every user-tunable one.
- **Wrong image suffix per transport variant.** `azure-template-with-servicebus.json` referencing the base `:latest` image (instead of `-amqp:latest`) deploys the Kafka container against a Service Bus broker. Audit suffix matches the variant before merging.
- Shipping a new source without container docs.
- Leaving `EVENTS.md` stale after changing xreg.
- **Shipping a source without `kql/<source>.kql`.** The Fabric deployers print "No KQL script — database schema step will be skipped" and the deployed database has only the auto-provisioned `_cloudevents_dispatch` table; every typed-table consumer (Eventhouse Maps, Activator rules, materialized `*Latest` views, KQL dashboards) is broken. Generate with `tools/generate-kql-from-xreg.ps1 -Qualified`.
- **Forgetting to add the `kql` key to the source's `catalog.json` entry.** Even when the file is committed, the gh-pages portal won't surface the schema until the catalog reference exists.
- Adding a Dockerfile that does not match the env var contract described in the docs.
- Forgetting to expose the source through the root `README.md` catalog when it is a new addition.
- **Not adding `avro` to `pyproject.toml`.** The generated `_data` sub-package imports `avro` at runtime. Without it, the container crashes immediately with `ModuleNotFoundError: No module named 'avro'`.
- **Not adding the source to the Docker E2E CI workflow matrix.** Test class exists in `test_docker_kafka_flow.py` but the CI matrix in `.github/workflows/docker_e2e.yml` (or equivalent) must also include the source name. Without it, the E2E test never runs in CI.
- **E2E CI workflow path triggers missing xreg files.** If the workflow only triggers on `Dockerfile` and `pyproject.toml` changes, xreg contract changes won't trigger E2E validation. Add `**/xreg/*.xreg.json` and bridge source `**/<source>/<source>.py` to the workflow path filters.
- **Not regenerating producers after schema field renames.** The generated data classes and producer methods reflect the old field names until `generate_producer.ps1` is rerun. The bridge will crash with `AttributeError` or `TypeError` at runtime.