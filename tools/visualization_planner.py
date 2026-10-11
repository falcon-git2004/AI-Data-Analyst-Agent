def choose_chart(relationship):


    relationship_type = relationship["type"]


    if relationship_type == "numeric_numeric":

        return {
            "chart": "scatter",
            "x": relationship["feature_1"],
            "y": relationship["feature_2"]
        }


    elif relationship_type == "numeric_target":

        return {
            "chart": "boxplot",
            "feature": relationship["feature_1"],
            "target": relationship["feature_2"]
        }


    elif relationship_type == "categorical_target":

        return {
            "chart": "bar",
            "feature": relationship["feature_1"],
            "target": relationship["feature_2"]
        }


    elif relationship_type == "categorical_categorical":

        return {
            "chart": "heatmap",
            "x": relationship["feature_1"],
            "y": relationship["feature_2"]
        }


    return None



def create_visualization_plan(
    relationships
):

    plans = []


    for relationship in relationships:

        chart_plan = choose_chart(
            relationship
        )


        if chart_plan:

            plans.append(
                chart_plan
            )


    return plans