from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
todos = []

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    # if request.method == "POST":
    #     item = request.form["todo"]
        # todos.append(item)
        # prompt = "Here is my todo list:\n" + "\n".join(todos)
        # completion = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # response = completion["choices"][0]["message"]["content"]

    return render_template("index.html")
