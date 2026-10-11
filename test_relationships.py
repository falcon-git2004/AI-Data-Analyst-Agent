import pandas as pd

from tools.profiler import profile_dataset
from tools.relationship_engine import discover_relationships


data = pd.read_csv("data/uploaded_data.csv")

profile = profile_dataset(data)

print("PROFILE IDS:")
print(profile["id_columns"])


target = profile["detected_target"]


relationships = discover_relationships(
    data,
    target,
    profile
)


print("\nTop Relationships:")

for r in relationships:
    print(r)