from extractor import extract_text_from_pdf

pdf_path = input("Enter the PDF file path: ")

try:
    pages = extract_text_from_pdf(pdf_path)

    if not pages:
        print("No extractable text found in this PDF.")
    else:
        for page in pages:
            print(f"\n--- Page {page['page_number']} ---")
            print(page["text"])

except Exception as error:
    print("Could not read the PDF:", error)
