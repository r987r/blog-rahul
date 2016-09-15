import webapp2

class User(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    salt = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
