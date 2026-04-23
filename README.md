# Streaming Platform Comparison Dashboard

**Track:** Track 4 – Interactive Tool  
**Module:** ACC102 Mini Assignment

## 1. Project Summary
This project upgrades the earlier notebook analysis into an interactive **Streamlit dashboard**.  
It compares **Netflix, Bilibili, and iQIYI** to explore:

- revenue scale and profitability;
- the relationship between user growth and revenue; and
- business-model differences between a global streaming platform and Chinese video platforms.

The dashboard is designed for a **non-technical business audience**, such as students, beginner investors, or readers who want a simple and visual comparison.

## 2. Files Included
```text
track4_streamlit_package/
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

## 3. Data Sources
The data were compiled from official investor-relations materials and arranged into annual CSV files for teaching use.

- **Netflix Investor Relations** – annual reports and investor materials  
- **Bilibili Investor Relations** – annual reports and financial information  
- **iQIYI Investor Relations** – annual reports and financial information  
- **Access date:** 22 April 2026

### Variables
- `Year`
- `Revenue`
- `NetIncome`
- `Subscribers` or `MAU`

### Comparability note
Netflix and iQIYI are interpreted mainly using **subscribers**.  
Bilibili is interpreted using **MAU**, because its platform model is broader than a pure subscription service.

## 4. Dashboard Features
The Streamlit app includes:

1. **Overview tab**
   - project purpose
   - latest KPI snapshot
   - summary comparison table

2. **Company Comparison tab**
   - line chart for revenue, net income, profit margin, revenue growth, user scale, or revenue per user
   - latest-year bar chart

3. **Growth vs Revenue tab**
   - scatter plot of user metric vs revenue
   - revenue growth trend
   - automatic text insight

4. **Business Model Insights tab**
   - company-specific interpretation
   - downloadable filtered CSV

## 5. How to Run Locally
Open a terminal in this project folder and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 6. How to Upload to GitHub
1. Create a new GitHub repository.
2. Upload all files in this folder.
3. Make sure the `data/` folder is included.
4. Check that `app.py`, `requirements.txt`, and `README.md` appear in the repo root.

## 7. How to Deploy on Streamlit Community Cloud
1. Push the repo to GitHub.
2. Open **Streamlit Community Cloud**.
3. Click **New app**.
4. Connect your GitHub repository.
5. Set the main file path to `app.py`.
6. Deploy the app.
7. Copy the public app link into your final submission.

## 8. Suggested Submission Items
For the final Track 4 submission, prepare:

- GitHub repository link
- interactive tool link
- notebook or code files
- README
- 1–3 minute demo video
- reflection report

## 9. Demo Video Suggestions
In your video, show these parts in order:

1. project title and question
2. how the sidebar filters work
3. one comparison chart
4. the growth vs revenue page
5. the business-model interpretation
6. your final takeaway

## 10. Short Project Conclusion
The current data suggest that **Netflix** has the strongest combination of scale and profitability.  
**Bilibili** shows fast user growth but weaker monetisation.  
**iQIYI** is smaller than Netflix, but later years show improving profitability.

This supports the main idea of the project: **user growth matters, but monetisation design matters even more**.
