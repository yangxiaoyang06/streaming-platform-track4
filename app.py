from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Streaming Platform Comparison Dashboard",
    page_icon="🎬",
    layout="wide"
)

DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_platform_data():
    merged_path = DATA_DIR / "merged_platform_data.csv"

    if merged_path.exists():
        df = pd.read_csv(merged_path)
    else:
        files = {
            "Netflix": DATA_DIR / "netflix_financials.csv",
            "Bilibili": DATA_DIR / "bilibili_financials.csv",
            "iQIYI": DATA_DIR / "iqiyi_financials.csv",
        }

        frames = []
        for platform, path in files.items():
            temp = pd.read_csv(path)
            temp["Platform"] = platform
            frames.append(temp)

        df = pd.concat(frames, ignore_index=True)

    df.columns = [col.strip() for col in df.columns]

    for col in ["Year", "Revenue", "NetIncome", "Subscribers", "MAU", "Users"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Platform" not in df.columns:
        raise ValueError("The dataset must include a Platform column.")

    if "Users" not in df.columns:
        if "Subscribers" in df.columns and "MAU" in df.columns:
            df["Users"] = df["Subscribers"].fillna(df["MAU"])
        elif "Subscribers" in df.columns:
            df["Users"] = df["Subscribers"]
        elif "MAU" in df.columns:
            df["Users"] = df["MAU"]
        else:
            df["Users"] = pd.NA

    df["ProfitMargin"] = df["NetIncome"] / df["Revenue"] * 100
    df["RevenuePerUser"] = df["Revenue"] / df["Users"]

    df = df.sort_values(["Platform", "Year"])
    df["RevenueGrowth"] = df.groupby("Platform")["Revenue"].pct_change() * 100

    return df


df = load_platform_data()

st.title("Streaming Platform Comparison Dashboard")

st.write(
    "This interactive dashboard compares Netflix, Bilibili, and iQIYI using "
    "revenue, profitability, user scale, and business model indicators."
)

st.sidebar.header("Filters")

platforms = sorted(df["Platform"].dropna().unique())
selected_platforms = st.sidebar.multiselect(
    "Choose platforms",
    platforms,
    default=platforms
)

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Choose year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

metric_options = {
    "Revenue": "Revenue",
    "Net income": "NetIncome",
    "Profit margin (%)": "ProfitMargin",
    "Revenue growth (%)": "RevenueGrowth",
    "User scale": "Users",
    "Revenue per user": "RevenuePerUser",
}

selected_metric_label = st.sidebar.selectbox(
    "Choose comparison metric",
    list(metric_options.keys())
)

selected_metric = metric_options[selected_metric_label]

filtered = df[
    (df["Platform"].isin(selected_platforms))
    & (df["Year"] >= selected_years[0])
    & (df["Year"] <= selected_years[1])
].copy()

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.subheader("Problem and User")
st.write(
    "The dashboard is designed for a general business audience. It answers the question: "
    "How do global and Chinese streaming platforms differ in revenue performance, "
    "user growth, profitability, and business model design?"
)

latest_year = int(filtered["Year"].max())
latest_data = filtered[filtered["Year"] == latest_year]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Latest year in view", latest_year)

with col2:
    total_revenue = latest_data["Revenue"].sum()
    st.metric("Total revenue in latest year", f"${total_revenue:,.0f}m")

with col3:
    avg_margin = latest_data["ProfitMargin"].mean()
    st.metric("Average profit margin", f"{avg_margin:.1f}%")

st.divider()

st.subheader("Company Comparison")

fig_line = px.line(
    filtered,
    x="Year",
    y=selected_metric,
    color="Platform",
    markers=True,
    title=f"{selected_metric_label} by Platform"
)
st.plotly_chart(fig_line, use_container_width=True)

fig_bar = px.bar(
    latest_data,
    x="Platform",
    y=selected_metric,
    title=f"{selected_metric_label} in {latest_year}",
    text_auto=".2s"
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

st.subheader("Growth vs Revenue")

fig_scatter = px.scatter(
    filtered,
    x="Users",
    y="Revenue",
    color="Platform",
    size="Revenue",
    hover_data=["Year", "NetIncome", "ProfitMargin"],
    title="User Scale and Revenue"
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.write(
    "This chart helps show whether a larger user base is linked with stronger revenue. "
    "The comparison should be read carefully because Netflix and iQIYI mainly report "
    "subscriber figures, while Bilibili is better represented by monthly active users."
)

st.divider()

st.subheader("Business Model Insights")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown(
        """
        **Netflix** mainly depends on paid subscriptions and has the strongest revenue scale.

        **Bilibili** has a broad community-based platform model. Its user base is large, but
        monetisation is weaker because revenue comes from several mixed sources.

        **iQIYI** is closer to a subscription video model, but its scale and profitability are
        weaker than Netflix.
        """
    )

with insight_col2:
    st.markdown(
        """
        **Main takeaway:** user growth alone is not enough. A streaming platform also needs
        to convert users into stable revenue and profit.

        This is why profitability, revenue per user, and business model design should be
        considered together rather than only looking at audience size.
        """
    )

st.divider()

st.subheader("Filtered Data")
st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name="filtered_streaming_platform_data.csv",
    mime="text/csv"
)
