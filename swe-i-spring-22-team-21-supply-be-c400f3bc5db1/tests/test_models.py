from unittest import TestCase

from mongoengine import connect, disconnect

from supply.models import Fleet


class TestFleet(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_create_fleet(self):
        new_fleet = Fleet(name='Test Fleet', service='test-plugin', owner='test',
                          description='A test fleet.', city='test')
        new_fleet.save()

        fleet = Fleet.objects.first()
        self.assertTrue(fleet.name == 'Test Fleet')

    def test_delete_fleet(self):
        # Create our fleet
        new_fleet = Fleet(name='Test Fleet', service='test-plugin', owner='test',
                          description='A test fleet.', city='test')
        new_fleet.save()

        # Check if creation actually worked
        fleet = Fleet.objects(id=new_fleet.id).first()
        self.assertTrue(fleet.id == new_fleet.id)

        # Delete our fleet
        new_fleet.delete()

        # Check if the fleet is actually gone
        fleet = Fleet.objects(id=new_fleet.id).first()
        self.assertTrue(fleet is None)

    def test_update_fleet(self):
        # Create our fleet
        new_fleet = Fleet(name='Test Fleet', service='test-plugin', owner='test',
                          description='A test fleet.', city='test')
        new_fleet.save()

        # Check if creation actually worked
        fleet = Fleet.objects(id=new_fleet.id).first()
        self.assertTrue(fleet.id == new_fleet.id)

        # Update our fleet
        new_description = 'Beyond the walls of intelligence, life is defined.'
        new_fleet.update(description=new_description)

        fleet = Fleet.objects(id=new_fleet.id).first()
        self.assertTrue(fleet.description == new_description)