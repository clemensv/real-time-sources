# Bluesky Firehose Events

This document describes the CloudEvents that are emitted by the Bluesky Firehose Producer.

- [Bluesky.Feed](#message-group-blueskyfeed)
  - [Bluesky.Feed.Post](#message-blueskyfeedpost)
  - [Bluesky.Feed.Like](#message-blueskyfeedlike)
  - [Bluesky.Feed.Repost](#message-blueskyfeedrepost)
- [Bluesky.Graph](#message-group-blueskygraph)
  - [Bluesky.Graph.Follow](#message-blueskygraphfollow)
  - [Bluesky.Graph.Block](#message-blueskygraphblock)
- [Bluesky.Actor](#message-group-blueskyactor)
  - [Bluesky.Actor.Profile](#message-blueskyactorprofile)

---

## Message Group: Bluesky.Feed

Events related to Bluesky feed activities (posts, likes, reposts).

---

### Message: Bluesky.Feed.Post

A post in the Bluesky feed, including original posts and replies.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Post` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `False` | `{did}` |

#### Schema:

##### Record: Post

*A post in the Bluesky feed*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `uri` | *string* | AT-URI of the post (at://did:plc:xxx/app.bsky.feed.post/xxx) |
| `cid` | *string* | Content Identifier (CID) of the post |
| `did` | *string* | Decentralized Identifier of the author |
| `handle` | *string* (nullable) | Handle of the author (requires DID resolution, null in firehose) |
| `text` | *string* | Text content of the post |
| `langs` | *array of string* | Language codes for the post (max 3) |
| `reply_parent` | *string* (nullable) | AT-URI of parent post if this is a reply |
| `reply_parent_cid` | *string* (nullable) | CID of parent post if this is a reply |
| `reply_root` | *string* (nullable) | AT-URI of root post in thread |
| `reply_root_cid` | *string* (nullable) | CID of root post in thread |
| `embed_type` | *string* (nullable) | Type of embedded content (images, video, external, record, recordWithMedia) |
| `embed_uri` | *string* (nullable) | URI of embedded content (for external, record, recordWithMedia; null for images/video) |
| `facets` | *string* (nullable) | JSON string of rich text facets (mentions, links, hashtags) |
| `labels` | *string* (nullable) | JSON string of self-applied content labels (content warnings: porn, sexual, nudity, nsfl, gore, etc.) |
| `tags` | *array of string* | Additional hashtags in the post (max 8) |
| `created_at` | *string* | ISO 8601 timestamp of post creation |
| `indexed_at` | *string* | ISO 8601 timestamp of when the post was indexed |
| `seq` | *long* | Firehose sequence number |

---

### Message: Bluesky.Feed.Like

A like on a post.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Like` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `False` | `{did}` |

#### Schema:

##### Record: Like

*A like on a post*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `uri` | *string* | AT-URI of the like record |
| `cid` | *string* | Content Identifier of the like |
| `did` | *string* | DID of the user who liked |
| `handle` | *string* (nullable) | Handle of the user who liked |
| `subject_uri` | *string* | AT-URI of the liked post |
| `subject_cid` | *string* | CID of the liked post |
| `created_at` | *string* | ISO 8601 timestamp of like creation |
| `indexed_at` | *string* | ISO 8601 timestamp of indexing |
| `seq` | *long* | Firehose sequence number |

---

### Message: Bluesky.Feed.Repost

A repost of a post.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Repost` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `False` | `{did}` |

#### Schema:

##### Record: Repost

*A repost of a post*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `uri` | *string* | AT-URI of the repost record |
| `cid` | *string* | Content Identifier of the repost |
| `did` | *string* | DID of the user who reposted |
| `handle` | *string* (nullable) | Handle of the user who reposted |
| `subject_uri` | *string* | AT-URI of the reposted post |
| `subject_cid` | *string* | CID of the reposted post |
| `created_at` | *string* | ISO 8601 timestamp of repost creation |
| `indexed_at` | *string* | ISO 8601 timestamp of indexing |
| `seq` | *long* | Firehose sequence number |

---

## Message Group: Bluesky.Graph

Events related to the Bluesky social graph (follows, blocks).

---

### Message: Bluesky.Graph.Follow

A follow relationship between users.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Graph.Follow` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `False` | `{did}` |

#### Schema:

##### Record: Follow

*A follow relationship between users*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `uri` | *string* | AT-URI of the follow record |
| `cid` | *string* | Content Identifier of the follow |
| `did` | *string* | DID of the follower |
| `handle` | *string* (nullable) | Handle of the follower |
| `subject` | *string* | DID of the followed user |
| `subject_handle` | *string* (nullable) | Handle of the followed user |
| `created_at` | *string* | ISO 8601 timestamp of follow creation |
| `indexed_at` | *string* | ISO 8601 timestamp of indexing |
| `seq` | *long* | Firehose sequence number |

---

### Message: Bluesky.Graph.Block

A block relationship between users.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Graph.Block` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `False` | `{did}` |

#### Schema:

##### Record: Block

*A block relationship between users*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `uri` | *string* | AT-URI of the block record |
| `cid` | *string* | Content Identifier of the block |
| `did` | *string* | DID of the blocker |
| `handle` | *string* (nullable) | Handle of the blocker |
| `subject` | *string* | DID of the blocked user |
| `subject_handle` | *string* (nullable) | Handle of the blocked user |
| `created_at` | *string* | ISO 8601 timestamp of block creation |
| `indexed_at` | *string* | ISO 8601 timestamp of indexing |
| `seq` | *long* | Firehose sequence number |

---

## Message Group: Bluesky.Actor

Events related to Bluesky user profiles.

---

### Message: Bluesky.Actor.Profile

A user profile update.

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Actor.Profile` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `False` | `{did}` |

#### Schema:

##### Record: Profile

*A user profile update*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `did` | *string* | Decentralized Identifier |
| `handle` | *string* | User handle |
| `display_name` | *string* (nullable) | Display name |
| `description` | *string* (nullable) | Bio/description |
| `avatar` | *string* (nullable) | Avatar image URL |
| `banner` | *string* (nullable) | Banner image URL |
| `created_at` | *string* | ISO 8601 timestamp of profile creation |
| `indexed_at` | *string* | ISO 8601 timestamp of indexing |
| `seq` | *long* | Firehose sequence number |
