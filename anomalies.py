
import pandas as pd


def find_duplicate_records(dataframe):
    duplicates = dataframe[
        dataframe.duplicated(keep=False)
    ]

    return duplicates


def find_unusual_numeric_values(dataframe):
    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns

    unusual_values = []

    for column in numeric_columns:
        values = dataframe[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr

        for index, value in values.items():
            if value < lower_limit or value > upper_limit:
                unusual_values.append({
                    "row_index": index,
                    "column": column,
                    "value": value,
                    "reason": "Outside IQR range"
                })

    return pd.DataFrame(unusual_values)
