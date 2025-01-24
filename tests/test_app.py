# tests/test_app.py

import unittest
from app import app

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear items before each test
        from app.routes import items
        items.clear()

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self):
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Item added successfully'})

        # Verify the item was added with completed=False by default
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1', 'completed': False}})

    def test_get_item_route(self):
        self.app.post('/items', json={"name": "item1"})
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1', 'completed': False}})

    def test_get_nonexistent_item_route(self):
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_complete_item_route(self):
        # Add a test item
        self.app.post('/items', json={"name": "test todo"})
        
        # Mark it as completed
        response = self.app.patch('/items/0/complete')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'message': 'Item marked as completed',
            'item': {'name': 'test todo', 'completed': True}
        })

        # Verify it's completed in the GET response
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'item': {'name': 'test todo', 'completed': True}
        })

    def test_complete_nonexistent_item_route(self):
        response = self.app.patch('/items/0/complete')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

if __name__ == '__main__':
    unittest.main()

