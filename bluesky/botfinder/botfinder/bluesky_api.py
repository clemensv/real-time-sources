"""Bluesky AT Protocol API client for enriching bot detection data."""

import httpx
import asyncio
from dataclasses import dataclass, field
from datetime import datetime


XRPC_BASE = "https://public.api.bsky.app/xrpc"


@dataclass
class BlueskyProfile:
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
    did: str
    handle: str
    display_name: str
    created_at: str
    indexed_at: str


class BlueskyClient:
    """Public Bluesky API client for bot analysis enrichment."""

    def __init__(self, concurrency: int = 10, timeout: float = 30.0):
        self._semaphore = asyncio.Semaphore(concurrency)
        self._timeout = timeout

    async def _get(self, client: httpx.AsyncClient, endpoint: str, params: dict) -> dict | None:
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
        """Fetch up to 25 profiles in a single request."""
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
        """Get recent posts from an account to assess activity patterns."""
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
        """Get accounts that an actor follows — to detect follow-overlap in the botnet."""
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
        """Get followers of an account."""
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
    """Enrich a list of suspect DIDs with full profile + feed data from the Bluesky API.

    Returns a dict keyed by DID with profile, posts, and follows data.
    """
    bsky = BlueskyClient(concurrency=concurrency)
    results: dict[str, dict] = {}

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Batch-resolve profiles (25 per request)
        all_profiles: dict[str, BlueskyProfile] = {}
        for i in range(0, len(dids), 25):
            batch = dids[i:i + 25]
            profiles = await bsky.get_profiles_batch(client, batch)
            for p in profiles:
                all_profiles[p.did] = p

        # Fetch feeds + follows for top suspects concurrently
        async def _enrich_one(did: str) -> None:
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
    from ._async import run_async
    return run_async(enrich_suspects(dids, concurrency))
