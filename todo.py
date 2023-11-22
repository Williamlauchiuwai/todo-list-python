from flask import Flask, jsonify, request, abort
from task import TaskDAO
import pymongo.errors

app = Flask('todoapp')
client = pymongo.MongoClient('mongodb://localhost')
database = client.todo_list
tasks_dao = TaskDAO(database)


@app.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = tasks_dao.list()
    return jsonify(tasks), 200


@app.route('/tasks/<pk>', methods=['GET'])
def get_task(pk):
    try:
        task = tasks_dao.read(pk)
        return jsonify(task)
    except pymongo.errors.NotFound:
        abort(404)


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title', None)
    description = data.get('description', None)

    if not title or not description:
        abort(400, "The fields 'title' and 'description' are required")

    task = tasks_dao.create(data)
    return jsonify(task), 201


if __name__ == '__main__':
    app.run()
