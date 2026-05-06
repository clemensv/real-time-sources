"""HTML dossier report generator using Jinja2 templates."""

from datetime import datetime, timezone
from pathlib import Path

import plotly.io as pio
from jinja2 import Template

from .scoring import BotScore


DOSSIER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Bot Network Dossier — @{{ target_handle }}</title>
<style>
:root { --bg: #ffffff; --surface: #f5f5f5; --accent: #cc0000; --text: #1a1a1a; --muted: #555555; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; line-height: 1.6; }
h1 { color: var(--accent); margin-bottom: 0.5rem; font-size: 2rem; }
h2 { color: var(--accent); margin: 2rem 0 1rem; border-bottom: 1px solid var(--accent); padding-bottom: 0.3rem; }
h3 { color: var(--text); margin: 1.5rem 0 0.5rem; }
.subtitle { color: var(--muted); margin-bottom: 2rem; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.kpi { background: var(--surface); border-radius: 8px; padding: 1.2rem; text-align: center; border-left: 4px solid var(--accent); }
.kpi .value { font-size: 2rem; font-weight: bold; color: var(--accent); }
.kpi .label { font-size: 0.85rem; color: var(--muted); margin-top: 0.3rem; }
.chart-container { background: var(--surface); border-radius: 8px; padding: 1rem; margin: 1.5rem 0; }
.methodology { background: var(--surface); border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; }
.methodology ul { margin-left: 1.5rem; }
.methodology li { margin: 0.5rem 0; }
table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.85rem; }
th, td { padding: 0.5rem 0.8rem; text-align: left; border-bottom: 1px solid #ddd; }
th { background: var(--surface); color: var(--accent); position: sticky; top: 0; }
tr:hover { background: rgba(233,69,96,0.1); }
.score-high { color: #cc0000; font-weight: bold; }
.score-medium { color: #cc5500; }
.score-low { color: #228b22; }
.flag { display: inline-block; background: var(--accent); color: white; font-size: 0.7rem;
        padding: 0.1rem 0.4rem; border-radius: 3px; margin: 0.1rem; }
.findings { background: var(--surface); border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0;
            border-left: 4px solid var(--accent); }
.footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #333; color: var(--muted); font-size: 0.8rem; }
</style>
</head>
<body>

<h1>🚨 Bot Network Dossier</h1>
<p class="subtitle">Target: <strong>@{{ target_handle }}</strong> — Generated {{ generated_at }}</p>

<h2>Executive Summary</h2>
<div class="findings">
<p>Analysis of <strong>{{ stats.total_suspects }}</strong> followers of <strong>@{{ target_handle }}</strong>
reveals a coordinated inauthentic behavior (CIB) pattern consistent with a manufactured follower network:</p>
<ul style="margin: 1rem 0 0 1.5rem;">
<li><strong>{{ stats.high_confidence_bots }}</strong> accounts ({{ "%.0f"|format(stats.high_confidence_bots / stats.total_suspects * 100) }}%) scored as <em>high-confidence bots</em> (score ≥ 0.7)</li>
<li><strong>{{ stats.medium_confidence_bots }}</strong> accounts ({{ "%.0f"|format(stats.medium_confidence_bots / stats.total_suspects * 100) }}%) scored as <em>medium-confidence bots</em> (score 0.4–0.7)</li>
<li><strong>{{ "%.0f"|format(stats.pct_instant_follow) }}%</strong> of recent followers followed within 5 minutes of account creation</li>
<li><strong>{{ "%.0f"|format(stats.pct_anonymous) }}%</strong> have anonymous/incomplete profiles</li>
<li>Account creations cluster in tight temporal bursts indicating automation</li>
</ul>
</div>

<h2>Key Performance Indicators</h2>
<div class="kpi-grid">
<div class="kpi"><div class="value">{{ stats.total_suspects }}</div><div class="label">Total Followers Analyzed</div></div>
<div class="kpi"><div class="value">{{ stats.high_confidence_bots }}</div><div class="label">High-Confidence Bots</div></div>
<div class="kpi"><div class="value">{{ "%.0f"|format(stats.pct_instant_follow) }}%</div><div class="label">Instant Follows (&lt;5 min)</div></div>
<div class="kpi"><div class="value">{{ "%.0f"|format(stats.pct_anonymous) }}%</div><div class="label">Anonymous Profiles</div></div>
<div class="kpi"><div class="value">{{ "%.2f"|format(stats.mean_score) }}</div><div class="label">Mean Bot Score</div></div>
<div class="kpi"><div class="value">{{ "%.2f"|format(stats.p90_score) }}</div><div class="label">P90 Bot Score</div></div>
</div>

<h2>Temporal Analysis</h2>
{% for chart_html in chart_htmls[:4] %}
<div class="chart-container">{{ chart_html }}</div>
{% endfor %}

<h2>Bot Score Analysis</h2>
{% for chart_html in chart_htmls[4:6] %}
<div class="chart-container">{{ chart_html }}</div>
{% endfor %}

{% if chart_htmls|length > 6 %}
<h2>Network Coordination</h2>
{% for chart_html in chart_htmls[6:] %}
<div class="chart-container">{{ chart_html }}</div>
{% endfor %}
{% endif %}

<h2>Top Suspect Accounts</h2>
<div style="overflow-x: auto; max-height: 600px; overflow-y: auto;">
<table>
<thead>
<tr><th>Handle</th><th>Display Name</th><th>Bot Score</th><th>Flags</th><th>Posts</th><th>Followers</th><th>Age@Follow</th><th>Source</th></tr>
</thead>
<tbody>
{% for row in top_suspects %}
<tr>
<td><a href="https://bsky.app/profile/{{ row.handle }}" target="_blank" style="color: var(--accent);">@{{ row.handle }}</a></td>
<td>{{ row.display_name or '—' }}</td>
<td class="{{ 'score-high' if row.total_score >= 0.7 else 'score-medium' if row.total_score >= 0.4 else 'score-low' }}">{{ "%.2f"|format(row.total_score) }}</td>
<td>{% for f in row.flags %}<span class="flag">{{ f }}</span>{% endfor %}</td>
<td>{{ row.posts_count }}</td>
<td>{{ row.followers_count }}</td>
<td>{{ row.age_minutes if row.age_minutes >= 0 else '—' }} {{ 'min' if row.age_minutes >= 0 else '' }}</td>
<td>{{ row.source }}</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>

<h2>Methodology</h2>
<div class="methodology">
<h3>Detection Signals (Weighted Composite Score)</h3>
<ul>
<li><strong>Temporal Proximity (30%)</strong> — Time between account creation and first follow of target. Instant follows (&lt;5 min) are the strongest single indicator of automation.</li>
<li><strong>Follow Overlap (20%)</strong> — Coordination signal: suspect accounts following the same set of other targets indicates botnet control from a single operator.</li>
<li><strong>Activity Pattern (20%)</strong> — Post behavior analysis: high repost ratio, no original content, multilingual posting, and low engagement received.</li>
<li><strong>Anonymity (15%)</strong> — Profile completeness: missing avatar, display name, bio, or algorithmically-generated handle patterns.</li>
<li><strong>Account Age (15%)</strong> — Absolute age of the account. Brand-new accounts (&lt;24h) created in temporal clusters are highly suspicious.</li>
</ul>
<h3>Data Sources</h3>
<ul>
<li>Bluesky Firehose — Real-time ingestion of profiles, follows, and posts</li>
<li>Bluesky AT Protocol — Profile enrichment, feed analysis, follow graph traversal</li>
</ul>
<h3>Academic Basis</h3>
<ul>
<li>Yang & Menczer (2023) "Anatomy of an AI-powered malicious social botnet" — arXiv:2307.16336</li>
<li>DFRLab "#BotSpot: Twelve Ways to Spot a Bot" — Activity, Anonymity, Amplification framework</li>
<li>Botometer/BotometerLite — Indiana University OSoMe</li>
</ul>
</div>

<div class="footer">
<p>Generated by <code>nius-bot-dossier</code> | Analysis period: last {{ lookback_days }} days | Target: @{{ target_handle }}</p>
<p>This report uses heuristic scoring. High scores indicate bot-like behavior but are not definitive proof. Human review recommended.</p>
</div>

</body>
</html>"""


def render_dossier(
    target_handle: str,
    stats: dict,
    figures: list,
    top_suspects: list[dict],
    lookback_days: int,
    output_path: Path,
) -> Path:
    """Render the full HTML dossier report."""
    chart_htmls = []
    for fig in figures:
        html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn" if not chart_htmls else False)
        chart_htmls.append(html)

    template = Template(DOSSIER_TEMPLATE)
    html_content = template.render(
        target_handle=target_handle,
        stats=stats,
        chart_htmls=chart_htmls,
        top_suspects=top_suspects,
        lookback_days=lookback_days,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )

    output_path.write_text(html_content, encoding="utf-8")
    return output_path
