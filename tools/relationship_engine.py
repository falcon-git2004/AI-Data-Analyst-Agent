import pandas as pd

from scipy.stats import (
    chi2_contingency,
    spearmanr
)



# ==========================================
# Relationship Strength Interpretation
# ==========================================


import pandas as pd

from scipy.stats import (
    chi2_contingency,
    spearmanr
)


def interpret_effect_size(value):

    if value < 0.2:
        return "negligible effect"

    elif value < 0.5:
        return "small effect"

    elif value < 0.8:
        return "medium effect"

    else:
        return "large effect"



def interpret_strength(value):

    if value < 0.1:
        return "very weak"

    elif value < 0.3:
        return "weak"

    elif value < 0.5:
        return "moderate"

    elif value < 0.7:
        return "strong"

    else:
        return "very strong"



# ==========================================
# Cohen's d Effect Size
# ==========================================

def calculate_cohens_d(group1, group2):

    n1 = len(group1)
    n2 = len(group2)


    if n1 < 2 or n2 < 2:
        return 0


    pooled_std = (
        (
            (n1 - 1) * group1.std() ** 2
            +
            (n2 - 1) * group2.std() ** 2
        )
        /
        (n1 + n2 - 2)
    ) ** 0.5


    if pooled_std == 0:
        return 0


    return abs(
        group1.mean()
        -
        group2.mean()
    ) / pooled_std



# ==========================================
# Numeric ↔ Numeric
# ==========================================

def analyze_numeric_relationships(
    data,
    profile
):

    relationships = []


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



    for i in range(
        len(numeric_columns)
    ):

        for j in range(
            i + 1,
            len(numeric_columns)
        ):

            col1 = numeric_columns[i]

            col2 = numeric_columns[j]


            pearson = data[col1].corr(
                data[col2],
                method="pearson"
            )


            spearman, _ = spearmanr(
                data[col1],
                data[col2]
            )


            if pd.isna(pearson):
                continue



            strength = max(
                abs(pearson),
                abs(spearman)
            )


            if strength >= 0.5:

                method = (
                    "pearson"
                    if abs(pearson)
                    >= abs(spearman)
                    else "spearman"
                )


                relationships.append(
                    {
                        "feature_1": col1,

                        "feature_2": col2,

                        "type":
                            "numeric_numeric",

                        "method":
                            method,

                        "strength":
                            round(
                                float(strength),
                                2
                            ),

                        "interpretation":
                            interpret_strength(
                                strength
                            ),

                        "correlation":
                            round(
                                float(
                                    pearson
                                ),
                                2
                            ),

                        "chart":
                            "scatter"
                    }
                )


    return relationships




# ==========================================
# Categorical ↔ Categorical
# ==========================================

def analyze_categorical_relationships(
    data,
    profile
):

    relationships = []


    excluded_columns = profile.get(
        "id_columns",
        []
    )


    categorical_columns = [
        column
        for column in data.select_dtypes(
            include=[
                "object",
                "category",
                "string"
            ]
        ).columns
        if column not in excluded_columns
    ]



    for i in range(
        len(categorical_columns)
    ):

        for j in range(
            i + 1,
            len(categorical_columns)
        ):


            col1 = categorical_columns[i]

            col2 = categorical_columns[j]


            table = pd.crosstab(
                data[col1],
                data[col2]
            )


            if table.empty:
                continue



            chi2, p_value, _, _ = (
                chi2_contingency(table)
            )


            n = table.values.sum()


            minimum = min(
                table.shape[0] - 1,
                table.shape[1] - 1
            )


            if minimum == 0:
                continue



            cramers_v = (
                (chi2 / n)
                /
                minimum
            ) ** 0.5



            if (
                p_value < 0.05
                and cramers_v >= 0.2
            ):

                relationships.append(
                    {
                        "feature_1": col1,

                        "feature_2": col2,

                        "type":
                            "categorical_categorical",

                        "method":
                            "chi_square",

                        "strength":
                            round(
                                float(
                                    cramers_v
                                ),
                                2
                            ),

                        "p_value":
                            round(
                                float(
                                    p_value
                                ),
                                4
                            ),

                        "interpretation":
                            interpret_strength(
                                cramers_v
                            ),

                        "chart":
                            "heatmap"
                    }
                )


    return relationships




# ==========================================
# Feature ↔ Target
# ==========================================

def analyze_target_relationships(
    data,
    target,
    profile
):

    relationships = []


    if target is None:
        return relationships



    excluded_columns = profile.get(
        "id_columns",
        []
    )



    features = [
        column
        for column in data.columns
        if column != target
        and column not in excluded_columns
    ]



    for column in features:


        # Numeric Feature vs Binary Target

        if pd.api.types.is_numeric_dtype(
            data[column]
        ):


            groups = [
                group[column].dropna()
                for _, group
                in data.groupby(target)
            ]


            if len(groups) == 2:


                effect = calculate_cohens_d(
                    groups[0],
                    groups[1]
                )



                if effect >= 0.3:

                    relationships.append(
                        {
                            "feature_1":
                                column,

                            "feature_2":
                                target,

                            "type":
                                "numeric_target",

                            "method":
                                "cohens_d",

                            "strength":
                                round(
                                    float(effect),
                                    2
                                ),

                            "interpretation":
                                interpret_effect_size(
                                    effect
                                ),

                            "chart":
                                "boxplot"
                        }
                    )



        # Categorical Feature vs Target

        else:


            table = pd.crosstab(
                data[column],
                data[target]
            )


            if table.empty:
                continue



            chi2, p_value, _, _ = (
                chi2_contingency(table)
            )


            n = table.values.sum()


            minimum = min(
                table.shape[0] - 1,
                table.shape[1] - 1
            )


            if minimum == 0:
                continue



            cramers_v = (
                (chi2 / n)
                /
                minimum
            ) ** 0.5



            if (
                p_value < 0.05
                and cramers_v >= 0.2
            ):


                relationships.append(
                    {
                        "feature_1":
                            column,

                        "feature_2":
                            target,

                        "type":
                            "categorical_target",

                        "method":
                            "chi_square",

                        "strength":
                            round(
                                float(
                                    cramers_v
                                ),
                                2
                            ),

                        "p_value":
                            round(
                                float(
                                    p_value
                                ),
                                4
                            ),

                        "interpretation":
                            interpret_strength(
                                cramers_v
                            ),

                        "chart":
                            "bar"
                    }
                )


    return relationships




# ==========================================
# Main Engine
# ==========================================

def discover_relationships(
    data,
    target=None,
    profile=None
):

    if profile is None:

        profile = {
            "id_columns": []
        }


    relationships = []


    relationships.extend(
        analyze_numeric_relationships(
            data,
            profile
        )
    )


    relationships.extend(
        analyze_categorical_relationships(
            data,
            profile
        )
    )


    relationships.extend(
        analyze_target_relationships(
            data,
            target,
            profile
        )
    )


    relationships = sorted(
        relationships,
        key=lambda x:
            x["strength"],
        reverse=True
    )


    return relationships[:15]