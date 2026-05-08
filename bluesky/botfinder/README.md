# botfinder

Bluesky bot-network detection and dossier generation around an anchor
account, powered by the [`bluesky` real-time-sources bridge][bridge] and a
Microsoft Fabric KQL database.

```python
from botfinder import Config, run_full_pipeline

cfg = Config(anchor_handle="niusde.bsky.social")
result = run_full_pipeline(cfg)
for card_id, fig in result.cards.items():
    fig.show()
```

## Prerequisites

Before running botfinder, you need the Bluesky firehose data flowing into a
KQL database. This requires three components:

1. **Bluesky firehose bridge** — a container that reads the AT Protocol
   firehose and writes CloudEvents to Kafka / Event Hubs / Fabric Event
   Streams.
2. **Fabric Eventhouse with a KQL database** — stores the firehose events in
   typed tables (`Bluesky.Graph.Follow_v1`, `Bluesky.Feed.Post_v1`,
   `Bluesky.Feed.Like_v2`, etc.).
3. **The botfinder notebook or CLI** — queries the KQL database and generates
   the analysis.

## Step 1 — Deploy the Bluesky Firehose Bridge

The bridge container image is published at
`ghcr.io/clemensv/real-time-sources-bluesky:latest`. Full documentation:
[bluesky/CONTAINER.md][container-doc].

### Option A: One-click Azure + Fabric deployment

The [`deploy-fabric.ps1`][deploy-fabric] script (designed for Azure Cloud Shell)
deploys everything end-to-end: Azure Container Instance, Event Hub, Fabric KQL
database with schema, and Event Stream wiring.

```powershell
# In Azure Cloud Shell (PowerShell):
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/clemensv/real-time-sources/main/tools/deploy-fabric/deploy-fabric.ps1' -OutFile deploy-fabric.ps1

./deploy-fabric.ps1 `
    -Source bluesky `
    -ResourceGroup rg-bluesky `
    -WorkspaceId "<your-fabric-workspace-id>" `
    -EventhouseId "<your-fabric-eventhouse-id>"
```

This script:
1. Deploys an Azure Container Instance running the bridge via ARM template
2. Creates a KQL database in your Fabric Eventhouse
3. Runs the [KQL schema scripts][kql-scripts] to create typed tables,
   update policies, and materialized views
4. Creates a Fabric Event Stream with a Custom Endpoint
5. Wires the container to send events directly to Fabric

See [`tools/deploy-fabric/README.md`][deploy-fabric-readme] for full parameter
reference and prerequisites.

### Option B: Bring your own infrastructure

If you already have Event Hubs or a Kafka broker:

```bash
docker run --rm \
    -e CONNECTION_STRING='<your-event-hubs-or-fabric-connection-string>' \
    ghcr.io/clemensv/real-time-sources-bluesky:latest
```

Or with Kafka:

```bash
docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<brokers>' \
    -e KAFKA_TOPIC='<topic>' \
    -e SASL_USERNAME='<user>' \
    -e SASL_PASSWORD='<pass>' \
    ghcr.io/clemensv/real-time-sources-bluesky:latest
```

## Step 2 — Set up the KQL Database Schema

If you used `deploy-fabric.ps1` (Option A above), the schema is already
created. Otherwise, run the KQL scripts manually:

The schema definitions are in [`bluesky/kql/`][kql-scripts]. They create:

- **`_cloudevents_dispatch`** — landing table for raw CloudEvents from the
  Event Stream
- **Typed tables** — `Bluesky.Graph.Follow_v1`, `Bluesky.Feed.Post_v1`,
  `Bluesky.Feed.Like_v2`, `Bluesky.Feed.Repost_v1`,
  `Bluesky.Actor.Profile_v2`, `Bluesky.Graph.Block_v1`
- **Update policies** — automatically fan out events from the dispatch table
  into the typed tables
- **Materialized views** — latest-state projections

Execute these scripts against your KQL database using the Fabric portal's
query editor or `az kusto script`.

## Step 3 — Wait for Data

The firehose produces roughly 500–1000 events/second. For meaningful bot
analysis, let the bridge run for at least **3–7 days** to accumulate follow
patterns, likes, and profile data.

## Step 4 — Deploy the Botfinder Notebook

### Option A: Fabric notebook (recommended)

Use the [`deploy-fabric-notebook.ps1`][deploy-notebook] script to upload the
notebook into your Fabric workspace and bind it to the KQL database:

```powershell
./tools/deploy-fabric/deploy-fabric-notebook.ps1 `
    -Source bluesky `
    -Workspace "<workspace-name-or-id>" `
    -Eventhouse "<eventhouse-name>" `
    -DatabaseName bluesky
```

The script:
1. Resolves the workspace, eventhouse, and KQL database
2. Patches the notebook's `KUSTO_URI` and `KUSTO_DATABASE` parameters
3. Creates or updates the notebook item in the Fabric workspace

Open the notebook in Fabric, set `ANCHOR_HANDLE` to the account you want to
analyze, and run all cells.

### Option B: Local CLI

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=bluesky/botfinder
```

```bash
export BOTFINDER_KUSTO_URI="https://<your-eventhouse>.z2.kusto.fabric.microsoft.com"
export BOTFINDER_KUSTO_DATABASE="bluesky"

botfinder --anchor niusde.bsky.social --output-dir output
```

### Option C: Python API

```python
from botfinder import Config, run_full_pipeline

cfg = Config(
    anchor_handle="niusde.bsky.social",
    kusto_uri="https://<your-eventhouse>.z2.kusto.fabric.microsoft.com",
    kusto_database="bluesky",
)
result = run_full_pipeline(cfg)
```

## Configuration

`Config` resolves Kusto connection details in this order:

1. Constructor arguments (`kusto_uri`, `kusto_database`)
2. Fabric notebook context (`notebookutils.kql.listDatabases()`)
3. Environment variables `BOTFINDER_KUSTO_URI`, `BOTFINDER_KUSTO_DATABASE`

## What the Analysis Produces

The pipeline generates:

- **Bot scores** — composite 0–1 score per follower from 5 signals (temporal
  proximity, anonymity, activity patterns, follow overlap, account age)
- **Co-follow graph** — network of accounts that suspect followers share,
  revealing coordinated clusters
- **Cross-follow speed** — how fast suspects find the rest of the network
- **15 visualization cards** — publication-ready PNG charts
- **HTML dossier** — standalone report with all findings

## Links

- [Bluesky bridge documentation][bridge]
- [Container image and deployment options][container-doc]
- [Deploy to Fabric (one-click)][deploy-fabric-readme]
- [KQL schema scripts][kql-scripts]
- [Notebook deployment script][deploy-notebook]
- [Event schema reference][events-doc]

[bridge]: https://github.com/clemensv/real-time-sources/tree/main/bluesky
[container-doc]: https://github.com/clemensv/real-time-sources/blob/main/bluesky/CONTAINER.md
[deploy-fabric]: https://github.com/clemensv/real-time-sources/blob/main/tools/deploy-fabric/deploy-fabric.ps1
[deploy-fabric-readme]: https://github.com/clemensv/real-time-sources/tree/main/tools/deploy-fabric
[deploy-notebook]: https://github.com/clemensv/real-time-sources/blob/main/tools/deploy-fabric/deploy-fabric-notebook.ps1
[kql-scripts]: https://github.com/clemensv/real-time-sources/tree/main/bluesky/kql
[events-doc]: https://github.com/clemensv/real-time-sources/blob/main/bluesky/EVENTS.md
