import pandas as pd


def analyze_data(data):

    if data is None:
        return None


    insights = {}

    insights["total_sales"] = data["Sales"].sum()

    insights["average_sales"] = data["Sales"].mean()

    best_product = data.loc[
        data["Sales"].idxmax()
    ]

    insights["best_product"] = best_product["Product"]

    category_sales = (
        data.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    insights["top_category"] = category_sales.index[0]


    return insights