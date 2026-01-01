import sys
import os
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm

from app.prompt import prompt
# from app.mcp_server import mcp_tools

from google.adk.apps import App
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams

KB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "tools.py")
)

mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params={
            "command": sys.executable,  
            "args": [KB_PATH],
        },
        timeout=60.0,
    )
)

os.environ['GROQ_API_KEY']

llm_model = "gemini-2.5-flash" #groq/llama-3.1-8b-instant

nutritionist = Agent(
    name="Nutritionist",
    model=llm_model, 
    instruction=prompt.food,
    tools=[mcp_tools]
)

sleep_guardian = Agent(
    name="SleepGuardian",
    model=llm_model,
    instruction=prompt.sleep,
    tools=[mcp_tools]
)

fitness_coach = Agent(
    name="FitnessCoach",
    model=llm_model, 
    instruction=prompt.fitness,
    tools=[mcp_tools]
)

medical_assistant = Agent(
    name="MedicalAssistant",
    model=llm_model,
    instruction=prompt.medical_assistant,
    tools=[mcp_tools]
)


coordinator = Agent(
    name="HealthSystem",
    model=llm_model,
    instruction=prompt.coordination,
    sub_agents=[sleep_guardian, fitness_coach, medical_assistant, nutritionist]
)

root_agent = SequentialAgent(
    name="PhysiqAgent",
    description=(
        "PhysiqAgent is the primary entry point for users. "
        "It delegates all user requests to the HealthSystem coordinator, "
        "which routes them to the appropriate health specialist agent."
    ),
    sub_agents=[coordinator],
)
