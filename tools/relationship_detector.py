import pandas as pd


def detect_relationships(data, target, profile):

    relationships = []


    if target is None:
        return relationships


    # Columns that should not be analyzed
    excluded_columns = (
        profile.get("id_columns", [])
    )


    features = [
        col
        for col in data.columns
        if col != target
        and col not in excluded_columns
    ]


    for feature in features:


        # =========================
        # Numeric Feature vs Target
        # =========================

        if pd.api.types.is_numeric_dtype(
            data[feature]
        ):

            grouped = (
                data.groupby(target)[feature]
                .mean()
            )


            # Binary target comparison

            if len(grouped) == 2:

                difference = abs(
                    float(grouped.iloc[0])
                    -
                    float(grouped.iloc[1])
                )


                mean_value = abs(
                    float(data[feature].mean())
                )


                if mean_value != 0:

                    strength = (
                        difference /
                        mean_value
                    )


                    if strength > 0.2:

                        relationships.append(
                            {
                                "feature": feature,
                                "type": "numeric_target",
                                "strength": round(
                                    float(strength),
                                    2
                                ),
                                "chart": "boxplot"
                            }
                        )



        # =========================
        # Categorical Feature vs Target
        # =========================

        else:


            # Calculate target rate per category

            rates = (
                data.groupby(feature)[target]
                .mean()
            )


            if len(rates) > 1:


                difference = (
                    float(rates.max())
                    -
                    float(rates.min())
                )


                if difference > 0.15:


                    relationships.append(
                        {
                            "feature": feature,
                            "type": "categorical_target",
                            "strength": round(
                                difference,
                                2
                            ),
                            "chart": "bar"
                        }
                    )



    # Sort by importance

    relationships = sorted(
        relationships,
        key=lambda x: x["strength"],
        reverse=True
    )


    return relationships[:10]