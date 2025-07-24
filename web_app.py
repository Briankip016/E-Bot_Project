from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import openai
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')  # homepage explaining your bot

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple hardcoded login for demo
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI code assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response['choices'][0]['message']['content']
    return jsonify({'reply': reply})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
