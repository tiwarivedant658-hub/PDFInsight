
import pandas as pd
from backend.anomalies import (
    find_duplicate_records,
    find_unusual_numeric_values
)

data = pd.DataFrame({
    "StudentID": [101, 102, 102, 103, 104, 105],
    "Marks": [70, 75, 75, 80, 78, 500]
})

print("\nDUPLICATE RECORDS")
print(find_duplicate_records(data))

print("\nUNUSUAL NUMERIC VALUES")
print(find_unusual_numeric_values(data))
