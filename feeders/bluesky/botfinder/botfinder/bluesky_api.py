"""Async Bluesky AT Protocol client used to enrich KQL-derived cohorts.

The acquisition stage gets broad firehose coverage from Kusto, but several
scoring and graph signals need live public API lookups: profiles, recent
posts, follows, and followers. This module wraps the public ``bsky.app``
XRPC endpoints into typed dataclasses that downstream scoring, cluster, and
cross-follow stages can consume without parsing raw JSON repeatedly.
"""

import os
import httpx
import asyncio
from dataclasses import dataclass, field
from datetime import datetime


XRPC_BASE = "https://public.api.bsky.app/xrpc"

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-bluesky/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)


@dataclass
class BlueskyProfile:
    """Normalized snapshot of a Bluesky actor profile.
    
    The scoring stage uses these fields to judge anonymity and account age, and
    the dossier uses handles and display names to make suspect rows readable.
    
    Attributes:
        did: Permanent decentralized identifier for the account.
        handle: Current Bluesky handle, which may change over time.
        display_name: Human-readable profile name shown in the UI.
        description: Profile bio text.
        avatar: Avatar URL; missing avatars are part of the anonymity signal.
        banner: Banner image URL.
        created_at: Account creation timestamp from the public API.
        followers_count: Number of followers the account currently has.
        follows_count: Number of accounts the actor follows.
        posts_count: Number of posts on the account.
        labels: Moderation or classification labels returned by Bluesky.
        indexed_at: When Bluesky last indexed this profile snapshot.
    """

    did: str
    handle: str
    display_name: str
    description: str
    avatar: str
    banner: str
    created_at: str
    followers_count: int
    follows_count: int
    posts_count: int
    labels: list[str] = field(default_factory=list)
    indexed_at: str = ""


@dataclass
class BlueskyPost:
    """Normalized author-feed item used for activity-pattern scoring.
    
    The scoring stage looks at repost ratios, reply-heavy behavior,
    language diversity, and low-engagement posting to detect amplification
    accounts that mainly boost political narratives instead of acting like
    organic users.
    """

    uri: str
    cid: str
    text: str
    created_at: str
    reply_count: int
    repost_count: int
    like_count: int
    is_reply: bool
    is_repost: bool
    langs: list[str] = field(default_factory=list)


@dataclass
class FollowRecord:
    """Compact follow-edge record returned by Bluesky graph endpoints.
    
    Instances represent either who an account follows or who follows it,
    depending on the endpoint. These records feed cohort extension, co-follow
    overlap measurements, and cross-follow sampling.
    """

    did: str
    handle: str
    display_name: str
    created_at: str
    indexed_at: str


class BlueskyClient:
    """Rate-limited async client for the public Bluesky XRPC API.
    
    The client centralizes retry, concurrency control, and JSON-to-dataclass
    conversion so the rest of the pipeline can ask domain-level questions such
    as which profiles look anonymous, what suspects post, and which other
    political targets they follow.
    """

    def __init__(self, concurrency: int = 10, timeout: float = 30.0):
        """Configure concurrency and timeout limits for Bluesky API calls.
        
        Args:
            concurrency: Maximum number of concurrent requests allowed from this
                client instance.
            timeout: Request timeout in seconds.
        """
        self._semaphore = asyncio.Semaphore(concurrency)
        self._timeout = timeout

    async def _get(self, client: httpx.AsyncClient, endpoint: str, params: dict) -> dict | None:
        """Issue a single XRPC GET request with lightweight rate-limit handling.
        
        Args:
            client: Shared async HTTP client.
            endpoint: XRPC method path relative to ``XRPC_BASE``.
            params: Query-string parameters for the endpoint.
        
        Returns:
            dict | None: Parsed JSON response on success, otherwise ``None``.
        
        Notes:
            The public Bluesky API occasionally returns HTTP 429 while crawling
            suspect cohorts. The helper honors ``retry-after`` once so scoring and
            graph stages degrade gracefully instead of failing the run.
        """
        async with self._semaphore:
            try:
                resp = await client.get(f"{XRPC_BASE}/{endpoint}", params=params)
                if resp.status_code == 200:
                    return resp.json()
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("retry-after", "2"))
                    await asyncio.sleep(retry_after)
                    resp = await client.get(f"{XRPC_BASE}/{endpoint}", params=params)
                    if resp.status_code == 200:
                        return resp.json()
                return None
            except httpx.HTTPError:
                return None

    async def get_profile(self, client: httpx.AsyncClient, actor: str) -> BlueskyProfile | None:
        """Fetch one profile for a DID or handle.
        
        Args:
            client: Shared async HTTP client.
            actor: DID or handle to resolve.
        
        Returns:
            BlueskyProfile | None: Normalized profile, or ``None`` when the account
            is unavailable or the request fails.
        """
        data = await self._get(client, "app.bsky.actor.getProfile", {"actor": actor})
        if not data:
            return None
        return BlueskyProfile(
            did=data.get("did", actor),
            handle=data.get("handle", ""),
            display_name=data.get("displayName", ""),
            description=data.get("description", ""),
            avatar=data.get("avatar", ""),
            banner=data.get("banner", ""),
            created_at=data.get("createdAt", ""),
            followers_count=data.get("followersCount", 0),
            follows_count=data.get("followsCount", 0),
            posts_count=data.get("postsCount", 0),
            labels=[lbl.get("val", "") for lbl in data.get("labels", [])],
            indexed_at=data.get("indexedAt", ""),
        )

    async def get_profiles_batch(
        self, client: httpx.AsyncClient, actors: list[str]
    ) -> list[BlueskyProfile]:
        """Fetch a batch of profile snapshots for enrichment-heavy stages.
        
        Args:
            client: Shared async HTTP client.
            actors: DIDs or handles to resolve. Bluesky accepts at most 25 per
                request, so larger input is truncated by this helper.
        
        Returns:
            list[BlueskyProfile]: Parsed profile dataclasses for all rows the API
            returned successfully.
        """
        data = await self._get(client, "app.bsky.actor.getProfiles", {"actors": actors[:25]})
        if not data:
            return []
        profiles = []
        for p in data.get("profiles", []):
            profiles.append(BlueskyProfile(
                did=p.get("did", ""),
                handle=p.get("handle", ""),
                display_name=p.get("displayName", ""),
                description=p.get("description", ""),
                avatar=p.get("avatar", ""),
                banner=p.get("banner", ""),
                created_at=p.get("createdAt", ""),
                followers_count=p.get("followersCount", 0),
                follows_count=p.get("followsCount", 0),
                posts_count=p.get("postsCount", 0),
                labels=[lbl.get("val", "") for lbl in p.get("labels", [])],
                indexed_at=p.get("indexedAt", ""),
            ))
        return profiles

    async def get_author_feed(
        self, client: httpx.AsyncClient, actor: str, limit: int = 30
    ) -> list[BlueskyPost]:
        """Fetch recent posts from a suspect for activity-pattern scoring.
        
        Args:
            client: Shared async HTTP client.
            actor: DID or handle whose author feed should be inspected.
            limit: Maximum number of feed items to inspect.
        
        Returns:
            list[BlueskyPost]: Recent posts normalized into scoring-friendly
            dataclasses.
        
        Notes:
            The scoring module uses this feed to spot amplification-heavy
            accounts that mostly repost, rarely create original content, and
            receive little engagement.
        """
        data = await self._get(
            client, "app.bsky.feed.getAuthorFeed",
            {"actor": actor, "limit": min(limit, 100), "filter": "posts_and_author_threads"},
        )
        if not data:
            return []
        posts = []
        for item in data.get("feed", []):
            post = item.get("post", {})
            record = post.get("record", {})
            posts.append(BlueskyPost(
                uri=post.get("uri", ""),
                cid=post.get("cid", ""),
                text=record.get("text", ""),
                created_at=record.get("createdAt", ""),
                reply_count=post.get("replyCount", 0),
                repost_count=post.get("repostCount", 0),
                like_count=post.get("likeCount", 0),
                is_reply="reply" in record,
                is_repost="reason" in item and item["reason"].get("$type") == "app.bsky.feed.defs#reasonRepost",
                langs=record.get("langs", []),
            ))
        return posts

    async def get_follows(
        self, client: httpx.AsyncClient, actor: str, limit: int = 100
    ) -> list[FollowRecord]:
        """Fetch accounts followed by an actor.
        
        Args:
            client: Shared async HTTP client.
            actor: DID or handle whose outbound follows should be fetched.
            limit: Maximum number of follow edges to collect.
        
        Returns:
            list[FollowRecord]: Follow edges suitable for co-follow overlap and
            cluster-graph construction.
        
        Notes:
            Shared outbound follows are one of the clearest coordination signals in
            this project: bot operators often point many throwaway accounts at the
            same political targets.
        """
        records: list[FollowRecord] = []
        cursor = None
        while len(records) < limit:
            params: dict = {"actor": actor, "limit": min(100, limit - len(records))}
            if cursor:
                params["cursor"] = cursor
            data = await self._get(client, "app.bsky.graph.getFollows", params)
            if not data:
                break
            for f in data.get("follows", []):
                records.append(FollowRecord(
                    did=f.get("did", ""),
                    handle=f.get("handle", ""),
                    display_name=f.get("displayName", ""),
                    created_at=f.get("createdAt", ""),
                    indexed_at=f.get("indexedAt", ""),
                ))
            cursor = data.get("cursor")
            if not cursor:
                break
        return records

    async def get_followers(
        self, client: httpx.AsyncClient, actor: str, limit: int = 100
    ) -> list[FollowRecord]:
        """Fetch followers of an anchor account from the public API.
        
        Args:
            client: Shared async HTTP client.
            actor: DID or handle whose followers should be enumerated.
            limit: Maximum number of followers to return.
        
        Returns:
            list[FollowRecord]: Follower records used to extend the cohort beyond
            the KQL lookback window.
        """
        records: list[FollowRecord] = []
        cursor = None
        while len(records) < limit:
            params: dict = {"actor": actor, "limit": min(100, limit - len(records))}
            if cursor:
                params["cursor"] = cursor
            data = await self._get(client, "app.bsky.graph.getFollowers", params)
            if not data:
                break
            for f in data.get("followers", []):
                records.append(FollowRecord(
                    did=f.get("did", ""),
                    handle=f.get("handle", ""),
                    display_name=f.get("displayName", ""),
                    created_at=f.get("createdAt", ""),
                    indexed_at=f.get("indexedAt", ""),
                ))
            cursor = data.get("cursor")
            if not cursor:
                break
        return records


async def enrich_suspects(
    dids: list[str], concurrency: int = 10
) -> dict[str, dict]:
    """Enrich suspect accounts with the API data needed for scoring.
    
    Args:
        dids: Suspect or priority cohort DIDs selected by ``run_analysis``.
        concurrency: Maximum parallel request count for the underlying client.
    
    Returns:
        dict[str, dict]: Mapping from DID to a dictionary containing a profile
        snapshot, recent posts, and outbound follows.
    
    Notes:
        This function bridges acquisition and scoring. KQL provides the broad
        cohort, while this helper selectively enriches the most suspicious or
        analytically useful accounts so later heuristics can inspect anonymity,
        posting behavior, and follow overlap in detail.
    """
    bsky = BlueskyClient(concurrency=concurrency)
    results: dict[str, dict] = {}

    async with httpx.AsyncClient(timeout=30.0, headers={"User-Agent": USER_AGENT}) as client:
        # Batch-resolve profiles (25 per request)
        all_profiles: dict[str, BlueskyProfile] = {}
        for i in range(0, len(dids), 25):
            batch = dids[i:i + 25]
            profiles = await bsky.get_profiles_batch(client, batch)
            for p in profiles:
                all_profiles[p.did] = p

        # Fetch feeds + follows for top suspects concurrently
        async def _enrich_one(did: str) -> None:
            """Fetch per-account activity and follow data for one suspect DID."""
            profile = all_profiles.get(did)
            posts = await bsky.get_author_feed(client, did, limit=50)
            follows = await bsky.get_follows(client, did, limit=100)
            results[did] = {
                "profile": profile,
                "posts": posts,
                "follows": follows,
            }

        tasks = [_enrich_one(did) for did in dids]
        await asyncio.gather(*tasks)

    return results


def enrich_suspects_sync(dids: list[str], concurrency: int = 10) -> dict[str, dict]:
    """Run :func:`enrich_suspects` from synchronous pipeline code.
    
    Args:
        dids: Suspect DIDs to enrich.
        concurrency: Maximum parallel request count.
    
    Returns:
        dict[str, dict]: Same structure as :func:`enrich_suspects`.
    """
    from ._async import run_async
    return run_async(enrich_suspects(dids, concurrency))
