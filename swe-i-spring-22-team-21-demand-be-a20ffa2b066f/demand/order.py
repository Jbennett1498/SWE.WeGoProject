import requests
from flask_mongoengine import Document, MongoEngine
from mongoengine import StringField, IntField

db = MongoEngine()


class Order(Document):
    # adds in all the order form information into db
    phone_number = StringField(required=True)
    address = StringField(max_length=150, required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    zip = IntField(required=True)

    # sends request to supply / dispatches and returns response
    def orderReq(self):
        r = requests.post('https://supply.team21.sweispring22.gq/supply/dispatches')
        return r.json()
