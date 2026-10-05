class DataAnalysisAgent:

    def __init__(self):
        self.steps = []


    def plan(self, task):

        task = task.lower()

        if "analyze" in task:
            self.steps = [
                "load_data",
                "clean_data",
                "visualize",
                "generate_report"
            ]

        else:
            self.steps = [
                "load_data"
            ]

        return self.steps