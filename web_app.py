from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__, template_folder="templates")
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt", "")
    mode = data.get("mode", "lesson")

    if not prompt:
        return jsonify({"reply": "❗ Please enter a question or code."})

    # ✨ Mode-specific prompt instructions
    if mode == "bugfix":
        prompt = f"This code has a bug:\n\n{prompt}\n\nPlease explain what's wrong and give a fixed version."
    elif mode == "quiz":
        prompt = f"Create 3 multiple-choice questions with answers to test knowledge on: {prompt}"
    elif mode == "lesson":
        prompt = f"Explain this topic in 3 clear sentences for a beginner: {prompt}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply.strip()})
    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
