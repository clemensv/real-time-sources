"""Bot behavior scoring and network analysis.

Implements heuristics based on DFRLab's bot detection methodology and
academic research on coordinated inauthentic behavior (CIB):

Signals scored:
1. Account age at first follow (temporal proximity)
2. Profile completeness (anonymity)
3. Activity volume and patterns
4. Follow overlap (coordinated following)
5. Posting behavior (amplification vs. original content)
6. Handle pattern analysis (random alphanumeric handles)
7. Temporal burst detection (synchronized account creation)
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .bluesky_api import BlueskyProfile, BlueskyPost


@dataclass
class BotScore:
    did: str
    handle: str
    display_name: str
    total_score: float  # 0.0 (human) to 1.0 (certain bot)
    signals: dict[str, float] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)


def score_temporal_proximity(age_at_follow_minutes: float) -> float:
    """Score based on how quickly after creation the account followed the target.

    < 1 min: 1.0 (instant follow = strong bot signal)
    < 5 min: 0.9
    < 30 min: 0.7
    < 60 min: 0.5
    < 240 min (4h): 0.3
    > 24h: 0.0
    NaN: 0.0 (unknown — don't penalize)
    """
    if pd.isna(age_at_follow_minutes):
        return 0.0  # Unknown timing — rely on other signals
    if age_at_follow_minutes < 1:
        return 1.0
    if age_at_follow_minutes < 5:
        return 0.9
    if age_at_follow_minutes < 30:
        return 0.7
    if age_at_follow_minutes < 60:
        return 0.5
    if age_at_follow_minutes < 240:
        return 0.3
    if age_at_follow_minutes < 1440:
        return 0.1
    return 0.0


def score_profile_completeness(profile: BlueskyProfile | None, handle: str = "") -> float:
    """Score anonymity — incomplete profiles are more suspicious.

    Unresolvable/deleted account: 1.0 (strongest signal)
    Missing avatar: +0.25
    Missing display name: +0.25
    Missing description/bio: +0.25
    Default/random handle: +0.25
    """
    if not profile:
        if not handle:
            return 1.0  # Deleted/suspended account that still appears as follower
        return 0.75  # Can't resolve but has a handle
    score = 0.0
    if not profile.avatar:
        score += 0.25
    if not profile.display_name:
        score += 0.25
    if not profile.description:
        score += 0.25
    if _is_random_handle(profile.handle):
        score += 0.25
    return score


def _is_random_handle(handle: str) -> bool:
    """Detect likely auto-generated handles (alphanumeric gibberish)."""
    local_part = handle.split(".")[0] if "." in handle else handle
    if not local_part:
        return True
    if len(local_part) > 12 and re.match(r"^[a-z0-9]+$", local_part):
        digit_ratio = sum(c.isdigit() for c in local_part) / len(local_part)
        if digit_ratio > 0.4:
            return True
    if re.match(r"^[a-z]{2,4}\d{5,}$", local_part):
        return True
    return False


def score_activity_pattern(posts: list[BlueskyPost], profile: BlueskyProfile | None) -> float:
    """Score based on posting behavior analysis.

    High amplification (repost ratio): suspicious
    No original content: suspicious
    Zero posts from a new account following someone: strong signal
    Burst posting: suspicious
    """
    if not posts:
        if profile and profile.posts_count == 0:
            return 0.8  # Zero posts = purpose-built follow account
        if not profile:
            return 0.6  # Can't assess, but absence of data for new account is suspicious
        return 0.3  # Has posts but we didn't fetch them

    total = len(posts)
    reposts = sum(1 for p in posts if p.is_repost)
    replies = sum(1 for p in posts if p.is_reply)
    original = total - reposts - replies

    score = 0.0

    # High repost ratio
    repost_ratio = reposts / total if total > 0 else 0
    if repost_ratio > 0.9:
        score += 0.4
    elif repost_ratio > 0.7:
        score += 0.2

    # No original content
    if original == 0 and total > 5:
        score += 0.3

    # Check for language diversity (multilingual bots)
    all_langs = set()
    for p in posts:
        all_langs.update(p.langs)
    if len(all_langs) > 3:
        score += 0.2

    # Low engagement received
    avg_likes = np.mean([p.like_count for p in posts]) if posts else 0
    if avg_likes < 0.5 and total > 10:
        score += 0.1

    return min(score, 1.0)


def score_follow_overlap(
    suspect_follows: list[str], common_targets: set[str], total_suspects: int
) -> float:
    """Score based on how many of the same accounts this suspect follows
    compared to other suspects in the cluster.

    High overlap = coordinated behavior.
    """
    if not suspect_follows or not common_targets:
        return 0.0
    overlap = len(set(suspect_follows) & common_targets)
    ratio = overlap / max(len(common_targets), 1)
    return min(ratio, 1.0)


def score_account_age(created_at: str, lookback_days: int = 7) -> float:
    """Score based on account age. Accounts created within the analysis window are suspicious."""
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        age_hours = (datetime.now(timezone.utc) - created).total_seconds() / 3600
        lookback_hours = lookback_days * 24
        if age_hours < 6:
            return 1.0
        if age_hours < 24:
            return 0.9
        if age_hours < 48:
            return 0.8
        if age_hours < 72:
            return 0.7
        if age_hours < lookback_hours:
            return 0.6
        return 0.0
    except (ValueError, TypeError):
        return 0.5


def compute_bot_score(
    did: str,
    profile: BlueskyProfile | None,
    posts: list[BlueskyPost],
    age_at_follow_minutes: float,
    suspect_follows_dids: list[str],
    common_targets: set[str],
    total_suspects: int,
    lookback_days: int = 7,
) -> BotScore:
    """Compute composite bot score from all signals."""
    signals = {}
    flags = []

    # Signal 1: Temporal proximity
    signals["temporal_proximity"] = score_temporal_proximity(age_at_follow_minutes)
    if signals["temporal_proximity"] >= 0.9:
        flags.append("INSTANT_FOLLOW")

    # Signal 2: Profile completeness
    handle_str = profile.handle if profile else ""
    signals["anonymity"] = score_profile_completeness(profile, handle=handle_str)
    if signals["anonymity"] >= 0.75:
        flags.append("ANONYMOUS_PROFILE")
    if signals["anonymity"] >= 1.0:
        flags.append("DELETED_OR_SUSPENDED")

    # Signal 3: Activity pattern
    signals["activity_pattern"] = score_activity_pattern(posts, profile)
    if signals["activity_pattern"] >= 0.6:
        flags.append("AMPLIFICATION_BOT")

    # Signal 4: Follow overlap
    signals["follow_overlap"] = score_follow_overlap(
        suspect_follows_dids, common_targets, total_suspects
    )
    if signals["follow_overlap"] >= 0.5:
        flags.append("COORDINATED_FOLLOWING")

    # Signal 5: Account age
    created_at = profile.created_at if profile else ""
    signals["account_age"] = score_account_age(created_at, lookback_days)
    if signals["account_age"] >= 0.7:
        flags.append("BRAND_NEW_ACCOUNT")

    # Adaptive weighted composite score
    # When temporal_proximity is unknown (API-sourced older accounts),
    # redistribute its weight to other signals
    has_timing = not pd.isna(age_at_follow_minutes)
    if has_timing:
        weights = {
            "temporal_proximity": 0.30,
            "anonymity": 0.15,
            "activity_pattern": 0.20,
            "follow_overlap": 0.20,
            "account_age": 0.15,
        }
    else:
        # No timing data — weight shifts to profile + activity + overlap
        weights = {
            "temporal_proximity": 0.00,
            "anonymity": 0.25,
            "activity_pattern": 0.30,
            "follow_overlap": 0.30,
            "account_age": 0.15,
        }
    total_score = sum(signals[k] * weights[k] for k in weights)

    handle = profile.handle if profile else ""
    display_name = profile.display_name if profile else ""

    return BotScore(
        did=did,
        handle=handle,
        display_name=display_name,
        total_score=total_score,
        signals=signals,
        flags=flags,
    )


def detect_temporal_bursts(
    df: pd.DataFrame, time_col: str, window: str = "5min", threshold: int = 5
) -> pd.DataFrame:
    """Detect bursts of coordinated activity within tight time windows.

    Returns DataFrame with burst windows and account counts.
    """
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    binned = df.set_index(time_col).resample(window).size().reset_index(name="count")
    bursts = binned[binned["count"] >= threshold].copy()
    bursts["burst_intensity"] = bursts["count"] / bursts["count"].mean() if len(bursts) > 0 else 0
    return bursts


def compute_network_statistics(scores: list[BotScore]) -> dict:
    """Aggregate network-level statistics for the dossier."""
    if not scores:
        return {}

    total = len(scores)
    high_confidence = [s for s in scores if s.total_score >= 0.7]
    medium_confidence = [s for s in scores if 0.4 <= s.total_score < 0.7]
    low_confidence = [s for s in scores if s.total_score < 0.4]

    all_scores = [s.total_score for s in scores]
    flag_counts: dict[str, int] = {}
    for s in scores:
        for f in s.flags:
            flag_counts[f] = flag_counts.get(f, 0) + 1

    return {
        "total_suspects": total,
        "high_confidence_bots": len(high_confidence),
        "medium_confidence_bots": len(medium_confidence),
        "low_confidence": len(low_confidence),
        "mean_score": float(np.mean(all_scores)),
        "median_score": float(np.median(all_scores)),
        "p90_score": float(np.percentile(all_scores, 90)),
        "flag_distribution": flag_counts,
        "pct_instant_follow": flag_counts.get("INSTANT_FOLLOW", 0) / total * 100,
        "pct_anonymous": flag_counts.get("ANONYMOUS_PROFILE", 0) / total * 100,
        "pct_coordinated": flag_counts.get("COORDINATED_FOLLOWING", 0) / total * 100,
    }
