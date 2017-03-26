from handlers import BlogHandler
from models import Post
import time
import helpers.decorators as decorators

user_logged_in      = decorators.user_logged_in
post_exists         = decorators.post_exists
user_owns_post      = decorators.user_owns_post

class DeletePost(BlogHandler):

    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self, post_id, post):
        self.render('delete_post.html',post=post,logged_in=True)

    @user_logged_in
    @post_exists
    @user_owns_post
    def post(self, post_id, post):
        post.delete()
        time.sleep(0.1)
        self.redirect('/')
