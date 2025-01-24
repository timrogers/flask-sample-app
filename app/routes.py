# app/routes.py

from app import app
from flask import request

items = []

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/items', methods=['GET'])
def get_items():
    return {'items': items}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if item_id < len(items):
        return {'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404

@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json()
    if 'completed' not in item:
        item['completed'] = False
    items.append(item)
    return {'message': 'Item added successfully'}, 201

@app.route('/items/<int:item_id>/complete', methods=['PATCH'])
def complete_item(item_id):
    if item_id < len(items):
        items[item_id]['completed'] = True
        return {'message': 'Item marked as completed', 'item': items[item_id]}
    else:
        return {'error': 'Item not found'}, 404
