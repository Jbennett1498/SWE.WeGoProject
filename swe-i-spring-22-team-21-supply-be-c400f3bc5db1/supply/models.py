import requests as requests
from flask_mongoengine import Document, MongoEngine
from mongoengine import ReferenceField, IntField, EnumField, StringField, DynamicField

from supply.enums import CarStatus, JobStatus
from supply.map_services import get_durations_matrix, get_route
from supply.utils import gen_id

db = MongoEngine()


class Fleet(Document):
    id = StringField(primary_key=True, default=gen_id)
    name = StringField(required=True)
    service = StringField(required=True)
    owner = StringField(required=True)
    description = StringField()
    city = StringField()

    def get_vehicle_from_order(self, order):
        vehicles = Vehicle.objects(fleet=self.id, job_status=JobStatus.WAITING)

        if vehicles.count() == 0:
            return None

        coordinates = ';'.join([order['origin'], *[vehicle.position for vehicle in vehicles]])
        destinations = '0'
        sources = ';'.join([str(i) for i in range(1, vehicles.count() + 1)])
        response = get_durations_matrix(coordinates, destinations, sources)
        durations = map(lambda x: x[0], response['durations'])
        vehicles_with_durations = list(zip(vehicles, durations))

        closest_vehicle = None
        shortest_duration = None
        for vehicle, duration in vehicles_with_durations:
            if shortest_duration is None or duration < shortest_duration:
                closest_vehicle = vehicle
                shortest_duration = duration

        return closest_vehicle, shortest_duration


class Vehicle(Document):
    id = StringField(primary_key=True, default=gen_id)
    fleet = ReferenceField(Fleet, required=True)
    vin = StringField(required=True)
    make = StringField(required=True)
    model = StringField(required=True)
    year = IntField(required=True)
    # below are fields that are to be updated during a vehicle's heartbeat loop
    charge = IntField(default=100)
    mileage = IntField(default=0)
    service_status = EnumField(CarStatus, default=CarStatus.NORMAL)
    job_status = EnumField(JobStatus, default=JobStatus.NONE)
    dispatch = ReferenceField('Dispatch')  # defined as a string since the dispatch class has yet to be declared
    position = StringField()
    route = DynamicField()

    def set_route_from_order(self, order):
        coordinates = ';'.join([self.position, order['origin'], order['destination']])
        response = get_route(coordinates)
        self.route = response['routes']

    def set_dispatch(self, dispatch):
        self.dispatch = dispatch
        dispatch.vehicle = self


class Dispatch(Document):
    id = StringField(primary_key=True, default=gen_id)
    customer = StringField(required=True)
    origin = StringField(required=True)
    destination = StringField(required=True)
    vehicle = ReferenceField(Vehicle)
