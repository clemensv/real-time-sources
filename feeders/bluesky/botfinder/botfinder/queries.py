"""KQL queries for bot network analysis.

All queries accept a `target_did` parameter (the resolved DID of the target account).
DID resolution is handled by the caller via the Bluesky API before query execution.
"""

TARGET_RESOLUTION = """
['Bluesky.Actor.Profile_v2']
| where did == "{target_did}"
| top 1 by ___time desc
| project did
"""

NEW_FOLLOWERS_DETAIL = """
let target_did = "{target_did}";
let follows = ['Bluesky.Graph.Follow_v1']
| where subject == target_did
| join kind=leftouter (
    ['Bluesky.Actor.Profile_v2']
    | project follower_did=did, follower_display_name=display_name,
              follower_handle=handle, follower_created_at=created_at,
              follower_description=description, follower_avatar=avatar
) on $left.did == $right.follower_did
| summarize arg_max(ingestion_time(), *) by follower_did
| project follower_did, follower_display_name, follower_handle,
          follower_created_at=todatetime(follower_created_at),
          follow_created_at=todatetime(created_at),
          follower_description, follower_avatar
| where isnotempty(follower_created_at) and follower_created_at > ago({lookback_days}d);
follows
| extend age_at_follow_minutes = datetime_diff('minute', follow_created_at, follower_created_at)
| order by follower_created_at asc
"""

FOLLOW_TIMECHART = """
let target_did = "{target_did}";
let follows = ['Bluesky.Graph.Follow_v1']
| where subject == target_did
| join kind=leftouter (
    ['Bluesky.Actor.Profile_v2']
    | project follower_did=did, follower_created_at=created_at
) on $left.did == $right.follower_did
| summarize arg_max(ingestion_time(), *) by follower_did
| project follower_did, follower_created_at=todatetime(follower_created_at),
          follow_created_at=todatetime(created_at)
| where isnotempty(follower_created_at) and follower_created_at > ago({lookback_days}d);
follows
| summarize count() by bin(follow_created_at, {bin_size})
| order by follow_created_at asc
"""

ACCOUNT_CREATION_TIMECHART = """
let target_did = "{target_did}";
let follows = ['Bluesky.Graph.Follow_v1']
| where subject == target_did
| join kind=leftouter (
    ['Bluesky.Actor.Profile_v2']
    | project follower_did=did, follower_created_at=created_at
) on $left.did == $right.follower_did
| summarize arg_max(ingestion_time(), *) by follower_did
| project follower_did, follower_created_at=todatetime(follower_created_at),
          follow_created_at=todatetime(created_at)
| where isnotempty(follower_created_at) and follower_created_at > ago({lookback_days}d);
follows
| summarize count() by bin(follower_created_at, {bin_size})
| order by follower_created_at asc
"""

FOLLOW_OVERLAP = """
let target_did = "{target_did}";
let suspect_dids = ['Bluesky.Graph.Follow_v1']
| where subject == target_did
| join kind=leftouter (
    ['Bluesky.Actor.Profile_v2']
    | project follower_did=did, follower_created_at=created_at
) on $left.did == $right.follower_did
| summarize arg_max(ingestion_time(), *) by follower_did
| where isnotempty(follower_created_at) and todatetime(follower_created_at) > ago({lookback_days}d)
| where datetime_diff('minute', todatetime(created_at), todatetime(follower_created_at)) < 60
| project follower_did;
['Bluesky.Graph.Follow_v1']
| where did in (suspect_dids)
| join kind=leftouter (
    ['Bluesky.Actor.Profile_v2']
    | project target_did2=did, target_display_name=display_name, target_handle=handle
) on $left.subject == $right.target_did2
| summarize followers=dcount(did), follower_list=make_set(did, 100) by subject, target_display_name, target_handle
| where followers > 5
| order by followers desc
| take 50
"""

SUMMARY_STATS = """
let target_did = "{target_did}";
let follows = ['Bluesky.Graph.Follow_v1']
| where subject == target_did
| join kind=leftouter (
    ['Bluesky.Actor.Profile_v2']
    | project follower_did=did, follower_created_at=created_at,
              follower_display_name=display_name, follower_avatar=avatar,
              follower_description=description
) on $left.did == $right.follower_did
| summarize arg_max(ingestion_time(), *) by follower_did
| project follower_did, follower_created_at=todatetime(follower_created_at),
          follow_created_at=todatetime(created_at),
          follower_display_name, follower_avatar, follower_description
| where isnotempty(follower_created_at) and follower_created_at > ago({lookback_days}d)
| extend age_at_follow_minutes = datetime_diff('minute', follow_created_at, follower_created_at);
follows
| summarize
    total_new_followers = count(),
    median_age_minutes = percentile(age_at_follow_minutes, 50),
    p10_age_minutes = percentile(age_at_follow_minutes, 10),
    p90_age_minutes = percentile(age_at_follow_minutes, 90),
    under_1h = countif(age_at_follow_minutes < 60),
    under_5m = countif(age_at_follow_minutes < 5),
    under_1m = countif(age_at_follow_minutes < 1),
    no_display_name = countif(isempty(follower_display_name)),
    no_avatar = countif(isempty(follower_avatar)),
    no_description = countif(isempty(follower_description)),
    earliest_account = min(follower_created_at),
    latest_account = max(follower_created_at)
"""
