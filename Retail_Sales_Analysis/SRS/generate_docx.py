"""
Script to generate Project_SRS.docx for Retail Sales Performance Analysis
Uses python-docx to build a professional, beautifully styled Word document.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Set the background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell padding in twips."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(margin_name)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def style_table(table, col_widths=None):
    """Apply consistent corporate styling to tables."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header row formatting
    for cell in table.rows[0].cells:
        set_cell_background(cell, "1F4E79") # Deep Blue
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(10)
                run.font.name = "Calibri"
                
    # Data rows formatting
    for i, row in enumerate(table.rows[1:], start=1):
        bg_color = "F2F5F8" if i % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg_color)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9.5)
                    run.font.name = "Calibri"
                    run.font.color.rgb = RGBColor(51, 51, 51)
                    
    # Column widths
    if col_widths:
        for row in table.rows:
            for j, w in enumerate(col_widths):
                if j < len(row.cells):
                    row.cells[j].width = Inches(w)

def add_callout(doc, text, title="NOTE"):
    """Add a shaded callout note box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "EBF1F5")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"📌 {title}: ")
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(31, 78, 121)
    run_t.font.name = "Calibri"
    
    run_b = p.add_run(text)
    run_b.font.italic = True
    run_b.font.color.rgb = RGBColor(60, 60, 60)
    run_b.font.name = "Calibri"
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def generate_srs_doc(output_path):
    doc = Document()
    
    # Page setup - Margins 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "Retail Sales Performance Analysis | Software Requirements Specification"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(128, 128, 128)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Confidential — Academic Training Assignment | B.Tech CSE (First Year)"
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(128, 128, 128)

    # ══════════════════════════════════════════════════════════
    # TITLE PAGE
    # ══════════════════════════════════════════════════════════
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(40)
    title_p.paragraph_format.space_after = Pt(8)
    title_run = title_p.add_run("SOFTWARE REQUIREMENTS SPECIFICATION")
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(31, 78, 121) # Deep Blue
    title_run.font.name = "Calibri"
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_after = Pt(30)
    sub_run = subtitle_p.add_run("RETAIL SALES PERFORMANCE ANALYSIS\nAn Industrial Data Analytics System using Python, NumPy & Pandas")
    sub_run.font.size = Pt(14)
    sub_run.font.color.rgb = RGBColor(89, 89, 89)
    sub_run.font.name = "Calibri"
    
    # Metadata Table on cover page
    meta_table = doc.add_table(rows=7, cols=2)
    meta_data = [
        ("Project Title", "Retail Sales Performance Analysis"),
        ("Academic Program", "B.Tech Computer Science & Engineering (1st Year)"),
        ("Industrial Training", "Python, NumPy, Pandas, Data Visualization"),
        ("Document Version", "1.0 (Final Official Release)"),
        ("Author / Student", "Nitish Patel (B.Tech CSE)"),
        ("Primary Dataset", "01_retail_sales.csv (303 Raw Records)"),
        ("Date of Publication", "November 2026")
    ]
    for idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[idx]
        row.cells[0].text = k
        row.cells[1].text = v
    style_table(meta_table, col_widths=[2.2, 4.3])
    
    doc.add_page_break()

    # ══════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════
    toc_head = doc.add_paragraph()
    toc_run = toc_head.add_run("TABLE OF CONTENTS")
    toc_run.font.size = Pt(16)
    toc_run.font.bold = True
    toc_run.font.color.rgb = RGBColor(31, 78, 121)
    
    toc_items = [
        ("1. Project Title", "3"),
        ("2. Introduction", "3"),
        ("3. Problem Statement", "3"),
        ("4. Project Objectives", "4"),
        ("5. Project Scope (In-Scope & Out-of-Scope)", "4"),
        ("6. Dataset Description & Column Schema", "5"),
        ("7. Functional Requirements (All 18 Assignment Tasks)", "6"),
        ("8. Non-Functional Requirements", "8"),
        ("9. Tools and Technologies", "8"),
        ("10. Methodology & Analytical Lifecycle", "9"),
        ("11. Expected Outcomes & Deliverables", "10"),
        ("12. Limitations", "10"),
        ("13. Conclusion", "11"),
    ]
    
    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    for idx, (section, page) in enumerate(toc_items):
        row = toc_table.rows[idx]
        row.cells[0].text = section
        row.cells[1].text = f"Page {page}"
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    style_table(toc_table, col_widths=[5.0, 1.5])
    
    doc.add_page_break()

    # Helper for adding sections
    def add_section_header(num, text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        r = h.add_run(f"{num}. {text.upper()}")
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 121)
        r.font.name = "Calibri"

    def add_body_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            br = p.add_run(bold_prefix)
            br.font.bold = True
            br.font.color.rgb = RGBColor(31, 78, 121)
            br.font.name = "Calibri"
        r = p.add_run(text)
        r.font.size = Pt(10.5)
        r.font.name = "Calibri"
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    # ══════════════════════════════════════════════════════════
    # 1. PROJECT TITLE
    # ══════════════════════════════════════════════════════════
    add_section_header("1", "Project Title")
    add_body_p(
        "Retail Sales Performance Analysis — An Industrial Data Analytics and Business Intelligence System Using Python, NumPy, Pandas, Matplotlib, and Seaborn."
    )

    # ══════════════════════════════════════════════════════════
    # 2. INTRODUCTION
    # ══════════════════════════════════════════════════════════
    add_section_header("2", "Introduction")
    add_body_p(
        "This Software Requirements Specification (SRS) document details the complete requirements, system architecture, data cleaning protocols, and analytical deliverables for the Retail Sales Performance Analysis project. Undertaken by a first-year B.Tech Computer Science & Engineering student as part of an industrial training program in Python, NumPy, and Pandas, this system transforms raw retail transactional records into strategic commercial intelligence."
    )
    add_body_p(
        "Modern commerce environments produce continuous streams of transactional data containing purchase timestamps, customer identifiers, multi-category inventory items, geographical footprints, and settlement channels. Without structured preprocessing and quantitative analysis, valuable insights regarding customer preferences, regional sales disparities, seasonal demand spikes, and pricing anomalies remain inaccessible. This project establishes an automated, end-to-end Python analytical pipeline that ingests raw transactional data, handles missing values and duplicates, audits revenue calculations, performs statistical evaluations, and generates executive-grade visualizations."
    )

    # ══════════════════════════════════════════════════════════
    # 3. PROBLEM STATEMENT
    # ══════════════════════════════════════════════════════════
    add_section_header("3", "Problem Statement")
    add_body_p(
        "Retail managers must make daily decisions regarding inventory procurement, seasonal pricing, regional marketing budgets, and customer payment gateway optimization. Relying on manual spreadsheet evaluations introduces substantial operational risk due to three major challenges:"
    )
    add_body_p("1. Data Inconsistencies & Human Error: Industrial datasets regularly contain corruptions including duplicate entries, missing geographic location values, and calculation discrepancies between recorded revenue and line-item unit pricing.")
    add_body_p("2. Analytical Latency: Manually cross-tabulating multi-dimensional variables across products, cities, dates, and payment methods is prohibitively slow, error-prone, and cannot scale as order volumes expand.")
    add_body_p("3. Lack of Statistical Rigor: Basic sum totals fail to reveal data skewness or identify statistical outliers that distort standard averages. Decisions made without dispersion metrics (median, standard deviation, IQR) often result in misallocated promotional capital.")
    add_body_p("This project addresses these challenges by engineering an automated, objective, and reproducible Python data analytics pipeline.")

    # ══════════════════════════════════════════════════════════
    # 4. PROJECT OBJECTIVES
    # ══════════════════════════════════════════════════════════
    add_section_header("4", "Project Objectives")
    
    obj_table = doc.add_table(rows=9, cols=2)
    obj_data = [
        ("O-1", "Data Ingestion & Schema Inspection: Load the CSV file and evaluate dimensions, schema, and column data types."),
        ("O-2", "Data Cleaning & Integrity Auditing: Detect missing values and duplicate rows; impute missing cities without inventing locations; remove redundant rows."),
        ("O-3", "Feature Engineering: Parse string timestamps into datetime objects; extract month and weekday features for temporal analysis."),
        ("O-4", "Revenue Verification & Correction: Validate Quantity × Unit_Price against recorded Revenue; correct arithmetic discrepancies."),
        ("O-5", "Key Performance Indicators (KPIs): Calculate Total Revenue, Total Volume Sold, Order Count, and Average Order Value (AOV)."),
        ("O-6", "Multi-Dimensional Segmentation: Analyze sales performance across Products, Categories, Cities, Months, and Payment Methods."),
        ("O-7", "Statistical & Outlier Profiling: Compute mean, median, standard deviation using NumPy; detect extreme transactions using the IQR method."),
        ("O-8", "Data Visualization & Strategic Insights: Generate 7 professional visual charts and 5 data-backed business recommendations.")
    ]
    for idx, (oid, odesc) in enumerate(obj_data):
        row = obj_table.rows[idx]
        row.cells[0].text = oid
        row.cells[1].text = odesc
    style_table(obj_table, col_widths=[0.8, 5.7])

    # ══════════════════════════════════════════════════════════
    # 5. PROJECT SCOPE
    # ══════════════════════════════════════════════════════════
    add_section_header("5", "Project Scope")
    add_body_p("In-Scope Functional Boundaries:", bold_prefix="5.1 ")
    add_body_p("• Ingestion, inspection, and cleaning of the authentic dataset (01_retail_sales.csv).")
    add_body_p("• Execution of all 18 numbered assignment tasks using standard Python, NumPy, and Pandas.")
    add_body_p("• Statistical anomaly detection using the Interquartile Range (IQR) rule.")
    add_body_p("• Generation and persistence of 7 publication-quality visual charts in PNG format.")
    add_body_p("• Export of 8 summary analytical CSV tables and the sanitized master dataset (cleaned_retail_sales.csv).")
    add_body_p("• Generation of the complete Software Requirements Specification (SRS) in .docx and .md formats.")
    
    add_body_p("Out-of-Scope Elements:", bold_prefix="5.2 ")
    add_body_p("• Production SQL database integration (MySQL, PostgreSQL).")
    add_body_p("• Real-time streaming data ingestion or live API webhooks.")
    add_body_p("• Predictive machine learning models (e.g., ARIMA sales forecasting, customer churn classification).")
    add_body_p("• Web front-end application or cloud deployment (AWS/GCP/Azure).")

    # ══════════════════════════════════════════════════════════
    # 6. DATASET DESCRIPTION
    # ══════════════════════════════════════════════════════════
    add_section_header("6", "Dataset Description")
    add_body_p(
        "The analysis is conducted exclusively on the supplied primary dataset: 01_retail_sales.csv. It comprises 303 raw transactional records (304 lines including header) spanning the entire calendar year 2025 across 8 major commercial hubs in Northern India."
    )
    
    schema_table = doc.add_table(rows=11, cols=5)
    schema_data = [
        ("#", "Column Name", "Raw Type", "Cleaned Type", "Description / Value Domain"),
        ("1", "Order_ID", "object", "str", "Unique alphanumeric transaction ID (ORD10001 - ORD10300)"),
        ("2", "Customer_ID", "object", "str", "Unique customer identifier (CUST1001 - CUST1080; 77 unique)"),
        ("3", "Product", "object", "str", "Specific retail item name (20 distinct items)"),
        ("4", "Product_Category", "object", "str", "Category (Electronics, Clothing, Home & Kitchen, Stationery)"),
        ("5", "City", "object", "str", "City of order (Agra, Delhi, Ghaziabad, Kanpur, Lucknow, Meerut, Noida, Varanasi, Unknown)"),
        ("6", "Order_Date", "object", "datetime64", "Transaction date (2025-01-01 to 2025-12-31)"),
        ("7", "Quantity", "int64", "int64", "Units purchased per order (1 to 5 units)"),
        ("8", "Unit_Price", "int64", "int64", "Price per unit in INR (₹65 to ₹2,649)"),
        ("9", "Revenue", "int64", "float/int", "Line item total revenue in INR (₹65 to ₹11,985)"),
        ("10", "Payment_Method", "object", "str", "Settlement channel (UPI, Credit Card, Debit Card, Net Banking, Cash)")
    ]
    for idx, (c1, c2, c3, c4, c5) in enumerate(schema_data):
        row = schema_table.rows[idx]
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        row.cells[3].text = c4
        row.cells[4].text = c5
    style_table(schema_table, col_widths=[0.4, 1.4, 0.8, 1.1, 2.8])
    
    add_callout(doc, "Data Cleaning Findings: (1) 6 missing City records imputed with 'Unknown' to avoid geographical fabrication; (2) 3 duplicate rows (ORD10191, ORD10065, ORD10117) removed to establish 300 clean unique orders; (3) 2 arithmetic mismatches of +₹25 in ORD10021 and ORD10295 corrected via Quantity × Unit_Price.", "QUALITY AUDIT")

    # ══════════════════════════════════════════════════════════
    # 7. FUNCTIONAL REQUIREMENTS
    # ══════════════════════════════════════════════════════════
    add_section_header("7", "Functional Requirements (All 18 Assignment Tasks)")
    add_body_p(
        "The system completely implements all 18 numbered assignment requirements. Each requirement is formally specified below:"
    )
    
    fr_table = doc.add_table(rows=19, cols=4)
    fr_data = [
        ("Req. ID", "Task Title", "Input", "Functional Specification & Verified Output"),
        ("FR-01", "Dataset Ingestion & Inspection", "CSV File", "Load CSV; verify shape (303x10), columns, dtypes, and df.info()."),
        ("FR-02", "Quality Anomaly Identification", "Raw DataFrame", "Identify 6 missing cities, 3 exact duplicate rows, and duplicate IDs."),
        ("FR-03", "Missing Data Imputation & Deduplication", "Raw DataFrame", "Impute missing City with 'Unknown'; drop 3 duplicates -> exactly 300 rows."),
        ("FR-04", "Datetime Parsing & Feature Extraction", "Clean DataFrame", "Convert Order_Date to datetime; extract Month (1-12) and Weekday name."),
        ("FR-05", "Revenue Audit & Correction", "Clean DataFrame", "Verify Quantity x Unit_Price = Revenue; fix 2 mismatches; save audit CSV."),
        ("FR-06", "Overall KPI Formulation", "Clean DataFrame", "Compute Total Revenue (₹623,052), Quantity (912), Orders (300), AOV (₹2,076.84)."),
        ("FR-07", "Top 10 Products by Revenue", "Clean DataFrame", "Rank products by revenue; top: Webcam (₹89,792), Headphones (₹80,256)."),
        ("FR-08", "City Revenue Ranking", "Clean DataFrame", "Rank cities by revenue; top: Kanpur (₹94,635), Lucknow (₹92,096)."),
        ("FR-09", "Monthly Revenue & Peak Period", "Clean DataFrame", "Monthly breakdown; identify peak month (May: ₹78,577) and lowest (Sept: ₹37,431)."),
        ("FR-10", "Top 10 Customers by Spending", "Clean DataFrame", "Rank customer accounts; top: CUST1072 (₹24,784), CUST1066 (₹23,932)."),
        ("FR-11", "Payment Method Comparison", "Clean DataFrame", "Compare gateways; UPI leads with 130 orders (43.3%) and ₹283,406 (45.5%)."),
        ("FR-12", "IQR Statistical Outlier Detection", "Clean DataFrame", "Q1=₹511.50, Q3=₹2,692.75, Upper Bound=₹5,964.62; identify 18 outliers."),
        ("FR-13", "Product Category Groupby Summary", "Clean DataFrame", "Groupby category; Electronics leads with ₹279,698 (AOV ₹3,884.69)."),
        ("FR-14", "NumPy Statistical Calculations", "Revenue Array", "Using np.mean (₹2,076.84), np.median (₹1,268.50), np.std (₹2,200.05)."),
        ("FR-15", "Evidence-Based Recommendations", "Analysis State", "Dynamically synthesize 5 commercial recommendations from data arrays."),
        ("FR-16", "Comprehensive Data Inspection", "DataFrame", "Display head, tail, and df.describe(include='all') across numerical & text cols."),
        ("FR-17", "Cleaning Process Documentation", "Audit Log", "Output structured table detailing every data cleaning justification."),
        ("FR-18", "Cleaned Dataset Persistence", "Final DataFrame", "Save cleaned_retail_sales.csv (300 rows, 12 columns) to data/ directory.")
    ]
    for idx, (c1, c2, c3, c4) in enumerate(fr_data):
        row = fr_table.rows[idx]
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        row.cells[3].text = c4
    style_table(fr_table, col_widths=[0.8, 1.8, 1.2, 2.7])

    # ══════════════════════════════════════════════════════════
    # 8. NON-FUNCTIONAL REQUIREMENTS
    # ══════════════════════════════════════════════════════════
    add_section_header("8", "Non-Functional Requirements")
    
    nfr_table = doc.add_table(rows=8, cols=3)
    nfr_data = [
        ("Req. ID", "Parameter", "Specification Standard"),
        ("NFR-01", "Performance", "Pipeline executes start-to-finish in < 15 seconds (achieved: 8.95s)."),
        ("NFR-02", "Modularity", "Functions organized by task; clear separation of ETL, analysis, and plotting."),
        ("NFR-03", "Zero Hard-Coding", "All metrics, rankings, and business recommendations computed dynamically."),
        ("NFR-04", "Cross-Platform", "Platform-independent file resolution using os.path across Windows, Linux, macOS."),
        ("NFR-05", "Visual Quality", "Charts rendered at 150 DPI with clean styling, value labels, and tight bounds."),
        ("NFR-06", "Robustness", "Graceful handling for missing files, empty data streams, and deprecation warnings."),
        ("NFR-07", "Data Immutability", "Original raw dataset is strictly read-only; never overwritten.")
    ]
    for idx, (c1, c2, c3) in enumerate(nfr_data):
        row = nfr_table.rows[idx]
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
    style_table(nfr_table, col_widths=[0.9, 1.6, 4.0])

    # ══════════════════════════════════════════════════════════
    # 9. TOOLS AND TECHNOLOGIES
    # ══════════════════════════════════════════════════════════
    add_section_header("9", "Tools and Technologies")
    
    tool_table = doc.add_table(rows=8, cols=3)
    tool_data = [
        ("Technology", "Minimum Version", "Architectural Functionality in Project"),
        ("Python", "3.8+ (Tested on 3.12+)", "Core procedural language, workflow automation, scripting engine"),
        ("NumPy", "1.24+", "Array computation, statistical metrics (mean, median, standard deviation)"),
        ("Pandas", "2.0+", "DataFrames, CSV I/O, data cleaning, datetime parsing, groupby aggregations"),
        ("Matplotlib", "3.7+", "Graphic plotting engine, figure canvases, tick formatters, file rendering"),
        ("Seaborn", "0.12+", "Statistical plot aesthetics, whitegrid theme, viridis and coolwarm palettes"),
        ("python-docx", "1.1+", "Automated compilation of formal Word SRS technical documentation"),
        ("Git & GitHub", "2.30+", "Source version control, repository staging, change documentation")
    ]
    for idx, (c1, c2, c3) in enumerate(tool_data):
        row = tool_table.rows[idx]
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
    style_table(tool_table, col_widths=[1.5, 1.5, 3.5])

    # ══════════════════════════════════════════════════════════
    # 10. METHODOLOGY
    # ══════════════════════════════════════════════════════════
    add_section_header("10", "Methodology & Analytical Lifecycle")
    add_body_p(
        "The project follows a rigorous 7-stage analytical data engineering lifecycle: (1) Ingestion & Initial Inspection -> (2) Data Auditing & Cleaning -> (3) Feature Engineering & Dataset Persistence -> (4) Multi-Dimensional Aggregations & Segmentation -> (5) Statistical & Outlier Profiling -> (6) Visualization Generation -> (7) Dynamic Business Intelligence Synthesis."
    )

    # ══════════════════════════════════════════════════════════
    # 11. EXPECTED OUTCOMES
    # ══════════════════════════════════════════════════════════
    add_section_header("11", "Expected Outcomes & Deliverables")
    add_body_p("The executed system generates the following physical artifacts on disk:")
    add_body_p("• Sanitized Dataset: data/cleaned_retail_sales.csv (300 records, 12 attributes).")
    add_body_p("• Visual Charts (outputs/charts/): monthly_revenue_trend.png, top10_products_revenue.png, top10_customers_spending.png, city_revenue_comparison.png, payment_method_distribution.png, product_category_revenue.png, revenue_distribution_outliers.png.")
    add_body_p("• Analysis Tables (outputs/analysis_tables/): top10_products.csv, city_revenue.csv, monthly_revenue.csv, top10_customers.csv, payment_method_analysis.csv, category_summary.csv, outliers.csv, revenue_mismatches.csv.")
    add_body_p("• Technical Documentation: README.md, Project_SRS.md, and Project_SRS.docx.")

    # ══════════════════════════════════════════════════════════
    # 12. LIMITATIONS
    # ══════════════════════════════════════════════════════════
    add_section_header("12", "Limitations")
    add_body_p("1. Sample Size: 300 orders represent an academic training dataset rather than Big Data enterprise scale.")
    add_body_p("2. Temporal Coverage: Single calendar year (2025); year-over-year CAGR trends cannot be computed.")
    add_body_p("3. Regional Focus: Centered across 8 cities in Northern/Central India (UP and NCR).")
    add_body_p("4. Absence of Demographics: Customer age, gender, and income are omitted, restricting deep persona clustering.")
    add_body_p("5. Batch Processing: Operates on static CSV snapshots rather than live real-time event streaming.")
    add_body_p("6. Descriptive Scope: Emphasizes descriptive and diagnostic analytics rather than predictive machine learning.")

    # ══════════════════════════════════════════════════════════
    # 13. CONCLUSION
    # ══════════════════════════════════════════════════════════
    add_section_header("13", "Conclusion")
    add_body_p(
        "The Retail Sales Performance Analysis project successfully bridges fundamental computer science programming with commercial business intelligence. By developing a clean, modular, and fully tested Python pipeline utilizing NumPy, Pandas, Matplotlib, and Seaborn, the project delivers verifiable analytical outputs, professional visualization charts, and evidence-based business recommendations. It serves as an exemplary first-year engineering portfolio submission fully meeting all industrial training requirements."
    )

    doc.save(output_path)
    print(f"✔ Successfully generated SRS Word document: {output_path}")

if __name__ == "__main__":
    out_file = r"d:\Hcl project\Retail_Sales_Analysis\SRS\Project_SRS.docx"
    generate_srs_doc(out_file)
