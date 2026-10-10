class DataAnalysisAgent:


    def __init__(self):

        self.steps = []



    def plan(self, task):

        task = task.lower()



        # ==========================
        # Quick Analysis Mode
        # ==========================

        if "quick" in task:


            self.steps = [

                "load_data",

                "clean_data",

                "quick_analysis"

            ]



        # ==========================
        # Deep Analysis Mode
        # ==========================

        elif "analyze" in task:


            self.steps = [

                "load_data",

                "clean_data",

                "profile_data",

                "detect_outliers",

                "analyze_distribution",

                "discover_relationships",

                "visualize",

                "generate_report"

            ]



        # ==========================
        # Default
        # ==========================

        else:


            self.steps = [

                "load_data"

            ]



        return self.steps