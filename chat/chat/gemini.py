import os
from google import genai

API_KEYS = [
    os.getenv("API_KEY_1"),
    os.getenv("API_KEY_2")
]

def ask_gemini(
    crop,
    days_since,
    days_since_last_water,
    temp_avg,
    et0,
    precip_7d,
    wind,
    soil_moisture,
    pred_mm
):
    client = genai.Client(api_key=API_KEY_1)

    contents=f"""
Act as an agronomist. Explain why {pred_mm:.1f}mm irrigation is needed for {crop}.
Context: {days_since} days since sowing, {days_since_last_water} days since last water.
Weather: {temp_avg:.1f}°C, ET0: {et0:.1f}mm/day, 7d Precip: {precip_7d:.1f}mm, Wind: {wind:.2f}m/s, Soil Moisture: {soil_moisture:.2f}.
Thresholds (High Temp/Low Rain/High ET0): Maize (>30/ <5/ >6), Wheat (>27/ <7/ >5).

Rules:
- Professional 1-paragraph explanation (6-10 sentences).
- Connect weather, stage, and soil to the {pred_mm:.1f}mm amount.
- Don't change amount. Don't mention AI/Models.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            contents=contents
        )
        return response.text
    except Exception as e:
        print(f"Error in Gemini: {e}")
        return "Explanation unavailable at the moment."
    
def ask_gemini_chat(user_question):
    client = genai.Client(api_key=API_KEY_2)

    system_instr = """You are an AI assistant for a water-saving website. 
    Rules: Answer in user's language. Don't give exact water amounts. 
    Website helps farmers conserve water using weather data and crop types."""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            contents=f"{system_instr}\n\nUser: {user_question}"
        )
        return response.text
    except Exception as e:
        print(f"DEBUG ERROR in Gemini Chat: {e}")
        return "I'm having trouble connecting to my brain. Try again later!"

