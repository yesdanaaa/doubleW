import os
from google import genai

def ask_gemini_chat(user_question):
    api_key = "AIzaSyCMITxBny2faIscvtSxbxMc4u7BSptpYw8"
    
    try:
        client = genai.Client(api_key=api_key)
        system_instr = """You are an AI assistant for a water-saving website. 
        Rules: Answer in simple English. Never give exact water amounts—tell them to use the 'Calculate' button.
        ABOUT THE WEBSITE: This platform helps farmers conserve water in agriculture. It calculates the optimal irrigation amount based on: - crop type (e.g., corn, wheat)- sowing date - last irrigation date - weather data from Open-Meteo (temperature, humidity, rainfall, wind, evaporation, etc.) 
        Website Goals: The platform aims to promote efficient and sustainable water use in agriculture.Its primary objectives are:1. to help farmers conserve water resources by avoiding over-irrigation;2.to improve irrigation accuracy using crop type, sowing date, last watering date, and reliable weather data;3.to support environmentally sustainable farming practices;4.to increase crop productivity by ensuring plants receive sufficient but not excessive moisture;5.to digitalize agricultural decision-making through modern AI-based tools;6.to provide educational guidance about irrigation principles, crop needs, and weather influence;7.to offer accessible analytics without requiring technical expertise.. 
        Limit answers to 3-4 sentences."""
        for m in client.models.list():
          print(f"Доступная модель: {m.name}")
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=f"{system_instr}\n\nUser: {user_question}"
        )
        
        return response.text

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return f"Error: {e}"