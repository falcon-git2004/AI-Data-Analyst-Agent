from tools.visualization_planner import create_visualization_plan


relationships = [

    {
        "feature_1": "Discount_offered",
        "feature_2": "Reached.on.Time_Y.N",
        "type": "numeric_target"
    },

    {
        "feature_1": "Weight_in_gms",
        "feature_2": "Cost_of_the_Product",
        "type": "numeric_numeric"
    }

]


plans = create_visualization_plan(
    relationships
)


for plan in plans:
    print(plan)