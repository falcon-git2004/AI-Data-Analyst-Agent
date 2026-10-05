import matplotlib.pyplot as plt


def create_bar_chart(data, column, output_path):
    """
    Create a bar chart from a selected column
    """

    if data is None:
        return

    plt.figure(figsize=(8, 5))

    data[column].value_counts().plot(kind="bar")

    plt.title(f"{column} Distribution")
    plt.xlabel(column)
    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()

    print(f"📊 Chart saved: {output_path}")