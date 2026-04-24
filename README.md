# Streaming Platform Comparison Dashboard

## 1. Problem & User

This project compares Netflix, Bilibili, and iQIYI to see how their revenue, user scale, and profitability are different. The dashboard is made for a general business or class audience who wants to quickly compare global and Chinese streaming platforms.

## 2. Data

The data was collected from official investor relations pages and annual reports, then organised into CSV files for analysis.

**Sources**

- Netflix Investor Relations: https://ir.netflix.net/financials/annual-reports-and-proxies/default.aspx
- Bilibili Investor Relations: https://ir.bilibili.com/
- iQIYI Investor Relations: https://ir.iqiyi.com/

**Access date:** 22 April 2026

**Main files**

```text
data/netflix_financials.csv
data/bilibili_financials.csv
data/iqiyi_financials.csv
data/merged_platform_data.csv
```

**Key fields**

- `Year`
- `Platform`
- `Revenue`
- `NetIncome`
- `Subscribers` or `MAU`
- `ProfitMargin`
- `RevenueGrowth`
- `RevenuePerUser`

Revenue and net income are shown in USD millions. User figures are shown in millions. Netflix and iQIYI are mainly compared with subscriber figures, while Bilibili is compared with MAU because it uses a wider community-platform model rather than only a subscription model.

## 3. Methods

The main Python steps were:

1. Load the company CSV files with pandas.
2. Clean column names and make the units consistent.
3. Merge the three company datasets into one combined file.
4. Calculate extra metrics such as profit margin, revenue growth, and revenue per user.
5. Build charts with Plotly to compare platforms by year and metric.
6. Turn the notebook analysis into a Streamlit dashboard with filters and downloadable data.

## 4. Key Findings

- Netflix has the largest revenue scale and the strongest profitability among the three platforms.
- Bilibili has a large user base, but its revenue per user is lower because it depends on a mix of ads, games, live streaming, and memberships.
- iQIYI is smaller than Netflix, but its profitability improves in the later years of the dataset.
- User growth does not automatically mean better financial performance. The platform also needs a strong way to convert users into revenue.
- The comparison shows that business model differences matter as much as platform size.

## 5. How to Run

To run the app locally, open a terminal in the project folder and use:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Main project files:

```text
app.py
notebook.ipynb
requirements.txt
README.md
data/
```

## 6. Product Link / Demo

**Live Streamlit app:**  
https://acc102-streaming-platform-analysis-nhc9uif2n4bul6bcnxdvmj.streamlit.app/

**GitHub repository:**  
https://github.com/yangxiaoyang06/streaming-platform-track4

The app lets users choose platforms, years, and metrics. It includes revenue and profitability charts, a growth vs revenue section, business model notes, and a filtered data download button.

## 7. Limitations & Next Step

One limitation is that the three companies do not report user metrics in exactly the same way. Netflix and iQIYI use paid subscriber-related figures, while Bilibili uses MAU, so the user comparison is not perfectly equal.

Another limitation is that the project mainly uses annual company-level data. It does not include more detailed information such as region, content spending, pricing plans, or advertising revenue by segment.

A useful next step would be to add more years of data and include more detailed revenue categories. This would make it easier to explain why each platform performs differently, not only whether it performs better or worse.
