from tools import (
    load_data,
    clean_data,
    create_bar_chart,
    analyze_data,
    generate_report
)


class AgentExecutor:

    def __init__(self, plan):
        self.plan = plan
        self.data = None
        self.insights = None


    def execute(self, file_path):

        print("🤖 Agent Execution Started")

        for step in self.plan:

            if step == "load_data":

                self.data = load_data(file_path)


            elif step == "clean_data":

                self.data = clean_data(self.data)


            elif step == "visualize":

                create_bar_chart(
                    self.data,
                    "Category",
                    "reports/category_chart.png"
                )


            elif step == "generate_report":

                self.insights = analyze_data(self.data)

                print("\n🧠 Data Insights:")

                for key, value in self.insights.items():
                    print(f"{key}: {value}")


                generate_report(
                    self.insights,
                    "reports/AI_Analysis_Report.pdf"
                )


        print("\n✅ Agent Execution Finished")

        return self.data