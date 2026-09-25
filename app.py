
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from pathlib import Path
import html

st.set_page_config(page_title="NIOTA Ministry Of Housing Intelligence", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

BASE = Path(__file__).parent
regional = pd.read_csv(BASE / "data" / "regional_housing_summary.csv")
schemes = pd.read_csv(BASE / "data" / "scheme_housing_summary.csv")

st.markdown("""
<style>
.stApp {background: linear-gradient(180deg, #ffffff 0%, #f1f2f3 100%); color:#171717;}
.block-container {padding-top:1.3rem; max-width:1320px;}
h1,h2,h3 {letter-spacing:-.03em; color:#171717;}
.niota-label {color:#d95f02; font-size:13px; font-weight:800; letter-spacing:.24em; text-transform:uppercase;}
.hero-title {font-size:50px; line-height:1.02; font-weight:850; letter-spacing:-.045em; margin:8px 0 4px;}
.hero-sub {color:#5f6368; font-size:18px; max-width:980px;}
.pill {display:inline-block; padding:6px 11px; border-radius:999px; background:#fff1e8; border:1px solid #f4b183; color:#8b3d00; font-weight:700; font-size:12px; margin-right:6px;}
.clean-card {background:#fff; border:1px solid #e9eaec; border-radius:18px; padding:18px; box-shadow:0 10px 28px rgba(31,41,51,.06);}
.insight-card {background:linear-gradient(135deg,#fff 0%,#fff4ec 100%); border:1px solid #f4b183; border-radius:18px; padding:20px; box-shadow:0 10px 28px rgba(217,95,2,.08);}
.small-muted {color:#5f6368; font-size:13px;}
div[data-testid="stMetric"] {background:#fff; border:1px solid #e9eaec; border-radius:16px; padding:14px 16px; box-shadow:0 8px 22px rgba(31,41,51,.04);}
section[data-testid="stSidebar"] {background:#171717; border-right:4px solid #d95f02;}
section[data-testid="stSidebar"] * {color:#fff !important;}
section[data-testid="stSidebar"] [data-testid="stRadio"] label {padding:8px 10px; border-radius:6px;}
button[kind="primary"] {background:#171717 !important; border-color:#171717 !important;}
</style>
""", unsafe_allow_html=True)

def fmt_int(x):
    return f"{int(round(x)):,}"

def map_metric_label(metric):
    return {
        "allocated": "Allocated lots",
        "approval_rate_pct": "Approval rate",
        "pending_backlog": "Pending backlog",
        "avg_processing_days": "Processing speed",
        "allocation_rate_pct": "Allocation rate"
    }.get(metric, metric)

def metric_color(value, metric):
    vals = regional[metric]
    q1, q2, q3 = vals.quantile([0.25, 0.5, 0.75])
    if metric in ["pending_backlog", "avg_processing_days"]:
        if value >= q3:
            return "#c84b31"
        if value >= q2:
            return "#e7a83b"
        if value >= q1:
            return "#f2d17d"
        return "#2e9b67"
    else:
        if value >= q3:
            return "#1e8e5a"
        if value >= q2:
            return "#9bcb78"
        if value >= q1:
            return "#f2d17d"
        return "#e7a83b"

def make_guyana_svg(metric="allocated", selected_region=4):
    # Stylized presentation map for demo purposes. Region labels and hover details included.
    region_polys = {
        1: "90,30 205,38 230,145 185,220 110,200 70,115",
        2: "70,115 110,200 95,300 35,300 28,215",
        3: "95,300 185,290 220,365 175,440 85,410 35,300",
        4: "185,290 300,275 335,350 285,425 220,365",
        5: "230,145 335,155 300,275 185,290 185,220",
        6: "335,155 445,210 435,340 335,350 300,275",
        7: "205,38 355,25 420,100 335,155 230,145",
        8: "355,25 455,55 520,160 445,210 420,100",
        9: "445,210 555,310 525,455 435,340",
        10:"285,425 435,340 525,455 490,560 335,545 175,440"
    }
    label_positions = {
        1: (142,116), 2: (70,250), 3: (126,356), 4: (266,348), 5: (255,220),
        6: (384,270), 7: (320,94), 8: (442,128), 9: (492,335), 10: (350,465)
    }
    rows = regional.set_index("region_no").to_dict("index")
    items = []
    for rno, pts in region_polys.items():
        row = rows[rno]
        fill = metric_color(row[metric], metric)
        stroke = "#111827" if rno == selected_region else "#ffffff"
        stroke_width = "4" if rno == selected_region else "2"
        title = (
            f"Region {rno} — {row['region']}\n"
            f"Applications: {fmt_int(row['applications'])}\n"
            f"Approved: {fmt_int(row['approved'])}\n"
            f"Allocated: {fmt_int(row['allocated'])}\n"
            f"Pending: {fmt_int(row['pending_backlog'])}\n"
            f"Processing: {row['avg_processing_days']} days"
        )
        label_x, label_y = label_positions[rno]
        region_name = row["region"]
        region_name = region_name.replace("Essequibo Islands-West Demerara", "Essequibo Is.-W. Dem.")
        region_name = region_name.replace("Upper Takutu-Upper Essequibo", "Upper Takutu-Essequibo")
        items.append(f"""
        <polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="0.98">
          <title>{html.escape(title)}</title>
        </polygon>
        <text x="{label_x}" y="{label_y}" text-anchor="middle" class="region-no">R{rno}</text>
        <text x="{label_x}" y="{label_y + 17}" text-anchor="middle" class="region-name">{html.escape(region_name)}</text>
        """)
    svg = f"""
    <div style="background:#fff;border:1px solid #e7e8ea;border-radius:20px;padding:18px;box-shadow:0 10px 26px rgba(31,41,51,.06);">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:10px;">
        <div>
          <div style="font-size:12px;font-weight:800;color:#b88a2c;letter-spacing:.18em;text-transform:uppercase;">Guyana regional map</div>
          <div style="font-size:23px;font-weight:850;color:#1f2933;line-height:1.1;">Color view: {html.escape(map_metric_label(metric))}</div>
        </div>
        <div style="font-size:12px;color:#6b7280;text-align:right;max-width:280px;">Region names are shown directly on the map. Hover over any region for details.</div>
      </div>
      <svg viewBox="0 0 610 610" width="100%" height="620" role="img" aria-label="Stylized map of Guyana regions">
        <style>
          .region-no {{ font: 800 16px Arial, sans-serif; fill: #111827; pointer-events:none; }}
          .region-name {{ font: 700 10px Arial, sans-serif; fill: #111827; pointer-events:none; }}
          polygon {{ transition: opacity .15s ease; }}
          polygon:hover {{ opacity:.82; filter: drop-shadow(0px 5px 5px rgba(0,0,0,.18)); }}
          .outline {{ fill:none; stroke:#111827; stroke-width:3; opacity:.14; }}
        </style>
        <path d="M90 30 L355 25 L455 55 L520 160 L555 310 L525 455 L490 560 L335 545 L85 410 L28 215 Z" class="outline"/>
        {''.join(items)}
      </svg>
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:4px;">
        <span style="font-size:12px;color:#1e8e5a;font-weight:800;">■ Strong / high</span>
        <span style="font-size:12px;color:#f2d17d;font-weight:800;">■ Moderate</span>
        <span style="font-size:12px;color:#e7a83b;font-weight:800;">■ Watch</span>
        <span style="font-size:12px;color:#c84b31;font-weight:800;">■ Pressure / delay</span>
      </div>
    </div>
    """
    return svg

def answer_question(q):
    top_alloc = regional.sort_values("allocated", ascending=False).iloc[0]
    top_backlog = regional.sort_values("pending_backlog", ascending=False).iloc[0]
    fastest = regional.sort_values("avg_processing_days").iloc[0]
    slowest = regional.sort_values("avg_processing_days", ascending=False).iloc[0]
    r4 = schemes[schemes["region"] == "Demerara-Mahaica"].copy()
    r4_pressure = r4.sort_values("pending_backlog", ascending=False).iloc[0]
    r4_ready = r4.sort_values("infrastructure_ready_pct", ascending=False).iloc[0]
    if "most house lot allocations" in q:
        return f"Region {int(top_alloc.region_no)} — {top_alloc.region} has the highest number of allocated lots, with {fmt_int(top_alloc.allocated)} allocations. It also has a large remaining backlog, so demand management is still important."
    if "highest backlog" in q:
        return f"Region {int(top_backlog.region_no)} — {top_backlog.region} has the highest pending backlog, with {fmt_int(top_backlog.pending_backlog)} applicants still waiting."
    if "processing applications fastest" in q:
        return f"Region {int(fastest.region_no)} — {fastest.region} is processing fastest, averaging {fastest.avg_processing_days:.0f} days. It can be compared against slower regions such as Region {int(slowest.region_no)}."
    if "Region 4" in q:
        return f"Within Region 4, the largest pressure point is {r4_pressure.scheme_area}, with {fmt_int(r4_pressure.pending_backlog)} pending applications. The strongest readiness signal is {r4_ready.scheme_area}, with {r4_ready.infrastructure_ready_pct:.0f}% infrastructure readiness."
    return f"Management should focus where high demand, backlog, and slow processing overlap. In this demo, Region {int(top_backlog.region_no)} has the largest backlog and Region {int(slowest.region_no)} has the slowest processing."

st.markdown('<div class="niota-label">NIOTA LABS</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Ministry Of Housing Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">A clean demonstration of how housing applications, approvals, house lot allocations, backlog, and regional readiness can become decision intelligence.</div>', unsafe_allow_html=True)
st.markdown('<span class="pill">Demo data only</span><span class="pill">Guyana Regions 1–10</span><span class="pill">6–7 minute walkthrough</span>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="niota-label">NIOTA LABS</div>', unsafe_allow_html=True)
st.sidebar.markdown("## Ministry Of Housing Intelligence")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Regional Map", "Region 4 Deep Dive", "Ask NIOTA", "Management Brief"],
    label_visibility="collapsed"
)

total_app = regional["applications"].sum()
total_approved = regional["approved"].sum()
total_allocated = regional["allocated"].sum()
total_pending = regional["pending_backlog"].sum()
approval_rate = total_approved / total_app * 100
allocation_rate = total_allocated / total_app * 100
avg_days = np.average(regional["avg_processing_days"], weights=regional["applications"])

if page == "Overview":
    st.markdown("### Executive overview")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Applications", fmt_int(total_app))
    c2.metric("Approved", fmt_int(total_approved), f"{approval_rate:.1f}%")
    c3.metric("Allocated", fmt_int(total_allocated), f"{allocation_rate:.1f}%")
    c4.metric("Pending backlog", fmt_int(total_pending))
    c5.metric("Avg. processing", f"{avg_days:.0f} days")
    c6.metric("Mortgage-ready", fmt_int(regional["mortgage_ready"].sum()))

    left, right = st.columns([1.35, .9])
    with left:
        st.markdown("#### Allocated lots by region")
        st.bar_chart(
            regional.sort_values("allocated").set_index("region")[["allocated"]],
            color="#d95f02"
        )
    with right:
        top_region = regional.sort_values("allocated", ascending=False).iloc[0]
        backlog_region = regional.sort_values("pending_backlog", ascending=False).iloc[0]
        st.markdown(f"""
        <div class="insight-card">
            <div class="niota-label">Executive signal</div>
            <h3 style="margin-top:8px;">Where the story begins</h3>
            <p><b>Region {int(top_region.region_no)} — {top_region.region}</b> leads with <b>{fmt_int(top_region.allocated)}</b> house lots allocated.</p>
            <p><b>Region {int(backlog_region.region_no)} — {backlog_region.region}</b> has the largest pending backlog with <b>{fmt_int(backlog_region.pending_backlog)}</b> applicants still waiting.</p>
            <p class="small-muted">This uses fictional data for demo purposes only.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Regional Map":
    st.markdown("### Guyana regional map")
    st.caption("Use the selector to change what the colors mean. Region names show directly on the map.")
    metric_choice = st.selectbox(
        "Color the map by",
        ["allocated", "approval_rate_pct", "pending_backlog", "avg_processing_days", "allocation_rate_pct"],
        format_func=map_metric_label,
        index=0
    )
    selected = st.selectbox(
        "Selected region",
        regional["region_no"].tolist(),
        format_func=lambda r: f"Region {int(r)} — {regional.loc[regional.region_no == r, 'region'].iloc[0]}",
        index=3
    )
    map_col, detail_col = st.columns([1.25, .75])
    with map_col:
        components.html(make_guyana_svg(metric_choice, int(selected)), height=760, scrolling=False)
    with detail_col:
        row = regional[regional.region_no == selected].iloc[0]
        st.markdown(f"""
        <div class="clean-card">
            <div class="niota-label">Selected region</div>
            <h2>Region {int(row.region_no)} — {row.region}</h2>
            <p class="small-muted">Housing allocation snapshot</p>
            <hr style="border:0;border-top:1px solid #e5e7eb;margin:14px 0;">
            <p><b>Applications:</b> {fmt_int(row.applications)}</p>
            <p><b>Approved:</b> {fmt_int(row.approved)} ({row.approval_rate_pct:.1f}%)</p>
            <p><b>Allocated:</b> {fmt_int(row.allocated)} ({row.allocation_rate_pct:.1f}%)</p>
            <p><b>Pending backlog:</b> {fmt_int(row.pending_backlog)}</p>
            <p><b>Avg. processing:</b> {row.avg_processing_days:.0f} days</p>
            <p><b>Infrastructure readiness:</b> {row.infrastructure_ready_pct:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Region 4 Deep Dive":
    st.markdown("### Region 4 deep dive")
    st.caption("A closer look at Demerara-Mahaica, using illustrative area-level housing data.")
    r4 = schemes[schemes["region"] == "Demerara-Mahaica"].copy()
    a, b, c, d = st.columns(4)
    a.metric("Applications", fmt_int(r4["applications"].sum()))
    b.metric("Approved", fmt_int(r4["approved"].sum()))
    c.metric("Allocated", fmt_int(r4["allocated"].sum()))
    d.metric("Pending", fmt_int(r4["pending_backlog"].sum()))

    left, right = st.columns(2)
    with left:
        st.markdown("#### Pending backlog by area")
        st.bar_chart(r4.sort_values("pending_backlog").set_index("scheme_area")[["pending_backlog"]])
    with right:
        st.markdown("#### Infrastructure readiness")
        st.bar_chart(r4.sort_values("infrastructure_ready_pct").set_index("scheme_area")[["infrastructure_ready_pct"]])
    st.dataframe(r4[["scheme_area", "applications", "approved", "allocated", "pending_backlog", "avg_processing_days", "infrastructure_ready_pct", "note"]], use_container_width=True, hide_index=True)

elif page == "Ask NIOTA":
    st.markdown("### Ask NIOTA")
    st.caption("Pre-tested executive questions keep the launch demo smooth and predictable.")
    q = st.selectbox("Choose a question", [
        "Which region has the most house lot allocations?",
        "Which region has the highest backlog?",
        "Which region is processing applications fastest?",
        "Which areas in Region 4 are under the most pressure?",
        "Where should management focus next?"
    ])
    if st.button("Generate executive answer", type="primary", use_container_width=True):
        st.markdown(f"""
        <div class="insight-card">
            <div class="niota-label">NIOTA answer</div>
            <h3>{html.escape(q)}</h3>
            <p style="font-size:17px;line-height:1.55;">{html.escape(answer_question(q))}</p>
            <p class="small-muted">Production version: connect live databases, user permissions, audit trails, document workflows, and approved AI models.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("### Management brief")
    top_alloc = regional.sort_values("allocated", ascending=False).iloc[0]
    top_backlog = regional.sort_values("pending_backlog", ascending=False).iloc[0]
    fastest = regional.sort_values("avg_processing_days").iloc[0]
    slowest = regional.sort_values("avg_processing_days", ascending=False).iloc[0]
    r4_pressure = schemes[schemes["region"] == "Demerara-Mahaica"].sort_values("pending_backlog", ascending=False).iloc[0]
    st.markdown(f"""
    <div class="insight-card">
        <div class="niota-label">Executive brief</div>
        <h2>Housing allocation intelligence summary</h2>
        <p><b>National picture:</b> This demo tracks <b>{fmt_int(total_app)}</b> housing applications across Guyana’s 10 regions, with <b>{fmt_int(total_allocated)}</b> lots allocated and <b>{fmt_int(total_pending)}</b> applicants still pending.</p>
        <p><b>Allocation leader:</b> Region {int(top_alloc.region_no)} — {top_alloc.region} leads allocations with <b>{fmt_int(top_alloc.allocated)}</b> lots allocated.</p>
        <p><b>Backlog pressure:</b> Region {int(top_backlog.region_no)} — {top_backlog.region} has the largest backlog, with <b>{fmt_int(top_backlog.pending_backlog)}</b> pending applications.</p>
        <p><b>Processing signal:</b> Region {int(fastest.region_no)} is fastest at <b>{fastest.avg_processing_days:.0f} days</b>, while Region {int(slowest.region_no)} is slowest at <b>{slowest.avg_processing_days:.0f} days</b>.</p>
        <p><b>Region 4 focus:</b> {r4_pressure.scheme_area} has the largest Region 4 area backlog, with <b>{fmt_int(r4_pressure.pending_backlog)}</b> applicants still waiting.</p>
        <p><b>Management action:</b> Prioritize regions and schemes where high demand, slow processing, and infrastructure readiness gaps overlap.</p>
    </div>
    """, unsafe_allow_html=True)
    st.download_button("Download demo regional data", regional.to_csv(index=False), "niota_housing_regional_demo_data.csv", "text/csv", use_container_width=True)
