
import pandas as pd

from backend.reporting import export_audit_report


report_data = {
    "Added Records": pd.DataFrame({
        "Name": ["Neha"],
        "Marks": [88]
    }),

    "Missing Records": pd.DataFrame({
        "Name": ["Aman"],
        "Marks": [78]
    }),

    "Changed Values": pd.DataFrame({
        "Name": ["Rahul"],
        "Column": ["Marks"],
        "Old Value": [85],
        "New Value": [90]
    })
}

file_path = export_audit_report(report_data)

print("Audit report created successfully!")
print("File location:", file_path)
