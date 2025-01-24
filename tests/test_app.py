# tests/test_app.py

import unittest
from app import app

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self):
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Item added successfully'})

    def test_get_item_route(self):
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1'}})

    def test_get_nonexistent_item_route(self):
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_mark_todo_as_completed(self):
        # First create a todo item
        response = self.app.post('/items', json={'title': 'Test todo', 'completed': False})
        self.assertEqual(response.status_code, 201)

        # Get all items to find the ID
        response = self.app.get('/items')
        items = response.get_json()['items']
        self.assertEqual(len(items), 1)
        item_id = 0  # First item has ID 0

        # Mark the todo as completed
        response = self.app.patch(f'/items/{item_id}/complete')
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertTrue(response_data['item']['completed'])

        # Verify the item is completed by getting it
        response = self.app.get(f'/items/{item_id}')
        self.assertEqual(response.status_code, 200)
        item = response.get_json()['item']
        self.assertTrue(item['completed'])

    def test_mark_nonexistent_todo_as_completed(self):
        # Try to mark a non-existent todo as completed
        response = self.app.patch('/items/999/complete')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['error'], 'Item not found')

if __name__ == '__main__':
    unittest.main()

