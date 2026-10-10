from tools import (
    load_data,
    clean_data,
    analyze_data,
    generate_report
)

from tools.profiler import profile_dataset
from tools.relationship_engine import discover_relationships
from tools.visualization_planner import create_visualization_plan
from tools.visualization import create_chart
from tools.outlier_detector import detect_outliers
from tools.distribution_analyzer import analyze_distribution
from tools.insight_generator import generate_insights
from tools.output_formatter import format_output
from tools.quick_analyzer import quick_analyze



class AgentExecutor:


    def __init__(self, plan):

        self.plan = plan

        self.data = None

        self.insights = None

        self.profile = None

        self.relationships = []

        self.outliers = []

        self.distribution = {}

        self.visualization_plans = []

        self.chart_info = []

        self.ai_insights = []

        self.quick_result = {}



    def execute(self, file_path):

        print(
            "🤖 Agent Execution Started"
        )


        for step in self.plan:



            # ==========================
            # Load Data
            # ==========================

            if step == "load_data":

                self.data = load_data(
                    file_path
                )



            # ==========================
            # Clean Data
            # ==========================

            elif step == "clean_data":

                self.data = clean_data(
                    self.data
                )



            # ==========================
            # Quick Analysis
            # ==========================

            elif step == "quick_analysis":

                print(
                    "\n⚡ Running Quick Analysis..."
                )


                self.quick_result = quick_analyze(
                    self.data
                )


                format_output(
                    {
                        "quick_analysis":
                            self.quick_result
                    }
                )



            # ==========================
            # Profile Dataset
            # ==========================

            elif step == "profile_data":

                print(
                    "\n🔍 Understanding Dataset..."
                )


                self.profile = profile_dataset(
                    self.data
                )


                print(
                    f"Rows: {self.profile['rows']}"
                )


                print(
                    f"Columns: {self.profile['columns']}"
                )


                print(
                    "Detected Target:",
                    self.profile["detected_target"]
                )


                if "target_confidence" in self.profile:

                    print(
                        "Target Confidence:",
                        self.profile["target_confidence"]
                    )



            # ==========================
            # Outliers
            # ==========================

            elif step == "detect_outliers":

                print(
                    "\n🚨 Detecting Outliers..."
                )


                self.outliers = detect_outliers(
                    self.data,
                    self.profile
                )


                if self.outliers:

                    for outlier in self.outliers:

                        print(
                            outlier
                        )

                else:

                    print(
                        "No outliers detected."
                    )



            # ==========================
            # Distribution
            # ==========================

            elif step == "analyze_distribution":

                print(
                    "\n📈 Analyzing Data Distribution..."
                )


                self.distribution = analyze_distribution(
                    self.data,
                    self.profile
                )


                print(
                    self.distribution
                )



            # ==========================
            # Relationships
            # ==========================

            elif step == "discover_relationships":

                print(
                    "\n🔗 Discovering Relationships..."
                )


                self.relationships = discover_relationships(
                    self.data,
                    self.profile["detected_target"],
                    self.profile
                )


                for relationship in self.relationships[:5]:

                    print(
                        relationship
                    )



            # ==========================
            # Visualization
            # ==========================

            elif step == "visualize":

                print(
                    "\n📊 Creating Intelligent Visualizations..."
                )


                self.visualization_plans = create_visualization_plan(
                    self.relationships
                )


                for index, plan in enumerate(
                    self.visualization_plans
                ):


                    output_path = (
                        f"reports/chart_{index + 1}.png"
                    )


                    chart = create_chart(
                        self.data,
                        plan,
                        output_path
                    )


                    self.chart_info.append(
                        chart
                    )



            # ==========================
            # Deep Report
            # ==========================

            elif step == "generate_report":


                self.insights = analyze_data(
                    self.data,
                    self.relationships
                )


                self.insights[
                    "outlier_analysis"
                ] = self.outliers


                self.insights[
                    "distribution_analysis"
                ] = self.distribution



                self.ai_insights = generate_insights(
                    self.profile,
                    self.outliers,
                    self.distribution,
                    self.relationships
                )


                self.insights[
                    "ai_insights"
                ] = self.ai_insights



                print(
                    "\n🧠 Data Insights:"
                )


                format_output(
                    self.insights
                )



                generate_report(
                    self.insights,
                    "reports/AI_Analysis_Report.pdf",
                    self.chart_info
                )



        print(
            "\n✅ Agent Execution Finished"
        )


        return self.data