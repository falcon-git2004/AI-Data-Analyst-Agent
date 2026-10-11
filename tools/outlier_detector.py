import pandas as pd


def detect_outliers(data, profile):
    """
    Detect numerical outliers using IQR method.
    """

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


        if len(series) < 5:
            continue



        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)


        iqr = q3 - q1


        lower_bound = (
            q1 - 1.5 * iqr
        )


        upper_bound = (
            q3 + 1.5 * iqr
        )


        outliers = series[
            (series < lower_bound)
            |
            (series > upper_bound)
        ]


        count = len(outliers)


        if count > 0:


            percentage = (
                count /
                len(series)
            ) * 100


            results.append(
                {
                    "column": column,

                    "method": "IQR",

                    "outlier_count":
                        count,

                    "percentage":
                        round(
                            percentage,
                            2
                        ),

                    "lower_bound":
                        round(
                            float(lower_bound),
                            2
                        ),

                    "upper_bound":
                        round(
                            float(upper_bound),
                            2
                        ),

                    "severity":
                        (
                            "high"
                            if percentage > 5
                            else
                            "low"
                        )
                }
            )


    return results