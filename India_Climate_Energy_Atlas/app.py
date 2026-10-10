from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from atlas.analysis import coverage_table

st.set_page_config(page_title="India Climate & Energy Atlas", page_icon="🌏", layout="wide")

# ---------- Theme / page shell ----------
st.markdown("""
<style>
    .block-container {padding-top: 1.4rem; padding-bottom: 2.4rem; max-width: 1450px;}
    [data-testid="stMetric"] {background: linear-gradient(135deg, rgba(32,91,111,.12), rgba(62,130,119,.08)); padding: 18px 18px 14px; border: 1px solid rgba(90,130,140,.22); border-radius: 14px;}
    [data-testid="stMetricLabel"] {font-size: .88rem;}
    .hero {padding: 1.3rem 1.5rem; border-radius: 18px; background: linear-gradient(120deg, #102f3a 0%, #1b5962 55%, #397c70 100%); color: white; margin-bottom: 1rem;}
    .hero h1 {color:white; margin:0; font-size:2.1rem;}
    .hero p {color:#e1eff0; margin:.45rem 0 0; font-size:1rem;}
    .small-muted {color: #7b8790; font-size: .82rem;}
    .finding {padding: .8rem 1rem; border-left: 4px solid #3c897d; background: rgba(60,137,125,.08); border-radius: 6px; margin: .45rem 0;}
</style>
<div class="hero">
  <h1>🌏 India Climate &amp; Energy Atlas</h1>
  <p>Evidence-led exploration of development, electricity access, renewable energy and emissions.</p>
</div>
""", unsafe_allow_html=True)
st.caption("World Bank Indicators API · Observational country-level data · Descriptive analysis, not causal proof")

DATA_PATH = ROOT / "data" / "processed" / "world_bank_panel.csv"
uploaded = st.sidebar.file_uploader("Use a panel CSV", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
    data_source = "Uploaded CSV"
elif DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
    data_source = "Local World Bank API download"
else:
    st.warning("No real-data panel found yet. Fetch observations first; this app does not create synthetic values.")
    st.code("python3 scripts/fetch_data.py --start 2000 --end 2023\npython3 scripts/analyze.py\npython3 -m streamlit run app.py")
    st.markdown("[World Bank API](https://api.worldbank.org/v2/) · [Indicator catalogue](https://data.worldbank.org/indicator)")
    st.stop()

id_cols = {"country_code", "country", "year"}
if not id_cols.issubset(df.columns):
    st.error(f"Dataset must contain: {', '.join(sorted(id_cols))}")
    st.stop()
df["year"] = pd.to_numeric(df["year"], errors="coerce")
metrics = [c for c in df.columns if c not in id_cols and pd.api.types.is_numeric_dtype(pd.to_numeric(df[c], errors="coerce"))]
for metric in metrics:
    df[metric] = pd.to_numeric(df[metric], errors="coerce")
if not metrics:
    st.error("No numeric indicator columns were found.")
    st.stop()

countries = sorted(df["country_code"].dropna().astype(str).unique().tolist())
default_country = "IND" if "IND" in countries else countries[0]
st.sidebar.header("Explore")
country = st.sidebar.selectbox("Focus country", countries, index=countries.index(default_country))
metric_default = "GDP per capita (constant 2015 US$)"
metric = st.sidebar.selectbox("Primary indicator", metrics, index=metrics.index(metric_default) if metric_default in metrics else 0)
available_years = sorted(df["year"].dropna().astype(int).unique().tolist())
if len(available_years) >= 2:
    year_range = st.sidebar.slider("Analysis year range", min_value=min(available_years), max_value=max(available_years),
                                   value=(min(available_years), max(available_years)))
else:
    year_range = (available_years[0], available_years[0]) if available_years else (2000, 2023)
compare_default = [c for c in ["IND", "BGD", "CHN", "IDN", "LKA", "VNM"] if c in countries]
compare_countries = st.sidebar.multiselect("Countries to compare", countries, default=compare_default or [country])
df_range = df[df["year"].between(year_range[0], year_range[1])].copy()
focus = df_range[df_range["country_code"] == country].sort_values("year")
metric_data = focus.dropna(subset=[metric])
country_name = str(focus["country"].dropna().iloc[0]) if focus["country"].notna().any() else country

# KPI row
vals = metric_data[["year", metric]].sort_values("year")
if not vals.empty:
    first, last = vals.iloc[0], vals.iloc[-1]
    change = ((last[metric] / first[metric]) - 1) * 100 if first[metric] != 0 else np.nan
else:
    first = last = None
    change = np.nan
all_years = int(metric_data["year"].nunique())
c1, c2, c3, c4 = st.columns(4)
c1.metric("Focus country", country_name)
c2.metric("Observed points", f"{len(metric_data):,}")
c3.metric("Coverage window", f"{int(vals.year.min())}–{int(vals.year.max())}" if not vals.empty else "No observations")
c4.metric("Endpoint change", f"{change:+.1f}%" if pd.notna(change) else "N/A", help="First and last available observations within the selected range; not necessarily adjacent years.")

tab_overview, tab_compare, tab_relationships, tab_quality = st.tabs([
    "📈 Overview", "🌐 Country comparison", "🔬 Relationships", "🧪 Data quality"
])

with tab_overview:
    left, right = st.columns([2.1, 1])
    with left:
        st.subheader("Indicator trajectory")
        if vals.empty:
            st.info("No observations for this country, indicator and year range.")
        else:
            fig = px.line(vals, x="year", y=metric, markers=True,
                          labels={"year": "Year", metric: metric},
                          title=metric, template="plotly_white")
            fig.update_traces(line=dict(width=3), marker=dict(size=6))
            fig.update_layout(margin=dict(l=10, r=10, t=55, b=10), hovermode="x unified",
                              title_font_size=18, yaxis_title=metric)
            st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("What the data support")
        if not vals.empty:
            st.markdown(f'<div class="finding"><b>First observed value</b><br>{int(first["year"])}: {first[metric]:,.3g}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="finding"><b>Last observed value</b><br>{int(last["year"])}: {last[metric]:,.3g}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="finding"><b>Net endpoint change</b><br>{change:+.2f}%</div>' if pd.notna(change) else '<div class="finding">Endpoint change cannot be computed.</div>', unsafe_allow_html=True)
            st.caption("Endpoint change compares the first and last non-missing values. It does not describe every year in between.")
        else:
            st.info("Choose another indicator or year range.")
    st.subheader("Annual observations")
    st.dataframe(vals.rename(columns={"year":"Year", metric:"Value"}), use_container_width=True, hide_index=True)

with tab_compare:
    st.subheader("Compare selected countries")
    comp = df_range[df_range["country_code"].isin(compare_countries)].dropna(subset=[metric]).copy()
    if comp.empty:
        st.info("No observations in this selection.")
    else:
        fig = px.line(comp, x="year", y=metric, color="country", markers=False,
                      labels={"year":"Year", metric:metric, "country":"Country"}, template="plotly_white")
        fig.update_layout(hovermode="x unified", margin=dict(l=10,r=10,t=30,b=10), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
        endpoints = []
        for code, grp in comp.groupby("country_code"):
            grp = grp.sort_values("year")
            a, b = grp.iloc[0], grp.iloc[-1]
            pct = ((b[metric] / a[metric]) - 1) * 100 if a[metric] != 0 else np.nan
            endpoints.append({"Country": b["country"], "First year": int(a["year"]), "First value": a[metric],
                              "Last year": int(b["year"]), "Last value": b[metric],
                              "Endpoint change (%)": pct, "Observations": len(grp)})
        st.dataframe(pd.DataFrame(endpoints).sort_values("Endpoint change (%)", ascending=False, na_position="last"),
                     use_container_width=True, hide_index=True)
        st.caption("Country endpoint changes can cover different years when source series have different reporting coverage.")

with tab_relationships:
    st.subheader("Explore associations")
    numeric_metrics = [m for m in metrics if df_range[m].notna().sum() >= 3]
    if len(numeric_metrics) < 2:
        st.info("At least two indicators with three or more observations are needed.")
    else:
        r1, r2 = st.columns(2)
        with r1:
            x_metric = st.selectbox("X-axis indicator", numeric_metrics, index=0, key="x_metric")
        with r2:
            y_default = 1 if len(numeric_metrics) > 1 else 0
            y_metric = st.selectbox("Y-axis indicator", numeric_metrics, index=y_default, key="y_metric")
        rel = df_range[df_range["country_code"] == country][["year", x_metric, y_metric]].dropna()
        if len(rel) >= 3:
            corr = rel[x_metric].corr(rel[y_metric])
            fig = px.scatter(rel, x=x_metric, y=y_metric, hover_data=["year"], trendline="ols" if len(rel) >= 3 else None,
                             labels={"year":"Year"}, template="plotly_white",
                             title=f"{country_name}: {x_metric} vs {y_metric}")
            fig.update_layout(margin=dict(l=10,r=10,t=55,b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Pearson correlation (complete years)", f"{corr:.3f}", help=f"n = {len(rel)} complete year-pairs")
            st.caption(f"Computed from {len(rel)} complete annual pairs. Correlation is descriptive and does not establish causation; time trends may create spurious associations.")
        else:
            st.info("Fewer than three complete year-pairs for this indicator combination.")
        st.markdown("**Correlation matrix across countries (selected period)**")
        corr_df = df_range[df_range["country_code"].isin(compare_countries)].groupby("country_code")[numeric_metrics].mean(numeric_only=True)
        if len(corr_df.columns) >= 2 and len(corr_df) >= 3:
            matrix = corr_df.corr(min_periods=3)
            heat = px.imshow(matrix, text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="RdBu",
                             origin="lower", aspect="auto", title="Correlation of country-level mean indicators")
            heat.update_layout(margin=dict(l=10,r=10,t=55,b=10))
            st.plotly_chart(heat, use_container_width=True)
            st.caption("This matrix correlates country-level period averages, not annual changes. It is exploratory and can be confounded by country differences.")
        else:
            st.info("Not enough country-level data to calculate the matrix.")

with tab_quality:
    st.subheader("Coverage and missingness")
    coverage = coverage_table(df_range)
    st.dataframe(coverage, use_container_width=True, hide_index=True)
    coverage_plot = px.bar(coverage.sort_values("coverage_pct"), x="coverage_pct", y="indicator", orientation="h",
                           range_x=[0,100], labels={"coverage_pct":"Non-missing coverage (%)","indicator":"Indicator"},
                           title="Data availability by indicator", template="plotly_white")
    coverage_plot.update_layout(margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(coverage_plot, use_container_width=True)
    st.info("Missing observations remain missing. They are never silently converted to zero or interpolated.")
    st.subheader("Download the data used")
    st.download_button("Download current panel as CSV", df.to_csv(index=False).encode("utf-8"),
                       file_name="world_bank_panel.csv", mime="text/csv")
    st.subheader("Provenance")
    provenance_path = ROOT / "reports" / "data_provenance.json"
    if provenance_path.exists():
        try:
            st.json(json.loads(provenance_path.read_text()))
        except Exception:
            st.caption("Provenance file exists but could not be parsed.")
    else:
        st.caption("Run scripts/fetch_data.py to create a retrieval metadata file.")

st.divider()
st.markdown("**Source:** [World Bank Indicators API](https://api.worldbank.org/v2/) · [Indicator catalogue](https://data.worldbank.org/indicator)")
st.markdown('<p class="small-muted">Research note: values and coverage depend on each indicator’s published series. Use the indicator definitions and retrieval metadata when citing findings.</p>', unsafe_allow_html=True)
