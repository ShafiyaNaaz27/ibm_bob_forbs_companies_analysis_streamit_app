# Fortune Company Performance Analysis

## Project Overview

This project performs an exploratory data analysis on the **Forbes 2000 Companies 2026** dataset. The goal is to uncover revenue and profit patterns across global companies and industries using an interactive Streamlit dashboard powered by Plotly charts.

---

## Business Problem

Corporate leaders, investors, and analysts need a fast, visual way to:

- Identify which companies and industries generate the highest revenues and profits.
- Spot high-revenue companies that deliver low profits (efficiency problem).
- Understand average profit margins across industries.
- Compare company-level financial performance without querying raw spreadsheets.

---

## Dataset Description

| Field | Description |
|---|---|
| **File** | `Forbes_2000_Companies_2026.csv` |
| **Source** | Forbes Global 2000 Companies – 2026 edition |
| **Rows** | ~2,000 global companies |
| **Columns** | Rank, Company, Headquarters, Industry, Sales ($B), Profit ($B), Assets ($B), Market Value ($B) |

### Column Definitions

| Column | Meaning |
|---|---|
| Rank | Forbes Global 2000 ranking position |
| Company | Legal company name |
| Headquarters | City and country of headquarters |
| Industry | Industry sector classification |
| Sales ($B) | Annual revenue in billions of US dollars |
| Profit ($B) | Annual net profit in billions of US dollars |
| Assets ($B) | Total assets in billions of US dollars |
| Market Value ($B) | Market capitalisation in billions of US dollars |

---

## Tools Used

| Tool | Purpose |
|---|---|
| **Python 3** | Core programming language |
| **Pandas** | Data loading, cleaning, and analysis |
| **NumPy** | Numerical operations and percentile calculations |
| **Streamlit** | Interactive web dashboard |
| **Plotly Express** | Interactive charts and visualisations |

---

## Steps Used for Analysis

1. Collect and load the CSV dataset.
2. Check the data for missing or incorrect values.
3. Clean and prepare the available numeric and categorical columns.
4. Calculate relevant business metrics such as profit margin, revenue per employee and revenue per asset when the required columns are available.
5. Group and summarize the data using totals, counts and averages.
6. Compare companies and industries using tables and charts.
7. Identify high-performing industries, leading companies and high-revenue but low-profit companies.
8. Create charts to compare the results.
9. Use the results to make data-driven business recommendations.

---

## KPI Definitions

| KPI | Definition |
|---|---|
| **Total Companies** | Count of companies present after cleaning and filtering |
| **Total Revenue** | Sum of Sales ($B) for all filtered companies |
| **Total Profit** | Sum of Profit ($B) for all filtered companies |
| **Average Profit Margin** | Mean of (Profit / Revenue × 100) across all filtered companies |

---

## Dashboard Features

| Section | Description |
|---|---|
| **Dataset Overview** | Displays row count, column count, missing values, and duplicate records |
| **Data Cleaning** | Removes commas, currency symbols, and percentage signs from numeric columns; drops duplicates |
| **Industry Filter (sidebar)** | Multi-select sidebar to filter all charts and KPIs by industry |
| **KPI Cards** | Four headline metrics: Total Companies, Total Revenue, Total Profit, Avg Profit Margin |
| **Top 15 by Revenue** | Horizontal bar chart of the 15 highest-revenue companies |
| **Top 15 by Profit** | Horizontal bar chart of the 15 most profitable companies |
| **Industry Revenue** | Bar chart of the top 20 industries by total revenue |
| **Industry Profit** | Bar chart of the top 20 industries by total profit |
| **Revenue vs Profit Scatter** | Scatter plot comparing every company's revenue and profit, coloured by industry |
| **Avg Profit Margin by Industry** | Bar chart ranking industries by average profit margin |
| **High-Revenue / Low-Profit Table** | Companies whose revenue is in the top 25 % but profit is in the bottom 25 % |
| **Full Filtered Table** | Paginated table of all companies after applying sidebar filters |

---

## Installation and Run Instructions

### 1. Clone or copy the project files

```
Forbes_2000_Companies_2026.csv
app.py
requirements.txt
README.md
project_report.md
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`.

---

## Business Recommendations

The following recommendations are based on patterns typically observed in Forbes 2000 data. Actual numerical conclusions should be drawn from the live dashboard.

1. **Focus investment on high-margin industries** – Industries with the highest average profit margins offer the best return on revenue.
2. **Investigate high-revenue, low-profit companies** – Companies appearing in the high-revenue / low-profit table may be experiencing cost inefficiencies, heavy reinvestment, or sector-specific pressures.
3. **Monitor dominant industries** – The top industries by total revenue often house the companies with the largest global economic footprint; tracking their trends over time provides early signals of market shifts.
4. **Benchmark against industry averages** – A company's profit margin is most meaningful when compared against its industry peers rather than the global average.
5. **Prioritise asset-heavy sectors carefully** – High total-asset industries (e.g. Banking) may show large revenue figures but thinner margins due to cost of capital; investors should weigh return on assets alongside raw revenue.

---

## Limitations

- The dataset reflects a single-year snapshot (2026); trend analysis over multiple years is not possible with this file alone.
- All financial values are in billions of USD; small-cap companies may appear less significant than they are in local markets.
- Industry classifications are as assigned by Forbes and may not align with other classification systems (e.g. GICS, SIC).
- Missing or null values in any financial column are excluded from that column's calculations.
- Profit margin calculations rely on non-zero revenue; companies with zero or missing revenue are excluded from margin analysis.
- No machine learning, external APIs, or databases are used; all insights are purely descriptive.
