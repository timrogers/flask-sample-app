# tests/test_app.py

import unittest
from app import app
import uuid

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear the items dictionary before each test
        from app.routes import items
        items.clear()

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self):
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        response_json = response.get_json()
        self.assertEqual(response_json['message'], 'Item added successfully')
        self.assertEqual(response_json['item']['name'], 'item1')
        # Verify UUID format
        uuid.UUID(response_json['item']['id'])

    def test_get_item_route(self):
        # First add an item
        add_response = self.app.post('/items', json={"name": "item1"})
        item_id = add_response.get_json()['item']['id']
        
        # Then get it
        response = self.app.get(f'/items/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'id': item_id, 'name': 'item1'}})

    def test_get_nonexistent_item_route(self):
        # Test with invalid UUID
        response = self.app.get('/items/not-a-uuid')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})
        
        # Test with non-existent UUID
        response = self.app.get(f'/items/{uuid.uuid4()}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_delete_item_route(self):
        # First add an item
        add_response = self.app.post('/items', json={"name": "item_to_delete"})
        item_id = add_response.get_json()['item']['id']
        
        # Then delete it
        response = self.app.delete(f'/items/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'message': 'Item deleted successfully',
            'item': {'id': item_id, 'name': 'item_to_delete'}
        })
        
        # Verify it's gone
        response = self.app.get(f'/items/{item_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_item_route(self):
        # Test with invalid UUID
        response = self.app.delete('/items/not-a-uuid')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})
        
        # Test with non-existent UUID
        response = self.app.delete(f'/items/{uuid.uuid4()}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_get_items_includes_ids(self):
        # Add a couple of items
        response1 = self.app.post('/items', json={"name": "item1"})
        response2 = self.app.post('/items', json={"name": "item2"})
        
        item1_id = response1.get_json()['item']['id']
        item2_id = response2.get_json()['item']['id']
        
        # Get the list
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        items = response.get_json()['items']
        self.assertEqual(len(items), 2)
        
        # Convert to set for unordered comparison
        items_set = {(item['id'], item['name']) for item in items}
        expected_set = {(item1_id, 'item1'), (item2_id, 'item2')}
        self.assertEqual(items_set, expected_set)

if __name__ == '__main__':
    unittest.main()

