# Proposal Notes

This folder contains the current mockups for presenting and onboarding the real-time source bridges.

## Proposal Set

- [design1-fluent-ops-console.html](design1-fluent-ops-console.html): strongest intro and grouping language. Good landing-page framing.
- [design2-data-flow-blueprint.html](design2-data-flow-blueprint.html): strongest operations-heavy visual direction.
- [design3-catalog-table.html](design3-catalog-table.html): strongest dense catalog pattern for comparing bridges and exposing setup details.
- [design4-geographic-explorer.html](design4-geographic-explorer.html): strongest geographic storytelling, but weaker for setup-first workflows.
- [design5-pipeline-configurator.html](design5-pipeline-configurator.html): strongest Fabric-native configurator concept.
- [design6-guided-setup-hybrid.html](design6-guided-setup-hybrid.html): recommended direction. It combines the reassuring intro from design 1 with the dense operational catalog from design 3 and adds the setup-pack / launcher model.

## Recommended Direction

The best next step is to treat the site as a guided setup surface instead of only a source catalog.

- Keep the high-level intro and topic grouping from design 1.
- Keep the dense, expandable table from design 3.
- Make every expanded row operational: exact launcher, ACI path, generated KQL bundle, validation query, and fallback instructions.
- Optimize for time to first rows in Fabric, not for visual novelty alone.

## Proposed User Flow

The intended onboarding flow is:

1. User answers a few setup-critical questions on the web page.
2. The page generates a short launcher command for Azure Cloud Shell.
3. The user opens shell.azure.com and pastes the command.
4. Cloud Shell deploys the feeder to Azure Container Instances, creates or configures the Fabric-side items, applies KQL, and returns a setup pack plus validation queries.

This avoids asking the user to manually discover topic names, table names, ingestion mappings, or first validation commands.

## Why Cloud Shell Fits

- It is a good orchestration environment for Azure and Fabric bootstrap work.
- It already runs inside the user's authenticated Azure context.
- It is a better target for a copy-paste launcher than local PowerShell because it removes local environment setup from the critical path.

Cloud Shell should orchestrate the setup, not host the bridge container itself. The long-running bridge should run in Azure Container Instances or another managed runtime.

## Important Constraint

Cloud Shell is not the right model for arbitrary third-party embedding. The supported UX is to send users to Microsoft-hosted surfaces such as shell.azure.com or the Azure portal, then have them paste the launcher there.

## Why The Launcher Model Is Plausible

The Fabric platform now exposes enough API surface for this flow to be realistic:

- Workspaces can be listed and validated.
- Eventhouse items can be created.
- KQL Database items can be created, including definitions that carry schema bootstrap content.
- Eventstream items can be created from definitions.

This means the remaining problem is no longer "can Fabric be automated at all" but "which parts of Eventstream connection wiring can be automated cleanly."

## Main Remaining Risk

The biggest open technical risk is Eventstream connection-level configuration.

- Some Eventstream definitions still appear to need values such as data connection ids, connection names, or mapping rule names.
- If those values cannot be created or resolved cleanly through API calls, the launcher should degrade gracefully.
- The fallback should be explicit: stop at the exact point where manual confirmation is needed and show the operator the precise values to paste.

## Repo Reality Behind The Mockup

- Azure deployment coverage is already strong because most bridges already ship azure-template.json files.
- Fabric/KQL coverage exists but is not complete for every bridge yet.
- That is why the hybrid mockup intentionally assumes generated per-bridge setup packs, validation queries, ingestion JSON, and launcher payloads.

## What To Build Next

1. A small launcher service that issues short-lived payload URLs.
2. A Cloud Shell entry script that reads the payload and orchestrates Azure plus Fabric setup.
3. Per-bridge generated assets: bootstrap wrapper, Eventstream definition, validation KQL, operator runbook, setup-pack zip.
4. A clean fallback for the last manual Eventstream connection step if API coverage is incomplete.