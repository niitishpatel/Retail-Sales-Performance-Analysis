"""
Retail Sales Performance Analysis
==================================
A comprehensive analysis of retail sales data including data cleaning,
exploratory analysis, visualizations, and business recommendations.

Author: Nitish Patel
"""

# Set matplotlib backend BEFORE any other matplotlib imports
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PATH CONFIGURATION
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_CSV = os.path.join(DATA_DIR, "01_retail_sales.csv")
CLEANED_CSV = os.path.join(DATA_DIR, "cleaned_retail_sales.csv")
CHARTS_DIR = os.path.join(BASE_DIR, "outputs", "charts")
TABLES_DIR = os.path.join(BASE_DIR, "outputs", "analysis_tables")

# ─────────────────────────────────────────────────────────────
# STYLE CONFIGURATION
# ─────────────────────────────────────────────────────────────
sns.set_style("whitegrid")
PALETTE = sns.color_palette("viridis", 12)
ACCENT = "#2196F3"
TITLE_SIZE = 14
LABEL_SIZE = 11
DPI = 150


def ensure_directories():
    """Create output directories if they don't exist."""
    for d in [CHARTS_DIR, TABLES_DIR]:
        os.makedirs(d, exist_ok=True)
        print(f"  ✔ Directory ready: {d}")


# ═══════════════════════════════════════════════════════════════
# TASK 1 — Load & Inspect
# ═══════════════════════════════════════════════════════════════
def load_and_inspect(filepath):
    """Load the CSV and print shape, columns, dtypes, info, head."""
    print("\n" + "=" * 70)
    print("TASK 1: LOADING & INSPECTING THE DATASET")
    print("=" * 70)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at: {filepath}")

    df = pd.read_csv(filepath)
    print(f"\n📂 Loaded file : {filepath}")
    print(f"📐 Shape        : {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n📋 Columns ({len(df.columns)}):")
    for col in df.columns:
        print(f"   • {col}")

    print("\n📊 Data Types:")
    print(df.dtypes.to_string())

    print("\n📊 DataFrame Info:")
    df.info()

    print("\n🔍 First 5 rows:")
    print(df.head().to_string())

    return df


# ═══════════════════════════════════════════════════════════════
# TASK 16 — Data Inspection (first/last 5 rows, describe)
# ═══════════════════════════════════════════════════════════════
def data_inspection(df):
    """Display first/last 5 rows and descriptive statistics."""
    print("\n" + "=" * 70)
    print("TASK 16: DETAILED DATA INSPECTION")
    print("=" * 70)

    print("\n🔍 First 5 rows:")
    print(df.head().to_string())

    print("\n🔍 Last 5 rows:")
    print(df.tail().to_string())

    print("\n📈 Descriptive Statistics:")
    print(df.describe().to_string())

    print("\n📈 Descriptive Statistics (all columns):")
    print(df.describe(include='all').to_string())


# ═══════════════════════════════════════════════════════════════
# TASK 2 — Identify Missing Values & Duplicates
# ═══════════════════════════════════════════════════════════════
def identify_quality_issues(df):
    """Find missing values and duplicate rows/Order_IDs."""
    print("\n" + "=" * 70)
    print("TASK 2: IDENTIFYING DATA QUALITY ISSUES")
    print("=" * 70)

    # --- Missing values ---
    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(f"\n❓ Missing Values per Column (total = {total_missing}):")
    print(missing.to_string())

    if total_missing > 0:
        cols_with_missing = missing[missing > 0]
        for col, count in cols_with_missing.items():
            print(f"\n  ⚠ Column '{col}' has {count} missing value(s):")
            missing_rows = df[df[col].isnull()]
            for _, row in missing_rows.iterrows():
                print(f"    - Order_ID: {row['Order_ID']}")

    # --- Exact duplicate rows ---
    exact_dups = df[df.duplicated(keep='first')]
    print(f"\n🔁 Exact Duplicate Rows: {len(exact_dups)}")
    if len(exact_dups) > 0:
        for _, row in exact_dups.iterrows():
            print(f"    - Order_ID: {row['Order_ID']} (row index {row.name})")

    # --- Duplicate Order_IDs (regardless of other columns) ---
    dup_ids = df[df.duplicated(subset=['Order_ID'], keep=False)]
    unique_dup_ids = dup_ids['Order_ID'].unique()
    print(f"\n🆔 Duplicate Order_IDs: {len(unique_dup_ids)} unique IDs appearing more than once")
    for oid in unique_dup_ids:
        indices = df[df['Order_ID'] == oid].index.tolist()
        print(f"    - {oid} appears at row indices: {indices}")

    return missing, exact_dups


# ═══════════════════════════════════════════════════════════════
# TASK 3 — Clean Missing City Values
# ═══════════════════════════════════════════════════════════════
def clean_missing_cities(df):
    """Fill missing City values with 'Unknown'."""
    print("\n" + "=" * 70)
    print("TASK 3: CLEANING MISSING CITY VALUES")
    print("=" * 70)

    missing_city_count = df['City'].isnull().sum()
    print(f"\n  Missing City values before cleaning: {missing_city_count}")

    if missing_city_count > 0:
        missing_orders = df.loc[df['City'].isnull(), 'Order_ID'].tolist()
        print(f"  Affected Order_IDs: {missing_orders}")

    # Fill with "Unknown"
    df['City'] = df['City'].fillna("Unknown")

    print(f"  Missing City values after cleaning : {df['City'].isnull().sum()}")
    print("\n  ✅ Justification: We cannot infer the actual city from the available")
    print("     data. Inventing locations would be dishonest. Filling with 'Unknown'")
    print("     preserves data integrity while keeping these rows in the analysis.")

    return df


# ═══════════════════════════════════════════════════════════════
# TASK 3 (cont.) — Remove Exact Duplicate Rows
# ═══════════════════════════════════════════════════════════════
def remove_duplicates(df):
    """Remove exact duplicate rows, keeping the first occurrence."""
    print("\n" + "=" * 70)
    print("TASK 3 (cont.): REMOVING DUPLICATE ROWS")
    print("=" * 70)

    before = len(df)
    df = df.drop_duplicates(keep='first').reset_index(drop=True)
    after = len(df)
    removed = before - after

    print(f"\n  Rows before : {before}")
    print(f"  Rows after  : {after}")
    print(f"  Removed     : {removed} exact duplicate row(s)")

    return df


# ═══════════════════════════════════════════════════════════════
# TASK 4 — Convert Order_Date, Extract Month & Weekday
# ═══════════════════════════════════════════════════════════════
def convert_dates(df):
    """Convert Order_Date to datetime; extract month number and weekday name."""
    print("\n" + "=" * 70)
    print("TASK 4: DATE CONVERSION & FEATURE EXTRACTION")
    print("=" * 70)

    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Month'] = df['Order_Date'].dt.month
    df['Weekday'] = df['Order_Date'].dt.day_name()

    print(f"\n  Order_Date dtype : {df['Order_Date'].dtype}")
    print(f"  Date range       : {df['Order_Date'].min().date()} → {df['Order_Date'].max().date()}")
    print(f"  Months present   : {sorted(df['Month'].unique())}")
    print(f"  Weekdays present : {df['Weekday'].unique().tolist()}")

    return df


# ═══════════════════════════════════════════════════════════════
# TASK 5 — Revenue Validation
# ═══════════════════════════════════════════════════════════════
def validate_revenue(df):
    """Calculate Quantity × Unit_Price, compare with Revenue, flag mismatches."""
    print("\n" + "=" * 70)
    print("TASK 5: REVENUE VALIDATION (Quantity × Unit_Price vs Revenue)")
    print("=" * 70)

    df['Calculated_Revenue'] = df['Quantity'] * df['Unit_Price']
    df['Revenue_Mismatch'] = ~np.isclose(df['Revenue'], df['Calculated_Revenue'], atol=0.01)

    mismatches = df[df['Revenue_Mismatch']]
    print(f"\n  Total orders checked : {len(df)}")
    print(f"  Mismatches found     : {len(mismatches)}")

    if len(mismatches) > 0:
        print("\n  ⚠ Revenue Mismatch Details:")
        for _, row in mismatches.iterrows():
            diff = row['Revenue'] - row['Calculated_Revenue']
            print(f"    - {row['Order_ID']}: {int(row['Quantity'])} × {row['Unit_Price']}"
                  f" = {row['Calculated_Revenue']:.0f}, but Revenue = {row['Revenue']:.0f}"
                  f" (difference = {diff:+.0f})")

        # Save mismatches to CSV
        mismatch_df = mismatches[['Order_ID', 'Product', 'Quantity', 'Unit_Price',
                                   'Revenue', 'Calculated_Revenue']].copy()
        mismatch_df['Difference'] = mismatch_df['Revenue'] - mismatch_df['Calculated_Revenue']
        mismatch_path = os.path.join(TABLES_DIR, "revenue_mismatches.csv")
        mismatch_df.to_csv(mismatch_path, index=False)
        print(f"\n  💾 Saved mismatch details → {mismatch_path}")

    # Correct the Revenue column using Calculated_Revenue
    df['Revenue'] = df['Calculated_Revenue']
    print("\n  ✅ Revenue column corrected using Calculated_Revenue (Quantity × Unit_Price).")

    return df


# ═══════════════════════════════════════════════════════════════
# TASK 6 — Total Revenue, Total Quantity, Avg Order Value
# ═══════════════════════════════════════════════════════════════
def overall_metrics(df):
    """Calculate total revenue, total quantity, and average order value."""
    print("\n" + "=" * 70)
    print("TASK 6: OVERALL SALES METRICS")
    print("=" * 70)

    total_revenue = df['Revenue'].sum()
    total_quantity = df['Quantity'].sum()
    num_orders = len(df)
    avg_order_value = total_revenue / num_orders

    print(f"\n  💰 Total Revenue       : ₹{total_revenue:,.2f}")
    print(f"  📦 Total Quantity Sold : {total_quantity:,}")
    print(f"  🧾 Number of Orders   : {num_orders:,}")
    print(f"  📊 Avg. Order Value    : ₹{avg_order_value:,.2f}")

    return total_revenue, total_quantity, avg_order_value


# ═══════════════════════════════════════════════════════════════
# TASK 7 — Top 10 Products by Revenue
# ═══════════════════════════════════════════════════════════════
def top10_products(df):
    """Find top 10 products by total revenue."""
    print("\n" + "=" * 70)
    print("TASK 7: TOP 10 PRODUCTS BY TOTAL REVENUE")
    print("=" * 70)

    product_revenue = (df.groupby('Product')['Revenue']
                       .sum()
                       .sort_values(ascending=False))
    top10 = product_revenue.head(10).reset_index()
    top10.columns = ['Product', 'Total_Revenue']
    top10['Rank'] = range(1, len(top10) + 1)

    print()
    for _, row in top10.iterrows():
        print(f"  {row['Rank']:>2}. {row['Product']:<25} ₹{row['Total_Revenue']:>12,.2f}")

    # Save to CSV
    save_path = os.path.join(TABLES_DIR, "top10_products.csv")
    top10.to_csv(save_path, index=False)
    print(f"\n  💾 Saved → {save_path}")

    return top10


# ═══════════════════════════════════════════════════════════════
# TASK 8 — City-wise Revenue Ranking
# ═══════════════════════════════════════════════════════════════
def city_revenue(df):
    """Rank cities by total revenue."""
    print("\n" + "=" * 70)
    print("TASK 8: CITY-WISE REVENUE RANKING")
    print("=" * 70)

    city_rev = (df.groupby('City')['Revenue']
                .sum()
                .sort_values(ascending=False)
                .reset_index())
    city_rev.columns = ['City', 'Total_Revenue']
    city_rev['Rank'] = range(1, len(city_rev) + 1)

    print()
    for _, row in city_rev.iterrows():
        print(f"  {row['Rank']:>2}. {row['City']:<20} ₹{row['Total_Revenue']:>12,.2f}")

    save_path = os.path.join(TABLES_DIR, "city_revenue.csv")
    city_rev.to_csv(save_path, index=False)
    print(f"\n  💾 Saved → {save_path}")

    return city_rev


# ═══════════════════════════════════════════════════════════════
# TASK 9 — Monthly Revenue & Best Month
# ═══════════════════════════════════════════════════════════════
def monthly_revenue(df):
    """Calculate monthly revenue and identify the best month."""
    print("\n" + "=" * 70)
    print("TASK 9: MONTHLY REVENUE ANALYSIS")
    print("=" * 70)

    monthly = (df.groupby('Month')['Revenue']
               .sum()
               .sort_index()
               .reset_index())
    monthly.columns = ['Month', 'Total_Revenue']

    # Month names for display
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    monthly['Month_Name'] = monthly['Month'].map(month_names)

    print()
    for _, row in monthly.iterrows():
        print(f"  {row['Month_Name']:<12} ₹{row['Total_Revenue']:>12,.2f}")

    best_idx = monthly['Total_Revenue'].idxmax()
    best_month = monthly.loc[best_idx]
    print(f"\n  🏆 Best Month: {best_month['Month_Name']} with ₹{best_month['Total_Revenue']:,.2f}")

    save_path = os.path.join(TABLES_DIR, "monthly_revenue.csv")
    monthly.to_csv(save_path, index=False)
    print(f"\n  💾 Saved → {save_path}")

    return monthly


# ═══════════════════════════════════════════════════════════════
# TASK 10 — Top 10 Customers by Spending
# ═══════════════════════════════════════════════════════════════
def top10_customers(df):
    """Find the top 10 customers by total spending."""
    print("\n" + "=" * 70)
    print("TASK 10: TOP 10 CUSTOMERS BY TOTAL SPENDING")
    print("=" * 70)

    cust_spending = (df.groupby('Customer_ID')['Revenue']
                     .sum()
                     .sort_values(ascending=False))
    top10 = cust_spending.head(10).reset_index()
    top10.columns = ['Customer_ID', 'Total_Spending']
    top10['Rank'] = range(1, len(top10) + 1)

    print()
    for _, row in top10.iterrows():
        print(f"  {row['Rank']:>2}. {row['Customer_ID']:<15} ₹{row['Total_Spending']:>12,.2f}")

    save_path = os.path.join(TABLES_DIR, "top10_customers.csv")
    top10.to_csv(save_path, index=False)
    print(f"\n  💾 Saved → {save_path}")

    return top10


# ═══════════════════════════════════════════════════════════════
# TASK 11 — Payment Method Comparison
# ═══════════════════════════════════════════════════════════════
def payment_method_analysis(df):
    """Compare payment methods by order count and total revenue."""
    print("\n" + "=" * 70)
    print("TASK 11: PAYMENT METHOD COMPARISON")
    print("=" * 70)

    payment = df.groupby('Payment_Method').agg(
        Order_Count=('Order_ID', 'count'),
        Total_Revenue=('Revenue', 'sum'),
        Avg_Order_Value=('Revenue', 'mean')
    ).sort_values('Total_Revenue', ascending=False).reset_index()

    print()
    print(f"  {'Payment Method':<20} {'Orders':>8} {'Total Revenue':>15} {'Avg Value':>12}")
    print("  " + "-" * 58)
    for _, row in payment.iterrows():
        print(f"  {row['Payment_Method']:<20} {row['Order_Count']:>8}"
              f" ₹{row['Total_Revenue']:>13,.2f} ₹{row['Avg_Order_Value']:>10,.2f}")

    save_path = os.path.join(TABLES_DIR, "payment_method_analysis.csv")
    payment.to_csv(save_path, index=False)
    print(f"\n  💾 Saved → {save_path}")

    return payment


# ═══════════════════════════════════════════════════════════════
# TASK 12 — Outlier Detection (IQR Method)
# ═══════════════════════════════════════════════════════════════
def detect_outliers(df):
    """Find unusually large order values using the IQR method."""
    print("\n" + "=" * 70)
    print("TASK 12: OUTLIER DETECTION (IQR METHOD)")
    print("=" * 70)

    Q1 = df['Revenue'].quantile(0.25)
    Q3 = df['Revenue'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f"\n  Q1 (25th percentile) : ₹{Q1:,.2f}")
    print(f"  Q3 (75th percentile) : ₹{Q3:,.2f}")
    print(f"  IQR                  : ₹{IQR:,.2f}")
    print(f"  Lower Bound          : ₹{lower_bound:,.2f}")
    print(f"  Upper Bound          : ₹{upper_bound:,.2f}")

    outliers = df[(df['Revenue'] < lower_bound) | (df['Revenue'] > upper_bound)]
    print(f"\n  🔴 Outliers Found: {len(outliers)}")

    if len(outliers) > 0:
        print(f"\n  {'Order_ID':<12} {'Product':<25} {'Revenue':>10}")
        print("  " + "-" * 50)
        for _, row in outliers.iterrows():
            tag = "HIGH" if row['Revenue'] > upper_bound else "LOW"
            print(f"  {row['Order_ID']:<12} {row['Product']:<25} ₹{row['Revenue']:>8,.0f}  [{tag}]")

    outlier_df = outliers[['Order_ID', 'Product', 'Product_Category', 'City',
                           'Quantity', 'Unit_Price', 'Revenue']].copy()
    outlier_df['Outlier_Type'] = outlier_df['Revenue'].apply(
        lambda x: 'Above Upper Bound' if x > upper_bound else 'Below Lower Bound')

    save_path = os.path.join(TABLES_DIR, "outliers.csv")
    outlier_df.to_csv(save_path, index=False)
    print(f"\n  💾 Saved → {save_path}")

    return outlier_df, lower_bound, upper_bound


# ═══════════════════════════════════════════════════════════════
# TASK 13 — Product Category Summary
# ═══════════════════════════════════════════════════════════════
def category_summary(df):
    """Create a grouped summary for each Product_Category."""
    print("\n" + "=" * 70)
    print("TASK 13: PRODUCT CATEGORY SUMMARY")
    print("=" * 70)

    cat_summary = df.groupby('Product_Category').agg(
        Total_Revenue=('Revenue', 'sum'),
        Total_Quantity=('Quantity', 'sum'),
        Num_Orders=('Order_ID', 'count'),
        Avg_Order_Value=('Revenue', 'mean')
    ).sort_values('Total_Revenue', ascending=False).reset_index()

    print()
    print(f"  {'Category':<20} {'Revenue':>12} {'Qty':>6} {'Orders':>7} {'Avg Value':>12}")
    print("  " + "-" * 60)
    for _, row in cat_summary.iterrows():
        print(f"  {row['Product_Category']:<20} ₹{row['Total_Revenue']:>10,.0f}"
              f" {row['Total_Quantity']:>6} {row['Num_Orders']:>7}"
              f" ₹{row['Avg_Order_Value']:>10,.2f}")

    save_path = os.path.join(TABLES_DIR, "category_summary.csv")
    cat_summary.to_csv(save_path, index=False)
    print(f"\n  💾 Saved → {save_path}")

    return cat_summary


# ═══════════════════════════════════════════════════════════════
# TASK 14 — NumPy Statistical Calculations
# ═══════════════════════════════════════════════════════════════
def numpy_statistics(df):
    """Use NumPy to compute mean, median, and std of Revenue."""
    print("\n" + "=" * 70)
    print("TASK 14: NUMPY STATISTICAL CALCULATIONS")
    print("=" * 70)

    revenue_array = df['Revenue'].values

    mean_rev = np.mean(revenue_array)
    median_rev = np.median(revenue_array)
    std_rev = np.std(revenue_array)

    print(f"\n  Using np.mean()   → Mean Revenue   : ₹{mean_rev:,.2f}")
    print(f"  Using np.median() → Median Revenue : ₹{median_rev:,.2f}")
    print(f"  Using np.std()    → Std Deviation   : ₹{std_rev:,.2f}")

    # Additional context
    if mean_rev > median_rev:
        print("\n  📝 Mean > Median → Revenue distribution is right-skewed (some high-value orders).")
    elif mean_rev < median_rev:
        print("\n  📝 Mean < Median → Revenue distribution is left-skewed.")
    else:
        print("\n  📝 Mean ≈ Median → Revenue distribution is roughly symmetric.")

    return mean_rev, median_rev, std_rev


# ═══════════════════════════════════════════════════════════════
# TASK 17 — Data Cleaning Documentation
# ═══════════════════════════════════════════════════════════════
def document_cleaning(original_rows, cleaned_rows, missing_city_count,
                      dup_count, mismatch_count):
    """Print a summary of every cleaning decision made."""
    print("\n" + "=" * 70)
    print("TASK 17: DATA CLEANING DOCUMENTATION")
    print("=" * 70)

    print(f"""
  ┌─────────────────────────────────────────────────────────────┐
  │                DATA CLEANING SUMMARY                       │
  ├─────────────────────────────────────────────────────────────┤
  │  Original rows loaded          : {original_rows:<25}│
  │  Rows after cleaning           : {cleaned_rows:<25}│
  ├─────────────────────────────────────────────────────────────┤
  │  CLEANING DECISIONS:                                       │
  │                                                            │
  │  1. Missing City Values ({missing_city_count} rows)                          │
  │     → Filled with "Unknown"                                │
  │     → Reason: Cannot infer actual city; inventing          │
  │       locations would be dishonest. "Unknown" preserves    │
  │       data integrity while keeping rows in analysis.       │
  │                                                            │
  │  2. Duplicate Rows ({dup_count} exact duplicates)                       │
  │     → Removed, keeping first occurrence                    │
  │     → Reason: Exact copies add no information and          │
  │       inflate aggregated metrics.                          │
  │                                                            │
  │  3. Revenue Mismatches ({mismatch_count} rows)                           │
  │     → Replaced Revenue with Quantity × Unit_Price          │
  │     → Reason: Calculated_Revenue is more reliable;         │
  │       the original values had unexplained +25 offsets.     │
  │                                                            │
  │  4. Date Conversion                                        │
  │     → Converted Order_Date from string to datetime         │
  │     → Extracted Month (1-12) and Weekday name              │
  └─────────────────────────────────────────────────────────────┘
""")


# ═══════════════════════════════════════════════════════════════
# TASK 18 — Save Cleaned Dataset
# ═══════════════════════════════════════════════════════════════
def save_cleaned_data(df):
    """Save the cleaned DataFrame to CSV."""
    print("\n" + "=" * 70)
    print("TASK 18: SAVING CLEANED DATASET")
    print("=" * 70)

    # Select columns to save (drop helper columns)
    cols_to_save = ['Order_ID', 'Customer_ID', 'Product', 'Product_Category',
                    'City', 'Order_Date', 'Quantity', 'Unit_Price', 'Revenue',
                    'Payment_Method', 'Month', 'Weekday']
    # Only include columns that actually exist
    cols_to_save = [c for c in cols_to_save if c in df.columns]

    df_save = df[cols_to_save].copy()
    df_save.to_csv(CLEANED_CSV, index=False)

    print(f"\n  💾 Cleaned dataset saved → {CLEANED_CSV}")
    print(f"     Rows: {len(df_save)}, Columns: {len(df_save.columns)}")
    print(f"     Columns saved: {cols_to_save}")


# ═══════════════════════════════════════════════════════════════
# VISUALIZATIONS
# ═══════════════════════════════════════════════════════════════

def plot_monthly_revenue(monthly_df):
    """Line chart of monthly revenue trend."""
    fig, ax = plt.subplots(figsize=(10, 5))

    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                   5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                   9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    months = monthly_df['Month'].values
    revenues = monthly_df['Total_Revenue'].values
    labels = [month_names.get(m, str(m)) for m in months]

    ax.plot(labels, revenues, marker='o', linewidth=2.5, color=ACCENT,
            markersize=8, markerfacecolor='white', markeredgewidth=2,
            markeredgecolor=ACCENT)

    # Annotate each point
    for i, (label, rev) in enumerate(zip(labels, revenues)):
        ax.annotate(f'₹{rev:,.0f}', (label, rev),
                    textcoords="offset points", xytext=(0, 12),
                    ha='center', fontsize=8, fontweight='bold')

    ax.set_title('Monthly Revenue Trend', fontsize=TITLE_SIZE, fontweight='bold', pad=15)
    ax.set_xlabel('Month', fontsize=LABEL_SIZE)
    ax.set_ylabel('Revenue (₹)', fontsize=LABEL_SIZE)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "monthly_revenue_trend.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved → {path}")


def plot_top10_products(top10_df):
    """Horizontal bar chart of top 10 products by revenue."""
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = sns.color_palette("viridis", len(top10_df))
    # Reverse for horizontal bar (top product at top)
    data = top10_df.sort_values('Total_Revenue', ascending=True)

    bars = ax.barh(data['Product'], data['Total_Revenue'], color=colors)

    for bar, val in zip(bars, data['Total_Revenue']):
        ax.text(val + max(data['Total_Revenue']) * 0.01, bar.get_y() + bar.get_height() / 2,
                f'₹{val:,.0f}', va='center', fontsize=9, fontweight='bold')

    ax.set_title('Top 10 Products by Total Revenue', fontsize=TITLE_SIZE,
                 fontweight='bold', pad=15)
    ax.set_xlabel('Total Revenue (₹)', fontsize=LABEL_SIZE)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "top10_products_revenue.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved → {path}")


def plot_top10_customers(top10_df):
    """Horizontal bar chart of top 10 customers by spending."""
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = sns.color_palette("magma", len(top10_df))
    data = top10_df.sort_values('Total_Spending', ascending=True)

    bars = ax.barh(data['Customer_ID'], data['Total_Spending'], color=colors)

    for bar, val in zip(bars, data['Total_Spending']):
        ax.text(val + max(data['Total_Spending']) * 0.01, bar.get_y() + bar.get_height() / 2,
                f'₹{val:,.0f}', va='center', fontsize=9, fontweight='bold')

    ax.set_title('Top 10 Customers by Total Spending', fontsize=TITLE_SIZE,
                 fontweight='bold', pad=15)
    ax.set_xlabel('Total Spending (₹)', fontsize=LABEL_SIZE)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "top10_customers_spending.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved → {path}")


def plot_city_revenue(city_df):
    """Bar chart of city-wise revenue."""
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = sns.color_palette("coolwarm", len(city_df))
    bars = ax.bar(city_df['City'], city_df['Total_Revenue'], color=colors)

    # Annotate bars
    for bar, val in zip(bars, city_df['Total_Revenue']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(city_df['Total_Revenue']) * 0.01,
                f'₹{val:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold', rotation=45)

    ax.set_title('City-wise Revenue Comparison', fontsize=TITLE_SIZE, fontweight='bold', pad=15)
    ax.set_xlabel('City', fontsize=LABEL_SIZE)
    ax.set_ylabel('Total Revenue (₹)', fontsize=LABEL_SIZE)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "city_revenue_comparison.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved → {path}")


def plot_payment_methods(payment_df):
    """Two subplots: pie chart for order count, bar chart for revenue."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = sns.color_palette("Set2", len(payment_df))

    # Pie chart — order count
    wedges, texts, autotexts = ax1.pie(
        payment_df['Order_Count'],
        labels=payment_df['Payment_Method'],
        autopct='%1.1f%%',
        colors=colors,
        startangle=140,
        textprops={'fontsize': 10}
    )
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    ax1.set_title('Order Count by Payment Method', fontsize=TITLE_SIZE, fontweight='bold')

    # Bar chart — revenue
    bars = ax2.bar(payment_df['Payment_Method'], payment_df['Total_Revenue'], color=colors)
    for bar, val in zip(bars, payment_df['Total_Revenue']):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(payment_df['Total_Revenue']) * 0.01,
                 f'₹{val:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax2.set_title('Revenue by Payment Method', fontsize=TITLE_SIZE, fontweight='bold')
    ax2.set_ylabel('Total Revenue (₹)', fontsize=LABEL_SIZE)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "payment_method_distribution.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved → {path}")


def plot_category_revenue(cat_df):
    """Bar chart of product category revenue."""
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = sns.color_palette("viridis", len(cat_df))
    bars = ax.bar(cat_df['Product_Category'], cat_df['Total_Revenue'], color=colors)

    for bar, val in zip(bars, cat_df['Total_Revenue']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(cat_df['Total_Revenue']) * 0.01,
                f'₹{val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_title('Revenue by Product Category', fontsize=TITLE_SIZE, fontweight='bold', pad=15)
    ax.set_xlabel('Product Category', fontsize=LABEL_SIZE)
    ax.set_ylabel('Total Revenue (₹)', fontsize=LABEL_SIZE)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
    plt.xticks(rotation=30, ha='right')

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "product_category_revenue.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved → {path}")


def plot_revenue_distribution(df, lower_bound, upper_bound):
    """Histogram + boxplot showing revenue distribution and outliers."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8),
                                    gridspec_kw={'height_ratios': [3, 1]})

    # Histogram
    ax1.hist(df['Revenue'], bins=25, color=ACCENT, edgecolor='white', alpha=0.8)
    ax1.axvline(lower_bound, color='red', linestyle='--', linewidth=1.5,
                label=f'Lower Bound (₹{lower_bound:,.0f})')
    ax1.axvline(upper_bound, color='red', linestyle='--', linewidth=1.5,
                label=f'Upper Bound (₹{upper_bound:,.0f})')

    mean_rev = df['Revenue'].mean()
    median_rev = df['Revenue'].median()
    ax1.axvline(mean_rev, color='orange', linestyle='-', linewidth=1.5,
                label=f'Mean (₹{mean_rev:,.0f})')
    ax1.axvline(median_rev, color='green', linestyle='-', linewidth=1.5,
                label=f'Median (₹{median_rev:,.0f})')

    ax1.set_title('Revenue Distribution with Outlier Boundaries', fontsize=TITLE_SIZE,
                  fontweight='bold', pad=15)
    ax1.set_xlabel('Revenue (₹)', fontsize=LABEL_SIZE)
    ax1.set_ylabel('Frequency', fontsize=LABEL_SIZE)
    ax1.legend(fontsize=9)

    # Boxplot
    try:
        bp = ax2.boxplot(df['Revenue'], orientation='horizontal', patch_artist=True,
                         boxprops=dict(facecolor=ACCENT, alpha=0.5),
                         flierprops=dict(marker='o', markerfacecolor='red', markersize=6))
    except (TypeError, ValueError):
        bp = ax2.boxplot(df['Revenue'], vert=False, patch_artist=True,
                         boxprops=dict(facecolor=ACCENT, alpha=0.5),
                         flierprops=dict(marker='o', markerfacecolor='red', markersize=6))
    ax2.set_xlabel('Revenue (₹)', fontsize=LABEL_SIZE)
    ax2.set_yticks([])

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, "revenue_distribution_outliers.png")
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  📊 Saved → {path}")


# ═══════════════════════════════════════════════════════════════
# TASK 15 — Business Recommendations (data-driven)
# ═══════════════════════════════════════════════════════════════
def generate_recommendations(df, top10_prod, city_df, monthly_df, payment_df, cat_df):
    """Generate 5 evidence-based business recommendations from analysis results."""
    print("\n" + "=" * 70)
    print("TASK 15: EVIDENCE-BASED BUSINESS RECOMMENDATIONS")
    print("=" * 70)

    recommendations = []

    # --- Recommendation 1: Focus on top products ---
    top_product = top10_prod.iloc[0]['Product']
    top_product_rev = top10_prod.iloc[0]['Total_Revenue']
    total_rev = df['Revenue'].sum()
    top_product_pct = (top_product_rev / total_rev) * 100
    recommendations.append(
        f"1. INVEST IN TOP-PERFORMING PRODUCTS\n"
        f"   '{top_product}' generated ₹{top_product_rev:,.0f} ({top_product_pct:.1f}% of total revenue).\n"
        f"   → Increase stock levels and marketing spend for the top 10 products\n"
        f"     which collectively account for a significant share of revenue.\n"
        f"   → Consider bundling top products with slower movers to boost overall sales."
    )

    # --- Recommendation 2: Capitalize on the best month ---
    best_month_idx = monthly_df['Total_Revenue'].idxmax()
    best_month = monthly_df.loc[best_month_idx]
    worst_month_idx = monthly_df['Total_Revenue'].idxmin()
    worst_month = monthly_df.loc[worst_month_idx]
    recommendations.append(
        f"2. OPTIMIZE SEASONAL SALES STRATEGY\n"
        f"   {best_month['Month_Name']} is the strongest month (₹{best_month['Total_Revenue']:,.0f}),\n"
        f"   while {worst_month['Month_Name']} is the weakest (₹{worst_month['Total_Revenue']:,.0f}).\n"
        f"   → Launch promotional campaigns in {worst_month['Month_Name']} to boost low-season sales.\n"
        f"   → Maximize inventory and staffing during {best_month['Month_Name']} to meet peak demand."
    )

    # --- Recommendation 3: Expand in top-revenue cities ---
    real_cities = city_df[city_df['City'] != 'Unknown']
    top_city = real_cities.iloc[0]['City']
    top_city_rev = real_cities.iloc[0]['Total_Revenue']
    bottom_city = real_cities.iloc[-1]['City']
    bottom_city_rev = real_cities.iloc[-1]['Total_Revenue']
    unknown_orders = (city_df['City'] == 'Unknown').sum()
    unknown_rev = city_df[city_df['City'] == 'Unknown']['Total_Revenue'].sum() if unknown_orders > 0 else 0
    recommendations.append(
        f"3. GEO-TARGETED GROWTH STRATEGY\n"
        f"   Among verified cities, {top_city} leads with ₹{top_city_rev:,.0f} revenue, while\n"
        f"   {bottom_city} generates ₹{bottom_city_rev:,.0f}.\n"
        f"   → Reinforce presence in high-performing markets like {top_city} and Lucknow with\n"
        f"     loyalty rewards and priority fulfillment.\n"
        f"   → Conduct targeted regional campaigns to stimulate demand in {bottom_city}.\n"
        f"   → Address data capture gaps: ₹{unknown_rev:,.0f} in sales lacked verified city data;\n"
        f"     enforce mandatory address validation at checkout."
    )

    # --- Recommendation 4: Payment method optimization ---
    top_payment = payment_df.iloc[0]['Payment_Method']
    top_payment_orders = payment_df.iloc[0]['Order_Count']
    total_orders = payment_df['Order_Count'].sum()
    top_payment_pct = (top_payment_orders / total_orders) * 100
    recommendations.append(
        f"4. PAYMENT METHOD OPTIMIZATION\n"
        f"   '{top_payment}' is the most popular method with {top_payment_orders} orders\n"
        f"   ({top_payment_pct:.1f}% of all orders).\n"
        f"   → Ensure a seamless checkout experience for {top_payment} users.\n"
        f"   → Offer incentives (cashback, discounts) on less popular methods to\n"
        f"     diversify payment options and reduce dependency on a single channel."
    )

    # --- Recommendation 5: Category diversification ---
    top_cat = cat_df.iloc[0]['Product_Category']
    top_cat_rev = cat_df.iloc[0]['Total_Revenue']
    bottom_cat = cat_df.iloc[-1]['Product_Category']
    bottom_cat_rev = cat_df.iloc[-1]['Total_Revenue']
    recommendations.append(
        f"5. PRODUCT CATEGORY DIVERSIFICATION\n"
        f"   '{top_cat}' leads with ₹{top_cat_rev:,.0f} revenue, while\n"
        f"   '{bottom_cat}' trails at ₹{bottom_cat_rev:,.0f}.\n"
        f"   → Investigate cross-selling opportunities between top and bottom categories.\n"
        f"   → Evaluate if the low-performing category needs better product selection,\n"
        f"     pricing adjustments, or increased marketing visibility."
    )

    # Print all recommendations
    print()
    for rec in recommendations:
        print(f"  {rec}\n")

    return recommendations


# ═══════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════
def main():
    """Run the complete Retail Sales Performance Analysis pipeline."""

    start_time = datetime.now()

    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█    RETAIL SALES PERFORMANCE ANALYSIS                              █")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    # Setup
    ensure_directories()

    # ── TASK 1: Load & Inspect ──
    df = load_and_inspect(RAW_CSV)
    original_rows = len(df)

    # ── TASK 16: Data Inspection ──
    data_inspection(df)

    # ── TASK 2: Identify Quality Issues ──
    missing, exact_dups = identify_quality_issues(df)
    missing_city_count = df['City'].isnull().sum()
    dup_count = len(exact_dups)

    # ── TASK 3: Clean Missing Cities ──
    df = clean_missing_cities(df)

    # ── TASK 3 (cont.): Remove Duplicates ──
    df = remove_duplicates(df)

    # ── TASK 4: Date Conversion ──
    df = convert_dates(df)

    # ── TASK 5: Revenue Validation ──
    mismatch_count = 0
    df_temp = df.copy()
    df_temp['Calc'] = df_temp['Quantity'] * df_temp['Unit_Price']
    mismatch_count = (~np.isclose(df_temp['Revenue'], df_temp['Calc'], atol=0.01)).sum()
    df = validate_revenue(df)

    # ── TASK 17: Cleaning Documentation ──
    document_cleaning(original_rows, len(df), missing_city_count, dup_count, mismatch_count)

    # ── TASK 18: Save Cleaned Dataset ──
    save_cleaned_data(df)

    # ── TASK 6: Overall Metrics ──
    total_rev, total_qty, avg_ov = overall_metrics(df)

    # ── TASK 7: Top 10 Products ──
    top10_prod = top10_products(df)

    # ── TASK 8: City Revenue ──
    city_df = city_revenue(df)

    # ── TASK 9: Monthly Revenue ──
    monthly_df = monthly_revenue(df)

    # ── TASK 10: Top 10 Customers ──
    top10_cust = top10_customers(df)

    # ── TASK 11: Payment Methods ──
    payment_df = payment_method_analysis(df)

    # ── TASK 12: Outlier Detection ──
    outlier_df, lower_b, upper_b = detect_outliers(df)

    # ── TASK 13: Category Summary ──
    cat_df = category_summary(df)

    # ── TASK 14: NumPy Statistics ──
    mean_r, median_r, std_r = numpy_statistics(df)

    # ── TASK 15: Business Recommendations ──
    recommendations = generate_recommendations(df, top10_prod, city_df,
                                                monthly_df, payment_df, cat_df)

    # ── VISUALIZATIONS ──
    print("\n" + "=" * 70)
    print("GENERATING VISUALIZATIONS")
    print("=" * 70)

    plot_monthly_revenue(monthly_df)
    plot_top10_products(top10_prod)
    plot_top10_customers(top10_cust)
    plot_city_revenue(city_df)
    plot_payment_methods(payment_df)
    plot_category_revenue(cat_df)
    plot_revenue_distribution(df, lower_b, upper_b)

    # ── FINAL SUMMARY ──
    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█    ANALYSIS COMPLETE — TASK SUMMARY                               █")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    tasks = [
        ("Task  1", "Load & Inspect Dataset", "✅"),
        ("Task  2", "Identify Missing Values & Duplicates", "✅"),
        ("Task  3", "Clean Missing Cities & Remove Duplicates", "✅"),
        ("Task  4", "Date Conversion & Feature Extraction", "✅"),
        ("Task  5", "Revenue Validation & Correction", "✅"),
        ("Task  6", "Overall Sales Metrics", "✅"),
        ("Task  7", "Top 10 Products by Revenue", "✅"),
        ("Task  8", "City-wise Revenue Ranking", "✅"),
        ("Task  9", "Monthly Revenue & Best Month", "✅"),
        ("Task 10", "Top 10 Customers by Spending", "✅"),
        ("Task 11", "Payment Method Comparison", "✅"),
        ("Task 12", "Outlier Detection (IQR Method)", "✅"),
        ("Task 13", "Product Category Summary", "✅"),
        ("Task 14", "NumPy Statistical Calculations", "✅"),
        ("Task 15", "Evidence-Based Recommendations", "✅"),
        ("Task 16", "Detailed Data Inspection", "✅"),
        ("Task 17", "Data Cleaning Documentation", "✅"),
        ("Task 18", "Save Cleaned Dataset", "✅"),
    ]

    print()
    for task_id, desc, status in tasks:
        print(f"  {status} {task_id}: {desc}")

    print(f"\n  📂 Charts saved to    : {CHARTS_DIR}")
    print(f"  📂 Tables saved to    : {TABLES_DIR}")
    print(f"  📂 Cleaned data saved : {CLEANED_CSV}")
    print(f"\n  ⏱  Total execution time: {elapsed:.2f} seconds")
    print(f"\n  🎉 All 18 tasks completed successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"\n❌ FILE ERROR: {e}")
        print("   Please ensure the dataset file exists at the specified path.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("\n❌ DATA ERROR: The CSV file is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
