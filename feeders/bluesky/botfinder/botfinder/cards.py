"""Social-media-style cards (1200x675) for inline notebook display.

Verbatim port of ``tmp/generate_cards.py`` — original German strings and
styling preserved. No PNG export, no kaleido. ``render_all_cards`` is the
orchestrator used by the pipeline / notebook.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if TYPE_CHECKING:  # pragma: no cover
    from .cluster import ClusterResult
    from .cross_follow import CrossFollowResult
    from .pipeline import AnalysisResult


CARD_W, CARD_H = 1200, 675
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1a1a1a"
ACCENT = "#cc0000"
ACCENT2 = "#cc5500"
ACCENT3 = "#996600"
MUTED = "#555555"
GRID_COLOR = "#e0e0e0"
FONT = "Roboto, sans-serif"
FONT_BOLD = "Roboto Black, Roboto, sans-serif"


def card_layout(fig: go.Figure, title: str = "", subtitle: str = "") -> go.Figure:
    """Apply consistent card styling with Roboto, clear headlines, no overlap."""
    existing = list(fig.layout.annotations) if fig.layout.annotations else []

    new_annotations = []
    if title:
        new_annotations.append(dict(
            text=f"<b>{title}</b>", xref="paper", yref="paper",
            x=0.5, y=1.14, showarrow=False, xanchor="center", yanchor="top",
            font=dict(size=30, color=TEXT_COLOR, family=FONT_BOLD),
        ))
    if subtitle:
        new_annotations.append(dict(
            text=subtitle, xref="paper", yref="paper",
            x=0.5, y=1.05, showarrow=False, xanchor="center", yanchor="top",
            font=dict(size=16, color=MUTED, family=FONT),
        ))
    new_annotations.append(dict(
        text="Bot-Netzwerk-Analyse \u2022 Bluesky Firehose + AT Protocol \u2022 Mai 2026",
        xref="paper", yref="paper", x=0.5, y=-0.14, showarrow=False,
        xanchor="center", yanchor="bottom",
        font=dict(size=10, color="#777777", family=FONT),
    ))

    fig.update_layout(
        width=CARD_W, height=CARD_H,
        paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR,
        margin=dict(l=60, r=60, t=80, b=60),
        annotations=existing + new_annotations,
        font=dict(color=TEXT_COLOR, family=FONT, size=14),
    )
    return fig


def card_1_overview(scores_df: pd.DataFrame, nodes_df: pd.DataFrame) -> go.Figure:
    """Card 1: Headline overview \u2014 key stats about the network."""
    total = len(scores_df)

    suspicious = len(scores_df[scores_df["score"] >= 0.5])
    normal = total - suspicious
    deleted = len(scores_df[scores_df["flags"].str.contains("DELETED", na=False)])
    anonymous = len(scores_df[scores_df["flags"].str.contains("ANONYMOUS_PROFILE", na=False)])
    instant = len(scores_df[scores_df["flags"].str.contains("INSTANT_FOLLOW", na=False)])

    now = datetime.now()
    date_str = now.strftime("%d. %B %Y, %H:%M Uhr")

    fig = make_subplots(
        rows=2, cols=4,
        row_heights=[0.55, 0.45],
        specs=[
            [{"colspan": 4, "type": "indicator"}, None, None, None],
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
        ],
        vertical_spacing=0.08,
    )

    fig.add_trace(go.Indicator(
        mode="number",
        value=total,
        number=dict(font=dict(size=1, color=BG_COLOR)),
    ), row=1, col=1)

    fig.add_annotation(
        text=f"<b>{total}</b> Follower",
        x=0.5, y=0.78, xref="paper", yref="paper",
        font=dict(size=62, color=TEXT_COLOR, family=FONT_BOLD),
        showarrow=False,
    )
    fig.add_annotation(
        text=f"davon <b>{suspicious}</b> Bots, <b>{normal}</b> unauff\u00e4llig",
        x=0.5, y=0.58, xref="paper", yref="paper",
        font=dict(size=34, color=ACCENT, family=FONT_BOLD),
        showarrow=False,
    )

    stats = [
        (deleted, "Gel\u00f6scht", ACCENT2),
        (instant, "Sofort-Follow", ACCENT2),
        (anonymous, "Anonym", ACCENT2),
        (normal, "Unauff\u00e4llig", MUTED),
    ]
    for i, (val, label, color) in enumerate(stats):
        fig.add_trace(go.Indicator(
            mode="number",
            value=val,
            title=dict(text=label, font=dict(size=14, color=MUTED, family=FONT)),
            number=dict(font=dict(size=42, color=color, family=FONT_BOLD)),
        ), row=2, col=i + 1)

    return card_layout(fig,
        title="Bot-Netzwerk um @niusde.bsky.social",
        subtitle=f"Analyse vom {date_str}"
    )


def card_2_anchors(nodes_df: pd.DataFrame) -> go.Figure:
    """Card 2: Anchor accounts \u2014 the hotspots being boosted."""
    df = nodes_df[nodes_df["handle"] != "bsky.app"].head(10).copy()
    df = df.sort_values("suspect_followers", ascending=True)

    colors = []
    for h in df["handle"]:
        if h == "niusde.bsky.social":
            colors.append(ACCENT)
        elif df[df["handle"] == h]["suspect_followers"].iloc[0] >= 50:
            colors.append(ACCENT2)
        else:
            colors.append(ACCENT3)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=["@" + h for h in df["handle"]],
        x=df["suspect_followers"],
        orientation="h",
        marker_color=colors,
        text=df["suspect_followers"],
        textposition="outside",
        textfont=dict(size=15, color=TEXT_COLOR, family=FONT),
    ))
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(tickfont=dict(size=14, color=TEXT_COLOR, family=FONT), domain=[0.0, 0.82])
    fig.update_layout(bargap=0.3, margin=dict(l=50, r=70, t=100, b=45))
    return card_layout(fig,
        title="Anker-Konten \u2014 Wen das Bot-Cluster pusht",
        subtitle="Konten, die von den meisten verd\u00e4chtigen Bot-Accounts gemeinsam gefolgt werden"
    )


def card_3_behavior(scores_df: pd.DataFrame) -> go.Figure:
    """Card 3: Bot behavior signals \u2014 what gives them away."""
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]],
                        column_widths=[0.4, 0.6], horizontal_spacing=0.08)

    bins = [
        ("Hohes Risiko (\u22650,6)", len(scores_df[scores_df["score"] >= 0.6]), ACCENT),
        ("Mittel (0,5\u20130,6)", len(scores_df[(scores_df["score"] >= 0.5) & (scores_df["score"] < 0.6)]), ACCENT2),
        ("Niedrig (<0,5)", len(scores_df[scores_df["score"] < 0.5]), "#999999"),
    ]
    fig.add_trace(go.Pie(
        labels=[b[0] for b in bins],
        values=[b[1] for b in bins],
        marker=dict(colors=[b[2] for b in bins]),
        textinfo="percent+value",
        textfont=dict(size=14, family=FONT),
        hole=0.4,
    ), row=1, col=1)

    high_risk = scores_df[scores_df["score"] >= 0.5]
    signals = ["temporal_proximity", "anonymity", "activity_pattern", "follow_overlap", "account_age"]
    signal_labels = ["Timing", "Anonymit\u00e4t", "Aktivit\u00e4t", "\u00dcberlapp.", "Alter"]
    means = [high_risk[s].mean() for s in signals]

    fig.add_trace(go.Bar(
        x=signal_labels,
        y=means,
        marker_color=[ACCENT, ACCENT2, ACCENT3, "#1565c0", "#6a1b9a"],
        text=[f"{m:.2f}" for m in means],
        textposition="outside",
        textfont=dict(size=14, color=TEXT_COLOR, family=FONT),
        showlegend=False,
    ), row=1, col=2)

    fig.update_yaxes(range=[0, 1.08], showgrid=True, gridcolor=GRID_COLOR, row=1, col=2)
    fig.update_xaxes(tickfont=dict(size=13, color=TEXT_COLOR, family=FONT), row=1, col=2)

    return card_layout(fig,
        title="Bot-Verhaltenssignale \u2014 Erkennungsmethode",
        subtitle="5-Signal-Scoring: Timing, Profil, Aktivit\u00e4t, \u00dcberlappung, Kontoalter"
    )


def card_4_timeline(detail_df: pd.DataFrame) -> go.Figure:
    """Card 4: Temporal pattern \u2014 follow bursts."""
    df = detail_df.copy()
    df["follow_created_at"] = pd.to_datetime(df["follow_created_at"], errors="coerce")
    df = df.dropna(subset=["follow_created_at"])

    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Keine Zeitdaten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return card_layout(fig, title="Follow-Burst-Zeitverlauf")

    hourly = df.set_index("follow_created_at").resample("1h").size().reset_index(name="count")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=hourly["follow_created_at"], y=hourly["count"],
        marker_color=ACCENT, opacity=0.85,
    ))
    fig.update_xaxes(title_text="Datum / Zeit (UTC)", tickfont=dict(size=11, family=FONT),
                     showgrid=False, tickangle=-45, tickformat="%d.%m. %H:%M")
    fig.update_yaxes(title_text="Follows pro Stunde", tickfont=dict(size=13, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR)
    return card_layout(fig,
        title="Follow-Burst-Zeitverlauf",
        subtitle="St\u00fcndliche Follow-Ereignisse \u2014 Spitzen deuten auf koordinierte Bot-Aktivit\u00e4t hin"
    )


def card_5_cluster(nodes_df: pd.DataFrame, edges_df: pd.DataFrame) -> go.Figure:
    """Card 5: Square cluster graph \u2014 core/periphery with legend and method footer."""
    CARD5_SIZE = 1200

    G = nx.Graph()
    min_suspect = 10
    filtered_nodes = nodes_df[
        (nodes_df["handle"] != "bsky.app") & (nodes_df["suspect_followers"] >= min_suspect)
    ]
    for _, row in filtered_nodes.iterrows():
        G.add_node(row["handle"], weight=row["suspect_followers"])

    handles_set = set(filtered_nodes["handle"])
    for _, row in edges_df.iterrows():
        if row["source"] in handles_set and row["target"] in handles_set:
            G.add_edge(row["source"], row["target"], weight=row["shared_followers"])

    if len(G.nodes()) == 0:
        fig = go.Figure()
        fig.add_annotation(text="Unzureichende Cluster-Daten", xref="paper", yref="paper",
                           x=0.5, y=0.5, showarrow=False, font=dict(size=16, family=FONT))
        fig.update_layout(width=CARD5_SIZE, height=CARD5_SIZE)
        return card_layout(fig, title="Follow-Cluster")

    weights = nx.get_node_attributes(G, "weight")
    max_w = max(weights.values()) if weights else 1

    target_handle = "niusde.bsky.social"
    cluster_members = set(
        nodes_df[nodes_df["is_cluster_member"] == True]["handle"]
    ) if "is_cluster_member" in nodes_df.columns else set(G.nodes())

    core_nodes = [n for n in G.nodes() if n in cluster_members or n == target_handle]
    periphery_nodes = [n for n in G.nodes() if n not in cluster_members and n != target_handle]
    periphery_set = set(periphery_nodes)

    core_sorted = sorted(core_nodes, key=lambda n: weights.get(n, 0), reverse=True)
    pos = {}
    rings = [1, 5, 15, 40, 80, 200]
    ring_radii = [0.0, 0.18, 0.35, 0.52, 0.68, 0.80]
    placed = 0
    for ring_idx in range(len(rings)):
        ring_count = rings[ring_idx] - (rings[ring_idx - 1] if ring_idx > 0 else 0)
        radius = ring_radii[ring_idx]
        nodes_in_ring = core_sorted[placed:placed + ring_count]
        if not nodes_in_ring:
            break
        for i, n in enumerate(nodes_in_ring):
            if radius == 0:
                pos[n] = np.array([0.0, 0.0])
            else:
                angle = 2 * np.pi * i / len(nodes_in_ring) + ring_idx * 0.3
                pos[n] = np.array([radius * np.cos(angle), radius * np.sin(angle)])
        placed += len(nodes_in_ring)
    remaining = core_sorted[placed:]
    if remaining:
        for i, n in enumerate(remaining):
            angle = 2 * np.pi * i / len(remaining) + 0.1
            pos[n] = np.array([0.85 * np.cos(angle), 0.85 * np.sin(angle)])

    if periphery_nodes:
        margin = 1.05
        n_peri = len(periphery_nodes)
        perimeter = 8 * margin
        for i, n in enumerate(periphery_nodes):
            t = (i / n_peri) * perimeter
            if t < 2 * margin:
                pos[n] = np.array([-margin + t, margin])
            elif t < 4 * margin:
                pos[n] = np.array([margin, margin - (t - 2 * margin)])
            elif t < 6 * margin:
                pos[n] = np.array([margin - (t - 4 * margin), -margin])
            else:
                pos[n] = np.array([-margin, -margin + (t - 6 * margin)])
    else:
        margin = 1.05

    edge_core_x, edge_core_y = [], []
    edge_peri_x, edge_peri_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        if u in periphery_set or v in periphery_set:
            edge_peri_x.extend([x0, x1, None])
            edge_peri_y.extend([y0, y1, None])
        else:
            edge_core_x.extend([x0, x1, None])
            edge_core_y.extend([y0, y1, None])

    edge_core_trace = go.Scatter(
        x=edge_core_x, y=edge_core_y, mode="lines",
        line=dict(width=0.4, color="rgba(200,0,0,0.15)"),
        hoverinfo="none", showlegend=False,
    )
    edge_peri_trace = go.Scatter(
        x=edge_peri_x, y=edge_peri_y, mode="lines",
        line=dict(width=0.4, color="rgba(0,160,0,0.18)"),
        hoverinfo="none", showlegend=False,
    )

    sorted_nodes = sorted(G.nodes(), key=lambda n: weights.get(n, 0), reverse=True)
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    node_sizes = [max(7, 45 * (weights.get(n, 0) / max_w)) for n in G.nodes()]
    node_colors = []
    for n in G.nodes():
        if n == target_handle:
            node_colors.append(ACCENT)
        elif n in periphery_set:
            node_colors.append("#aaaaaa")
        elif weights.get(n, 0) >= max_w * 0.3:
            node_colors.append(ACCENT2)
        else:
            node_colors.append(ACCENT3)

    node_degrees = [G.degree(n) for n in G.nodes()]
    node_texts = [str(d) if sz >= 14 else "" for d, sz in zip(node_degrees, node_sizes)]

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_texts, textposition="middle center",
        textfont=dict(size=9, color="white", family=FONT_BOLD),
        marker=dict(size=node_sizes, color=node_colors, line=dict(width=0.6, color="#333333")),
        hovertext=[f"@{n}: {weights.get(n,0)} suspects, {G.degree(n)} edges" for n in G.nodes()],
        hoverinfo="text", showlegend=False,
    )

    top_core = [n for n in sorted_nodes if n in core_nodes][:15]

    core_label_x = [pos[n][0] for n in top_core]
    core_label_y = [pos[n][1] for n in top_core]
    core_label_text = ["@" + n.split(".")[0] for n in top_core]
    core_label_trace = go.Scatter(
        x=core_label_x, y=core_label_y, mode="text",
        text=core_label_text, textposition="top center",
        textfont=dict(size=9, color=TEXT_COLOR, family=FONT),
        hoverinfo="none", showlegend=False,
    )

    peri_with_weight = [(n, weights.get(n, 0)) for n in periphery_nodes]
    peri_with_weight.sort(key=lambda x: x[1], reverse=True)
    labeled_peri = [n for n, _ in peri_with_weight]

    left_peri, right_peri, top_peri, bottom_peri = [], [], [], []
    for n in labeled_peri:
        nx_pos, ny_pos = pos[n]
        dist_left = abs(nx_pos - (-margin))
        dist_right = abs(nx_pos - margin)
        dist_top = abs(ny_pos - margin)
        dist_bottom = abs(ny_pos - (-margin))
        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)
        if min_dist == dist_top:
            top_peri.append(n)
        elif min_dist == dist_bottom:
            bottom_peri.append(n)
        elif min_dist == dist_left:
            left_peri.append(n)
        else:
            right_peri.append(n)

    left_peri.sort(key=lambda n: -pos[n][1])
    right_peri.sort(key=lambda n: -pos[n][1])
    top_peri.sort(key=lambda n: pos[n][0])
    bottom_peri.sort(key=lambda n: pos[n][0])

    label_offset = 0.08
    left_label_x = -(margin + label_offset)
    right_label_x = margin + label_offset

    peri_lx, peri_ly, peri_labels, peri_positions = [], [], [], []

    for n in left_peri:
        _, ny = pos[n]
        peri_lx.append(left_label_x)
        peri_ly.append(ny)
        peri_labels.append("@" + n.split(".")[0])
        peri_positions.append("middle left")

    for n in right_peri:
        _, ny = pos[n]
        peri_lx.append(right_label_x)
        peri_ly.append(ny)
        peri_labels.append("@" + n.split(".")[0])
        peri_positions.append("middle right")

    peri_label_trace = go.Scatter(
        x=peri_lx, y=peri_ly, mode="text",
        text=peri_labels, textposition=peri_positions,
        textfont=dict(size=16, color="#222222", family=FONT_BOLD),
        hoverinfo="none", showlegend=False,
    )

    leader_trace = go.Scatter(
        x=[None], y=[None], mode="lines",
        line=dict(width=0.5, color="rgba(100,100,100,0.35)"),
        hoverinfo="none", showlegend=False,
    )

    top_label_y = margin + label_offset
    bottom_label_y = -(margin + label_offset)
    top_positions = [(pos[n][0], top_label_y) for n in top_peri]
    bottom_positions = [(pos[n][0], bottom_label_y) for n in bottom_peri]

    fig = go.Figure(data=[
        edge_peri_trace, leader_trace, edge_core_trace,
        node_trace, core_label_trace, peri_label_trace
    ])

    x_range = margin + label_offset + 0.55
    y_range = margin + label_offset + 0.35
    fig.update_xaxes(visible=False, range=[-x_range, x_range])
    fig.update_yaxes(visible=False, range=[-y_range, y_range], scaleanchor="x", scaleratio=1)

    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color=ACCENT), name="Zielkonto (@niusde)",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color=ACCENT2), name="Top-Verst\u00e4rker (Kern)",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color=ACCENT3), name="Cluster-Mitglieder (Kern)",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color="#aaaaaa"), name="Troll-Ziele (Ring)",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="lines",
        line=dict(width=2, color="rgba(200,0,0,0.5)"), name="Kante: folgt sich gegenseitig",
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="lines",
        line=dict(width=2, color="rgba(0,160,0,0.6)"), name="Kante: nur gefolgt (Ziel)",
        showlegend=True,
    ))

    n_suspects = len(nodes_df[nodes_df["suspect_followers"] >= min_suspect])
    method_text = (
        f"Methode: Follow-Listen aller {n_suspects} Bot-Verd\u00e4chtigen (Score \u2265 0.45) abgerufen \u2192 "
        f"gemeinsame Zielkonten (\u2265 {min_suspect} Verd\u00e4chtige) als Knoten \u2192 "
        "Co-Follow-Anzahl als Kantengewicht.<br>"
        "Kern = folgt > 5 Cluster-Mitglieder zur\u00fcck. "
        "Peripherie (Troll-Ziel) = folgt \u2264 5 Mitglieder zur\u00fcck."
    )

    fig.update_layout(
        width=CARD5_SIZE, height=CARD5_SIZE,
        paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR,
        margin=dict(l=10, r=10, t=70, b=70),
        font=dict(color=TEXT_COLOR, family=FONT, size=14),
        legend=dict(
            x=0.0, y=0.0, xanchor="left", yanchor="bottom",
            bgcolor="rgba(255,255,255,0.85)", bordercolor="#cccccc", borderwidth=1,
            font=dict(size=10, family=FONT), orientation="v",
        ),
        annotations=[
            dict(
                text="<b>Bot-Cluster-Netzwerk</b>", xref="paper", yref="paper",
                x=0.5, y=1.06, showarrow=False, xanchor="center", yanchor="top",
                font=dict(size=28, color=TEXT_COLOR, family=FONT_BOLD),
            ),
            dict(
                text=(f"Kern: {len(core_nodes)} vernetzte Konten \u2022 "
                      f"Ring: {len(periphery_nodes)} Einzelziele \u2022 "
                      f"Zahl in Knoten = Verbindungsgrad"),
                xref="paper", yref="paper",
                x=0.5, y=1.015, showarrow=False, xanchor="center", yanchor="top",
                font=dict(size=13, color=MUTED, family=FONT),
            ),
            dict(
                text=method_text,
                xref="paper", yref="paper",
                x=0.5, y=-0.02, showarrow=False, xanchor="center", yanchor="top",
                font=dict(size=9, color="#777777", family=FONT),
            ),
            dict(
                text="Bot-Netzwerk-Analyse \u2022 Bluesky Firehose + AT Protocol \u2022 Mai 2026",
                xref="paper", yref="paper",
                x=0.5, y=-0.07, showarrow=False, xanchor="center", yanchor="top",
                font=dict(size=9, color="#999999", family=FONT),
            ),
        ],
    )

    for i, n in enumerate(top_peri):
        x, y = top_positions[i]
        fig.add_annotation(
            x=x, y=y, text="@" + n.split(".")[0],
            showarrow=False, textangle=-90,
            font=dict(size=16, color="#222222", family=FONT_BOLD),
            xanchor="center", yanchor="bottom",
        )
    for i, n in enumerate(bottom_peri):
        x, y = bottom_positions[i]
        fig.add_annotation(
            x=x, y=y, text="@" + n.split(".")[0],
            showarrow=False, textangle=-90,
            font=dict(size=16, color="#222222", family=FONT_BOLD),
            xanchor="center", yanchor="top",
        )

    return fig


def card_6_deleted(scores_df: pd.DataFrame) -> go.Figure:
    """Card 6: Deleted/suspended accounts \u2014 evidence of cleanup."""
    deleted = scores_df[scores_df["flags"].str.contains("DELETED", na=False)]
    active = scores_df[~scores_df["flags"].str.contains("DELETED", na=False)]

    total_deleted = len(deleted)
    total_active = len(active)
    pct_deleted = 100 * total_deleted / len(scores_df) if len(scores_df) > 0 else 0

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.35, 0.65],
        specs=[[{"type": "indicator"}], [{"type": "xy"}]],
        vertical_spacing=0.12,
    )

    fig.add_trace(go.Indicator(
        mode="number",
        value=total_deleted,
        number=dict(font=dict(size=64, color=ACCENT, family=FONT_BOLD),
                    suffix=f"  ({pct_deleted:.0f}%)"),
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=[total_active, total_deleted],
        y=["Noch aktiv", "Gel\u00f6scht/Gesperrt"],
        orientation="h",
        marker_color=["#cccccc", ACCENT],
        text=[total_active, total_deleted],
        textposition="inside",
        textfont=dict(size=18, color="white", family=FONT),
        showlegend=False,
    ), row=2, col=1)

    fig.update_xaxes(visible=False, row=2, col=1)
    fig.update_yaxes(tickfont=dict(size=16, color=TEXT_COLOR, family=FONT), row=2, col=1)
    fig.update_layout(margin=dict(l=50, r=50, t=120, b=45))

    return card_layout(fig,
        title="Kontol\u00f6schungen \u2014 Hinweis auf Bot-Bereinigung",
        subtitle="Konten, die @niusde folgten und inzwischen gel\u00f6scht oder gesperrt wurden"
    )


def card_7_lifecycle_waves(detail_df: pd.DataFrame, scores_df: pd.DataFrame) -> go.Figure:
    """Card 7: Bot lifecycle waves \u2014 creation vs follow activity over time."""
    merged = detail_df.merge(
        scores_df[["did", "flags"]], left_on="follower_did", right_on="did", how="left"
    )
    df = merged.copy()
    df["is_deleted"] = df["flags"].str.contains("DELETED", na=False)

    bin_freq = "1h"
    df["created_bin"] = df["follower_created_at"].dt.floor(bin_freq)
    df["follow_bin"] = df["follow_created_at"].dt.floor(bin_freq)

    t_min = df["follower_created_at"].min().floor("h")
    t_max = df["follow_created_at"].max().ceil("h")
    all_bins = pd.date_range(t_min, t_max, freq=bin_freq)

    created_counts = df.groupby("created_bin").size().reindex(all_bins, fill_value=0)
    follow_counts = df.groupby("follow_bin").size().reindex(all_bins, fill_value=0)

    x_labels = [t.strftime("%H:%M") for t in all_bins]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_labels, y=created_counts.values,
        name="Konten erstellt",
        marker_color="rgba(30,136,229,0.6)",
    ))
    fig.add_trace(go.Bar(
        x=x_labels, y=follow_counts.values,
        name="Follow-Ereignisse",
        marker_color="rgba(204,0,0,0.5)",
    ))

    y_max = max(created_counts.max(), follow_counts.max())
    fig.update_xaxes(title_text="Zeit (UTC)", tickfont=dict(size=11, family=FONT),
                     showgrid=False, tickangle=-45, dtick=2)
    fig.update_yaxes(title_text="Ereignisse pro Stunde", tickfont=dict(size=13, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR, range=[0, y_max * 1.15])
    fig.update_layout(
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0,
                    font=dict(size=13, family=FONT)),
    )
    return card_layout(fig,
        title="Lebenszyklus-Wellen \u2014 Erstellung & Follow-Aktivit\u00e4t",
        subtitle="Kontoerstellungs-Bursts eng gekoppelt mit Follow-Ereignissen"
    )


def card_8_cumulative(detail_df: pd.DataFrame, scores_df: pd.DataFrame) -> go.Figure:
    """Card 8: Cumulative growth curve."""
    merged = detail_df.merge(
        scores_df[["did", "flags"]], left_on="follower_did", right_on="did", how="left"
    )
    df = merged.copy()
    df["is_deleted"] = df["flags"].str.contains("DELETED", na=False)
    df["follow_created_at"] = pd.to_datetime(df["follow_created_at"], errors="coerce")
    df = df.dropna(subset=["follow_created_at"])

    if df.empty:
        return card_layout(go.Figure(), title="Kumulatives Netzwerk-Wachstum")

    bin_freq = "1h"
    df["follow_bin"] = df["follow_created_at"].dt.floor(bin_freq)
    t_min = df["follow_created_at"].min().floor("h")
    t_max = df["follow_created_at"].max().ceil("h")
    all_bins = pd.date_range(t_min, t_max, freq=bin_freq)

    follow_counts = df.groupby("follow_bin").size().reindex(all_bins, fill_value=0)
    deleted_counts = df[df["is_deleted"]].groupby("follow_bin").size().reindex(all_bins, fill_value=0)

    cum_total = follow_counts.cumsum()
    cum_deleted = deleted_counts.cumsum()
    cum_surviving = cum_total - cum_deleted

    x_vals = all_bins.to_pydatetime().tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=cum_total.values,
        name="Gesamt gefolgt", mode="lines",
        line=dict(width=2.5, color="#555555", dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=x_vals, y=cum_surviving.values,
        name="\u00dcberlebend", mode="lines",
        line=dict(width=3, color="#2e7d32"),
    ))
    fig.add_trace(go.Scatter(
        x=x_vals, y=cum_deleted.values,
        name="Gel\u00f6scht", mode="lines",
        line=dict(width=3, color=ACCENT),
        fill="tozeroy", fillcolor="rgba(204,0,0,0.1)",
    ))

    fig.update_xaxes(title_text="Zeit (UTC)", tickfont=dict(size=11, family=FONT),
                     showgrid=False, tickangle=-45, tickformat="%d.%m. %H:%M")
    fig.update_yaxes(title_text="Kumulierte Konten", tickfont=dict(size=13, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5,
                    font=dict(size=12, family=FONT)),
    )
    return card_layout(fig,
        title="Kumulatives Netzwerk-Wachstum & Schwund",
        subtitle="Laufende Summe: Wie schnell das Bot-Netzwerk wuchs und wie viele entfernt wurden"
    )


def card_9_age_at_follow(detail_df: pd.DataFrame) -> go.Figure:
    """Card 9: Age at follow \u2014 how fast bots acted after creation."""
    ages = detail_df["age_at_follow_minutes"].dropna()

    age_bins = [0, 1, 2, 5, 10, 30, 60, 120, 360, 1440]
    age_labels = ["<1m", "1\u20132m", "2\u20135m", "5\u201310m", "10\u201330m", "30\u201360m", "1\u20132h", "2\u20136h", "6\u201324h"]
    bucketed = pd.cut(ages, bins=age_bins, labels=age_labels, right=False)
    counts = bucketed.value_counts().reindex(age_labels, fill_value=0)

    colors = [ACCENT if i < 3 else ACCENT2 if i < 5 else ACCENT3 for i in range(len(age_labels))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=age_labels, y=counts.values,
        marker_color=colors,
        text=counts.values,
        textposition="outside",
        textfont=dict(size=14, family=FONT),
    ))
    fig.update_xaxes(title_text="Zeit von Kontoerstellung bis Follow",
                     tickfont=dict(size=14, family=FONT))
    fig.update_yaxes(title_text="Anzahl Konten",
                     tickfont=dict(size=13, family=FONT), showgrid=True, gridcolor=GRID_COLOR)

    under_5 = int(counts.iloc[:3].sum())
    total = int(counts.sum())
    return card_layout(fig,
        title="Dauer von Erstellung bis Follow",
        subtitle=f"{under_5} von {total} neuen Konten ({100*under_5/total:.0f}%) folgten innerhalb von 5 Min. nach Erstellung"
    )


def card_10_score_distribution(scores_df: pd.DataFrame) -> go.Figure:
    """Card 10: Bot score distribution histogram."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=scores_df["score"],
        nbinsx=25,
        marker_color=ACCENT,
        opacity=0.85,
    ))
    fig.add_vline(x=0.7, line_dash="dash", line_color="#cc0000",
                  annotation_text="Hohe Konfidenz", annotation_position="bottom right",
                  annotation_font=dict(size=13, family=FONT, color=ACCENT))
    fig.add_vline(x=0.4, line_dash="dash", line_color=ACCENT2,
                  annotation_text="Mittel", annotation_position="bottom left",
                  annotation_font=dict(size=13, family=FONT, color=ACCENT2))
    fig.update_xaxes(title_text="Bot-Score (0 = Mensch, 1 = Bot)",
                     tickfont=dict(size=13, family=FONT))
    fig.update_yaxes(title_text="Anzahl Konten",
                     tickfont=dict(size=13, family=FONT), showgrid=True, gridcolor=GRID_COLOR)

    mean_score = scores_df["score"].mean()
    return card_layout(fig,
        title="Bot-Score-Verteilung",
        subtitle=f"Mittelwert: {mean_score:.2f} \u2014 h\u00f6her = bot-\u00e4hnlicheres Verhalten"
    )


def card_11_creation_vs_follow(detail_df: pd.DataFrame) -> go.Figure:
    """Card 11: Scatter of creation time vs time-to-follow."""
    df = detail_df.dropna(subset=["age_at_follow_minutes"]).copy()
    df["age_capped"] = df["age_at_follow_minutes"].clip(upper=120)
    df["created_str"] = df["follower_created_at"].dt.strftime("%d.%m. %H:%M")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["created_str"],
        y=df["age_capped"],
        mode="markers",
        marker=dict(
            size=5, opacity=0.7,
            color=df["age_capped"].values,
            colorscale="RdYlGn",
            cmin=0, cmax=60,
            showscale=True,
            colorbar=dict(title=dict(text="Min", font=dict(size=12, family=FONT)),
                          tickfont=dict(size=11, family=FONT)),
        ),
    ))
    fig.add_hline(y=5, line_dash="dash", line_color=ACCENT, line_width=1.5,
                  annotation_text="5-Min-Schwelle", annotation_position="top right",
                  annotation_font=dict(size=12, family=FONT, color=ACCENT))
    fig.update_xaxes(title_text="Konto erstellt am (UTC)", tickfont=dict(size=12, family=FONT),
                     type="category")
    fig.update_yaxes(title_text="Minuten bis Follow", tickfont=dict(size=12, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR)
    return card_layout(fig,
        title="Kontoerstellung vs. Zeit bis Follow",
        subtitle="Rote Punkte = Follow fast sofort nach Kontoerstellung"
    )


def card_12_amplifiers(scores_df: pd.DataFrame, cross_df: pd.DataFrame) -> go.Figure:
    """Card 12: Amplification accounts deep-dive \u2014 coordinated trolls."""
    amplifiers = scores_df[
        (scores_df["score"] < 0.5) &
        (scores_df["flags"].str.contains("AMPLIFICATION", na=False))
    ]
    non_amp = scores_df[
        (scores_df["score"] < 0.5) &
        (~scores_df["flags"].str.contains("AMPLIFICATION", na=False))
    ]
    bots = scores_df[scores_df["score"] >= 0.5]
    n_amp = len(amplifiers)
    n_amp_anon = len(amplifiers[amplifiers["flags"].str.contains("ANONYMOUS", na=False)])

    valid_cross = cross_df[cross_df["total_follows_fetched"] > 0]
    bot_cross = valid_cross[valid_cross["is_bot"]]
    non_bot_cross = valid_cross[~valid_cross["is_bot"]]
    bot_mean_pct = bot_cross["cohort_pct"].mean() if len(bot_cross) > 0 else 0
    non_bot_mean_pct = non_bot_cross["cohort_pct"].mean() if len(non_bot_cross) > 0 else 0
    bot_mean_n = bot_cross["cohort_follows"].mean() if len(bot_cross) > 0 else 0
    non_bot_mean_n = non_bot_cross["cohort_follows"].mean() if len(non_bot_cross) > 0 else 0

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.45, 0.55],
        horizontal_spacing=0.12,
        specs=[[{"type": "pie"}, {"type": "bar"}]],
    )

    labels = [f"Bots ({len(bots)})", f"Verst\u00e4rker ({n_amp})", f"Unauff\u00e4llig ({len(non_amp)})"]
    values = [len(bots), n_amp, len(non_amp)]
    colors = [ACCENT, ACCENT3, "#bbbbbb"]
    fig.add_trace(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors),
        textinfo="percent+label",
        textfont=dict(size=12, family=FONT),
        hole=0.35,
        showlegend=False,
    ), row=1, col=1)

    categories = ["Bots", "Verst\u00e4rker/\nNon-Bots"]
    cross_vals = [bot_mean_pct, non_bot_mean_pct]
    bar_colors = [ACCENT, ACCENT3]
    fig.add_trace(go.Bar(
        x=categories, y=cross_vals,
        marker_color=bar_colors,
        text=[f"{v:.0f}%" for v in cross_vals],
        textposition="outside",
        textfont=dict(size=16, family=FONT_BOLD, color=TEXT_COLOR),
        showlegend=False,
        width=0.5,
    ), row=1, col=2)

    fig.update_yaxes(
        title_text="\u00d8 Quervernetzung (%)",
        tickfont=dict(size=12, family=FONT),
        showgrid=True, gridcolor=GRID_COLOR,
        range=[0, max(cross_vals) * 1.3 if max(cross_vals) > 0 else 1],
        row=1, col=2,
    )
    fig.update_xaxes(tickfont=dict(size=13, family=FONT), row=1, col=2)

    return card_layout(fig,
        title="Verst\u00e4rker-Konten \u2014 Koordinierte Quervernetzung",
        subtitle=f"{n_amp} Amplifier-Konten \u2022 \u00d8 {non_bot_mean_n:.0f} gegenseitige Follows \u2022 {n_amp_anon} anonym"
    )


def card_13_cross_speed(per_account_df: pd.DataFrame) -> go.Figure:
    """Card 13: Cross-follow speed \u2014 how fast do new accounts find the network."""
    df = per_account_df.copy()
    df["first_cross_min"] = df["first_cross"] * 1440
    df["first_cross_capped"] = df["first_cross_min"].clip(upper=120)

    cat_order = ["Bot", "Verst\u00e4rker", "Unauff\u00e4llig"]
    cat_colors = {"Bot": ACCENT, "Verst\u00e4rker": ACCENT3, "Unauff\u00e4llig": MUTED}

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.55, 0.45],
        horizontal_spacing=0.12,
        subplot_titles=["Minuten bis erste Quervernetzung", "Anteil < 60 Min"],
    )

    for cat in cat_order:
        subset = df[df["category"] == cat]
        fig.add_trace(go.Box(
            y=subset["first_cross_capped"],
            name=cat,
            marker_color=cat_colors[cat],
            boxmean=True,
            showlegend=False,
            width=0.5,
        ), row=1, col=1)

    pcts = []
    labels = []
    colors = []
    for cat in cat_order:
        subset = df[df["category"] == cat]
        if len(subset) > 0:
            pct = 100 * (subset["first_cross_min"] < 60).sum() / len(subset)
        else:
            pct = 0
        pcts.append(pct)
        labels.append(cat)
        colors.append(cat_colors[cat])

    fig.add_trace(go.Bar(
        x=labels, y=pcts,
        marker_color=colors,
        text=[f"{v:.0f}%" for v in pcts],
        textposition="outside",
        textfont=dict(size=16, family=FONT_BOLD, color=TEXT_COLOR),
        showlegend=False,
        width=0.5,
    ), row=1, col=2)

    fig.update_yaxes(title_text="Minuten", showgrid=True, gridcolor=GRID_COLOR,
                     tickfont=dict(size=11, family=FONT), range=[0, 125], row=1, col=1)
    fig.update_yaxes(title_text="%", range=[0, 115], showgrid=True, gridcolor=GRID_COLOR,
                     tickfont=dict(size=11, family=FONT), row=1, col=2)
    fig.update_xaxes(tickfont=dict(size=12, family=FONT))

    bot_subset = df[df["category"] == "Bot"]
    bot_median_min = bot_subset["first_cross_min"].median() if len(bot_subset) > 0 else 0
    bot_pct_60 = 100 * (bot_subset["first_cross_min"] < 60).sum() / len(bot_subset) if len(bot_subset) > 0 else 0
    fig = card_layout(fig,
        title="Quervernetzungs-Geschwindigkeit",
        subtitle=f"Bot-Median: {bot_median_min:.0f} Min \u2022 {bot_pct_60:.0f}% der Bots vernetzen sich in < 1 Stunde"
    )
    for ann in fig.layout.annotations:
        if ann.text in ["Minuten bis erste Quervernetzung", "Anteil < 60 Min"]:
            ann.font = dict(size=13, family=FONT_BOLD, color=TEXT_COLOR)
            ann.y = 0.95
            ann.yanchor = "bottom"
    fig.update_layout(margin=dict(t=140, b=65))
    return fig


def card_14_blocks_likes(scores_df: pd.DataFrame, blocks_df: pd.DataFrame, likes_df: pd.DataFrame) -> go.Figure:
    """Card 14: Block intensity and like patterns across categories."""
    merged = scores_df.merge(blocks_df, on="did", how="left")
    merged["block_count"] = merged["block_count"].fillna(0).astype(int)

    merged = merged.merge(likes_df, on="did", how="left")
    merged["like_count"] = merged["like_count"].fillna(0).astype(int)

    is_bot = merged["score"] >= 0.5
    is_amp = (merged["score"] < 0.5) & (merged["flags"].str.contains("AMPLIFICATION", na=False))
    is_normal = (merged["score"] < 0.5) & (~merged["flags"].str.contains("AMPLIFICATION", na=False))

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.5, 0.5],
        horizontal_spacing=0.12,
        subplot_titles=["\u00d8 Blocks erhalten", "\u00d8 Likes abgegeben"],
    )

    categories = ["Bots", "Verst\u00e4rker", "Unauff\u00e4llig"]
    block_means = [
        merged[is_bot]["block_count"].mean(),
        merged[is_amp]["block_count"].mean(),
        merged[is_normal]["block_count"].mean(),
    ]
    bar_colors = [ACCENT, ACCENT3, MUTED]
    fig.add_trace(go.Bar(
        x=categories, y=block_means,
        marker_color=bar_colors,
        text=[f"{v:.0f}" for v in block_means],
        textposition="outside",
        textfont=dict(size=14, family=FONT_BOLD, color=TEXT_COLOR),
        showlegend=False,
        width=0.5,
    ), row=1, col=1)

    like_means = [
        merged[is_bot]["like_count"].mean(),
        merged[is_amp]["like_count"].mean(),
        merged[is_normal]["like_count"].mean(),
    ]
    zero_pcts = [
        100 * (merged[is_bot]["like_count"] == 0).sum() / max(is_bot.sum(), 1),
        100 * (merged[is_amp]["like_count"] == 0).sum() / max(is_amp.sum(), 1),
        100 * (merged[is_normal]["like_count"] == 0).sum() / max(is_normal.sum(), 1),
    ]
    fig.add_trace(go.Bar(
        x=categories, y=like_means,
        marker_color=bar_colors,
        text=[f"{v:.0f}" for v in like_means],
        textposition="outside",
        textfont=dict(size=14, family=FONT_BOLD, color=TEXT_COLOR),
        showlegend=False,
        width=0.5,
    ), row=1, col=2)

    max_likes = max(like_means) if max(like_means) > 0 else 1
    for i, (cat, pct) in enumerate(zip(categories, zero_pcts)):
        fig.add_annotation(
            x=cat, y=-max_likes * 0.12,
            text=f"{pct:.0f}% ohne Likes",
            font=dict(size=11, color=MUTED, family=FONT),
            showarrow=False,
            xref="x2", yref="y2",
        )

    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=11, family=FONT))
    fig.update_xaxes(tickfont=dict(size=12, family=FONT))
    max_blocks = max(block_means) if max(block_means) > 0 else 1
    fig.update_yaxes(range=[0, max_blocks * 1.25], row=1, col=1)
    fig.update_yaxes(range=[-max_likes * 0.2, max_likes * 1.35], row=1, col=2)

    for ann in fig.layout.annotations:
        if ann.text in ["\u00d8 Blocks erhalten", "\u00d8 Likes abgegeben"]:
            ann.font = dict(size=15, family=FONT_BOLD, color=TEXT_COLOR)

    amp_block_median = int(merged[is_amp]["block_count"].median()) if is_amp.sum() > 0 else 0
    return card_layout(fig,
        title="Blockiert & Liken \u2014 Alle Kategorien betroffen",
        subtitle=f"100% aller Konten auf Blocklisten \u2022 Verst\u00e4rker-Median: {amp_block_median} Blocks"
    )


def card_15_block_hitlist(scores_df: pd.DataFrame, blocks_df: pd.DataFrame, nodes_df: pd.DataFrame) -> go.Figure:
    """Card 15: Top blocked accounts from the cluster \u2014 block hitlist."""
    merged = scores_df[["did", "score", "flags"]].merge(blocks_df, on="did", how="left")
    merged["block_count"] = merged["block_count"].fillna(0).astype(int)
    merged = merged.merge(
        nodes_df[["did", "handle"]].drop_duplicates(), on="did", how="left"
    )

    merged["category"] = "Unauff\u00e4llig"
    merged.loc[merged["score"] >= 0.5, "category"] = "Bot"
    merged.loc[
        (merged["score"] < 0.5) &
        (merged["flags"].str.contains("AMPLIFICATION", na=False)),
        "category"
    ] = "Verst\u00e4rker"

    top = merged.nlargest(15, "block_count").copy()
    top["label"] = top["handle"].apply(
        lambda h: f"@{h.replace('.bsky.social', '')}" if pd.notna(h) else "(anonym)"
    )
    top = top.sort_values("block_count", ascending=True)

    cat_colors = {"Bot": ACCENT, "Verst\u00e4rker": ACCENT3, "Unauff\u00e4llig": MUTED}
    colors = [cat_colors[c] for c in top["category"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top["label"],
        x=top["block_count"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:,}".replace(",", ".") for v in top["block_count"]],
        textposition="outside",
        textfont=dict(size=13, family=FONT_BOLD, color=TEXT_COLOR),
        showlegend=False,
    ))

    for i, (cat, color) in enumerate(cat_colors.items()):
        fig.add_annotation(
            x=0.98 - i * 0.18, y=1.02, xref="paper", yref="paper",
            text=f"<b>\u25cf</b> {cat}",
            font=dict(size=12, color=color, family=FONT),
            showarrow=False,
        )

    fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(size=11, family=FONT))
    fig.update_yaxes(tickfont=dict(size=12, family=FONT))
    fig.update_layout(xaxis_range=[0, top["block_count"].max() * 1.18])

    median_all = int(merged["block_count"].median())
    return card_layout(fig,
        title="Block-Hitliste \u2014 Meistgeblockte im Cluster",
        subtitle=f"Median \u00fcber alle {len(merged)} Konten: {median_all} Blocks"
    )


# --- Orchestrator ----------------------------------------------------------

def render_all_cards(
    analysis: "AnalysisResult",
    cluster: "ClusterResult",
    cross: "CrossFollowResult",
) -> dict[str, go.Figure]:
    """Render every available card. Returns a dict keyed by card id."""
    scores = analysis.scores_df
    detail = analysis.detail_df
    nodes = cluster.nodes_df
    edges = cluster.edges_df
    blocks = analysis.acquired.blocks_received
    likes = analysis.acquired.likes_made
    sample = cross.sample
    per_acct = cross.per_account

    cards: dict[str, go.Figure] = {
        "card_01_overview": card_1_overview(scores, nodes),
        "card_02_anchors": card_2_anchors(nodes),
        "card_03_behavior": card_3_behavior(scores),
        "card_04_timeline": card_4_timeline(detail),
        "card_05_cluster": card_5_cluster(nodes, edges),
        "card_06_deleted": card_6_deleted(scores),
        "card_07_lifecycle": card_7_lifecycle_waves(detail, scores),
        "card_08_cumulative": card_8_cumulative(detail, scores),
        "card_09_age_at_follow": card_9_age_at_follow(detail),
        "card_10_score_dist": card_10_score_distribution(scores),
        "card_11_scatter": card_11_creation_vs_follow(detail),
    }
    if sample is not None and not sample.empty:
        cards["card_12_amplifiers"] = card_12_amplifiers(scores, sample)
    if per_acct is not None and not per_acct.empty:
        cards["card_13_cross_speed"] = card_13_cross_speed(per_acct)
    if blocks is not None and not blocks.empty and likes is not None and not likes.empty:
        cards["card_14_blocks_likes"] = card_14_blocks_likes(scores, blocks, likes)
    if blocks is not None and not blocks.empty:
        cards["card_15_block_hitlist"] = card_15_block_hitlist(scores, blocks, nodes)
    return cards
