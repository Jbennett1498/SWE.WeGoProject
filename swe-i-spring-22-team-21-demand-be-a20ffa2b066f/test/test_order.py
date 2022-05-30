import unittest
from unittest import TestCase

from mongoengine import connect, disconnect

from demand.order import Order


class TestOrder(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create_fleet(self):
        new_order = Order(phone_number='123-456-7890', address='123 Main St.', city='Austin', state='Texas',
                          zip='10001')
        new_order.save()

        order = Order.objects.first()
        self.assertTrue(order.phone_number == '123-456-7890')
        self.assertTrue(order.address == '123 Main St.')
        self.assertTrue(order.city == 'Austin')
        self.assertTrue(order.state == 'Texas')

    @unittest.expectedFailure
    def test_order_regex(self):
        new_order = Order(phone_number='123-456-7890', address='123 Main St.', city='123', state='153Ab',
                          zip='10001')
        new_order.save()
