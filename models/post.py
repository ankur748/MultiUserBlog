from google.appengine.ext import db
from models import User

class Post(db.Model):
    subject     = db.StringProperty(required = True)
    content     = db.TextProperty(required = True)
    user        = db.ReferenceProperty(User, collection_name = 'post_user', required = True)
    created     = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def find_latest_posts(cls, length=10):
        posts =  Post.all().order('-created').fetch(length)
        return posts

    @classmethod
    def find_by_user(cls, user_id):
        user = User.find_by_id(int(user_id))
        posts = Post.all().filter('user = ', user.key()).order('-created')
        return posts

    @classmethod
    def find_by_id(cls, postid):
        return Post.get_by_id(int(postid))

    @classmethod
    def save_new_post(cls, subject, content,user_id):
        user = User.find_by_id(int(user_id))
        return Post(subject=subject,content=content,user=user)
