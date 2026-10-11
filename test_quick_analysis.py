import pandas as pd

from tools.quick_analyzer import (
    quick_analyze
)


data = pd.read_csv(
    "data/uploaded_data.csv"
)


result = quick_analyze(
    data
)


print("\n⚡ QUICK ANALYSIS\n")


print("Overview:")
print(
    result["overview"]
)


print("\nData Quality:")
print(
    result["data_quality"]
)


print("\nQuick Findings:")

for finding in result[
    "quick_findings"
]:

    print(
        "-",
        finding["message"]
    )