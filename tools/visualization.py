import matplotlib.pyplot as plt
import pandas as pd


def create_chart(
    data,
    chart_plan,
    output_path
):

    if data is None or data.empty:
        print("⚠️ No data available.")
        return None


    chart_type = chart_plan["chart"]


    plt.figure(figsize=(8, 5))


    # ==============================
    # Boxplot
    # ==============================

    if chart_type == "boxplot":

        feature = chart_plan["feature"]
        target = chart_plan["target"]


        data.boxplot(
            column=feature,
            by=target
        )


        plt.title(
            f"{feature} vs {target}"
        )

        plt.suptitle("")



    # ==============================
    # Scatter
    # ==============================

    elif chart_type == "scatter":

        x = chart_plan["x"]
        y = chart_plan["y"]


        plt.scatter(
            data[x],
            data[y]
        )


        plt.xlabel(x)
        plt.ylabel(y)

        plt.title(
            f"{x} vs {y}"
        )



    # ==============================
    # Bar
    # ==============================

    elif chart_type == "bar":

        feature = chart_plan["feature"]
        target = chart_plan["target"]


        (
            data.groupby(feature)[target]
            .mean()
            .plot(kind="bar")
        )


        plt.ylabel(
            "Average"
        )

        plt.title(
            f"{feature} vs {target}"
        )



    # ==============================
    # Heatmap
    # ==============================

    elif chart_type == "heatmap":

        import seaborn as sns


        x = chart_plan["x"]
        y = chart_plan["y"]


        table = pd.crosstab(
            data[x],
            data[y]
        )


        sns.heatmap(
            table,
            annot=True,
            fmt="d"
        )


        plt.title(
            f"{x} vs {y}"
        )



    else:

        print(
            "⚠️ Unknown chart type"
        )

        plt.close()

        return None



    plt.tight_layout()

    plt.savefig(
        output_path
    )

    plt.close()


    print(
        f"📊 {chart_type} chart saved: {output_path}"
    )


    return {
        "chart_type": chart_type,
        "output_path": output_path
    }