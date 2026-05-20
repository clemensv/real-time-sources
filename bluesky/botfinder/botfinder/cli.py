"""Command-line entry point for running the full botfinder workflow.

The CLI turns user-supplied runtime parameters into a :class:`Config`, runs
the full acquisition → scoring → graph/card pipeline, and writes the two
primary deliverables: per-card Plotly HTML files and a consolidated dossier
for the anchor account under investigation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import plotly.io as pio

from .config import Config
from .pipeline import run_full_pipeline


def _build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser for a botfinder run.
    
    Returns:
        argparse.ArgumentParser: Parser configured with analysis, API, Kusto,
        and output options for the end-to-end pipeline.
    """
    p = argparse.ArgumentParser(prog="botfinder",
                                description="Bluesky bot-cluster analysis")
    p.add_argument("--anchor", required=True,
                   help="Bluesky handle of the cluster anchor (e.g. niusde.bsky.social)")
    p.add_argument("--lookback", type=int, default=90,
                   help="Lookback window in days (default 90)")
    p.add_argument("--max-followers", type=int, default=5000,
                   help="Cap on followers fetched via public API (default 5000)")
    p.add_argument("--enrich-limit", type=int, default=400,
                   help="Cap on profiles enriched via API (default 400)")
    p.add_argument("--api-concurrency", type=int, default=10)
    p.add_argument("--skip-api", action="store_true",
                   help="Skip Bluesky public API calls (KQL only)")
    p.add_argument("--kusto-uri", default=None,
                   help="Kusto cluster URI (overrides BOTFINDER_KUSTO_URI)")
    p.add_argument("--kusto-database", default=None,
                   help="Kusto database name (overrides BOTFINDER_KUSTO_DATABASE)")
    p.add_argument("--output-dir", default="botfinder-output",
                   help="Directory for HTML dossier and per-card files")
    return p


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments, run the pipeline, and write report artifacts.
    
    Args:
        argv: Optional argument vector for testing. When ``None``, arguments
            are read from ``sys.argv``.
    
    Returns:
        int: Process exit code. ``0`` means success, while ``2`` indicates a
        missing Kusto configuration.
    
    Notes:
        The CLI intentionally keeps orchestration thin: acquisition, scoring,
        clustering, and reporting remain in library modules so notebooks and
        tests can reuse the same logic.
    """
    args = _build_parser().parse_args(argv)

    overrides: dict = {}
    if args.kusto_uri:
        overrides["kusto_uri"] = args.kusto_uri
    if args.kusto_database:
        overrides["kusto_database"] = args.kusto_database

    config = Config(
        anchor_handle=args.anchor,
        lookback_days=args.lookback,
        max_followers=args.max_followers,
        enrich_limit=args.enrich_limit,
        api_concurrency=args.api_concurrency,
        skip_api=args.skip_api,
        **overrides,
    )

    if not config.kusto_uri or not config.kusto_database:
        print("ERROR: Kusto URI/database not set. Use --kusto-uri/--kusto-database "
              "or set BOTFINDER_KUSTO_URI / BOTFINDER_KUSTO_DATABASE.", file=sys.stderr)
        return 2

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"=== botfinder run for @{args.anchor} ===")
    print(f"  cluster:  {config.kusto_uri}")
    print(f"  database: {config.kusto_database}")
    print(f"  output:   {out.resolve()}")

    result = run_full_pipeline(config)

    # Per-card HTML
    card_dir = out / "cards"
    card_dir.mkdir(exist_ok=True)
    for card_id, fig in result.cards.items():
        path = card_dir / f"{card_id}.html"
        pio.write_html(fig, str(path), full_html=True, include_plotlyjs="cdn")
    print(f"  Wrote {len(result.cards)} cards to {card_dir}")

    # Dossier
    try:
        from .dossier import render_dossier
        scores = result.analysis.scores_df
        if scores.empty:
            stats = {
                "total_suspects": 0, "high_confidence_bots": 0, "medium_confidence_bots": 0,
                "pct_instant_follow": 0.0, "pct_anonymous": 0.0,
                "mean_score": 0.0, "p90_score": 0.0,
            }
        else:
            total = len(scores)
            stats = {
                "total_suspects": total,
                "high_confidence_bots": int((scores["score"] >= 0.7).sum()),
                "medium_confidence_bots": int(((scores["score"] >= 0.4) & (scores["score"] < 0.7)).sum()),
                "pct_instant_follow": 100 * scores["flags"].fillna("").str.contains("INSTANT_FOLLOW").sum() / total,
                "pct_anonymous":      100 * scores["flags"].fillna("").str.contains("ANONYMOUS_PROFILE").sum() / total,
                "mean_score": float(scores["score"].mean()),
                "p90_score":  float(scores["score"].quantile(0.9)),
            }
        top_suspects = []
        if not scores.empty:
            top = scores.nlargest(50, "score")
            for _, row in top.iterrows():
                flags_str = row.get("flags", "") or ""
                top_suspects.append({
                    "handle":          row.get("handle", "") or "",
                    "display_name":    row.get("display_name", "") or "",
                    "total_score":     float(row["score"]),
                    "flags":           [f for f in flags_str.split(",") if f],
                    "posts_count":     0,
                    "followers_count": 0,
                    "age_minutes":     -1,
                    "source":          row.get("source", "") or "",
                })
        figures = [fig for _, fig in result.cards.items()]
        dossier_path = out / f"dossier_{config.anchor_slug}.html"
        render_dossier(
            target_handle=config.anchor_handle,
            stats=stats, figures=figures, top_suspects=top_suspects,
            lookback_days=config.lookback_days, output_path=dossier_path,
        )
        print(f"  Wrote HTML dossier to {dossier_path}")
    except Exception as e:
        print(f"  WARNING: dossier render failed: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
