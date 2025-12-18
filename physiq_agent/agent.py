import os
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

os.environ['GROQ_API_KEY']

mcp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[os.path.abspath("kb_server.py")],
        )
    )
)

nutritionist = Agent(
    name="Nutritionist",
    model="groq/llama-3.1-8b-instant", 
    instruction="""You are a certified Nutritionist. 
    1. Always calculate the user's BMI first using 'calculate_bmi' if they provide weight/height.
    2. Based on the BMI category (weight_loss or weight_gain), use 'get_top_foods' 
       to suggest a specific meal plan.
    3. Be encouraging and focus on health metrics.""",
    tools=[mcp_tools]
)

sleep_guardian = Agent(
    name="SleepGuardian",
    model="groq/llama-3.1-8b-instant",
    instruction="""You are a certified Sleepguide. use 'get_top_foodscalculate_sleep_debt' to calculate sleep
    and 'get_sleep_hygiene_tips' to make a suggestion.
    1. Calculate sleep debt based on actual vs. recommended sleep.
    2. Suggest adjustments to bedtime, wake time, and nap strategies.
    3. Include guidance on circadian rhythm alignment.
    4. Encourage gradual, sustainable changes. """,
    tools=[mcp_tools]
)

fitness_coach = Agent(
    name="FitnessCoach",
    model="groq/llama-3.1-8b-instant", 
    instruction="""You are a certified FitnessCoach. use 'get_top_exercises' to make a suggestions
    according to the muscle user wants to follow.""",
    tools=[mcp_tools]
)

health_specialist = Agent(
    name="HealthSpecialist",
    model="groq/llama-3.1-8b-instant",
    instruction="""You are a certified HealthSpecialist. use 'get_top_doctors' 
    1. Analyize users problem and suggest a solution for it.
    2. Make a simple suggestion what could have led to the issue.
    3. use 'get_top_doctors' to suggest a doctor based on the users city and what the ussers problem was.
    4. Make sure to inform the user that seek professional help from the suggested doctors as yoy can only tell the probable issue. """,
    tools=[mcp_tools]
)

coordinator = Agent(
    name="HealthSystem",
    model="gemini-2.5-flash",
    instruction="""Route the user to the correct expert based on their need:
    - Tired/Sleep/Circadian -> SleepGuardian
    - Workouts/Muscle/Exercise -> FitnessCoach
    - Doctors/Clinics/Specialists/Health issues -> HealthSpecialist
    - Diet/BMI/Food/Weight goals -> Nutritionist
    
    If the user's request is vague, ask clarifying questions.""",
    sub_agents=[sleep_guardian, fitness_coach, health_specialist, nutritionist]
)

root_agent = SequentialAgent(
    name="PhysiqAgent",
    description="An agent thatRoute the user to the correct expert based on their need",
    sub_agents=[coordinator],
)

