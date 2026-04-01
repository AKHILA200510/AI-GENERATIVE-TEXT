from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
API_KEY = os.getenv("api")
if not API_KEY:
    raise ValueError("API key not found. Set GEMINI_API_KEY in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_input = data.get("message") if data else None

    if not user_input:
        return jsonify({"error": "Empty input"}), 400

    try:
        response = model.generate_content(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Render requires this
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)