from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates")
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    mode = data.get("mode", "general").strip().lower()

    # Supported modes
    allowed_modes = {
        "general": "You are a helpful AI assistant that answers general programming and software-related questions.",
        "lesson": "You are an educational tutor that gives beginner-friendly coding lessons. Explain concepts step-by-step.",
        "bugfix": "You are a debugging assistant. Find bugs in user code and explain how to fix them clearly.",
        "quiz": "You are a programming quiz bot. Ask coding-related quiz questions or explain quiz answers.",
        "explainer": "You are a code explainer bot. Explain what the provided code does in simple terms.",
        "career": "You are a programming career coach. Give advice on tech careers, interview prep, or portfolios."
    }

    if mode not in allowed_modes:
        return jsonify({"reply": "❌ Unsupported mode selected."}), 400

    # Create system and user messages
    system_prompt = allowed_modes[mode]
    user_message = prompt

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content.strip()

        # Optional: Add markdown styling or formatting if needed
        return jsonify({"reply": answer})

    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
