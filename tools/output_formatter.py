def format_output(insights):

    print("\n" + "=" * 50)
    print("🤖 AI DATA ANALYSIS SUMMARY")
    print("=" * 50)


    # Dataset Overview

    if "dataset_overview" in insights:

        print("\n📊 Dataset Overview")

        overview = insights["dataset_overview"]

        for key, value in overview.items():

            print(
                f"- {key.replace('_',' ').title()}: {value}"
            )


    # AI Insights

    if "ai_insights" in insights:

        print("\n🧠 AI Findings")


        for index, item in enumerate(
            insights["ai_insights"],
            start=1
        ):

            print(
                f"\n{index}. {item['title']}"
            )

            print(
                f"   Finding: {item['finding']}"
            )

            print(
                f"   Recommendation: {item['recommendation']}"
            )



    # Relationships

    if "relationship_findings" in insights:

        print("\n🔗 Important Relationships")


        for relationship in insights["relationship_findings"]:

            print(
                f"- {relationship['between'][0]} "
                f"↔ "
                f"{relationship['between'][1]}"
            )

            print(
                f"  Strength: {relationship['strength']}"
            )



    # Distribution

    if "distribution_analysis" in insights:

        print("\n📈 Distribution Findings")


        numeric = (
            insights["distribution_analysis"]
            .get(
                "numeric_distribution",
                []
            )
        )


        for item in numeric:

            print(
                f"- {item['column']}: "
                f"{item['distribution']}"
            )


    print("\n" + "=" * 50)