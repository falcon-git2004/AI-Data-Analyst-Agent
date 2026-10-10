import pandas as pd


def analyze_numeric_distribution(data, profile):

    results = []

    excluded_columns = profile.get(
        "id_columns",
        []
    )


    numeric_columns = [
        column
        for column in data.select_dtypes(
            include="number"
        ).columns
        if column not in excluded_columns
    ]


    for column in numeric_columns:


        series = data[column].dropna()


        if len(series) < 3:
            continue


        skewness = series.skew()


        if skewness > 0.5:

            distribution = "right_skewed"

        elif skewness < -0.5:

            distribution = "left_skewed"

        else:

            distribution = "approximately_normal"



        results.append(
            {
                "column": column,

                "type": "numeric",

                "average":
                    round(
                        float(series.mean()),
                        2
                    ),

                "minimum":
                    float(series.min()),

                "maximum":
                    float(series.max()),

                "skewness":
                    round(
                        float(skewness),
                        2
                    ),

                "distribution":
                    distribution
            }
        )


    return results



def analyze_categorical_distribution(data, profile):

    results = []


    categorical_columns = [
        column
        for column in data.select_dtypes(
            include=[
                "object",
                "category",
                "string"
            ]
        ).columns
    ]



    for column in categorical_columns:


        counts = (
            data[column]
            .value_counts(
                normalize=True
            )
            .head(5)
        )


        if counts.empty:
            continue



        dominant_value = counts.index[0]


        dominant_percentage = (
            counts.iloc[0] * 100
        )


        if dominant_percentage > 70:

            balance = "highly_imbalanced"

        elif dominant_percentage > 50:

            balance = "moderately_imbalanced"

        else:

            balance = "balanced"



        results.append(
            {
                "column": column,

                "type": "categorical",

                "unique_values":
                    int(
                        data[column].nunique()
                    ),

                "most_common":
                    dominant_value,

                "percentage":
                    round(
                        float(
                            dominant_percentage
                        ),
                        2
                    ),

                "distribution":
                    balance
            }
        )


    return results



def analyze_distribution(data, profile):

    return {

        "numeric_distribution":
            analyze_numeric_distribution(
                data,
                profile
            ),

        "categorical_distribution":
            analyze_categorical_distribution(
                data,
                profile
            )
    }