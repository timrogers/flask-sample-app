# app/routes.py

from app import app
from flask import request

items = []

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items():
    return {'items': [{'id': i + 1, **item} for i, item in enumerate(items)]}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if item_id < 1:
        return {'error': 'Item not found'}, 404
    list_index = item_id - 1
    if list_index < len(items):
        return {'item': {'id': item_id, **items[list_index]}}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json()
    items.append(item)
    item_id = len(items)  # One-based index
    return {'message': 'Item added successfully', 'item': {'id': item_id, **item}}, 201

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id < 1:
        return {'error': 'Item not found'}, 404
    list_index = item_id - 1
    if list_index < len(items):
        deleted_item = items.pop(list_index)
        return {'message': 'Item deleted successfully', 'item': {'id': item_id, **deleted_item}}, 200
    else:
        return {'error': 'Item not found'}, 404
