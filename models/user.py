from google.appengine.ext import db

class User(db.Model):
    username        = db.StringProperty(required = True)
    password_hash   = db.StringProperty(required = True)
    email           = db.StringProperty()
    created         = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def find_by_id(cls, userid):
        return User.get_by_id(userid)

    @classmethod
    def find_by_name(cls, name):
        return User.all().filter('username =', name.strip()).get()

    @classmethod
    def register_new_user(cls, username, password_hash, email=None):
        return User(username=username,password_hash=password_hash,email=email)
