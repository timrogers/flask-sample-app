# app/routes.py

from app import app
from flask import request
import uuid

# Dictionary to store items with their UUIDs as keys
items = {}

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items():
    return {'items': [{'id': item_id, **item} for item_id, item in items.items()]}

@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    if item_id in items:
        return {'item': {'id': item_id, **items[item_id]}}
    return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json()
    item_id = str(uuid.uuid4())
    items[item_id] = item
    return {'message': 'Item added successfully', 'item': {'id': item_id, **item}}, 201

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in items:
        deleted_item = items.pop(item_id)
        return {'message': 'Item deleted successfully', 'item': {'id': item_id, **deleted_item}}, 200
    return {'error': 'Item not found'}, 404
