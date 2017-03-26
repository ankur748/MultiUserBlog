from google.appengine.ext import db
from models import User,Post

class Comment(db.Model):
    post    = db.ReferenceProperty(Post, collection_name = 'comment_post', required = True)
    user    = db.ReferenceProperty(User, collection_name = 'comment_user', required = True)
    comment = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    edited  = db.DateTimeProperty(auto_now = True)

    @classmethod
    def comment_post(cls, post_id, user_id, comment):
        post = Post.find_by_id(post_id)
        user = User.find_by_id(int(user_id))
        return Comment(post=post, user=user, comment=comment)

    @classmethod
    def find_by_post(cls, post_id):
        post = Post.find_by_id(int(post_id))
        return Comment.all().filter('post = ', post.key()).order('-edited').run()

    @classmethod
    def find_by_id(cls, comment_id):
        return Comment.get_by_id(int(comment_id))
