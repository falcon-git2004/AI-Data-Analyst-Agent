import pandas as pd



def is_id_column(column_name):
    """
    Detect obvious identifier columns.
    """

    name = column_name.lower().strip()

    return (
        name == "id"
        or name.endswith("_id")
        or name == "index"
        or "uuid" in name
    )



def quick_analyze(data):
    """
    Generate fast dataset-independent insights.
    """

    if data is None or data.empty:

        return {
            "overview": {},
            "data_quality": {},
            "quick_findings": []
        }



    # ==========================================
    # Dataset Overview
    # ==========================================

    rows = int(data.shape[0])

    columns = int(data.shape[1])


    missing_values = int(
        data.isnull()
        .sum()
        .sum()
    )


    duplicate_rows = int(
        data.duplicated()
        .sum()
    )


    overview = {

        "rows": rows,

        "columns": columns

    }



    data_quality = {

        "missing_values":
            missing_values,

        "duplicate_rows":
            duplicate_rows

    }



    # ==========================================
    # Detect Columns
    # ==========================================

    ignored_columns = [

        column

        for column in data.columns

        if is_id_column(column)

    ]


    useful_columns = [

        column

        for column in data.columns

        if column not in ignored_columns

    ]



    numeric_columns = [

        column

        for column in useful_columns

        if pd.api.types.is_numeric_dtype(
            data[column]
        )

    ]



    categorical_columns = [

        column

        for column in useful_columns

        if (
            pd.api.types.is_object_dtype(
                data[column]
            )

            or pd.api.types.is_string_dtype(
                data[column]
            )

            or isinstance(
                data[column].dtype,
                pd.CategoricalDtype
            )
        )

    ]



    findings = []



    # ==========================================
    # Quick Numeric Relationship
    # ==========================================

    strongest_relationship = None


    if len(numeric_columns) >= 2:


        correlation_matrix = (
            data[numeric_columns]
            .corr()
        )


        for i in range(
            len(numeric_columns)
        ):

            for j in range(
                i + 1,
                len(numeric_columns)
            ):


                column_1 = numeric_columns[i]

                column_2 = numeric_columns[j]


                correlation = (
                    correlation_matrix
                    .loc[
                        column_1,
                        column_2
                    ]
                )


                if pd.isna(correlation):
                    continue


                strength = abs(
                    float(correlation)
                )


                if (
                    strongest_relationship is None
                    or strength >
                    strongest_relationship["strength"]
                ):


                    strongest_relationship = {

                        "feature_1":
                            column_1,

                        "feature_2":
                            column_2,

                        "correlation":
                            round(
                                float(correlation),
                                2
                            ),

                        "strength":
                            round(
                                strength,
                                2
                            )

                    }



    if (
        strongest_relationship
        and strongest_relationship["strength"] >= 0.5
    ):


        direction = (

            "positive"

            if strongest_relationship["correlation"] > 0

            else "negative"

        )


        findings.append(

            {

                "priority":
                    "high",

                "type":
                    "relationship",

                **strongest_relationship,


                "message":
                    (
                        f"A strong {direction} relationship "
                        f"was detected between "
                        f"{strongest_relationship['feature_1']} "
                        f"and "
                        f"{strongest_relationship['feature_2']}."
                    )

            }

        )



    # ==========================================
    # Data Quality Findings
    # ==========================================

    if missing_values == 0:


        findings.append(

            {

                "priority":
                    "medium",

                "type":
                    "data_quality",

                "message":
                    "No missing values were detected."

            }

        )


    else:


        findings.append(

            {

                "priority":
                    "high",

                "type":
                    "data_quality",

                "message":
                    f"{missing_values} missing values were detected."

            }

        )



    if duplicate_rows > 0:


        findings.append(

            {

                "priority":
                    "medium",

                "type":
                    "data_quality",

                "message":
                    f"{duplicate_rows} duplicate rows were detected."

            }

        )



    # ==========================================
    # Numeric Summary
    # ==========================================

    for column in numeric_columns[:3]:


        series = data[column].dropna()


        if series.empty:
            continue



        findings.append(

            {

                "priority":
                    "low",

                "type":
                    "numeric_summary",

                "column":
                    column,

                "average":
                    round(
                        float(series.mean()),
                        2
                    ),

                "minimum":
                    round(
                        float(series.min()),
                        2
                    ),

                "maximum":
                    round(
                        float(series.max()),
                        2
                    ),

                "message":
                    (
                        f"{column} average is "
                        f"{round(float(series.mean()),2)}."
                    )

            }

        )



    # ==========================================
    # Categorical Summary
    # ==========================================

    for column in categorical_columns[:3]:


        counts = (

            data[column]

            .dropna()

            .astype(str)

            .value_counts()

        )


        if counts.empty:
            continue



        value = str(
            counts.index[0]
        )


        percentage = round(

            (
                counts.iloc[0]
                /
                counts.sum()
            )
            * 100,

            1

        )


        findings.append(

            {

                "priority":
                    "low",

                "type":
                    "categorical_summary",

                "column":
                    column,

                "most_common":
                    value,

                "percentage":
                    percentage,

                "message":
                    (
                        f"{column} most common value "
                        f"is {value} ({percentage}%)."
                    )

            }

        )



    return {

        "overview":
            overview,

        "data_quality":
            data_quality,

        "ignored_columns":
            ignored_columns,

        "numeric_columns":
            numeric_columns,

        "categorical_columns":
            categorical_columns,

        "quick_findings":
            findings

    }