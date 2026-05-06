"""Build the follow co-occurrence cluster graph for the suspect cohort.

Pure-functional refactor of ``scripts/cluster_graph.py`` and
``tmp/cluster_graph.py``. Returns a :class:`ClusterResult` dataclass with
nodes, edges and an interactive Plotly figure ready for inline display.
"""

from __future__ import annotations

import asyncio
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .bluesky_api import BlueskyClient

if TYPE_CHECKING:  # pragma: no cover
    from .pipeline import AnalysisResult


@dataclass
class ClusterResult:
    nodes_df: pd.DataFrame
    edges_df: pd.DataFrame
    figure: go.Figure
    target_did: str
    target_handle: str


async def _fetch_follows_for_suspects(
    suspect_dids: list[str],
    concurrency: int,
    limit_per_account: int,
) -> dict[str, list[str]]:
    bsky = BlueskyClient(concurrency=concurrency)
    results: dict[str, list[str]] = {}
    async with httpx.AsyncClient(timeout=30.0) as client:
        sem = asyncio.Semaphore(concurrency)

        async def _get_one(did: str):
            async with sem:
                try:
                    follows = await bsky.get_follows(client, did, limit=limit_per_account)
                    results[did] = [f.did for f in follows]
                except Exception:
                    results[did] = []

        await asyncio.gather(*[_get_one(did) for did in suspect_dids])
    return results


async def _resolve_handles(dids: list[str], concurrency: int = 25) -> dict[str, str]:
    bsky = BlueskyClient(concurrency=concurrency)
    handles: dict[str, str] = {}
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i in range(0, len(dids), 25):
            batch = dids[i: i + 25]
            try:
                profiles = await bsky.get_profiles_batch(client, batch)
                for p in profiles:
                    handles[p.did] = p.handle or p.did[:16]
            except Exception:
                for d in batch:
                    handles[d] = d[:16]
    return handles


def _build_graph(
    suspect_follows: dict[str, list[str]],
    min_followers: int,
) -> tuple[nx.Graph, dict[str, int]]:
    target_counts: Counter = Counter()
    for did, follows in suspect_follows.items():
        for fdid in follows:
            target_counts[fdid] += 1

    significant = {d: c for d, c in target_counts.items() if c >= min_followers}
    G = nx.Graph()
    for d, c in significant.items():
        G.add_node(d, weight=c)

    target_list = list(significant.keys())
    suspect_to_targets: dict[str, set[str]] = defaultdict(set)
    for s_did, follows in suspect_follows.items():
        for fdid in follows:
            if fdid in significant:
                suspect_to_targets[s_did].add(fdid)

    for i in range(len(target_list)):
        for j in range(i + 1, len(target_list)):
            t1, t2 = target_list[i], target_list[j]
            shared = sum(1 for ts in suspect_to_targets.values() if t1 in ts and t2 in ts)
            if shared >= min_followers:
                G.add_edge(t1, t2, weight=shared)
    return G, significant


def _render_figure(
    G: nx.Graph,
    handles: dict[str, str],
    target_did: str,
    target_handle: str,
) -> go.Figure:
    if len(G.nodes()) == 0:
        return go.Figure().update_layout(title="No significant cluster found")

    try:
        pos = nx.spring_layout(G, k=2.0 / np.sqrt(len(G.nodes())), iterations=100, seed=42, weight="weight")
    except Exception:
        pos = nx.circular_layout(G)

    weights = nx.get_node_attributes(G, "weight")
    max_w = max(weights.values()) if weights else 1

    node_x, node_y, node_text, node_size, node_color = [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x); node_y.append(y)
        w = weights.get(node, 0)
        handle = handles.get(node, node[:16])
        node_text.append(f"@{handle}<br>Suspects following: {w}<br>Connections: {G.degree(node)}")
        node_size.append(max(10, 60 * (w / max_w)))
        if node == target_did:
            node_color.append("crimson")
        elif w >= max_w * 0.5:
            node_color.append("darkorange")
        elif w >= max_w * 0.25:
            node_color.append("gold")
        else:
            node_color.append("lightblue")

    edge_traces = []
    edge_weights = [G[u][v].get("weight", 1) for u, v in G.edges()]
    max_edge = max(edge_weights) if edge_weights else 1
    for (u, v), ew in zip(G.edges(), edge_weights):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        width = max(0.5, 4 * (ew / max_edge))
        opacity = max(0.2, 0.8 * (ew / max_edge))
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None], mode="lines",
            line=dict(width=width, color=f"rgba(80,80,80,{opacity})"),
            hoverinfo="none", showlegend=False,
        ))

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=[handles.get(n, n[:12]) for n in G.nodes()],
        textposition="top center",
        textfont=dict(size=9, color="#1a1a1a"),
        marker=dict(size=node_size, color=node_color, line=dict(width=1, color="#333333")),
        hovertext=node_text, hoverinfo="text", showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title=dict(
            text=f"Follow Cluster Network — @{target_handle}<br>"
                 "<sup>Node size = #suspects following, edges = shared followers</sup>",
            font=dict(size=16),
        ),
        template="plotly_white", width=1400, height=900,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=80, b=20),
    )
    return fig


def build_cluster_graph(
    analysis: "AnalysisResult",
    *,
    min_followers: int = 5,
    classify_top: int = 200,
    verbose: bool = True,
) -> ClusterResult:
    config = analysis.config
    scores_df = analysis.scores_df
    suspects = scores_df[scores_df["score"] >= config.cluster_score_threshold]
    suspect_dids = suspects.sort_values("score", ascending=False)["did"].tolist()
    if verbose:
        print(f"  Cluster suspects (score≥{config.cluster_score_threshold}): {len(suspect_dids)}")

    if not suspect_dids:
        empty = pd.DataFrame()
        return ClusterResult(empty, empty, go.Figure(), analysis.acquired.target_did, config.anchor_handle)

    suspect_follows = asyncio.run(
        _fetch_follows_for_suspects(suspect_dids, config.api_concurrency, limit_per_account=200)
    )
    if verbose:
        total = sum(len(f) for f in suspect_follows.values())
        print(f"  Suspect follow edges fetched: {total}")

    G, target_weights = _build_graph(suspect_follows, min_followers=min_followers)
    if verbose:
        print(f"  Graph: {len(G.nodes())} nodes / {len(G.edges())} edges")

    target_dids = list(G.nodes())
    handles = asyncio.run(_resolve_handles(target_dids, concurrency=25)) if target_dids else {}

    edges_data = [
        {"source": handles.get(u, u), "target": handles.get(v, v), "shared_followers": G[u][v]["weight"]}
        for u, v in G.edges()
    ]
    edges_df = pd.DataFrame(edges_data) if edges_data else pd.DataFrame(
        columns=["source", "target", "shared_followers"]
    )

    nodes_data = [
        {
            "did": n,
            "handle": handles.get(n, n),
            "suspect_followers": target_weights.get(n, 0),
            "graph_degree": G.degree(n),
        }
        for n in G.nodes()
    ]
    nodes_df = pd.DataFrame(nodes_data).sort_values("suspect_followers", ascending=False)

    # Anchor classification
    if not nodes_df.empty:
        top_anchor_dids = nodes_df.head(classify_top)["did"].tolist()
        top10_set = set(nodes_df.head(10)["did"].tolist())
        suspect_did_set = set(suspect_dids)
        all_cluster = top10_set | suspect_did_set

        anchor_follows = asyncio.run(
            _fetch_follows_for_suspects(top_anchor_dids, config.api_concurrency, limit_per_account=500)
        )
        cluster_member: dict[str, int] = {}
        for did in top_anchor_dids:
            follows_set = set(anchor_follows.get(did, []))
            overlap = follows_set & all_cluster
            overlap.discard(did)
            cluster_member[did] = len(overlap)
        nodes_df["follows_cluster_members"] = nodes_df["did"].map(
            lambda d: cluster_member.get(d, -1)
        )
        nodes_df["is_cluster_member"] = nodes_df["follows_cluster_members"].apply(
            lambda x: x >= 5 if x >= 0 else True
        )

        # Demote periphery accounts that get blocked a lot — they're active
        if not analysis.acquired.blocks_received.empty:
            blocks = analysis.acquired.blocks_received.rename(columns={"subject": "did"})
            nodes_df = nodes_df.merge(blocks, on="did", how="left")
            nodes_df["block_count"] = nodes_df["block_count"].fillna(0).astype(int)
            demoted = (~nodes_df["is_cluster_member"]) & (nodes_df["block_count"] > 5)
            nodes_df.loc[demoted, "is_cluster_member"] = True
        else:
            nodes_df["block_count"] = 0

    figure = _render_figure(G, handles, analysis.acquired.target_did, config.anchor_handle)

    return ClusterResult(
        nodes_df=nodes_df,
        edges_df=edges_df,
        figure=figure,
        target_did=analysis.acquired.target_did,
        target_handle=config.anchor_handle,
    )
