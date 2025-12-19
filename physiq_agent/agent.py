import os
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from prompt import prompt

os.environ['GROQ_API_KEY']

mcp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[os.path.abspath("kb_server.py")],
        )
    )
)

root_agent = Agent(
    name="Nutritionist",
    model="groq/llama-3.1-8b-instant", 
    instruction="food",
    tools=[mcp_tools]
)

# sleep_guardian = Agent(
#     name="SleepGuardian",
#     model="groq/llama-3.1-8b-instant",
#     instruction="sleep",
#     tools=[mcp_tools]
# )

# fitness_coach = Agent(
#     name="FitnessCoach",
#     model="groq/llama-3.1-8b-instant", 
#     instruction="fitness",
#     tools=[mcp_tools]
# )

# MedicalAssistant = Agent(
#     name="MedicalAssistant",
#     model="groq/llama-3.1-8b-instant",
#     instruction="medical_assistant",
#     tools=[mcp_tools]
# )

# coordinator = Agent(
#     name="HealthSystem",
#     model="gemini-2.5-flash",
#     instruction="""Route the user to the correct expert based on their need:
#     - Tired/Sleep/Circadian -> SleepGuardian
#     - Workouts/Muscle/Exercise -> FitnessCoach
#     - Doctors/Clinics/Specialists/Health issues -> HealthSpecialist
#     - Diet/BMI/Food/Weight goals -> Nutritionist
    
#     If the user's request is vague, ask clarifying questions.""",
#     sub_agents=[sleep_guardian, fitness_coach, health_specialist, nutritionist]
# )

# root_agent = SequentialAgent(
#     name="PhysiqAgent",
#     description="An agent thatRoute the user to the correct expert based on their need",
#     sub_agents=[coordinator],
# )
