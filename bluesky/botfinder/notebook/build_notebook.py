"""Build the botfinder Fabric notebook programmatically.

Run::

    python build_notebook.py

Outputs ``botfinder.ipynb`` next to this script.

The notebook is **workspace-agnostic**: the parameters cell carries empty
defaults for ``KUSTO_URI`` / ``KUSTO_DATABASE``; the deploy script
:script:`deploy-fabric-notebook.ps1` patches both the parameters cell and
``metadata.dependencies.kqlDatabases`` when the notebook is uploaded.
"""

from __future__ import annotations

import json
from pathlib import Path

NB_PATH = Path(__file__).parent / "botfinder.ipynb"


def code(src: str, tags: list[str] | None = None) -> dict:
    cell = {
        "cell_type": "code",
        "metadata": {"language": "python"},
        "execution_count": None,
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }
    if tags:
        cell["metadata"]["tags"] = tags
    return cell


def md(src: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": src.splitlines(keepends=True),
    }


CELLS = [
    md(
        "# Bluesky Bot-Cluster Analysis\n\n"
        "This notebook produces a complete bot-cluster report around a "
        "Bluesky anchor account. The only mandatory configuration is "
        "`ANCHOR_HANDLE` in the parameters cell below.\n\n"
        "**Prerequisites**\n"
        "- Notebook is bound to a Bluesky KQL database (see KQL tab on the left). "
        "`deploy-fabric-notebook.ps1` wires this up automatically.\n"
        "- The identity running the notebook has Reader rights on the "
        "Eventhouse database.\n"
    ),
    code(
        "# Upgrade plotly to a recent version (Fabric ships an older default)\n"
        "%pip install -q --upgrade plotly\n"
        "# Install module from the real-time-sources repo (SHA-pinned)\n"
        "%pip install -q --upgrade --force-reinstall --no-cache-dir --no-deps "
        "git+https://github.com/clemensv/real-time-sources@373e3f9c66ddc15a9d9d06cacfcd79000b424f5d"
        "#subdirectory=bluesky/botfinder\n"
        "%pip install -q "
        "git+https://github.com/clemensv/real-time-sources@373e3f9c66ddc15a9d9d06cacfcd79000b424f5d"
        "#subdirectory=bluesky/botfinder\n"
    ),
    code(
        "# === PARAMETERS ===\n"
        "# Main knob: ANCHOR_HANDLE.\n"
        "# KUSTO_URI / KUSTO_DATABASE are populated by the deploy script per workspace.\n"
        'ANCHOR_HANDLE  = "niusde.bsky.social"\n'
        "LOOKBACK_DAYS  = 90\n"
        "MAX_FOLLOWERS  = 5000\n"
        "ENRICH_LIMIT   = 400\n"
        "SKIP_API       = False\n"
        "\n"
        "# Workspace-specific defaults - overwritten by the deploy script.\n"
        'KUSTO_URI      = ""\n'
        'KUSTO_DATABASE = ""\n',
        tags=["parameters"],
    ),
    code(
        "from botfinder import Config, run_full_pipeline\n"
        "\n"
        "config = Config.from_fabric_context(\n"
        "    anchor_handle=ANCHOR_HANDLE,\n"
        "    kusto_uri=KUSTO_URI or None,\n"
        "    kusto_database=KUSTO_DATABASE or None,\n"
        "    lookback_days=LOOKBACK_DAYS,\n"
        "    max_followers=MAX_FOLLOWERS,\n"
        "    enrich_limit=ENRICH_LIMIT,\n"
        "    skip_api=SKIP_API,\n"
        ")\n"
        'print(f"Cluster:  {config.kusto_uri}")\n'
        'print(f"Database: {config.kusto_database}")\n'
        'print(f"Anchor:   @{config.anchor_handle}")\n'
        "assert config.kusto_uri and config.kusto_database, (\n"
        '    "KQL database not configured. Re-deploy this notebook via "\n'
        '    "deploy-fabric-notebook.ps1 or set KUSTO_URI / KUSTO_DATABASE "\n'
        '    "in the parameters cell."\n'
        ")\n"
    ),
    md("## Run the full pipeline\n"
       "Acquire (KQL) -> API enrichment -> scoring -> cluster graph -> "
       "cross-follow -> cards."),
    code(
        "result = run_full_pipeline(config)\n"
        "scores = result.analysis.scores_df\n"
        'print(f"Cohort: {len(scores)} accounts")\n'
        "print(f\"Bots:   {(scores['score'] >= config.bot_score_threshold).sum()}\")\n"
    ),
    md("## KPI overview"),
    code(
        "import pandas as pd\n"
        "scores = result.analysis.scores_df\n"
        "flags = scores['flags'].fillna('')\n"
        "kpis = pd.DataFrame([\n"
        "    {'Metric': 'Cohort total',        'Value': len(scores)},\n"
        "    {'Metric': 'Bots (score>=0.5)',   'Value': int((scores['score'] >= 0.5).sum())},\n"
        "    {'Metric': 'Instant follow',      'Value': int(flags.str.contains('INSTANT_FOLLOW').sum())},\n"
        "    {'Metric': 'Anonymous profiles',  'Value': int(flags.str.contains('ANONYMOUS_PROFILE').sum())},\n"
        "    {'Metric': 'Deleted profiles',    'Value': int(flags.str.contains('DELETED').sum())},\n"
        "    {'Metric': 'Cluster nodes',       'Value': len(result.cluster_nodes)},\n"
        "    {'Metric': 'Cluster edges',       'Value': len(result.cluster_edges)},\n"
        "])\n"
        "display(kpis)\n"
    ),
    md("## Top suspects"),
    code(
        "top = scores.nlargest(20, 'score')[['handle', 'display_name', 'score', 'flags']]\n"
        "display(top)\n"
    ),
    md("## Cards\n"
       "Each card is a standalone Plotly visualization in 1200x675 format "
       "(card 5 is 1200x1200). One cell per card so individual figures can be "
       "re-rendered without re-running the whole pipeline."),
    code(
        "CARD_TITLES = {\n"
        "    'card_01_overview':     '1. Overview',\n"
        "    'card_02_anchors':      '2. Anchor accounts',\n"
        "    'card_03_behavior':     '3. Bot behavior signals',\n"
        "    'card_04_timeline':     '4. Follow burst timeline',\n"
        "    'card_05_cluster':      '5. Bot cluster network',\n"
        "    'card_06_deleted':      '6. Account deletions',\n"
        "    'card_07_lifecycle':    '7. Lifecycle waves',\n"
        "    'card_08_cumulative':   '8. Cumulative growth',\n"
        "    'card_09_age_at_follow':'9. Time from creation to follow',\n"
        "    'card_10_score_dist':   '10. Bot score distribution',\n"
        "    'card_11_scatter':      '11. Creation vs. time to follow',\n"
        "    'card_12_amplifiers':   '12. Amplifier accounts',\n"
        "    'card_13_cross_speed':  '13. Cross-following speed',\n"
        "    'card_14_blocks_likes': '14. Blocks & likes',\n"
        "    'card_15_block_hitlist':'15. Block hit list',\n"
        "}\n"
    ),
]

# One markdown header + one render cell per card
_CARD_IDS = [
    ("card_01_overview",     "Overview"),
    ("card_02_anchors",      "Anchor accounts"),
    ("card_03_behavior",     "Bot behavior signals"),
    ("card_04_timeline",     "Follow burst timeline"),
    ("card_05_cluster",      "Bot cluster network"),
    ("card_06_deleted",      "Account deletions"),
    ("card_07_lifecycle",    "Lifecycle waves"),
    ("card_08_cumulative",   "Cumulative growth"),
    ("card_09_age_at_follow","Time from creation to follow"),
    ("card_10_score_dist",   "Bot score distribution"),
    ("card_11_scatter",      "Creation vs. time to follow"),
    ("card_12_amplifiers",   "Amplifier accounts"),
    ("card_13_cross_speed",  "Cross-following speed"),
    ("card_14_blocks_likes", "Blocks & likes"),
    ("card_15_block_hitlist","Block hit list"),
]
for _idx, (_cid, _title) in enumerate(_CARD_IDS, start=1):
    CELLS.append(md(f"### Card {_idx} - {_title}"))
    CELLS.append(code(
        f"_fig = result.cards.get({_cid!r})\n"
        f"if _fig is None:\n"
        f'    print("Card {_cid} not produced (input data unavailable).")\n'
        f"else:\n"
        f"    _fig.show()\n"
    ))

CELLS += [
    md("## Write HTML dossier to the lakehouse (optional)"),
    code(
        "from pathlib import Path\n"
        "from botfinder.dossier import render_dossier\n"
        "\n"
        "try:\n"
        "    out = Path('/lakehouse/default/Files/botfinder')\n"
        "    out.mkdir(parents=True, exist_ok=True)\n"
        "    figures = list(result.cards.values())\n"
        "    flags = scores['flags'].fillna('')\n"
        "    total = len(scores)\n"
        "    stats = {\n"
        "        'total_suspects':         total,\n"
        "        'high_confidence_bots':   int((scores['score'] >= 0.7).sum()),\n"
        "        'medium_confidence_bots': int(((scores['score'] >= 0.4) & (scores['score'] < 0.7)).sum()),\n"
        "        'pct_instant_follow':     100 * flags.str.contains('INSTANT_FOLLOW').sum() / max(total, 1),\n"
        "        'pct_anonymous':          100 * flags.str.contains('ANONYMOUS_PROFILE').sum() / max(total, 1),\n"
        "        'mean_score':             float(scores['score'].mean()),\n"
        "        'p90_score':              float(scores['score'].quantile(0.9)),\n"
        "    }\n"
        "    suspects = []\n"
        "    for _, row in scores.nlargest(50, 'score').iterrows():\n"
        "        suspects.append({\n"
        "            'handle':          row.get('handle') or '',\n"
        "            'display_name':    row.get('display_name') or '',\n"
        "            'total_score':     float(row['score']),\n"
        "            'flags':           [f for f in (row.get('flags') or '').split(',') if f],\n"
        "            'posts_count':     0, 'followers_count': 0, 'age_minutes': -1,\n"
        "            'source':          row.get('source') or '',\n"
        "        })\n"
        "    path = out / f'dossier_{config.anchor_slug}.html'\n"
        "    render_dossier(config.anchor_handle, stats, figures, suspects, config.lookback_days, path)\n"
        "    print(f'Dossier written to {path}')\n"
        "except Exception as e:\n"
        "    print(f'(Lakehouse write skipped: {e})')\n"
    ),
]


NB = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "name": "synapse_pyspark",
            "display_name": "Synapse PySpark",
            "language": "Python",
        },
        "language_info": {"name": "python"},
        "microsoft": {
            "language": "python",
            "language_group": "synapse_pyspark",
            "ms_spell_check": {"ms_spell_check_language": "en"},
        },
        # Populated by deploy-fabric-notebook.ps1 with the workspace's
        # KQL database id at deploy time. Empty here keeps the repo copy
        # workspace-agnostic.
        "dependencies": {"kqlDatabases": []},
    },
    "cells": CELLS,
}


def main() -> None:
    NB_PATH.write_text(json.dumps(NB, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {NB_PATH}")


if __name__ == "__main__":
    main()









