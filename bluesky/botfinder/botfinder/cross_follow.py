"""Cross-following analysis — sample cohort accounts and measure how many
others in the cohort each one follows. Powers cards 12–13.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx
import pandas as pd

from .bluesky_api import BlueskyClient
from .kusto import execute_query

if TYPE_CHECKING:  # pragma: no cover
    from .pipeline import AnalysisResult


@dataclass
class CrossFollowResult:
    sample: pd.DataFrame  # API-sampled bot vs. non-bot cross-follow rates
    speed: pd.DataFrame  # KQL-derived per-event days_to_cross_follow
    per_account: pd.DataFrame  # min/median days per account


async def _measure_via_api(
    scores_df: pd.DataFrame, sample_size: int, concurrency: int
) -> pd.DataFrame:
    all_dids = set(scores_df["did"].tolist())
    all_handles = set(scores_df["handle"].dropna().tolist())

    bot_pool = scores_df[scores_df["score"] >= 0.5]
    non_pool = scores_df[scores_df["score"] < 0.5]
    bot_n = min(sample_size // 2, len(bot_pool))
    non_n = min(sample_size // 2, len(non_pool))
    sample = pd.concat([
        bot_pool.sample(bot_n, random_state=42) if bot_n else bot_pool.head(0),
        non_pool.sample(non_n, random_state=42) if non_n else non_pool.head(0),
    ])

    client_obj = BlueskyClient(concurrency=concurrency, timeout=30.0)
    results = []

    async with httpx.AsyncClient(timeout=30.0) as http_client:
        for _, row in sample.iterrows():
            did = row["did"]
            handle = row.get("handle", "")
            score = row["score"]
            try:
                follows = await client_obj.get_follows(http_client, did, limit=200)
                followed_dids = {f.did for f in follows}
                followed_handles = {f.handle for f in follows}
                cohort_overlap = max(
                    len(followed_dids & all_dids),
                    len(followed_handles & all_handles),
                )
                total = len(follows)
                results.append({
                    "did": did, "handle": handle, "score": score,
                    "is_bot": score >= 0.5,
                    "total_follows_fetched": total,
                    "cohort_follows": cohort_overlap,
                    "cohort_pct": (cohort_overlap / total * 100) if total > 0 else 0,
                })
            except Exception:
                results.append({
                    "did": did, "handle": handle, "score": score,
                    "is_bot": score >= 0.5,
                    "total_follows_fetched": 0, "cohort_follows": 0, "cohort_pct": 0,
                })
            await asyncio.sleep(0.05)

    return pd.DataFrame(results)


def _kql_cross_speed(
    analysis: "AnalysisResult",
    anchor_dids: list[str],
    verbose: bool,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    config = analysis.config
    scores_df = analysis.scores_df
    detail_df = analysis.detail_df
    cohort_dids = scores_df["did"].tolist()
    if not anchor_dids or not cohort_dids:
        empty = pd.DataFrame()
        return empty, empty

    BATCH = config.cohort_batch_size
    anchor_str = ",".join(f'"{d}"' for d in anchor_dids)
    rows = []
    for i in range(0, len(cohort_dids), BATCH):
        batch = cohort_dids[i:i + BATCH]
        batch_str = ",".join(f'"{d}"' for d in batch)
        query = f"""
        let anchors = dynamic([{anchor_str}]);
        let cohort = dynamic([{batch_str}]);
        ['Bluesky.Graph.Follow_v1']
        | where did in (cohort) and subject in (anchors)
        | project did, subject, follow_time = ___time
        """
        df = execute_query(config, query)
        if not df.empty:
            rows.append(df)
        if verbose:
            print(f"  cross-speed batch {i // BATCH + 1}/{(len(cohort_dids) + BATCH - 1) // BATCH}: {len(df)}")

    cross = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(
        columns=["did", "subject", "follow_time"]
    )

    creation_map = (
        detail_df.set_index("follower_did")["follower_created_at"].to_dict()
        if not detail_df.empty else {}
    )
    cross["created_at"] = cross["did"].map(creation_map)
    cross["follow_time"] = pd.to_datetime(cross["follow_time"], utc=True, errors="coerce")
    cross["created_at"] = pd.to_datetime(cross["created_at"], utc=True, errors="coerce")
    cross = cross.dropna(subset=["created_at", "follow_time"])
    cross["days_to_cross_follow"] = (
        (cross["follow_time"] - cross["created_at"]).dt.total_seconds() / 86400
    )
    cross = cross[cross["days_to_cross_follow"] >= 0]

    cross = cross.merge(scores_df[["did", "score", "flags"]], on="did", how="left")
    cross["category"] = "Unauffällig"
    cross.loc[cross["score"] >= 0.5, "category"] = "Bot"
    cross.loc[
        (cross["score"] < 0.5)
        & (cross["flags"].fillna("").str.contains("AMPLIFICATION", na=False)),
        "category",
    ] = "Verstärker"

    if cross.empty:
        per = pd.DataFrame(columns=["did", "first_cross", "median_cross", "n_cross", "category", "score"])
    else:
        per = cross.groupby("did").agg(
            first_cross=("days_to_cross_follow", "min"),
            median_cross=("days_to_cross_follow", "median"),
            n_cross=("days_to_cross_follow", "count"),
            category=("category", "first"),
            score=("score", "first"),
        ).reset_index()

    return cross, per


def measure_cross_following(
    analysis: "AnalysisResult",
    *,
    sample_size: int = 80,
    verbose: bool = True,
) -> CrossFollowResult:
    config = analysis.config
    scores_df = analysis.scores_df

    sample_df = pd.DataFrame()
    if not config.skip_api and not scores_df.empty:
        sample_df = asyncio.run(
            _measure_via_api(scores_df, sample_size, config.api_concurrency)
        )

    # KQL speed needs anchor dids — i.e. cluster nodes outside the cohort.
    # We let the caller pass them via re-running with cluster info; here we
    # do a best-effort using outbound follows already in acquired data.
    anchor_dids: list[str] = []
    if not analysis.acquired.follows_from_cohort.empty:
        target_counts = analysis.acquired.follows_from_cohort["subject"].value_counts()
        cohort_set = set(scores_df["did"].tolist())
        anchor_dids = [d for d in target_counts.head(50).index.tolist() if d not in cohort_set]

    speed_df, per_account = _kql_cross_speed(analysis, anchor_dids, verbose=verbose)

    return CrossFollowResult(sample=sample_df, speed=speed_df, per_account=per_account)
