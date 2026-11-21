# 🛒 Retail Sales Performance Analysis

An end-to-end, professional data analytics and business intelligence project built using **Python**, **NumPy**, **Pandas**, **Matplotlib**, and **Seaborn**.

Developed as part of the **B.Tech Computer Science & Engineering (1st Year)** Industrial Training module on Python and Data Analytics.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Key Objectives](#-key-objectives)
- [Technologies Used](#-technologies-used)
- [Dataset Description](#-dataset-description)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Setup](#-installation--setup)
- [Execution Instructions](#-execution-instructions)
- [Assignment Tasks & Analysis Pipeline](#-assignment-tasks--analysis-pipeline)
- [Summary of Key Findings](#-summary-of-key-findings)
- [Evidence-Based Business Recommendations](#-evidence-based-business-recommendations)
- [Generated Outputs & Deliverables](#-generated-outputs--deliverables)
- [Project Limitations](#-project-limitations)
- [GitHub Setup Instructions](#-github-setup-instructions)
- [Author & License](#-author--license)

---

## 📌 Project Overview

This project provides an automated, modular data analysis pipeline applied to an authentic industrial retail sales dataset (`01_retail_sales.csv`). The dataset contains 303 raw transactional orders across 8 commercial centers in Northern India during the calendar year 2025.

The pipeline performs rigorous data quality auditing (identifying missing values, exact duplicate rows, and arithmetic price-volume discrepancies), cleanses and sanitizes the data without fabricating artificial points, parses datetime features, aggregates sales across multiple dimensions (products, categories, cities, months, customers, and payment methods), calculates statistical dispersion and detects outliers using the Interquartile Range (IQR) method, and generates executive-grade visual charts and summary tables.

---

## 🎯 Key Objectives

1. **Integrity Auditing & Cleansing:** Ingest raw CSV data, identify data quality defects, impute missing geographic locations transparently with `"Unknown"`, eliminate duplicate rows, and correct arithmetic line-item mismatches.
2. **Feature Engineering:** Parse raw date strings into standard datetime objects and extract temporal attributes (`Month` and `Weekday`) for chronological analysis.
3. **Core Financial KPIs:** Quantify Total Gross Revenue, Total Units Sold, Order Count, and Average Order Value (AOV).
4. **Multi-Dimensional Segmentation:** Aggregate sales performance across top products, leading customers, regional cities, monthly seasonality, payment methods, and product categories.
5. **Statistical Characterization:** Utilize **NumPy** for vector operations (`mean`, `median`, `std`) and evaluate distribution skewness.
6. **Outlier Detection:** Implement the statistical Interquartile Range (IQR) technique to detect unusually high-value transactions.
7. **Publication-Quality Visualizations:** Export 7 high-resolution charts (150 DPI) with clear legends and value annotations.
8. **Business Intelligence:** Synthesize 5 data-driven, actionable recommendations to optimize inventory, marketing, and operational fulfillment.

---

## 🛠️ Technologies Used

| Technology | Minimum Version | Specific Role in Architecture |
|---|---|---|
| **Python** | `3.8+` (Tested on 3.12+) | Core programming language, procedural modularity, workflow logic |
| **NumPy** | `1.24+` | Vectorized mathematical operations, statistical metrics (`mean`, `median`, `std`) |
| **Pandas** | `2.0+` | DataFrame data wrangling, CSV I/O, `groupby` aggregations, date handling |
| **Matplotlib** | `3.7+` | Canvas generation, axes formatting, figure rendering (`Agg` backend) |
| **Seaborn** | `0.12+` | Statistical visualizations, `whitegrid` styling, color palettes (`viridis`, `coolwarm`) |
| **python-docx** | `1.1+` | Automated generation of the formal Word SRS document |

---

## 📊 Dataset Description

- **Raw Data File:** `data/01_retail_sales.csv`
- **Initial Shape:** 303 rows × 10 columns (304 lines including header)
- **Sanitized Dataset:** 300 unique orders (3 duplicate rows removed)
- **Temporal Horizon:** Full calendar year 2025 (`2025-01-01` to `2025-12-31`)
- **Geographic Coverage:** 8 commercial hubs (Agra, Delhi, Ghaziabad, Kanpur, Lucknow, Meerut, Noida, Varanasi)

### Column Schema

| # | Column Name | Raw Data Type | Cleaned Type | Description | Observed Range |
|---|---|---|---|---|---|
| 1 | `Order_ID` | `object` | `str` | Unique transaction identifier | `ORD10001` – `ORD10300` |
| 2 | `Customer_ID` | `object` | `str` | Unique customer account ID | `CUST1001` – `CUST1080` (77 unique) |
| 3 | `Product` | `object` | `str` | Specific product name | 20 distinct retail items |
| 4 | `Product_Category` | `object` | `str` | Retail department | Electronics, Clothing, Home & Kitchen, Stationery |
| 5 | `City` | `object` | `str` | City of purchase | 8 cities + `Unknown` (6 missing imputed) |
| 6 | `Order_Date` | `object` | `datetime64[ns]` | Transaction date | `2025-01-01` – `2025-12-31` |
| 7 | `Quantity` | `int64` | `int64` | Units purchased | 1 – 5 units |
| 8 | `Unit_Price` | `int64` | `int64` | Price per unit (INR) | ₹65 – ₹2,649 |
| 9 | `Revenue` | `int64` | `float64` / `int64` | Line total (INR) | ₹65 – ₹11,985 (corrected via $Q \times P$) |
| 10 | `Payment_Method` | `object` | `str` | Payment channel | UPI, Credit Card, Debit Card, Net Banking, Cash |

### Data Quality Decisions Documented

1. **Missing Cities (6 rows):** `ORD10010`, `ORD10064`, `ORD10115`, `ORD10131`, `ORD10239`, `ORD10299` had null values. Imputed with `"Unknown"` to maintain data integrity without inventing fictional locations.
2. **Exact Duplicate Records (3 rows):** Rows 300 (`ORD10191`), 301 (`ORD10065`), and 302 (`ORD10117`) were exact duplicate copies. Removed to restore the true count of 300 unique orders.
3. **Revenue Arithmetic Mismatches (2 rows):** `ORD10021` (recorded ₹1,711 vs. calculated ₹1,686) and `ORD10295` (recorded ₹1,868 vs. calculated ₹1,843) exhibited an unexplained +₹25 offset. Corrected to `Quantity × Unit_Price`.

---

## 📁 Project Directory Structure

```
Retail_Sales_Analysis/
│
├── data/
│   ├── 01_retail_sales.csv            # Original raw dataset (read-only, untouched)
│   └── cleaned_retail_sales.csv       # Sanitized & feature-engineered dataset (300 rows, 12 cols)
│
├── src/
│   └── main.py                        # Complete, self-contained modular analysis pipeline
│
├── outputs/
│   ├── charts/                        # 7 High-resolution PNG visualizations (150 DPI)
│   │   ├── city_revenue_comparison.png
│   │   ├── monthly_revenue_trend.png
│   │   ├── payment_method_distribution.png
│   │   ├── product_category_revenue.png
│   │   ├── revenue_distribution_outliers.png
│   │   ├── top10_customers_spending.png
│   │   └── top10_products_revenue.png
│   │
│   └── analysis_tables/               # 8 Summary CSV analytical tables
│       ├── category_summary.csv
│       ├── city_revenue.csv
│       ├── monthly_revenue.csv
│       ├── outliers.csv
│       ├── payment_method_analysis.csv
│       ├── revenue_mismatches.csv
│       ├── top10_customers.csv
│       └── top10_products.csv
│
├── SRS/
│   ├── Project_SRS.docx               # Professional Microsoft Word SRS document
│   ├── Project_SRS.md                 # Markdown version of the SRS specification
│   └── generate_docx.py               # Automated Word document generator script
│
├── README.md                          # Comprehensive project documentation
├── requirements.txt                   # Exact Python dependencies
└── .gitignore                         # Version control ignore definitions
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher installed
- Git version control installed

### 2. Environment Setup

```bash
# Navigate to the project root directory
cd Retail_Sales_Analysis

# Create a dedicated virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows Command Prompt:
venv\Scripts\activate.bat
# On Linux / macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## 🚀 Execution Instructions

Run the complete pipeline from start to finish:

```bash
# Option 1: Run directly from project root
python src/main.py

# Option 2: Run from inside src directory
cd src
python main.py
```

### What Happens During Execution:
- Ingests and inspects `01_retail_sales.csv`.
- Performs all data quality audits and displays cleaning summaries.
- Exports `data/cleaned_retail_sales.csv`.
- Executes all 18 numbered assignment tasks sequentially.
- Computes statistical metrics with NumPy and IQR outlier detection.
- Generates 8 analytical CSV tables in `outputs/analysis_tables/`.
- Renders and saves 7 publication-grade PNG charts in `outputs/charts/`.
- Prints executive-level business recommendations and final task checklists.
- Average execution time: **~9 seconds**.

---

## 📈 Assignment Tasks & Analysis Pipeline

All 18 numbered requirements from the assignment are fully implemented:

| Task # | Analysis Description | Implemented Function | Output Artifact |
|---|---|---|---|
| **Task 1** | Ingest CSV, inspect dimensions, columns, and data types | `load_and_inspect()` | Console shape (303, 10), schema, dtypes, info |
| **Task 2** | Identify missing values and duplicate orders | `identify_quality_issues()` | Identified 6 missing cities, 3 exact duplicates |
| **Task 3** | Clean missing cities (impute "Unknown") & deduplicate | `clean_missing_cities()`, `remove_duplicates()` | Cleaned 300 rows, 0 nulls |
| **Task 4** | Convert `Order_Date` to datetime; extract Month & Weekday | `convert_dates()` | Engineered `Month` (1–12) and `Weekday` |
| **Task 5** | Verify row-wise revenue ($Q \times P$ vs. Revenue) | `validate_revenue()` | Corrected 2 mismatches; `revenue_mismatches.csv` |
| **Task 6** | Calculate Total Revenue, Quantity, and Average Order Value | `overall_metrics()` | Total: ₹623,052; Qty: 912; AOV: ₹2,076.84 |
| **Task 7** | Find top 10 products with highest revenue | `top10_products()` | `top10_products.csv`, chart generated |
| **Task 8** | Rank all cities by revenue | `city_revenue()` | `city_revenue.csv`, chart generated |
| **Task 9** | Calculate monthly revenue and identify peak month | `monthly_revenue()` | `monthly_revenue.csv`; Peak: May (₹78,577) |
| **Task 10** | Find top 10 customers by total spending | `top10_customers()` | `top10_customers.csv`, chart generated |
| **Task 11** | Compare payment methods by order count and revenue | `payment_method_analysis()` | `payment_method_analysis.csv`, chart generated |
| **Task 12** | Detect unusually large order values using IQR method | `detect_outliers()` | `outliers.csv` (18 outliers detected) |
| **Task 13** | Product category summary using Pandas groupby | `category_summary()` | `category_summary.csv`, chart generated |
| **Task 14** | NumPy statistical metrics (mean, median, std dev) | `numpy_statistics()` | Mean: ₹2,076.84, Median: ₹1,268.50, Std: ₹2,200.05 |
| **Task 15** | Five evidence-based commercial recommendations | `generate_recommendations()` | Console printout of 5 dynamic recommendations |
| **Task 16** | Detailed data inspection (head, tail, descriptive stats) | `data_inspection()` | Console summary of head, tail, `df.describe()` |
| **Task 17** | Document all data cleaning decisions with justification | `document_cleaning()` | Console documentation summary box |
| **Task 18** | Save sanitized dataset to disk | `save_cleaned_data()` | `data/cleaned_retail_sales.csv` |

---

## 🔍 Summary of Key Findings

All figures below are computed dynamically from `01_retail_sales.csv`:

### 1. Macro KPIs
- **Gross Revenue:** ₹623,052.00
- **Total Units Sold:** 912 units
- **Total Clean Orders:** 300 orders
- **Average Order Value (AOV):** ₹2,076.84

### 2. Product Leadership
- **Top Product by Revenue:** **Webcam** (₹89,792.00 — 14.4% of total sales)
- **Top 5 Products:**
  1. Webcam: ₹89,792.00
  2. Headphones: ₹80,256.00
  3. Jeans: ₹58,843.00
  4. Keyboard: ₹55,708.00
  5. Backpack: ₹51,743.00

### 3. Category Breakdown
- **Electronics:** ₹279,698.00 (72 orders, 224 units, AOV: ₹3,884.69) — *44.9% Revenue Share*
- **Clothing:** ₹181,464.00 (65 orders, 185 units, AOV: ₹2,791.75) — *29.1% Revenue Share*
- **Home & Kitchen:** ₹107,721.00 (75 orders, 230 units, AOV: ₹1,436.28) — *17.3% Revenue Share*
- **Stationery:** ₹54,169.00 (88 orders, 273 units, AOV: ₹615.56) — *8.7% Revenue Share*

### 4. Regional Distribution
- **Top City:** **Kanpur** (₹94,635.00)
- **Second Top City:** **Lucknow** (₹92,096.00)
- **Third Top City:** **Agra** (₹87,589.00)
- **Lowest Verified City:** **Delhi** (₹55,428.00)
- **Unverified Records (`Unknown`):** ₹8,640.00 across 6 orders

### 5. Temporal & Seasonal Velocity
- **Best Month:** **May 2025** (₹78,577.00 across 34 orders)
- **Second Best Month:** **June 2025** (₹70,347.00 across 32 orders)
- **Slowest Month:** **September 2025** (₹37,431.00 across 19 orders)

### 6. Payment Channels
- **UPI:** 130 orders (43.3% order volume), ₹283,406.00 revenue (45.5% revenue share, AOV: ₹2,180.05)
- **Credit Card:** 57 orders, ₹104,453.00 revenue (AOV: ₹1,832.51)
- **Debit Card:** 47 orders, ₹113,845.00 revenue (AOV: ₹2,422.23)
- **Cash:** 34 orders, ₹57,441.00 revenue (AOV: ₹1,689.44)
- **Net Banking:** 32 orders, ₹63,907.00 revenue (AOV: ₹1,997.09)

### 7. Statistical & Anomaly Metrics
- **Mean Revenue:** ₹2,076.84
- **Median Revenue:** ₹1,268.50
- **Standard Deviation:** ₹2,200.05
- **Distribution Skewness:** Positive right-skew ($\text{Mean} > \text{Median}$), driven by premium electronics orders.
- **IQR Outlier Bounds:** $Q_1 = ₹511.50$, $Q_3 = ₹2,692.75$, $IQR = ₹2,181.25$, $\text{Upper Bound} = ₹5,964.62$.
- **Outliers Detected:** 18 transactions exceeded ₹5,964.62 (peak transaction: `ORD10086`, Webcam purchase of ₹11,985.00).

---

## 💡 Evidence-Based Business Recommendations

1. **Prioritize High-Margin Tech Inventory:**  
   Webcams and Headphones collectively generate ₹170,048 (27.3% of enterprise revenue). Maintain safety stock for the top 5 electronic items and bundle them with accessories (mouse pads, USB cables) to expand transaction basket sizes.
2. **Capitalize on Mid-Year Seasonality:**  
   May and June generate over ₹148,900 in sales. Secure supplier inventory discounts in March/April and staff logistics hubs to meet the May surge. Conversely, run back-to-school promotional campaigns in September to offset the annual sales dip.
3. **Regional Expansion in Central UP Hubs:**  
   Kanpur (₹94,635) and Lucknow (₹92,096) represent the strongest geographical markets. Establish dedicated micro-fulfillment hubs in Kanpur and Lucknow for same-day delivery. Furthermore, introduce localized promotions in Delhi to address underperformance.
4. **Optimize Checkout for UPI Dominance:**  
   With UPI processing 43.3% of orders and 45.5% of total revenue, partner with UPI payment gateways to ensure 99.9% uptime and zero-drop checkout flows. Offer 2% instant cashback on credit/debit cards to diversify settlement channels.
5. **Enforce Mandatory Address Capture:**  
   Six customer transactions (₹8,640) lacked city data. Enforce mandatory postal PIN code validation at web checkout to eliminate unallocated regional revenue.

---

## 📦 Generated Outputs & Deliverables

### Charts (`outputs/charts/`)
- `monthly_revenue_trend.png`: Chronological monthly revenue curve highlighting the May peak.
- `top10_products_revenue.png`: Horizontal bar chart of top 10 items led by Webcams and Headphones.
- `top10_customers_spending.png`: Customer value ranking profiling high-spending accounts.
- `city_revenue_comparison.png`: Territorial comparison of sales across commercial centers.
- `payment_method_distribution.png`: Dual-panel figure showing order share (pie) and revenue contribution (bar).
- `product_category_revenue.png`: Visual breakdown of revenue share across the 4 retail categories.
- `revenue_distribution_outliers.png`: Dual distribution graph (histogram with KDE + box plot with outliers).

### Analytical Tables (`outputs/analysis_tables/`)
- `category_summary.csv`, `city_revenue.csv`, `monthly_revenue.csv`, `outliers.csv`, `payment_method_analysis.csv`, `revenue_mismatches.csv`, `top10_customers.csv`, `top10_products.csv`.

### Specifications & Documentation (`SRS/`)
- `Project_SRS.docx`: Formatted Microsoft Word Software Requirements Specification document.
- `Project_SRS.md`: Complete Markdown SRS specification document.

---

## ⚠️ Project Limitations

1. **Sample Scope:** The dataset contains 300 unique transactional records. While statistically sufficient for descriptive training, it does not represent enterprise Big Data scale.
2. **Single-Year Snapshot:** Covers January 1, 2025 to December 31, 2025; multi-year compound annual growth rates (CAGR) cannot be established.
3. **Geographical Concentration:** Limited to Northern/Central India (UP and NCR); trends cannot be directly generalized nationwide.
4. **Missing Demographic Dimensions:** Omission of customer age, gender, and income precludes behavioral persona clustering.
5. **Static Batch Execution:** Processes historical CSV files rather than continuous live data streams.
6. **Descriptive Analytics Focus:** Does not include predictive machine learning algorithms (e.g., time-series ARIMA forecasting).

---

## 🔧 GitHub Setup Instructions

To push this project to your GitHub profile:

```bash
# 1. Open terminal inside the project directory
cd Retail_Sales_Analysis

# 2. Initialize local Git repository
git init

# 3. Stage all project files
git add .

# 4. Commit the staged files
git commit -m "feat: complete Retail Sales Performance Analysis project"

# 5. Create a new repository on your GitHub account (e.g., named 'retail-sales-analysis')
# Then link your local repository to GitHub:
git remote add origin https://github.com/<your-username>/retail-sales-analysis.git

# 6. Set main branch and push
git branch -M main
git push -u origin main
```

---

## 👤 Author & Academic Details

- **Student Name:** Nitish Patel
- **Academic Degree:** B.Tech Computer Science & Engineering (1st Year)
- **Curriculum:** Industrial Training in Python, NumPy & Pandas
- **Academic Year:** 2025–2026

## 📄 License

This academic project is open-source and licensed under the [MIT License](LICENSE).
