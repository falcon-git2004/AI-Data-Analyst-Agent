from agent.planner import DataAnalysisAgent
from agent.executor import AgentExecutor


file_path = "data/sample.csv"


# Create the plan
agent = DataAnalysisAgent()

plan = agent.plan(
    "Analyze my sales data"
)


print("\n🤖 Agent Plan:")
for step in plan:
    print("-", step)


# Execute the plan
executor = AgentExecutor(plan)

result = executor.execute(file_path)