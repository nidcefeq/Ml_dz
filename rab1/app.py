from flask import Flask, jsonify, request


app = Flask(__name__)
tasks = [
    {"id": 1, "title": "Learn Flask", "description": "Study Flask framework"},
    {"id": 2, "title": "Build a REST API", "description": "Create a simple REST API"}
]


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    return jsonify(tasks)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    t = None
    for task in tasks:
        if task["id"] == task_id:
            t = task
            break
    if t is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(t)


@app.route("/tasks", methods=["POST"])
def create_task():
    add_data = request.get_json()
    if not add_data or "title" not in add_data or "description" not in add_data:
        return jsonify({"error": "invalid input"}), 400

    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": add_data["title"],
        "description": add_data["description"],
    }

    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = None
    for t in tasks:
        if t["id"] == task_id:
            task = t
            break

    if task is None:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "Invalid input"}), 400
    task.update({"title": data["title"], "description": data["description"]})
    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True)
