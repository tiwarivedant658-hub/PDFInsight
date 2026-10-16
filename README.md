# PDFInsight

A Python-based web application for PDF extraction, document comparison, anomaly exploration, and CSV transaction analytics.

## Features

- **PDF Text Extraction:** Extract text from PDF documents using `pdfplumber`.
- **PDF Analysis:** Analyze extracted information and numerical data.
- **Document Comparison:** Compare documents to explore differences.
- **Anomaly Exploration:** Identify duplicate values and potentially unusual numerical patterns.
- **CSV Analytics:** Process transaction datasets using Pandas.
- **Interactive Dashboard:** Visualize daily transactions, transaction types, and top merchants using Chart.js.
- **Excel Reports:** Export analysis results to Excel where supported.

## Tech Stack

- Python
- Flask
- Pandas
- pdfplumber
- OpenPyXL
- HTML
- CSS
- JavaScript
- Chart.js
- Gunicorn

## Project Structure

```text
PDFInsight/
├── app.py
├── requirements.txt
├── README.md
├── backend/
│   ├── extractor.py
│   ├── analyzer.py
│   ├── comparison.py
│   ├── anomalies.py
│   ├── reporting.py
│   └── csv_analyzer.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PDFInsight
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open the local URL shown in your terminal, usually:

`http://127.0.0.1:5000`

## Deployment

The application can be deployed to a compatible Python hosting platform such as Render.

Example production start command:

```bash
gunicorn app:app
```

This assumes the Flask application instance is named `app` inside `app.py`.

## Security Notes

- Do not upload confidential documents or sensitive financial data to an untrusted server.
- Never commit credentials, private datasets, or environment files to GitHub.
- Unusual values are not necessarily fraudulent; this project provides data analysis rather than validated fraud detection.

## Future Improvements

- Enhanced PDF table extraction.
- More document comparison options.
- Additional data visualizations.
- Improved error handling for large files.
- Persistent storage and user authentication.

## License

A license can be added when the project’s distribution and reuse terms are decided.

---

**PDFInsight — Built with Python and Flask.**
