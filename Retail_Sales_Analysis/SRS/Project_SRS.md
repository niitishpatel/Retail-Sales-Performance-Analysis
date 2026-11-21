# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

## Retail Sales Performance Analysis

| Document Information | Details |
|---|---|
| **Project Title** | Retail Sales Performance Analysis |
| **Academic Level** | First-Year B.Tech Computer Science & Engineering |
| **Course Module** | Python, NumPy, and Pandas Industrial Training Assignment |
| **Document Type** | Software Requirements Specification (SRS) |
| **Version** | 1.0 (Final) |
| **Author** | Nitish Patel (B.Tech CSE, 1st Year) |
| **Dataset Source** | `01_retail_sales.csv` |
| **Date** | November 2026 |

---

## Table of Contents

1. [Project Title](#1-project-title)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Project Objectives](#4-project-objectives)
5. [Project Scope](#5-project-scope)
6. [Dataset Description](#6-dataset-description)
7. [Functional Requirements](#7-functional-requirements)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Tools and Technologies](#9-tools-and-technologies)
10. [Methodology](#10-methodology)
11. [Expected Outcomes](#11-expected-outcomes)
12. [Limitations](#12-limitations)
13. [Conclusion](#13-conclusion)

---

## 1. Project Title

**Retail Sales Performance Analysis**  
*An End-to-End Exploratory Data Analysis and Business Intelligence System Using Python, NumPy, Pandas, Matplotlib, and Seaborn.*

---

## 2. Introduction

This Software Requirements Specification (SRS) document defines the architectural, functional, and non-functional specifications for the **Retail Sales Performance Analysis** project. Developed as part of an industrial training curriculum in Python programming, NumPy array computation, and Pandas data analytics, this project serves as a cornerstone academic application for first-year undergraduate students in Computer Science and Engineering (B.Tech CSE).

Retail enterprises capture vast volumes of daily transactional records comprising orders, customer identifiers, product details, geographic footprints, and monetary figures. To derive strategic value from such operational datasets, raw transactional logs must undergo rigorous validation, systematic cleaning, exploratory analysis, statistical evaluation, and data visualization.

This project delivers an automated, reproducible Python data analytics pipeline that processes the actual industrial dataset (`01_retail_sales.csv`), handles inherent real-world data imperfections (missing attributes, duplicate transactions, and computational discrepancies), computes core business metrics, uncovers underlying sales patterns across regional and temporal dimensions, detects numerical anomalies using statistical methods, and outputs executive-ready visual charts and structured analytical tables.

---

## 3. Problem Statement

Modern retail management requires agile, evidence-based decision-making to maintain competitive advantage. However, unstructured or raw transactional logs frequently present several operational bottlenecks:

1. **Data Quality Degradation:** Real-world retail data often suffers from human error, transmission drops, and system anomalies — including duplicate record entries, unrecorded customer locations, and mismatched arithmetic calculations between unit prices, quantities, and line totals.
2. **Analytical Latency and Inefficiency:** Conducting manual spreadsheets or ad-hoc analyses across multi-dimensional parameters (product categories, geographical territories, monthly timelines, and payment gateways) is error-prone, labor-intensive, and unscalable.
3. **Absence of Actionable Intelligence:** Without structured exploratory data analysis (EDA) and robust statistical summaries (central tendency, dispersion, and outlier detection), managers cannot reliably identify high-yield inventory, underperforming distribution hubs, peak seasonal demand windows, or customer payment patterns.

To solve these problems, this project provides a modular, Python-driven computational solution that automatically audits, cleans, analyzes, and visualizes retail sales performance without human bias or manual errors.

---

## 4. Project Objectives

The project is designed to accomplish the following core technical and analytical objectives:

- **O-1 (Data Ingestion & Integrity Auditing):** Load the raw CSV dataset, inspect dimensional attributes, evaluate column data types, and identify data anomalies including missing values and duplicate rows.
- **O-2 (Principled Data Cleansing):** Apply transparent, scientifically justified data cleaning protocols: impute missing geographical attributes without fabricating false locations, isolate and remove redundant duplicate transactions, and rectify arithmetic inconsistencies in revenue figures.
- **O-3 (Feature Engineering):** Parse raw textual dates into standard datetime objects and extract temporal attributes (calendar month, month name, and day of the week) to facilitate seasonal and behavioral trend analysis.
- **O-4 (Core Financial & Volume Metrics):** Calculate essential Key Performance Indicators (KPIs) including Total Gross Revenue, Total Quantity Sold, Total Order Count, and Average Order Value (AOV).
- **O-5 (Multi-Dimensional Segmentation):** Perform group-wise aggregations across multiple retail facets:
  - Top 10 revenue-generating products
  - Top 10 high-value customers
  - Regional revenue ranking across Indian commercial centers
  - Month-over-month revenue velocity and peak sales periods
  - Channel distribution across payment methods (order volume vs. revenue contribution)
  - Comprehensive product category performance (revenue, quantity, order count, and AOV)
- **O-6 (Statistical Outlier Detection):** Implement the Interquartile Range (IQR) statistical technique to identify unusually large transaction values and assess distribution skewness.
- **O-7 (NumPy Numerical Analysis):** Use NumPy vectorized mathematical functions to compute the arithmetic mean, median, and standard deviation of transaction values.
- **O-8 (Data Visualization & Reporting):** Generate seven high-resolution, professionally styled charts (line trends, horizontal bar charts, dual-panel distribution graphs, and outlier plots) and export structured CSV summary tables for business consumption.
- **O-9 (Evidence-Based Strategy Formulation):** Formulate five concrete, data-backed commercial recommendations to guide inventory, marketing, and operational decisions.

---

## 5. Project Scope

### 5.1 In-Scope Deliverables

- Ingestion and auditing of the supplied transactional dataset (`01_retail_sales.csv`).
- Comprehensive data inspection: dimensional profiling (`shape`), column schema, data types (`dtypes`), structural info (`df.info()`), head/tail samples, and statistical summaries (`df.describe()`).
- Data cleaning: separate detection of duplicate `Order_ID` entries and exact duplicate records; justified imputation of missing `City` values using `"Unknown"`; verification of `Quantity × Unit_Price` against `Revenue` with correction of arithmetic anomalies.
- Creation and export of the curated dataset (`cleaned_retail_sales.csv`).
- Implementation of all 18 numbered assignment tasks using standard Python, NumPy, and Pandas constructs.
- Statistical anomaly detection using the Interquartile Range (IQR) rule ($Q_1 - 1.5 \times IQR$ to $Q_3 + 1.5 \times IQR$).
- Generation and export of seven visualization charts in PNG format (`outputs/charts/`).
- Export of eight summary analytical tables in CSV format (`outputs/analysis_tables/`).
- Formulation of five non-hardcoded, data-driven commercial recommendations.
- Provision of modular Python code (`src/main.py`), requirements specification (`requirements.txt`), repository configuration (`.gitignore`), and project documentation (`README.md`, `Project_SRS.md`, `Project_SRS.docx`).

### 5.2 Out-of-Scope Elements

- Relational database management systems (RDBMS) or SQL database hosting.
- Real-time streaming data ingestion or API web sockets.
- Machine learning, predictive sales forecasting, or deep learning models.
- Web-based front-end applications, GUI wrappers, or cloud microservice deployments.
- Multi-year comparative analysis beyond the 2025 calendar year.

---

## 6. Dataset Description

The analysis operates on the authentic primary dataset: `01_retail_sales.csv`.

### 6.1 Basic Dataset Parameters

- **File Name:** `01_retail_sales.csv`
- **Initial Dimensionality:** 303 rows × 10 columns (304 lines including header row)
- **Unique Transactions:** 300 unique orders (3 exact duplicate records appended at the end)
- **Temporal Horizon:** Full calendar year 2025 (January 1, 2025 to December 31, 2025)
- **Currency:** Indian Rupee (INR / ₹)

### 6.2 Data Dictionary (Column Schema)

| # | Column Name | Raw Data Type | Cleaned Type | Description | Observed Domain / Range |
|---|---|---|---|---|---|
| 1 | `Order_ID` | String (`object`) | String (`str`) | Unique alphanumeric identifier for each order | `ORD10001` to `ORD10300` |
| 2 | `Customer_ID` | String (`object`) | String (`str`) | Unique identifier representing the purchasing customer | `CUST1001` to `CUST1080` (77 unique customers) |
| 3 | `Product` | String (`object`) | String (`str`) | Commercial name of the specific product item sold | 20 distinct retail items (e.g., Webcam, Headphones, Jeans) |
| 4 | `Product_Category` | String (`object`) | String (`str`) | Broader classification group of the retail product | 4 categories: `Electronics`, `Clothing`, `Home & Kitchen`, `Stationery` |
| 5 | `City` | String (`object`) | String (`str`) | Urban commercial center of the transaction | 8 cities: Agra, Delhi, Ghaziabad, Kanpur, Lucknow, Meerut, Noida, Varanasi (+ `Unknown` for 6 missing records) |
| 6 | `Order_Date` | String (`object`) | Datetime (`datetime64[ns]`) | Calendar date on which the purchase occurred | `2025-01-01` to `2025-12-31` |
| 7 | `Quantity` | Integer (`int64`) | Integer (`int64`) | Total unit count purchased in the order | Integer values ranging from 1 to 5 |
| 8 | `Unit_Price` | Integer (`int64`) | Integer (`int64`) | Monetary price per single product unit in INR | ₹65 to ₹2,649 |
| 9 | `Revenue` | Integer (`int64`) | Float / Integer | Total monetary value of the line item | Raw: ₹65 to ₹11,985; Corrected: ₹65 to ₹11,985 |
| 10 | `Payment_Method` | String (`object`) | String (`str`) | Monetary channel through which payment was cleared | 5 methods: `UPI`, `Credit Card`, `Debit Card`, `Net Banking`, `Cash` |

### 6.3 Identified Data Quality Anomalies

1. **Missing Geographical Data (6 rows):**  
   Records `ORD10010`, `ORD10064`, `ORD10115`, `ORD10131`, `ORD10239`, and `ORD10299` contained null / empty values in the `City` column.  
   *Resolution:* Imputed with `"Unknown"`. Since external geolocation or customer residence cannot be inferred without bias, filling with `"Unknown"` preserves overall revenue and item statistics without fabricating false geographical assignments.
2. **Redundant Duplicate Rows (3 rows):**  
   Rows 300, 301, and 302 were exact duplicate replicas of earlier records (`ORD10191`, `ORD10065`, and `ORD10117`).  
   *Resolution:* Detected via `df.duplicated()` and removed, retaining the initial valid transaction and bringing the clean record count to exactly 300.
3. **Arithmetic Inconsistencies in Revenue (2 rows):**  
   - `ORD10021`: Quantity = 1, Unit_Price = ₹1,686, Recorded Revenue = ₹1,711 (discrepancy of +₹25).  
   - `ORD10295`: Quantity = 1, Unit_Price = ₹1,843, Recorded Revenue = ₹1,868 (discrepancy of +₹25).  
   *Resolution:* Recomputed line totals as `Quantity × Unit_Price` and rectified the discrepancy, ensuring strict arithmetic auditability.

---

## 7. Functional Requirements

The functional requirements cover all 18 numbered assignment tasks:

| Req. ID | Task Title | Description | Input | Expected Output |
|---|---|---|---|---|
| **FR-01** | Dataset Loading & Dimensional Inspection | Ingest raw CSV; verify dimensions, column list, and pandas data types. | `01_retail_sales.csv` | Printed shape (303, 10), column schema, dtypes, `df.info()`, first 5 rows. |
| **FR-02** | Quality Auditing (Missing & Duplicates) | Quantify null values per column; detect exact duplicate rows and duplicate `Order_ID`s separately. | Raw DataFrame | Null value count (City = 6), exact duplicates (3 rows), duplicate IDs identified. |
| **FR-03** | Missing Data Imputation & Deduplication | Impute missing cities with `"Unknown"`; eliminate verified duplicate records. | Raw DataFrame | Cleaned DataFrame with 300 rows and 0 null values; justification documented. |
| **FR-04** | Datetime Parsing & Feature Engineering | Convert `Order_Date` to pandas datetime; extract calendar month integer and weekday name. | Cleaned DataFrame | New columns: `Month` (1–12), `Weekday` (Monday–Sunday); date range verified. |
| **FR-05** | Revenue Audit & Rectification | Compute `Quantity × Unit_Price`; compare with provided `Revenue`; flag and correct discrepancies. | Cleaned DataFrame | Mismatch report (2 rows with +₹25 offset); corrected `Revenue` column; CSV report exported. |
| **FR-06** | Key Metric Formulation | Calculate overall financial KPIs: Total Revenue, Total Volume, Order Count, and AOV. | Validated DataFrame | Total Revenue = ₹623,052; Quantity = 912; Orders = 300; AOV = ₹2,076.84. |
| **FR-07** | Product Revenue Ranking | Aggregate revenue by product; extract top 10 items in descending monetary order. | Validated DataFrame | Ranked table of top 10 products led by Webcam (₹89,792) and Headphones (₹80,256). |
| **FR-08** | Territorial Revenue Segmentation | Group transactions by city; rank all urban centers by aggregate sales revenue. | Validated DataFrame | Ranked city sales table led by Kanpur (₹94,635) and Lucknow (₹92,096). |
| **FR-09** | Monthly Trend & Peak Identification | Aggregate revenue by month; identify best-performing month and seasonality. | Validated DataFrame | Monthly revenue table; peak identified: May (₹78,577); lowest: September (₹37,431). |
| **FR-10** | High-Value Customer Profiling | Group revenue by `Customer_ID`; identify top 10 spending accounts. | Validated DataFrame | Ranked table of top 10 customers led by `CUST1072` (₹24,784) and `CUST1066` (₹23,932). |
| **FR-11** | Payment Channel Evaluation | Compare payment methods by transaction frequency and gross revenue contribution. | Validated DataFrame | Comparative table: UPI dominates (130 orders, ₹283,406; 45.5% revenue share). |
| **FR-12** | IQR Statistical Outlier Detection | Compute $Q_1$, $Q_3$, $IQR = Q_3 - Q_1$, and bounds; filter high-value outliers. | Validated DataFrame | $Q_1 = ₹511.50$, $Q_3 = ₹2,692.75$, Upper Bound = ₹5,964.62; 18 high outliers detected. |
| **FR-13** | Category Groupby Summarization | Group by `Product_Category`; compute aggregate revenue, volume, orders, and AOV. | Validated DataFrame | 4-category summary table: Electronics leads revenue (₹279,698; AOV ₹3,884.69). |
| **FR-14** | NumPy Statistical Characterization | Compute arithmetic mean, median, and population standard deviation using NumPy. | `df['Revenue'].to_numpy()` | `np.mean` = ₹2,076.84, `np.median` = ₹1,268.50, `np.std` = ₹2,200.05 (right-skewed). |
| **FR-15** | Evidence-Based Business Insights | Synthesize analytical findings into five concrete, non-hardcoded business recommendations. | Analytical Outputs | 5 evidence-based recommendations covering products, seasonality, cities, payments, and categories. |
| **FR-16** | Comprehensive Data Inspection | Display first 5 and last 5 records; display numerical and comprehensive descriptive stats. | Cleaned DataFrame | Console display of head, tail, and `df.describe(include='all')`. |
| **FR-17** | Cleaning Process Documentation | Output a structured, human-readable summary documenting every cleaning decision. | Cleaning State Variables | Console table documenting decisions on missing cities, duplicate rows, revenue fixes, dates. |
| **FR-18** | Cleaned Dataset Export | Persist the sanitized, feature-engineered dataset to disk. | Final DataFrame | Exported file: `Retail_Sales_Analysis/data/cleaned_retail_sales.csv` (300 rows, 12 cols). |

---

## 8. Non-Functional Requirements

| Req. ID | Parameter | Requirement Specification |
|---|---|---|
| **NFR-01** | **Execution Performance** | The complete end-to-end analytical pipeline (loading, cleaning, statistical analysis, table export, and chart generation) shall execute in **under 15 seconds** on a standard dual-core laptop with 4 GB RAM. |
| **NFR-02** | **Code Readability & Modularity** | The software shall strictly adhere to PEP 8 standards, utilizing modular functional decomposition, descriptive variable nomenclature, type hints, and explanatory docstrings suitable for academic review. |
| **NFR-03** | **Zero Hard-Coding** | All analytical findings, rankings, statistical parameters, and business recommendations shall be computed dynamically at runtime from data arrays; no analytical numbers shall be hard-coded. |
| **NFR-04** | **Platform Portability** | The code shall execute seamlessly across Windows (PowerShell/CMD), macOS (Zsh), and Linux (Bash) without platform-dependent path errors, leveraging Python's `os.path` module. |
| **NFR-05** | **Visualization Quality** | All Matplotlib/Seaborn graphics shall be rendered with a minimum resolution of **150 DPI**, featuring clear titles, labeled axes, currency formatting, and tight bounding boxes (`bbox_inches='tight'`). |
| **NFR-06** | **Fault Tolerance & Error Handling** | The system shall incorporate structured `try...except` exception handling for missing files (`FileNotFoundError`), empty streams (`EmptyDataError`), and environment anomalies. |
| **NFR-07** | **Data Immutability** | The primary input file (`01_retail_sales.csv`) shall remain strictly read-only and unmutated throughout execution. All transformed data shall be written exclusively to separate target files. |

---

## 9. Tools and Technologies

| Technology | Minimum Version | Specific Role in Project Architecture |
|---|---|---|
| **Python** | 3.8+ (Tested on 3.12+) | Core programming runtime, structured logic, procedural modularity |
| **NumPy** | 1.24+ | Vectorized numerical arrays, statistical metrics (`mean`, `median`, `std`), boolean masks |
| **Pandas** | 2.0+ | Tabular data structures (`DataFrame`, `Series`), CSV I/O, `groupby`, aggregations, datetime parsing |
| **Matplotlib** | 3.7+ | Foundation plotting engine, figure canvases, subplots, tick formatters, file rendering (`Agg` backend) |
| **Seaborn** | 0.12+ | High-level aesthetic themes (`whitegrid`), categorical palettes (`viridis`, `coolwarm`), distribution plots |
| **python-docx** | 1.1+ | Automated generation and compilation of the formal Microsoft Word SRS specification document |
| **Git / GitHub** | 2.30+ | Source code version control, repository staging, branch management, and collaborative tracking |

---

## 10. Methodology

The project adheres to a sequential 7-stage analytical engineering lifecycle:

```
┌────────────────────────────────────────────────────────┐
│  STAGE 1: Ingestion & Inspection (Tasks 1 & 16)        │
│  • Load CSV, verify shape (303×10), dtypes, head/tail  │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 2: Data Auditing & Cleaning (Tasks 2, 3, 5, 17) │
│  • Detect 6 missing cities → Impute "Unknown"          │
│  • Detect & remove 3 exact duplicates → 300 rows       │
│  • Recompute Quantity × Unit_Price → Fix 2 offsets     │
│  • Document all cleaning decisions                     │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 3: Feature Engineering & Export (Tasks 4 & 18)  │
│  • Parse Order_Date to datetime                        │
│  • Extract Month (1-12) and Weekday name               │
│  • Export cleaned_retail_sales.csv (300 rows, 12 cols) │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 4: Aggregations & Segmentation (Tasks 6-11, 13) │
│  • Overall KPIs: Total Rev, Volume, Orders, AOV        │
│  • Groupby: Products, Cities, Months, Customers,       │
│    Payment Methods, and Categories                     │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 5: Statistical & Outlier Analysis (Tasks 12, 14)│
│  • NumPy stats: np.mean, np.median, np.std             │
│  • IQR method: Q1, Q3, IQR, bounds → 18 outliers       │
│  • Skewness evaluation (Mean > Median)                 │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 6: Visualization Suite (7 Core Charts)          │
│  • Monthly trend, Top 10 products, Top 10 customers,   │
│    City revenue, Payment methods, Category revenue,    │
│    Revenue distribution & Outliers                     │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 7: Business Intelligence (Task 15)              │
│  • Synthesize 5 dynamic, evidence-based recommendations│
│    covering inventory, seasonality, regions, payments,  │
│    and product portfolio diversification               │
└────────────────────────────────────────────────────────┘
```

---

## 11. Expected Outcomes

Upon project execution, the system generates the following comprehensive suite of deliverables:

### 11.1 Processed Data Artifacts
- `data/cleaned_retail_sales.csv`: Sanitized, 300-row transactional master table with engineered `Month` and `Weekday` features.

### 11.2 Analytical Summary Tables (`outputs/analysis_tables/`)
1. `top10_products.csv`: Ranked list of the 10 highest-grossing products.
2. `city_revenue.csv`: Complete city-level revenue breakdown and ranking.
3. `monthly_revenue.csv`: Chronological monthly revenue, order count, and volume summary.
4. `top10_customers.csv`: Spending totals and order counts for top customer accounts.
5. `payment_method_analysis.csv`: Distribution of orders and revenue across payment gateways.
6. `category_summary.csv`: Macro-level summary across all 4 product categories.
7. `outliers.csv`: Granular list of all 18 statistical outlier transactions identified via IQR.
8. `revenue_mismatches.csv`: Audit log detailing the 2 identified raw revenue discrepancies.

### 11.3 Graphical Visualizations (`outputs/charts/`)
1. `monthly_revenue_trend.png`: High-resolution line plot tracking 2025 revenue trajectory and peak months.
2. `top10_products_revenue.png`: Horizontal bar chart illustrating revenue contributions of leading items.
3. `top10_customers_spending.png`: Horizontal bar chart profiling the top spending customer accounts.
4. `city_revenue_comparison.png`: Vertical bar chart comparing revenue generation across commercial hubs.
5. `payment_method_distribution.png`: Dual-panel figure (donut chart of order volume + bar chart of revenue).
6. `product_category_revenue.png`: Categorical bar chart highlighting revenue share across industry verticals.
7. `revenue_distribution_outliers.png`: Composite graphic (histogram with KDE, mean/median lines + horizontal boxplot).

---

## 12. Limitations

While the system provides robust academic and operational insights, the analysis is subject to the following contextual constraints:

1. **Sample Size Constraints:** The dataset comprises 300 unique transactional records. While statistically informative for training and regional profiling, it does not represent enterprise-scale Big Data volumes.
2. **Single-Year Time Horizon:** The data spans exclusively from January to December 2025. Consequently, multi-year compounding growth rates (CAGR) and multi-year cyclical patterns cannot be evaluated.
3. **Regional Concentration:** The transactions are concentrated across eight urban centers in Northern and Central India (Uttar Pradesh and Delhi NCR), limiting generalization to pan-Indian or international retail markets.
4. **Absence of Customer Demographics:** The dataset records customer identifiers but omits demographic attributes (age, gender, income bracket, household size), restricting deep customer persona clustering.
5. **Static Batch Execution:** The pipeline processes static historical CSV snapshots rather than live transactional streaming queues or cloud database endpoints.
6. **Descriptive Scope:** The scope focuses on descriptive and diagnostic analytics. It does not incorporate predictive machine learning models (e.g., ARIMA sales forecasting or churn prediction).

---

## 13. Conclusion

The **Retail Sales Performance Analysis** project successfully demonstrates the end-to-end data analytics lifecycle using standard Python data engineering tools. By applying NumPy for vector computations, Pandas for tabular data wrangling and aggregation, and Matplotlib/Seaborn for data storytelling, the project bridges the gap between theoretical classroom programming and practical business problem-solving.

Through this project, the student demonstrates mastery of:
- Inspecting and auditing raw data integrity.
- Defending principled, transparent data cleaning choices.
- Applying feature engineering to extract temporal intelligence.
- Utilizing vectorized operations and groupby aggregations.
- Formulating statistical boundary tests (IQR outlier filtering).
- Producing executive-ready visual assets and structured tabular reports.
- Translating computational findings into actionable commercial strategy.

This project constitutes a robust, verifiable academic portfolio asset fulfilling all requirements of the industrial training curriculum.

---
*End of Software Requirements Specification Document.*
