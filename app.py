import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS  # 追加

# Flaskアプリを定義（最初に書く！）
app = Flask(__name__)
CORS(app)  # 追加

# .envファイルの読み込み
load_dotenv()

# OpenAI APIキーを環境変数から取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "サーバーが動作しています！"

@app.route("/generate-dialogue", methods=["POST"])
def generate_dialogue():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "JSONデータが送信されていません"}), 400

        name = data.get("name", "名無し")
        personality = data.get("personality", "普通")
        profession = data.get("profession", "冒険者")

        prompt = f"""
        キャラクターの名前: {name}
        性格: {personality}
        職業: {profession}
        以下のセリフを生成してください：
        1. 初対面のメッセージ
        2. 励ましの言葉
        3. 戦闘中のセリフ
        4. 日常の挨拶
        """

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "あなたは親切なAIアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        response_data = response.json()

        print("OpenAI APIのレスポンス:", response_data)

        if response.status_code == 200:
            return jsonify({"dialogue": response_data["choices"][0]["message"]["content"].strip()}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({"error": response_data}), 500
    except Exception as e:
        print("❌ OpenAI APIエラー:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
