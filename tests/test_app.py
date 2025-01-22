# tests/test_app.py

import unittest
from app import app

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear the items list before each test
        from app.routes import items
        items.clear()

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self):
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            'message': 'Item added successfully',
            'item': {'id': 0, 'name': 'item1'}
        })

    def test_get_item_route(self):
        # First add an item
        self.app.post('/items', json={"name": "item1"})
        
        # Then get it
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'id': 0, 'name': 'item1'}})

    def test_get_nonexistent_item_route(self):
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_delete_item_route(self):
        # First add an item
        self.app.post('/items', json={"name": "item_to_delete"})
        
        # Then delete it
        response = self.app.delete('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'message': 'Item deleted successfully',
            'item': {'id': 0, 'name': 'item_to_delete'}
        })
        
        # Verify it's gone
        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_item_route(self):
        response = self.app.delete('/items/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_get_items_includes_ids(self):
        # Add a couple of items
        self.app.post('/items', json={"name": "item1"})
        self.app.post('/items', json={"name": "item2"})
        
        # Get the list
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        items = response.get_json()['items']
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0], {'id': 0, 'name': 'item1'})
        self.assertEqual(items[1], {'id': 1, 'name': 'item2'})

if __name__ == '__main__':
    unittest.main()

