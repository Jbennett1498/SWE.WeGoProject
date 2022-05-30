from flask import Flask
from flask_cors import CORS

from supply.resources import FleetsEndpoint, FleetEndpoint, FleetVehiclesEndpoint, VehiclesEndpoint, VehicleEndpoint, \
    VehicleDispatchesEndpoint, DispatchesEndpoint


def setup_app(app):
    from supply.models import db
    db.init_app(app)

    from supply.resources import api
    api.add_resource(FleetsEndpoint, '/fleets')
    api.add_resource(FleetEndpoint, '/fleets/<fleet_id>')
    api.add_resource(FleetVehiclesEndpoint, '/fleets/<fleet_id>/vehicles')
    api.add_resource(VehiclesEndpoint, '/vehicles')
    api.add_resource(VehicleEndpoint, '/vehicles/<vehicle_id>')
    api.add_resource(VehicleDispatchesEndpoint, '/vehicles/<vehicle_id>/dispatches')
    api.add_resource(DispatchesEndpoint, '/dispatches')

    api.init_app(app)

    CORS(app)

    return app


def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'supply',
        'username': 'supply',
        'password': 'password'
    }

    return setup_app(app)


def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MONGODB_SETTINGS'] = {
        'db': 'mongoenginetest',
        'host': 'mongomock://localhost'
    }

    return setup_app(app)
