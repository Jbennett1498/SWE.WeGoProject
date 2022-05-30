from flask import Flask, request
from flask_cors import CORS
from mongoengine import ValidationError

from demand.order import Order


def setup_app(app):
    from demand.order import db
    db.init_app(app)

    CORS(app)

    @app.post('/demand/order')
    def order():
        # takes in information
        body = request.json
        # add in all user input and saves it
        # return success if True and returns vehicle information, else Fail
        orderForm = Order()
        orderForm.phone_number = body['number']
        orderForm.address = body['address']
        orderForm.city = body['city']
        orderForm.state = body['state']
        orderForm.zip = body['zip']
        try:
            orderForm.save()
        except ValidationError as e:
            return {'error': e}
        orderForm.orderReq()

        if isinstance(orderForm, bool):
            return {'status': orderForm}
        elif isinstance(orderForm, dict):
            return orderForm
        else:
            return {}

    return app


def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'demand',
        'username': 'demand',
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
