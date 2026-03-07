"""
Etopaz Platform Analytics â Static Dashboard
No file upload required. Data is pre-loaded.
Claude AI insights integrated.
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# âââââââââââââââââââââââââââââââââââââââââââââ
# PAGE CONFIG
# âââââââââââââââââââââââââââââââââââââââââââââ
st.set_page_config(
    page_title="Etopaz Platform Analytics",
    page_icon="ð",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# âââââââââââââââââââââââââââââââââââââââââââââ
# COLOURS
# âââââââââââââââââââââââââââââââââââââââââââââ
C = {
    "bg":      "#0d0f14",
    "card":    "#13161d",
    "card2":   "#1a1e28",
    "border":  "#2a2f3e",
    "green":   "#10d98a",
    "blue":    "#3d9bff",
    "orange":  "#ff7043",
    "yellow":  "#ffc13d",
    "red":     "#f03e3e",
    "purple":  "#9b72f4",
    "white":   "#f0f2f8",
    "light":   "#c8ccda",
    "muted":   "#7b8299",
    "dim":     "#454c60",
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

# âââââââââââââââââââââââââââââââââââââââââââââ
# CSS
# âââââââââââââââââââââââââââââââââââââââââââââ
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap');

html, body, .stApp {{ background-color:{C['bg']} !important; font-family:'Inter',system-ui,sans-serif; color:{C['white']}; }}
section[data-testid="stSidebar"] {{ background-color:{C['card']} !important; border-right:1px solid {C['border']}; }}
section[data-testid="stSidebar"] * {{ color:{C['light']} !important; }}
.block-container {{ padding:2rem 2.5rem 4rem !important; max-width:100% !important; }}
h1,h2,h3,h4 {{ font-family:'Outfit',sans-serif !important; color:{C['white']} !important; }}
#MainMenu, footer, header {{ visibility:hidden; }}
hr {{ border-color:{C['border']} !important; }}
div[data-testid="stTextInput"] input {{ background:{C['card2']} !important; border:1px solid {C['border']} !important; color:{C['white']} !important; border-radius:8px; }}
div[data-testid="stTextInput"] label {{ color:{C['muted']} !important; font-size:11px !important; }}

.kpi-card {{
    background:{C['card']}; border:1px solid {C['border']}; border-radius:12px;
    padding:20px 18px 18px; position:relative; overflow:hidden; height:100%;
}}
.kpi-card::before {{ content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:12px 12px 0 0; }}
.kpi-card.green::before  {{ background:{C['green']}; }}
.kpi-card.blue::before   {{ background:{C['blue']}; }}
.kpi-card.orange::before {{ background:{C['orange']}; }}
.kpi-card.yellow::before {{ background:{C['yellow']}; }}
.kpi-card.red::before    {{ background:{C['red']}; }}
.kpi-label {{ font-size:11px; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:{C['muted']}; margin-bottom:9px; }}
.kpi-val {{ font-family:'Outfit',sans-serif; font-size:26px; font-weight:800; letter-spacing:-.02em; line-height:1; margin-bottom:7px; }}
.kpi-val.green  {{ color:{C['green']}; }}
.kpi-val.blue   {{ color:{C['blue']}; }}
.kpi-val.orange {{ color:{C['orange']}; }}
.kpi-val.yellow {{ color:{C['yellow']}; }}
.kpi-val.red    {{ color:{C['red']}; }}
.kpi-sub {{ font-size:12px; color:{C['muted']}; margin-bottom:7px; line-height:1.4; }}
.badge {{ display:inline-flex; align-items:center; gap:3px; font-size:11.5px; font-weight:600; padding:2px 9px; border-radius:20px; }}
.badge.up   {{ background:rgba(16,217,138,.12); color:{C['green']}; }}
.badge.down {{ background:rgba(240,62,62,.12);  color:{C['red']}; }}
.badge.warn {{ background:rgba(255,193,61,.12); color:{C['yellow']}; }}

.sec-head {{ display:flex; align-items:center; gap:12px; margin:44px 0 18px; }}
.sec-head span {{ font-family:'Outfit',sans-serif; font-size:12px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:{C['muted']}; white-space:nowrap; }}
.sec-line {{ flex:1; height:1px; background:{C['border']}; }}

.c-title {{ font-family:'Outfit',sans-serif; font-size:15px; font-weight:700; color:{C['white']}; margin-bottom:3px; }}

.styled-table {{ width:100%; border-collapse:collapse; font-size:13.5px; }}
.styled-table th {{
    background:{C['card2']}; font-size:10.5px; font-weight:700;
    letter-spacing:.1em; text-transform:uppercase; color:{C['muted']};
    padding:11px 14px; text-align:right; white-space:nowrap;
    border-bottom:1px solid {C['border']};
}}
.styled-table th:first-child {{ text-align:left; }}
.styled-table td {{ padding:11px 14px; text-align:right; color:{C['light']}; border-top:1px solid {C['border']}; white-space:nowrap; }}
.styled-table td:first-child {{ text-align:left; font-weight:600; color:{C['white']}; }}
.styled-table tr:hover td {{ background:{C['card2']}; }}
.vg {{ color:{C['green']}!important; font-weight:600; }}
.vy {{ color:{C['yellow']}!important; font-weight:600; }}
.vr {{ color:{C['red']}!important;    font-weight:600; }}

.ret-card {{ background:{C['card']}; border:1px solid {C['border']}; border-radius:12px; padding:16px 12px; text-align:center; height:100%; }}
.ret-per {{ font-size:10px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:{C['muted']}; margin-bottom:9px; }}
.ret-pct {{ font-family:'Outfit',sans-serif; font-size:24px; font-weight:800; line-height:1; margin-bottom:7px; }}
.ret-new   {{ font-size:11.5px; color:{C['green']}; font-weight:500; }}
.ret-churn {{ font-size:11.5px; color:{C['orange']}; font-weight:500; margin-top:2px; }}

.ai-box {{ background:rgba(155,114,244,.04); border:1px solid rgba(155,114,244,.35);
           border-radius:14px; padding:26px 28px; margin-top:10px; }}
.ai-box h3 {{ font-family:'Outfit',sans-serif!important; font-size:18px!important;
              font-weight:700; color:{C['purple']}!important; margin-bottom:16px!important; }}
.ai-content {{ font-size:14px; color:{C['light']}; line-height:1.9; white-space:pre-wrap; }}
</style>
""", unsafe_allow_html=True)

# âââââââââââââââââââââââââââââââââââââââââââââ
# HARDCODED DATA  (Jun 2025 â Feb 2026)
# âââââââââââââââââââââââââââââââââââââââââââââ
RAW_KPI = {
    "2025-06": {"label":"Ä°yun 2025",     "turnover":6.041,  "ggr":1.373, "payout_ratio":77.28, "deposits":2.744,  "withdrawals":1.44,  "tickets":324681,  "users":10315, "risk_users":1097, "pareto_top1_pct":40.2, "pareto_top1_count":103},
    "2025-07": {"label":"Ä°yul 2025",     "turnover":18.107, "ggr":4.295, "payout_ratio":76.28, "deposits":8.59,   "withdrawals":4.286, "tickets":970138,  "users":14412, "risk_users":1297, "pareto_top1_pct":43.1, "pareto_top1_count":144},
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
    "2025-06": {"label":"Ä°yun 2025",     "given":0.12,  "used":0.084, "fb_payout":0.033, "payout_ratio":38.71},
    "2025-07": {"label":"Ä°yul 2025",     "given":0.393, "used":0.359, "fb_payout":0.152, "payout_ratio":42.15},
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

# âââââââââââââââââââââââââââââââââââââââââââââ
# SESSION STATE
# âââââââââââââââââââââââââââââââââââââââââââââ
ADMIN_PASS = "etopaz2026"

_defaults = {
    "admin_mode":    False,
    "title_main":    "Etopaz Platform Analytics",
    "title_sub":     "OMT DÃ¶vrÃ¼  Â·  MÃ¼ÅtÉri SÉviyyÉsindÉ DÉrin Analiz",
    "title_kpi":     "Æsas GÃ¶stIricilÉr",
    "title_trend":   "AylÄ±q Trend Analizi",
    "title_table":   "AylÄ±q Tam CÉdvÉl",
    "title_ret":     "MÃ¼ÅtÉri SaxlanÄ±lmasÄ± â Retention",
    "title_fb":      "Freebet Analizi",
    "title_ai":      "Claude AI â Etopaz AnalitikasÄ±",
    "ai_result":     "",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# âââââââââââââââââââââââââââââââââââââââââââââ
# SIDEBAR
# âââââââââââââââââââââââââââââââââââââââââââââ
with st.sidebar:
    st.markdown(f"""
    <div style="padding:14px 0 18px">
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

    st.markdown("**ð Tarix AralÄ±ÄÄ±**")
    labels_all = [LABELS[p] for p in ALL_PERIODS]
    start_i = st.selectbox("BaÅlanÄÄ±c", range(len(ALL_PERIODS)),
                           format_func=lambda i: labels_all[i], key="s_start")
    end_i   = st.selectbox("Son ay",    range(len(ALL_PERIODS)),
                           format_func=lambda i: labels_all[i],
                           index=len(ALL_PERIODS)-1, key="s_end")
    if start_i > end_i:
        st.error("BaÅlanÄÄ±c son aydan bÃ¶yÃ¼k ola bilmÉz!")
        sel = ALL_PERIODS[:]
    else:
        sel = ALL_PERIODS[start_i:end_i+1]

    st.divider()
    st.markdown("**âï¸ Admin Modu**")
    if not st.session_state.admin_mode:
        pw = st.text_input("ÅifrÉ", type="password", placeholder="â¢â¢â¢â¢â¢â¢â¢â¢", key="pw_input")
        if pw == ADMIN_PASS:
            st.session_state.admin_mode = True
            st.rerun()
        elif pw:
            st.error("ÅifrÉ yanlÄ±ÅdÄ±r")
    else:
        st.success("â Admin modu aktiv")
        if st.button("ÃÄ±xÄ±Å"):
            st.session_state.admin_mode = False
            st.rerun()

# âââââââââââââââââââââââââââââââââââââââââââââ
# ADMIN TITLE EDITOR
# âââââââââââââââââââââââââââââââââââââââââââââ
if st.session_state.admin_mode:
    with st.expander("âï¸ BaÅlÄ±qlarÄ± RedaktÉ Et", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.title_main  = st.text_input("Æsas baÅlÄ±q",        st.session_state.title_main,  key="e1")
            st.session_state.title_sub   = st.text_input("Alt baÅlÄ±q",          st.session_state.title_sub,   key="e2")
            st.session_state.title_kpi   = st.text_input("KPI bÃ¶lmÉsi",         st.session_state.title_kpi,   key="e3")
            st.session_state.title_trend = st.text_input("Trend bÃ¶lmÉsi",       st.session_state.title_trend, key="e4")
        with c2:
            st.session_state.title_table = st.text_input("CÉdvÉl bÃ¶lmÉsi",      st.session_state.title_table, key="e5")
            st.session_state.title_ret   = st.text_input("Retention bÃ¶lmÉsi",   st.session_state.title_ret,   key="e6")
            st.session_state.title_fb    = st.text_input("Freebet bÃ¶lmÉsi",     st.session_state.title_fb,    key="e7")
            st.session_state.title_ai    = st.text_input("AI bÃ¶lmÉsi baÅlÄ±ÄÄ±",  st.session_state.title_ai,    key="e8")

# âââââââââââââââââââââââââââââââââââââââââââââ
# HELPERS
# âââââââââââââââââââââââââââââââââââââââââââââ
def section(title):
    st.markdown(
        f'<div class="sec-head"><span>{title}</span><div class="sec-line"></div></div>',
        unsafe_allow_html=True)

def kpi_card(label, value, sub, badge_txt, badge_cls, color):
    st.markdown(f"""
    <div class="kpi-card {color}">
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
                         hovertemplate=f"<b>%{{x}}</b><br>{bar_name}: â¼%{{y:.2f}}M<extra></extra>"),
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

# âââââââââââââââââââââââââââââââââââââââââââââ
# FILTER DATA
# âââââââââââââââââââââââââââââââââââââââââââââ
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
to_mom    = round((to_list[-1]/to_list[-2]-1)*100,1) if len(to_list)>1 else 0
ggr_mom   = round((ggr_list[-1]/ggr_list[-2]-1)*100,1) if len(ggr_list)>1 else 0
cust_mom  = round((cust_list[-1]/cust_list[-2]-1)*100,1) if len(cust_list)>1 else 0

# âââââââââââââââââââââââââââââââââââââââââââââ
# HEADER
# âââââââââââââââââââââââââââââââââââââââââââââ
st.markdown(f"""
<div style="padding-bottom:24px;border-bottom:1px solid {C['border']}">
    <div style="font-family:'Outfit',sans-serif;font-size:30px;font-weight:900;
                background:linear-gradient(120deg,{C['green']} 0%,{C['blue']} 60%);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1">
        {st.session_state.title_main}
    </div>
    <div style="font-size:13px;color:{C['muted']};margin-top:5px">
        {st.session_state.title_sub}
    </div>
</div>
""", unsafe_allow_html=True)

# âââââââââââââââââââââââââââââââââââââââââââââ
# KPI CARDS
# âââââââââââââââââââââââââââââââââââââââââââââ
section(st.session_state.title_kpi)
k1,k2,k3,k4,k5 = st.columns(5)
with k1:
    kpi_card("Ãmumi DÃ¶vriyyÉ", f"â¼{total_to:.1f}M",
             f"{len(sel)} ay Ã¼zrÉ",
             f"{'â²' if to_mom>=0 else 'â¼'} {abs(to_mom):.1f}% son ay",
             "up" if to_mom>=0 else "down", "green")
with k2:
    kpi_card("Ãmumi GGR", f"â¼{total_ggr:.1f}M",
             f"Margin: {total_ggr/total_to*100:.1f}%",
             f"{'â²' if ggr_mom>=0 else 'â¼'} {abs(ggr_mom):.1f}% son ay",
             "up" if ggr_mom>=0 else "down", "blue")
with k3:
    kpi_card("Son Ay Payout", f"{last_pr:.1f}%",
             f"Ortalama: {avg_pr:.1f}% | Benchmark: 77%",
             "â  YÃ¼ksÉk" if last_pr>78 else "â Normal",
             "warn" if last_pr>78 else "up",
             "red" if last_pr>78 else "yellow")
with k4:
    kpi_card("Son Ay MÃ¼ÅtÉri", f"{cust_list[-1]:,}",
             f"Ä°lk ay: {cust_list[0]:,}",
             f"{'â²' if cust_mom>=0 else 'â¼'} {abs(cust_mom):.1f}% son ay",
             "up" if cust_mom>=0 else "down", "orange")
with k5:
    kpi_card("Depozit / ÃÄ±xarÄ±Å", f"â¼{total_dep:.1f}M",
             f"ÃÄ±xarÄ±Å: â¼{total_wd:.1f}M",
             f"NisbÉt: {dep_wd_r:.2f}Ã",
             "up", "green")

# âââââââââââââââââââââââââââââââââââââââââââââ
# TREND CHARTS
# âââââââââââââââââââââââââââââââââââââââââââââ
section(st.session_state.title_trend)
tc1, tc2 = st.columns(2)
with tc1:
    st.markdown('<div class="c-title">AylÄ±q DÃ¶vriyyÉ (â¼M)</div>', unsafe_allow_html=True)
    to_colors = [C["green"] if v==max(to_list) else C["blue"] for v in to_list]
    st.plotly_chart(bar_chart(labs, to_list, to_colors), use_container_width=True, config={"displayModeBar":False})
with tc2:
    st.markdown('<div class="c-title">GGR (â¼M) vÉ Payout Ratio (%)</div>', unsafe_allow_html=True)
    st.plotly_chart(
        bar_line_chart(labs, ggr_list, pr_list, "GGR (â¼M)", "Payout %",
                       C["blue"], C["yellow"], y2_range=[60,90]),
        use_container_width=True, config={"displayModeBar":False})

tc3, tc4 = st.columns(2)
with tc3:
    st.markdown('<div class="c-title">Aktiv MÃ¼ÅtÉri SayÄ±</div>', unsafe_allow_html=True)
    cust_colors = [C["orange"] if v==max(cust_list) else C["purple"] for v in cust_list]
    st.plotly_chart(bar_chart(labs, cust_list, cust_colors), use_container_width=True, config={"displayModeBar":False})
with tc4:
    st.markdown('<div class="c-title">Depozit vs ÃÄ±xarÄ±Å (â¼M)</div>', unsafe_allow_html=True)
    fig_dw = go.Figure()
    fig_dw.add_trace(go.Bar(x=labs, y=dep_list, name="Depozit", marker_color=C["green"],  marker_line_width=0))
    fig_dw.add_trace(go.Bar(x=labs, y=wd_list,  name="ÃÄ±xarÄ±Å", marker_color=C["orange"], marker_line_width=0))
    fig_dw.update_layout(**{**PL,"height":260,"showlegend":True,"barmode":"group",
                            "legend":dict(orientation="h",y=1.12,bgcolor="rgba(0,0,0,0)")})
    st.plotly_chart(fig_dw, use_container_width=True, config={"displayModeBar":False})

# âââââââââââââââââââââââââââââââââââââââââââââ
# MONTHLY TABLE
# âââââââââââââââââââââââââââââââââââââââââââââ
section(st.session_state.title_table)

def pcls(v):
    return "vg" if v<75 else ("vy" if v<79 else "vr")

rows = ""
for p in sel:
    d = kpi_d[p]
    rows += f"""<tr>
        <td>{d['label']}</td>
        <td>â¼{d['turnover']:.3f}M</td>
        <td>â¼{d['ggr']:.3f}M</td>
        <td class="{pcls(d['payout_ratio'])}">{d['payout_ratio']:.2f}%</td>
        <td>{d['users']:,}</td>
        <td>â¼{d['deposits']:.3f}M</td>
        <td>â¼{d['withdrawals']:.3f}M</td>
        <td>{d['tickets']:,}</td>
        <td class="vr">{d['risk_users']:,}</td>
    </tr>"""

st.markdown(f"""
<div style="background:{C['card']};border:1px solid {C['border']};border-radius:12px;overflow:hidden;overflow-x:auto">
<table class="styled-table"><thead><tr>
    <th>Ay</th><th>DÃ¶vriyyÉ</th><th>GGR</th><th>Payout %</th>
    <th>MÃ¼ÅtÉri</th><th>Depozit</th><th>ÃÄ±xarÄ±Å</th><th>Ticket</th><th>Riskli</th>
</tr></thead><tbody>{rows}</tbody></table>
</div>
""", unsafe_allow_html=True)

# âââââââââââââââââââââââââââââââââââââââââââââ
# RETENTION
# âââââââââââââââââââââââââââââââââââââââââââââ
ret_periods = [p for p in sel if p in ret_d]
if ret_periods:
    section(st.session_state.title_ret)
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
                <div class="ret-churn">-{r['churned']:,} Ã§Ä±xdÄ±</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ret_labs  = [kpi_d[p]["label"] for p in ret_periods]
    ret_rates = [ret_d[p]["rate"]  for p in ret_periods]
    ret_clrs  = [C["green"] if v>=85 else (C["yellow"] if v>=80 else C["red"]) for v in ret_rates]
    st.plotly_chart(bar_chart(ret_labs, ret_rates, ret_clrs, height=220),
                    use_container_width=True, config={"displayModeBar":False})

# âââââââââââââââââââââââââââââââââââââââââââââ
# FREEBET
# âââââââââââââââââââââââââââââââââââââââââââââ
if fb_d:
    section(st.session_state.title_fb)
    fb_labs  = [fb_d[p]["label"]        for p in sel if p in fb_d]
    fb_given = [fb_d[p]["given"]        for p in sel if p in fb_d]
    fb_used  = [fb_d[p]["used"]         for p in sel if p in fb_d]
    fb_pr    = [fb_d[p]["payout_ratio"] for p in sel if p in fb_d]

    fb1, fb2 = st.columns(2)
    with fb1:
        st.markdown('<div class="c-title">Freebet VerilÉn vs Ä°stifadÉ (â¼M)</div>', unsafe_allow_html=True)
        fig_fb = go.Figure()
        fig_fb.add_trace(go.Bar(x=fb_labs, y=fb_given, name="VerilÉn",   marker_color=C["purple"], marker_line_width=0))
        fig_fb.add_trace(go.Bar(x=fb_labs, y=fb_used,  name="Ä°stifadÉ", marker_color=C["blue"],   marker_line_width=0))
        fig_fb.update_layout(**{**PL,"height":250,"showlegend":True,"barmode":"group",
                                "legend":dict(orientation="h",y=1.12,bgcolor="rgba(0,0,0,0)")})
        st.plotly_chart(fig_fb, use_container_width=True, config={"displayModeBar":False})
    with fb2:
        st.markdown('<div class="c-title">Freebet Payout Ratio (%)</div>', unsafe_allow_html=True)
        fb_clrs = [C["red"] if v>47 else C["green"] for v in fb_pr]
        st.plotly_chart(bar_chart(fb_labs, fb_pr, fb_clrs, height=250),
                        use_container_width=True, config={"displayModeBar":False})

# âââââââââââââââââââââââââââââââââââââââââââââ
# CLAUDE AI SECTION
# âââââââââââââââââââââââââââââââââââââââââââââ
section(st.session_state.title_ai)

def build_prompt():
    lines = [
        f"SÉn Etopaz platformasÄ±nÄ±n (AzÉrbaycan) analitika ekspertisÉn.",
        f"AÅaÄÄ±dakÄ± {len(sel)} aylÄ±q real mÉlumatÄ± analiz et. AzÉrbaycanca dÉrin, konkret, rÉqÉmlÉrÉ Ésaslanan analiz ver.\n",
        f"=== DÃVR: {labs[0]} â {labs[-1]} ===",
        f"Ãmumi dÃ¶vriyyÉ: â¼{total_to:.2f}M",
        f"Ãmumi GGR: â¼{total_ggr:.2f}M  |  Margin: {total_ggr/total_to*100:.1f}%",
        f"Ortalama payout ratio: {avg_pr:.2f}%",
        f"Son ay payout: {last_pr:.2f}%  {'â ï¸ KRÄ°TÄ°K â 78% hÉddi aÅÄ±lÄ±b!' if last_pr>78 else 'â Normal'}",
        f"MÃ¼ÅtÉri: {cust_list[0]:,} â {cust_list[-1]:,}  (MoM: {cust_mom:+.1f}%)",
        f"Depozit: â¼{total_dep:.2f}M  |  ÃÄ±xarÄ±Å: â¼{total_wd:.2f}M  |  NisbÉt: {dep_wd_r:.2f}Ã\n",
        "=== AYLIK MÆLUMAT ===",
    ]
    for p in sel:
        d = kpi_d[p]
        lines.append(f"{d['label']}: TO=â¼{d['turnover']:.2f}M  GGR=â¼{d['ggr']:.2f}M  PR={d['payout_ratio']:.1f}%  USR={d['users']:,}  RISK={d['risk_users']:,}")
    if ret_d:
        lines.append("\n=== RETENTION ===")
        for p in ret_periods:
            r = ret_d[p]
            lines.append(f"{kpi_d[p]['label']}: Retention={r['rate']}%  Yeni={r['new']:,}  Churn={r['churned']:,}")
    if fb_d:
        lines.append("\n=== FREEBET ===")
        for p in sel:
            if p in fb_d:
                f2 = fb_d[p]
                lines.append(f"{f2['label']}: VerilÉn=â¼{f2['given']:.3f}M  Ä°stifadÉ=â¼{f2['used']:.3f}M  FB_PR={f2['payout_ratio']:.1f}%")
    lines.append("""
=== ANALÄ°Z STRUKTURU ===
AÅaÄÄ±dakÄ± 4 bÃ¶lmÉ Ã¼zrÉ analiz ver. HÉr bÃ¶lmÉ 4-5 cÃ¼mlÉ olsun. Konkret rÉqÉmlÉr istifadÉ et:

1. ð Performans XÃ¼lasÉsi
2. â ï¸ Kritik RisklÉr (payout, churn, riskli mÃ¼ÅtÉrilÉr)
3. ð¡ Strateji TÃ¶vsiyÉlÉr (3 konkret addÄ±m)
4. ð NÃ¶vbÉti Ay Proqnozu
""")
    return "\n".join(lines)

# API key
api_key = ""
try:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
except Exception:
    pass

if st.session_state.admin_mode and not api_key:
    api_key = st.text_input("ð Anthropic API AÃ§arÄ±",
                            type="password", placeholder="sk-ant-...", key="api_key_input")

btn_col, info_col = st.columns([2, 8])
with btn_col:
    run_ai = st.button("ð¤ AI Analiz Et", type="primary", disabled=not bool(api_key))
with info_col:
    if not api_key:
        st.markdown(
            f'<div style="color:{C["muted"]};font-size:12.5px;padding-top:10px">'
            f'Claude AI analizi Ã¼Ã§Ã¼n admin modunda API aÃ§arÄ±nÄ± daxil edin.</div>',
            unsafe_allow_html=True)

if run_ai and api_key:
    with st.spinner("Claude analiz edir..."):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model="claude-opus-4-5-20251101",
                max_tokens=1800,
                messages=[{"role": "user", "content": build_prompt()}]
            )
            st.session_state.ai_result = msg.content[0].text
        except Exception as e:
            st.session_state.ai_result = f"â XÉta: {e}"

if st.session_state.ai_result:
    st.markdown(f"""
    <div class="ai-box">
        <h3>ð¤ Claude AI Analizi â {labs[0]} â {labs[-1]}</h3>
        <div class="ai-content">{st.session_state.ai_result}</div>
    </div>
    """, unsafe_allow_html=True)

# âââââââââââââââââââââââââââââââââââââââââââââ
# FOOTER
# âââââââââââââââââââââââââââââââââââââââââââââ
st.markdown(f"""
<div style="margin-top:60px;padding-top:20px;border-top:1px solid {C['border']};
            text-align:center;font-size:11px;color:{C['dim']};
            letter-spacing:.07em;text-transform:uppercase">
    Etopaz Platform Analytics &nbsp;Â·&nbsp; OMT DÃ¶vrÃ¼ &nbsp;Â·&nbsp; Mart 2026
</div>
""", unsafe_allow_html=True)

