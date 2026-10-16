
import os
import pandas as pd


def export_audit_report(report_data, output_folder="reports"):
    os.makedirs(output_folder, exist_ok=True)

    report_path = os.path.join(
        output_folder,
        "audit_report.xlsx"
    )

    with pd.ExcelWriter(report_path) as writer:
        for sheet_name, dataframe in report_data.items():
            dataframe.to_excel(
                writer,
                sheet_name=sheet_name[:31],
                index=False
            )

    return report_path
