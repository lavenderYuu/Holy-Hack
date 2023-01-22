import os
import uuid
import openai
import requests
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")
# model = "text-davinci-003"
history = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/session_id', methods=["GET"])
def get_id():
    session_id = uuid.uuid4()
    history[session_id] = ""
    return {
        "session_id": session_id
    }

@app.route("/chat", methods=["GET"])
def chat():
    if request["session_id"]:
        session_id = request["session_id"]
        if session_id not in history:
            history["session_id"] = ""
        text = history[session_id] + "\nYou: " + request["text"] + "\nBot:"
        history[session_id] = text
    else:
        return "Missing Session ID"
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
        "session_id": session_id,
        "text": respond_text
    }

@app.route("/image", methods=["GET", "POST"])
def image():
    if not request["session_id"]:
        return "Missing session ID"
    session_id = request["session_id"]
    if request.method == "GET":
        response = openai.Image.create(
            prompt=request["prompts"],
            n=1,
            size="128x128"
        )
        # filename = wget.download(response['data'][0]['url'], '/openAI/')
        img_data = requests.get(response['data'][0]['url']).content
        filename = '{}/openAI/{}.jpg'.format(os.getcwd(), request["session_id"])
        f = open(filename, 'wb+')
        f.write(img_data)
        f.close()
        return {
            "session_id": session_id,
            "image": filename,
        }
    elif request.method == "POST":
        pass
