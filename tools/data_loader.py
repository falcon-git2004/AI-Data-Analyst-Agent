import pandas as pd


def load_data(file_path):
    """
    Load CSV data and return a pandas DataFrame
    """

    try:
        data = pd.read_csv(file_path)

        print("✅ Data loaded successfully!")
        print(f"Rows: {data.shape[0]}")
        print(f"Columns: {data.shape[1]}")

        return data

    except Exception as error:
        print(f"❌ Error loading data: {error}")
        return None


def get_data_summary(data):
    """
    Generate basic information about the dataset
    """

    if data is None:
        return None

    summary = {
        "shape": data.shape,
        "columns": list(data.columns),
        "missing_values": data.isnull().sum().to_dict(),
        "data_types": data.dtypes.astype(str).to_dict()
    }

    return summary