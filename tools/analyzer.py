import pandas as pd


def analyze_data(data, relationships=None):
    """
    Generate dataset-independent AI insights.
    """

    if data is None or data.empty:
        return {}


    insights = {}


    # =========================
    # Dataset Overview
    # =========================

    insights["dataset_overview"] = {

        "rows": int(data.shape[0]),

        "columns": int(data.shape[1]),

        "missing_values": int(
            data.isnull()
            .sum()
            .sum()
        ),

        "duplicate_rows": int(
            data.duplicated()
            .sum()
        )
    }


    # =========================
    # Column Understanding
    # =========================

    numeric_columns = [
        column
        for column in data.select_dtypes(
            include="number"
        ).columns
        if column.lower() != "id"
    ]


    categorical_columns = list(
        data.select_dtypes(
            include=[
                "object",
                "string",
                "category"
            ]
        ).columns
    )


    insights["column_summary"] = {

        "numeric_columns":
            numeric_columns,

        "categorical_columns":
            categorical_columns
    }



    # =========================
    # Numeric Findings
    # =========================

    numeric_findings = []


    for column in numeric_columns:

        numeric_findings.append(
            {
                "column": column,

                "average": round(
                    float(
                        data[column].mean()
                    ),
                    2
                ),

                "min": float(
                    data[column].min()
                ),

                "max": float(
                    data[column].max()
                )
            }
        )


    insights["numeric_findings"] = numeric_findings



    # =========================
    # Categorical Findings
    # =========================

    categorical_findings = []


    for column in categorical_columns:

        counts = (
            data[column]
            .value_counts()
        )


        if not counts.empty:

            categorical_findings.append(
                {
                    "column": column,

                    "unique_values":
                        int(
                            data[column]
                            .nunique()
                        ),

                    "most_common":
                        str(
                            counts.index[0]
                        ),

                    "frequency":
                        int(
                            counts.iloc[0]
                        )
                }
            )


    insights["categorical_findings"] = categorical_findings



    # =========================
    # Relationship Findings
    # =========================

    relationship_findings = []


    if relationships:

        for relationship in relationships[:10]:

            relationship_findings.append(
                {
                    "between":
                    [
                        relationship["feature_1"],
                        relationship["feature_2"]
                    ],

                    "type":
                    relationship["type"],

                    "strength":
                    relationship["strength"],

                    "recommended_chart":
                    relationship["chart"]
                }
            )


    insights["relationship_findings"] = (
        relationship_findings
    )



    # =========================
    # Automatic Recommendations
    # =========================

    recommendations = []


    if insights["dataset_overview"]["missing_values"] > 0:

        recommendations.append(
            "Dataset contains missing values that may require cleaning."
        )


    if insights["dataset_overview"]["duplicate_rows"] > 0:

        recommendations.append(
            "Duplicate records were detected."
        )


    if relationship_findings:

        recommendations.append(
            "Important relationships were discovered and visualizations were generated."
        )


    if not recommendations:

        recommendations.append(
            "Dataset quality looks good and no major issues were detected."
        )


    insights["recommendations"] = recommendations



    return insights