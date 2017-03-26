import random
import string
import hmac

from handlers import Handler
from models import *

SECRET      = "EcstasyBlogSecret" #secret used for cookie hashing

#salt generation used for password hashing
def generate_salt(length=5):
    return ''.join(random.choice(string.letters) for i in range(length))

#hash the given password with a salt used in sign up and password verification
def hash_password(password, salt=""):
    if not salt:
        salt = generate_salt()
    password_hash = str(hash_str(password, salt))
    return '%s|%s' % (password_hash,salt)

#used in both cookie and password hash generation
def hash_str(s, salt):
    return hmac.new(str(salt),str(s)).hexdigest()

#used for cookie generation
def make_secure_val(s, salt=SECRET):
    return '%s|%s' % (s,hash_str(s,salt))

#used for cookie verification
def check_secure_val(s, salt=SECRET):
    val = s.split('|')[0]
    if (s == make_secure_val(val,salt)):
        return val
    else:
        return None

def valid_password_hash(password_hash, password):

    salt = password_hash.split('|')[1]
    return password_hash == hash_password(password, salt)

class BlogHandler(Handler):

    def logout(self):
        userid = self.request.cookies.get("userid")
        if userid:
            self.response.headers.add_header('Set-Cookie', 'userid=; Path=/')

    def login(self, user):
        if user:
            user_id = user.key().id()
            self.response.headers.add_header('Set-Cookie', 'userid=%s; Path=/' % str(make_secure_val(user_id)))

    def is_cookie_valid(self):
        userid = self.request.cookies.get("userid")
        return userid and check_secure_val(userid)

    def get_user_id(self):
        userid = self.request.cookies.get("userid")
        if userid:
            return userid.split('|')[0]

    def is_post_owner(self,post):
        user_id         = self.get_user_id()
        if post:
            post_user_id    = str(post.user.key().id())
            return post_user_id == user_id
        else:
            return False

    def is_comment_owner(self,comment):
        user_id         = self.get_user_id()
        if comment:
            comment_user_id    = str(comment.user.key().id())
            return comment_user_id == user_id
        else:
            return False

    def hash_password(self, password):
        return hash_password(password)

    def valid_password_hash(self, db_hash, password):
        return valid_password_hash(db_hash, password)
