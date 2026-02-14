from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from datetime import datetime, date
import pandas as pd
from chat.chat.gemini import ask_gemini


app = Flask(__name__)
CORS(app)

weather_df = None
try:
    weather_df = pd.read_csv(
        "open-meteo-2025.csv",
        skiprows=2
        #header=0
    )
    weather_df['time'] = pd.to_datetime(weather_df['time'], errors='coerce')
    weather_df = weather_df.dropna(subset=['time'])
    weather_df['date'] = weather_df['time'].dt.date

    numeric_cols = [
        'temperature_2m (°C)',
        'et0_fao_evapotranspiration (mm)',
        'wind_speed_10m (km/h)',
        'soil_moisture_0_to_1cm (m³/m³)',
        'precipitation (mm)'
    ]

    for col in numeric_cols:
        if col in weather_df.columns:
            weather_df[col] = pd.to_numeric(weather_df[col], errors='coerce')
            print(f"Столбец '{col}' преобразован в float, NaN: {weather_df[col].isna().sum()}")

    print("CSV loaded successfully")
    print("Columns:", list(weather_df.columns))
    print(f"Rows: {len(weather_df)}, dates from {weather_df['date'].min()} to {weather_df['date'].max()}")
except Exception as e:
    print("Ошибка загрузки CSV:", e)
    weather_df = None
model = None
try:
    model = joblib.load("irrigation_model.pkl")
    print("Модель загружена успешно")
    print("Model type:", type(model))
    print("Model class name:", model._class._name_)

    if hasattr(model,"get_params"):
        print("Parameters:", model.get_params())

    print("Ожидаемое количество признаков:", model.n_features_in_)
    print("Model loaded successfully (irrigation_model.pkl)")
except Exception as e:
    print(f"Model loading error: {e}")
    print("Модель загружена, ожидает признаков:", model.n_features_in_)

    
    

    


@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Watering calculation API. Use POST /predict",
        "required_fields": ["sowing_date", "crop", "simulated_date"],
        "optional_fields": ["lastWateringDate"]
    })
@app.route('/predict', methods=['POST'])
def predict():
    print("=== НОВЫЙ POST /predict ===")
    print("Метод:", request.method)
    print("Headers:", dict(request.headers))
    print("Raw body (байты):", request.data)
    print("Content-Type из заголовков:", request.headers.get('Content-Type'))

    if model is None:
        return jsonify({"error": "Модель не загружена"}), 500
    data = request.get_json()
    if not data:
       return jsonify({"error": "Нет JSON"}), 400
    print("Запрос:", data)
    try:
        print("1. Начало try")
        simulated_date_str = data.get('simulated_date')
        print("2. simulated_date_str:", simulated_date_str)
        if not simulated_date_str:
            print("Нет simulated_date")
            return jsonify({"error": "Укажите simulated_date (YYYY-MM-DD)"}), 400
        simulated_date = datetime.strptime(simulated_date_str, "%Y-%m-%d").date()
        print("3. simulated_date распарсена:", simulated_date)

        sowing_date_str = data['sowing_date']
        print("4. sowing_date_str:", sowing_date_str)
        sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d").date()
        days_since = (simulated_date - sowing_date).days
        print("5. days_since:", days_since)
        if days_since < 0:
            return jsonify({"error": "Дата посева позже даты расчёта"}), 400
        
        #Дата последнего полива
        last_watering_str = data.get('lastWateringDate')
        print("6. last_watering_str:", last_watering_str)
        days_since_last_water = days_since
        if last_watering_str:
            last_watering_date = datetime.strptime(last_watering_str, "%Y-%m-%d").date()
            days_since_last_water = (simulated_date - last_watering_date).days
            print("7. days_since_last_water:", days_since_last_water)
            if days_since_last_water < 0:
                return jsonify({"error": "Дата полива позже даты расчёта"}), 400
            
        print("8. Погода — дефолты")    
        temp_avg = 25.0
        et0 = 5.0
        precip_7d = 0.0
        wind = 3.0
        soil_moisture = 0.25    

        if weather_df is not None:
            day_rows = weather_df[weather_df['date'] == simulated_date]

            if not day_rows.empty:
                temp_avg = day_rows['temperature_2m (°C)'].mean()

                if 'et0_fao_evapotranspiration (mm)' in day_rows.columns:
                    et0 = day_rows['et0_fao_evapotranspiration (mm)'].mean()

                precip_daily = day_rows['precipitation (mm)'].sum()
                start_7d = simulated_date - pd.Timedelta(days=6)
                week_rows = weather_df[(weather_df['date'] >= start_7d) & (weather_df['date'] <= simulated_date)]
                precip_7d = week_rows['precipitation (mm)'].sum()

                if 'wind_speed_10m (km/h)' in day_rows.columns:
                    wind = day_rows['wind_speed_10m (km/h)'].mean() / 3.6
                    
                if 'soil_moisture_0_to_1cm (m³/m³)' in day_rows.columns:
                    soil_moisture = day_rows['soil_moisture_0_to_1cm (m³/m³)'].mean()

                print(f"Погода для {simulated_date}: T={temp_avg:.1f}°C, ET0={et0:.1f}, Precip7d={precip_7d:.1f}мм")
            else:
                print(f"Дата {simulated_date} не найдена в CSV — используются дефолтные значения")
        else:
            print("CSV не загружен — используются дефолтные значения")

        print("Погода вычислена: temp_avg=", temp_avg, ", et0=", et0, ", precip_7d=", precip_7d, ", wind=", wind, ", soil_moisture=", soil_moisture)

        print("11. Формируем features")
        features = np.array([[
        temp_avg,
        et0,
        precip_7d,
        wind, 
        soil_moisture,
        float(days_since),
        float(days_since_last_water),
        float(data['crop'])
        ]])
        print("12. Features сформированы:", features.shape)
        print("13. Запуск модели")
        pred_mm = model.predict(features)[0]
        print("14. Модель отработала, pred_mm:", pred_mm)

        explanation = ask_gemini(
            crop="maize" if data['crop'] == 0 else "wheat",
            days_since=days_since,
            days_since_last_water=days_since_last_water,
            temp_avg=temp_avg,
            et0=et0,
            precip_7d=precip_7d,
            wind=wind,
            soil_moisture=soil_moisture,
            pred_mm=pred_mm
        )


        #faza rosta
        print("15. Возврат ответа")
        crop = int(data['crop'])
        approx_gdd = days_since * max((temp_avg - 10 if crop == 0 else temp_avg - 4), 0)
        if crop == 0:  # кукуруза
            total_gdd_to_maturity = 1800
            if days_since < 10 or approx_gdd < 100:
                phase_name = "Germination"
            elif approx_gdd < 600:
                phase_name = "Vegetative stage"
            elif approx_gdd < 1100:
                phase_name = "Flowering"
            elif approx_gdd < 1600: 
                phase_name = "Grain filling"
            else:
                phase_name = "Maturation"
        else:  # пшеница
            total_gdd_to_maturity = 1600
            if days_since < 20 or approx_gdd < 200:
                phase_name = "Seedling stage"
            elif approx_gdd < 700:
                phase_name = "Stem elongation"
            elif approx_gdd < 1100:
                phase_name = "Flowering"
            elif approx_gdd < 1500:
                phase_name = "Grain filling"
            else:
                phase_name = "Maturation"
        phase_progress = min(approx_gdd / total_gdd_to_maturity, 1.0)

        response = {
            "water_mm": round(float(pred_mm), 1),
            "unit": "mm (≈ liters per m²)",
            "phase_progress": round(phase_progress, 2),
            "phase_name": phase_name,
            "explanation": explanation,
            "calculation_date": simulated_date_str,
            "crop": "maize" if data['crop'] == 0 else "wheat",
            "days_since": days_since,
            "days_since_last_water": days_since_last_water
        }
        return jsonify(response)
    except KeyError as e:
        print("ОШИБКА В PREDICT:", str(e))
        return jsonify({"error": f"Отсутствует обязательное поле: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Неверный формат даты или числа: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Внутренняя ошибка: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)