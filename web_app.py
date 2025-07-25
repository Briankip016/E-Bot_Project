from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message', '')
    mode = data.get('mode', 'general')

    # Build a system prompt based on selected mode
    if mode == 'mini-lesson':
        system_prompt = "You are a programming tutor. Explain the concept in a short and clear way, suitable for a beginner."
    elif mode == 'bug-fix':
        system_prompt = "You are a programming assistant that helps fix bugs. Read the code and provide corrections with brief explanations."
    elif mode == 'quiz':
        system_prompt = "You are a programming quiz master. Ask the user a beginner-level quiz question related to programming."
    else:  # General mode
        system_prompt = "You are an AI programming assistant that answers coding questions clearly and helpfully."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or gpt-3.5-turbo
            messages=messages
        )
        reply = response.choices[0].message.content
        return jsonify({'answer': reply})
    except Exception as e:
        return jsonify({'answer': f"⚠️ Error: {str(e)}"}), 500
