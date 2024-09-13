import unittest
from flask import json
from app import app, db

class CustomerTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object('yourapplication.test_config')
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_post_customer(self):
        # Send a POST request
        response = self.client.post('/customers', json={
            'name': 'John Doe',
            'phone': '1234567890',
            'address': '123 Elm Street'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('John Doe', str(response.data))

    def test_get_customers(self):
        # First, insert a test customer
        response = self.client.post('/customers', json={
            'name': 'Jane Doe',
            'phone': '0987654321',
            'address': '321 Oak Street'
        })
        self.assertEqual(response.status_code, 201)

        # Now, fetch the list of customers
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Jane Doe', str(response.data))

if __name__ == '__main__':
    unittest.main()
