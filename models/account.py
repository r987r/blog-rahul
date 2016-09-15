from google.appengine.ext import db
import re
import hashlib
import random
import string

hash_seed = "vumb;gtink2;rahul;twenty"


class User(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    salt = db.StringProperty(required=True)
    email = db.StringProperty(required=False)

    @staticmethod
    def make_salt():
        return ''.join(random.choice(string.letters) for x in xrange(5))

    @staticmethod
    def make_pw_hash(name, pw):
        salt = User.make_salt()
        h = hashlib.sha256(hash_seed + name + pw + salt).hexdigest()
        return h, salt

    @staticmethod
    def valid_pw(name, pw, salt, check_hash):
        if(hashlib.sha256(hash_seed + name + pw + salt).hexdigest() == check_hash):
            return True
        else:
            return False

    @staticmethod
    def lookup_user(username):
        return User.all().filter('username =', username).get()

    @staticmethod
    def check_credentials(username, password):
        user = User.lookup_user(username)
        if(user and User.valid_pw(username, password, user.salt, user.pw_hash)):
            return user.pw_hash

    @staticmethod
    def make_user(username, password, email):
        pw_hash, salt = User.make_pw_hash(username, password)
        return User(username=username,
                    pw_hash=pw_hash,
                    email=email,
                    salt=salt)
