"""
AI Resume Skill Gap Analyzer — v2
Premium UI · Accurate Analysis · Weighted Scoring · ATS Intelligence

Run: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time, re, io

from text_extractor import extract_text, preprocess_text
from skill_extractor import (
    extract_skills,
    get_flat_skill_list,
    group_by_category,
    compare_skills,
    get_ats_analysis,
    semantic_similarity,
)
from skill_database import get_recommendation
from pdf_export import build_weekly_plan, generate_html_report
from job_roles import (
    detect_job_role, get_interview_questions, get_letter_grade,
    get_competitive_score, generate_cover_letter, analyze_bullets,
)

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SkillScope AI — Resume Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:12px 0 4px;'>
        <span style='font-size:1.5rem;font-weight:800;background:linear-gradient(90deg,#7C3AED,#00F5FF);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>⚡ SkillScope AI</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🌙 Theme**")
    theme_choice = st.radio(
        "Select Theme", ["Dark (Default)", "Light"],
        label_visibility="collapsed", key="theme_choice",
    )
    st.markdown("---")
    st.markdown("**ℹ️ About**")
    st.caption("AI-powered resume analyzer with weighted scoring, ATS simulation, and personalised learning roadmaps.")
    st.markdown("---")
    st.caption("⚡ Built with Python + Streamlit")

# ═══════════════════════════════════════════════════════════════
#  STYLES
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMain"],
[data-testid="block-container"] {
    background: #0B1020 !important;
    font-family: 'Inter', sans-serif !important;
    color: #E6E9F2 !important;
}

/* hide chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; visibility: hidden !important; }

/* ── Hero ── */
.hero {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 56px 48px 48px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 36px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 20% 50%, rgba(124,58,237,.15) 0%, transparent 70%),
        radial-gradient(ellipse 60% 50% at 80% 50%, rgba(0,245,255,.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(0,245,255,0.3);
    color: #00F5FF;
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 999px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    font-weight: 700;
    line-height: 1.15;
    background: linear-gradient(90deg, #7C3AED, #00F5FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
    position: relative;
    letter-spacing: -1px;
}
.hero-sub {
    color: #B8C1EC;
    font-size: 1.05rem;
    max-width: 560px;
    margin: 0 auto 32px;
    line-height: 1.75;
    position: relative;
    font-weight: 400;
}
.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    position: relative;
}
.hero-chip {
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(0,245,255,0.3);
    color: #00F5FF;
    font-size: .78rem;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* ── Panel / Card ── */
.panel {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 28px;
    transition: all .3s ease;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.panel:hover { transform: translateY(-5px); border-color: rgba(0,245,255,0.2); box-shadow: 0 15px 40px rgba(0,245,255,0.1); }

/* ── Section label ── */
.sec-label {
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #7C3AED;
    margin-bottom: 6px;
}
.sec-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #E6E9F2;
    margin-bottom: 16px;
    letter-spacing: -.3px;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0,245,255,.3) !important;
    border-radius: 16px !important;
    background: rgba(124,58,237,.08) !important;
    padding: 8px !important;
    transition: all .3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,245,255,.7) !important;
    background: rgba(124,58,237,.15) !important;
    box-shadow: 0 0 20px rgba(0,245,255,.1) !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; }
[data-testid="stFileUploaderDropzone"] svg { fill: #00F5FF !important; }

/* ── Text area ── */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #E6E9F2 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .9rem !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    transition: border-color .3s !important;
    padding: 10px !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,245,255,.5) !important;
    box-shadow: 0 0 0 3px rgba(0,245,255,.1) !important;
    outline: none !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: #4a5568 !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #7C3AED, #00F5FF) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 48px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: .3px !important;
    transition: 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(124,58,237,.35) !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(124,58,237,.4) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 14px !important;
    padding: 5px 6px !important;
    gap: 4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #B8C1EC !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    padding: 9px 18px !important;
    transition: all .2s !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(90deg, #7C3AED, #00F5FF) !important;
    color: #fff !important;
    box-shadow: 0 3px 14px rgba(124,58,237,.4) !important;
}

/* ── Metric-style stat cards ── */
.kpi-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.kpi {
    flex: 1 1 120px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 22px 20px;
    text-align: center;
    transition: all .3s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.kpi::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 18px 18px 0 0;
}
.kpi.purple::before { background: linear-gradient(90deg,#7C3AED,#00F5FF); }
.kpi.green::before  { background: linear-gradient(90deg,#059669,#10b981); }
.kpi.red::before    { background: linear-gradient(90deg,#be123c,#ef4444); }
.kpi.cyan::before   { background: linear-gradient(90deg,#7C3AED,#00F5FF); }
.kpi.amber::before  { background: linear-gradient(90deg,#d97706,#f59e0b); }
.kpi:hover { transform: translateY(-5px); border-color: rgba(0,245,255,.25); box-shadow: 0 15px 40px rgba(0,245,255,.12); transition: 0.3s ease; }
.kpi-val {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi.purple .kpi-val { color: #00F5FF; }
.kpi.green  .kpi-val { color: #10b981; }
.kpi.red    .kpi-val { color: #f87171; }
.kpi.cyan   .kpi-val { color: #00F5FF; }
.kpi.amber  .kpi-val { color: #fbbf24; }
.kpi-label { font-size: .7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }

/* ── Skill pills ── */
.pills { display: flex; flex-wrap: wrap; gap: 8px; }
.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: .8rem;
    font-weight: 600;
    transition: transform .2s;
}
.pill:hover { transform: scale(1.05); }
.pill-matched  { background:rgba(0,245,255,.12); border:1px solid rgba(0,245,255,.4); color:#00F5FF; }
.pill-missing  { background:rgba(239,68,68,.12); border:1px solid rgba(239,68,68,.4); color:#f87171; }
.pill-critical { background:rgba(239,68,68,.18); border:1.5px solid rgba(239,68,68,.7); color:#fca5a5; font-weight:700; }
.pill-nice     { background:rgba(251,191,36,.1); border:1px solid rgba(251,191,36,.4); color:#fbbf24; }
.pill-extra    { background:rgba(124,58,237,.15); border:1px solid rgba(0,245,255,.3); color:#00F5FF; }
.pill-w { font-family:'JetBrains Mono',monospace; font-size:.7rem; opacity:.55; }

/* ── Recommendation card ── */
.rec {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 4px solid #7C3AED;
    border-radius: 0 16px 16px 0;
    padding: 20px 22px;
    margin-bottom: 14px;
    transition: all .3s ease;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.rec:hover { border-left-color: #00F5FF; background: rgba(0,245,255,.04); box-shadow: 0 15px 40px rgba(0,245,255,.12); }
.rec-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
.rec-name { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.05rem; font-weight:800; color:#00F5FF; }
.rec-meta { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.badge {
    font-size:.68rem; font-weight:700; padding:3px 10px; border-radius:999px; letter-spacing:.5px;
}
.badge-dur  { background:rgba(124,58,237,.15); color:#00F5FF; border:1px solid rgba(0,245,255,.3); }
.badge-diff { background:rgba(16,185,129,.1);  color:#6ee7b7; border:1px solid rgba(16,185,129,.3); }
.badge-diff.adv { background:rgba(239,68,68,.1); color:#fca5a5; border:1px solid rgba(239,68,68,.3); }
.badge-diff.int { background:rgba(251,191,36,.1); color:#fbbf24; border:1px solid rgba(251,191,36,.3); }
.rec-cols { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; }
.rec-col-title { font-size:.68rem; text-transform:uppercase; letter-spacing:2px; color:#7C3AED; font-weight:700; margin-bottom:8px; }
.rec-item { font-size:.82rem; color:#B8C1EC; line-height:1.6; padding-left:4px; }

/* ── Progress ── */
.prog-row { margin-bottom:14px; }
.prog-label { display:flex; justify-content:space-between; margin-bottom:5px; font-size:.82rem; }
.prog-label span:first-child { color:#B8C1EC; }
.prog-label span:last-child  { font-weight:700; color:#00F5FF; font-variant-numeric:tabular-nums; }
.prog-track { background:rgba(255,255,255,.08); border-radius:99px; height:7px; overflow:hidden; }
.prog-fill  {
    height:100%; border-radius:99px;
    background: linear-gradient(90deg, #7C3AED, #00F5FF);
    transition: width 1s ease;
}

/* ── Timeline ── */
.timeline { position:relative; padding-left:28px; }
.timeline::before {
    content:'';
    position:absolute;
    left:8px; top:8px; bottom:8px;
    width:2px;
    background: linear-gradient(180deg, #7C3AED, #00F5FF);
    border-radius:2px;
}
.tl-item { position:relative; margin-bottom:22px; }
.tl-dot {
    position:absolute;
    left:-24px;
    top:4px;
    width:12px; height:12px;
    border-radius:50%;
    background:linear-gradient(135deg,#7C3AED,#00F5FF);
    border:2px solid #0B1020;
    box-shadow: 0 0 10px rgba(0,245,255,.5);
}
.tl-title { font-weight:700; color:#E6E9F2; font-size:.9rem; margin-bottom:4px; }
.tl-desc  { font-size:.8rem; color:#B8C1EC; line-height:1.5; }

/* ── Divider ── */
.divider {
    height:1px;
    background: linear-gradient(to right, transparent, #7C3AED, transparent);
    margin:32px 0;
}

/* ── Label overrides ── */
label, [data-testid="stMarkdownContainer"] p { color:#B8C1EC !important; }
[data-testid="stExpander"] { background:rgba(255,255,255,.04) !important; border:1px solid rgba(255,255,255,.1) !important; border-radius:14px !important; }
[data-testid="stExpander"] summary { color:#B8C1EC !important; font-weight:600 !important; }
[data-testid="stDataFrame"] { border-radius:14px !important; overflow:hidden; }
[data-testid="stAlert"] { border-radius:12px !important; }
a { color:#00F5FF !important; text-decoration:none !important; }
a:hover { color:#7C3AED !important; }

/* ── Number/score highlight ── */
.score-highlight {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:4rem;
    font-weight:800;
    background:linear-gradient(90deg,#7C3AED,#00F5FF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    line-height:1;
}

/* ── Chart containers ── */
.chart-wrap {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;
    padding:16px;
    box-shadow:0 8px 30px rgba(0,0,0,.3);
}
.chart-wrap:hover { box-shadow:0 15px 40px rgba(0,245,255,.1); }

/* ── Footer ── */
.footer {
    text-align:center;
    color:#4B5563;
    font-size:.78rem;
    padding:24px 0 12px;
    letter-spacing:.5px;
    border-top:1px solid rgba(255,255,255,.06);
    margin-top:8px;
}
.footer span { color:#00F5FF; font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  CHART HELPERS
# ═══════════════════════════════════════════════════════════════

CHART_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#B8C1EC', family='Inter'),
    margin=dict(l=16, r=16, t=36, b=16),
)


def gauge(value: float, title: str, max_val: float = 100) -> go.Figure:
    pct = value / max_val
    if   pct >= .80: bar_color = "#00F5FF"
    elif pct >= .65: bar_color = "#7C3AED"
    elif pct >= .50: bar_color = "#f59e0b"
    elif pct >= .35: bar_color = "#f97316"
    else:            bar_color = "#ef4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%" if max_val == 100 else "",
                "font": {"size": 48, "color": bar_color, "family": "Plus Jakarta Sans"}},
        gauge={
            "axis": {"range": [0, max_val], "tickfont": {"color": "#4B5563"}, "tickwidth": 1},
            "bar":  {"color": bar_color, "thickness": .25},
            "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
            "steps": [
                {"range": [0,       max_val*.35], "color": "rgba(239,68,68,.06)"},
                {"range": [max_val*.35, max_val*.55], "color": "rgba(245,158,11,.06)"},
                {"range": [max_val*.55, max_val*.75], "color": "rgba(124,58,237,.08)"},
                {"range": [max_val*.75, max_val],     "color": "rgba(0,245,255,.08)"},
            ],
            "threshold": {"line": {"color": bar_color, "width": 3}, "thickness": .88, "value": value}
        },
        title={"text": title, "font": {"size": 14, "color": "#6B7280", "family": "Inter"}},
        domain={"x": [0,1], "y": [0,1]}
    ))
    fig.update_layout(**CHART_BASE, height=270)
    return fig


def donut(matched: int, missing: int, extra: int) -> go.Figure:
    total = matched + missing + extra or 1
    fig = go.Figure(go.Pie(
        labels=["Matched", "Missing", "Bonus"],
        values=[matched, missing, extra],
        hole=.65,
        marker=dict(
            colors=["#00F5FF", "#ef4444", "#7C3AED"],
            line=dict(color="#0B1020", width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=12, color='#E6E9F2'),
        pull=[.04, .04, 0],
        sort=False,
    ))
    fig.add_annotation(
        text=f"<b>{matched}</b><br><span style='font-size:11px'>matched</span>",
        x=.5, y=.5, showarrow=False,
        font=dict(size=16, color="#E6E9F2", family="Plus Jakarta Sans"),
    )
    fig.update_layout(**CHART_BASE, height=290, showlegend=True,
                      legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=12, color='#B8C1EC')))
    return fig


def category_bar(data_dict: dict, title: str) -> go.Figure:
    if not data_dict:
        return None
    cats   = [k.replace("_"," ") for k in data_dict]
    counts = [len(v) for v in data_dict.values()]
    pairs  = sorted(zip(counts, cats), reverse=True)
    counts, cats = zip(*pairs) if pairs else ([], [])

    fig = go.Figure(go.Bar(
        x=list(counts), y=list(cats), orientation='h',
        marker=dict(color=list(counts), colorscale="Plasma", opacity=.85,
                    line=dict(width=0)),
        text=list(counts), textposition='outside',
        textfont=dict(color='#64748b', size=12),
    ))
    fig.update_layout(
        **CHART_BASE,
        title=dict(text=title, font=dict(size=13, color='#6B7280', family='Inter')),
        height=max(160, len(cats) * 44),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,.05)',
                   tickfont=dict(color='#6B7280'), zeroline=False),
        yaxis=dict(tickfont=dict(color='#B8C1EC', size=11),
                   gridcolor='rgba(0,0,0,0)'),
    )
    return fig


def radar_chart(resume_cats: dict, jd_cats: dict) -> go.Figure:
    all_cats = sorted(set(resume_cats) | set(jd_cats))
    if not all_cats:
        return None

    r_vals = [len(resume_cats.get(c, [])) for c in all_cats]
    j_vals = [len(jd_cats.get(c, []))    for c in all_cats]
    cats_wrapped = [c.replace(" & ", "<br>&<br>") for c in all_cats]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=j_vals + [j_vals[0]], theta=cats_wrapped + [cats_wrapped[0]],
        fill='toself', name='Job Required',
        line=dict(color='#ef4444', width=2),
        fillcolor='rgba(239,68,68,.1)',
    ))
    fig.add_trace(go.Scatterpolar(
        r=r_vals + [r_vals[0]], theta=cats_wrapped + [cats_wrapped[0]],
        fill='toself', name='Your Resume',
        line=dict(color='#00F5FF', width=2),
        fillcolor='rgba(0,245,255,.08)',
    ))
    fig.update_layout(
        **CHART_BASE,
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, gridcolor='rgba(255,255,255,.06)',
                            tickfont=dict(color='#4B5563', size=9)),
            angularaxis=dict(gridcolor='rgba(255,255,255,.06)',
                             tickfont=dict(color='#B8C1EC', size=10)),
        ),
        showlegend=True,
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=12, color='#B8C1EC')),
        height=360,
    )
    return fig


# ═══════════════════════════════════════════════════════════════
#  HELPER HTML BUILDERS
# ═══════════════════════════════════════════════════════════════

def pills_html(skills: list, cls: str, show_weight=False) -> str:
    if not skills:
        return "<p style='color:#4B5563;font-size:.85rem;font-style:italic;'>None detected</p>"
    parts = []
    for s in skills:
        name = s["display"].title() if isinstance(s, dict) else str(s).title()
        wt   = s.get("weight", "") if isinstance(s, dict) else ""
        w_badge = f'<span class="pill-w">w{wt}</span>' if show_weight and wt else ""
        parts.append(f'<span class="pill {cls}">{name}{w_badge}</span>')
    return f'<div class="pills">' + "".join(parts) + '</div>'


def kpi_html(val, label: str, color_cls: str) -> str:
    return f"""
    <div class="kpi {color_cls}">
        <div class="kpi-val">{val}</div>
        <div class="kpi-label">{label}</div>
    </div>"""


def prog_html(label: str, pct: float, color_hex: str = "#7c3aed") -> str:
    pct_clamped = max(0, min(100, pct))
    return f"""
    <div class="prog-row">
        <div class="prog-label">
            <span>{label}</span>
            <span>{pct_clamped:.0f}%</span>
        </div>
        <div class="prog-track">
            <div class="prog-fill" style="width:{pct_clamped}%;"></div>
        </div>
    </div>"""


def diff_badge(diff: str) -> str:
    cls = "adv" if diff == "Advanced" else ("int" if diff == "Intermediate" else "")
    return f'<span class="badge badge-diff {cls}">{diff}</span>'


# ═══════════════════════════════════════════════════════════════
#  HERO HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">⚡ AI-Powered · Weighted Scoring · ATS Intelligence</div>
    <div class="hero-title">SkillScope AI<br>Resume Analyzer</div>
    <div class="hero-sub">
        Upload your resume, paste a job description, and get an instant deep analysis —
        skill gaps, weighted match score, ATS compatibility, and a personalised learning roadmap.
    </div>
    <div class="hero-chips">
        <span class="hero-chip">🧠 200+ Skills Tracked</span>
        <span class="hero-chip">⚖️ Weighted Scoring</span>
        <span class="hero-chip">🤖 ATS Simulation</span>
        <span class="hero-chip">📚 Curated Recommendations</span>
        <span class="hero-chip">🎯 Critical Gap Detection</span>
        <span class="hero-chip">📊 Radar & Visual Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  INPUT SECTION
# ═══════════════════════════════════════════════════════════════
c_left, c_right = st.columns(2, gap="large")

with c_left:
    st.markdown('<div class="sec-label">Step 1</div><div class="sec-title">📄 Upload Your Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader(
        "Drop PDF, DOCX, or TXT",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        key="resume_file",
    )
    if resume_file:
        st.success(f"✅  **{resume_file.name}** — {resume_file.size // 1024} KB")
        # ── Resume Text Preview ──────────────────────────────────
        with st.expander("🔍 Preview Extracted Resume Text", expanded=False):
            try:
                _prev_bytes = resume_file.read()
                resume_file.seek(0)          # reset so later .read() still works
                _prev_file  = io.BytesIO(_prev_bytes)
                _prev_text  = extract_text(_prev_file, resume_file.name)
                if _prev_text.strip():
                    st.markdown(f"""
                    <div style="background:rgba(0,0,0,0.35);border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px;padding:16px;font-size:.78rem;color:#B8C1EC;
                    line-height:1.7;white-space:pre-wrap;max-height:320px;overflow-y:auto;
                    font-family:'JetBrains Mono',monospace;">{_prev_text[:3000]}{' …[truncated]' if len(_prev_text)>3000 else ''}
                    </div>""", unsafe_allow_html=True)
                    st.caption(f"📊 {len(_prev_text.split())} words · {len(_prev_text)} chars extracted")
                else:
                    st.warning("⚠️ Could not extract text — try a text-based PDF or DOCX.")
            except Exception as _e:
                st.warning(f"Preview unavailable: {_e}")

with c_right:
    st.markdown('<div class="sec-label">Step 2</div><div class="sec-title">📋 Paste Job Description</div>', unsafe_allow_html=True)
    jd_raw = st.text_area(
        "JD",
        height=200,
        placeholder="Paste the full job description here …\n\ne.g. We are hiring a Data Scientist with Python, SQL, ML, AWS, Docker …",
        label_visibility="collapsed",
        key="jd_raw",
    )
    if jd_raw:
        st.info(f"📝 JD: **{len(jd_raw.split())} words** · {len(jd_raw)} chars")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Analyze button ──────────────────────────────────────────────
_l, btn_col, _r = st.columns([2, 1, 2])
with btn_col:
    go_btn = st.button("⚡ Analyze My Skill Gap", key="go_btn", use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  ANALYSIS RESULTS
# ═══════════════════════════════════════════════════════════════
if go_btn:
    # ── Validation ──────────────────────────────────────────────
    if not resume_file:
        st.error("❌ Please upload your resume (PDF / DOCX / TXT).")
        st.stop()
    if not jd_raw.strip():
        st.error("❌ Please paste a job description.")
        st.stop()

    # ── Extract resume text ─────────────────────────────────────
    prog = st.progress(0, text="🔍 Extracting resume text …")
    try:
        resume_text = extract_text(resume_file, resume_file.name)
    except Exception as e:
        st.error(f"❌ Could not read resume: {e}")
        st.stop()

    if len(resume_text.strip()) < 50:
        st.error("❌ Resume text too short or unreadable. Try a text-based PDF.")
        st.stop()

    resume_clean = preprocess_text(resume_text)
    jd_clean     = preprocess_text(jd_raw)
    prog.progress(30, text="🤖 Extracting skills …")

    # ── Skill extraction ────────────────────────────────────────
    resume_skills = extract_skills(resume_clean)
    jd_skills     = extract_skills(jd_clean)
    prog.progress(60, text="📊 Running gap analysis …")

    if not jd_skills:
        st.warning("⚠️ No recognisable skills found in the JD. Make sure it contains technical keywords.")
        st.stop()

    # ── Gap analysis ────────────────────────────────────────────
    gap  = compare_skills(resume_skills, jd_skills)
    ats  = get_ats_analysis(gap, resume_text, jd_raw)
    sem  = semantic_similarity(resume_clean, jd_clean)

    resume_by_cat = group_by_category(resume_skills)
    jd_by_cat     = group_by_category(jd_skills)

    prog.progress(100, text="✅ Analysis complete!")
    time.sleep(0.4)
    prog.empty()

    # ── Cache everything in session_state ────────────────────────────
    st.session_state['_analysis'] = {
        'gap': gap, 'ats': ats, 'sem': sem,
        'resume_text': resume_text, 'jd_raw': jd_raw,
        'resume_by_cat': resume_by_cat, 'jd_by_cat': jd_by_cat,
        'resume_name': resume_file.name,
    }

# ─────────────────────────────────────────────────────────────
#  DISPLAY RESULTS (from session_state — survives reruns)
# ─────────────────────────────────────────────────────────────
if '_analysis' in st.session_state:
    _r = st.session_state['_analysis']
    gap           = _r['gap']
    ats           = _r['ats']
    sem           = _r['sem']
    resume_text   = _r['resume_text']
    jd_raw        = _r['jd_raw']
    resume_by_cat = _r['resume_by_cat']
    jd_by_cat     = _r['jd_by_cat']
    _resume_name  = _r['resume_name']

    # ═══════════════════════════════════════════════════════════
    #  KPI STRIP
    # ═══════════════════════════════════════════════════════════
    st.markdown("""
    <div style="text-align:center;margin:8px 0 28px;">
        <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:800;
        background:linear-gradient(135deg,#4338ca,#7c3aed,#a21caf);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
        📈 Analysis Results
        </span>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    for col, val, lbl, cls in [
        (k1, f"{gap['weighted_score']}%", "Weighted Score",  "purple"),
        (k2, f"{gap['total_matched']}",   "Matched Skills",  "green"),
        (k3, f"{gap['total_missing']}",   "Missing Skills",  "red"),
        (k4, f"{ats['ats_score']}%",      "ATS Score",       "cyan"),
        (k5, f"{sem}%",                   "Text Similarity", "amber"),
    ]:
        with col:
            st.markdown(kpi_html(val, lbl, cls), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Score Card + Job Role + Competitive ─────────────────────────────────────
    _grade   = get_letter_grade(gap['weighted_score'], ats['ats_score'], sem)
    _role    = detect_job_role(jd_raw)
    _compete = get_competitive_score(gap['weighted_score'])

    sc_a, sc_b, sc_c = st.columns(3, gap="large")
    with sc_a:
        st.markdown(f"""
        <div class="panel" style="text-align:center;border:1px solid {_grade['color']}44;background:{_grade['bg']};">
            <div style="font-size:3.5rem;font-weight:900;color:{_grade['color']};line-height:1;">{_grade['grade']}</div>
            <div style="font-size:.85rem;font-weight:700;color:{_grade['color']};margin-top:6px;">{_grade['label']}</div>
            <div style="font-size:.75rem;color:#B8C1EC;margin-top:8px;line-height:1.5;">{_grade['advice']}</div>
        </div>
        """, unsafe_allow_html=True)
    with sc_b:
        st.markdown(f"""
        <div class="panel" style="text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:4px;">{_role['icon']}</div>
            <div style="font-size:.7rem;color:#6B7280;text-transform:uppercase;letter-spacing:1.5px;">Detected Role</div>
            <div style="font-size:1.05rem;font-weight:800;color:#E6E9F2;margin:6px 0;">{_role['role']}</div>
            <div style="font-size:.73rem;color:#B8C1EC;">{_role['focus']}</div>
            <div style="margin-top:10px;font-size:.7rem;color:{_role['color']};">{_role['confidence']}% confidence</div>
        </div>
        """, unsafe_allow_html=True)
    with sc_c:
        st.markdown(f"""
        <div class="panel" style="text-align:center;">
            <div style="font-size:.7rem;color:#6B7280;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">Competitive Standing</div>
            <div style="font-size:2.8rem;font-weight:900;color:{_compete['color']};line-height:1;">{_compete['percentile']}%</div>
            <div style="font-size:.78rem;color:#B8C1EC;margin-top:8px;">{_compete['label']}</div>
            <div style="margin-top:12px;background:rgba(255,255,255,0.06);border-radius:99px;height:6px;overflow:hidden;">
                <div style="width:{_compete['percentile']}%;height:100%;background:linear-gradient(90deg,#7C3AED,{_compete['color']});"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    #  TABS
    # ═══════════════════════════════════════════════════════════
    t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs([
        "📊  Scores & ATS",
        "🎯  Skill Gap",
        "📡  Visual Breakdown",
        "🚀  Roadmap",
        "📅  Weekly Plan",
        "📂  Full Breakdown",
        "❓  Interview Prep",
        "✉️  Cover Letter",
    ])

    # ─────────────────────────────────────────────────────────────
    # TAB 1 — Scores & ATS
    # ─────────────────────────────────────────────────────────────
    with t1:
        sc1, sc2, sc3 = st.columns(3, gap="large")

        with sc1:
            st.markdown('<div class="sec-title">⚖️ Weighted Match</div>', unsafe_allow_html=True)
            st.plotly_chart(gauge(gap['weighted_score'], "Importance-Weighted Score"),
                            use_container_width=True, config={"displayModeBar": False})

        with sc2:
            st.markdown('<div class="sec-title">📊 Skill Count Match</div>', unsafe_allow_html=True)
            st.plotly_chart(gauge(gap['simple_score'], "Skills Matched (count)"),
                            use_container_width=True, config={"displayModeBar": False})

        with sc3:
            st.markdown('<div class="sec-title">🤖 ATS Compatibility</div>', unsafe_allow_html=True)
            st.plotly_chart(gauge(ats['ats_score'], "ATS Simulation Score"),
                            use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        a1, a2 = st.columns([1.2, 1], gap="large")
        with a1:
            st.markdown('<div class="sec-title">🤖 ATS Intelligence Report</div>', unsafe_allow_html=True)
            # Grade badge
            grade_col = ats['grade_color']
            st.markdown(f"""
            <div style="display:inline-flex;align-items:center;gap:14px;margin-bottom:20px;">
                <div class="score-highlight">{ats['ats_score']}%</div>
                <div>
                    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.3rem;font-weight:800;color:{grade_col};">
                        {ats['grade']}
                    </div>
                    <div style="font-size:.8rem;color:#94a3b8;">ATS Grade</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Factors
            st.markdown(prog_html("Skill Match Score",      gap['weighted_score']), unsafe_allow_html=True)
            st.markdown(prog_html("Keyword Overlap",        ats['kw_overlap']), unsafe_allow_html=True)
            st.markdown(prog_html("Overall Text Similarity", sem), unsafe_allow_html=True)
            st.markdown(prog_html("Critical Skill Coverage",
                sum(1 for m in gap['matched'] if m['weight'] >= 8) /
                max(sum(1 for m in gap['matched'] if m['weight'] >= 8) +
                    len(gap['critical_missing']), 1) * 100
            ), unsafe_allow_html=True)

        with a2:
            st.markdown('<div class="sec-title">💡 ATS Improvement Tips</div>', unsafe_allow_html=True)
            wc_status = ats['length_status']
            st.markdown(f"""
            <div class="panel">
                <div style="margin-bottom:14px;">
                    <span style="font-size:.75rem;color:#B8C1EC;text-transform:uppercase;letter-spacing:1.5px;">Resume Length</span><br>
                    <span style="font-weight:700;color:#E6E9F2;">{ats['word_count']} words</span>
                    <span style="margin-left:8px;font-size:.78rem;color:{'#00F5FF' if 'Optimal' in wc_status else '#fbbf24'};">  
                        {wc_status}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            for tip in ats['tips']:
                st.markdown(f"""<div style="font-size:.83rem;color:#B8C1EC;margin-bottom:8px;padding-left:4px;">
                    {tip}</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    # TAB 2 — Skill Gap
    # ─────────────────────────────────────────────────────────────
    with t2:
        g1, g2 = st.columns([1, 1.4], gap="large")

        with g1:
            st.markdown('<div class="sec-title">📉 Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(
                donut(gap['total_matched'], gap['total_missing'], gap['total_extra']),
                use_container_width=True, config={"displayModeBar": False}
            )

            # Weight coverage bar
            st.markdown('<div class="sec-title" style="margin-top:8px;">⚖️ Weighted Coverage</div>', unsafe_allow_html=True)
            wt_pct = gap['matched_weight'] / max(gap['total_jd_weight'], 1) * 100
            st.markdown(prog_html(f"Importance weight matched ({gap['matched_weight']}/{gap['total_jd_weight']})", wt_pct),
                        unsafe_allow_html=True)

        with g2:
            st.markdown('<div class="sec-title">✅ Matched Skills</div>', unsafe_allow_html=True)
            st.markdown(pills_html(gap['matched'], "pill-matched", show_weight=True), unsafe_allow_html=True)

            st.markdown('<div class="divider" style="margin:18px 0;"></div>', unsafe_allow_html=True)

            st.markdown('<div class="sec-title">🔴 Critical Missing <small style="font-size:.75rem;color:#475569;">(weight ≥ 8)</small></div>', unsafe_allow_html=True)
            st.markdown(pills_html(gap['critical_missing'], "pill-critical", show_weight=True), unsafe_allow_html=True)

            st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-title">🟡 Nice-to-Have Missing</div>', unsafe_allow_html=True)
            st.markdown(pills_html(gap['nice_to_have'], "pill-nice", show_weight=True), unsafe_allow_html=True)

            st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-title">⭐ Bonus Skills</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:.78rem;color:#334155;margin-bottom:8px;">Extra skills on your resume beyond JD requirements</p>', unsafe_allow_html=True)
            st.markdown(pills_html(gap['extra'][:15], "pill-extra"), unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    # TAB 3 — Visual Breakdown
    # ─────────────────────────────────────────────────────────────
    with t3:
        st.markdown('<div class="sec-title">📡 Skill Category Radar</div>', unsafe_allow_html=True)
        rdr = radar_chart(
            {k: v for k, v in resume_by_cat.items()},
            {k: v for k, v in jd_by_cat.items()},
        )
        if rdr:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(rdr, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        v1, v2 = st.columns(2, gap="large")

        with v1:
            fig_r = category_bar(resume_by_cat, "Resume Skills by Category")
            if fig_r:
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

        with v2:
            fig_j = category_bar(jd_by_cat, "JD Required Skills by Category")
            if fig_j:
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.plotly_chart(fig_j, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

        # Missing skills by weight chart
        if gap['missing']:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-title">🏋️ Missing Skills — Importance Weight</div>', unsafe_allow_html=True)
            miss_df = pd.DataFrame([
                {"Skill": s["display"].title(), "Weight": s["weight"], "Category": s["category"]}
                for s in sorted(gap['missing'], key=lambda x: x['weight'], reverse=True)
            ])
            fig_miss = px.bar(
                miss_df, x="Skill", y="Weight", color="Category",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                labels={"Weight": "Importance (1–10)"},
            )
            fig_miss.update_layout(
                **CHART_BASE, height=320,
                xaxis=dict(tickangle=-35, tickfont=dict(size=11, color='#94a3b8')),
                yaxis=dict(gridcolor='rgba(255,255,255,.05)', tickfont=dict(color='#475569')),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
            )
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_miss, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Word Cloud (Skill Frequency Treemap) ───────────────────
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">☁️ JD Skill Word Cloud</div>', unsafe_allow_html=True)
        if jd_by_cat:
            _wc_labels, _wc_parents, _wc_values, _wc_colors = [], [], [], []
            _palette = ["#7C3AED", "#00F5FF", "#34d399", "#f59e0b", "#f87171",
                        "#a78bfa", "#38bdf8", "#fb923c", "#4ade80", "#e879f9"]
            for _ci, (_cat, _skills) in enumerate(jd_by_cat.items()):
                _wc_labels.append(_cat); _wc_parents.append(""); _wc_values.append(0)
                _wc_colors.append(_palette[_ci % len(_palette)])
                for _s in _skills:
                    _wc_labels.append(_s['display'].title())
                    _wc_parents.append(_cat)
                    _wc_values.append(_s['weight'])
                    _wc_colors.append(_palette[_ci % len(_palette)])
            _wc_fig = go.Figure(go.Treemap(
                labels=_wc_labels, parents=_wc_parents, values=_wc_values,
                marker=dict(colors=_wc_colors, line=dict(width=2, color='#0B1020')),
                textfont=dict(size=14, color='white', family='Plus Jakarta Sans'),
                hovertemplate='<b>%{label}</b><br>Weight: %{value}/10<extra></extra>',
            ))
            _wc_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Plus Jakarta Sans', color='#E6E9F2'),
                margin=dict(t=10, b=10, l=10, r=10), height=300,
            )
            st.plotly_chart(_wc_fig, use_container_width=True, config={"displayModeBar": False})

    # ─────────────────────────────────────────────────────────────
    # TAB 4 — Learning Roadmap
    # ─────────────────────────────────────────────────────────────
    with t4:
        if not gap['missing']:
            st.success("🎉 Outstanding! You have every required skill. Focus on showcasing your projects and applying confidently!")
        else:
            # Priority order: critical first, then nice-to-have
            ordered = sorted(gap['missing'], key=lambda x: x['weight'], reverse=True)
            total = len(ordered)

            st.markdown(f"""
            <div class="panel" style="margin-bottom:24px;">
                <div style="display:flex;align-items:center;gap:16px;">
                    <div class="score-highlight">{total}</div>
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#e2e8f0;">
                            Skills to Learn
                        </div>
                        <div style="font-size:.82rem;color:#475569;">
                            {len(gap['critical_missing'])} critical · {len(gap['nice_to_have'])} nice-to-have
                            &nbsp;·&nbsp; Prioritised by importance weight
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            for i, skill_info in enumerate(ordered):
                rec   = get_recommendation(skill_info["display"])
                is_critical = skill_info["weight"] >= 8
                badge_critical = '<span class="badge badge-diff adv">🔴 Critical</span>' if is_critical else '<span class="badge badge-diff">🟡 Nice-to-have</span>'
                diff_cls = diff_badge(rec.get("difficulty", "Varies"))

                courses_html  = "".join(f'<div class="rec-item">📚 {c}</div>' for c in rec["courses"])
                projects_html = "".join(f'<div class="rec-item">🛠️ {p}</div>' for p in rec["projects"])
                resources_html = "".join(f'<div class="rec-item">🔗 {r}</div>' for r in rec["resources"])

                st.markdown(f"""
                <div class="rec">
                    <div class="rec-head">
                        <div class="rec-name">#{i+1} — {skill_info['display'].title()}</div>
                        <div class="rec-meta">
                            {badge_critical}
                            <span class="badge badge-dur">⏱ {rec['duration']}</span>
                            {diff_cls}
                            <span style="font-family:'JetBrains Mono',monospace;font-size:.7rem;
                            color:#334155;">w{skill_info['weight']}/10</span>
                        </div>
                    </div>
                    <div class="rec-cols">
                        <div>
                            <div class="rec-col-title">📚 Courses</div>
                            {courses_html}
                        </div>
                        <div>
                            <div class="rec-col-title">🛠 Projects</div>
                            {projects_html}
                        </div>
                        <div>
                            <div class="rec-col-title">🔗 Resources</div>
                            {resources_html}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    # TAB 5 — Weekly Study Plan
    # ─────────────────────────────────────────────────────────────
    with t5:
        st.markdown('<div class="sec-title">📅 Your Personalised Weekly Study Plan</div>', unsafe_allow_html=True)
        weekly_plan = build_weekly_plan(gap['missing'], get_recommendation)

        if not weekly_plan:
            st.info("🎉 No missing skills — you're a perfect match!")
        else:
            total_wks = weekly_plan[-1]['week_end']
            st.markdown(f"""
            <div class="panel" style="margin-bottom:20px;padding:18px 22px;">
                <span style="color:#00F5FF;font-weight:700;font-size:1.05rem;">⏱ Total Duration: {total_wks} weeks</span>
                <span style="margin-left:20px;color:#B8C1EC;font-size:.85rem;">{len(weekly_plan)} skills to learn · Prioritised by importance weight</span>
            </div>
            """, unsafe_allow_html=True)

            for p in weekly_plan:
                wk_label = f"Week {p['week_start']}" if p['week_start'] == p['week_end'] else f"Week {p['week_start']} – {p['week_end']}"
                diff_color = {"Beginner": "#00F5FF", "Intermediate": "#a78bfa", "Advanced": "#f87171"}.get(p['difficulty'], "#B8C1EC")
                weight_bar = int(p['weight'] * 10)
                st.markdown(f"""
                <div class="panel" style="margin-bottom:14px;border-left:4px solid {diff_color};">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px;">
                        <div>
                            <span style="font-size:.7rem;color:#6B7280;text-transform:uppercase;letter-spacing:1.5px;">{wk_label}</span>
                            <div style="font-size:1.05rem;font-weight:700;color:#E6E9F2;margin-top:2px;">📘 {p['skill']}</div>
                        </div>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;">
                            <span class="badge" style="background:rgba(255,255,255,0.06);color:{diff_color};border:1px solid {diff_color}33;">⏱ {p['duration']}</span>
                            <span class="badge" style="background:rgba(255,255,255,0.06);color:{diff_color};border:1px solid {diff_color}33;">{p['difficulty']}</span>
                            <span class="badge" style="background:rgba(255,255,255,0.06);color:#94a3b8;">w{p['weight']}/10</span>
                        </div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
                        <div>
                            <div style="font-size:.68rem;color:#7C3AED;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:6px;">📚 Course</div>
                            <div style="font-size:.82rem;color:#B8C1EC;">{p['course']}</div>
                            {f'<div style="font-size:.78rem;color:#64748b;margin-top:4px;">{p["course2"]}</div>' if p['course2'] else ''}
                        </div>
                        <div>
                            <div style="font-size:.68rem;color:#7C3AED;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:6px;">🛠 Project</div>
                            <div style="font-size:.82rem;color:#B8C1EC;">{p['project']}</div>
                        </div>
                        <div>
                            <div style="font-size:.68rem;color:#7C3AED;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:6px;">🔗 Resource</div>
                            <div style="font-size:.82rem;color:#00F5FF;">{p['resource']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    # TAB 7 — Interview Prep
    # ─────────────────────────────────────────────────────────────
    with t7:
        st.markdown('<div class="sec-title">❓ Interview Question Predictor</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="panel" style="margin-bottom:20px;padding:14px 20px;">
            <span style="color:#00F5FF;font-weight:700;">🎯 Role: {_role['icon']} {_role['role']}</span>
            <span style="margin-left:16px;color:#B8C1EC;font-size:.85rem;">Based on matched &amp; missing skills from the JD</span>
        </div>""", unsafe_allow_html=True)

        all_jd_skills = [s['display'] for s in (gap['matched'] + gap['missing'])[:12]]
        if not all_jd_skills:
            st.info("No skills detected in JD.")
        else:
            for _skill in all_jd_skills:
                _qs = get_interview_questions(_skill)
                with st.expander(f"💬 {_skill.title()} — {len(_qs)} Questions", expanded=False):
                    for _qi, _q in enumerate(_qs, 1):
                        st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.04);border-left:3px solid #7C3AED;
                        border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:10px;
                        font-size:.87rem;color:#B8C1EC;line-height:1.6;">
                            <span style="color:#7C3AED;font-weight:700;margin-right:8px;">Q{_qi}.</span>{_q}
                        </div>""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    # TAB 8 — Cover Letter
    # ─────────────────────────────────────────────────────────────
    with t8:
        st.markdown('<div class="sec-title">✉️ AI Cover Letter Generator</div>', unsafe_allow_html=True)
        cl_a, cl_b = st.columns(2, gap="large")
        with cl_a:
            _cand_name = st.text_input("Your Name", placeholder="e.g. Rohan Yadav", key="cand_name")
            _company   = st.text_input("Company Name", placeholder="e.g. Google, TCS, Infosys", key="company_name")
        with cl_b:
            st.markdown(f"""<div class="panel" style="padding:14px;">
                <div style="font-size:.75rem;color:#6B7280;margin-bottom:6px;">Auto-detected role</div>
                <div style="font-weight:700;color:#00F5FF;">{_role['icon']} {_role['role']}</div>
                <div style="font-size:.77rem;color:#B8C1EC;margin-top:6px;">Based on your JD analysis</div>
            </div>""", unsafe_allow_html=True)

        if st.button("⚡ Generate Cover Letter", key="gen_cl", use_container_width=False):
            st.session_state['_cl_text'] = generate_cover_letter(
                candidate_name = _cand_name,
                job_role       = _role['role'],
                matched_skills = gap['matched'],
                missing_skills = gap['missing'],
                company        = _company if _company else "your company",
            )
            st.session_state['_cl_role']    = _role['role']
            st.session_state['_cl_name']    = _cand_name
            st.session_state['_cl_company'] = _company or "your company"

        if '_cl_text' in st.session_state:
            _cl_text    = st.session_state['_cl_text']
            _cl_role    = st.session_state.get('_cl_role', _role['role'])
            _cl_name    = st.session_state.get('_cl_name', '')
            _cl_company = st.session_state.get('_cl_company', 'your company')

            st.markdown("""<div style="font-size:.75rem;color:#6B7280;margin:14px 0 4px;">
                ✅ Generated — edit as needed before sending:</div>""", unsafe_allow_html=True)
            _cl_edited = st.text_area(
                "Cover Letter", value=_cl_text, height=420,
                key="cl_output", label_visibility="collapsed"
            )

            # ── Download options ────────────────────────────────────
            st.markdown("""<div style="font-size:.8rem;color:#B8C1EC;margin:14px 0 8px;font-weight:600;">
                📥 Download As:</div>""", unsafe_allow_html=True)

            _dl_a, _dl_b, _dl_c = st.columns([1, 1, 2])

            with _dl_a:
                st.download_button(
                    label    = "📄 TXT",
                    data     = _cl_edited.encode("utf-8"),
                    file_name= f"CoverLetter_{_cl_role.replace(' ','_')}.txt",
                    mime     = "text/plain",
                    key      = "dl_cl_txt",
                    use_container_width=True,
                )

            # Build a clean PDF-ready HTML version
            _cl_html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>Cover Letter — {_cl_name}</title>
<style>
  @page {{ margin: 2.5cm; }}
  body {{
    font-family: 'Georgia', serif; font-size: 12pt;
    line-height: 1.8; color: #1a1a1a; max-width: 700px;
    margin: 40px auto; padding: 40px;
    border: 1px solid #e5e5e5; border-radius: 8px;
  }}
  .header {{
    text-align: center; border-bottom: 2px solid #7C3AED;
    padding-bottom: 16px; margin-bottom: 28px;
  }}
  .header h1 {{ font-size: 1.6rem; color: #7C3AED; margin: 0; }}
  .header p  {{ color: #666; font-size: 0.9rem; margin: 4px 0 0; }}
  .body {{ white-space: pre-wrap; }}
  .footer {{
    margin-top: 40px; text-align: center;
    font-size: 0.7rem; color: #aaa;
    border-top: 1px solid #eee; padding-top: 14px;
  }}
  @media print {{
    body {{ border: none; }}
    .footer {{ display: block; }}
  }}
</style>
</head><body>
  <div class="header">
    <h1>{_cl_name if _cl_name else 'Cover Letter'}</h1>
    <p>Applying for: <strong>{_cl_role}</strong> at <strong>{_cl_company}</strong></p>
  </div>
  <div class="body">{_cl_edited.replace('<','&lt;').replace('>','&gt;')}</div>
  <div class="footer">Generated by ⚡ SkillScope AI &nbsp;|&nbsp; Open in browser → Ctrl+P → Save as PDF</div>
</body></html>"""

            with _dl_b:
                st.download_button(
                    label    = "🖨️ PDF (HTML)",
                    data     = _cl_html.encode("utf-8"),
                    file_name= f"CoverLetter_{_cl_role.replace(' ','_')}.html",
                    mime     = "text/html",
                    key      = "dl_cl_pdf",
                    use_container_width=True,
                )

            with _dl_c:
                st.markdown("""<div style="font-size:.72rem;color:#6B7280;padding-top:8px;">
                    💡 <b>For PDF:</b> Open the downloaded .html file in Chrome/Edge →
                    press <b>Ctrl+P</b> → choose <b>Save as PDF</b>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("👆 Enter your name and company, then click Generate.")


    # ─────────────────────────────────────────────────────────────
    # TAB 6 — Full Breakdown
    # ─────────────────────────────────────────────────────────────
    with t6:
        # ── Bullet Analyzer ─────────────────────────────────────────
        st.markdown('<div class="sec-title">✏️ Resume Bullet Analyser</div>', unsafe_allow_html=True)
        _bullet_suggests = analyze_bullets(resume_text)
        _type_colors = {"✅": "#34d399", "⚠️": "#fbbf24", "📊": "#f87171", "📝": "#f97316"}
        for _bs in _bullet_suggests:
            _icon = _bs['type'].split()[0]
            _bc   = _type_colors.get(_icon, "#B8C1EC")
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border-left:4px solid {_bc};
            border-radius:0 12px 12px 0;padding:14px 18px;margin-bottom:10px;">
                <div style="display:flex;gap:10px;align-items:flex-start;">
                    <div style="min-width:130px;font-size:.72rem;color:{_bc};font-weight:700;
                    text-transform:uppercase;letter-spacing:1px;margin-top:2px;">{_bs['type']}</div>
                    <div>
                        <div style="font-size:.85rem;color:#E6E9F2;margin-bottom:4px;">{_bs['issue']}</div>
                        <div style="font-size:.8rem;color:#B8C1EC;">{_bs['fix']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        b1, b2 = st.columns(2, gap="large")
        with b1:
            st.markdown('<div class="sec-title">📄 Resume — Detected Skills</div>', unsafe_allow_html=True)
            if resume_by_cat:
                rows = []
                for cat, skills in resume_by_cat.items():
                    for s in skills:
                        rows.append({
                            "Skill": s["display"].title(),
                            "Category": cat,
                            "Weight": s["weight"],
                            "Confidence": f"{s['confidence']*100:.0f}%",
                            "Mentions": s["count"],
                        })
                df = pd.DataFrame(rows).sort_values("Weight", ascending=False)
                st.dataframe(df, use_container_width=True, hide_index=True,
                             column_config={"Weight": st.column_config.NumberColumn(format="%d ⭐")})
            else:
                st.info("No skills detected in resume.")

        with b2:
            st.markdown('<div class="sec-title">📋 JD — Required Skills</div>', unsafe_allow_html=True)
            if jd_by_cat:
                rows_j = []
                for cat, skills in jd_by_cat.items():
                    for s in skills:
                        status = "✅ Matched" if any(
                            m["display"].lower() == s["display"].lower()
                            for m in gap['matched']
                        ) else ("🔴 Critical" if s["weight"] >= 8 else "🟡 Missing")
                        rows_j.append({
                            "Skill": s["display"].title(),
                            "Category": cat,
                            "Weight": s["weight"],
                            "Status": status,
                        })
                df_j = pd.DataFrame(rows_j).sort_values("Weight", ascending=False)
                st.dataframe(df_j, use_container_width=True, hide_index=True,
                             column_config={"Weight": st.column_config.NumberColumn(format="%d ⭐")})
            else:
                st.info("No skills detected in JD.")

    # ── Download HTML Report ─────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title" style="text-align:center;">📥 Download Your Report</div>', unsafe_allow_html=True)

    _plan_for_report = build_weekly_plan(gap['missing'], get_recommendation)
    _html_bytes = generate_html_report(
        resume_name   = resume_file.name,
        gap           = gap,
        ats           = ats,
        sem           = sem,
        plan          = _plan_for_report,
        missing_skills = gap['missing'],
        matched_skills = gap['matched'],
    )
    _dl1, _dl2, _dl3 = st.columns([2, 1, 2])
    with _dl2:
        st.download_button(
            label        = "📄 Download Full Report (HTML)",
            data         = _html_bytes,
            file_name    = f"SkillScope_Report_{resume_file.name.rsplit('.',1)[0]}.html",
            mime         = "text/html",
            use_container_width = True,
            key          = "dl_report",
        )
    st.markdown("""
    <div style="text-align:center;font-size:.75rem;color:#4B5563;margin-top:8px;">
        Open the downloaded .html file in any browser for a beautifully styled full-page report
    </div>
    """, unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        ⚡ SkillScope AI &nbsp;|&nbsp; 
        &nbsp;|&nbsp; <span>Empowering students to close skill gaps and land their dream job</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  LANDING PAGE (no analysis yet)
# ═══════════════════════════════════════════════════════════════
else:
    # How it works
    with st.expander("⚙️  How SkillScope AI Works — 7-Step Pipeline", expanded=False):
        steps = [
            ("Upload", "Resume PDF / DOCX / TXT is uploaded"),
            ("Extract", "Text is extracted from files (pdfplumber / python-docx)"),
            ("Preprocess", "Text normalised: lowercase, symbols handled, aliases expanded"),
            ("Skill Detection", "200+ skills matched using regex (word-boundary, phrase-level)"),
            ("Weighted Scoring", "Each skill carries an importance weight (1–10); score = Σmatched_weights / Σjd_weights"),
            ("ATS Simulation", "Keyword density, length, critical skill coverage combined for ATS score"),
            ("Recommendations", "Curated courses, projects & resources for every missing skill"),
        ]
        st.markdown('<div class="timeline">', unsafe_allow_html=True)
        for title, desc in steps:
            st.markdown(f"""
            <div class="tl-item">
                <div class="tl-dot"></div>
                <div class="tl-title">{title}</div>
                <div class="tl-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Feature cards
    st.markdown('<div class="sec-label">What You Get</div><div class="sec-title">🌟 Features</div>', unsafe_allow_html=True)
    f_cols = st.columns(4, gap="medium")
    feats = [
        ("⚖️", "Weighted Match Score",    "Skills ranked by importance — not just a simple count"),
        ("🔴", "Critical Gap Detection",  "Instantly see which missing skills hurt you most"),
        ("🤖", "ATS Intelligence",        "Simulates how ATS bots score your resume"),
        ("🚀", "Learning Roadmap",        "Courses, projects & resources for every gap"),
        ("📡", "Radar Analytics",         "Visual radar comparing your skills vs JD requirements"),
        ("📊", "Visual Dashboard",        "Interactive charts & category breakdowns"),
        ("🧠", "200+ Skills",             "10 categories: ML, Cloud, Web, DB, Security…"),
        ("💡", "Confidence Scoring",      "Each skill scored by how strongly it appears"),
    ]
    all_fcols = st.columns(4, gap="medium")
    for i, (icon, title, desc) in enumerate(feats):
        with all_fcols[i % 4]:
            st.markdown(f"""
            <div class="panel" style="text-align:center;min-height:150px;margin-bottom:16px;">
                <div style="font-size:2rem;margin-bottom:10px;">{icon}</div>
                <div style="font-weight:700;color:#e2e8f0;margin-bottom:6px;font-size:.92rem;">{title}</div>
                <div style="font-size:.78rem;color:#475569;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        ⚡ SkillScope AI &nbsp;|&nbsp; 
        &nbsp;|&nbsp; <span>Empowering students to close skill gaps and land their dream job</span>
    </div>
    """, unsafe_allow_html=True)
