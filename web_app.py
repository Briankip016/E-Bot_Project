from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from datetime import datetime
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    mode = data.get("mode", "general")

    full_prompt = f"[Mode: {mode}] {prompt}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful AI code assistant in {mode} mode."},
                {"role": "user", "content": full_prompt}
            ]
        )
        answer = response['choices'][0]['message']['content']
        return jsonify({"reply": answer.strip()})
    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
