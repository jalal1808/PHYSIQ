import sqlite3
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("HealthKnowledgeBase")
DB_PATH = "knowledge_base.db"

def query_db(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

@mcp.tool()
def get_top_doctors(location, speciality: str = None) -> str:
    """Finds the top 3 doctors. Optionally filter by speciality OR location."""
    query = "SELECT name, designation, speciality, location, fee FROM doctors"
    if speciality:
        query += " WHERE speciality LIKE ?"
        results = query_db(query + " ORDER BY fee ASC LIMIT 3", (f"%{speciality}%",))
    elif location:
        query += " WHERE location LIKE ?"
        results = query_db(query + " ORDER BY fee ASC LIMIT 3", (f"%{location}%",))
    else:
        results = query_db(query + " ORDER BY fee ASC LIMIT 3")
    return str(results)

@mcp.tool()
def get_top_exercises(muscle_group: str = None) -> str:
    """Returns top 3 exercises based on rating. Filter by muscle group."""
    query = "SELECT exercise_name, muscle, equipment, rating FROM exercises"
    if muscle_group:
        query += " WHERE muscle LIKE ?"
        results = query_db(query + " ORDER BY rating DESC LIMIT 3", (f"%{muscle_group}%",))
    else:
        results = query_db(query + " ORDER BY rating DESC LIMIT 3")
    return str(results)

@mcp.tool()
def get_top_foods(goal: str = "weight_loss") -> str:
    """Returns top 3 foods for 'weight_loss' or 'weight_gain'."""
    sort_col = "weight_loss_rating" if goal == "weight_loss" else "weight_gain_rating"
    query = f"SELECT food_item, category, calories, protein FROM food ORDER BY {sort_col} DESC LIMIT 3"
    results = query_db(query)
    return str(results)

@mcp.tool()
def calculate_sleep_debt(actual_sleep_hours: float, required_hours: float = 8.0) -> str:
    """Calculates sleep debt for a single day and provides a recovery tip."""
    debt = required_hours - actual_sleep_hours
    status = "Credit" if debt <= 0 else "Debt"
    
    advice = "Great job!" if debt <= 0 else "Try a 20-min power nap today."
    return f"Status: {status} | Difference: {abs(debt)} hours. Advice: {advice}"

@mcp.tool()
def get_sleep_hygiene_tips(issue: str = "general") -> str:
    """Provides science-based tips for specific sleep issues like 'insomnia' or 'restlessness'."""
    tips = {
        "insomnia": "Avoid screens 1hr before bed; try magnesium-rich foods.",
        "restlessness": "Keep your room at 18°C (65°F); use a weighted blanket.",
        "general": "Stick to a consistent wake-up time even on weekends."
    }
    return tips.get(issue.lower(), tips["general"])

@mcp.tool()
def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """Calculates BMI and returns the health category."""
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m**2), 1)
    
    if bmi < 18.5:
        category = "Underweight (Goal: weight_gain)"
    elif 18.5 <= bmi < 25:
        category = "Healthy weight (Goal: weight_loss for maintenance)"
    elif 25 <= bmi < 30:
        category = "Overweight (Goal: weight_loss)"
    else:
        category = "Obese (Goal: weight_loss)"
        
    return f"Your BMI is {bmi} ({category})."

if __name__ == "__main__":
    mcp.run(transport="stdio")