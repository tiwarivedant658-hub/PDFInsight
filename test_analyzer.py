
from backend.extractor import extract_tables_from_pdf
from backend.analyzer import convert_table_to_dataframe

pdf_path = input("Enter PDF path: ").strip().strip('"')

try:
    tables = extract_tables_from_pdf(pdf_path)

    if not tables:
        print("No tables detected in this PDF.")
    else:
        for table in tables:
            dataframe = convert_table_to_dataframe(table["data"])

            print(f"\nPage {table['page_number']}")
            print(dataframe)
            print("\nData types:")
            print(dataframe.dtypes)

except Exception as error:
    print("Analysis failed:", error)