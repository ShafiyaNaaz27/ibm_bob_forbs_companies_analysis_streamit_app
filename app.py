import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fortune Company Performance Analysis",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Fortune Company Performance Analysis")
st.markdown("**Forbes 2000 Companies – 2026**")
st.markdown("---")

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    return df

df_raw = load_data("Forbes_2000_Companies_2026.csv")

# ── Section 1 – Raw data overview ─────────────────────────────────────────────
st.header("1. Dataset Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rows", df_raw.shape[0])
col2.metric("Total Columns", df_raw.shape[1])
col3.metric("Missing Values", int(df_raw.isnull().sum().sum()))
col4.metric("Duplicate Records", int(df_raw.duplicated().sum()))

with st.expander("View raw column names and dtypes"):
    st.dataframe(
        pd.DataFrame({"Column": df_raw.columns, "Dtype": df_raw.dtypes.values}),
        use_container_width=True,
    )

with st.expander("View first 10 rows of raw data"):
    st.dataframe(df_raw.head(10), use_container_width=True)

# ── Section 2 – Data cleaning ─────────────────────────────────────────────────
st.header("2. Data Cleaning")

df = df_raw.copy()

# Strip whitespace from string columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Clean numeric columns: remove commas, $, %, B suffixes then cast to float
def clean_numeric(series: pd.Series) -> pd.Series:
    if series.dtype == object:
        s = (
            series.astype(str)
            .str.replace(r"[$,%]", "", regex=True)
            .str.replace(r"\s*B$", "", regex=True)   # remove trailing B (billion)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        return pd.to_numeric(s, errors="coerce")
    return pd.to_numeric(series, errors="coerce")

# Identify numeric-like columns (exclude obvious text columns)
text_cols = {"Company", "Headquarters", "Industry"}
for col in df.columns:
    if col not in text_cols:
        df[col] = clean_numeric(df[col])

# Identify revenue and profit columns
REVENUE_COL = None
PROFIT_COL = None
ASSETS_COL = None
MARKET_COL = None

for c in df.columns:
    cl = c.lower()
    if any(k in cl for k in ["sales", "revenue"]):
        REVENUE_COL = c
    if "profit" in cl:
        PROFIT_COL = c
    if "asset" in cl:
        ASSETS_COL = c
    if "market" in cl:
        MARKET_COL = c

# Calculate profit margin
if REVENUE_COL and PROFIT_COL:
    df["Profit Margin (%)"] = (df[PROFIT_COL] / df[REVENUE_COL] * 100).round(2)

# Drop duplicates
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)

st.success(
    f"Cleaning complete. Duplicates removed: {before - after}. "
    f"Working dataset: {after} rows × {df.shape[1]} columns."
)

with st.expander("View cleaned data (first 10 rows)"):
    st.dataframe(df.head(10), use_container_width=True)

# ── Section 3 – Industry filter (sidebar) ─────────────────────────────────────
st.sidebar.header("🔍 Filters")

if "Industry" in df.columns:
    all_industries = sorted(df["Industry"].dropna().unique().tolist())
    selected_industries = st.sidebar.multiselect(
        "Select Industries",
        options=all_industries,
        default=all_industries,
    )
    df_filtered = df[df["Industry"].isin(selected_industries)].copy()
else:
    df_filtered = df.copy()
    st.sidebar.info("No 'Industry' column found for filtering.")

# ── Section 4 – KPI cards ──────────────────────────────────────────────────────
st.header("3. Key Performance Indicators")

total_companies = len(df_filtered)

kpi_cols = st.columns(4)

kpi_cols[0].metric("🏢 Total Companies", f"{total_companies:,}")

if REVENUE_COL:
    total_revenue = df_filtered[REVENUE_COL].sum()
    kpi_cols[1].metric("💰 Total Revenue", f"${total_revenue:,.2f}B")
else:
    kpi_cols[1].metric("💰 Total Revenue", "N/A")

if PROFIT_COL:
    total_profit = df_filtered[PROFIT_COL].sum()
    kpi_cols[2].metric("📈 Total Profit", f"${total_profit:,.2f}B")
else:
    kpi_cols[2].metric("📈 Total Profit", "N/A")

if "Profit Margin (%)" in df_filtered.columns:
    avg_margin = df_filtered["Profit Margin (%)"].mean()
    kpi_cols[3].metric("📊 Avg Profit Margin", f"{avg_margin:.2f}%")
else:
    kpi_cols[3].metric("📊 Avg Profit Margin", "N/A")

st.markdown("---")

# ── Section 5 – Charts ─────────────────────────────────────────────────────────
st.header("4. Visual Analysis")

# ── 5a. Top 15 companies by revenue ───────────────────────────────────────────
if REVENUE_COL and "Company" in df_filtered.columns:
    st.subheader("Top 15 Companies by Revenue")
    top_rev = (
        df_filtered[["Company", REVENUE_COL]]
        .dropna()
        .sort_values(REVENUE_COL, ascending=False)
        .head(15)
    )
    fig_top_rev = px.bar(
        top_rev,
        x=REVENUE_COL,
        y="Company",
        orientation="h",
        labels={REVENUE_COL: "Revenue ($B)", "Company": "Company"},
        color=REVENUE_COL,
        color_continuous_scale="Blues",
        title="Top 15 Companies by Revenue ($B)",
    )
    fig_top_rev.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig_top_rev, use_container_width=True)

# ── 5b. Top 15 companies by profit ────────────────────────────────────────────
if PROFIT_COL and "Company" in df_filtered.columns:
    st.subheader("Top 15 Companies by Profit")
    top_profit = (
        df_filtered[["Company", PROFIT_COL]]
        .dropna()
        .sort_values(PROFIT_COL, ascending=False)
        .head(15)
    )
    fig_top_profit = px.bar(
        top_profit,
        x=PROFIT_COL,
        y="Company",
        orientation="h",
        labels={PROFIT_COL: "Profit ($B)", "Company": "Company"},
        color=PROFIT_COL,
        color_continuous_scale="Greens",
        title="Top 15 Companies by Profit ($B)",
    )
    fig_top_profit.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig_top_profit, use_container_width=True)

# ── 5c. Industry-wise total revenue ───────────────────────────────────────────
if REVENUE_COL and "Industry" in df_filtered.columns:
    st.subheader("Industry-Wise Total Revenue")
    ind_rev = (
        df_filtered.groupby("Industry")[REVENUE_COL]
        .sum()
        .reset_index()
        .sort_values(REVENUE_COL, ascending=False)
        .head(20)
    )
    fig_ind_rev = px.bar(
        ind_rev,
        x="Industry",
        y=REVENUE_COL,
        labels={REVENUE_COL: "Total Revenue ($B)", "Industry": "Industry"},
        color=REVENUE_COL,
        color_continuous_scale="Teal",
        title="Top 20 Industries by Total Revenue ($B)",
    )
    fig_ind_rev.update_layout(xaxis_tickangle=-40, coloraxis_showscale=False)
    st.plotly_chart(fig_ind_rev, use_container_width=True)

# ── 5d. Industry-wise total profit ────────────────────────────────────────────
if PROFIT_COL and "Industry" in df_filtered.columns:
    st.subheader("Industry-Wise Total Profit")
    ind_profit = (
        df_filtered.groupby("Industry")[PROFIT_COL]
        .sum()
        .reset_index()
        .sort_values(PROFIT_COL, ascending=False)
        .head(20)
    )
    fig_ind_profit = px.bar(
        ind_profit,
        x="Industry",
        y=PROFIT_COL,
        labels={PROFIT_COL: "Total Profit ($B)", "Industry": "Industry"},
        color=PROFIT_COL,
        color_continuous_scale="Purples",
        title="Top 20 Industries by Total Profit ($B)",
    )
    fig_ind_profit.update_layout(xaxis_tickangle=-40, coloraxis_showscale=False)
    st.plotly_chart(fig_ind_profit, use_container_width=True)

# ── 5e. Revenue vs Profit scatter ─────────────────────────────────────────────
if REVENUE_COL and PROFIT_COL and "Company" in df_filtered.columns:
    st.subheader("Revenue vs Profit (Scatter)")
    scatter_df = df_filtered[[REVENUE_COL, PROFIT_COL, "Company"]].dropna()
    if "Industry" in scatter_df.columns or "Industry" in df_filtered.columns:
        scatter_df = scatter_df.copy()
        scatter_df["Industry"] = df_filtered.loc[scatter_df.index, "Industry"]
        color_col = "Industry"
    else:
        color_col = None
    fig_scatter = px.scatter(
        scatter_df,
        x=REVENUE_COL,
        y=PROFIT_COL,
        hover_name="Company",
        color=color_col,
        labels={REVENUE_COL: "Revenue ($B)", PROFIT_COL: "Profit ($B)"},
        title="Revenue vs Profit by Company",
        opacity=0.75,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── 5f. Industry profit margin box / bar ──────────────────────────────────────
if "Profit Margin (%)" in df_filtered.columns and "Industry" in df_filtered.columns:
    st.subheader("Average Profit Margin by Industry (Top 20)")
    margin_df = (
        df_filtered.groupby("Industry")["Profit Margin (%)"]
        .mean()
        .reset_index()
        .sort_values("Profit Margin (%)", ascending=False)
        .head(20)
    )
    fig_margin = px.bar(
        margin_df,
        x="Industry",
        y="Profit Margin (%)",
        color="Profit Margin (%)",
        color_continuous_scale="RdYlGn",
        title="Average Profit Margin by Industry (Top 20)",
    )
    fig_margin.update_layout(xaxis_tickangle=-40, coloraxis_showscale=False)
    st.plotly_chart(fig_margin, use_container_width=True)

st.markdown("---")

# ── Section 6 – High-revenue, low-profit companies ────────────────────────────
st.header("5. High-Revenue but Low-Profit Companies")

if REVENUE_COL and PROFIT_COL:
    rev_threshold = df_filtered[REVENUE_COL].quantile(0.75)
    profit_threshold = df_filtered[PROFIT_COL].quantile(0.25)
    hl_df = df_filtered[
        (df_filtered[REVENUE_COL] >= rev_threshold) &
        (df_filtered[PROFIT_COL] <= profit_threshold)
    ].copy()

    display_cols = [c for c in ["Rank", "Company", "Industry", REVENUE_COL, PROFIT_COL, "Profit Margin (%)"] if c in hl_df.columns]
    hl_df_display = hl_df[display_cols].sort_values(REVENUE_COL, ascending=False)

    st.markdown(
        f"Companies with revenue ≥ **${rev_threshold:,.2f}B** (75th percentile) "
        f"and profit ≤ **${profit_threshold:,.2f}B** (25th percentile):"
    )
    st.dataframe(hl_df_display, use_container_width=True)
else:
    st.info("Revenue and/or Profit columns not found — cannot compute this table.")

st.markdown("---")

# ── Section 7 – Full filtered data table ──────────────────────────────────────
st.header("6. Filtered Dataset")
st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Fortune Company Performance Analysis · Forbes 2000 Companies 2026 · Built with Streamlit & Plotly")
