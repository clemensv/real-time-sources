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
        "# Bluesky Bot-Cluster Analyse\n\n"
        "Diese Notebook erstellt einen vollständigen Bot-Cluster-Report rund um einen "
        "Bluesky-Anker-Account. Die einzige Konfiguration ist der `ANCHOR_HANDLE` "
        "in der Parameterzelle weiter unten.\n\n"
        "**Voraussetzungen**\n"
        "- Notebook ist mit einer Bluesky-KQL-Datenbank verbunden (KQL-Tab links). "
        "`deploy-fabric-notebook.ps1` setzt diese Bindung automatisch.\n"
        "- Identität, mit der das Notebook ausgeführt wird, hat Reader-Rechte auf "
        "der Eventhouse-Datenbank.\n"
    ),
    code(
        "# Modul aus dem real-time-sources Repo installieren (SHA-pinned)\n"
        "%pip install -q --upgrade --force-reinstall --no-cache-dir --no-deps "
        "git+https://github.com/clemensv/real-time-sources@65de3934a024261d87ebcabc42426b3d82616e83"
        "#subdirectory=bluesky/botfinder\n"
        "%pip install -q "
        "git+https://github.com/clemensv/real-time-sources@65de3934a024261d87ebcabc42426b3d82616e83"
        "#subdirectory=bluesky/botfinder\n"
    ),
    code(
        "# === PARAMETERS ===\n"
        "# Inhaltliche Variable: ANCHOR_HANDLE.\n"
        "# KUSTO_URI / KUSTO_DATABASE werden vom Deploy-Skript pro Workspace gesetzt.\n"
        'ANCHOR_HANDLE  = "niusde.bsky.social"\n'
        "LOOKBACK_DAYS  = 90\n"
        "MAX_FOLLOWERS  = 5000\n"
        "ENRICH_LIMIT   = 400\n"
        "SKIP_API       = False\n"
        "\n"
        "# Workspace-spezifische Defaults — vom Deploy-Skript überschrieben.\n"
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
    md("## Vollständige Pipeline ausführen\n"
       "Akquise (KQL) → API-Anreicherung → Scoring → Cluster-Graph → "
       "Cross-Follow → Karten."),
    code(
        "result = run_full_pipeline(config)\n"
        "scores = result.analysis.scores_df\n"
        'print(f"Cohort: {len(scores)} accounts")\n'
        "print(f\"Bots:   {(scores['score'] >= config.bot_score_threshold).sum()}\")\n"
    ),
    md("## KPI-Übersicht"),
    code(
        "import pandas as pd\n"
        "scores = result.analysis.scores_df\n"
        "flags = scores['flags'].fillna('')\n"
        "kpis = pd.DataFrame([\n"
        "    {'Metrik': 'Cohort total',        'Wert': len(scores)},\n"
        "    {'Metrik': 'Bots (score≥0.5)',    'Wert': int((scores['score'] >= 0.5).sum())},\n"
        "    {'Metrik': 'Sofort-Follow',       'Wert': int(flags.str.contains('INSTANT_FOLLOW').sum())},\n"
        "    {'Metrik': 'Anonyme Profile',     'Wert': int(flags.str.contains('ANONYMOUS_PROFILE').sum())},\n"
        "    {'Metrik': 'Gelöschte Profile',   'Wert': int(flags.str.contains('DELETED').sum())},\n"
        "    {'Metrik': 'Cluster-Knoten',      'Wert': len(result.cluster_nodes)},\n"
        "    {'Metrik': 'Cluster-Kanten',      'Wert': len(result.cluster_edges)},\n"
        "])\n"
        "display(kpis)\n"
    ),
    md("## Top-Verdächtige"),
    code(
        "top = scores.nlargest(20, 'score')[['handle', 'display_name', 'score', 'flags']]\n"
        "display(top)\n"
    ),
    md("## Karten\n"
       "Jede Karte ist eine eigenständige Plotly-Visualisierung im 1200×675-Format "
       "(Karte 5 ist 1200×1200)."),
    code(
        "for card_id, fig in result.cards.items():\n"
        "    print(card_id)\n"
        "    fig.show()\n"
    ),
    md("## HTML-Dossier ins Lakehouse schreiben (optional)"),
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

