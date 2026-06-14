from gevent import monkey
monkey.patch_all()
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import numpy as np
from datetime import datetime, date, timedelta
import pandas as pd
from chat.chat.openai_client import ask_openai, ask_openai_chat
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
import os
import traceback
from flask_socketio import SocketIO, emit, join_room
from flask_jwt_extended import decode_token

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)     # access — короткий
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=180)       # refresh — длинный
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_CSRF_CHECK_FORM"] = False 
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

database_url = os.environ.get("DATABASE_URL")

if database_url:
    database_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def custom_unauthorized_response(reason):
    # Этот код сработает, если в запросе вообще нет токена
    return jsonify({"error": "unauthorized", "message": reason}), 401

@jwt.invalid_token_loader
def custom_invalid_token_response(reason):
    # Этот код сработает, если токен есть, но он не правильный (ошибка 422)
    return jsonify({"error": "invalid_token", "message": reason}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": "token_expired",
        "message": "Access token has expired"
    }), 401

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    crop = db.Column(db.String(50), nullable=True)
    sowing_date = db.Column(db.String(10), nullable=True)
    last_irrigation_date = db.Column(db.String(10), nullable=True)   #при регистрации
    last_irrigation_date_real = db.Column(db.DateTime, nullable=True) #кнопка высчитать

    water_used_mm = db.Column(db.Float, default=0.0)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)


class AIChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    message = db.Column(db.Text)
    response = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FarmerChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CommunityMessage(db.Model):
    __tablename__ = "community_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_name = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Irrigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    crop = db.Column(db.String(50))
    sowing_date = db.Column(db.String(20))
    calculation_date = db.Column(db.String(20))
    last_watering_date = db.Column(db.String(20))

    water_mm = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Создание базы
with app.app_context():
    db.create_all()

@app.route('/set_crop', methods=['POST'])
@jwt_required()
def set_crop():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    crop = data.get('crop')
    
    if crop not in ['Maize', 'Wheat']:
        return jsonify({"error": "Invalid crop (only Maize or Wheat)"}), 400
    
    user.crop = crop
    db.session.commit()
    
    return jsonify({
        "message": "Crop saved successfully",
        "crop": user.crop
    }), 200

@app.route('/set_sowing_date', methods=['POST'])
@jwt_required()
def set_sowing_date():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    date_str = data.get('sowing_date')
    
    if not date_str or not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return jsonify({"error": "Invalid date format (use YYYY-MM-DD)"}), 400
    
    user.sowing_date = date_str
    db.session.commit()
    
    return jsonify({
        "message": "Sowing date saved successfully",
        "sowing_date": user.sowing_date
    }), 200

@app.route('/set_initial_irrigation_date', methods=['POST'])
@jwt_required()
def set_initial_irrigation():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    date_str = data.get('last_irrigation_date')

    if not date_str or not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return jsonify({"error": "Ожидается формат YYYY-MM-DD"}), 400

    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        if d > datetime.now():
            return jsonify({"error": "Дата полива не может быть в будущем"}), 400
    except:
        return jsonify({"error": "Неверный формат даты"}), 400

    user.last_irrigation_date = date_str
    db.session.commit()

    return jsonify({"message": "Дата последнего полива сохранена", "date": date_str}), 200

@app.route('/debug_user', methods=['GET'])
@jwt_required()
def debug_user():
    """Временный эндпоинт для проверки пользователя"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "crop": user.crop,
            "has_crop": user.crop is not None,
            "registered_at": str(user.registered_at)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#отметка полива вручную
@app.route('/update_irrigation_date', methods=['POST'])
@jwt_required()
def update_irrigation_date():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    date_str = data.get('irrigation_date')
    
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    try:
        irrigation_date = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return jsonify({"error": "Неверный формат даты"}), 400
    
    user.last_irrigation_date = date_str
    user.last_irrigation_date_real = irrigation_date
    db.session.commit()
    
    return jsonify({
        "message": "Дата полива обновлена",
        "date": date_str
    }), 200


@app.route('/get_sowing_date', methods=['GET'])
@jwt_required()
def get_sowing_date():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "sowing_date": user.sowing_date
    }), 200

@app.route('/get_last_irrigation_date', methods=['GET'])
@jwt_required()
def get_last_irrigation_date():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "last_irrigation_date": user.last_irrigation_date,
        "last_irrigation_date_real": user.last_irrigation_date_real.strftime("%Y-%m-%d %H:%M:%S") if user.last_irrigation_date_real else None
    }), 200

    
@app.route("/community/messages", methods=["GET"])
@jwt_required()
def get_community_messages():
    current_user_id = get_jwt_identity()

    messages = CommunityMessage.query.order_by(CommunityMessage.created_at.asc()).all()

    result = []
    for msg in messages:
        result.append({
            "id": msg.id,
            "user": msg.user_name,
            "text": msg.text,
            "time": msg.created_at.strftime("%H:%M"),
            "sent": str(msg.user_id) == str(current_user_id),
        })

    return jsonify(result), 200

@socketio.on("connect")
def handle_connect(auth):
    try:
        if not auth or "token" not in auth:
            return False

        token = auth["token"]
        decoded = decode_token(token)
        user_id = decoded["sub"]

        user = User.query.get(user_id)
        if not user:
            return False

        join_room("farmers_community")

        emit("connected", {"message": "Connected successfully"})

    except Exception as e:
        print("Socket connect error:", e)
        return False

@socketio.on("send_message")
def handle_send_message(data):
    try:
        # Берем токен из данных, которые прислал фронтенд
        token = data.get("token")
        text = (data.get("text") or "").strip()

        if not token or not text:
            return

        # Декодируем и ищем юзера
        decoded = decode_token(token)
        user_id = decoded["sub"]
        user = User.query.get(user_id)

        if user:
            # Сохраняем в базу данных CommunityMessage
            new_msg = CommunityMessage(
                user_id=user.id,
                user_name=user.name,
                text=text
            )
            db.session.add(new_msg)
            db.session.commit()

            # Рассылаем ВСЕМ в комнате
            emit("new_message", {
                "id": new_msg.id,
                "user": user.name,
                "text": text,
                "time": new_msg.created_at.strftime("%H:%M"),
                "user_id": user.id
            }, room="farmers_community")
    except Exception as e:
        print(f"Chat Error: {e}")

# Регистрация
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))
    refresh_token = create_refresh_token(identity=str(new_user.id))

    return jsonify({
    "message": "User registered successfully",
    "access_token": access_token,
    "refresh_token": refresh_token,
    "user": {
        "name": new_user.name}
    }), 201

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Логин
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "name": user.name
            }
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/profile_stats', methods=['GET'])
@jwt_required()
def profile_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # отслеживание = сегодня - registered_at
    today = datetime.utcnow().date()
    reg_date = user.registered_at.date()
    days_tracked = (today - reg_date).days + 1  # +1 чтобы день регистрации тоже считался
    
    # Сумма воды
    water_used = user.water_used_mm or 0
    
    return jsonify({
        "days_tracked": days_tracked,
        "water_used_mm": round(water_used, 1),
        "registered_at": user.registered_at.strftime("%Y-%m-%d") if user.registered_at else None
    }), 200

# refresh
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200


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
    if hasattr(model, "n_features_in_"):
        print("Ожидаемое количество признаков:", model.n_features_in_)
    else:
        print("Модель загружена, но n_features_in_ отсутствует")
except Exception as e:
    print(f"Model loading error: {e}")
    model = None


@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Watering calculation API. Use POST /predict",
        "required_fields": ["sowing_date", "crop", "simulated_date"],
        "optional_fields": ["lastWateringDate"]
    })
@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    user_id = get_jwt_identity()

    print("=== НОВЫЙ POST /predict ===")
    print("Метод:", request.method)
    print("Headers:", dict(request.headers))
    print("Raw body (байты):", request.data)
    print("Content-Type из заголовков:", request.headers.get('Content-Type'))

    if model is None:
        return jsonify({"error": "Модель не загружена"}), 500
    data = request.get_json()

    crop_val = data.get("crop")

    if crop_val in [0, "0", "Maize", "maize"]:
        crop = 0
    elif crop_val in [1, "1", "Wheat", "wheat"]:
        crop = 1
    else:
        return jsonify({"error": "Invalid crop"}), 400
    
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
        float(crop)
        ]])
        print("12. Features сформированы:", features.shape)
        print("13. Запуск модели")
        pred_mm = float(model.predict(features)[0])
        print("14. Модель отработала, pred_mm:", pred_mm)

        explanation = ask_openai(
            crop="maize" if crop == 0 else "wheat",
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

        new_irrigation = Irrigation(
            user_id=user_id,
            crop="maize" if crop == 0 else "wheat",
            sowing_date=sowing_date_str,
            calculation_date=simulated_date_str,
            last_watering_date=last_watering_str,
            water_mm=float(pred_mm)
        )
        db.session.add(new_irrigation)
        db.session.commit()

        # Обновление water_used_mm у пользователя (добавляем pred_mm как сэкономленную воду)
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        user.water_used_mm = float(user.water_used_mm or 0.0) + float(pred_mm)
        db.session.commit()

        response = {
            "water_mm": round(float(pred_mm), 1),
            "unit": "mm (≈ liters per m²)",
            "phase_progress": round(phase_progress, 2),
            "phase_name": phase_name,
            "explanation": explanation,
            "calculation_date": simulated_date_str,
            "crop": "maize" if crop == 0 else "wheat",
            "days_since": days_since,
            "days_since_last_water": days_since_last_water
        }

        if simulated_date_str == datetime.now().strftime("%Y-%m-%d"):
            user = User.query.get(user_id)
            user.last_irrigation_date_real = datetime.now()
            db.session.commit()
            print(f"Automatically updated watering date for user {user_id}")

        return jsonify(response)
    except KeyError as e:
        print("ОШИБКА В PREDICT:", str(e))
        traceback.print_exc()
        return jsonify({"error": f"Отсутствует обязательное поле: {str(e)}"}), 400
    except ValueError as e:
        print("ОШИБКА В PREDICT ValueError:", str(e))
        traceback.print_exc()
        return jsonify({"error": f"Неверный формат даты или числа: {str(e)}"}), 400
    except Exception as e:
        print("ОШИБКА В PREDICT Exception:", str(e))
        traceback.print_exc()
        return jsonify({"error": f"Внутренняя ошибка: {str(e)}"}), 500

# маршрут для чата с AI
@app.route('/ai_chat', methods=['POST'])
@jwt_required()
def ai_chat():
    user_id = get_jwt_identity()
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({"error": "No message"}), 400

    response_text = ask_openai_chat(user_question=message)

    new_chat = AIChat(
        user_id=user_id,
        message=message,
        response=response_text
    )
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"response": response_text}), 200

# маршрут для истории чата с AI
@app.route('/ai_chat_history', methods=['GET'])
@jwt_required()
def ai_chat_history():
    user_id = get_jwt_identity()
    chats = AIChat.query.filter_by(user_id=user_id).order_by(AIChat.created_at.asc()).all()
    history = [{"message": chat.message, "response": chat.response, "created_at": chat.created_at} for chat in chats]
    return jsonify({"history": history}), 200

# маршрут для фермерского чата
@app.route('/farmer_chat', methods=['POST'])
@jwt_required()
def farmer_chat_post():
    user_id = get_jwt_identity()
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({"error": "Нет сообщения"}), 400

    new_message = FarmerChat(
        user_id=user_id,
        message=message
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Сообщение отправлено"}), 200

# Получение всех сообщений фермерского чата
@app.route('/farmer_chat', methods=['GET'])
@jwt_required()
def farmer_chat_get():
    messages = FarmerChat.query.order_by(FarmerChat.created_at.asc()).all()
    chat_data = []
    for msg in messages:
        user = User.query.get(msg.user_id)
        chat_data.append({
            "user_name": user.name,
            "message": msg.message,
            "created_at": msg.created_at
        })
    return jsonify({"messages": chat_data}), 200

# Получение истории ирригаций пользователя
@app.route('/irrigation_history', methods=['GET'])
@jwt_required()
def irrigation_history():
    user_id = get_jwt_identity()
    irrigations = Irrigation.query.filter_by(user_id=user_id).order_by(Irrigation.created_at.desc()).all()
    history = [{
        "crop": irr.crop,
        "sowing_date": irr.sowing_date,
        "calculation_date": irr.calculation_date,
        "last_watering_date": irr.last_watering_date,
        "water_mm": irr.water_mm,
        "created_at": irr.created_at
    } for irr in irrigations]
    return jsonify({"history": history}), 200

if __name__ == "__main__":
    # Используем socketio.run только для локального запуска
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)