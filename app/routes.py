# app/routes.py

from app import app
from flask import request

items = []

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items():
    return {'items': [{'id': i, **item} for i, item in enumerate(items)]}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if item_id < len(items):
        return {'item': {'id': item_id, **items[item_id]}}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json()
    items.append(item)
    item_id = len(items) - 1
    return {'message': 'Item added successfully', 'item': {'id': item_id, **item}}, 201

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id < len(items):
        deleted_item = items.pop(item_id)
        return {'message': 'Item deleted successfully', 'item': {'id': item_id, **deleted_item}}, 200
    else:
        return {'error': 'Item not found'}, 404
