"""KQL data acquisition — extract follows, profiles, blocks, likes for the
follower cohort of the anchor account.

Returns an in-memory ``AcquiredData`` bundle (no disk caching). Optional
parquet caching is exposed via ``AcquiredData.save`` / ``AcquiredData.load``
for local development.
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
    target_did: str
    follows_to_target: pd.DataFrame
    profiles: pd.DataFrame
    follows_from_cohort: pd.DataFrame
    blocks_received: pd.DataFrame
    likes_made: pd.DataFrame

    @property
    def cohort_dids(self) -> list[str]:
        if self.follows_to_target.empty:
            return []
        return self.follows_to_target["follower_did"].dropna().unique().tolist()

    def save(self, directory: Path) -> None:
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
    """Resolve target handle to DID via Bluesky API."""
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
    """Run a KQL query in cohort batches and concat the results."""
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
    """Extract everything we need for the analysis. Returns an
    in-memory ``AcquiredData`` bundle."""

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
