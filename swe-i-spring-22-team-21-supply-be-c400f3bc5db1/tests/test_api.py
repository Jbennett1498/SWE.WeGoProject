from unittest import TestCase
from supply.app import create_test_app
from supply.models import Fleet


class TestFleetsEndpoint(TestCase):

    def setUp(self):
        self.app = create_test_app()
        self.client = self.app.test_client()

        fleet = Fleet(name="Test fleet", service='test-plugin', owner='testowner', description='test desc',
                      city='austin')
        fleet.save()

    def test_get(self):
        response = self.client.get('/fleets')
        data = response.json

        self.assertTrue(response.status_code == 200)
        self.assertTrue(data['fleets'] is not None)
        self.assertTrue(len(data['fleets']) == 1)
        self.assertTrue(data['fleets'][0]['name'] == 'Test fleet')
