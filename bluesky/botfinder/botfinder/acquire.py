"""Acquire the raw cohort tables that feed scoring and graph analysis.

This stage resolves the anchor handle to a stable DID, queries the Bluesky
firehose stored in Kusto/Fabric for recent follows into that anchor, and
then collects the auxiliary tables needed downstream: cohort profile rows,
outbound follow edges, blocks received, and like counts. The result is an
in-memory ``AcquiredData`` bundle consumed by ``pipeline.run_analysis`` and,
through it, all later scoring, clustering, and dossier steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd

from .config import Config
from .kusto import execute_query


@dataclass
class AcquiredData:
    """Container for all raw tables fetched during acquisition.
    
    The bundle represents the cohort before any heuristic scoring is applied.
    ``run_analysis`` reads ``follows_to_target`` as its primary cohort table,
    uses ``profiles`` to backfill account creation timestamps and handles, and
    passes ``follows_from_cohort`` plus the block/like aggregates into overlap
    and cluster computations.
    
    Attributes:
        target_did: Permanent DID for the anchor account being investigated.
        follows_to_target: Follow events where cohort accounts followed the
            anchor inside the lookback window.
        profiles: Latest known profile rows for cohort members and frequently
            co-followed targets.
        follows_from_cohort: Outbound follow edges from cohort accounts to
            other Bluesky accounts, used for overlap and graph analysis.
        blocks_received: Aggregate count of blocks received by cohort accounts.
        likes_made: Aggregate count of likes emitted by cohort accounts.
    """

    target_did: str
    follows_to_target: pd.DataFrame
    profiles: pd.DataFrame
    follows_from_cohort: pd.DataFrame
    blocks_received: pd.DataFrame
    likes_made: pd.DataFrame

    @property
    def cohort_dids(self) -> list[str]:
        """Return the unique follower DIDs that make up the anchor cohort.
        
        Returns:
            list[str]: Unique DIDs from ``follows_to_target`` in first-seen order.
            Returns an empty list when the anchor has no qualifying follows in the
            current analysis window.
        """
        if self.follows_to_target.empty:
            return []
        return self.follows_to_target["follower_did"].dropna().unique().tolist()

    def save(self, directory: Path) -> None:
        """Persist the acquired tables for repeatable local analysis.
        
        Args:
            directory: Destination directory where each table is written as a
                parquet file plus a text file for the anchor DID.
        
        Returns:
            None
        
        Notes:
            This is intended for developer workflows so later scoring or card work
            can iterate without re-querying Kusto. The pipeline itself keeps
            acquisition in memory.
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.follows_to_target.to_parquet(directory / "follows_to_target.parquet", index=False)
        self.profiles.to_parquet(directory / "profiles.parquet", index=False)
        self.follows_from_cohort.to_parquet(directory / "follows_from_cohort.parquet", index=False)
        self.blocks_received.to_parquet(directory / "blocks_received.parquet", index=False)
        self.likes_made.to_parquet(directory / "likes_made.parquet", index=False)
        (directory / "target_did.txt").write_text(self.target_did, encoding="utf-8")

    @classmethod
    def load(cls, directory: Path) -> "AcquiredData":
        """Reload a previously saved acquisition bundle from disk.
        
        Args:
            directory: Directory created by :meth:`save`.
        
        Returns:
            AcquiredData: Bundle reconstructed from the parquet snapshots and
            ``target_did.txt``.
        """
        directory = Path(directory)
        return cls(
            target_did=(directory / "target_did.txt").read_text(encoding="utf-8").strip(),
            follows_to_target=pd.read_parquet(directory / "follows_to_target.parquet"),
            profiles=pd.read_parquet(directory / "profiles.parquet"),
            follows_from_cohort=pd.read_parquet(directory / "follows_from_cohort.parquet"),
            blocks_received=pd.read_parquet(directory / "blocks_received.parquet"),
            likes_made=pd.read_parquet(directory / "likes_made.parquet"),
        )


def _resolve_target_did(config: Config) -> str:
    """Resolve the anchor handle to its permanent Bluesky DID.
    
    Args:
        config: Runtime configuration containing ``anchor_handle``.
    
    Returns:
        str: DID for the anchor account.
    
    Notes:
        DIDs are used throughout the pipeline because handles can change while
        firehose records and KQL templates are keyed on the stable identifier.
    """
    import httpx
    handle = config.anchor_handle
    try:
        r = httpx.get(
            "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle",
            params={"handle": handle},
        )
        r.raise_for_status()
        return r.json()["did"]
    except Exception as exc:
        raise RuntimeError(f"Could not resolve DID for @{handle}: {exc}") from exc


def _extract_follows_to_target(config: Config, target_did: str) -> pd.DataFrame:
    """Fetch recent follow events into the anchor and join account creation time.
    
    Args:
        config: Runtime configuration containing the Kusto connection and
            lookback window.
        target_did: DID of the anchor account under investigation.
    
    Returns:
        pd.DataFrame: One row per cohort member with ``follower_did``, account
        creation time, follow time, and Kusto ingestion time.
    
    Notes:
        The join against ``Bluesky.Actor.Profile_v2`` is what enables the later
        temporal-proximity signal: how quickly after account creation each
        follower attached to the anchor.
    """
    query = f"""
    ['Bluesky.Graph.Follow_v1']
    | where subject == "{target_did}"
    | where ___time > ago({config.lookback_days}d)
    | join kind=leftouter (
        ['Bluesky.Actor.Profile_v2']
        | summarize arg_max(___time, *) by did
        | project follower_did=did, follower_created_at=created_at
    ) on $left.did == $right.follower_did
    | summarize arg_max(ingestion_time(), *) by did
    | project follower_did=did,
              follower_created_at=todatetime(follower_created_at),
              follow_created_at=todatetime(created_at),
              ingestion_time=ingestion_time()
    | order by follow_created_at asc
    """
    return execute_query(config, query)


def _batched_query(
    config: Config,
    dids: list[str],
    template: str,
    label: str,
    progress: bool = True,
) -> pd.DataFrame:
    """Execute a parameterised KQL template over cohort-sized DID batches.
    
    Args:
        config: Runtime configuration with Kusto connection details and batch
            size.
        dids: Cohort or target DIDs to inject into the query template.
        template: KQL template expecting ``did_list`` and ``lookback_days``
            placeholders.
        label: Human-readable label for progress output.
        progress: Whether to print per-batch row counts.
    
    Returns:
        pd.DataFrame: Concatenated rows from all successful batches, or an
        empty frame when no rows are returned.
    
    Notes:
        The firehose tables can be large; batching avoids oversized
        ``dynamic`` literals while still letting downstream scoring see the full
        cohort.
    """
    all_rows: list[pd.DataFrame] = []
    n = len(dids)
    if n == 0:
        return pd.DataFrame()
    batch = config.cohort_batch_size
    for i in range(0, n, batch):
        chunk = dids[i:i + batch]
        did_list = ", ".join(f"'{d}'" for d in chunk)
        query = template.format(did_list=did_list, lookback_days=config.lookback_days)
        df = execute_query(config, query)
        if not df.empty:
            all_rows.append(df)
        if progress:
            print(f"  {label} batch {i // batch + 1}/{(n + batch - 1) // batch}: {len(df)} rows")
    if not all_rows:
        return pd.DataFrame()
    return pd.concat(all_rows, ignore_index=True)


_OUTBOUND_FOLLOWS_TPL = """
let cohort = dynamic([{did_list}]);
['Bluesky.Graph.Follow_v1']
| where did in (cohort)
| where ___time > ago({lookback_days}d)
| project did, subject, follow_time=___time, created_at=todatetime(created_at)
"""

_BLOCKS_TPL = """
let cohort = dynamic([{did_list}]);
['Bluesky.Graph.Block_v1']
| where subject in (cohort)
| summarize block_count = count() by subject
"""

_LIKES_TPL = """
let cohort = dynamic([{did_list}]);
['Bluesky.Feed.Like_v2']
| where did in (cohort)
| summarize like_count = count() by did
"""

_PROFILES_TPL = """
let targets = dynamic([{did_list}]);
['Bluesky.Actor.Profile_v2']
| where did in (targets)
| summarize arg_max(___time, *) by did
| project did, created_at, handle, display_name
"""


def acquire_all(config: Config, *, verbose: bool = True) -> AcquiredData:
    """Acquire the complete raw dataset required by the botfinder pipeline.
    
    Args:
        config: Runtime configuration describing the anchor account, lookback
            window, Kusto connection, and batching parameters.
        verbose: Whether to print stage-by-stage acquisition progress.
    
    Returns:
        AcquiredData: Raw cohort bundle consumed by scoring, cluster
        detection, and cross-follow analysis.
    
    Notes:
        The function first builds the anchor cohort from follows into the
        anchor, then enriches that cohort with outbound follows, received
        blocks, likes, and the latest profiles for both cohort members and
        frequently followed targets. Those downstream tables power overlap-based
        coordination signals and the co-follow graph.
    """

    if verbose:
        print(f"═══ Acquire: anchor=@{config.anchor_handle}, lookback={config.lookback_days}d ═══")

    target_did = _resolve_target_did(config)
    if verbose:
        print(f"  Target DID: {target_did}")

    follows_to_target = _extract_follows_to_target(config, target_did)
    if verbose:
        print(f"  Follows to target: {len(follows_to_target)}")

    cohort_dids: list[str] = (
        follows_to_target["follower_did"].dropna().unique().tolist()
        if not follows_to_target.empty else []
    )
    if verbose:
        print(f"  Cohort: {len(cohort_dids)}")

    follows_from_cohort = _batched_query(
        config, cohort_dids, _OUTBOUND_FOLLOWS_TPL, "outbound", progress=verbose
    )
    if verbose:
        print(f"  Outbound follows: {len(follows_from_cohort)}")

    blocks_received = _batched_query(
        config, cohort_dids, _BLOCKS_TPL, "blocks", progress=verbose
    )
    if blocks_received.empty:
        blocks_received = pd.DataFrame(columns=["subject", "block_count"])
    if verbose:
        print(f"  Blocked accounts: {len(blocks_received)}")

    likes_made = _batched_query(
        config, cohort_dids, _LIKES_TPL, "likes", progress=verbose
    )
    if likes_made.empty:
        likes_made = pd.DataFrame(columns=["did", "like_count"])
    if verbose:
        print(f"  Accounts with likes: {len(likes_made)}")

    profile_dids = list(set(cohort_dids))
    if not follows_from_cohort.empty:
        target_counts = follows_from_cohort["subject"].value_counts()
        frequent_targets = target_counts[target_counts >= 5].index.tolist()
        profile_dids = list(set(profile_dids + frequent_targets))
    profiles = _batched_query(
        config, profile_dids, _PROFILES_TPL, "profiles", progress=verbose
    )
    if profiles.empty:
        profiles = pd.DataFrame(columns=["did", "created_at", "handle", "display_name"])
    if verbose:
        print(f"  Profiles: {len(profiles)}")

    return AcquiredData(
        target_did=target_did,
        follows_to_target=follows_to_target,
        profiles=profiles,
        follows_from_cohort=follows_from_cohort,
        blocks_received=blocks_received.rename(columns={}),
        likes_made=likes_made,
    )
