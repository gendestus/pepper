from flask import Flask, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
todos = []

with open("/app/app/system.txt", "r", encoding="utf-8") as system_prompt_file:
    system_prompt = system_prompt_file.read()


def generate_response(system_message: str, user_message: str) -> str:
    oai_api_key = os.getenv("OPENAI_API_KEY")

    if not oai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(
        api_key=oai_api_key,
    )

    response = client.responses.create(
        model="gpt-4o",
        instructions=system_message,
        input=user_message,
    )
    return response.output_text

@app.route("/priority", methods=["POST"])
def priority():
    if request.method == "POST":
        data = request.get_json()
        # To be filled in later by a database call
        tasks = []

        time_available = data.get('time_available', '')
        user_message = data.get('user_message', '')
        
        tasks_prompt = "Tasks:\n"
        for task in tasks:
            tasks_prompt += f"- {task}\n"
        if not tasks:
            tasks_prompt += "No tasks right now.\n"
        tasks_prompt += f"Time available: {time_available}\n"
        if user_message:
            tasks_prompt += f"User message: {user_message}\n"
        return generate_response(system_prompt, tasks_prompt)

    return "Method not allowed", 405

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
