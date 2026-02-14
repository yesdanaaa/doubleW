from flask import Flask, request, jsonify
from flask_cors import CORS
from ch.gemini import ask_gemini_chat

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200



    try:
        data = request.json
        if not data or "message" not in data:
            return jsonify({"reply": "No message provided"}), 400
        user_question = data.get("message")
        print(f"Вопрос пользователя: {user_question}")
        reply = ask_gemini_chat(user_question)
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Ошибка на сервере: {e}")
        return jsonify({"reply": "Sorry, server error occurred."}), 500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)