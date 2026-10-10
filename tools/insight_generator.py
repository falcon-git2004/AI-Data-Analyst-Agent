def generate_insights(
    profile,
    outliers,
    distribution,
    relationships
):

    insights = []


    # ==========================
    # Data Quality Insights
    # ==========================

    missing_values = sum(
        profile["missing_values"].values()
    )


    if missing_values == 0:

        insights.append(
            {
                "type": "quality",

                "title":
                    "Dataset Quality",

                "finding":
                    "No missing values were detected.",

                "recommendation":
                    "The dataset is ready for analysis."
            }
        )


    else:

        insights.append(
            {
                "type": "quality",

                "title":
                    "Missing Values",

                "finding":
                    f"{missing_values} missing values detected.",

                "recommendation":
                    "Consider data cleaning before further analysis."
            }
        )



    # ==========================
    # Outlier Insights
    # ==========================

    for item in outliers:


        insights.append(
            {
                "type": "outlier",

                "title":
                    f"Outliers in {item['column']}",

                "finding":
                    f"{item['outlier_count']} unusual values detected.",

                "recommendation":
                    "Investigate extreme values before making conclusions."
            }
        )



    # ==========================
    # Distribution Insights
    # ==========================

    numeric_distribution = (
        distribution.get(
            "numeric_distribution",
            []
        )
    )


    for item in numeric_distribution:


        if item["distribution"] == "right_skewed":


            insights.append(
                {
                    "type": "distribution",

                    "title":
                        f"{item['column']} Distribution",

                    "finding":
                        "Values are right-skewed. "
                        "Some observations are higher than most values.",

                    "recommendation":
                        "Investigate high-value observations."
                }
            )


        elif item["distribution"] == "left_skewed":


            insights.append(
                {
                    "type": "distribution",

                    "title":
                        f"{item['column']} Distribution",

                    "finding":
                        "Values are left-skewed.",

                    "recommendation":
                        "Check lower extreme values."
                }
            )



    # ==========================
    # Relationship Insights
    # ==========================

    for relationship in relationships:


        if relationship.get(
            "interpretation"
        ) == "large effect":


            insights.append(
                {
                    "type": "relationship",

                    "title":
                        "Strong Relationship Found",

                    "finding":
                        (
                            f"{relationship['feature_1']} "
                            f"shows a large effect on "
                            f"{relationship['feature_2']}."
                        ),

                    "recommendation":
                        "Explore this relationship further."
                }
            )



    return insights