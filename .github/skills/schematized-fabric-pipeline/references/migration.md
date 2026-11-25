# Migrate an existing feeder to schematized Fabric

Back to the [pipeline skill](../SKILL.md).

Use this runbook for one feeder or an approved fleet rollout. The merged
[Pegelonline pilot](https://github.com/clemensv/real-time-sources/pull/1747)
qualifies shared schema authoring, AMQP JSON/raw Avro, deployment-bound notebook
schema URLs and analytics-only Map wiring. It does not establish compatibility
for every feeder, transport, production schedule or in-place encoding change.
Keep all operator configuration, resource coordinates, captures and acceptance
receipts outside Git. Repository contracts and docs remain portable.

## 1. Prepare shared tooling before scheduling the fleet

Use a branch containing the merged pilot and this skill. Read the
[shared authoring guide](../../../../tools/deploy-fabric/schema-set-authoring.md)
and [notebook hosting skill](../../fabric-notebook-deployment/SKILL.md).
Check the actual implementations, not only their names.

- Use `tools\deploy-fabric\generate_schema_set.py` for xRegistry selection,
  inheritance, Avro variants and Event Schema Set definition assembly.
  Install its pinned requirements into an external tooling environment.
  Avrotize owns datatype conversion; correct upstream defects and regenerate.
- Use `tools\deploy-fabric\bind_notebook_schemas.py` only after service metadata
  has established exact versions, fingerprints, content type and history
  serialization. It injects a literal map; it is not a metadata resolver.
- The pilot's read-only resolver is still in `pegelonline_core.fabric`.
  Before automated fleet deployment, extract its non-domain schema-resolution
  logic into shared tooling with existing tests and synthetic identities.
  Do not copy it into every feeder or make other feeders depend on Pegelonline.
  Its same-workspace schema-set limitation remains a qualification gate.
- The legacy shared deployers create dispatch ingestion and can overwrite the
  Spark kernel/Environment. They are not a qualified schematized path.
  A shared migration deployer must preserve every definition part, source
  association, pinned destination selection, Environment/Lakehouse/database
  binding and dedupe path. Prove creation and update/readback before fleet use.
  Until then, use an approved bounded operator following the linked API contracts,
  not a legacy deployer with guessed patches.
- Maintain a separate preparation PR for shared runtime/deployment extraction.
  Then one migration PR per feeder. Never combine a shared dependency/codegen
  version bump with unrelated feeder changes.

The Avrotize nullable-zero and xrcg structured-JSON corrections are pinned in
the pilot requirements. Retain those revisions until corrected releases pass
the same tests. Regeneration, wheel upload and Environment publication are
separate steps; none updates an already running notebook by itself.

## 2. Inventory each candidate and establish ownership

Record outside Git:

1. Feeder slug, branch/base commit, selected families and all shipped transports.
   Include reference events and their stable subject/key identities.
2. Canonical registry, selected source and projected schema versions,
   fingerprints, serializer output, units, nullability, enums and timestamps.
3. Hosting mode: notebook poller or independently hosted streaming producer.
   Poll-based feeders require notebook hosting. WebSocket/MQTT/TCP/SSE firehoses
   do not become scheduled one-shot pollers as part of this migration.
4. Existing pipeline and exact source node, schema awareness, history database,
   tables/mappings/update policies, output consumers and protocol bindings.
5. Notebook definition, Environment dependencies and loaded package versions,
   state file, approved schedule/expiry and any active invocation.
6. Dependent functions, Maps, dashboards, latest-state materializations,
   geometry/reference assets and consumers that refer to physical table names.
7. Approved identity/audiences/roles, candidate resource ownership, cutover
   permission, rollback retention and bounded event/time limits.

A clean branch is not proof that its worktree is idle. Check editor sessions,
agents, test/build processes and locks before reuse. Do not replace resources
or pause schedules without approval. Do not broaden privileges or use SAS as an
unannounced fallback when workspace identity is unsupported.

Prioritize a small poller with matching transport support and few downstream
dependencies. Mark each feeder ready, requiring shared work, blocked, or out of
scope with a reason; do not exclude failing selected families from acceptance.

## 3. Author portable contracts and adapt the runtime

Load the [source-contract skill](../../xreg-source-contract/SKILL.md) for
contract edits. Resolve every selected message's authoritative schema, including
reference families. Reuse an existing Avro variant only if its actual serialized
payload matches it; names such as `.avro` do not prove that.

For a missing JSON Structure projection, run from the repository root:

```powershell
python tools\deploy-fabric\generate_schema_set.py `
  --registry feeders\<source>\xreg\<source>.xreg.json `
  --messagegroup <canonical-message-group> `
  --schema-version "#/schemagroups/<group>/schemas/<schema>=<source-version>" `
  --projected-version "#/schemagroups/<group>/schemas/<schema>=<projection-version>" `
  --create-avro-variants `
  --output-registry <operator-directory>\<source>.fabric.xreg.json `
  --definition <operator-directory>\EventSchemaSetDefinition.json
```

Repeat version options for every selected schema. Explicit versions and
fingerprints are decisions, not a highest-version heuristic. Preserve canonical
endpoints, CloudEvents wire types, subject/key identities and default encodings.
Promote portable validated artifacts into the source only through its reviewed
PR. Never promote registered URLs or live captures.

For dual-encoding data generation, select the validated Avro group and add
`--python-data-output <package-directory> --python-package <package_name>`.
Do not combine runtime generation with `--include-history`; one selected version
per record defines the runtime type. Regenerate clients through the enforced
source generator, never hand-edit generated packages or add local converters.

Adapt only the needed feeder calls: explicitly accept an optional schema override
map, pass it to the generated producer, and preserve behavior when absent.
A deployment map uses original generated schema URIs as keys, not event types.
Test missing/duplicate/conflicting bindings, drift and unmapped family coverage.
If selecting another payload encoding, verify both encoders against the same
schema, including nullable zeros, strings/datetimes and nested/default fields.

## 4. Build and bind a candidate pipeline

Use a newly owned schema-aware Eventstream when existing items cannot enable
the required mode. Preserve the old pipeline for rollback. Follow
[programmatic authoring](./programmatic.md) and the verified native API
references; an inaccessible API is a blocker, not permission to guess endpoints.

1. Register schema versions and read back schema content/fingerprints.
2. Create/read back schema-aware mode, then associate the selected versions
   with the exact source node. Preserve all returned definition parts.
3. Configure custom output and typed history for every selected family.
   Match registered payload media type and history `Json`/`Avro` serialization.
   Let Eventstream create and own the typed base tables.
4. Resolve exact service-issued schema-version URLs only after association.
   Verify selected versions, fingerprints and receiver configuration.
   Never construct URLs from hosts or identifiers found in examples.
5. For a notebook, build the actual dependency graph's wheels outside Git,
   strip wheel path dependencies with the shared helper, and record hashes.
   Native Proton must match the Environment's Linux platform/Python ABI and
   pass `from proton import SSL; assert SSL.present()` in a compatible clean
   container. Retain TLS certificate verification.
6. Upload/publish the source Environment; wait/read back success. Bind Spark,
   Environment, Lakehouse and paired database. No cell `%pip` or `asyncio.run()`.
   Reuse qualified native wheels only when ABI/platform/dependency hashes match.
7. Bind the external deployed notebook copy:

```powershell
python tools\deploy-fabric\bind_notebook_schemas.py `
  --notebook feeders\<source>\notebook\<source>-feed.ipynb `
  --resolved-map <operator-directory>\resolved-map.json `
  --payload-encoding <json-or-avro> `
  --output <operator-directory>\<source>-deployed.ipynb
```

Read back the uploaded cell and bindings. The portable placeholder must fail
unbound. Refresh the cell on target/version changes. The pilot's notebook
requires `ONCE_MODE=True` and matching injected/runtime payload encoding;
continuous mode is unsafe without cooperative shutdown. Source-specific notebook
adaptation must retain those guards rather than blindly copying a template.

Do not clear dedupe state to manufacture fresh events. A new binding/state path
requires an explicit replay decision and retention of the old file. If an upstream
dry period yields no new observations, wait within the approved deadline or report
blocked acceptance; do not use old rows or synthetic telemetry as runtime proof.

## 5. Replace analytics dependencies, not ingestion ownership

After fresh typed-history acceptance, read actual table names and schemas using
`.show table ["<discovered-table>"] schema as json`. Bind source analytics to
those names through validated renderers; do not guess names from schema IDs.
Accept service UTF-8 BOM where present.

Keep legacy KQL artifacts for non-schematized deployments. Separate function-only
analytics from dispatch/base-table DDL, JSON mappings and routing policies.
Static river geometry or another genuinely distinct reference dataset may still
need its own tables; removing dispatch ingestion does not remove every other table.
Inspect update policies per table:
`.show table ["<discovered-table>"] policy update`.
Do not use the invalid `.show tables policy update` command.

Preserve retained-history visibility, time semantics, null/zero behavior, units
and labels. Latest metadata may use envelope time while measurements use
observation time. A recent cutoff that hides stale entities is not equivalent.
Missing comparison history yields unknown trends, not false rising/falling
states. Test thresholds with actual elapsed intervals, including nonpositive
intervals and missing metadata. Measure refresh cost before materialization.

Read back every deployed Map/dashboard query and execute it against the actual
tables. Verify actual styling and data sources, not only a sibling query file.
Perform authenticated visual checks after API configuration: layer visibility,
colored geometry/points, zoom-gated labels, reading units and popups where present.
Selecting a layer row does not necessarily toggle visibility; use its Show/Hide
control. Grey unknown trends can be correct in fresh one-shot history; distinguish
that rendering proof from non-unknown trend boundary tests. Do not claim dashboard
coverage merely because the feeder has a Map.

If the managed automation browser closes, do not infer a cause without evidence.
A separately launched dedicated browser/profile may retain interactive sign-in;
restrict debugging to loopback, disconnect automation without closing the user's
browser, and never copy its authentication profile into artifacts or Git.
Browser automation is for visual checks only, not resource authoring or cleanup.

## 6. Require fresh end-to-end acceptance

Run the applicable repository pre-commit gates and the
[release checklist](../../feeder-release-checklist/SKILL.md):

- Import every touched transport's actual runtime/app module and compile the
  complete changed source tree, including generated code.
- Run the source tests, related shared-tool tests and repository-wide mypy with
  CI's producer `MYPYPATH`. Build every touched source Dockerfile variant.
- Run Docker E2E for bridge/contract/generated changes. Observe at least one real
  event on every shipped transport, not merely imports or a started container.
- Obtain xRegistry, JSON Structure and Avro expert reviews for contract changes,
  plus KQL review where required. Fix blockers, regenerate and re-review.
- Preserve source documentation, generated EVENTS, catalog/notebook flags and
  deployment instructions; retain unchanged defaults and non-Fabric options.

Then apply [registered-schema verification](./verification.md):
finite real events after readiness; successful OneLake runtime log for notebooks;
loaded package versions matching the qualified wheels; and fresh events from
every selected family matched between independently decoded custom output and
typed history by ID, payload, envelope and exact registered `dataschema`.
Registration, broker acceptance, job completion and old counts are separate
observations, never substitutes for that correlation.

Match history serialization at candidate creation. Raw Avro passed without OCF
or Confluent framing, but an in-place decoder flip failed and rollback did not
recover it ([#1763](https://github.com/clemensv/real-time-sources/issues/1763)).
Do not repeat that mutation on production or treat custom-output bytes alone as
acceptance. Original JSON Structure constraints remain necessary because generic
Avro/Fabric readers do not enforce all patterns, enum domains or numeric bounds.

Store full evidence externally. PRs include exact validation commands/results,
review verdicts, acceptance counts and remaining blockers, without deployment
coordinates or live payloads. No completed status while a required gate is open.

## 7. Cut over with a usable rollback

Before mutation, save the old pipeline/notebook definitions, complete bindings,
schema selections, consumer routing, state file location and approved schedule
outside Git. Record owned candidate IDs as soon as creation is reconciled.
An uncertain create response requires readback before retry, not another create.

After manual candidate acceptance, obtain approved cutover/retention decisions.
Pause only the relevant schedule, reconcile its active invocation, and establish
a single writer unless deliberate dual publishing/replay has been approved.
Switch consumers and dependent analytics only after their candidate tests pass.
Restore the approved schedule/expiry, read it back and observe an actual scheduled
invocation with fresh output/history acceptance. Include compute startup in
whole-job duration; cadence alone is not a freshness guarantee.

On failure, stop only the owned candidate writer/schedule. Restore the saved old
bindings, routing and schedule without trying to reverse an unqualified decoder
mutation. Retain both histories and state for reconciliation, and verify the old
path with genuine fresh events. Document any replay/gap decision explicitly.

Retire old resources only after acceptance, consumer handoff, approved rollback
retention and explicit deletion authorization. Delete only recorded owned items,
in dependency order, and verify absence. A workspace-wide wipe is never migration
cleanup. Retain unrelated Maps, dashboards, histories, locks and invocations.

## 8. Execute with a measured disk budget

Inventory registered worktrees, object-store sharing, dirty/untracked files,
unpublished commits, locks and active owners before allocating another checkout.
Measure free disk and logical/allocated sizes separately; nested worktrees and
hard-linked dependencies can distort summed logical bytes.

Reuse an existing idle clean worktree only after its branch work is merged or
preserved remotely and the owner permits repurposing. Merged via squash does not
mean the old HEAD is an ancestor of main; verify the PR/patch independently.
Dirty, ahead, detached, locked or active worktrees are preservation candidates,
not automatic deletion targets. Keep the native-wheel and upstream-generator
worktrees needed by still-pinned/unmerged fixes until their artifacts and commits
have a verified replacement.

Prefer a single clean execution worktree containing current main and this skill.
Create a new feeder branch in it after the previous PR is merged and the worktree
is clean; an unmerged feeder PR requires another approved slot or a pause.
Sparse checkout may reduce a new/repurposed slot to selected feeders and shared
tools/tests, but verify generator/dependency paths first. Repository-wide mypy
and fleet-wide gates require a full checkout or an approved complete CI runner;
sparse checkout is not permission to omit them.

Share only immutable dependency caches and hash-qualified native wheels.
Use one bounded build environment at a time unless measured peak usage supports
more. Budget source checkout, wheel/build contexts, test containers, logs and
rollback evidence, with an operator-approved reserve. Pause new work when that
reserve would be crossed. A disk shortage does not justify skipping validation.

For approved reclamation, remove registered idle worktrees with
`git worktree remove <exact-path>` without `--force`, after preservation checks.
Do not recursively delete checkout roots, session folders or shared caches.
`git worktree prune --dry-run` only reports stale registration metadata; it does
not reclaim live checkout bytes. Inventory Docker usage before any targeted image
removal; never run a blanket system/volume prune on the shared machine.

## Completion checklist

- [ ] Shared tooling/identity path qualified; feeder scope and ownership approved.
- [ ] Portable variants, versions, fingerprints and serializer behavior reviewed.
- [ ] All required local/CI gates and shipped-transport runtime proof passed.
- [ ] Source association, receiver serialization and typed tables read back.
- [ ] Environment/native TLS and deployed notebook binding verified, if applicable.
- [ ] State/history preserved; fresh output/history matched for every family.
- [ ] Deployed analytics and visual Map/dashboard checks passed, where applicable.
- [ ] Approved cutover and actual scheduled invocation verified, if applicable.
- [ ] Rollback retained and cleanup limited to authorized owned assets.
- [ ] PR verdicts and external operator evidence saved; disk reserve respected.

Mark not-applicable items with the actual reason. Migration authoring, isolated
acceptance and production cutover are different outcomes; report which completed.
