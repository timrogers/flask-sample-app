import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_mark_todo_as_completed(client):
    # First create a todo item
    response = client.post('/items', json={'title': 'Test todo', 'completed': False})
    assert response.status_code == 201

    # Get all items to find the ID
    response = client.get('/items')
    items = response.get_json()['items']
    assert len(items) == 1
    item_id = 0  # First item has ID 0

    # Mark the todo as completed
    response = client.patch(f'/items/{item_id}/complete')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['item']['completed'] is True

    # Verify the item is completed by getting it
    response = client.get(f'/items/{item_id}')
    assert response.status_code == 200
    item = response.get_json()['item']
    assert item['completed'] is True

def test_mark_nonexistent_todo_as_completed(client):
    # Try to mark a non-existent todo as completed
    response = client.patch('/items/999/complete')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Item not found'