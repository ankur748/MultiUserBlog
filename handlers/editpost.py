from handlers import BlogHandler
from models import Post
import time
import helpers.decorators as decorators

user_logged_in      = decorators.user_logged_in
post_exists         = decorators.post_exists
user_owns_post      = decorators.user_owns_post

class EditPost(BlogHandler):

    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self, post_id, post):
        self.render('edit_post.html',post=post,logged_in=True)

    @user_logged_in
    @post_exists
    @user_owns_post
    def post(self, post_id, post):

        subject   = self.request.get("subject")
        content   = self.request.get("content")

        post.subject = subject
        post.content = content
        post.put()
        time.sleep(0.1)

        self.redirect('/blogpost/%s' % str(post.key().id()))
