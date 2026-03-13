"""
Etopaz Platform Analytics v2
Dark / Light mode · Material Icons · Rich AI analysis
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Etopaz Platform Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# SESSION STATE  (must be before theme)
# ─────────────────────────────────────────────
ADMIN_PASS = "etopaz2026"

_defaults = {
    "dark_mode":     True,
    "admin_mode":    False,
    "title_main":    "Etopaz Platform Analytics",
    "title_sub":     "OMT Dövrü  ·  Müştəri Səviyyəsində Dərin Analiz",
    "title_kpi":     "Əsas Göstəricilər",
    "title_trend":   "Aylıq Trend Analizi",
    "title_table":   "Aylıq Tam Cədvəl",
    "title_ret":     "Müştəri Saxlanılması — Retention",
    "title_fb":      "Freebet Analizi",
    "title_ai":      "Claude AI — Etopaz Analitikası",
    "ai_result":     "",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# THEME COLOURS
# ─────────────────────────────────────────────
dark_mode = st.session_state["dark_mode"]

if dark_mode:
    C = {
        "bg":       "#0d0f14",
        "card":     "#13161d",
        "card2":    "#1a1e28",
        "border":   "#2a2f3e",
        "green":    "#10d98a",
        "blue":     "#3d9bff",
        "orange":   "#ff7043",
        "yellow":   "#ffc13d",
        "red":      "#f03e3e",
        "purple":   "#9b72f4",
        "white":    "#f0f2f8",
        "light":    "#c8ccda",
        "muted":    "#7b8299",
        "dim":      "#454c60",
        "sidebar":  "#0f1117",
        "shadow":   "rgba(0,0,0,0.4)",
        "ai_bg":    "rgba(155,114,244,.04)",
        "ai_bdr":   "rgba(155,114,244,.3)",
    }
else:
    C = {
        "bg":       "#f0f4fc",
        "card":     "#ffffff",
        "card2":    "#edf0f8",
        "border":   "#dde1ed",
        "green":    "#0cb877",
        "blue":     "#2563eb",
        "orange":   "#e05a38",
        "yellow":   "#c4890a",
        "red":      "#dc2626",
        "purple":   "#7c3aed",
        "white":    "#111827",
        "light":    "#374151",
        "muted":    "#6b7280",
        "dim":      "#9ca3af",
        "sidebar":  "#f8faff",
        "shadow":   "rgba(0,0,0,0.08)",
        "ai_bg":    "rgba(124,58,237,.04)",
        "ai_bdr":   "rgba(124,58,237,.25)",
    }

PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color=C["muted"], size=12),
    xaxis=dict(gridcolor=C["border"], tickfont=dict(color=C["muted"]),
               linecolor=C["border"], zeroline=False),
    yaxis=dict(gridcolor=C["border"], tickfont=dict(color=C["muted"]),
               linecolor=C["border"], zeroline=False),
    margin=dict(l=8, r=8, t=36, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["muted"])),
    hoverlabel=dict(bgcolor=C["card2"], bordercolor=C["border"],
                    font=dict(color=C["white"], family="Inter, sans-serif")),
    height=260,
)

# ─────────────────────────────────────────────
# CSS  +  Material Icons
# ─────────────────────────────────────────────
st.markdown("""
<link rel="stylesheet"
  href="https://fonts.googleapis.com/icon?family=Material+Icons+Round">
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap');

html, body, .stApp {{
    background-color: {C['bg']} !important;
    font-family: 'Inter', system-ui, sans-serif;
    color: {C['white']};
    transition: background-color .3s ease, color .3s ease;
}}
section[data-testid="stSidebar"] {{
    background-color: {C['sidebar']} !important;
    border-right: 1px solid {C['border']};
}}
section[data-testid="stSidebar"] * {{ color: {C['light']} !important; }}
section[data-testid="stSidebar"] .stToggle label {{
    color: {C['muted']} !important; font-size: 13px !important;
}}
.block-container {{ padding: 2rem 2.5rem 4rem !important; max-width: 100% !important; }}
h1,h2,h3,h4 {{ font-family: 'Outfit', sans-serif !important; color: {C['white']} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
hr {{ border-color: {C['border']} !important; }}
div[data-testid="stTextInput"] input {{
    background: {C['card2']} !important; border: 1px solid {C['border']} !important;
    color: {C['white']} !important; border-radius: 8px;
}}
div[data-testid="stTextInput"] label {{ color: {C['muted']} !important; font-size: 11px !important; }}

/* ── KPI Cards ── */
.kpi-card {{
    background: {C['card']}; border: 1px solid {C['border']}; border-radius: 14px;
    padding: 20px 18px 18px; position: relative; overflow: hidden; height: 100%;
    box-shadow: 0 4px 20px {C['shadow']};
    transition: transform .18s ease, box-shadow .18s ease;
}}
.kpi-card:hover {{ transform: translateY(-2px); box-shadow: 0 8px 28px {C['shadow']}; }}
.kpi-card::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 14px 14px 0 0;
}}
.kpi-card.green::before  {{ background: {C['green']}; }}
.kpi-card.blue::before   {{ background: {C['blue']}; }}
.kpi-card.orange::before {{ background: {C['orange']}; }}
.kpi-card.yellow::before {{ background: {C['yellow']}; }}
.kpi-card.red::before    {{ background: {C['red']}; }}

.kpi-icon {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 10px; margin-bottom: 10px;
    font-size: 18px !important;
}}
.kpi-icon.green  {{ background: rgba(16,217,138,.12); color: {C['green']} !important; }}
.kpi-icon.blue   {{ background: rgba(61,155,255,.12); color: {C['blue']} !important; }}
.kpi-icon.orange {{ background: rgba(255,112,67,.12); color: {C['orange']} !important; }}
.kpi-icon.yellow {{ background: rgba(255,193,61,.12); color: {C['yellow']} !important; }}
.kpi-icon.red    {{ background: rgba(240,62,62,.12);  color: {C['red']} !important; }}

.kpi-label {{ font-size: 11px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: {C['muted']}; margin-bottom: 7px; }}
.kpi-val {{ font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; letter-spacing: -.02em; line-height: 1; margin-bottom: 6px; }}
.kpi-val.green  {{ color: {C['green']}; }}
.kpi-val.blue   {{ color: {C['blue']}; }}
.kpi-val.orange {{ color: {C['orange']}; }}
.kpi-val.yellow {{ color: {C['yellow']}; }}
.kpi-val.red    {{ color: {C['red']}; }}
.kpi-sub {{ font-size: 12px; color: {C['muted']}; margin-bottom: 7px; line-height: 1.4; }}
.badge {{
    display: inline-flex; align-items: center; gap: 3px;
    font-size: 11.5px; font-weight: 600; padding: 3px 10px;
    border-radius: 20px;
}}
.badge.up   {{ background: rgba(16,217,138,.12); color: {C['green']}; }}
.badge.down {{ background: rgba(240,62,62,.12);  color: {C['red']}; }}
.badge.warn {{ background: rgba(255,193,61,.12); color: {C['yellow']}; }}

/* ── Section Headers ── */
.sec-head {{
    display: flex; align-items: center; gap: 12px; margin: 44px 0 18px;
}}
.sec-head .sec-icon {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 9px;
    font-size: 17px !important; flex-shrink: 0;
}}
.sec-head span.sec-title {{
    font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase; color: {C['muted']};
    white-space: nowrap;
}}
.sec-line {{ flex: 1; height: 1px; background: {C['border']}; }}

.c-title {{ font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 700; color: {C['white']}; margin-bottom: 3px; }}

/* ── Data Table ── */
.styled-table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
.styled-table th {{
    background: {C['card2']}; font-size: 10.5px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase; color: {C['muted']};
    padding: 11px 14px; text-align: right; white-space: nowrap;
    border-bottom: 1px solid {C['border']};
}}
.styled-table th:first-child {{ text-align: left; }}
.styled-table td {{ padding: 11px 14px; text-align: right; color: {C['light']}; border-top: 1px solid {C['border']}; white-space: nowrap; }}
.styled-table td:first-child {{ text-align: left; font-weight: 600; color: {C['white']}; }}
.styled-table tr:hover td {{ background: {C['card2']}; }}
.vg {{ color: {C['green']} !important; font-weight: 600; }}
.vy {{ color: {C['yellow']} !important; font-weight: 600; }}
.vr {{ color: {C['red']} !important;    font-weight: 600; }}

/* ── Retention Cards ── */
.ret-card {{
    background: {C['card']}; border: 1px solid {C['border']}; border-radius: 12px;
    padding: 16px 12px; text-align: center; height: 100%;
    box-shadow: 0 2px 12px {C['shadow']};
}}
.ret-per  {{ font-size: 10px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: {C['muted']}; margin-bottom: 9px; }}
.ret-pct  {{ font-family: 'Outfit', sans-serif; font-size: 24px; font-weight: 800; line-height: 1; margin-bottom: 7px; }}
.ret-new  {{ font-size: 11.5px; color: {C['green']}; font-weight: 500; }}
.ret-churn {{ font-size: 11.5px; color: {C['orange']}; font-weight: 500; margin-top: 2px; }}

/* ── AI Analysis Box ── */
.ai-outer {{
    background: {C['ai_bg']};
    border: 1px solid {C['ai_bdr']};
    border-radius: 16px;
    overflow: hidden;
    margin-top: 14px;
    box-shadow: 0 4px 24px {C['shadow']};
}}
.ai-header {{
    display: flex; align-items: center; gap: 12px;
    padding: 18px 24px 16px;
    border-bottom: 1px solid {C['ai_bdr']};
    background: linear-gradient(135deg, rgba(155,114,244,.08) 0%, rgba(61,155,255,.05) 100%);
}}
.ai-header .mat-icon {{
    font-size: 22px !important; color: {C['purple']};
}}
.ai-header-text {{
    font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 700; color: {C['purple']};
}}
.ai-header-sub {{
    font-size: 11.5px; color: {C['muted']}; margin-top: 1px;
}}
.ai-body {{
    padding: 20px 24px 24px;
}}
.ai-section {{
    border-radius: 10px; padding: 16px 18px;
    margin-bottom: 12px; border: 1px solid transparent;
}}
.ai-section-title {{
    font-family: 'Outfit', sans-serif; font-size: 14px; font-weight: 700;
    display: flex; align-items: center; gap: 8px; margin-bottom: 10px;
}}
.ai-section-title .mat-icon {{ font-size: 18px !important; }}
.ai-section-body {{
    font-size: 13.5px; line-height: 1.85; color: {C['light']};
}}
.ai-section-body p {{ margin: 0 0 6px; }}
.ai-section-body ul {{ margin: 6px 0 6px 16px; padding: 0; }}
.ai-section-body li {{ margin-bottom: 5px; }}
.ai-section-body strong {{ color: {C['white']}; font-weight: 600; }}
.ai-intro {{
    font-size: 13px; color: {C['muted']}; line-height: 1.7;
    padding: 0 0 14px; border-bottom: 1px solid {C['border']}; margin-bottom: 16px;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HARDCODED DATA  (İyun 2025 – Fevral 2026)
# ─────────────────────────────────────────────
RAW_KPI = {
    "2025-06": {"label":"İyun 2025",     "turnover":6.041,  "ggr":1.373, "payout_ratio":77.28, "deposits":2.744,  "withdrawals":1.44,  "tickets":324681,  "users":10315, "risk_users":1097, "pareto_top1_pct":40.2, "pareto_top1_count":103},
    "2025-07": {"label":"İyul 2025",     "turnover":18.107, "ggr":4.295, "payout_ratio":76.28, "deposits":8.59,   "withdrawals":4.286, "tickets":970138,  "users":14412, "risk_users":1297, "pareto_top1_pct":43.1, "pareto_top1_count":144},
    "2025-08": {"label":"Avqust 2025",   "turnover":24.231, "ggr":6.098, "payout_ratio":74.83, "deposits":12.035, "withdrawals":5.972, "tickets":1384050, "users":17890, "risk_users":1308, "pareto_top1_pct":41.3, "pareto_top1_count":178},
    "2025-09": {"label":"Sentyabr 2025", "turnover":26.783, "ggr":5.721, "payout_ratio":78.64, "deposits":13.225, "withdrawals":7.347, "tickets":1498410, "users":20802, "risk_users":2430, "pareto_top1_pct":45.6, "pareto_top1_count":208},
    "2025-10": {"label":"Oktyabr 2025",  "turnover":28.156, "ggr":6.791, "payout_ratio":75.88, "deposits":14.187, "withdrawals":7.39,  "tickets":1765156, "users":24247, "risk_users":2234, "pareto_top1_pct":42.1, "pareto_top1_count":242},
    "2025-11": {"label":"Noyabr 2025",   "turnover":29.572, "ggr":7.195, "payout_ratio":75.67, "deposits":15.006, "withdrawals":7.652, "tickets":1872100, "users":25047, "risk_users":1966, "pareto_top1_pct":43.2, "pareto_top1_count":250},
    "2025-12": {"label":"Dekabr 2025",   "turnover":31.078, "ggr":7.286, "payout_ratio":76.55, "deposits":15.649, "withdrawals":8.439, "tickets":1955316, "users":25173, "risk_users":2397, "pareto_top1_pct":42.8, "pareto_top1_count":251},
    "2026-01": {"label":"Yanvar 2026",   "turnover":34.715, "ggr":7.993, "payout_ratio":76.97, "deposits":17.724, "withdrawals":9.435, "tickets":2055102, "users":27056, "risk_users":2025, "pareto_top1_pct":50.6, "pareto_top1_count":270},
    "2026-02": {"label":"Fevral 2026",   "turnover":33.437, "ggr":6.665, "payout_ratio":80.07, "deposits":16.421, "withdrawals":9.672, "tickets":2188421, "users":28670, "risk_users":3339, "pareto_top1_pct":42.2, "pareto_top1_count":286},
}
RAW_RET = {
    "2025-07": {"rate":89.1,"new":5225, "churned":1128,"retained":9187},
    "2025-08": {"rate":86.0,"new":5502, "churned":2024,"retained":12388},
    "2025-09": {"rate":84.3,"new":5718, "churned":2806,"retained":15084},
    "2025-10": {"rate":85.9,"new":6373, "churned":2928,"retained":17874},
    "2025-11": {"rate":80.6,"new":5507, "churned":4707,"retained":19540},
    "2025-12": {"rate":80.0,"new":5142, "churned":5016,"retained":20031},
    "2026-01": {"rate":81.9,"new":6440, "churned":4557,"retained":20616},
    "2026-02": {"rate":81.0,"new":6768, "churned":5154,"retained":21902},
}
RAW_FB = {
    "2025-06": {"label":"İyun 2025",     "given":0.12,  "used":0.084, "fb_payout":0.033, "payout_ratio":38.71},
    "2025-07": {"label":"İyul 2025",     "given":0.393, "used":0.359, "fb_payout":0.152, "payout_ratio":42.15},
    "2025-08": {"label":"Avqust 2025",   "given":0.591, "used":0.557, "fb_payout":0.203, "payout_ratio":36.51},
    "2025-09": {"label":"Sentyabr 2025", "given":0.667, "used":0.661, "fb_payout":0.299, "payout_ratio":45.23},
    "2025-10": {"label":"Oktyabr 2025",  "given":0.79,  "used":0.678, "fb_payout":0.301, "payout_ratio":44.49},
    "2025-11": {"label":"Noyabr 2025",   "given":0.831, "used":0.774, "fb_payout":0.269, "payout_ratio":34.82},
    "2025-12": {"label":"Dekabr 2025",   "given":0.91,  "used":0.854, "fb_payout":0.37,  "payout_ratio":43.25},
    "2026-01": {"label":"Yanvar 2026",   "given":1.118, "used":1.089, "fb_payout":0.493, "payout_ratio":45.31},
    "2026-02": {"label":"Fevral 2026",   "given":0.836, "used":0.805, "fb_payout":0.393, "payout_ratio":48.76},
}

ALL_PERIODS = sorted(RAW_KPI.keys())
LABELS = {p: RAW_KPI[p]["label"] for p in ALL_PERIODS}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:14px 0 6px">
        <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:800;
                    background:linear-gradient(120deg,{C['green']},{C['blue']});
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
            Etopaz
        </div>
        <div style="font-size:11px;color:{C['muted']};margin-top:2px;
                    text-transform:uppercase;letter-spacing:.07em">
            Platform Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Night / Light Mode Toggle ──
    new_dm = st.toggle(
        "🌙  Gecə rejimi" if dark_mode else "☀️  Gündüz rejimi",
        value=dark_mode,
        key="_theme_toggle",
    )
    if new_dm != dark_mode:
        st.session_state["dark_mode"] = new_dm
        st.rerun()

    st.divider()

    st.markdown(f'<div style="font-size:12px;font-weight:600;color:{C["muted"]};letter-spacing:.05em;text-transform:uppercase;margin-bottom:6px">📅 Tarix Aralığı</div>', unsafe_allow_html=True)
    labels_all = [LABELS[p] for p in ALL_PERIODS]
    start_i = st.selectbox("Başlanğıc", range(len(ALL_PERIODS)),
                           format_func=lambda i: labels_all[i], key="s_start")
    end_i   = st.selectbox("Son ay",    range(len(ALL_PERIODS)),
                           format_func=lambda i: labels_all[i],
                           index=len(ALL_PERIODS)-1, key="s_end")
    if start_i > end_i:
        st.error("Başlanğıc son aydan böyük ola bilməz!")
        sel = ALL_PERIODS[:]
    else:
        sel = ALL_PERIODS[start_i:end_i+1]

    st.divider()
    st.markdown(f'<div style="font-size:12px;font-weight:600;color:{C["muted"]};letter-spacing:.05em;text-transform:uppercase;margin-bottom:6px">⚙️ Admin Modu</div>', unsafe_allow_html=True)
    if not st.session_state.admin_mode:
        pw = st.text_input("Şifrə", type="password", placeholder="••••••••", key="pw_input")
        if pw == ADMIN_PASS:
            st.session_state.admin_mode = True
            st.rerun()
        elif pw:
            st.error("Şifrə yanlışdır")
    else:
        st.success("✅ Admin modu aktiv")
        if st.button("Çıxış"):
            st.session_state.admin_mode = False
            st.rerun()

# ─────────────────────────────────────────────
# ADMIN TITLE EDITOR
# ─────────────────────────────────────────────
if st.session_state.admin_mode:
    with st.expander("✏️ Başlıqları Redaktə Et", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.title_main  = st.text_input("Əsas başlıq",       st.session_state.title_main,  key="e1")
            st.session_state.title_sub   = st.text_input("Alt başlıq",         st.session_state.title_sub,   key="e2")
            st.session_state.title_kpi   = st.text_input("KPI bölməsi",        st.session_state.title_kpi,   key="e3")
            st.session_state.title_trend = st.text_input("Trend bölməsi",      st.session_state.title_trend, key="e4")
        with c2:
            st.session_state.title_table = st.text_input("Cədvəl bölməsi",     st.session_state.title_table, key="e5")
            st.session_state.title_ret   = st.text_input("Retention bölməsi",  st.session_state.title_ret,   key="e6")
            st.session_state.title_fb    = st.text_input("Freebet bölməsi",    st.session_state.title_fb,    key="e7")
            st.session_state.title_ai    = st.text_input("AI bölmə başlığı",   st.session_state.title_ai,    key="e8")

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def section(title, icon="analytics"):
    bg_map = {
        "analytics": C["blue"], "show_chart": C["green"],
        "table_chart": C["muted"], "group": C["orange"],
        "card_giftcard": C["purple"], "smart_toy": C["purple"],
        "trending_up": C["yellow"],
    }
    icon_color = bg_map.get(icon, C["blue"])
    icon_bg = icon_color + "18"
    st.markdown(f"""
    <div class="sec-head">
        <span class="material-icons-round sec-icon"
              style="background:{icon_bg};color:{icon_color}">{icon}</span>
        <span class="sec-title">{title}</span>
        <div class="sec-line"></div>
    </div>""", unsafe_allow_html=True)

def kpi_card(label, value, sub, badge_txt, badge_cls, color, icon="trending_up"):
    st.markdown(f"""
    <div class="kpi-card {color}">
        <span class="material-icons-round kpi-icon {color}">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-val {color}">{value}</div>
        <div class="kpi-sub">{sub}</div>
        <span class="badge {badge_cls}">{badge_txt}</span>
    </div>""", unsafe_allow_html=True)

def bar_chart(x, y, colors=None, height=260):
    if colors is None: colors = [C["blue"]]*len(y)
    fig = go.Figure(go.Bar(x=x, y=y, marker_color=colors, marker_line_width=0,
                           hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>"))
    fig.update_layout(**{**PL, "height": height})
    return fig

def bar_line_chart(x, bar_y, line_y, bar_name, line_name,
                   bar_color, line_color, y2_range=None, height=260):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=x, y=bar_y, name=bar_name,
                         marker_color=bar_color, marker_line_width=0,
                         hovertemplate=f"<b>%{{x}}</b><br>{bar_name}: ₼%{{y:.2f}}M<extra></extra>"),
                  secondary_y=False)
    fig.add_trace(go.Scatter(
        x=x, y=line_y, name=line_name,
        line=dict(color=line_color, width=2.5), mode="lines+markers",
        marker=dict(size=6, color=[C["red"] if v > 78 else line_color for v in line_y]),
        hovertemplate=f"<b>%{{x}}</b><br>{line_name}: %{{y:.1f}}%<extra></extra>"),
        secondary_y=True)
    layout = {**PL, "height": height, "showlegend": True,
              "legend": dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)")}
    if y2_range:
        layout["yaxis2"] = dict(range=y2_range, gridcolor=C["border"],
                                tickfont=dict(color=C["muted"]),
                                ticksuffix="%", zeroline=False, showgrid=False)
    fig.update_layout(**layout)
    return fig

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
kpi_d  = {p: RAW_KPI[p] for p in sel}
fb_d   = {p: RAW_FB[p]  for p in sel if p in RAW_FB}
ret_d  = {p: RAW_RET[p] for p in sel if p in RAW_RET}

labs      = [kpi_d[p]["label"]        for p in sel]
to_list   = [kpi_d[p]["turnover"]     for p in sel]
ggr_list  = [kpi_d[p]["ggr"]          for p in sel]
pr_list   = [kpi_d[p]["payout_ratio"] for p in sel]
cust_list = [kpi_d[p]["users"]        for p in sel]
dep_list  = [kpi_d[p]["deposits"]     for p in sel]
wd_list   = [kpi_d[p]["withdrawals"]  for p in sel]
tk_list   = [kpi_d[p]["tickets"]      for p in sel]

total_to  = sum(to_list)
total_ggr = sum(ggr_list)
total_dep = sum(dep_list)
total_wd  = sum(wd_list)
avg_pr    = sum(pr_list)/len(pr_list)
last_pr   = pr_list[-1]
dep_wd_r  = total_dep/total_wd if total_wd else 0
to_mom    = round((to_list[-1]/to_list[-2]-1)*100, 1) if len(to_list)>1 else 0
ggr_mom   = round((ggr_list[-1]/ggr_list[-2]-1)*100, 1) if len(ggr_list)>1 else 0
cust_mom  = round((cust_list[-1]/cust_list[-2]-1)*100, 1) if len(cust_list)>1 else 0
ret_periods = [p for p in sel if p in ret_d]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:24px;border-bottom:1px solid {C['border']};
            display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:12px">
    <div>
        <div style="font-family:'Outfit',sans-serif;font-size:30px;font-weight:900;
                    background:linear-gradient(120deg,{C['green']} 0%,{C['blue']} 60%);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1">
            {st.session_state.title_main}
        </div>
        <div style="font-size:13px;color:{C['muted']};margin-top:5px">
            {st.session_state.title_sub}
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:{C['muted']}">
        <span class="material-icons-round" style="font-size:16px;color:{C['green']}">fiber_manual_record</span>
        {labs[0]} — {labs[-1]}
        &nbsp;·&nbsp; {len(sel)} ay
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
section(st.session_state.title_kpi, "analytics")
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    kpi_card("Ümumi Dövriyyə", f"₼{total_to:.1f}M",
             f"{len(sel)} ay üzrə",
             f"{'▲' if to_mom>=0 else '▼'} {abs(to_mom):.1f}% son ay",
             "up" if to_mom>=0 else "down", "green", "payments")
with k2:
    kpi_card("Ümumi GGR", f"₼{total_ggr:.1f}M",
             f"Margin: {total_ggr/total_to*100:.1f}%",
             f"{'▲' if ggr_mom>=0 else '▼'} {abs(ggr_mom):.1f}% son ay",
             "up" if ggr_mom>=0 else "down", "blue", "account_balance")
with k3:
    kpi_card("Son Ay Payout", f"{last_pr:.1f}%",
             f"Ortalama: {avg_pr:.1f}% | Benchmark: 77%",
             "⚠ Yüksək" if last_pr>78 else "✓ Normal",
             "warn" if last_pr>78 else "up",
             "red" if last_pr>78 else "yellow", "percent")
with k4:
    kpi_card("Son Ay Müştəri", f"{cust_list[-1]:,}",
             f"İlk ay: {cust_list[0]:,}",
             f"{'▲' if cust_mom>=0 else '▼'} {abs(cust_mom):.1f}% son ay",
             "up" if cust_mom>=0 else "down", "orange", "group")
with k5:
    kpi_card("Depozit / Çıxarış", f"₼{total_dep:.1f}M",
             f"Çıxarış: ₼{total_wd:.1f}M",
             f"Nisbət: {dep_wd_r:.2f}×",
             "up", "green", "account_balance_wallet")

# ─────────────────────────────────────────────
# TREND CHARTS
# ─────────────────────────────────────────────
section(st.session_state.title_trend, "show_chart")
tc1, tc2 = st.columns(2)
with tc1:
    st.markdown('<div class="c-title">Aylıq Dövriyyə (₼M)</div>', unsafe_allow_html=True)
    to_colors = [C["green"] if v==max(to_list) else C["blue"] for v in to_list]
    st.plotly_chart(bar_chart(labs, to_list, to_colors), use_container_width=True, config={"displayModeBar":False})
with tc2:
    st.markdown('<div class="c-title">GGR (₼M) və Payout Ratio (%)</div>', unsafe_allow_html=True)
    st.plotly_chart(
        bar_line_chart(labs, ggr_list, pr_list, "GGR (₼M)", "Payout %",
                       C["blue"], C["yellow"], y2_range=[60, 90]),
        use_container_width=True, config={"displayModeBar":False})

tc3, tc4 = st.columns(2)
with tc3:
    st.markdown('<div class="c-title">Aktiv Müştəri Sayı</div>', unsafe_allow_html=True)
    cust_colors = [C["orange"] if v==max(cust_list) else C["purple"] for v in cust_list]
    st.plotly_chart(bar_chart(labs, cust_list, cust_colors), use_container_width=True, config={"displayModeBar":False})
with tc4:
    st.markdown('<div class="c-title">Depozit vs Çıxarış (₼M)</div>', unsafe_allow_html=True)
    fig_dw = go.Figure()
    fig_dw.add_trace(go.Bar(x=labs, y=dep_list, name="Depozit", marker_color=C["green"],  marker_line_width=0))
    fig_dw.add_trace(go.Bar(x=labs, y=wd_list,  name="Çıxarış", marker_color=C["orange"], marker_line_width=0))
    fig_dw.update_layout(**{**PL, "height":260, "showlegend":True, "barmode":"group",
                             "legend":dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)")})
    st.plotly_chart(fig_dw, use_container_width=True, config={"displayModeBar":False})

# ─────────────────────────────────────────────
# MONTHLY TABLE
# ─────────────────────────────────────────────
section(st.session_state.title_table, "table_chart")

def pcls(v):
    return "vg" if v<75 else ("vy" if v<79 else "vr")

rows = ""
for p in sel:
    d = kpi_d[p]
    rows += f"""<tr>
        <td>{d['label']}</td>
        <td>₼{d['turnover']:.3f}M</td>
        <td>₼{d['ggr']:.3f}M</td>
        <td class="{pcls(d['payout_ratio'])}">{d['payout_ratio']:.2f}%</td>
        <td>{d['users']:,}</td>
        <td>₼{d['deposits']:.3f}M</td>
        <td>₼{d['withdrawals']:.3f}M</td>
        <td>{d['tickets']:,}</td>
        <td class="vr">{d['risk_users']:,}</td>
    </tr>"""

st.markdown(f"""
<div style="background:{C['card']};border:1px solid {C['border']};border-radius:12px;
            overflow:hidden;overflow-x:auto;box-shadow:0 2px 16px {C['shadow']}">
<table class="styled-table"><thead><tr>
    <th>Ay</th><th>Dövriyyə</th><th>GGR</th><th>Payout %</th>
    <th>Müştəri</th><th>Depozit</th><th>Çıxarış</th><th>Ticket</th><th>Riskli</th>
</tr></thead><tbody>{rows}</tbody></table>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RETENTION
# ─────────────────────────────────────────────
if ret_periods:
    section(st.session_state.title_ret, "group")
    ret_cols = st.columns(min(len(ret_periods), 8))
    for col, p in zip(ret_cols, ret_periods):
        r = ret_d[p]
        color = C["green"] if r["rate"]>=85 else (C["yellow"] if r["rate"]>=80 else C["red"])
        with col:
            st.markdown(f"""
            <div class="ret-card">
                <div class="ret-per">{kpi_d[p]['label']}</div>
                <div class="ret-pct" style="color:{color}">{r['rate']}%</div>
                <div class="ret-new">+{r['new']:,} yeni</div>
                <div class="ret-churn">-{r['churned']:,} çıxdı</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ret_labs  = [kpi_d[p]["label"] for p in ret_periods]
    ret_rates = [ret_d[p]["rate"]  for p in ret_periods]
    ret_clrs  = [C["green"] if v>=85 else (C["yellow"] if v>=80 else C["red"]) for v in ret_rates]
    st.plotly_chart(bar_chart(ret_labs, ret_rates, ret_clrs, height=220),
                    use_container_width=True, config={"displayModeBar":False})

# ─────────────────────────────────────────────
# FREEBET
# ─────────────────────────────────────────────
if fb_d:
    section(st.session_state.title_fb, "card_giftcard")
    fb_labs  = [fb_d[p]["label"]        for p in sel if p in fb_d]
    fb_given = [fb_d[p]["given"]        for p in sel if p in fb_d]
    fb_used  = [fb_d[p]["used"]         for p in sel if p in fb_d]
    fb_pr    = [fb_d[p]["payout_ratio"] for p in sel if p in fb_d]

    fb1, fb2 = st.columns(2)
    with fb1:
        st.markdown('<div class="c-title">Freebet Verilən vs İstifadə (₼M)</div>', unsafe_allow_html=True)
        fig_fb = go.Figure()
        fig_fb.add_trace(go.Bar(x=fb_labs, y=fb_given, name="Verilən",   marker_color=C["purple"], marker_line_width=0))
        fig_fb.add_trace(go.Bar(x=fb_labs, y=fb_used,  name="İstifadə", marker_color=C["blue"],   marker_line_width=0))
        fig_fb.update_layout(**{**PL, "height":250, "showlegend":True, "barmode":"group",
                                 "legend":dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)")})
        st.plotly_chart(fig_fb, use_container_width=True, config={"displayModeBar":False})
    with fb2:
        st.markdown('<div class="c-title">Freebet Payout Ratio (%)</div>', unsafe_allow_html=True)
        fb_clrs = [C["red"] if v>47 else C["green"] for v in fb_pr]
        st.plotly_chart(bar_chart(fb_labs, fb_pr, fb_clrs, height=250),
                        use_container_width=True, config={"displayModeBar":False})

# ─────────────────────────────────────────────
# AI ANALYSIS HELPERS
# ─────────────────────────────────────────────
def _md_to_html(text, white_color, light_color, muted_color):
    """Minimal markdown → HTML (bold, bullets, paragraphs)."""
    lines = text.strip().split("\n")
    out = []
    in_ul = False
    for raw in lines:
        ln = raw.strip()
        # inline bold
        ln = re.sub(r"\*\*(.+?)\*\*",
                    rf'<strong style="color:{white_color};font-weight:600">\1</strong>', ln)
        if not ln:
            if in_ul:
                out.append("</ul>"); in_ul = False
            continue
        if ln.startswith(("- ", "• ", "* ")):
            if not in_ul:
                out.append(f'<ul style="margin:8px 0 8px 18px;padding:0">'); in_ul = True
            out.append(f'<li style="margin-bottom:5px;line-height:1.75;color:{light_color}">{ln[2:]}</li>')
        else:
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append(f'<p style="margin:5px 0;line-height:1.8;color:{light_color}">{ln}</p>')
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def render_ai_response(text):
    """Parse 4-section Claude response and render as rich cards."""
    SECTIONS = [
        ("1", C["blue"],   "analytics",     ),
        ("2", C["red"],    "warning_amber",  ),
        ("3", C["green"],  "lightbulb",      ),
        ("4", C["yellow"], "trending_up",    ),
    ]

    # Split by numbered section starts  e.g.  "1. 📊 ..."
    parts = re.split(r"(?m)^(?=\d+\.\s)", text.strip())

    # Intro paragraph (before first numbered section)
    intro = parts[0].strip() if parts and not re.match(r"^\d+\.\s", parts[0]) else ""
    section_parts = [p for p in parts if re.match(r"^\d+\.\s", p)]

    html_parts = []

    if intro:
        html_parts.append(
            f'<div class="ai-intro">{_md_to_html(intro, C["white"], C["muted"], C["dim"])}</div>'
        )

    for raw_sec in section_parts:
        m = re.match(r"^(\d+)\.\s+(.+?)\n(.*)", raw_sec, re.DOTALL)
        if not m:
            continue
        num, title, body = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()

        # pick colour / icon
        idx = int(num) - 1
        if 0 <= idx < len(SECTIONS):
            _, color, icon = SECTIONS[idx]
        else:
            color, icon = C["purple"], "smart_toy"

        body_html = _md_to_html(body, C["white"], C["light"], C["muted"])
        bg = color + "10"
        border = color + "30"

        html_parts.append(f"""
<div class="ai-section" style="background:{bg};border-color:{border};border-left:4px solid {color}">
  <div class="ai-section-title" style="color:{color}">
    <span class="material-icons-round mat-icon">{icon}</span>
    {num}. {title}
  </div>
  <div class="ai-section-body">{body_html}</div>
</div>""")

    return "\n".join(html_parts)


# ─────────────────────────────────────────────
# CLAUDE AI SECTION
# ─────────────────────────────────────────────
section(st.session_state.title_ai, "smart_toy")

def build_prompt():
    lines = [
        "Sən Etopaz platformasının (Azərbaycan) analitika ekspertisən.",
        f"Aşağıdakı {len(sel)} aylıq real məlumatı analiz et.",
        "**VACIB**: Azərbaycanca yaz. Markdown formatlaşdırma istifadə et — "
        "**qalın** mətn üçün **, siyahı üçün - işarəsi. Konkret rəqəmlər mütləq göstər.\n",
        f"=== DÖVR: {labs[0]} — {labs[-1]} ===",
        f"Ümumi dövriyyə: ₼{total_to:.2f}M",
        f"Ümumi GGR: ₼{total_ggr:.2f}M  |  Margin: {total_ggr/total_to*100:.1f}%",
        f"Ortalama payout ratio: {avg_pr:.2f}%",
        f"Son ay payout: {last_pr:.2f}%  {'⚠️ KRİTİK — 78% həddi aşılıb!' if last_pr>78 else '✓ Normal'}",
        f"Müştəri: {cust_list[0]:,} → {cust_list[-1]:,}  (MoM: {cust_mom:+.1f}%)",
        f"Depozit: ₼{total_dep:.2f}M  |  Çıxarış: ₼{total_wd:.2f}M  |  Nisbət: {dep_wd_r:.2f}×\n",
        "=== AYLIK MƏLUMAT ===",
    ]
    for p in sel:
        d = kpi_d[p]
        lines.append(f"{d['label']}: TO=₼{d['turnover']:.2f}M  GGR=₼{d['ggr']:.2f}M  "
                     f"PR={d['payout_ratio']:.1f}%  USR={d['users']:,}  RISK={d['risk_users']:,}")
    if ret_d:
        lines.append("\n=== RETENTION ===")
        for p in ret_periods:
            r = ret_d[p]
            lines.append(f"{kpi_d[p]['label']}: Retention={r['rate']}%  "
                         f"Yeni={r['new']:,}  Churn={r['churned']:,}")
    if fb_d:
        lines.append("\n=== FREEBET ===")
        for p in sel:
            if p in fb_d:
                f2 = fb_d[p]
                lines.append(f"{f2['label']}: Verilən=₼{f2['given']:.3f}M  "
                              f"İstifadə=₼{f2['used']:.3f}M  FB_PR={f2['payout_ratio']:.1f}%")
    lines.append("""
=== ANALİZ STRUKTURU ===
Aşağıdakı **4 bölmə** üzrə analiz ver. Hər bölmə 4-6 cümlə. Markdown istifadə et:

1. 📊 Performans Xülasəsi
(Əsas rəqəmlər, böyümə trendi, ən güclü/zəif aylar)

2. ⚠️ Kritik Risklər
(Payout ratio problemi, churn artımı, riskli müştəri sayı, konkret rəqəmlərlə)

3. 💡 Strateji Tövsiyələr
(3 konkret addım — hər birini bullet list olaraq yaz)

4. 📈 Növbəti Ay Proqnozu
(Rəqəmli hədəflər — dövriyyə, payout, müştəri üzrə)
""")
    return "\n".join(lines)


# API key
api_key = ""
try:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
except Exception:
    pass

if st.session_state.admin_mode and not api_key:
    api_key = st.text_input("🔑 Anthropic API Açarı",
                            type="password", placeholder="sk-ant-...", key="api_key_input")

btn_col, info_col = st.columns([2, 8])
with btn_col:
    run_ai = st.button("🤖 AI Analiz Et", type="primary", disabled=not bool(api_key))
with info_col:
    if not api_key:
        st.markdown(
            f'<div style="color:{C["muted"]};font-size:12.5px;padding-top:10px">'
            "Claude AI analizi üçün API açarı lazımdır (Streamlit Secrets).</div>",
            unsafe_allow_html=True)

if run_ai and api_key:
    with st.spinner("Claude analiz edir..."):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model="claude-opus-4-5-20251101",
                max_tokens=2000,
                messages=[{"role": "user", "content": build_prompt()}]
            )
            st.session_state.ai_result = msg.content[0].text
        except Exception as e:
            st.session_state.ai_result = f"HATA:{e}"

# ── Render AI result ──────────────────────────
if st.session_state.ai_result:
    raw = st.session_state.ai_result

    if raw.startswith("HATA:"):
        st.error(f"❌ Xəta: {raw[5:]}")
    else:
        cards_html = render_ai_response(raw)
        st.markdown(f"""
<div class="ai-outer">
  <div class="ai-header">
    <span class="material-icons-round mat-icon">smart_toy</span>
    <div>
      <div class="ai-header-text">Claude AI Analizi</div>
      <div class="ai-header-sub">{labs[0]} → {labs[-1]} · {len(sel)} ay · claude-opus-4-5</div>
    </div>
  </div>
  <div class="ai-body">
    {cards_html}
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:60px;padding-top:20px;border-top:1px solid {C['border']};
            text-align:center;font-size:11px;color:{C['dim']};
            letter-spacing:.07em;text-transform:uppercase">
    Etopaz Platform Analytics &nbsp;·&nbsp; OMT Dövrü &nbsp;·&nbsp; Mart 2026
</div>
""", unsafe_allow_html=True)
