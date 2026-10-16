
import pdfplumber


def extract_text_from_pdf(file_path):
    extracted_pages = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if text:
                extracted_pages.append({
                    "page_number": page_number,
                    "text": text
                })

    return extracted_pages

def extract_tables_from_pdf(file_path):
    all_tables = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            for table_number, table in enumerate(tables, start=1):
                if table:
                    all_tables.append({
                        "page_number": page_number,
                        "table_number": table_number,
                        "data": table
                    })

    return all_tables

def extract_tables_from_pdf(file_path):
    all_tables = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            for table_number, table in enumerate(tables, start=1):
                if table:
                    all_tables.append({
                        "page_number": page_number,
                        "table_number": table_number,
                        "data": table
                    })

    return all_tables
