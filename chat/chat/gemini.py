import os
from google import genai

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
    client = genai.Client(api_key="AIzaSyAvz2gBgfplWSVVgWemkWCE2yHNMDnFmqE")

    contents=f"""
You are an agricultural decision-support assistant.

The irrigation amount has already been calculated and must NOT be changed.
Your task is to clearly and convincingly explain why this specific amount of
irrigation is recommended under the given conditions.

Write in professional, agronomic English. The explanation should sound factual,
logical, and well-structured, as if written by an irrigation specialist.

Recommended irrigation: {pred_mm:.1f} mm

Agronomic thresholds:
- Maize: high temperature >30°C, low rainfall <5 mm/7 days, high ET0 >6 mm/day
- Wheat: high temperature >27°C, low rainfall <7 mm/7 days, high ET0 >5 mm/day

Context:
- Crop type: {crop}
- Days since sowing: {days_since}
- Days since last irrigation: {days_since_last_water}
- Average air temperature: {temp_avg:.1f} °C
- Reference evapotranspiration (ET0): {et0:.1f} mm/day
- Total precipitation over the last 7 days: {precip_7d:.1f} mm
- Average wind speed: {wind:.2f} m/s
- Soil moisture level: {soil_moisture:.2f}
- Recommended irrigation amount: {pred_mm:.1f} mm

Guidelines:
- Explain how temperature, rainfall, evapotranspiration, soil moisture,
  crop growth stage, and time since last irrigation affect water demand.
- If a factor is within a normal range, explain why it does not reduce irrigation needs.
- Emphasize potential water stress when rainfall is limited or evapotranspiration is high.
- Do NOT mention machine learning, models, or algorithms.
- Do NOT introduce new data or change the irrigation amount.
- Produce one coherent paragraph of 6–10 sentences.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=contents
        )
        return response.text
    except Exception as e:
        print(f"Error in Gemini: {e}")
        return "Explanation unavailable at the moment."