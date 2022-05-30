from unittest import TestCase

from common_services.app import create_test_app
from common_services.user import User


class TestLoginEndpoint(TestCase):

    def setUp(self):
        self.app = create_test_app()
        self.client = self.app.test_client()

        # create an example user
        user = User(first_name="Jane", last_name="Doe", date_of_birth="1970-1-1", email="jane@example.com")
        user.hashPass("crazypassword1!")
        user.save()

    # testing login function
    def test_login(self):
        data = {'email': 'jane@example.com', 'password': 'crazypassword1!' }
        response = self.client.post('/common/login', json=data).json
        self.assertTrue(response['status'] == 'success')
