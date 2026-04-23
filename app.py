
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Streaming Platform Comparison Dashboard",
    page_icon="📺",
    layout="wide",
)

DATA_FILES = {
    "Netflix": ("netflix_financials.csv", "Subscribers"),
    "Bilibili": ("bilibili_financials.csv", "MAU"),
    "iQIYI": ("iqiyi_financials.csv", "Subscribers"),
}

COMPANY_NOTES = {
    "Netflix": "Global subscription-led platform with the strongest revenue scale and the most stable profitability in this sample.",
    "Bilibili": "Chinese platform with a broader ecosystem model. User growth is strong, but monetisation and profitability remain weaker.",
    "iQIYI": "Chinese long-form video platform. It is smaller than Netflix, but later years show improving profitability.",
}

def find_data_file(filename: str) -> Path:
    candidates = [
        Path.cwd() / "data" / filename,
        Path.cwd() / filename,
        Path(__file__).resolve().parent / "data" / filename,
        Path("/mnt/data") / filename,
        Path("/mnt/data") / "data" / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"Could not find {filename} in expected folders.")

@st.cache_data
def load_company_data() -> pd.DataFrame:
    frames = []
    for company, (filename, user_col) in DATA_FILES.items():
        df = pd.read_csv(find_data_file(filename)).copy()
        df["Company"] = company
        df["UserMetric"] = df[user_col]
        df["UserMetricType"] = user_col
        df["ProfitMargin"] = df["NetIncome"] / df["Revenue"]
        df["RevenueGrowth"] = df["Revenue"].pct_change()
        df["RevenuePerUser"] = df["Revenue"] / df["UserMetric"]
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    combined["ProfitMarginPct"] = combined["ProfitMargin"] * 100
    combined["RevenueGrowthPct"] = combined["RevenueGrowth"] * 100
    return combined

def make_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for company, company_df in df.groupby("Company"):
        company_df = company_df.sort_values("Year")
        first_year = company_df["Year"].min()
        last_year = company_df["Year"].max()
        year_span = max(last_year - first_year, 1)
        start_rev = company_df["Revenue"].iloc[0]
        end_rev = company_df["Revenue"].iloc[-1]
        cagr = ((end_rev / start_rev) ** (1 / year_span) - 1) * 100 if start_rev > 0 else None

        rows.append(
            {
                "Company": company,
                "Latest Year": int(last_year),
                "Latest Revenue (USD mn)": round(company_df["Revenue"].iloc[-1], 1),
                "Latest Net Income (USD mn)": round(company_df["NetIncome"].iloc[-1], 1),
                "Latest User Metric (mn)": round(company_df["UserMetric"].iloc[-1], 1),
                "User Metric Type": company_df["UserMetricType"].iloc[-1],
                "Average Profit Margin (%)": round(company_df["ProfitMarginPct"].mean(), 2),
                "Revenue CAGR (%)": round(cagr, 2) if cagr is not None else None,
                "Revenue per User": round(company_df["RevenuePerUser"].iloc[-1], 2),
            }
        )
    return pd.DataFrame(rows).sort_values("Latest Revenue (USD mn)", ascending=False)

def auto_insight(df: pd.DataFrame) -> str:
    summary = make_summary_table(df)
    if summary.empty:
        return "No data is available for the current filter."
    top_revenue = summary.iloc[0]["Company"]
    best_margin = summary.sort_values("Average Profit Margin (%)", ascending=False).iloc[0]["Company"]
    weakest_margin = summary.sort_values("Average Profit Margin (%)", ascending=True).iloc[0]["Company"]

    lines = [
        f"{top_revenue} has the highest latest revenue in the filtered data.",
        f"{best_margin} shows the strongest average profit margin.",
        f"{weakest_margin} has the weakest average profit margin, which suggests that scale alone does not guarantee profitability.",
    ]

    bilibili = summary[summary["Company"] == "Bilibili"]
    if not bilibili.empty:
        b_margin = bilibili["Average Profit Margin (%)"].iloc[0]
        if b_margin < 0:
            lines.append("Bilibili's results support the idea that rapid user expansion does not automatically translate into profit.")
    return " ".join(lines)

df = load_company_data()

st.title("📺 Streaming Platform Comparison Dashboard")
st.caption("Track 4 interactive tool for comparing Netflix, Bilibili, and iQIYI.")

with st.sidebar:
    st.header("Filters")
    companies = st.multiselect(
        "Select companies",
        options=sorted(df["Company"].unique().tolist()),
        default=sorted(df["Company"].unique().tolist()),
    )

    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())
    selected_years = st.slider("Select year range", min_year, max_year, (min_year, max_year))

    metric_map = {
        "Revenue (USD mn)": "Revenue",
        "Net Income (USD mn)": "NetIncome",
        "Profit Margin (%)": "ProfitMarginPct",
        "Revenue Growth (%)": "RevenueGrowthPct",
        "User Metric (mn)": "UserMetric",
        "Revenue per User": "RevenuePerUser",
    }
    chart_metric_label = st.selectbox("Main comparison metric", list(metric_map.keys()))
    chart_metric = metric_map[chart_metric_label]

filtered = df[
    (df["Company"].isin(companies))
    & (df["Year"].between(selected_years[0], selected_years[1]))
].copy()

if filtered.empty:
    st.warning("No data matches the current filters.")
    st.stop()

latest_year = int(filtered["Year"].max())
latest_df = filtered[filtered["Year"] == latest_year].copy()
summary_table = make_summary_table(filtered)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Company Comparison", "Growth vs Revenue", "Business Model Insights"]
)

with tab1:
    st.subheader("Project overview")
    st.markdown(
        """
This app compares the financial performance of **Netflix**, **Bilibili**, and **iQIYI**.
It focuses on three questions:

1. Which company has the strongest revenue scale and profitability?
2. How closely does user growth relate to revenue?
3. What does the comparison suggest about different platform business models?

**Important comparability note:** Netflix and iQIYI are mainly interpreted with **subscribers**, while Bilibili is interpreted with **MAU** because its platform model is broader than a pure subscription service.
"""
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Companies shown", len(filtered["Company"].unique()))
    c2.metric("Latest year in view", latest_year)
    c3.metric("Observations", len(filtered))

    st.subheader(f"Latest snapshot ({latest_year})")
    metric_cols = st.columns(len(latest_df))
    for idx, (_, row) in enumerate(latest_df.sort_values("Revenue", ascending=False).iterrows()):
        with metric_cols[idx]:
            st.metric(
                label=f"{row['Company']} Revenue",
                value=f"{row['Revenue']:,.0f}",
                delta=f"{row['ProfitMarginPct']:.1f}% margin",
            )
            st.caption(f"{row['UserMetricType']}: {row['UserMetric']:,.0f} mn")

    st.subheader("Summary table")
    st.dataframe(summary_table, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Time-series comparison")
    fig_line = px.line(
        filtered,
        x="Year",
        y=chart_metric,
        color="Company",
        markers=True,
        title=chart_metric_label,
    )
    fig_line.update_layout(legend_title_text="")
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader(f"Latest-year comparison ({latest_year})")
    fig_bar = px.bar(
        latest_df.sort_values(chart_metric, ascending=False),
        x="Company",
        y=chart_metric,
        color="Company",
        title=f"{chart_metric_label} in {latest_year}",
        text_auto=".2s" if chart_metric not in ["ProfitMarginPct", "RevenueGrowthPct"] else ".2f",
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("User metric and revenue relationship")
    fig_scatter = px.scatter(
        filtered,
        x="UserMetric",
        y="Revenue",
        color="Company",
        size="Revenue",
        hover_data=["Year", "UserMetricType", "NetIncome", "ProfitMarginPct"],
        title="Revenue versus user metric",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Revenue growth by company")
    growth_df = filtered.dropna(subset=["RevenueGrowthPct"]).copy()
    if growth_df.empty:
        st.info("Revenue growth cannot be shown because the selected range starts with the first available year for all companies.")
    else:
        fig_growth = px.line(
            growth_df,
            x="Year",
            y="RevenueGrowthPct",
            color="Company",
            markers=True,
            title="Revenue Growth (%)",
        )
        fig_growth.add_hline(y=0, line_dash="dash")
        st.plotly_chart(fig_growth, use_container_width=True)

    st.subheader("Automatic insight")
    st.info(auto_insight(filtered))

with tab4:
    st.subheader("Business-model reading")
    for company in sorted(filtered["Company"].unique()):
        company_df = filtered[filtered["Company"] == company].sort_values("Year")
        latest = company_df.iloc[-1]
        start = company_df.iloc[0]
        revenue_change = latest["Revenue"] - start["Revenue"]
        st.markdown(f"### {company}")
        st.write(COMPANY_NOTES[company])
        st.write(
            f"- Revenue changed from **{start['Revenue']:,.0f}** to **{latest['Revenue']:,.0f}** million USD "
            f"between **{int(start['Year'])}** and **{int(latest['Year'])}**."
        )
        st.write(
            f"- Latest profit margin is **{latest['ProfitMarginPct']:.2f}%** and the latest user metric is "
            f"**{latest['UserMetric']:,.0f} million {latest['UserMetricType']}**."
        )
        if latest["ProfitMarginPct"] < 0:
            st.write("- Interpretation: the company is still struggling to convert scale into stable profit.")
        else:
            st.write("- Interpretation: the company shows a stronger ability to turn platform scale into earnings.")
        st.divider()

    st.subheader("Download cleaned data")
    download_df = filtered.sort_values(["Company", "Year"]).copy()
    st.download_button(
        label="Download filtered CSV",
        data=download_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_streaming_platform_data.csv",
        mime="text/csv",
    )
