from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

app.secret_key = os.getenv("SECRET_KEY", "change-me")  # required for sessions
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------- Public pages ---------
@app.route("/")
def home():
    return render_template("home.html")  # <-- simple homepage that explains the bot

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # Simple demo auth — replace with your real logic
        if username == "admin" and password == "password":
            session["user"] = username
            return redirect(url_for("chat"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# --------- Protected chat UI ---------
@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("login"))
    # Put your current main.html (the chatbot UI) in templates/main.html
    return render_template("main.html")

# --------- API ---------
@app.route('/ask', methods=['POST'])
def ask():
    # Optionally enforce auth here:
    if "user" not in session:
        return jsonify({"reply": "Unauthorized"}), 401

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
        answer = response.choices[0].message.content
        return jsonify({"reply": answer.strip()})
    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Render usually provides PORT
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
