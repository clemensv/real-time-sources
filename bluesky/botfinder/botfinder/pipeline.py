"""High-level orchestration for the botfinder analysis workflow.

This module connects the pipeline stages end to end. It starts from raw
cohort acquisition, optionally extends the cohort through the public
Bluesky API, computes per-account bot scores, derives overlap statistics,
and finally feeds cluster, cross-follow, and card-generation stages. It
exposes a scoring-only entry point and a full reporting entry point.
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from typing import Any

import httpx
import numpy as np
import pandas as pd

from .acquire import AcquiredData, acquire_all
from .bluesky_api import (
    BlueskyClient,
    BlueskyProfile,
    FollowRecord,
    enrich_suspects_sync,
)
from .config import Config
from .scoring import (
    BotScore,
    _is_random_handle,
    compute_bot_score,
    compute_network_statistics,
)


@dataclass
class AnalysisResult:
    """Outputs of the scoring-focused portion of the pipeline.
    
    Attributes:
        config: Runtime configuration used for the run.
        acquired: Raw acquisition bundle returned by ``acquire_all``.
        detail_df: Cohort-level detail table combining KQL-timed followers with
            older API-only followers.
        scores_df: Flattened per-account bot score table used by nearly every
            downstream stage.
        overlap_df: Table of frequently co-followed targets among instant or
            highly suspicious followers.
        network_stats: Aggregate statistics derived from the bot scores.
        enriched: API enrichment payloads keyed by suspect DID.
        api_followers: Followers fetched from the public API to extend the
            cohort beyond the KQL lookback window.
    """
    config: Config
    acquired: AcquiredData
    detail_df: pd.DataFrame
    scores_df: pd.DataFrame
    overlap_df: pd.DataFrame
    network_stats: dict
    enriched: dict[str, dict]
    api_followers: list[FollowRecord]


@dataclass
class FullResult:
    """Outputs of the full end-to-end pipeline including presentation artifacts.
    
    Attributes:
        analysis: Scoring-stage result from ``run_analysis``.
        cluster_nodes: Co-follow graph node table.
        cluster_edges: Co-follow graph edge table.
        cross_follow_per_account: Account-level cross-follow timing summary.
        cards: Mapping from card identifier to rendered Plotly figure.
    """
    analysis: AnalysisResult
    cluster_nodes: pd.DataFrame
    cluster_edges: pd.DataFrame
    cross_follow_per_account: pd.DataFrame
    cards: dict[str, Any]  # card_id -> plotly.Figure

    @property
    def scores_df(self) -> pd.DataFrame:
        """Expose the scored cohort table directly on the full result object.
        
        Returns:
            pd.DataFrame: Alias for ``analysis.scores_df``.
        """
        return self.analysis.scores_df


def _fetch_all_followers_via_api(
    target_handle: str, max_followers: int, concurrency: int
) -> list[FollowRecord]:
    """Fetch the anchor's follower list from the public API.
    
    Args:
        target_handle: Handle of the anchor account.
        max_followers: Maximum number of follower records to collect.
        concurrency: Maximum parallel Bluesky API calls.
    
    Returns:
        list[FollowRecord]: Follower records used to extend the cohort beyond
        KQL-timed follow events.
    """
    async def _fetch():
        """Run the async follower crawl used by the synchronous pipeline wrapper."""
        bsky = BlueskyClient(concurrency=concurrency)
        async with httpx.AsyncClient(timeout=30.0) as client:
            return await bsky.get_followers(client, target_handle, limit=max_followers)
    from ._async import run_async
    return run_async(_fetch())


def _compute_follow_overlap_from_data(
    suspect_dids: list[str],
    outbound_follows_df: pd.DataFrame,
    target_did: str,
) -> pd.DataFrame:
    """Summarize which external targets are shared across suspect follows.
    
    Args:
        suspect_dids: DIDs selected for overlap analysis, usually very fast
            followers of the anchor.
        outbound_follows_df: Cohort outbound follow edges collected during
            acquisition.
        target_did: DID of the anchor account so it can be excluded.
    
    Returns:
        pd.DataFrame: Ranked table of frequently co-followed targets and the
        number of suspect accounts following each one.
    
    Notes:
        This is the first overlap signal feeding the scorer. If many rapid
        followers also converge on the same political targets, that suggests a
        centrally managed follow program rather than organic discovery.
    """
    if outbound_follows_df.empty:
        return pd.DataFrame()
    suspect_follows = outbound_follows_df[outbound_follows_df["did"].isin(suspect_dids)]
    if suspect_follows.empty:
        return pd.DataFrame()
    target_counts = suspect_follows.groupby("subject")["did"].nunique().reset_index()
    target_counts.columns = ["subject", "followers"]
    target_counts = target_counts[
        (target_counts["subject"] != target_did) & (target_counts["followers"] > 5)
    ].sort_values("followers", ascending=False).head(50)
    return target_counts


def run_analysis(
    config: Config,
    acquired: AcquiredData | None = None,
    *,
    verbose: bool = True,
) -> AnalysisResult:
    """Run acquisition, optional enrichment, and bot scoring for one anchor.
    
    Args:
        config: Runtime configuration for the analysis.
        acquired: Optional precomputed acquisition bundle. When omitted, the
            function calls ``acquire_all`` first.
        verbose: Whether to print progress for the acquisition and scoring
            stages.
    
    Returns:
        AnalysisResult: Detailed cohort tables, bot scores, overlap summaries,
        and enrichment payloads.
    
    Notes:
        The function merges two cohort views: recent followers with precise KQL
        timing and older followers discoverable only through the public API. It
        then prioritizes enrichment budget toward the fastest followers and the
        most suspicious older accounts before computing the composite bot score
        for every cohort member.
    """
    if acquired is None:
        acquired = acquire_all(config, verbose=verbose)

    # KQL detail
    kql_df = acquired.follows_to_target.copy()
    if not kql_df.empty:
        kql_df["follower_created_at"] = pd.to_datetime(
            kql_df["follower_created_at"], utc=True
        )
        kql_df["follow_created_at"] = pd.to_datetime(
            kql_df["follow_created_at"], utc=True
        )
        kql_df["age_at_follow_minutes"] = (
            (kql_df["follow_created_at"] - kql_df["follower_created_at"]).dt.total_seconds() / 60
        )
    kql_df["source"] = "kql"

    if verbose:
        print(f"  KQL followers with timing: {len(kql_df)}")

    # API extension
    api_followers: list[FollowRecord] = []
    if not config.skip_api:
        api_followers = _fetch_all_followers_via_api(
            config.anchor_handle, config.max_followers, config.api_concurrency
        )
        if verbose:
            print(f"  API followers fetched: {len(api_followers)}")

    kql_dids = set(kql_df["follower_did"].dropna().tolist()) if not kql_df.empty else set()
    older_followers = [f for f in api_followers if f.did not in kql_dids]

    older_rows = []
    for f in older_followers:
        try:
            created_dt = pd.to_datetime(f.created_at, utc=True)
        except (ValueError, TypeError):
            created_dt = pd.NaT
        older_rows.append({
            "follower_did": f.did,
            "follower_created_at": created_dt,
            "follow_created_at": pd.NaT,
            "age_at_follow_minutes": np.nan,
            "source": "api",
        })
    older_df = pd.DataFrame(older_rows) if older_rows else pd.DataFrame(columns=kql_df.columns)
    detail_df = pd.concat([kql_df, older_df], ignore_index=True)
    if verbose:
        print(f"  Combined cohort: {len(detail_df)}")

    # Enrichment via API
    enriched: dict[str, dict] = {}
    if not config.skip_api:
        kql_priority: list[str] = []
        if not kql_df.empty:
            kql_priority = (
                kql_df.nsmallest(min(200, len(kql_df)), "age_at_follow_minutes")[
                    "follower_did"
                ].tolist()
            )
        older_suspicious = [
            f for f in older_followers
            if not f.display_name or _is_random_handle(f.handle)
        ]
        older_sample_dids = [f.did for f in older_suspicious[:100]]
        remaining_older = [f for f in older_followers if f.did not in set(older_sample_dids)]
        random.seed(42)
        budget = max(0, config.enrich_limit - len(older_sample_dids) - len(kql_priority))
        older_random_sample = (
            random.sample(remaining_older, min(budget, len(remaining_older)))
            if remaining_older and budget > 0 else []
        )
        older_sample_dids += [f.did for f in older_random_sample]

        all_enrich_dids = list(dict.fromkeys(kql_priority + older_sample_dids))[: config.enrich_limit]
        if verbose:
            print(f"  Enriching {len(all_enrich_dids)} accounts via Bluesky API...")
        if all_enrich_dids:
            enriched = enrich_suspects_sync(all_enrich_dids, concurrency=config.api_concurrency)

    # Follow overlap
    overlap_df = pd.DataFrame()
    if not acquired.follows_from_cohort.empty and not kql_df.empty:
        instant_dids = kql_df[kql_df["age_at_follow_minutes"] < 60]["follower_did"].tolist()
        overlap_df = _compute_follow_overlap_from_data(
            instant_dids, acquired.follows_from_cohort, acquired.target_did
        )
    common_targets = set(overlap_df["subject"].tolist()) if not overlap_df.empty else set()

    # Profile creation lookup
    profile_created_at: dict[str, str] = {}
    if not acquired.profiles.empty:
        for _, row in acquired.profiles.iterrows():
            profile_created_at[row["did"]] = str(row.get("created_at", ""))

    # Scoring
    scores: list[BotScore] = []
    for _, row in detail_df.iterrows():
        did = row["follower_did"]
        enrichment = enriched.get(did, {})
        profile = enrichment.get("profile") if enrichment else None
        if profile is None:
            created_at_val = str(row.get("follower_created_at", ""))
            if not created_at_val or created_at_val == "NaT":
                created_at_val = profile_created_at.get(did, "")
            profile = BlueskyProfile(
                did=did,
                handle="unknown",
                display_name="",
                description="",
                avatar="",
                banner="",
                followers_count=0,
                follows_count=0,
                posts_count=0,
                created_at=created_at_val,
            )
        posts = enrichment.get("posts", []) if enrichment else []
        follows_list = enrichment.get("follows", []) if enrichment else []
        follows_dids = [f.did for f in follows_list] if follows_list else []

        score = compute_bot_score(
            did=did,
            profile=profile,
            posts=posts,
            age_at_follow_minutes=row["age_at_follow_minutes"],
            suspect_follows_dids=follows_dids,
            common_targets=common_targets,
            total_suspects=len(detail_df),
            lookback_days=config.lookback_days,
        )
        scores.append(score)

    scores_df = pd.DataFrame([
        {
            "did": s.did,
            "handle": s.handle,
            "display_name": s.display_name,
            "score": s.total_score,
            "flags": ",".join(s.flags),
            "source": "kql" if s.did in kql_dids else "api",
            **s.signals,
        }
        for s in scores
    ])

    network_stats = compute_network_statistics(scores)

    if verbose:
        n_bots = int((scores_df["score"] >= config.bot_score_threshold).sum()) if not scores_df.empty else 0
        print(f"  Bots (≥{config.bot_score_threshold}): {n_bots}")

    return AnalysisResult(
        config=config,
        acquired=acquired,
        detail_df=detail_df,
        scores_df=scores_df,
        overlap_df=overlap_df,
        network_stats=network_stats,
        enriched=enriched,
        api_followers=api_followers,
    )


def run_full_pipeline(
    config: Config,
    acquired: AcquiredData | None = None,
    *,
    verbose: bool = True,
) -> FullResult:
    """Run the full botfinder workflow from acquisition to report figures.
    
    Args:
        config: Runtime configuration for the analysis.
        acquired: Optional precomputed acquisition bundle.
        verbose: Whether to print progress across all stages.
    
    Returns:
        FullResult: Scored analysis plus cluster tables, cross-follow
        summaries, and rendered Plotly cards.
    
    Notes:
        This is the entry point used by the CLI. It preserves the staged data
        flow so intermediate outputs remain available for notebooks and for the
        dossier generator.
    """
    from .cluster import build_cluster_graph
    from .cross_follow import measure_cross_following
    from .cards import render_all_cards

    analysis = run_analysis(config, acquired, verbose=verbose)

    if verbose:
        print("═══ Cluster graph ═══")
    cluster = build_cluster_graph(analysis, verbose=verbose)

    if verbose:
        print("═══ Cross-follow analysis ═══")
    cross = measure_cross_following(analysis, verbose=verbose)

    if verbose:
        print("═══ Render cards ═══")
    cards = render_all_cards(analysis, cluster, cross)

    return FullResult(
        analysis=analysis,
        cluster_nodes=cluster.nodes_df,
        cluster_edges=cluster.edges_df,
        cross_follow_per_account=cross.per_account,
        cards=cards,
    )
