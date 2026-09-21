# Project Report: Fortune Company Performance Analysis

**Dataset:** Forbes 2000 Companies – 2026
**Tools:** Python, Pandas, NumPy, Streamlit, Plotly
**Report Type:** Exploratory Data Analysis (EDA)

---

## 1. Executive Summary

This report documents the end-to-end data analytics process applied to the Forbes Global 2000 Companies 2026 dataset. The analysis identifies leading companies and industries by revenue and profit, highlights companies with weak profit efficiency despite high revenue, and provides data-driven business recommendations. All findings in this report are derived solely from the dataset; no external data sources, machine learning models, or databases are used.

---

## 2. Business Problem

Global investors, corporate strategists, and market analysts need a structured view of company-level and industry-level financial performance. Specifically, this project addresses:

- Which companies generate the highest revenues and profits?
- Which industries dominate in total revenue and total profit?
- Which companies have high revenue but low profit, indicating possible inefficiencies?
- What is the average profit margin across industries, and which industries are most efficient?

---

## 3. Dataset Overview

| Attribute | Detail |
|---|---|
| File Name | `Forbes_2000_Companies_2026.csv` |
| Source | Forbes Global 2000 – 2026 edition |
| Approximate Row Count | ~2,000 companies |
| Columns | Rank, Company, Headquarters, Industry, Sales ($B), Profit ($B), Assets ($B), Market Value ($B) |
| Geographic Scope | Global (multiple countries and regions) |
| Financial Unit | All monetary values are in billions of US dollars ($B) |

### Column Descriptions

| Column | Description |
|---|---|
| Rank | Forbes Global 2000 ranking position |
| Company | Legal company name |
| Headquarters | City and country of headquarters |
| Industry | Forbes industry sector classification |
| Sales ($B) | Annual revenue in billions USD |
| Profit ($B) | Annual net profit in billions USD |
| Assets ($B) | Total assets in billions USD |
| Market Value ($B) | Market capitalisation in billions USD |

---

## 4. Steps Used for Analysis

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

## 5. Data Cleaning Process

The following cleaning steps were applied to the raw dataset before analysis:

| Step | Action |
|---|---|
| **Encoding** | File loaded with `utf-8-sig` encoding to handle the BOM character in the header |
| **Column whitespace** | Leading and trailing whitespace stripped from all column names |
| **String whitespace** | Leading and trailing whitespace stripped from all string/object columns |
| **Numeric symbols** | Dollar signs (`$`), commas (`,`), percentage signs (`%`), and trailing billion markers (`B`) removed from numeric-looking columns before converting to float |
| **Type conversion** | All non-text columns converted to `float` using `pd.to_numeric(..., errors='coerce')`; unparseable values become `NaN` |
| **Duplicate records** | Full-row duplicate records identified and removed using `DataFrame.drop_duplicates()` |
| **Derived metric** | `Profit Margin (%)` calculated as `(Profit ($B) / Sales ($B)) × 100` for every row where both columns are non-null |

---

## 6. KPI Analysis

The dashboard computes the following headline KPIs after applying any active industry filters:

| KPI | Definition |
|---|---|
| **Total Companies** | Count of companies in the filtered dataset |
| **Total Revenue ($B)** | Sum of `Sales ($B)` across all filtered companies |
| **Total Profit ($B)** | Sum of `Profit ($B)` across all filtered companies |
| **Average Profit Margin (%)** | Mean of `Profit Margin (%)` across all filtered companies |

> **Note:** Exact numerical values for these KPIs are generated live by the dashboard based on the loaded dataset and active filters. They are not hardcoded in this report to avoid presenting results that could become stale or inaccurate if the dataset changes.

---

## 7. Industry Analysis

The following analyses are performed at the industry level:

### 7.1 Industry-Wise Total Revenue
Industries are grouped and their `Sales ($B)` values are summed. The top 20 industries are displayed in a bar chart, ranked from highest to lowest total revenue.

### 7.2 Industry-Wise Total Profit
Industries are grouped and their `Profit ($B)` values are summed. The top 20 industries are displayed in a bar chart, ranked from highest to lowest total profit.

### 7.3 Average Profit Margin by Industry
For each industry the mean `Profit Margin (%)` is calculated across its member companies. This highlights industries that convert a high proportion of revenue into profit, independent of absolute revenue size.

> **Note:** The specific industries that rank highest in each category are visible in the live dashboard. Rankings depend on the active sidebar filter selection.

---

## 8. Company Analysis

### 8.1 Top 15 Companies by Revenue
The 15 companies with the highest `Sales ($B)` are displayed in a horizontal bar chart. These companies represent the largest revenue-generators in the Forbes 2000 list.

### 8.2 Top 15 Companies by Profit
The 15 companies with the highest `Profit ($B)` are displayed in a separate horizontal bar chart. Companies that appear in both the revenue and profit top-15 lists demonstrate strong end-to-end financial performance.

### 8.3 Revenue vs Profit Scatter
A scatter plot plots every company's revenue on the x-axis and profit on the y-axis, coloured by industry. This reveals:
- Companies that achieve high profit relative to their revenue (above the trend line).
- Outliers with very high revenue but below-average profit.

### 8.4 High-Revenue but Low-Profit Companies
Companies are flagged as "high-revenue / low-profit" when:
- Revenue ≥ 75th percentile of all filtered companies, **and**
- Profit ≤ 25th percentile of all filtered companies.

This table surfaces companies that may be experiencing cost pressures, high capital expenditure, or thin operating margins despite their scale.

---

## 9. Key Findings

> **Placeholder – populate from the live dashboard**

The following findings are structural placeholders. Run the Streamlit dashboard with the full dataset to obtain actual values.

- **Highest-revenue company:** *(see dashboard – Top 15 by Revenue chart)*
- **Most profitable company:** *(see dashboard – Top 15 by Profit chart)*
- **Industry with highest total revenue:** *(see dashboard – Industry Revenue chart)*
- **Industry with highest total profit:** *(see dashboard – Industry Profit chart)*
- **Industry with highest average profit margin:** *(see dashboard – Profit Margin by Industry chart)*
- **Number of high-revenue / low-profit companies:** *(see dashboard – Section 5 table)*
- **Overall average profit margin:** *(see dashboard – KPI card)*

---

## 10. Business Recommendations

Based on the analytical framework applied in this project, the following recommendations apply when interpreting Forbes 2000 data:

1. **Prioritise high-margin industries for investment screening** – Industries with the highest average profit margins offer better capital efficiency. Analysts should weight margin alongside absolute profit when building investment criteria.

2. **Investigate high-revenue, low-profit companies** – Companies that appear in the high-revenue / low-profit table warrant closer scrutiny. Possible causes include heavy reinvestment, high operational costs, debt servicing, or sector-specific pricing pressure.

3. **Use industry-adjusted benchmarking** – A company's profit margin is only meaningful relative to its industry peers. Banking and insurance companies naturally carry large asset bases that compress margin ratios; technology companies typically show higher margins.

4. **Monitor asset-heavy sectors separately** – Industries such as Banking and Insurance report very large total assets ($B). Revenue and profit comparisons should be complemented with return-on-assets (ROA) analysis when the data supports it.

5. **Track market value divergence from profit** – Companies where market value significantly exceeds their profit base may be priced on future growth expectations. The Revenue vs Profit scatter chart can be cross-referenced with Market Value ($B) to identify such cases.

6. **Use geographic filters for regional strategy** – The Headquarters column (city, country) can be used to group companies by country or region for a geographical competitive analysis beyond the scope of this project.

---

## 11. Limitations

| Limitation | Description |
|---|---|
| **Single year snapshot** | The dataset covers 2026 only; multi-year trend analysis is not possible without additional yearly files |
| **No employee data** | Revenue-per-employee analysis cannot be performed as headcount is not included in this dataset |
| **No sub-industry detail** | Forbes uses broad industry labels; finer-grained sector analysis (e.g. GICS sub-industries) is not possible |
| **Currency** | All values are in USD billions; companies reporting in local currencies may have conversion-related distortions |
| **Missing values** | Any row with a null value in a required column (e.g. Profit) is excluded from that specific calculation |
| **Profit margin edge cases** | Companies with zero or negative revenue produce undefined or negative profit margin values and are treated as outliers |
| **No predictive modelling** | This project is purely descriptive; no forecasting or classification models are applied |

---

## 12. Conclusion

This project demonstrates a complete exploratory data analysis workflow applied to the Forbes 2000 Companies 2026 dataset. The interactive Streamlit dashboard provides stakeholders with a self-service tool to explore company and industry performance using real financial data. The analysis covers data loading, cleaning, KPI computation, visual comparison, and identification of outlier companies, without relying on any external APIs, databases, or machine learning techniques.

The high-revenue / low-profit analysis and industry-wise margin comparison are the most actionable outputs, as they directly point analysts toward companies and sectors that may require strategic attention. All numerical conclusions should be drawn from the live dashboard to ensure they reflect the current, cleaned state of the dataset.

---

*Report generated for the Fortune Company Performance Analysis project.*
*Dataset: Forbes 2000 Companies 2026 · Tools: Python, Pandas, NumPy, Streamlit, Plotly*
