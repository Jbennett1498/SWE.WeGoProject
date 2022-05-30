import unittest
from unittest import TestCase

from mongoengine import connect, disconnect

from common_services.user import User


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    # testing password hashing
    def test_password_hashing(self):
        test_password = "crazypassword1!"
        user = User(first_name="Jane", last_name="Doe", date_of_birth="1970-1-1", email="jane@example.com")
        user.hashPass(test_password)
        user.save()
        self.assertTrue(user.comparePass(test_password))

    # test user email is unique
    @unittest.expectedFailure
    def test_unique_email(self):
        userTest1 = User(first_name="Sam", last_name="Smith", date_of_birth="1970-2-1", email="SamSmith@example.com")
        password1 = "random"
        userTest1.hashPass(password1)
        userTest1.save()
        userTest2 = User(first_name="Joe", last_name="Smith", date_of_birth="1970-2-1", email="SamSmith@example.com")
        password2 = "random2"
        userTest2.hashPass(password2)
        userTest2.save()



if __name__ == '__main__':
    unittest.main()
