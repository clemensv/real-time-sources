"""Heuristic bot-scoring logic for Bluesky political-network analysis.

This module converts raw acquisition tables and optional API enrichment
into a composite 0–1 bot score for each cohort account. The signals are
tuned for the project's domain: accounts that are created shortly before
following the anchor, expose little identity information, mostly amplify
content, and share a follow graph with other suspects are more likely to
belong to a coordinated network rather than to genuine supporters or
opponents.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .bluesky_api import BlueskyProfile, BlueskyPost


@dataclass
class BotScore:
    """Structured result of scoring one cohort account.
    
    Attributes:
        did: Permanent DID of the scored account.
        handle: Current handle, if known.
        display_name: Current display name, if known.
        total_score: Composite bot-likelihood score from 0.0 to 1.0.
        signals: Individual signal scores that explain the composite result.
        flags: Human-readable labels for notable suspicious behaviors such as
            instant follows or anonymous profiles.
    """
    did: str
    handle: str
    display_name: str
    total_score: float  # 0.0 (human) to 1.0 (certain bot)
    signals: dict[str, float] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)


def score_temporal_proximity(age_at_follow_minutes: float) -> float:
    """Score how quickly an account followed the anchor after creation.
    
    Args:
        age_at_follow_minutes: Minutes between account creation and the follow
            event into the anchor.
    
    Returns:
        float: Suspicion score between 0.0 and 1.0.
    
    Notes:
        This signal targets throwaway accounts created specifically to attach to
        the anchor. Following within minutes is one of the clearest indicators
        of automation or preplanned coordination in the cohort. Unknown timing
        is treated as neutral rather than suspicious.
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
    """Score how anonymous or disposable an account appears.
    
    Args:
        profile: Resolved Bluesky profile, if one could be fetched.
        handle: Fallback handle string when the full profile is unavailable.
    
    Returns:
        float: Suspicion score between 0.0 and 1.0.
    
    Notes:
        Accounts with no avatar, no display name, no bio, and random-looking
        handles are more likely to be throwaway bot identities. Completely
        unresolvable accounts are scored most strongly because suspension or
        deletion is common among abusive campaign accounts.
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
    """Detect whether a handle looks auto-generated rather than human chosen.
    
    Args:
        handle: Bluesky handle to inspect.
    
    Returns:
        bool: ``True`` when the local part resembles alphanumeric gibberish or
        a short prefix followed by a long digit suffix.
    
    Notes:
        Random handles are not proof of abuse on their own, but in this domain
        they are a useful anonymity signal when combined with instant follows
        and sparse profile metadata.
    """
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
    """Score how much an account behaves like an amplifier instead of a person.
    
    Args:
        posts: Recent author-feed posts fetched from the Bluesky API.
        profile: Profile snapshot for context such as total post count.
    
    Returns:
        float: Suspicion score between 0.0 and 1.0.
    
    Notes:
        Accounts with no original content, extreme repost ratios,
        multilingual spray patterns, and near-zero engagement are more
        consistent with networked amplification than with ordinary political
        participation.
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
    """Score how strongly an account's follow graph overlaps suspect targets.
    
    Args:
        suspect_follows: Target DIDs followed by the account being scored.
        common_targets: Targets already identified as frequent co-follows among
            suspicious accounts.
        total_suspects: Total number of scored cohort accounts.
    
    Returns:
        float: Suspicion score between 0.0 and 1.0.
    
    Notes:
        A high score means the account is following the same external political
        targets as other suspects, which is a coordination signal. The
        ``total_suspects`` argument is kept for weighting symmetry with other
        scorers even though the current implementation only uses the shared
        target set.
    """
    if not suspect_follows or not common_targets:
        return 0.0
    overlap = len(set(suspect_follows) & common_targets)
    ratio = overlap / max(len(common_targets), 1)
    return min(ratio, 1.0)


def score_account_age(created_at: str, lookback_days: int = 7) -> float:
    """Score how newly created the account is relative to the analysis window.
    
    Args:
        created_at: Account creation timestamp from the profile or firehose.
        lookback_days: Width of the acquisition window for the anchor analysis.
    
    Returns:
        float: Suspicion score between 0.0 and 1.0.
    
    Notes:
        Brand-new accounts are more suspicious in this project because mass
        follower campaigns often mint large numbers of fresh identities shortly
        before they begin following political targets.
    """
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
    """Combine all bot signals into one explainable composite score.
    
    Args:
        did: DID of the account being scored.
        profile: Optional profile snapshot for anonymity and age signals.
        posts: Recent posts used for activity-pattern scoring.
        age_at_follow_minutes: Minutes from account creation to following the
            anchor, if known.
        suspect_follows_dids: Targets followed by this account.
        common_targets: Frequent co-follow targets derived from the suspect
            cohort.
        total_suspects: Total number of scored cohort accounts.
        lookback_days: Analysis lookback window used by the account-age scorer.
    
    Returns:
        BotScore: Composite score plus per-signal explanations and flags.
    
    Notes:
        Timing is weighted most heavily when it is available because instant
        follows are especially diagnostic. For older API-only followers with no
        precise follow timestamp, that weight is redistributed to profile,
        activity, and overlap signals so they are not unfairly penalized for
        missing data.
    """
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
    """Detect tight temporal bursts in account or follow timestamps.
    
    Args:
        df: Input DataFrame containing a timestamp column.
        time_col: Column name holding the timestamps to bucket.
        window: Resampling window such as ``"5min"``.
        threshold: Minimum event count required to label a bucket as a burst.
    
    Returns:
        pd.DataFrame: Burst windows with event counts and a relative intensity
        score.
    
    Notes:
        Temporal clustering is a common sign of centrally managed campaign
        behavior, such as account farms being created or deployed in batches.
    """
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    binned = df.set_index(time_col).resample(window).size().reset_index(name="count")
    bursts = binned[binned["count"] >= threshold].copy()
    bursts["burst_intensity"] = bursts["count"] / bursts["count"].mean() if len(bursts) > 0 else 0
    return bursts


def compute_network_statistics(scores: list[BotScore]) -> dict:
    """Aggregate cohort-wide statistics from per-account bot scores.
    
    Args:
        scores: Per-account score results for the analyzed cohort.
    
    Returns:
        dict: Summary metrics used by the dossier and CLI, including score
        distribution and flag prevalence.
    
    Notes:
        This is the bridge from individual suspect scoring to anchor-level
        narrative claims such as how many followers look highly automated and
        what fraction of the cohort followed instantly or anonymously.
    """
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
