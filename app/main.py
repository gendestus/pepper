from flask import Flask, request, render_template
from openai import OpenAI
import os
import pyodbc
import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
todos = []

with open("/app/app/system.txt", "r", encoding="utf-8") as system_prompt_file:
    system_prompt = system_prompt_file.read()





def call_stored_procedure(proc_name, params=None, fetch_results=False):
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    conn_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password};Encrypt=no;"
    try:
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            if params:
                placeholders = ", ".join([f"@{key}=?" for key in params])
                values = list(params.values())
                sql = f"EXEC {proc_name} {placeholders}"
            else:
                sql = f"EXEC {proc_name}"
                values = []
            cursor.execute(sql, values)
            if fetch_results:
                results = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in results]

            conn.commit()

    except pyodbc.Error as e:
        print(f"Error calling stored procedure '{proc_name}': {e}")
        return None
    
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
def generate_creation_message(dt_created: datetime.datetime) -> str:
    # should output something like: created 8 days ago or created 2 hours ago
    now = datetime.datetime.now()
    delta = now - dt_created
    if delta.days > 0:
        return f"created {delta.days} days ago"
    elif delta.seconds // 3600 > 0:
        return f"created {delta.seconds // 3600} hours ago"
    else:
        return f"created {delta.seconds // 60} minutes ago"

@app.route("/priority", methods=["POST"])
def priority():
    if request.method == "POST":
        data = request.get_json()
        # To be filled in later by a database call
        tasks = call_stored_procedure("GetOpenItems", fetch_results=True)

        time_available = data.get('time_available', '')
        user_message = data.get('user_message', '')
        
        tasks_prompt = "Tasks:\n"
        for task in tasks:
            tasks_prompt += f"- {task['item']} ({generate_creation_message(task['created'])}) \n"
        if not tasks:
            tasks_prompt += "No tasks right now.\n"
        tasks_prompt += f"Time available: {time_available}\n"
        if user_message:
            tasks_prompt += f"User message: {user_message}\n"
        return generate_response(system_prompt, tasks_prompt)
        #return tasks_prompt

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
@app.route("/items", methods=["GET"])
def get_items():
    open_items = call_stored_procedure("GetOpenItems", fetch_results=True)
    item_messages = []
    for item in open_items:
        item_message = f"{item['item']} ({generate_creation_message(item['created'])})"
        item_messages.append(item_message)
    return {"items": item_messages}

@app.route("/add_item", methods=["POST"])
def add_item():
    data = request.get_json()
    item_name = data.get("item")
    if not item_name:
        return {"error": "Item name is required"}, 400

    params = {"item": item_name}
    call_stored_procedure("AddItem", params=params)
    return {"message": "Item added successfully"}, 201
