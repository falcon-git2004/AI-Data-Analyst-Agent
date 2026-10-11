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
                    f"{missing_values} missing values were found in the "
                    "original data and filled automatically "
                    "(mean for numeric columns, 'Unknown' for text).",

                "recommendation":
                    "Review how these values were filled before "
                    "drawing conclusions."
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

        if relationship.get("interpretation") != "large effect":
            continue

        feature = relationship["feature_1"]
        target = relationship["feature_2"]
        means = relationship.get("group_means")

        if means and len(means) == 2:

            low_label, high_label = sorted(
                means, key=means.get
            )

            finding = (
                f"{feature} differs strongly between {target} groups: "
                f"average {means[high_label]} when {target} = {high_label} "
                f"vs {means[low_label]} when {target} = {low_label}."
            )

        else:

            finding = (
                f"{feature} shows a large effect on {target}."
            )

        insights.append(
            {
                "type": "relationship",
                "title": "Strong Relationship Found",
                "finding": finding,
                "recommendation": (
                    "This is an association, not proof of cause. "
                    "Explore it further before acting on it."
                )
            }
        )

    return insights