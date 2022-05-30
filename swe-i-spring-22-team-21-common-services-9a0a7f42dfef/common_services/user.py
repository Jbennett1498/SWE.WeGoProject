import hashlib
import hmac
import os

from flask_mongoengine import Document, MongoEngine
from mongoengine import StringField, DateTimeField, EmailField, BinaryField

db = MongoEngine()


class User(Document):
    # store all inputs in mongodb
    first_name = StringField(max_length=50, required=True, regex=r'^[A-Za-z]+$')
    last_name = StringField(max_length=50, required=True, regex=r'^[A-Za-z]+$')
    date_of_birth = DateTimeField(required=True)
    email = EmailField(unique=True, required=True)
    password = BinaryField(required=True)
    salt = BinaryField(required=True)

    # hash the given password
    def hashPass(self, password):
        # encode the password
        encoded_password = password.encode()
        # generate a random salt
        salt = os.urandom(16)
        # hash the encoded password with the salt
        password_hash = hashlib.pbkdf2_hmac("sha256", encoded_password, salt, 100000)
        # store the new hashed password and the salt
        self.password = password_hash
        self.salt = salt

    # compare given password with the password in db
    def comparePass(self, password):
        # encode the password and hash it with the salt
        encoded_password = password.encode()
        password_hash = hashlib.pbkdf2_hmac("sha256", encoded_password, self.salt, 100000)
        # compare the two passwords to see that they are correct
        if hmac.compare_digest(password_hash, self.password):
            return True
        else:
            return False
