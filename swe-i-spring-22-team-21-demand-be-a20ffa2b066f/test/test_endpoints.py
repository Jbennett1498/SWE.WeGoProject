import json
from unittest import TestCase
from unittest.mock import patch

import requests

from demand import create_test_app
from demand.order import Order


class TestOrderEndpoint(TestCase):
    def setUp(self):
        self.app = create_test_app()
        self.client = self.app.test_client()

        # create an example order
        order = Order(phone_number='123-456-7890', address='123 Main St.', city='Austin', state='New York',
                      zip='10001')
        order.save()

    @patch('requests.post')
    def test_post(self, mock_post):
        info = {'number': '134-555-3342', 'address': '123 Main Street', 'city': 'Austin', 'state': 'texas',
                'zip': '34212'}
        resp = requests.post('/demand/order', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        mock_post.assert_called_with('/demand/order', data=json.dumps(info),
                                     headers={'Content-Type': 'application/json'})

        self.assertTrue(resp.status_code == 200)
        self.assertTrue(resp['order'] is not None)
        self.assertTrue(len(resp['order']) == 1)
        self.assertTrue(resp['order'][0]['city'] == 'Austin')
