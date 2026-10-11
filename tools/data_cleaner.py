import pandas as pd


def clean_data(data):
    """
    Clean dataset by handling missing values and duplicates
    """

    if data is None:
        return None

    print("🧹 Starting data cleaning...")

    # Remove duplicates
    before = len(data)
    data = data.drop_duplicates()
    after = len(data)

    print(f"Removed duplicates: {before - after}")

    # Handle missing values
    for column in data.columns:

        if data[column].isnull().sum() > 0:

            if pd.api.types.is_numeric_dtype(data[column]):
                data[column] = data[column].fillna(
                    data[column].mean()
                )

            else:
                data[column] = data[column].fillna(
                    "Unknown"
                )

    print("✅ Data cleaning completed!")

    return data