import pandas as pd



def detect_target(data):
    """
    Automatically detect the most likely target column
    with confidence estimation.
    """

    candidates = []


    keywords = [
        "target",
        "label",
        "result",
        "status",
        "outcome",
        "class",
        "success",
        "failure",
        "fail",
        "churn",
        "default",
        "converted",
        "approved",
        "reached",
        "response",
        "decision"
    ]


    for column in data.columns:


        # Ignore ID columns

        if (
            column.lower() == "id"
            or column.lower().endswith("_id")
        ):
            continue


        unique_values = data[column].nunique()

        score = 0

        reasons = []


        column_name = column.lower()



        # Column name indicators

        for keyword in keywords:

            if keyword in column_name:

                score += 5

                reasons.append(
                    f"Column name contains '{keyword}'"
                )



        # Binary columns

        if unique_values == 2:

            score += 2

            reasons.append(
                "Binary column"
            )



        # Low cardinality categorical columns

        if (
            unique_values > 2
            and unique_values <= 10
            and not pd.api.types.is_numeric_dtype(
                data[column]
            )
        ):

            score += 1

            reasons.append(
                "Low-cardinality categorical column"
            )



        # Last column hint

        if column == data.columns[-1]:

            score += 1

            reasons.append(
                "Located at end of dataset"
            )



        candidates.append(
            {
                "column": column,
                "score": score,
                "reasons": reasons
            }
        )



    if not candidates:

        return {
            "column": None,
            "confidence": "Low",
            "reason": "No suitable target candidates found"
        }



    candidates = sorted(
        candidates,
        key=lambda x: x["score"],
        reverse=True
    )


    best = candidates[0]



    if best["score"] >= 6:

        confidence = "High"

    elif best["score"] >= 3:

        confidence = "Medium"

    else:

        confidence = "Low"



    # Do not force a target

    if best["score"] < 3:

        return {
            "column": None,
            "confidence": "Low",
            "reason": "No clear target detected"
        }



    return {
        "column": best["column"],
        "confidence": confidence,
        "reason": "; ".join(
            best["reasons"]
        )
    }





def profile_dataset(data):

    profile = {}


    profile["rows"] = int(
        data.shape[0]
    )

    profile["columns"] = int(
        data.shape[1]
    )


    profile["column_types"] = {}

    profile["binary_columns"] = []

    profile["id_columns"] = []



    for column in data.columns:


        dtype = data[column].dtype

        unique_values = data[column].nunique()



        # ID Detection

        if (
            column.lower() == "id"
            or column.lower().endswith("_id")
        ):

            column_type = "id"

            profile["id_columns"].append(
                column
            )



        # Binary Detection

        elif unique_values == 2:

            column_type = "binary"

            profile["binary_columns"].append(
                column
            )



        # Numeric Detection

        elif pd.api.types.is_numeric_dtype(
            dtype
        ):

            column_type = "numeric"



        # Categorical Detection

        else:

            column_type = "categorical"



        profile["column_types"][column] = (
            column_type
        )



    profile["missing_values"] = (
        data.isnull()
        .sum()
        .to_dict()
    )



    profile["duplicates"] = int(
        data.duplicated()
        .sum()
    )



    profile["numeric_columns"] = [
        col
        for col, typ in profile["column_types"].items()
        if typ == "numeric"
    ]



    profile["categorical_columns"] = [
        col
        for col, typ in profile["column_types"].items()
        if typ == "categorical"
    ]



    # Target Detection

    target_info = detect_target(
        data
    )


    profile["detected_target"] = (
        target_info["column"]
    )


    profile["target_confidence"] = (
        target_info["confidence"]
    )


    profile["target_reason"] = (
        target_info["reason"]
    )


    return profile