
import pandas as pd
from backend.comparison import compare_dataframes

old_data = pd.DataFrame({
    "Name": ["Rahul", "Priya", "Aman"],
    "Marks": [85, 91, 78]
})

new_data = pd.DataFrame({
    "Name": ["Rahul", "Priya", "Neha"],
    "Marks": [90, 91, 88]
})

result = compare_dataframes(old_data, new_data, "Name")

print("\nADDED RECORDS")
print(result["added"])

print("\nMISSING RECORDS")
print(result["missing"])

print("\nCHANGED VALUES")
print(result["changed"])
