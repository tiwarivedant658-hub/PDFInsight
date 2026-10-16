
from backend.extractor import extract_tables_from_pdf

pdf_path = input("Enter PDF path: ").strip().strip('"')

try:
    tables = extract_tables_from_pdf(pdf_path)

    if not tables:
        print("No tables detected in this PDF.")
    else:
        for table in tables:
            print(
                f"\nPage {table['page_number']}, "
                f"Table {table['table_number']}"
            )

            for row in table["data"]:
                print(row)

except Exception as error:
    print("Could not extract tables:", error)
