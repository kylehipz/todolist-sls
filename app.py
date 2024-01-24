import os
import uuid
from datetime import datetime

import boto3
import srl
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

dynamodb_client = boto3.client("dynamodb")

TODOS_TABLE = os.environ["TODOS_TABLE"]


@app.route("/todos", methods=["GET"])
def getTodos():
    result = dynamodb_client.scan(TableName=TODOS_TABLE)

    items = result.get("Items")
    deserialized = []

    for item in items:
        ds_item = srl.deserialize(item)
        print(ds_item)

        deserialized.append(ds_item)

    count = result.get("Count")

    return jsonify({"data": deserialized, "count": count})


@app.route("/todos", methods=["POST"])
def createTodo():
    body = request.json

    id = uuid.uuid4()
    content = body.get("content")
    createdAt = datetime.now().isoformat()

    todo = {
        "id": str(id),
        "content": content,
        "createdAt": createdAt,
    }

    serialized = srl.serialize(todo)

    dynamodb_client.put_item(TableName=TODOS_TABLE, Item=serialized)

    return (
        jsonify({"data": todo}),
        201,
    )


@app.route("/todos/<id>", methods=["PATCH"])
def updateTodo(id):
    body = request.json
    content = body.get("content")

    dynamodb_client.update_item(
        TableName=TODOS_TABLE,
        Key=srl.serialize({"id": id}),
        UpdateExpression="SET content = :content",
        ExpressionAttributeValues=srl.serialize({":content": content}),
    )

    return jsonify({"success": True, "content": content})


@app.route("/todos/<id>", methods=["DELETE"])
def deleteTodo(id):
    dynamodb_client.delete_item(TableName=TODOS_TABLE, Key=srl.serialize({"id": id}))
    return jsonify({"success": True})


@app.errorhandler(404)
def resourceNotFound(e):
    return make_response(jsonify(error="Not found!"), 404)
