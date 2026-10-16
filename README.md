# PDFInsight | Document & Transaction Analyzer

**A Python-based document analysis and transaction auditing tool that extracts information from PDFs, analyzes structured data, identifies potential anomalies, and generates insightful reports through an interactive web dashboard.**

PDFInsight is designed to simplify document analysis and financial transaction auditing by combining PDF extraction, tabular data processing, CSV analytics, anomaly detection, and data visualization in one application.

---

## 🚀 Key Features

### 📄 PDF Document Analysis
- Extract text from PDF documents.
- Extract tables from supported PDF files.
- Convert extracted tables into structured Pandas DataFrames.
- Organize document data for further analysis.

### 📊 CSV Transaction Analyzer
- Upload and analyze transaction CSV files.
- Calculate total transaction amount and transaction count.
- Identify minimum and maximum transaction values.
- Summarize transaction types and merchant activity.
- Analyze daily transaction amounts.
- Detect missing values and duplicate records.
- Process large CSV files using chunk-based reading.

### 🔍 Data Comparison & Anomaly Detection
- Compare structured datasets and identify differences.
- Detect duplicate records.
- Flag unusual numerical values for further investigation.
- Highlight potential data quality issues.

*Note: Unusual values are potential anomalies, not necessarily fraudulent transactions.*

### 📈 Interactive Dashboard
- Visualize daily transaction amounts using a line chart.
- Explore transaction-type distribution using a doughnut chart.
- View top merchants using a bar chart.
- Review merchant summaries and transaction statistics.
- Filter transaction analysis by date range and transaction type.

### 📑 Report Generation
- Generate downloadable analysis and audit reports.
- Export findings for documentation and further review.
- Organize reports for easier auditing and record-keeping.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Backend web framework and routing |
| Pandas | Data processing and DataFrame operations |
| pdfplumber | PDF text and table extraction |
| Chart.js | Interactive dashboard charts |
| HTML5 | Web page structure |
| CSS3 | Dashboard styling |
| Jinja2 | Dynamic HTML rendering through Flask |
| Git & GitHub | Version control and project hosting |

---

## 🏗️ Project Architecture

```text
PDFInsight/
│
├── app.py
│
├── backend/
│   ├── extractor.py
│   ├── analyzer.py
│   ├── comparison.py
│   ├── anomalies.py
│   ├── reporting.py
│   └── csv_analyzer.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── uploads/
├── reports/
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Module Overview

| File | Responsibility |
|---|---|
| `app.py` | Flask application, upload handling, routes, filters, and integration of analysis modules |
| `extractor.py` | Extracts text and tables from PDF documents |
| `analyzer.py` | Converts extracted tables into structured DataFrames |
| `comparison.py` | Compares datasets and identifies differences |
| `anomalies.py` | Detects duplicate records and unusual numerical values |
| `reporting.py` | Exports analysis findings into reports |
| `csv_analyzer.py` | Analyzes CSV transactions, aggregates statistics, and prepares chart data |
| `index.html` | Provides the main user interface and dashboard |
| `style.css` | Defines layout, styling, and responsive presentation |
| `uploads/` | Stores uploaded files during processing |
| `reports/` | Stores generated reports |

---

## ⚙️ How It Works

PDFInsight follows a modular data-processing pipeline.

1. **Upload:** The user uploads a PDF document or transaction CSV file through the web interface.
2. **Validation:** The Flask backend receives the file and checks the upload requirements.
3. **Extraction:** For PDFs, the extraction module retrieves text and tables.
4. **Transformation:** Extracted tables and CSV records are converted into structured data for analysis.
5. **Analysis:** The application calculates transaction statistics, compares datasets, checks data quality, and identifies potential anomalies.
6. **Visualization:** Aggregated results are displayed through interactive Chart.js visualizations.
7. **Reporting:** The reporting module exports findings for download and further review.

### CSV Processing Approach

The CSV analyzer uses Pandas chunk-based reading with a chunk size of 100,000 rows. This allows the application to process large CSV files incrementally instead of loading the entire dataset into memory at once.

The analyzer also attempts to identify relevant columns, such as amount, date, transaction type, and merchant, using column names. Actual results depend on the structure and quality of the uploaded data.

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.10 or later recommended.
- pip package manager.
- Git (optional, for cloning the repository).

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/PDFInsight.git
cd PDFInsight
```

Replace `YOUR-USERNAME` with your GitHub username and `PDFInsight` with your actual repository name if different.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Ensure that `requirements.txt` contains all the external packages used by your project.

### 4. Run the Application

```bash
python app.py
```

Open the local URL printed by Flask in your terminal, typically:

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing the Application

After launching the application:

1. Upload a supported PDF file and test text extraction.
2. Upload a PDF containing tables and inspect the extracted data.
3. Upload a transaction CSV file with appropriate date, amount, merchant, and transaction-type columns.
4. Review the calculated statistics and dashboard charts.
5. Apply the available date and transaction-type filters.
6. Check the duplicate-record and unusual-value results.
7. Generate and download an available report.

For reliable results, use files with valid formats and clearly identifiable column names.

---

## 📂 Dataset

PDFInsight is designed to analyze user-provided PDF documents and transaction CSV files.

A transaction dataset, including a Kaggle-sourced dataset during development, was used for testing the CSV analysis workflow.

The application is not limited to one fixed dataset; compatibility depends on the input schema and supported file formats.

If you redistribute a dataset with this project, include its original source and comply with its licensing and usage terms. Do not commit confidential transaction data or personally identifiable information.

---

## 🔐 Security & Data Handling

- The application uses a configured maximum upload size of **20 MB**.
- Uploaded files and generated reports are handled through dedicated directories.
- A production deployment should validate file extensions and content, generate safe filenames, restrict access to uploaded data, and clean up temporary files.
- Sensitive financial information should not be uploaded to a publicly accessible deployment.

**Important:** A file-size limit
