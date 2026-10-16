
import os
import uuid

import pandas as pd
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from backend.extractor import (
    extract_text_from_pdf,
    extract_tables_from_pdf,
)
from backend.analyzer import convert_table_to_dataframe
from backend.comparison import compare_dataframes
from backend.anomalies import (
    find_duplicate_records,
    find_unusual_numeric_values,
)
from backend.reporting import export_audit_report
from backend.csv_analyzer import analyze_transaction_csv


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# -------------------- FILE UPLOAD HELPERS --------------------

def save_uploaded_pdf(file):
    if file is None or not file.filename:
        raise ValueError("Please select a PDF file.")

    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed.")

    filename = secure_filename(file.filename)

    if not filename:
        raise ValueError("Invalid PDF filename.")

    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    return file_path


def save_uploaded_csv(file):
    if file is None or not file.filename:
        raise ValueError("Please select a CSV file.")

    if not file.filename.lower().endswith(".csv"):
        raise ValueError("Only CSV files are allowed.")

    filename = secure_filename(file.filename)

    if not filename:
        raise ValueError("Invalid CSV filename.")

    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    return file_path


# -------------------- PDF HELPERS --------------------

def get_first_table_dataframe(pdf_path):
    tables = extract_tables_from_pdf(pdf_path)

    if not tables:
        raise ValueError(
            "No tables were detected in this PDF. "
            "Please try a PDF containing a clear, text-based table."
        )

    dataframe = convert_table_to_dataframe(tables[0]["data"])

    if dataframe.empty or len(dataframe.columns) == 0:
        raise ValueError("The first detected table is empty.")

    dataframe.columns = [
        str(column).strip() for column in dataframe.columns
    ]

    if dataframe.columns.duplicated().any():
        raise ValueError(
            "Duplicate column headers were detected. "
            "Please use a table with unique column names."
        )

    return dataframe


def table_html(dataframe):
    if dataframe is None or dataframe.empty:
        return ""

    return dataframe.to_html(
        index=False,
        classes="data-table",
        border=0,
        na_rep="",
    )


def make_report(report_data):
    report_path = export_audit_report(
        report_data,
        output_folder=REPORT_FOLDER,
    )

    if not os.path.isfile(report_path):
        raise RuntimeError("The Excel report could not be created.")

    return report_path


# -------------------- MAIN PAGE --------------------

@app.route("/", methods=["GET", "POST"])
def home():
    extracted_pages = []
    error = None
    message = None
    results = {}
    report_ready = False

    if request.method == "POST":
        action = request.form.get("action", "extract")

        try:
            # -------------------- CSV TRANSACTION ANALYSIS --------------------
            if action == "csv_analyze":
                csv_path = save_uploaded_csv(
                    request.files.get("csv_file")
                )

                start_date = (
                    request.form.get("start_date", "").strip() or None
                )

                end_date = (
                    request.form.get("end_date", "").strip() or None
                )

                transaction_type = (
    request.form.get("transaction_type", "").strip() or None
)

                csv_summary = analyze_transaction_csv(
                    csv_path,
                    start_date=start_date,
                    end_date=end_date,
                    transaction_type=transaction_type,
                )

                results = {
                    "csv_analysis": csv_summary,
                }

                message = (
                    "CSV analysis complete: "
                    f"{csv_summary['total_rows']:,} matching "
                    "transactions processed."
                )

            # -------------------- PDF TEXT EXTRACTION --------------------
            elif action == "extract":
                pdf_path = save_uploaded_pdf(
                    request.files.get("pdf_file")
                )

                extracted_pages = extract_text_from_pdf(pdf_path)

                if not extracted_pages:
                    message = (
                        "The PDF was processed, but no readable text "
                        "was extracted. It may be scanned."
                    )

            # -------------------- PDF TABLE ANALYSIS --------------------
            elif action == "analyze":
                pdf_path = save_uploaded_pdf(
                    request.files.get("pdf_file")
                )

                dataframe = get_first_table_dataframe(pdf_path)

                duplicates = find_duplicate_records(dataframe)
                unusual = find_unusual_numeric_values(dataframe)

                results = {
                    "table": table_html(dataframe),
                    "duplicates": table_html(duplicates),
                    "unusual": table_html(unusual),
                    "duplicate_count": len(duplicates),
                    "unusual_count": len(unusual),
                }

                make_report({
                    "Extracted Table": dataframe,
                    "Duplicate Records": duplicates,
                    "Unusual Values": unusual,
                })

                report_ready = True

                message = (
                    f"Analysis complete: {len(duplicates)} duplicate "
                    f"rows and {len(unusual)} unusual values flagged."
                )

            # -------------------- PDF COMPARISON --------------------
            elif action == "compare":
                old_path = save_uploaded_pdf(
                    request.files.get("old_pdf")
                )

                new_path = save_uploaded_pdf(
                    request.files.get("new_pdf")
                )

                key_column = (
                    request.form.get("key_column", "").strip()
                )

                if not key_column:
                    raise ValueError(
                        "Enter the unique key column, such as StudentID."
                    )

                old_df = get_first_table_dataframe(old_path)
                new_df = get_first_table_dataframe(new_path)

                if key_column not in old_df.columns:
                    raise ValueError(
                        f"'{key_column}' was not found in the old PDF. "
                        f"Available columns: {', '.join(old_df.columns)}"
                    )

                if key_column not in new_df.columns:
                    raise ValueError(
                        f"'{key_column}' was not found in the new PDF. "
                        f"Available columns: {', '.join(new_df.columns)}"
                    )

                comparison = compare_dataframes(
                    old_df,
                    new_df,
                    key_column,
                )

                added = comparison["added"]
                missing = comparison["missing"]
                changed = comparison["changed"]

                results = {
                    "added": table_html(added),
                    "missing": table_html(missing),
                    "changed": table_html(changed),
                    "added_count": len(added),
                    "missing_count": len(missing),
                    "changed_count": len(changed),
                }

                make_report({
                    "Added Records": added,
                    "Missing Records": missing,
                    "Changed Values": changed,
                })

                report_ready = True

                message = (
                    f"Comparison complete: {len(added)} added records, "
                    f"{len(missing)} missing records and "
                    f"{len(changed)} changed values."
                )

            else:
                raise ValueError("Unknown operation selected.")

        except ValueError as exc:
            error = str(exc)

        except Exception:
            app.logger.exception("PDFInsight operation failed")
            error = (
                "The operation could not be completed. Check the "
                "terminal for details and verify the uploaded file."
            )

    return render_template(
        "index.html",
        extracted_pages=extracted_pages,
        error=error,
        message=message,
        results=results,
        report_ready=report_ready,
    )


# -------------------- REPORT DOWNLOAD --------------------

@app.route("/download-report")
def download_report():
    report_path = os.path.abspath(
        os.path.join(REPORT_FOLDER, "audit_report.xlsx")
    )

    if not os.path.isfile(report_path):
        return (
            "No audit report is available. Run an analysis or "
            "comparison first.",
            404,
        )

    return send_from_directory(
        os.path.abspath(REPORT_FOLDER),
        os.path.basename(report_path),
        as_attachment=True,
    )


# -------------------- UPLOAD SIZE ERROR --------------------

@app.errorhandler(413)
def file_too_large(error):
    return (
        "File too large. The current upload limit is 20 MB.",
        413,
    )


if __name__ == "__main__":
    app.run(debug=True)
