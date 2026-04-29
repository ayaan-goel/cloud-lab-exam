from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB using environment variable (Docker service name = 'mongo')
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["tododb"]
todos = db["tasks"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Docker To-Do App</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #eee;
    }
    .container {
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 20px;
      padding: 40px;
      width: 500px;
      box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }
    h1 { font-size: 2rem; margin-bottom: 8px; color: #e94560; }
    p.sub { font-size: 0.85rem; color: #aaa; margin-bottom: 28px; }
    .input-row { display: flex; gap: 10px; margin-bottom: 24px; }
    input[type=text] {
      flex: 1;
      padding: 12px 16px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.15);
      background: rgba(255,255,255,0.08);
      color: #fff;
      font-size: 0.95rem;
      outline: none;
      transition: border 0.2s;
    }
    input[type=text]:focus { border-color: #e94560; }
    button {
      padding: 12px 20px;
      border-radius: 10px;
      border: none;
      background: #e94560;
      color: white;
      cursor: pointer;
      font-size: 0.95rem;
      font-weight: 600;
      transition: transform 0.1s, background 0.2s;
    }
    button:hover { background: #c73652; transform: scale(1.03); }
    .task-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
    .task-item {
      background: rgba(255,255,255,0.07);
      border-radius: 10px;
      padding: 14px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      border: 1px solid rgba(255,255,255,0.08);
      transition: background 0.2s;
    }
    .task-item:hover { background: rgba(233,69,96,0.1); }
    .task-text { flex: 1; font-size: 0.95rem; }
    .del-btn {
      background: rgba(233,69,96,0.2);
      border: 1px solid rgba(233,69,96,0.4);
      padding: 6px 12px;
      font-size: 0.8rem;
    }
    .del-btn:hover { background: #e94560; }
    .empty { color: #666; text-align: center; padding: 20px 0; font-style: italic; }
    .badge {
      background: #e94560;
      border-radius: 50px;
      padding: 2px 10px;
      font-size: 0.75rem;
      font-weight: bold;
      margin-left: 8px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>📝 Docker To-Do <span class="badge">Flask + MongoDB</span></h1>
    <p class="sub">Running inside Docker containers • Connected via Docker Network</p>
    <div class="input-row">
      <input type="text" id="taskInput" placeholder="Add a new task..." onkeypress="if(event.key==='Enter') addTask()" />
      <button onclick="addTask()">Add</button>
    </div>
    <ul class="task-list" id="taskList">
      {% if tasks %}
        {% for task in tasks %}
        <li class="task-item">
          <span class="task-text">{{ task['text'] }}</span>
          <button class="del-btn" onclick="deleteTask('{{ task['id'] }}')">Delete</button>
        </li>
        {% endfor %}
      {% else %}
        <li class="empty">No tasks yet. Add one above!</li>
      {% endif %}
    </ul>
  </div>
  <script>
    function addTask() {
      const input = document.getElementById('taskInput');
      const text = input.value.trim();
      if (!text) return;
      fetch('/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text})
      }).then(() => { input.value = ''; location.reload(); });
    }
    function deleteTask(id) {
      fetch('/delete/' + id, {method: 'DELETE'})
        .then(() => location.reload());
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    task_list = [{"id": str(t["_id"]), "text": t["text"]} for t in todos.find()]
    return render_template_string(HTML_TEMPLATE, tasks=task_list)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    if data and data.get("text"):
        todos.insert_one({"text": data["text"]})
    return jsonify({"status": "ok"})

@app.route("/delete/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    from bson import ObjectId
    todos.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
