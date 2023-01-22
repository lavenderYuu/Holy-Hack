import os
import uuid
import openai
import requests
from flask import Flask, redirect, render_template, request, url_for, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")
history = {}

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.set_cookie("session_id", str(uuid.uuid4()))
    return response

@app.route('/chatbox')
def chatBox():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect("/")
    return render_template('chatTest.html')

@app.route('/session_id')
def sessionId():
    return {
        "session_id": str(uuid.uuid4())
    }

@app.route("/chat", methods=["POST"])
def chat():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect("/")
    body = request.get_json()
    if session_id not in history:
        history[session_id] = ""
    text = history[session_id] + "\nYou: " + body["text"] + "\nBot:"
    history[session_id] = text
    response = openai.Completion.create(
        model=model,
        prompt=text,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["Bot:", "You:"]
    )
    respond_text = response.choices[0].text
    history[session_id] = history[session_id] + respond_text
    return {
        "text": respond_text
    }

@app.route("/image", methods=["GET", "POST"])
def image():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect("/")
    if request.method == "POST":
        body = request.get_json()
        response = openai.Image.create(
            prompt=body["prompts"],
            n=1,
            size="256x256"
        )
        img_data = requests.get(response['data'][0]['url']).content
        filename = '{}/static/img/{}.png'.format(os.getcwd(), session_id)
        f = open(filename, 'wb+')
        f.write(img_data)
        f.close()
        return {}
    elif request.method == "GET":
        pass
