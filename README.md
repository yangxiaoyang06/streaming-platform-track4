# Streaming Platform Comparison Dashboard

**Track:** Track 4 – Interactive Tool  
**Module:** ACC102 Mini Assignment  
**Live app:** https://acc102-streaming-platform-analysis-nhc9uif2n4bul6bcnxdvmj.streamlit.app/

## 1. Project Overview

This project compares the financial performance and user growth of three major streaming platforms: **Netflix, Bilibili, and iQIYI**. The main research question is:

> How do global and Chinese streaming platforms differ in revenue performance, user growth, profitability, and business model design?

The analysis was first developed in a Jupyter Notebook and then converted into an interactive Streamlit dashboard. The dashboard is aimed at a general business audience, so the charts and explanations are kept clear and practical rather than overly technical.

## 2. Files in This Repository

```text
streaming-platform-track4/
│
├── app.py
├── README.md
├── requirements.txt
├── notebook.ipynb
└── data/
    ├── netflix_financials.csv
    ├── bilibili_financials.csv
    ├── iqiyi_financials.csv
    └── merged_platform_data.csv
```

## 3. Data Sources and Notes

The dataset was manually compiled from official company investor-relations materials and annual reports, then cleaned into CSV format for the dashboard.

Sources used:

- Netflix Investor Relations: https://ir.netflix.net/financials/annual-reports-and-proxies/default.aspx
- Bilibili Investor Relations: https://ir.bilibili.com/
- iQIYI Investor Relations: https://ir.iqiyi.com/

**Access date:** 22 April 2026

### Main Variables

- `Year`
- `Revenue`
- `NetIncome`
- `Subscribers` or `MAU`

### Unit Notes

- Revenue and net income are shown in **USD millions**.
- User metrics are shown in **millions**.
- Netflix and iQIYI are mainly compared using subscriber figures.
- Bilibili is compared using MAU because its business model is broader than a subscription-only streaming service.

Because the three companies report user metrics differently, the dashboard should be read as a business comparison rather than a perfectly standardised accounting dataset.

## 4. Dashboard Features

The Streamlit dashboard includes four main sections:

### Overview

- project background and research question
- latest KPI snapshot
- comparison table for the selected companies and years

### Company Comparison

- line chart for revenue, net income, profit margin, revenue growth, user scale, or revenue per user
- latest-year bar chart for quick comparison

### Growth vs Revenue

- scatter plot comparing user scale and revenue
- revenue growth trend over time
- short interpretation of the relationship between users and revenue

### Business Model Insights

- company-level interpretation
- comparison of monetisation models
- downloadable filtered CSV file

## 5. How to Run the App Locally

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app should then open in a browser at a local Streamlit address.

## 6. How to Deploy the App

The app is deployed through Streamlit Community Cloud.

Deployment settings:

```text
Repository: yangxiaoyang06/streaming-platform-track4
Branch: main
Main file path: app.py
```

## 7. Suggested Final Submission Items

For the Track 4 submission, I would include:

- GitHub repository link
- Streamlit app link
- notebook and source code files
- data folder
- README file
- short demo video
- reflection report

## 8. Demo Video Plan

A 1–3 minute demo video can follow this order:

1. introduce the topic and research question
2. show the sidebar filters
3. explain one company comparison chart
4. show the growth vs revenue section
5. explain the business model insights
6. finish with the main takeaway

## 9. Project Conclusion

The results suggest that **Netflix** has the strongest combination of revenue scale and profitability. **Bilibili** has a large user base, but its monetisation is weaker because its platform model depends on several revenue streams rather than only paid subscriptions. **iQIYI** is smaller than Netflix, but its later results show signs of improving profitability.

Overall, the project shows that user growth alone is not enough. For streaming platforms, long-term financial performance also depends on how effectively the company converts users into revenue and profit.
