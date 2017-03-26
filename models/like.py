from google.appengine.ext import db
from models import User,Post

class Like(db.Model):
    post    = db.ReferenceProperty(Post, collection_name = 'post', required = True)
    user    = db.ReferenceProperty(User, collection_name = 'like_user', required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def like_post(cls, post_id, user_id):
        post = Post.find_by_id(post_id)
        user = User.find_by_id(int(user_id))
        return Like(post=post, user=user)

    @classmethod
    def get_like(cls, post_id, user_id):
        post = Post.find_by_id(post_id)
        user = User.find_by_id(int(user_id))
        like = Like.all().filter('post = ', post.key()).filter('user = ', user.key()).get()

        return like
