from g4f.client import Client

client = Client()

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
    content = f"""
Act as an agronomist. Explain why {pred_mm:.1f} mm irrigation is needed for {crop}.

Context:
- {days_since} days since sowing
- {days_since_last_water} days since last water
- Temperature: {temp_avg:.1f}°C
- ET0: {et0:.1f} mm/day
- 7d Precipitation: {precip_7d:.1f} mm
- Wind: {wind:.2f} m/s
- Soil Moisture: {soil_moisture:.2f}

Thresholds:
- Maize: High Temp >30, Low Rain <5, High ET0 >6
- Wheat: High Temp >27, Low Rain <7, High ET0 >5

Rules:
- Write one professional paragraph (6–10 sentences).
- Explain why exactly {pred_mm:.1f} mm is needed.
- Connect crop stage, weather, and soil conditions.
- Do not change the irrigation amount.
- Do not mention AI, model, or prediction system.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in GPT explanation: {e}")
        return "Explanation unavailable at the moment."


def ask_gemini_chat(user_question):
    system_instr = """
You are an AI assistant for a water-saving website.
Rules:
- Answer in the user's language.
- Do not give exact water amounts.
- The website helps farmers conserve water using weather data and crop types.
- Be clear, short, and practical.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instr},
                {"role": "user", "content": user_question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"DEBUG ERROR in GPT Chat: {e}")
        return "I'm having trouble connecting right now. Try again later!"