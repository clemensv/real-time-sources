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

## Install

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=bluesky/botfinder
```

In a Fabric notebook:

```python
%pip install -q git+https://github.com/clemensv/real-time-sources#subdirectory=bluesky/botfinder
```

## CLI

```bash
botfinder --anchor niusde.bsky.social --output-dir output
```

## Configuration

`Config` resolves Kusto connection details in this order:

1. Constructor arguments
2. Fabric notebook context (`notebookutils.kql.listDatabases()`)
3. Environment variables `BOTFINDER_KUSTO_URI`, `BOTFINDER_KUSTO_DATABASE`

[bridge]: https://github.com/clemensv/real-time-sources/tree/main/bluesky
