
import pandas as pd


def convert_table_to_dataframe(table_data):
    if not table_data:
        return pd.DataFrame()

    headers = table_data[0]
    rows = table_data[1:]

    dataframe = pd.DataFrame(rows, columns=headers)

    return dataframe
