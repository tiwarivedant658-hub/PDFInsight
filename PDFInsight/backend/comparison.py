
import pandas as pd


def compare_dataframes(old_df, new_df, key_column):
    if key_column not in old_df.columns:
        raise ValueError(f"Key column '{key_column}' missing from old data.")

    if key_column not in new_df.columns:
        raise ValueError(f"Key column '{key_column}' missing from new data.")

    if old_df[key_column].duplicated().any():
        raise ValueError("Old data contains duplicate key values.")

    if new_df[key_column].duplicated().any():
        raise ValueError("New data contains duplicate key values.")

    old_df = old_df.set_index(key_column)
    new_df = new_df.set_index(key_column)

    old_keys = set(old_df.index)
    new_keys = set(new_df.index)

    added_keys = new_keys - old_keys
    missing_keys = old_keys - new_keys
    common_keys = old_keys & new_keys

    added = new_df.loc[sorted(added_keys)].reset_index()
    missing = old_df.loc[sorted(missing_keys)].reset_index()

    changed_records = []

    common_columns = old_df.columns.intersection(new_df.columns)

    for key in sorted(common_keys):
        for column in common_columns:
            old_value = old_df.at[key, column]
            new_value = new_df.at[key, column]

            if pd.isna(old_value) and pd.isna(new_value):
                continue

            if old_value != new_value:
                changed_records.append({
                    key_column: key,
                    "column": column,
                    "old_value": old_value,
                    "new_value": new_value
                })

    return {
        "added": added,
        "missing": missing,
        "changed": pd.DataFrame(changed_records)
    }
