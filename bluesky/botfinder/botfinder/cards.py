"""Social-media-style cards (1200x675) for inline notebook display.

Refactored from ``tmp/generate_cards.py`` — no kaleido / PNG export, anchor
handle parameterised, footer date computed dynamically.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

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

_MONTHS_DE = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]


def _footer_text() -> str:
    now = datetime.now()
    return (
        f"Bot-Netzwerk-Analyse • Bluesky Firehose + AT Protocol • "
        f"{_MONTHS_DE[now.month - 1]} {now.year}"
    )


def card_layout(fig: go.Figure, title: str = "", subtitle: str = "") -> go.Figure:
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
        text=_footer_text(), xref="paper", yref="paper",
        x=0.5, y=-0.14, showarrow=False, xanchor="center", yanchor="bottom",
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


def _date_str() -> str:
    now = datetime.now()
    return f"{now.day:02d}. {_MONTHS_DE[now.month - 1]} {now.year}, {now.strftime('%H:%M')} Uhr"


# ─── Cards ────────────────────────────────────────────────────────────────

def card_1_overview(scores_df: pd.DataFrame, anchor_handle: str) -> go.Figure:
    total = len(scores_df)
    suspicious = int((scores_df["score"] >= 0.5).sum())
    normal = total - suspicious
    deleted = int(scores_df["flags"].fillna("").str.contains("DELETED").sum())
    anonymous = int(scores_df["flags"].fillna("").str.contains("ANONYMOUS_PROFILE").sum())
    instant = int(scores_df["flags"].fillna("").str.contains("INSTANT_FOLLOW").sum())

    fig = make_subplots(
        rows=2, cols=4, row_heights=[0.55, 0.45],
        specs=[[{"colspan": 4, "type": "indicator"}, None, None, None],
               [{"type": "indicator"}] * 4],
        vertical_spacing=0.08,
    )
    fig.add_trace(go.Indicator(
        mode="number", value=total,
        number=dict(font=dict(size=1, color=BG_COLOR)),
    ), row=1, col=1)

    fig.add_annotation(
        text=f"<b>{total}</b> Follower",
        x=0.5, y=0.78, xref="paper", yref="paper",
        font=dict(size=62, color=TEXT_COLOR, family=FONT_BOLD), showarrow=False,
    )
    fig.add_annotation(
        text=f"davon <b>{suspicious}</b> Bots, <b>{normal}</b> unauffällig",
        x=0.5, y=0.58, xref="paper", yref="paper",
        font=dict(size=34, color=ACCENT, family=FONT_BOLD), showarrow=False,
    )
    stats = [
        (deleted, "Gelöscht", ACCENT2),
        (instant, "Sofort-Follow", ACCENT2),
        (anonymous, "Anonym", ACCENT2),
        (normal, "Unauffällig", MUTED),
    ]
    for i, (val, label, color) in enumerate(stats):
        fig.add_trace(go.Indicator(
            mode="number", value=val,
            title=dict(text=label, font=dict(size=14, color=MUTED, family=FONT)),
            number=dict(font=dict(size=42, color=color, family=FONT_BOLD)),
        ), row=2, col=i + 1)

    return card_layout(fig,
        title=f"Bot-Netzwerk um @{anchor_handle}",
        subtitle=f"Analyse vom {_date_str()}",
    )


def card_2_anchors(nodes_df: pd.DataFrame, anchor_handle: str) -> go.Figure:
    if nodes_df.empty:
        return card_layout(go.Figure(), title="Anker-Konten")
    df = nodes_df[nodes_df["handle"] != "bsky.app"].head(10).copy()
    df = df.sort_values("suspect_followers", ascending=True)
    colors = []
    for h in df["handle"]:
        if h == anchor_handle:
            colors.append(ACCENT)
        elif df[df["handle"] == h]["suspect_followers"].iloc[0] >= 50:
            colors.append(ACCENT2)
        else:
            colors.append(ACCENT3)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=["@" + h for h in df["handle"]],
        x=df["suspect_followers"],
        orientation="h", marker_color=colors,
        text=df["suspect_followers"], textposition="outside",
        textfont=dict(size=15, color=TEXT_COLOR, family=FONT),
    ))
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(tickfont=dict(size=14, color=TEXT_COLOR, family=FONT), domain=[0.0, 0.82])
    fig.update_layout(bargap=0.3, margin=dict(l=50, r=70, t=100, b=45))
    return card_layout(fig,
        title="Anker-Konten — Wen das Bot-Cluster pusht",
        subtitle="Konten, die von den meisten verdächtigen Bot-Accounts gemeinsam gefolgt werden",
    )


def card_3_behavior(scores_df: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]],
                        column_widths=[0.4, 0.6], horizontal_spacing=0.08)
    bins = [
        ("Hohes Risiko (≥0,6)", int((scores_df["score"] >= 0.6).sum()), ACCENT),
        ("Mittel (0,5–0,6)", int(((scores_df["score"] >= 0.5) & (scores_df["score"] < 0.6)).sum()), ACCENT2),
        ("Niedrig (<0,5)", int((scores_df["score"] < 0.5).sum()), "#999999"),
    ]
    fig.add_trace(go.Pie(
        labels=[b[0] for b in bins], values=[b[1] for b in bins],
        marker=dict(colors=[b[2] for b in bins]),
        textinfo="percent+value", textfont=dict(size=14, family=FONT), hole=0.4,
    ), row=1, col=1)
    high_risk = scores_df[scores_df["score"] >= 0.5]
    signals = ["temporal_proximity", "anonymity", "activity_pattern", "follow_overlap", "account_age"]
    labels = ["Timing", "Anonymität", "Aktivität", "Überlapp.", "Alter"]
    means = [high_risk[s].mean() if s in high_risk.columns else 0 for s in signals]
    fig.add_trace(go.Bar(
        x=labels, y=means,
        marker_color=[ACCENT, ACCENT2, ACCENT3, "#1565c0", "#6a1b9a"],
        text=[f"{m:.2f}" for m in means], textposition="outside",
        textfont=dict(size=14, color=TEXT_COLOR, family=FONT), showlegend=False,
    ), row=1, col=2)
    fig.update_yaxes(range=[0, 1.08], showgrid=True, gridcolor=GRID_COLOR, row=1, col=2)
    fig.update_xaxes(tickfont=dict(size=13, color=TEXT_COLOR, family=FONT), row=1, col=2)
    return card_layout(fig,
        title="Bot-Verhaltenssignale — Erkennungsmethode",
        subtitle="5-Signal-Scoring: Timing, Profil, Aktivität, Überlappung, Kontoalter",
    )


def card_4_timeline(detail_df: pd.DataFrame) -> go.Figure:
    df = detail_df.copy()
    df["follow_created_at"] = pd.to_datetime(df["follow_created_at"], errors="coerce")
    df = df.dropna(subset=["follow_created_at"])
    if df.empty:
        return card_layout(go.Figure(), title="Follow-Burst-Zeitverlauf")
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
        subtitle="Stündliche Follow-Ereignisse — Spitzen deuten auf koordinierte Bot-Aktivität hin",
    )


def card_5_cluster(nodes_df: pd.DataFrame, edges_df: pd.DataFrame, anchor_handle: str) -> go.Figure:
    """Square cluster graph — concentric rings + perimeter labels."""
    SIZE = 1200
    if nodes_df.empty:
        fig = go.Figure()
        fig.update_layout(width=SIZE, height=SIZE)
        return card_layout(fig, title="Bot-Cluster-Netzwerk")

    G = nx.Graph()
    min_suspect = 10
    filtered = nodes_df[(nodes_df["handle"] != "bsky.app") & (nodes_df["suspect_followers"] >= min_suspect)]
    for _, row in filtered.iterrows():
        G.add_node(row["handle"], weight=row["suspect_followers"])
    handles_set = set(filtered["handle"])
    for _, row in edges_df.iterrows():
        if row["source"] in handles_set and row["target"] in handles_set:
            G.add_edge(row["source"], row["target"], weight=row["shared_followers"])
    if len(G.nodes()) == 0:
        fig = go.Figure()
        fig.update_layout(width=SIZE, height=SIZE)
        return card_layout(fig, title="Bot-Cluster-Netzwerk")

    weights = nx.get_node_attributes(G, "weight")
    max_w = max(weights.values()) if weights else 1
    cluster_members = (
        set(nodes_df[nodes_df["is_cluster_member"] == True]["handle"])
        if "is_cluster_member" in nodes_df.columns else set(G.nodes())
    )
    core_nodes = [n for n in G.nodes() if n in cluster_members or n == anchor_handle]
    periphery_nodes = [n for n in G.nodes() if n not in cluster_members and n != anchor_handle]
    periphery_set = set(periphery_nodes)

    core_sorted = sorted(core_nodes, key=lambda n: weights.get(n, 0), reverse=True)
    pos: dict[str, np.ndarray] = {}
    rings = [1, 5, 15, 40, 80, 200]
    radii = [0.0, 0.18, 0.35, 0.52, 0.68, 0.80]
    placed = 0
    for ring_idx in range(len(rings)):
        ring_count = rings[ring_idx] - (rings[ring_idx - 1] if ring_idx > 0 else 0)
        radius = radii[ring_idx]
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
    for i, n in enumerate(core_sorted[placed:]):
        angle = 2 * np.pi * i / max(1, len(core_sorted) - placed) + 0.1
        pos[n] = np.array([0.85 * np.cos(angle), 0.85 * np.sin(angle)])

    if periphery_nodes:
        margin = 1.05
        n_p = len(periphery_nodes)
        perimeter = 8 * margin
        for i, n in enumerate(periphery_nodes):
            t = (i / n_p) * perimeter
            if t < 2 * margin:
                pos[n] = np.array([-margin + t, margin])
            elif t < 4 * margin:
                pos[n] = np.array([margin, margin - (t - 2 * margin)])
            elif t < 6 * margin:
                pos[n] = np.array([margin - (t - 4 * margin), -margin])
            else:
                pos[n] = np.array([-margin, -margin + (t - 6 * margin)])

    edge_core_x: list = []; edge_core_y: list = []
    edge_peri_x: list = []; edge_peri_y: list = []
    for u, v in G.edges():
        x0, y0 = pos[u]; x1, y1 = pos[v]
        if u in periphery_set or v in periphery_set:
            edge_peri_x.extend([x0, x1, None]); edge_peri_y.extend([y0, y1, None])
        else:
            edge_core_x.extend([x0, x1, None]); edge_core_y.extend([y0, y1, None])

    edge_core = go.Scatter(x=edge_core_x, y=edge_core_y, mode="lines",
                           line=dict(width=0.4, color="rgba(200,0,0,0.15)"),
                           hoverinfo="none", showlegend=False)
    edge_peri = go.Scatter(x=edge_peri_x, y=edge_peri_y, mode="lines",
                           line=dict(width=0.4, color="rgba(0,160,0,0.18)"),
                           hoverinfo="none", showlegend=False)

    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    sizes = [max(7, 45 * (weights.get(n, 0) / max_w)) for n in G.nodes()]
    colors = []
    for n in G.nodes():
        if n == anchor_handle:
            colors.append(ACCENT)
        elif n in periphery_set:
            colors.append("#aaaaaa")
        elif weights.get(n, 0) >= max_w * 0.3:
            colors.append(ACCENT2)
        else:
            colors.append(ACCENT3)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers",
        marker=dict(size=sizes, color=colors, line=dict(width=0.6, color="#333333")),
        hovertext=[f"@{n}: {weights.get(n,0)} suspects, {G.degree(n)} edges" for n in G.nodes()],
        hoverinfo="text", showlegend=False,
    )

    sorted_nodes = sorted(G.nodes(), key=lambda n: weights.get(n, 0), reverse=True)
    top_core = [n for n in sorted_nodes if n in core_nodes][:15]
    core_label = go.Scatter(
        x=[pos[n][0] for n in top_core], y=[pos[n][1] for n in top_core],
        mode="text", text=["@" + n.split(".")[0] for n in top_core],
        textposition="top center",
        textfont=dict(size=9, color=TEXT_COLOR, family=FONT),
        hoverinfo="none", showlegend=False,
    )

    fig = go.Figure(data=[edge_peri, edge_core, node_trace, core_label])
    fig.update_xaxes(visible=False, range=[-1.6, 1.6])
    fig.update_yaxes(visible=False, range=[-1.4, 1.4], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        width=SIZE, height=SIZE,
        paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR,
        margin=dict(l=10, r=10, t=70, b=70),
        font=dict(color=TEXT_COLOR, family=FONT, size=14),
        annotations=[
            dict(text="<b>Bot-Cluster-Netzwerk</b>", xref="paper", yref="paper",
                 x=0.5, y=1.06, showarrow=False, xanchor="center", yanchor="top",
                 font=dict(size=28, color=TEXT_COLOR, family=FONT_BOLD)),
            dict(text=(f"Kern: {len(core_nodes)} • Ring: {len(periphery_nodes)} • "
                       f"Knoten = co-gefolgte Anker"),
                 xref="paper", yref="paper",
                 x=0.5, y=1.015, showarrow=False, xanchor="center", yanchor="top",
                 font=dict(size=13, color=MUTED, family=FONT)),
            dict(text=_footer_text(), xref="paper", yref="paper",
                 x=0.5, y=-0.05, showarrow=False, xanchor="center", yanchor="top",
                 font=dict(size=9, color="#999999", family=FONT)),
        ],
    )
    return fig


def card_6_deleted(scores_df: pd.DataFrame) -> go.Figure:
    deleted = scores_df["flags"].fillna("").str.contains("DELETED")
    total_deleted = int(deleted.sum())
    total_active = len(scores_df) - total_deleted
    pct = 100 * total_deleted / max(len(scores_df), 1)
    fig = make_subplots(
        rows=2, cols=1, row_heights=[0.35, 0.65],
        specs=[[{"type": "indicator"}], [{"type": "xy"}]],
        vertical_spacing=0.12,
    )
    fig.add_trace(go.Indicator(
        mode="number", value=total_deleted,
        number=dict(font=dict(size=64, color=ACCENT, family=FONT_BOLD), suffix=f"  ({pct:.0f}%)"),
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=[total_active, total_deleted], y=["Noch aktiv", "Gelöscht/Gesperrt"],
        orientation="h", marker_color=["#cccccc", ACCENT],
        text=[total_active, total_deleted], textposition="inside",
        textfont=dict(size=18, color="white", family=FONT), showlegend=False,
    ), row=2, col=1)
    fig.update_xaxes(visible=False, row=2, col=1)
    fig.update_yaxes(tickfont=dict(size=16, color=TEXT_COLOR, family=FONT), row=2, col=1)
    fig.update_layout(margin=dict(l=50, r=50, t=120, b=45))
    return card_layout(fig,
        title="Kontolöschungen — Hinweis auf Bot-Bereinigung",
        subtitle="Konten, die der Anker folgten und inzwischen gelöscht oder gesperrt wurden",
    )


def card_7_lifecycle(detail_df: pd.DataFrame, scores_df: pd.DataFrame) -> go.Figure:
    merged = detail_df.merge(
        scores_df[["did", "flags"]], left_on="follower_did", right_on="did", how="left"
    )
    df = merged.copy()
    df["follower_created_at"] = pd.to_datetime(df["follower_created_at"], errors="coerce")
    df["follow_created_at"] = pd.to_datetime(df["follow_created_at"], errors="coerce")
    df = df.dropna(subset=["follower_created_at", "follow_created_at"])
    if df.empty:
        return card_layout(go.Figure(), title="Lebenszyklus-Wellen")
    bin_freq = "1h"
    df["created_bin"] = df["follower_created_at"].dt.floor(bin_freq)
    df["follow_bin"] = df["follow_created_at"].dt.floor(bin_freq)
    t_min = df["follower_created_at"].min().floor("h")
    t_max = df["follow_created_at"].max().ceil("h")
    all_bins = pd.date_range(t_min, t_max, freq=bin_freq)
    created = df.groupby("created_bin").size().reindex(all_bins, fill_value=0)
    followed = df.groupby("follow_bin").size().reindex(all_bins, fill_value=0)
    x_labels = [t.strftime("%d.%m. %H:%M") for t in all_bins]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_labels, y=created.values, name="Konten erstellt",
                         marker_color="rgba(30,136,229,0.6)"))
    fig.add_trace(go.Bar(x=x_labels, y=followed.values, name="Follow-Ereignisse",
                         marker_color="rgba(204,0,0,0.5)"))
    y_max = max(created.max(), followed.max())
    fig.update_xaxes(title_text="Zeit (UTC)", tickfont=dict(size=11, family=FONT),
                     showgrid=False, tickangle=-45)
    fig.update_yaxes(title_text="Ereignisse pro Stunde", tickfont=dict(size=13, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR, range=[0, y_max * 1.15])
    fig.update_layout(barmode="group",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                  xanchor="right", x=1.0,
                                  font=dict(size=13, family=FONT)))
    return card_layout(fig,
        title="Lebenszyklus-Wellen — Erstellung & Follow-Aktivität",
        subtitle="Kontoerstellungs-Bursts eng gekoppelt mit Follow-Ereignissen",
    )


def card_8_cumulative(detail_df: pd.DataFrame, scores_df: pd.DataFrame) -> go.Figure:
    merged = detail_df.merge(
        scores_df[["did", "flags"]], left_on="follower_did", right_on="did", how="left"
    )
    df = merged.copy()
    df["is_deleted"] = df["flags"].fillna("").str.contains("DELETED")
    df["follow_created_at"] = pd.to_datetime(df["follow_created_at"], errors="coerce")
    df = df.dropna(subset=["follow_created_at"])
    if df.empty:
        return card_layout(go.Figure(), title="Kumulatives Netzwerk-Wachstum")
    bin_freq = "1h"
    df["follow_bin"] = df["follow_created_at"].dt.floor(bin_freq)
    t_min = df["follow_created_at"].min().floor("h")
    t_max = df["follow_created_at"].max().ceil("h")
    all_bins = pd.date_range(t_min, t_max, freq=bin_freq)
    follow = df.groupby("follow_bin").size().reindex(all_bins, fill_value=0)
    deleted = df[df["is_deleted"]].groupby("follow_bin").size().reindex(all_bins, fill_value=0)
    cum_total = follow.cumsum()
    cum_deleted = deleted.cumsum()
    cum_surv = cum_total - cum_deleted
    x = all_bins.to_pydatetime().tolist()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=cum_total.values, name="Gesamt gefolgt", mode="lines",
                             line=dict(width=2.5, color="#555555", dash="dot")))
    fig.add_trace(go.Scatter(x=x, y=cum_surv.values, name="Überlebend", mode="lines",
                             line=dict(width=3, color="#2e7d32")))
    fig.add_trace(go.Scatter(x=x, y=cum_deleted.values, name="Gelöscht", mode="lines",
                             line=dict(width=3, color=ACCENT),
                             fill="tozeroy", fillcolor="rgba(204,0,0,0.1)"))
    fig.update_xaxes(title_text="Zeit (UTC)", tickfont=dict(size=11, family=FONT),
                     showgrid=False, tickangle=-45, tickformat="%d.%m. %H:%M")
    fig.update_yaxes(title_text="Kumulierte Konten", tickfont=dict(size=13, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR)
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.18,
                                  xanchor="center", x=0.5,
                                  font=dict(size=12, family=FONT)))
    return card_layout(fig,
        title="Kumulatives Netzwerk-Wachstum & Schwund",
        subtitle="Laufende Summe: Wachstum vs. Bereinigung",
    )


def card_9_age_at_follow(detail_df: pd.DataFrame) -> go.Figure:
    ages = detail_df["age_at_follow_minutes"].dropna()
    if ages.empty:
        return card_layout(go.Figure(), title="Dauer von Erstellung bis Follow")
    bins = [0, 1, 2, 5, 10, 30, 60, 120, 360, 1440]
    labels = ["<1m", "1–2m", "2–5m", "5–10m", "10–30m", "30–60m", "1–2h", "2–6h", "6–24h"]
    bucketed = pd.cut(ages, bins=bins, labels=labels, right=False)
    counts = bucketed.value_counts().reindex(labels, fill_value=0)
    colors = [ACCENT if i < 3 else ACCENT2 if i < 5 else ACCENT3 for i in range(len(labels))]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=counts.values, marker_color=colors,
                         text=counts.values, textposition="outside",
                         textfont=dict(size=14, family=FONT)))
    fig.update_xaxes(title_text="Zeit von Kontoerstellung bis Follow",
                     tickfont=dict(size=14, family=FONT))
    fig.update_yaxes(title_text="Anzahl Konten",
                     tickfont=dict(size=13, family=FONT), showgrid=True, gridcolor=GRID_COLOR)
    under_5 = int(counts.iloc[:3].sum())
    total = int(counts.sum())
    return card_layout(fig,
        title="Dauer von Erstellung bis Follow",
        subtitle=f"{under_5} von {total} neuen Konten ({100*under_5/max(total,1):.0f}%) folgten "
                 "innerhalb von 5 Min. nach Erstellung",
    )


def card_10_score_distribution(scores_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=scores_df["score"], nbinsx=25,
                               marker_color=ACCENT, opacity=0.85))
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
    return card_layout(fig,
        title="Bot-Score-Verteilung",
        subtitle=f"Mittelwert: {scores_df['score'].mean():.2f} — höher = bot-ähnlicheres Verhalten",
    )


def card_11_creation_vs_follow(detail_df: pd.DataFrame) -> go.Figure:
    df = detail_df.dropna(subset=["age_at_follow_minutes"]).copy()
    if df.empty:
        return card_layout(go.Figure(), title="Kontoerstellung vs. Zeit bis Follow")
    df["age_capped"] = df["age_at_follow_minutes"].clip(upper=120)
    df["follower_created_at"] = pd.to_datetime(df["follower_created_at"], errors="coerce")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["follower_created_at"], y=df["age_capped"], mode="markers",
        marker=dict(size=5, opacity=0.7, color=df["age_capped"].values,
                    colorscale="RdYlGn", cmin=0, cmax=60, showscale=True,
                    colorbar=dict(title=dict(text="Min", font=dict(size=12, family=FONT)),
                                  tickfont=dict(size=11, family=FONT))),
    ))
    fig.add_hline(y=5, line_dash="dash", line_color=ACCENT, line_width=1.5,
                  annotation_text="5-Min-Schwelle", annotation_position="top right",
                  annotation_font=dict(size=12, family=FONT, color=ACCENT))
    fig.update_xaxes(title_text="Konto erstellt am (UTC)",
                     tickfont=dict(size=12, family=FONT))
    fig.update_yaxes(title_text="Minuten bis Follow", tickfont=dict(size=12, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR)
    return card_layout(fig,
        title="Kontoerstellung vs. Zeit bis Follow",
        subtitle="Rote Punkte = Follow fast sofort nach Kontoerstellung",
    )


def card_12_amplifiers(scores_df: pd.DataFrame, cross_df: pd.DataFrame) -> go.Figure:
    flags = scores_df["flags"].fillna("")
    amp = scores_df[(scores_df["score"] < 0.5) & flags.str.contains("AMPLIFICATION")]
    non_amp = scores_df[(scores_df["score"] < 0.5) & ~flags.str.contains("AMPLIFICATION")]
    bots = scores_df[scores_df["score"] >= 0.5]
    n_amp = len(amp)
    n_amp_anon = int(amp["flags"].fillna("").str.contains("ANONYMOUS").sum())
    valid = cross_df[cross_df["total_follows_fetched"] > 0] if not cross_df.empty else pd.DataFrame()
    bot_cross = valid[valid["is_bot"]] if not valid.empty else pd.DataFrame()
    non_bot_cross = valid[~valid["is_bot"]] if not valid.empty else pd.DataFrame()
    bot_pct = bot_cross["cohort_pct"].mean() if not bot_cross.empty else 0
    non_pct = non_bot_cross["cohort_pct"].mean() if not non_bot_cross.empty else 0
    non_n = non_bot_cross["cohort_follows"].mean() if not non_bot_cross.empty else 0

    fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55],
                        horizontal_spacing=0.12,
                        specs=[[{"type": "pie"}, {"type": "bar"}]])
    fig.add_trace(go.Pie(
        labels=[f"Bots ({len(bots)})", f"Verstärker ({n_amp})", f"Unauffällig ({len(non_amp)})"],
        values=[len(bots), n_amp, len(non_amp)],
        marker=dict(colors=[ACCENT, ACCENT3, "#bbbbbb"]),
        textinfo="percent+label", textfont=dict(size=12, family=FONT),
        hole=0.35, showlegend=False,
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=["Bots", "Verstärker/\nNon-Bots"], y=[bot_pct, non_pct],
        marker_color=[ACCENT, ACCENT3],
        text=[f"{v:.0f}%" for v in [bot_pct, non_pct]],
        textposition="outside",
        textfont=dict(size=16, family=FONT_BOLD, color=TEXT_COLOR),
        showlegend=False, width=0.5,
    ), row=1, col=2)
    fig.update_yaxes(title_text="Ø Quervernetzung (%)",
                     tickfont=dict(size=12, family=FONT),
                     showgrid=True, gridcolor=GRID_COLOR,
                     range=[0, max(bot_pct, non_pct, 1) * 1.3], row=1, col=2)
    fig.update_xaxes(tickfont=dict(size=13, family=FONT), row=1, col=2)
    return card_layout(fig,
        title="Verstärker-Konten — Koordinierte Quervernetzung",
        subtitle=f"{n_amp} Amplifier-Konten • Ø {non_n:.0f} gegenseitige Follows • {n_amp_anon} anonym",
    )


def card_13_cross_speed(per_account_df: pd.DataFrame) -> go.Figure:
    if per_account_df.empty:
        return card_layout(go.Figure(), title="Quervernetzungs-Geschwindigkeit")
    df = per_account_df.copy()
    df["first_cross_min"] = df["first_cross"] * 1440
    df["first_cross_capped"] = df["first_cross_min"].clip(upper=120)
    cat_order = ["Bot", "Verstärker", "Unauffällig"]
    cat_colors = {"Bot": ACCENT, "Verstärker": ACCENT3, "Unauffällig": MUTED}
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45],
                        horizontal_spacing=0.12,
                        subplot_titles=["Minuten bis erste Quervernetzung",
                                        "Anteil < 60 Min"])
    for cat in cat_order:
        s = df[df["category"] == cat]
        fig.add_trace(go.Box(y=s["first_cross_capped"], name=cat,
                             marker_color=cat_colors[cat], boxmean=True,
                             showlegend=False, width=0.5), row=1, col=1)
    pcts, labels, colors = [], [], []
    for cat in cat_order:
        s = df[df["category"] == cat]
        pct = 100 * (s["first_cross_min"] < 60).sum() / len(s) if len(s) else 0
        pcts.append(pct); labels.append(cat); colors.append(cat_colors[cat])
    fig.add_trace(go.Bar(x=labels, y=pcts, marker_color=colors,
                         text=[f"{v:.0f}%" for v in pcts], textposition="outside",
                         textfont=dict(size=16, family=FONT_BOLD, color=TEXT_COLOR),
                         showlegend=False, width=0.5), row=1, col=2)
    fig.update_yaxes(title_text="Minuten", showgrid=True, gridcolor=GRID_COLOR,
                     tickfont=dict(size=11, family=FONT), range=[0, 125], row=1, col=1)
    fig.update_yaxes(title_text="%", range=[0, 115], showgrid=True,
                     gridcolor=GRID_COLOR, tickfont=dict(size=11, family=FONT), row=1, col=2)
    fig.update_xaxes(tickfont=dict(size=12, family=FONT))
    bot = df[df["category"] == "Bot"]
    bot_med = bot["first_cross_min"].median() if len(bot) else 0
    bot_pct60 = 100 * (bot["first_cross_min"] < 60).sum() / len(bot) if len(bot) else 0
    fig = card_layout(fig,
        title="Quervernetzungs-Geschwindigkeit",
        subtitle=f"Bot-Median: {bot_med:.0f} Min • {bot_pct60:.0f}% der Bots vernetzen sich in < 1 Stunde")
    fig.update_layout(margin=dict(t=140, b=65))
    return fig


def card_14_blocks_likes(
    scores_df: pd.DataFrame, blocks_df: pd.DataFrame, likes_df: pd.DataFrame
) -> go.Figure:
    if blocks_df.empty or likes_df.empty:
        return card_layout(go.Figure(), title="Blockiert & Liken")
    if "subject" in blocks_df.columns:
        blocks_df = blocks_df.rename(columns={"subject": "did"})
    merged = scores_df.merge(blocks_df, on="did", how="left").merge(likes_df, on="did", how="left")
    merged["block_count"] = merged["block_count"].fillna(0).astype(int)
    merged["like_count"] = merged["like_count"].fillna(0).astype(int)
    flags = merged["flags"].fillna("")
    is_bot = merged["score"] >= 0.5
    is_amp = (merged["score"] < 0.5) & flags.str.contains("AMPLIFICATION")
    is_norm = (merged["score"] < 0.5) & ~flags.str.contains("AMPLIFICATION")

    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5],
                        horizontal_spacing=0.12,
                        subplot_titles=["Ø Blocks erhalten", "Ø Likes abgegeben"])
    cats = ["Bots", "Verstärker", "Unauffällig"]
    block_means = [merged[is_bot]["block_count"].mean(),
                   merged[is_amp]["block_count"].mean(),
                   merged[is_norm]["block_count"].mean()]
    like_means = [merged[is_bot]["like_count"].mean(),
                  merged[is_amp]["like_count"].mean(),
                  merged[is_norm]["like_count"].mean()]
    bar_colors = [ACCENT, ACCENT3, MUTED]
    fig.add_trace(go.Bar(x=cats, y=block_means, marker_color=bar_colors,
                         text=[f"{v:.0f}" for v in block_means], textposition="outside",
                         textfont=dict(size=14, family=FONT_BOLD, color=TEXT_COLOR),
                         showlegend=False, width=0.5), row=1, col=1)
    fig.add_trace(go.Bar(x=cats, y=like_means, marker_color=bar_colors,
                         text=[f"{v:.0f}" for v in like_means], textposition="outside",
                         textfont=dict(size=14, family=FONT_BOLD, color=TEXT_COLOR),
                         showlegend=False, width=0.5), row=1, col=2)
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR,
                     tickfont=dict(size=11, family=FONT))
    fig.update_xaxes(tickfont=dict(size=12, family=FONT))
    fig.update_yaxes(range=[0, max(block_means) * 1.25 if block_means else 1], row=1, col=1)
    fig.update_yaxes(range=[0, max(like_means) * 1.35 if like_means else 1], row=1, col=2)
    amp_block_median = int(merged[is_amp]["block_count"].median()) if is_amp.sum() else 0
    return card_layout(fig,
        title="Blockiert & Liken — Alle Kategorien betroffen",
        subtitle=f"Verstärker-Median: {amp_block_median} Blocks erhalten",
    )


def card_15_block_hitlist(
    scores_df: pd.DataFrame, blocks_df: pd.DataFrame, nodes_df: pd.DataFrame
) -> go.Figure:
    if blocks_df.empty:
        return card_layout(go.Figure(), title="Block-Hitliste")
    if "subject" in blocks_df.columns:
        blocks_df = blocks_df.rename(columns={"subject": "did"})
    merged = scores_df[["did", "score", "flags"]].merge(blocks_df, on="did", how="left")
    merged["block_count"] = merged["block_count"].fillna(0).astype(int)
    if not nodes_df.empty:
        merged = merged.merge(
            nodes_df[["did", "handle"]].drop_duplicates(), on="did", how="left"
        )
    else:
        merged["handle"] = pd.NA
    merged["category"] = "Unauffällig"
    merged.loc[merged["score"] >= 0.5, "category"] = "Bot"
    flags = merged["flags"].fillna("")
    merged.loc[(merged["score"] < 0.5) & flags.str.contains("AMPLIFICATION"), "category"] = "Verstärker"
    top = merged.nlargest(15, "block_count").copy()
    if top.empty or top["block_count"].max() == 0:
        return card_layout(go.Figure(), title="Block-Hitliste",
                           subtitle="Keine Block-Daten verfügbar")
    top["label"] = top["handle"].apply(
        lambda h: f"@{h.replace('.bsky.social', '')}" if pd.notna(h) else "(anonym)"
    )
    top = top.sort_values("block_count", ascending=True)
    cat_colors = {"Bot": ACCENT, "Verstärker": ACCENT3, "Unauffällig": MUTED}
    colors = [cat_colors[c] for c in top["category"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top["label"], x=top["block_count"], orientation="h",
        marker_color=colors,
        text=[f"{v:,}".replace(",", ".") for v in top["block_count"]],
        textposition="outside",
        textfont=dict(size=13, family=FONT_BOLD, color=TEXT_COLOR),
        showlegend=False,
    ))
    fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR,
                     tickfont=dict(size=11, family=FONT))
    fig.update_yaxes(tickfont=dict(size=12, family=FONT))
    fig.update_layout(xaxis_range=[0, top["block_count"].max() * 1.18])
    median_all = int(merged["block_count"].median())
    return card_layout(fig,
        title="Block-Hitliste — Meistgeblockte im Cluster",
        subtitle=f"Median über alle {len(merged)} Konten: {median_all} Blocks",
    )


# ─── Orchestrator ─────────────────────────────────────────────────────────

def render_all_cards(
    analysis: "AnalysisResult",
    cluster: "ClusterResult",
    cross: "CrossFollowResult",
) -> dict[str, go.Figure]:
    """Render every available card. Returns a dict keyed by card id."""
    cfg = analysis.config
    scores = analysis.scores_df
    detail = analysis.detail_df
    nodes = cluster.nodes_df
    edges = cluster.edges_df
    blocks = analysis.acquired.blocks_received
    likes = analysis.acquired.likes_made
    sample = cross.sample
    per_acct = cross.per_account

    cards: dict[str, go.Figure] = {
        "card_01_overview": card_1_overview(scores, cfg.anchor_handle),
        "card_02_anchors": card_2_anchors(nodes, cfg.anchor_handle),
        "card_03_behavior": card_3_behavior(scores),
        "card_04_timeline": card_4_timeline(detail),
        "card_05_cluster": card_5_cluster(nodes, edges, cfg.anchor_handle),
        "card_06_deleted": card_6_deleted(scores),
        "card_07_lifecycle": card_7_lifecycle(detail, scores),
        "card_08_cumulative": card_8_cumulative(detail, scores),
        "card_09_age_at_follow": card_9_age_at_follow(detail),
        "card_10_score_dist": card_10_score_distribution(scores),
        "card_11_scatter": card_11_creation_vs_follow(detail),
    }
    if not sample.empty:
        cards["card_12_amplifiers"] = card_12_amplifiers(scores, sample)
    if not per_acct.empty:
        cards["card_13_cross_speed"] = card_13_cross_speed(per_acct)
    if not blocks.empty and not likes.empty:
        cards["card_14_blocks_likes"] = card_14_blocks_likes(scores, blocks, likes)
    if not blocks.empty:
        cards["card_15_block_hitlist"] = card_15_block_hitlist(scores, blocks, nodes)
    return cards
