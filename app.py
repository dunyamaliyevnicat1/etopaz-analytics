"""
Etopaz Platform Analytics
Streamlit Dashboard
"""

import io
import re
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Etopaz Platform Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# COLOURS
# ─────────────────────────────────────────────
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

# Base Plotly layout
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
# CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap');

html, body, .stApp {{ background-color:{C['bg']} !important; font-family:'Inter',system-ui,sans-serif; color:{C['white']}; }}
section[data-testid="stSidebar"] {{ background-color:{C['card']} !important; border-right:1px solid {C['border']}; }}
section[data-testid="stSidebar"] * {{ color:{C['light']} !important; }}
.block-container {{ padding:2rem 2rem 4rem !important; max-width:100% !important; }}
h1,h2,h3,h4 {{ font-family:'Outfit',sans-serif !important; color:{C['white']} !important; }}
#MainMenu, footer, header {{ visibility:hidden; }}
hr {{ border-color:{C['border']} !important; }}

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
.c-sub   {{ font-size:12px; color:{C['muted']}; margin-bottom:4px; line-height:1.5; }}

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

.insight {{ background:{C['card']}; border:1px solid {C['border']}; border-radius:12px; padding:22px; height:100%; }}
.insight.pos   {{ border-color:rgba(16,217,138,.3);  background:rgba(16,217,138,.04); }}
.insight.alert {{ border-color:rgba(240,62,62,.35);  background:rgba(240,62,62,.04); }}
.insight.warn  {{ border-color:rgba(255,193,61,.3);   background:rgba(255,193,61,.04); }}
.insight h4  {{ font-family:'Outfit',sans-serif!important; font-size:15px!important; font-weight:700; color:{C['white']}!important; margin:8px 0 10px!important; }}
.insight p   {{ font-size:13.5px; color:{C['light']}; line-height:1.75; }}
.insight p strong {{ color:{C['white']}; }}
.hi  {{ color:{C['green']};  font-weight:600; }}
.dng {{ color:{C['red']};    font-weight:600; }}
.wrn {{ color:{C['yellow']}; font-weight:600; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
MONTH_MAP = {
    "january": (1, "Yanvar"),   "february": (2, "Fevral"),
    "march":   (3, "Mart"),     "april":    (4, "Aprel"),
    "may":     (5, "May"),      "june":     (6, "İyun"),
    "july":    (7, "İyul"),     "august":   (8, "Avqust"),
    "september":(9,"Sentyabr"), "october": (10, "Oktyabr"),
    "november":(11,"Noyabr"),   "december":(12, "Dekabr"),
}

TIERS = [
    "Sharp Platinium", "Platinium", "Sharp Gold", "Gold",
    "Sharp Silver", "Silver", "Bronze", "Iron",
    "Rusty Iron", "Regular", "Inactive",
]

TIER_COLORS = {
    "Platinium": C["green"],  "Sharp Platinium": C["green"],
    "Gold":      C["yellow"], "Sharp Gold":      C["yellow"],
    "Silver":    C["blue"],   "Sharp Silver":    C["blue"],
    "Bronze":    C["orange"], "Iron":            C["muted"],
    "Rusty Iron":C["dim"],    "Regular":         C["dim"],
    "Inactive":  C["dim"],
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def extract_period(filename: str):
    fn = filename.lower()
    for eng, (num, az) in MONTH_MAP.items():
        if eng in fn:
            years = re.findall(r"20\d{2}", fn)
            if years:
                y = int(years[0])
                return f"{y}-{num:02d}", f"{az} {y}"
    return None, None


def section(title: str):
    st.markdown(
        f'<div class="sec-head"><span>{title}</span><div class="sec-line"></div></div>',
        unsafe_allow_html=True,
    )


def kpi_html(label, value, sub, badge_txt, badge_cls, color):
    return f"""
    <div class="kpi-card {color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val {color}">{value}</div>
        <div class="kpi-sub">{sub}</div>
        <span class="badge {badge_cls}">{badge_txt}</span>
    </div>"""


# ─────────────────────────────────────────────
# DATA PROCESSING (cached)
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def process_kpi(file_bytes: bytes):
    df = pd.read_excel(io.BytesIO(file_bytes))
    # Standardise column names by position
    cols = ["user_id", "period", "tickets", "turnover", "payout",
            "ggr", "payout_ratio", "fb_turnover", "fb_payout",
            "deposit", "withdrawal", "bet_days"]
    df.columns = cols[:len(df.columns)]

    users = df[(df["period"] == "Total") & (df["user_id"] != "Grand Total")].copy()
    users["user_id"] = users["user_id"].astype(str)
    for col in ["turnover", "ggr", "payout_ratio", "deposit", "withdrawal", "tickets"]:
        users[col] = pd.to_numeric(users[col], errors="coerce").fillna(0)

    gt_row = df[df["user_id"] == "Grand Total"]
    if gt_row.empty:
        return users, {}
    gt = gt_row.iloc[0]
    return users, {
        "users":        len(users),
        "turnover":     float(gt["turnover"]),
        "ggr":          float(gt["ggr"]),
        "payout_ratio": float(gt["payout_ratio"]),
        "deposits":     float(gt["deposit"]),
        "withdrawals":  float(gt["withdrawal"]),
        "tickets":      int(gt["tickets"]),
    }


@st.cache_data(show_spinner=False)
def process_fb(file_bytes: bytes):
    df = pd.read_excel(io.BytesIO(file_bytes))
    cols = ["user_id", "tier", "name", "category", "given", "used", "fb_payout", "fb_payout_ratio"]
    df.columns = cols[:len(df.columns)]

    gt_row = df[df["user_id"] == "Grand Total"]
    if gt_row.empty:
        return pd.DataFrame(), {}
    gt = gt_row.iloc[0]

    user_rows = df[df["tier"].isin(TIERS)].copy()
    for col in ["given", "used", "fb_payout", "fb_payout_ratio"]:
        user_rows[col] = pd.to_numeric(user_rows[col], errors="coerce").fillna(0)

    return user_rows, {
        "given":        float(gt["given"]),
        "used":         float(gt["used"]),
        "fb_payout":    float(gt["fb_payout"]),
        "payout_ratio": float(gt["fb_payout_ratio"]),
    }


# ─────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────
def bar_chart(x, y, colors=None, y_fmt=None, height=260):
    if colors is None:
        colors = [C["blue"]] * len(y)
    fig = go.Figure(go.Bar(
        x=x, y=y,
        marker_color=colors, marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>",
    ))
    layout = {**PL, "height": height}
    if y_fmt:
        layout["yaxis"] = {**layout.get("yaxis", {}),
                           "tickprefix": y_fmt.get("prefix", ""),
                           "ticksuffix": y_fmt.get("suffix", "")}
    fig.update_layout(**layout)
    return fig


def line_chart(x, y, color, fill=True, y_range=None, height=240):
    rgba = f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)"
    fig = go.Figure(go.Scatter(
        x=x, y=y,
        line=dict(color=color, width=2.5),
        mode="lines+markers",
        marker=dict(size=5, color=color),
        fill="tozeroy" if fill else None,
        fillcolor=rgba,
        hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>",
    ))
    layout = {**PL, "height": height}
    if y_range:
        layout["yaxis"] = {**layout.get("yaxis", {}), "range": y_range}
    fig.update_layout(**layout, showlegend=False)
    return fig


def bar_line_chart(x, bar_y, line_y, bar_name, line_name,
                   bar_color, line_color, y2_range=None, height=260):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=x, y=bar_y, name=bar_name,
        marker_color=bar_color, marker_line_width=0,
        hovertemplate=f"<b>%{{x}}</b><br>{bar_name}: %{{y:.2f}}<extra></extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=x, y=line_y, name=line_name,
        line=dict(color=line_color, width=2.5),
        mode="lines+markers",
        marker=dict(size=6, color=[C["red"] if v > 78 else line_color for v in line_y]),
        hovertemplate=f"<b>%{{x}}</b><br>{line_name}: %{{y:.1f}}%<extra></extra>",
    ), secondary_y=True)
    layout = {**PL, "height": height, "showlegend": True,
              "legend": dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)")}
    if y2_range:
        layout["yaxis2"] = dict(range=y2_range, gridcolor=C["border"],
                                tickfont=dict(color=C["muted"]),
                                ticksuffix="%", zeroline=False,
                                showgrid=False)
    fig.update_layout(**layout)
    return fig


def grouped_bar(x, y1, y2, name1, name2, c1, c2, height=240):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y1, name=name1, marker_color=c1, marker_line_width=0))
    fig.add_trace(go.Bar(x=x, y=y2, name=name2, marker_color=c2, marker_line_width=0))
    layout = {**PL, "height": height, "showlegend": True, "barmode": "group",
              "legend": dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)")}
    fig.update_layout(**layout)
    return fig


def donut_chart(labels, values, colors, height=240):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(width=0)),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
    ))
    layout = {**PL, "height": height, "showlegend": True,
              "legend": dict(orientation="v", x=1.0, y=0.5,
                             bgcolor="rgba(0,0,0,0)", font=dict(color=C["muted"], size=10))}
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:12px 0 20px">
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

    st.markdown("**📂 USER BASE KPI Faylları**")
    kpi_uploads = st.file_uploader(
        "kpi", type=["xlsx"], accept_multiple_files=True,
        label_visibility="collapsed",
        help="Hər ay üçün 'User Based KPI ...' Excel faylını yükləyin",
    )

    st.markdown("**🎁 Freebet Faylları** *(isteğe bağlı)*")
    fb_uploads = st.file_uploader(
        "fb", type=["xlsx"], accept_multiple_files=True,
        label_visibility="collapsed",
        help="Hər ay üçün 'Freebet Categories ...' Excel faylını yükləyin",
    )

    st.divider()

    # Date range — computed after files are loaded
    selected_periods = []
    if kpi_uploads:
        period_map = {}
        for f in kpi_uploads:
            pid, lbl = extract_period(f.name)
            if pid:
                period_map[pid] = lbl
        sorted_all = sorted(period_map.keys())
        labels_all = [period_map[p] for p in sorted_all]

        if len(sorted_all) >= 2:
            st.markdown("**📅 Tarix Aralığı**")
            start_i = st.selectbox(
                "Başlanğıc ay", range(len(labels_all)),
                format_func=lambda i: labels_all[i], key="s_start",
            )
            end_i = st.selectbox(
                "Son ay", range(len(labels_all)),
                format_func=lambda i: labels_all[i],
                index=len(labels_all) - 1, key="s_end",
            )
            if start_i > end_i:
                st.error("Başlanğıc son aydan böyük ola bilməz!")
                selected_periods = sorted_all
            else:
                selected_periods = sorted_all[start_i : end_i + 1]
        else:
            selected_periods = sorted_all

    st.divider()
    st.markdown(
        f"<div style='font-size:11px;color:{C['dim']};text-align:center'>Etopaz Platform · Mart 2026</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:24px;border-bottom:1px solid {C['border']}">
    <div style="font-family:'Outfit',sans-serif;font-size:30px;font-weight:900;
                background:linear-gradient(120deg,{C['green']} 0%,{C['blue']} 60%);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1">
        Etopaz Platform Analytics
    </div>
    <div style="font-size:13px;color:{C['muted']};margin-top:5px">
        Etopaz Platform &nbsp;·&nbsp; OMT Dövrü &nbsp;·&nbsp; Müştəri Səviyyəsində Dərin Analiz
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NO DATA STATE
# ─────────────────────────────────────────────
if not kpi_uploads:
    st.markdown(f"""
    <div style="text-align:center;padding:80px 20px">
        <div style="font-size:60px;margin-bottom:20px">📁</div>
        <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;
                    color:{C['white']};margin-bottom:12px">
            Məlumat yükləyin
        </div>
        <div style="font-size:14px;color:{C['muted']};max-width:420px;margin:0 auto;line-height:1.8">
            Sol paneldən <strong style="color:{C['light']}">USER BASE KPI</strong>
            Excel fayllarını yükləyin.<br>
            Hər ay üçün ayrı fayl yükləyə bilərsiniz.<br>
            Freebet faylları <em>isteğe bağlıdır</em>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# PROCESS FILES
# ─────────────────────────────────────────────
kpi_data  = {}   # pid -> {label, users, turnover, ...}
kpi_users = {}   # pid -> DataFrame

with st.spinner("Məlumatlar işlənir..."):
    for f in kpi_uploads:
        pid, label = extract_period(f.name)
        if pid and pid in selected_periods:
            raw = f.read(); f.seek(0)
            users_df, gt = process_kpi(raw)
            if gt:
                kpi_data[pid]  = {**gt, "label": label}
                kpi_users[pid] = users_df

fb_data       = {}   # pid -> {label, given, used, ...}
fb_users_data = {}   # pid -> DataFrame

if fb_uploads:
    for f in fb_uploads:
        pid, label = extract_period(f.name)
        if pid and pid in selected_periods:
            raw = f.read(); f.seek(0)
            fb_df, gt = process_fb(raw)
            if gt:
                fb_data[pid]       = {**gt, "label": label}
                fb_users_data[pid] = fb_df

if not kpi_data:
    st.warning("Seçilmiş tarix aralığı üçün məlumat tapılmadı. Faylları yoxlayın.")
    st.stop()

sorted_kpi    = sorted(kpi_data.keys())
months_labels = [kpi_data[p]["label"] for p in sorted_kpi]
months_short  = [l.split()[0][:3] for l in months_labels]

# ─────────────────────────────────────────────
# AGGREGATE METRICS
# ─────────────────────────────────────────────
total_to   = sum(d["turnover"]    for d in kpi_data.values())
total_ggr  = sum(d["ggr"]         for d in kpi_data.values())
total_dep  = sum(d["deposits"]    for d in kpi_data.values())
total_wd   = sum(d["withdrawals"] for d in kpi_data.values())
max_users  = max(d["users"]       for d in kpi_data.values())
dep_wd_r   = total_dep / total_wd if total_wd else 0

to_list   = [kpi_data[p]["turnover"] / 1e6       for p in sorted_kpi]
ggr_list  = [kpi_data[p]["ggr"] / 1e6            for p in sorted_kpi]
pr_list   = [kpi_data[p]["payout_ratio"] * 100   for p in sorted_kpi]
dep_list  = [kpi_data[p]["deposits"] / 1e6       for p in sorted_kpi]
wd_list   = [kpi_data[p]["withdrawals"] / 1e6    for p in sorted_kpi]
cust_list = [kpi_data[p]["users"]                for p in sorted_kpi]
tk_list   = [kpi_data[p]["tickets"]              for p in sorted_kpi]
last_pr   = pr_list[-1]

# Badges
to_chg = (to_list[-1] - to_list[0]) / to_list[0] * 100 if len(to_list) >= 2 else 0
to_badge = f"↑ +{to_chg:.0f}%" if to_chg >= 0 else f"↓ {to_chg:.0f}%"
to_badge_cls = "up" if to_chg >= 0 else "down"
pr_badge_cls = "down" if last_pr > 78 else "up"
pr_badge_txt = f"{'⚠️ ' if last_pr > 78 else '✅ '}Son ay: {last_pr:.1f}%"

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
section("Əsas Göstəricilər")
cols = st.columns(5)
kpis = [
    ("Ümumi Dövriyyə",     f"₼{total_to/1e6:.1f}M",  f"{len(sorted_kpi)} ay kumulativ",       to_badge,    to_badge_cls, "green"),
    ("Ümumi GGR",          f"₼{total_ggr/1e6:.1f}M", f"Orta margin: {total_ggr/total_to*100:.1f}%", "↑ Artım tendensiyası", "up",     "blue"),
    ("Aktiv Müştəri (Pik)",f"{max_users:,}",          "Ən yüksək dəyər",                       f"↑ {cust_list[0]:,} → {cust_list[-1]:,}", "up", "orange"),
    ("Ümumi Depozit",      f"₼{total_dep/1e6:.1f}M",  f"Dep/Wd: {dep_wd_r:.2f}×",             "↑ Sağlam nisbət",    "up",   "yellow"),
    ("Son Ay Payout",      f"{last_pr:.1f}%",          "Benchmark: 77%",                        pr_badge_txt, pr_badge_cls, "red" if last_pr > 78 else "green"),
]
for col, (lbl, val, sub, bdg, bcls, clr) in zip(cols, kpis):
    with col:
        st.markdown(kpi_html(lbl, val, sub, bdg, bcls, clr), unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MONTHLY TREND CHARTS
# ─────────────────────────────────────────────
section("Aylıq Trend Analizi")

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="c-title">Dövriyyə (Turnover)</div>'
                '<div class="c-sub">AZN milyon · Son ay vurğulanır</div>',
                unsafe_allow_html=True)
    bar_clrs = [
        "rgba(16,217,138,0.85)" if i == len(to_list) - 1
        else "rgba(61,155,255,0.45)"
        for i in range(len(to_list))
    ]
    fig = bar_chart(months_short, to_list, bar_clrs, {"prefix": "₼", "suffix": "M"})
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    st.markdown('<div class="c-title">GGR &amp; Payout Ratio</div>'
                '<div class="c-sub">Yaşıl sütun: GGR · Narıncı xətt: Payout% · Benchmark: 77%</div>',
                unsafe_allow_html=True)
    fig2 = bar_line_chart(
        months_short, ggr_list, pr_list,
        "GGR (₼M)", "Payout %",
        "rgba(16,217,138,0.5)", C["orange"],
        y2_range=[68, 86],
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="c-title">Aktiv Müştəri Sayı</div>'
                '<div class="c-sub">Unikal oyuncu · aylıq</div>',
                unsafe_allow_html=True)
    fig3 = line_chart(months_short, cust_list, C["blue"])
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with c4:
    st.markdown('<div class="c-title">Depozit vs Çıxarış</div>'
                '<div class="c-sub">AZN milyon · Mavi: Depozit · Narıncı: Çıxarış</div>',
                unsafe_allow_html=True)
    fig4 = grouped_bar(
        months_short, dep_list, wd_list,
        "Depozit", "Çıxarış",
        "rgba(61,155,255,0.6)", "rgba(255,112,67,0.5)",
    )
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# MONTHLY TABLE
# ─────────────────────────────────────────────
section("Aylıq Tam Cədvəl")

best_ggr = max(kpi_data[p]["ggr"] for p in sorted_kpi)
rows_html = ""
for p in sorted_kpi:
    d    = kpi_data[p]
    pr   = d["payout_ratio"] * 100
    ggr  = d["ggr"] / 1e6
    dratio = d["deposits"] / d["withdrawals"] if d["withdrawals"] else 0
    pr_cls  = "vr" if pr > 79 else ("vy" if pr > 77.5 else "vg")
    ggr_cls = "vr" if ggr < 5  else ("vy" if ggr < 6   else "vg")
    best    = d["ggr"] == best_ggr
    row_bg  = f"background:rgba(16,217,138,0.05)" if best else ""
    name_style = f"color:{C['green']}" if best else f"color:{C['white']}"
    rows_html += f"""
    <tr style="{row_bg}">
        <td style="{name_style}">{d['label']}{'&nbsp;🏆' if best else ''}</td>
        <td>{d['users']:,}</td>
        <td>₼{d['turnover']/1e6:.2f}M</td>
        <td class="{ggr_cls}">₼{ggr:.2f}M</td>
        <td class="{pr_cls}">{pr:.1f}%</td>
        <td>₼{d['deposits']/1e6:.2f}M</td>
        <td>₼{d['withdrawals']/1e6:.2f}M</td>
        <td class="{'vg' if dratio>=1.8 else 'vy'}">{dratio:.2f}×</td>
        <td>{d['tickets']:,}</td>
        <td>₼{d['turnover']/d['users']:,.0f}</td>
    </tr>"""

st.markdown(f"""
<div style="background:{C['card']};border:1px solid {C['border']};border-radius:12px;
            overflow:hidden;overflow-x:auto">
<table class="styled-table">
<thead><tr>
    <th>Ay</th><th>Müştəri</th><th>Dövriyyə</th><th>GGR</th>
    <th>Payout%</th><th>Depozit</th><th>Çıxarış</th>
    <th>Dep/Wd</th><th>Ticketlər</th><th>Ort. TO/Müştəri</th>
</tr></thead>
<tbody>{rows_html}</tbody>
</table></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RETENTION
# ─────────────────────────────────────────────
if len(sorted_kpi) >= 2:
    section("Müştəri Saxlanılması — Retention Analizi")

    ret_data = []
    for i in range(len(sorted_kpi) - 1):
        p1, p2 = sorted_kpi[i], sorted_kpi[i + 1]
        u1 = set(kpi_users.get(p1, pd.DataFrame()).get("user_id", pd.Series()).values)
        u2 = set(kpi_users.get(p2, pd.DataFrame()).get("user_id", pd.Series()).values)
        if not u1:
            continue
        retained = u1 & u2
        rate  = len(retained) / len(u1) * 100
        new_u = len(u2 - u1)
        churn = len(u1 - u2)
        short = (f"{kpi_data[p1]['label'].split()[0][:3]}→"
                 f"{kpi_data[p2]['label'].split()[0][:3]}")
        ret_data.append(dict(label=short, rate=rate, new=new_u, churn=churn))

    n_cols = min(len(ret_data), 8)
    ret_cols = st.columns(n_cols) if n_cols > 0 else []
    for i, rd in enumerate(ret_data[:n_cols]):
        pct_clr = (C["green"] if rd["rate"] >= 85
                   else C["yellow"] if rd["rate"] >= 82
                   else C["orange"])
        border = (f"border-color:rgba(240,62,62,0.35)"
                  if rd["churn"] > rd["new"] else "")
        with ret_cols[i]:
            st.markdown(f"""
            <div class="ret-card" style="{border}">
                <div class="ret-per">{rd['label']}</div>
                <div class="ret-pct" style="color:{pct_clr}">{rd['rate']:.1f}%</div>
                <div class="ret-new">+{rd['new']:,} yeni</div>
                <div class="ret-churn">−{rd['churn']:,} çıxdı</div>
            </div>""", unsafe_allow_html=True)

    if ret_data:
        rc1, rc2 = st.columns(2)
        rl = [r["label"] for r in ret_data]
        rr = [r["rate"]  for r in ret_data]
        pclrs = [C["green"] if v >= 85 else (C["yellow"] if v >= 82 else C["orange"])
                 for v in rr]

        with rc1:
            st.markdown('<div class="c-title">Retention Faizi Trendi</div>',
                        unsafe_allow_html=True)
            fig_r = go.Figure(go.Scatter(
                x=rl, y=rr,
                line=dict(color=C["green"], width=2.5),
                mode="lines+markers",
                marker=dict(size=7, color=pclrs),
                fill="tozeroy", fillcolor="rgba(16,217,138,0.07)",
            ))
            layout_r = {**PL, "height": 220,
                        "yaxis": {**PL.get("yaxis", {}), "range": [72, 93],
                                  "ticksuffix": "%"}}
            fig_r.update_layout(**layout_r, showlegend=False)
            st.plotly_chart(fig_r, use_container_width=True,
                            config={"displayModeBar": False})

        with rc2:
            st.markdown('<div class="c-title">Yeni Müştəri vs Churn</div>',
                        unsafe_allow_html=True)
            fig_ch = go.Figure()
            fig_ch.add_trace(go.Bar(x=rl, y=[r["new"]   for r in ret_data],
                                    name="Yeni Müştəri",
                                    marker_color="rgba(16,217,138,0.55)",
                                    marker_line_width=0))
            fig_ch.add_trace(go.Bar(x=rl, y=[r["churn"] for r in ret_data],
                                    name="Churn",
                                    marker_color="rgba(255,112,67,0.5)",
                                    marker_line_width=0))
            layout_ch = {**PL, "height": 220, "barmode": "group",
                         "legend": dict(orientation="h", y=1.12,
                                        bgcolor="rgba(0,0,0,0)")}
            fig_ch.update_layout(**layout_ch, showlegend=True)
            st.plotly_chart(fig_ch, use_container_width=True,
                            config={"displayModeBar": False})

# ─────────────────────────────────────────────
# CUSTOMER VALUE (PARETO) — latest month
# ─────────────────────────────────────────────
latest_p = sorted_kpi[-1]
if latest_p in kpi_users and not kpi_users[latest_p].empty:
    section(f"Müştəri Dəyər Analizi — {kpi_data[latest_p]['label']}")
    udf = kpi_users[latest_p].copy()
    total_to_m = udf["turnover"].sum()

    if total_to_m > 0:
        n = len(udf)
        top1  = udf.nlargest(max(1, int(n * 0.01)), "turnover")
        top5  = udf.nlargest(max(1, int(n * 0.05)), "turnover")
        top10 = udf.nlargest(max(1, int(n * 0.10)), "turnover")
        bot50 = udf.nsmallest(max(1, int(n * 0.50)), "turnover")
        low   = udf[udf["turnover"] < 100]

        pct1   = top1["turnover"].sum()  / total_to_m * 100
        pct5   = top5["turnover"].sum()  / total_to_m * 100
        pct10  = top10["turnover"].sum() / total_to_m * 100
        pct_b  = bot50["turnover"].sum() / total_to_m * 100
        pct_lw = len(low) / n * 100
        avg_to = udf["turnover"].mean()
        med_to = udf["turnover"].median()

        bars = [
            (f"Top 1% — {len(top1):,} nəfər",   pct1,   C["red"]),
            (f"Top 5% — {len(top5):,} nəfər",   pct5,   C["orange"]),
            (f"Top 10% — {len(top10):,} nəfər", pct10,  C["yellow"]),
            (f"Bottom 50% — {len(bot50):,} nəfər", pct_b, C["dim"]),
            (f"<₼100 TO — {len(low):,} nəfər",  pct_lw, C["border"]),
        ]
        bars_html = "".join(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:11px">
            <span style="font-size:13px;color:{C['light']};font-weight:500;width:210px;flex-shrink:0">{lbl}</span>
            <div style="flex:1;height:10px;background:{C['card2']};border-radius:5px;overflow:hidden">
                <div style="width:{min(pct,100):.1f}%;height:100%;background:{clr};border-radius:5px"></div>
            </div>
            <span style="font-family:'Outfit',sans-serif;font-weight:700;font-size:14px;
                         color:{clr};width:50px;text-align:right">{pct:.1f}%</span>
        </div>""" for lbl, pct, clr in bars)

        pc1, pc2 = st.columns([3, 2])
        with pc1:
            st.markdown(f"""
            <div style="background:rgba(240,62,62,0.04);border:1px solid rgba(240,62,62,0.3);
                        border-radius:12px;padding:24px">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:18px">
                    <span style="font-size:18px">⚠️</span>
                    <div style="font-family:'Outfit',sans-serif;font-size:16px;font-weight:700;
                                color:{C['white']}">KRİTİK: Müştəri Konsentrasiya Riski</div>
                </div>
                {bars_html}
                <div style="display:flex;gap:20px;margin-top:18px;padding:14px;
                            background:{C['card']};border-radius:8px">
                    <div>
                        <div style="font-size:11px;color:{C['muted']};font-weight:600;
                                    text-transform:uppercase;letter-spacing:.06em">Orta TO</div>
                        <div style="font-family:'Outfit',sans-serif;font-size:20px;
                                    font-weight:800;color:{C['white']}">₼{avg_to:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size:11px;color:{C['muted']};font-weight:600;
                                    text-transform:uppercase;letter-spacing:.06em">Median TO</div>
                        <div style="font-family:'Outfit',sans-serif;font-size:20px;
                                    font-weight:800;color:{C['yellow']}">₼{med_to:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size:11px;color:{C['muted']};font-weight:600;
                                    text-transform:uppercase;letter-spacing:.06em">Fərq</div>
                        <div style="font-family:'Outfit',sans-serif;font-size:20px;
                                    font-weight:800;color:{C['red']}">{avg_to/med_to:.1f}×</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        with pc2:
            st.markdown('<div class="c-title">Dövriyyə Paylanması</div>'
                        '<div class="c-sub">Pareto vizualizasiyası</div>',
                        unsafe_allow_html=True)
            fig_p = donut_chart(
                [f"Top 1% ({len(top1):,})",
                 f"2–5% ({len(top5)-len(top1):,})",
                 f"6–10% ({len(top10)-len(top5):,})",
                 f"11–50% ({int(n*0.5)-len(top10):,})",
                 f"Bottom 50% ({len(bot50):,})"],
                [pct1, pct5 - pct1, pct10 - pct5,
                 100 - pct10 - pct_b, pct_b],
                [C["red"], C["orange"], C["yellow"], C["blue"], C["dim"]],
            )
            st.plotly_chart(fig_p, use_container_width=True,
                            config={"displayModeBar": False})

# ─────────────────────────────────────────────
# GGR RISK — latest month
# ─────────────────────────────────────────────
if latest_p in kpi_users:
    udf = kpi_users[latest_p].copy()
    pos = udf[udf["ggr"] > 0]
    neg = udf[udf["ggr"] <= 0]
    over100 = udf[udf["payout_ratio"] > 1.0]

    if len(neg) > 0:
        section(f"Risk Analizi — {kpi_data[latest_p]['label']}")
        rr1, rr2, rr3 = st.columns(3)

        pos_pct = len(pos) / len(udf) * 100
        neg_pct = len(neg) / len(udf) * 100

        with rr1:
            st.markdown(f"""
            <div style="background:{C['card']};border:1px solid {C['border']};
                        border-radius:12px;padding:22px;height:100%">
                <div style="font-family:'Outfit',sans-serif;font-size:15px;
                            font-weight:700;margin-bottom:16px">GGR Risk Profili</div>
                <div style="margin-bottom:12px">
                    <div style="font-size:12px;color:{C['muted']};margin-bottom:5px">
                        Müsbət GGR — {pos_pct:.1f}% müştəri</div>
                    <div style="display:flex;align-items:center;gap:10px">
                        <div style="flex:1;height:10px;background:{C['card2']};border-radius:5px">
                            <div style="width:{pos_pct:.0f}%;height:100%;
                                        background:{C['green']};border-radius:5px"></div>
                        </div>
                        <span style="font-family:'Outfit',sans-serif;font-weight:700;
                                     color:{C['green']}">₼{pos['ggr'].sum()/1000:,.0f}K</span>
                    </div>
                </div>
                <div>
                    <div style="font-size:12px;color:{C['muted']};margin-bottom:5px">
                        Mənfi GGR — {neg_pct:.1f}% müştəri</div>
                    <div style="display:flex;align-items:center;gap:10px">
                        <div style="flex:1;height:10px;background:{C['card2']};border-radius:5px">
                            <div style="width:{neg_pct:.0f}%;height:100%;
                                        background:{C['red']};border-radius:5px"></div>
                        </div>
                        <span style="font-family:'Outfit',sans-serif;font-weight:700;
                                     color:{C['red']}">₼{neg['ggr'].sum()/1000:,.0f}K</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        with rr2:
            st.markdown('<div class="c-title">GGR Komponentləri</div>',
                        unsafe_allow_html=True)
            fig_rc = go.Figure(go.Bar(
                x=["Müsbət GGR", "Mənfi GGR"],
                y=[pos["ggr"].sum() / 1000, neg["ggr"].sum() / 1000],
                marker_color=["rgba(16,217,138,0.55)", "rgba(240,62,62,0.55)"],
                marker_line_color=[C["green"], C["red"]], marker_line_width=1.5,
            ))
            layout_rc = {**PL, "height": 200}
            fig_rc.update_layout(**layout_rc, showlegend=False)
            st.plotly_chart(fig_rc, use_container_width=True,
                            config={"displayModeBar": False})

        with rr3:
            st.markdown(f"""
            <div style="background:rgba(240,62,62,0.04);
                        border:1px solid rgba(240,62,62,0.35);
                        border-radius:12px;padding:22px;height:100%">
                <div style="font-size:22px;margin-bottom:8px">🚨</div>
                <div style="font-family:'Outfit',sans-serif;font-size:15px;
                            font-weight:700;margin-bottom:12px">Payout &gt;100% Müştərilər</div>
                <div style="font-family:'Outfit',sans-serif;font-size:28px;
                            font-weight:800;color:{C['red']};margin-bottom:4px">{len(over100):,}</div>
                <div style="font-size:12px;color:{C['muted']};margin-bottom:12px">
                    müştəri şirkətin ziyanına oynayır</div>
                <div style="font-size:13px;color:{C['light']};line-height:1.75">
                    Onların turnover-i:
                    <strong style="color:{C['white']}">₼{over100['turnover'].sum()/1e6:.2f}M</strong><br>
                    Neqativ GGR:
                    <strong style="color:{C['red']}">₼{over100['ggr'].sum()/1000:,.0f}K</strong>
                </div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FREEBET
# ─────────────────────────────────────────────
if fb_data:
    sorted_fb   = sorted(fb_data.keys())
    fb_m_short  = [fb_data[p]["label"].split()[0][:3] for p in sorted_fb]
    fb_given    = [fb_data[p]["given"]        / 1000 for p in sorted_fb]
    fb_pr       = [fb_data[p]["payout_ratio"] * 100  for p in sorted_fb]
    fb_usage    = [(fb_data[p]["used"] / fb_data[p]["given"] * 100
                    if fb_data[p]["given"] > 0 else 0) for p in sorted_fb]

    section("Freebet Analizi")

    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown('<div class="c-title">Freebet Verilmiş Məbləğ</div>'
                    '<div class="c-sub">₼K · Son ay vurğulanır</div>',
                    unsafe_allow_html=True)
        fb_clrs = ["rgba(255,193,61,0.85)" if i == len(fb_given) - 1
                   else "rgba(255,112,67,0.45)" for i in range(len(fb_given))]
        fig_fb = bar_chart(fb_m_short, fb_given, fb_clrs, {"prefix": "₼", "suffix": "K"})
        st.plotly_chart(fig_fb, use_container_width=True,
                        config={"displayModeBar": False})

    with fc2:
        st.markdown('<div class="c-title">Freebet Payout % &amp; İstifadə %</div>'
                    '<div class="c-sub">Narıncı: Payout · Mavi: İstifadə dərəcəsi</div>',
                    unsafe_allow_html=True)
        fig_fb2 = go.Figure()
        fig_fb2.add_trace(go.Scatter(
            x=fb_m_short, y=fb_pr, name="Payout %",
            line=dict(color=C["orange"], width=2.5), mode="lines+markers",
            marker=dict(size=6)))
        fig_fb2.add_trace(go.Scatter(
            x=fb_m_short, y=fb_usage, name="İstifadə %",
            line=dict(color=C["blue"], width=2.5), mode="lines+markers",
            marker=dict(size=6)))
        layout_fb2 = {**PL, "height": 260, "showlegend": True,
                      "legend": dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)")}
        fig_fb2.update_layout(**layout_fb2)
        st.plotly_chart(fig_fb2, use_container_width=True,
                        config={"displayModeBar": False})

    # Tier breakdown — latest FB month
    latest_fb = sorted_fb[-1]
    if latest_fb in fb_users_data and not fb_users_data[latest_fb].empty:
        section(f"Tier Üzrə Freebet — {fb_data[latest_fb]['label']}")
        fb_df = fb_users_data[latest_fb].copy()
        tier_s = (fb_df.groupby("tier")
                  .agg(count=("user_id", "count"), given=("given", "sum"))
                  .reset_index())
        tier_s["per_user"] = tier_s["given"] / tier_s["count"]
        tier_s = tier_s[tier_s["given"] > 0].sort_values("per_user", ascending=False)

        if not tier_s.empty:
            t_colors = [TIER_COLORS.get(t, C["dim"]) for t in tier_s["tier"]]
            fig_tier = go.Figure(go.Bar(
                x=tier_s["tier"], y=tier_s["per_user"],
                marker_color=t_colors, marker_line_width=0,
                text=[f"₼{v:,.0f}" for v in tier_s["per_user"]],
                textposition="outside",
                textfont=dict(color=C["muted"], size=11),
                customdata=tier_s["count"],
                hovertemplate="<b>%{x}</b><br>Nəfər başına: ₼%{y:,.0f}<br>"
                              "Müştəri sayı: %{customdata}<extra></extra>",
            ))
            layout_t = {**PL, "height": 300}
            fig_tier.update_layout(**layout_t, showlegend=False)
            st.plotly_chart(fig_tier, use_container_width=True,
                            config={"displayModeBar": False})

# ─────────────────────────────────────────────
# INSIGHTS
# ─────────────────────────────────────────────
section("Güclü Tərəflər")
ig1, ig2, ig3 = st.columns(3)
ins_pos = [
    ("🚀", "Sürətli Böyümə",
     f"OMT keçidindən <strong>{len(sorted_kpi)} ayda</strong> müştəri sayı "
     f"<span class='hi'>{cust_list[0]:,}</span>-dən "
     f"<span class='hi'>{cust_list[-1]:,}</span>-ə çatdı. "
     f"Dövriyyə ₼{to_list[0]:.1f}M-dan ₼{to_list[-1]:.1f}M-a artdı."),
    ("💰", "Sağlam Depozit Nisbəti",
     f"Depozit/Çıxarış nisbəti <span class='hi'>{dep_wd_r:.2f}×</span>. "
     "Müştərilər qoyduqlarından az çıxarır — "
     "<strong>sağlam müştəri davranışı</strong>."),
    ("📈", "Ticket Sayı Artımı",
     f"Aylıq ticket sayı <span class='hi'>{tk_list[0]:,}</span>-dən "
     f"<span class='hi'>{tk_list[-1]:,}</span>-ə çatdı. "
     "Oyunçular <strong>daha aktiv</strong> mərc edir."),
]
for col, (icon, title, text) in zip([ig1, ig2, ig3], ins_pos):
    with col:
        st.markdown(
            f'<div class="insight pos"><div class="insight-icon">{icon}</div>'
            f'<h4>{title}</h4><p>{text}</p></div>',
            unsafe_allow_html=True,
        )

section("Zəif Tərəflər &amp; Risklər")
iw1, iw2, iw3 = st.columns(3)
ins_neg = [
    ("⚠️", "Payout Ratio",
     f"Son ay payout: <span class='dng'>{last_pr:.1f}%</span>. Benchmark 77%. "
     + ("Həddindən yuxarıdır — <strong>limit management dərhal lazımdır</strong>."
        if last_pr > 78 else "Hələlik normal aralıqdadır, izlənilməlidir.")),
    ("🔄", "Churn Artımı",
     "Aylıq churn artım tendensiyası göstərir. "
     "<strong>Win-Back kampaniyası</strong> — 100% depozit bonusu + "
     "tier-based cap + 3× rollover modeli tətbiq edilməlidir."),
    ("💎", "VIP Konsentrasiya Riski",
     "Top 1% müştəri aylıq dövriyyənin <span class='dng'>50%+</span>-ini yaradır. "
     "Bu müştərilər üçün <strong>şəxsi hesab meneceri</strong> və "
     "xüsusi freebet proqramı vacibdir."),
]
for col, (icon, title, text) in zip([iw1, iw2, iw3], ins_neg):
    with col:
        st.markdown(
            f'<div class="insight alert"><div class="insight-icon">{icon}</div>'
            f'<h4>{title}</h4><p>{text}</p></div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:60px;padding-top:20px;border-top:1px solid {C['border']};
            text-align:center;font-size:11px;color:{C['dim']};
            letter-spacing:.07em;text-transform:uppercase">
    Etopaz Platform Analytics &nbsp;·&nbsp;
    OMT Dövrü &nbsp;·&nbsp; Mart 2026 &nbsp;·&nbsp; Nicat Dünyamaliyev
</div>
""", unsafe_allow_html=True)
