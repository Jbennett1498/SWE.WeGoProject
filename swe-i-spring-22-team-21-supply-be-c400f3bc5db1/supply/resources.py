import requests
from flask import request, Response, jsonify
from flask_restful import Resource, Api
from mongoengine import ValidationError, OperationError

from supply.enums import JobStatus
from supply.map_services import get_route
from supply.models import Fleet, Vehicle, Dispatch
from supply.utils import with_pagination

api = Api()


class FleetsEndpoint(Resource):
    # declaring a function as staticmethod doesn't actually do anything, just removes the pycharm warning
    @staticmethod
    def get():
        # available query parameters for this request
        service = request.args.get('service', default=None, type=str)
        city = request.args.get('city', default=None, type=str)
        sort = request.args.get('sort', default=None, type=str)
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)

        # ugh
        if service is not None and city is not None:
            fleets = Fleet.objects(service=service, city=city)
        elif service is not None:
            fleets = Fleet.objects(service=service)
        elif city is not None:
            fleets = Fleet.objects(city=city)
        else:
            fleets = Fleet.objects

        fleets = fleets.skip(offset).limit(limit)
        if sort is not None:
            fleets = fleets.order_by(sort)

        return jsonify({'fleets': fleets})

    # todo: needs to be made into authenticated route
    @staticmethod
    def post():
        body = request.json

        try:
            fleet = Fleet(**body)

            fleet.validate()
        except (KeyError, ValidationError) as e:
            print(e)
            return str(e), 400

        fleet.save()

        return {'id': fleet.id}, 201


class FleetEndpoint(Resource):
    @staticmethod
    def get(fleet_id):
        fleet = Fleet.objects(id=fleet_id).get_or_404()

        return jsonify(fleet)

    # todo: needs to be made into authenticated route
    @staticmethod
    def patch(fleet_id):
        body = request.json
        fleet = Fleet.objects(id=fleet_id).get_or_404()
        try:
            fleet.update(**body)
            fleet.validate()
        except (OperationError, ValidationError) as e:
            print(e)
            return str(e), 400

        fleet.save()

        return Response(status=200)

    # todo: needs to be made into authenticated route
    @staticmethod
    def delete(fleet_id):
        fleet = Fleet.objects(id=fleet_id).get_or_404()
        fleet.delete()
        return Response(status=200)


class FleetVehiclesEndpoint(Resource):
    @staticmethod
    def get(fleet_id):
        fleet = Fleet.objects(id=fleet_id).get_or_404()
        vehicles = with_pagination(Vehicle, {'fleet': fleet})
        return jsonify({'vehicles': vehicles})

    # todo: needs to be made into authenticated route
    @staticmethod
    def post(fleet_id):
        fleet = Fleet.objects(id=fleet_id).get_or_404()
        body = request.json

        try:
            vehicle = Vehicle(
                fleet=fleet,
                **body
            )
        except (KeyError, ValidationError) as e:
            print(e)
            return str(e), 400

        vehicle.save()

        return {'id': vehicle.id}, 201


class VehiclesEndpoint(Resource):
    @staticmethod
    def get():
        vehicles = with_pagination(Vehicle)
        return jsonify({'vehicles': vehicles})


class VehicleEndpoint(Resource):
    @staticmethod
    def get(vehicle_id):
        vehicle = Vehicle.objects(id=vehicle_id).get_or_404()

        return jsonify(vehicle)

    # todo: needs to be made into authenticated route
    @staticmethod
    def patch(vehicle_id):
        body = request.json
        vehicle = Vehicle.objects(id=vehicle_id).get_or_404()
        try:
            vehicle.update(**body)
            vehicle.validate()
        except (OperationError, ValidationError) as e:
            print(e)
            return str(e), 400

        vehicle.save()
        return Response(status=200)

    # todo: needs to be made into authenticated route
    @staticmethod
    def delete(vehicle_id):
        vehicle = Vehicle.objects(id=vehicle_id).get_or_404()
        vehicle.delete()
        return Response(status=200)


class VehicleDispatchesEndpoint(Resource):
    @staticmethod
    def get(vehicle_id):
        vehicle = Vehicle.objects(id=vehicle_id).get_or_404()
        dispatches = with_pagination(Dispatch, {'vehicle': vehicle})
        return jsonify({'dispatches': dispatches})


class DispatchesEndpoint(Resource):
    @staticmethod
    def get():
        dispatches = with_pagination(Dispatch)
        return jsonify({'dispatches': dispatches})

    # todo: needs to be made into authenticated route
    @staticmethod
    def post():
        order = request.json

        try:
            dispatch = Dispatch(**order)
        except (KeyError, ValidationError) as e:
            print(e)
            return str(e), 400

        # Performing an aggregate query on Mongo doesn't return Document instances. instead, it returns python dicts,
        # which doesn't give us access to the functions and utilities a Document would give us, so we
        # need to do two reads on the database
        random_fleet_id = Fleet.objects.aggregate({"$sample": {"size": 1}}).next()['_id']
        random_fleet = Fleet.objects(id=random_fleet_id).first()

        vehicle_eta_pair = random_fleet.get_vehicle_from_order(order)

        if vehicle_eta_pair is None:
            return {'error': 'No vehicles available.'}
        else:
            vehicle, eta = vehicle_eta_pair

        vehicle.set_route_from_order(order)
        vehicle.set_dispatch(dispatch)
        vehicle.job_status = JobStatus.IN_PROGRESS

        dispatch.save()
        vehicle.save()

        return jsonify({'vehicle': vehicle, 'eta': eta})
