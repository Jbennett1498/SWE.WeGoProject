from flask import Flask, request
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from common_services.user import User


def setup_app(app):
    from common_services.user import db
    db.init_app(app)

    CORS(app)

    @app.post('/common/login')
    def login():
        # takes in information
        body = request.json
        # check that user is in the DB
        grabUser = User.objects(email=body['email']).first()
        # if the user is in DB then compare the hashed passwords
        if grabUser is not None:
            info = grabUser.comparePass(body['password'])
            return {'status': 'success' if info is True else 'fail'}
        # if the user is not in DB then have the status return fail
        elif grabUser is None:
            return {'status': 'fail'}

    @app.post('/common/signup')
    def signup():
        # takes in information
        body = request.json

        # add in all user input and saves it
        # return success if True, else Fail
        user = User()
        user.first_name = body['firstName']
        user.last_name = body['lastName']
        user.date_of_birth = body['DoB']
        user.email = body['email']
        user.hashPass(body['password'])
        user.save()
        return {'status': 'success' if user is True else 'fail'}

    return app


def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'common-services',
        'username': 'common-services',
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
